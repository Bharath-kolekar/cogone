"""
Goal Integrity Service for Voice-to-App SaaS Platform
Maintains goal integrity during system activities and user interactions
"""

import structlog
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta
import uuid
import asyncio
from dataclasses import dataclass

from app.core.config import settings
from app.core.database import get_supabase_client
from app.models.goal_integrity import (
    GoalDefinition, GoalState, GoalViolation, GoalCheckpoint,
    GoalRecoveryAction, GoalIntegrityReport, GoalIntegrityRequest,
    GoalIntegrityResponse, GoalIntegrityConfig, GoalIntegrityMetrics,
    GoalIntegrityAlert, GoalIntegrityAuditLog,
    GoalType, GoalStatus, GoalPriority, IntegrityLevel
)

logger = structlog.get_logger()


@dataclass
class GoalIntegrityContext:
    """Context for goal integrity operations"""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    operation_type: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class GoalIntegrityService:
    """Service for maintaining goal integrity throughout the system"""
    
    def __init__(self):
        try:
            self.supabase = get_supabase_client()
        except RuntimeError:
            # Database not initialized yet, will be set later
            self.supabase = None
        self.config = GoalIntegrityConfig()
        self._active_goals: Dict[str, GoalDefinition] = {}
        self._goal_states: Dict[str, GoalState] = {}
        self._integrity_checkpoints: List[GoalCheckpoint] = []
        self._recovery_queue: List[GoalRecoveryAction] = []
    
    def _ensure_supabase_connected(self):
        """Ensure Supabase connection is available"""
        if self.supabase is None:
            try:
                self.supabase = get_supabase_client()
            except RuntimeError:
                raise RuntimeError("Database not initialized. Call init_db() first.")
        
    async def initialize(self):
        """Initialize the goal integrity system"""
        try:
            await self._load_active_goals()
            await self._load_goal_states()
            logger.info("Goal integrity service initialized", 
                       goals_loaded=len(self._active_goals))
        except Exception as e:
            logger.error("Failed to initialize goal integrity service", error=str(e))
            raise

    async def _load_active_goals(self):
        """Load active goals from database"""
        try:
            self._ensure_supabase_connected()
            result = self.supabase.table("goal_definitions").select("*").eq("is_active", True).execute()
            
            for goal_data in result.data:
                goal = GoalDefinition(**goal_data)
                self._active_goals[goal.id] = goal
                
        except Exception as e:
            logger.error("Failed to load active goals", error=str(e))
            raise

    async def _load_goal_states(self):
        """Load current goal states from database"""
        try:
            self._ensure_supabase_connected()
            result = self.supabase.table("goal_states").select("*").execute()
            
            for state_data in result.data:
                state = GoalState(**state_data)
                self._goal_states[state.goal_id] = state
                
        except Exception as e:
            logger.error("Failed to load goal states", error=str(e))
            raise

    async def register_goal(self, goal_definition: GoalDefinition, context: GoalIntegrityContext = None) -> str:
        """Register a new goal for integrity monitoring"""
        try:
            self._ensure_supabase_connected()
            goal_definition.id = str(uuid.uuid4())
            goal_definition.created_at = datetime.utcnow()
            goal_definition.updated_at = datetime.utcnow()
            
            # Store in database
            goal_data = goal_definition.dict()
            self.supabase.table("goal_definitions").insert(goal_data).execute()
            
            # Initialize goal state
            initial_state = GoalState(
                goal_id=goal_definition.id,
                status=GoalStatus.ACTIVE,
                integrity_score=1.0,
                last_verified=datetime.utcnow(),
                violation_count=0,
                recovery_attempts=0
            )
            
            state_data = initial_state.dict()
            self.supabase.table("goal_states").insert(state_data).execute()
            
            # Add to active goals
            self._active_goals[goal_definition.id] = goal_definition
            self._goal_states[goal_definition.id] = initial_state
            
            # Log the registration
            await self._log_activity("goal_registered", goal_definition.id, context, {
                "goal_name": goal_definition.name,
                "goal_type": goal_definition.goal_type,
                "priority": goal_definition.priority
            })
            
            logger.info("Goal registered successfully", 
                       goal_id=goal_definition.id, 
                       goal_name=goal_definition.name)
            
            return goal_definition.id
            
        except Exception as e:
            logger.error("Failed to register goal", error=str(e))
            raise

    async def verify_goal_integrity(self, goal_id: str, context: GoalIntegrityContext = None) -> bool:
        """Verify integrity of a specific goal"""
        try:
            if goal_id not in self._active_goals:
                logger.warning("Goal not found for integrity verification", goal_id=goal_id)
                return False
            
            goal = self._active_goals[goal_id]
            state = self._goal_states.get(goal_id)
            
            if not state:
                logger.warning("Goal state not found", goal_id=goal_id)
                return False
            
            # Perform integrity verification based on goal type and criteria
            integrity_verified = await self._perform_integrity_check(goal, state, context)
            
            # Create checkpoint
            checkpoint = GoalCheckpoint(
                id=str(uuid.uuid4()),
                goal_id=goal_id,
                checkpoint_name=f"integrity_verification_{datetime.utcnow().isoformat()}",
                expected_state=goal.success_criteria,
                actual_state=state.metadata,
                integrity_verified=integrity_verified,
                timestamp=datetime.utcnow(),
                verification_method="automated_check"
            )
            
            # Store checkpoint
            checkpoint_data = checkpoint.dict()
            self.supabase.table("goal_checkpoints").insert(checkpoint_data).execute()
            
            # Update goal state
            if integrity_verified:
                state.status = GoalStatus.MAINTAINED
                state.integrity_score = min(1.0, state.integrity_score + 0.1)
            else:
                state.status = GoalStatus.COMPROMISED
                state.integrity_score = max(0.0, state.integrity_score - 0.2)
                state.violation_count += 1
                
                # Record violation
                await self._record_violation(goal_id, "integrity_check_failed", 
                                           GoalPriority.MEDIUM, context)
            
            state.last_verified = datetime.utcnow()
            
            # Update database
            state_data = state.dict()
            self.supabase.table("goal_states").update(state_data).eq("goal_id", goal_id).execute()
            
            # Log verification
            await self._log_activity("goal_verified", goal_id, context, {
                "integrity_verified": integrity_verified,
                "integrity_score": state.integrity_score
            })
            
            return integrity_verified
            
        except Exception as e:
            logger.error("Failed to verify goal integrity", goal_id=goal_id, error=str(e))
            return False

    async def _perform_integrity_check(self, goal: GoalDefinition, state: GoalState, 
                                     context: GoalIntegrityContext = None) -> bool:
        """Perform the actual integrity check based on goal type"""
        try:
            if goal.goal_type == GoalType.USER_OBJECTIVE:
                return await self._check_user_objective_integrity(goal, state, context)
            elif goal.goal_type == GoalType.SYSTEM_GOAL:
                return await self._check_system_goal_integrity(goal, state, context)
            elif goal.goal_type == GoalType.BUSINESS_GOAL:
                return await self._check_business_goal_integrity(goal, state, context)
            elif goal.goal_type == GoalType.SECURITY_GOAL:
                return await self._check_security_goal_integrity(goal, state, context)
            elif goal.goal_type == GoalType.PERFORMANCE_GOAL:
                return await self._check_performance_goal_integrity(goal, state, context)
            else:
                return await self._check_generic_goal_integrity(goal, state, context)
                
        except Exception as e:
            logger.error("Failed to perform integrity check", 
                        goal_id=goal.id, error=str(e))
            return False

    async def _check_user_objective_integrity(self, goal: GoalDefinition, state: GoalState, 
                                            context: GoalIntegrityContext = None) -> bool:
        """Check integrity of user objectives"""
        # Verify user session is valid and active
        if context and context.user_id:
            user_active = await self._verify_user_activity(context.user_id)
            if not user_active:
                return False
        
        # Check if user objectives are being met
        success_criteria = goal.success_criteria
        required_response_time = success_criteria.get("max_response_time", 30)
        required_success_rate = success_criteria.get("min_success_rate", 0.95)
        
        # Get recent metrics
        metrics = await self._get_recent_metrics(goal.id)
        actual_response_time = metrics.get("avg_response_time", 0)
        actual_success_rate = metrics.get("success_rate", 0)
        
        return (actual_response_time <= required_response_time and 
                actual_success_rate >= required_success_rate)

    async def _check_system_goal_integrity(self, goal: GoalDefinition, state: GoalState, 
                                         context: GoalIntegrityContext = None) -> bool:
        """Check integrity of system goals"""
        success_criteria = goal.success_criteria
        
        # Check system health metrics
        system_health = await self._get_system_health()
        
        required_uptime = success_criteria.get("min_uptime", 0.99)
        required_performance = success_criteria.get("min_performance", 0.8)
        
        return (system_health.get("uptime", 0) >= required_uptime and
                system_health.get("performance_score", 0) >= required_performance)

    async def _check_business_goal_integrity(self, goal: GoalDefinition, state: GoalState, 
                                           context: GoalIntegrityContext = None) -> bool:
        """Check integrity of business goals"""
        success_criteria = goal.success_criteria
        
        # Check business metrics
        business_metrics = await self._get_business_metrics()
        
        required_revenue = success_criteria.get("min_revenue", 0)
        required_customer_satisfaction = success_criteria.get("min_customer_satisfaction", 0.8)
        
        return (business_metrics.get("revenue", 0) >= required_revenue and
                business_metrics.get("customer_satisfaction", 0) >= required_customer_satisfaction)

    async def _check_security_goal_integrity(self, goal: GoalDefinition, state: GoalState, 
                                           context: GoalIntegrityContext = None) -> bool:
        """Check integrity of security goals"""
        success_criteria = goal.success_criteria
        
        # Check security metrics
        security_metrics = await self._get_security_metrics()
        
        max_failed_logins = success_criteria.get("max_failed_logins", 10)
        max_security_incidents = success_criteria.get("max_security_incidents", 0)
        
        return (security_metrics.get("failed_logins", 0) <= max_failed_logins and
                security_metrics.get("security_incidents", 0) <= max_security_incidents)

    async def _check_performance_goal_integrity(self, goal: GoalDefinition, state: GoalState, 
                                              context: GoalIntegrityContext = None) -> bool:
        """Check integrity of performance goals"""
        success_criteria = goal.success_criteria
        
        # Check performance metrics
        performance_metrics = await self._get_performance_metrics()
        
        max_response_time = success_criteria.get("max_response_time", 1000)
        min_throughput = success_criteria.get("min_throughput", 100)
        
        return (performance_metrics.get("response_time", 0) <= max_response_time and
                performance_metrics.get("throughput", 0) >= min_throughput)

    async def _check_generic_goal_integrity(self, goal: GoalDefinition, state: GoalState, 
                                          context: GoalIntegrityContext = None) -> bool:
        """Generic integrity check for other goal types"""
        # Basic integrity check based on goal constraints
        constraints = goal.constraints
        
        for constraint_key, constraint_value in constraints.items():
            current_value = state.metadata.get(constraint_key)
            if current_value is None:
                continue
                
            # Check if constraint is violated
            if isinstance(constraint_value, dict):
                min_value = constraint_value.get("min")
                max_value = constraint_value.get("max")
                
                if min_value is not None and current_value < min_value:
                    return False
                if max_value is not None and current_value > max_value:
                    return False
            else:
                if current_value != constraint_value:
                    return False
        
        return True

    async def _record_violation(self, goal_id: str, violation_type: str, severity: GoalPriority,
                              context: GoalIntegrityContext = None):
        """Record a goal violation"""
        try:
            violation = GoalViolation(
                id=str(uuid.uuid4()),
                goal_id=goal_id,
                violation_type=violation_type,
                severity=severity,
                description=f"Goal integrity violation: {violation_type}",
                context=context.metadata if context else {},
                detected_at=datetime.utcnow(),
                impact_assessment={
                    "severity": severity.value,
                    "affected_operations": [],
                    "estimated_downtime": 0
                }
            )
            
            violation_data = violation.dict()
            self.supabase.table("goal_violations").insert(violation_data).execute()
            
            # Create alert if severity is high enough
            if severity in [GoalPriority.CRITICAL, GoalPriority.HIGH]:
                await self._create_alert(goal_id, violation_type, severity, context)
            
            logger.warning("Goal violation recorded", 
                          goal_id=goal_id, 
                          violation_type=violation_type,
                          severity=severity.value)
            
        except Exception as e:
            logger.error("Failed to record violation", error=str(e))

    async def _create_alert(self, goal_id: str, alert_type: str, severity: GoalPriority,
                          context: GoalIntegrityContext = None):
        """Create an alert for goal integrity issues"""
        try:
            alert = GoalIntegrityAlert(
                id=str(uuid.uuid4()),
                alert_type=alert_type,
                severity=severity,
                goal_id=goal_id,
                title=f"Goal Integrity Alert: {alert_type}",
                description=f"Goal integrity issue detected for goal {goal_id}",
                triggered_at=datetime.utcnow(),
                metadata=context.metadata if context else {}
            )
            
            alert_data = alert.dict()
            self.supabase.table("goal_integrity_alerts").insert(alert_data).execute()
            
            logger.warning("Goal integrity alert created", 
                          goal_id=goal_id, 
                          alert_type=alert_type,
                          severity=severity.value)
            
        except Exception as e:
            logger.error("Failed to create alert", error=str(e))

    async def trigger_recovery(self, goal_id: str, context: GoalIntegrityContext = None) -> bool:
        """Trigger recovery actions for a compromised goal"""
        try:
            if goal_id not in self._active_goals:
                return False
            
            goal = self._active_goals[goal_id]
            state = self._goal_states.get(goal_id)
            
            if not state:
                return False
            
            # Check if we've exceeded max recovery attempts
            if state.recovery_attempts >= self.config.max_recovery_attempts:
                logger.error("Max recovery attempts exceeded", goal_id=goal_id)
                return False
            
            # Determine recovery actions based on goal type
            recovery_actions = await self._determine_recovery_actions(goal, state, context)
            
            # Execute recovery actions
            recovery_success = True
            for action in recovery_actions:
                action_result = await self._execute_recovery_action(action, context)
                if not action_result:
                    recovery_success = False
            
            # Update recovery attempts
            state.recovery_attempts += 1
            if recovery_success:
                state.status = GoalStatus.RECOVERING
                state.integrity_score = min(1.0, state.integrity_score + 0.3)
            else:
                state.status = GoalStatus.COMPROMISED
            
            # Update database
            state_data = state.dict()
            self.supabase.table("goal_states").update(state_data).eq("goal_id", goal_id).execute()
            
            # Log recovery attempt
            await self._log_activity("recovery_triggered", goal_id, context, {
                "recovery_success": recovery_success,
                "attempts": state.recovery_attempts
            })
            
            return recovery_success
            
        except Exception as e:
            logger.error("Failed to trigger recovery", goal_id=goal_id, error=str(e))
            return False

    async def _determine_recovery_actions(self, goal: GoalDefinition, state: GoalState,
                                        context: GoalIntegrityContext = None) -> List[GoalRecoveryAction]:
        """Determine appropriate recovery actions for a goal"""
        actions = []
        
        if goal.goal_type == GoalType.SYSTEM_GOAL:
            # System recovery actions
            actions.append(GoalRecoveryAction(
                id=str(uuid.uuid4()),
                goal_id=goal.id,
                action_type="restart_service",
                description="Restart affected services",
                parameters={"services": ["auth", "voice", "ai"]},
                executed_at=datetime.utcnow(),
                success=False  # Will be updated after execution
            ))
        
        elif goal.goal_type == GoalType.SECURITY_GOAL:
            # Security recovery actions
            actions.append(GoalRecoveryAction(
                id=str(uuid.uuid4()),
                goal_id=goal.id,
                action_type="security_scan",
                description="Run security scan and patch vulnerabilities",
                parameters={"scan_type": "full"},
                executed_at=datetime.utcnow(),
                success=False
            ))
        
        elif goal.goal_type == GoalType.PERFORMANCE_GOAL:
            # Performance recovery actions
            actions.append(GoalRecoveryAction(
                id=str(uuid.uuid4()),
                goal_id=goal.id,
                action_type="scale_resources",
                description="Scale system resources",
                parameters={"scale_factor": 1.5},
                executed_at=datetime.utcnow(),
                success=False
            ))
        
        return actions

    async def _execute_recovery_action(self, action: GoalRecoveryAction, 
                                     context: GoalIntegrityContext = None) -> bool:
        """Execute a recovery action"""
        try:
            # Store action in database
            action_data = action.dict()
            self.supabase.table("goal_recovery_actions").insert(action_data).execute()
            
            # Simulate action execution (in real implementation, this would call actual recovery methods)
            await asyncio.sleep(0.1)  # Simulate processing time
            
            # Mark action as successful (in real implementation, check actual results)
            action.success = True
            action.result = {"status": "completed", "timestamp": datetime.utcnow().isoformat()}
            
            # Update database
            self.supabase.table("goal_recovery_actions").update(
                action.dict()
            ).eq("id", action.id).execute()
            
            logger.info("Recovery action executed", 
                       action_id=action.id, 
                       action_type=action.action_type,
                       success=action.success)
            
            return True
            
        except Exception as e:
            logger.error("Failed to execute recovery action", 
                        action_id=action.id, error=str(e))
            action.success = False
            action.result = {"error": str(e)}
            return False

    async def get_integrity_report(self, request: GoalIntegrityRequest) -> GoalIntegrityReport:
        """Generate a comprehensive goal integrity report"""
        try:
            report_id = str(uuid.uuid4())
            
            # Get goals to include in report
            goals_to_check = []
            if request.verify_all:
                goals_to_check = list(self._active_goals.keys())
            elif request.goal_ids:
                goals_to_check = request.goal_ids
            else:
                goals_to_check = list(self._active_goals.keys())
            
            # Filter goals by criteria
            filtered_goals = []
            for goal_id in goals_to_check:
                if goal_id in self._active_goals:
                    goal = self._active_goals[goal_id]
                    if request.integrity_level and goal.integrity_level != request.integrity_level:
                        continue
                    if request.priority_filter and goal.priority != request.priority_filter:
                        continue
                    filtered_goals.append(goal)
            
            # Calculate overall integrity score
            total_score = 0
            goal_summaries = []
            violations_summary = {"critical": 0, "high": 0, "medium": 0, "low": 0}
            recovery_actions_summary = {"successful": 0, "failed": 0}
            
            for goal in filtered_goals:
                state = self._goal_states.get(goal.id)
                if state:
                    total_score += state.integrity_score
                    
                    goal_summaries.append({
                        "goal_id": goal.id,
                        "goal_name": goal.name,
                        "status": state.status.value,
                        "integrity_score": state.integrity_score,
                        "violation_count": state.violation_count,
                        "recovery_attempts": state.recovery_attempts
                    })
            
            overall_integrity = total_score / len(filtered_goals) if filtered_goals else 0
            
            # Get violations summary
            if request.include_violations:
                violations_result = self.supabase.table("goal_violations").select("*").execute()
                for violation in violations_result.data:
                    severity = violation.get("severity", "medium")
                    violations_summary[severity] += 1
            
            # Get recovery actions summary
            if request.include_recovery:
                recovery_result = self.supabase.table("goal_recovery_actions").select("*").execute()
                for action in recovery_result.data:
                    if action.get("success"):
                        recovery_actions_summary["successful"] += 1
                    else:
                        recovery_actions_summary["failed"] += 1
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(filtered_goals)
            
            # Generate alerts
            alerts = []
            if overall_integrity < self.config.alert_threshold:
                alerts.append(f"Overall integrity score ({overall_integrity:.2f}) is below threshold ({self.config.alert_threshold})")
            
            report = GoalIntegrityReport(
                report_id=report_id,
                generated_at=datetime.utcnow(),
                time_range={
                    "start": datetime.utcnow() - timedelta(hours=24),
                    "end": datetime.utcnow()
                },
                overall_integrity_score=overall_integrity,
                goal_summaries=goal_summaries,
                violations_summary=violations_summary,
                recovery_actions_summary=recovery_actions_summary,
                recommendations=recommendations,
                alerts=alerts
            )
            
            # Store report
            report_data = report.dict()
            self.supabase.table("goal_integrity_reports").insert(report_data).execute()
            
            return report
            
        except Exception as e:
            logger.error("Failed to generate integrity report", error=str(e))
            raise

    async def _generate_recommendations(self, goals: List[GoalDefinition]) -> List[str]:
        """Generate recommendations based on goal analysis"""
        recommendations = []
        
        for goal in goals:
            state = self._goal_states.get(goal.id)
            if not state:
                continue
            
            if state.integrity_score < 0.7:
                recommendations.append(f"Goal '{goal.name}' has low integrity score ({state.integrity_score:.2f}). Consider investigating root causes.")
            
            if state.violation_count > 5:
                recommendations.append(f"Goal '{goal.name}' has high violation count ({state.violation_count}). Review and strengthen constraints.")
            
            if state.recovery_attempts > 3:
                recommendations.append(f"Goal '{goal.name}' requires frequent recovery ({state.recovery_attempts} attempts). Consider redesigning goal criteria.")
        
        if not recommendations:
            recommendations.append("All goals are maintaining good integrity. Continue monitoring.")
        
        return recommendations

    async def _log_activity(self, action: str, goal_id: Optional[str], 
                          context: GoalIntegrityContext = None, details: Dict[str, Any] = None):
        """Log goal integrity activities"""
        try:
            log_entry = GoalIntegrityAuditLog(
                id=str(uuid.uuid4()),
                timestamp=datetime.utcnow(),
                action=action,
                goal_id=goal_id,
                user_id=context.user_id if context else None,
                session_id=context.session_id if context else None,
                details=details or {},
                result="success",
                ip_address=context.metadata.get("ip_address") if context else None,
                user_agent=context.metadata.get("user_agent") if context else None
            )
            
            log_data = log_entry.dict()
            self.supabase.table("goal_integrity_audit_logs").insert(log_data).execute()
            
        except Exception as e:
            logger.error("Failed to log activity", error=str(e))

    # Helper methods for metrics collection
    async def _verify_user_activity(self, user_id: str) -> bool:
        """Verify user activity is valid"""
        # Implementation would check user session validity
        return True

    async def _get_recent_metrics(self, goal_id: str) -> Dict[str, Any]:
        """Get recent metrics for a goal"""
        # Implementation would fetch actual metrics
        return {"avg_response_time": 25, "success_rate": 0.98}

    async def _get_system_health(self) -> Dict[str, Any]:
        """Get current system health metrics"""
        # Implementation would fetch actual system health
        return {"uptime": 0.999, "performance_score": 0.95}

    async def _get_business_metrics(self) -> Dict[str, Any]:
        """Get current business metrics"""
        # Implementation would fetch actual business metrics
        return {"revenue": 10000, "customer_satisfaction": 0.92}

    async def _get_security_metrics(self) -> Dict[str, Any]:
        """Get current security metrics"""
        # Implementation would fetch actual security metrics
        return {"failed_logins": 2, "security_incidents": 0}

    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        # Implementation would fetch actual performance metrics
        return {"response_time": 800, "throughput": 150}

    async def get_metrics(self) -> GoalIntegrityMetrics:
        """Get current goal integrity metrics"""
        try:
            total_goals = len(self._active_goals)
            active_goals = sum(1 for state in self._goal_states.values() 
                             if state.status == GoalStatus.ACTIVE)
            compromised_goals = sum(1 for state in self._goal_states.values() 
                                  if state.status == GoalStatus.COMPROMISED)
            
            avg_integrity = (sum(state.integrity_score for state in self._goal_states.values()) 
                           / len(self._goal_states)) if self._goal_states else 0
            
            # Get recent violations and recovery actions
            one_hour_ago = datetime.utcnow() - timedelta(hours=1)
            
            violations_result = self.supabase.table("goal_violations").select("*").gte(
                "detected_at", one_hour_ago.isoformat()
            ).execute()
            
            recovery_result = self.supabase.table("goal_recovery_actions").select("*").gte(
                "executed_at", one_hour_ago.isoformat()
            ).execute()
            
            metrics = GoalIntegrityMetrics(
                timestamp=datetime.utcnow(),
                total_goals=total_goals,
                active_goals=active_goals,
                compromised_goals=compromised_goals,
                average_integrity_score=avg_integrity,
                violations_last_hour=len(violations_result.data),
                recovery_actions_last_hour=len(recovery_result.data),
                system_health_score=await self._get_system_health_score(),
                uptime_percentage=99.9
            )
            
            return metrics
            
        except Exception as e:
            logger.error("Failed to get metrics", error=str(e))
            raise

    async def _get_system_health_score(self) -> float:
        """Calculate overall system health score"""
        try:
            health_metrics = await self._get_system_health()
            return (health_metrics.get("uptime", 0) + health_metrics.get("performance_score", 0)) / 2
        except Exception:
            return 0.0


# Create service instance (will be initialized when database is ready)
goal_integrity_service = None

def get_goal_integrity_service():
    """Get the goal integrity service instance, creating it if needed"""
    global goal_integrity_service
    if goal_integrity_service is None:
        # Create a lazy-loaded service that won't fail during import
        goal_integrity_service = GoalIntegrityService()
    return goal_integrity_service
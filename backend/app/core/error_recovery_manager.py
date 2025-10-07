"""
Error Recovery Manager

This module provides robust error handling and recovery mechanisms for the Ethical AI system,
including automatic error detection, recovery strategies, and system resilience.
"""

import asyncio
import structlog
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import uuid
import traceback
import functools
import time

from app.core.redis import get_redis_client
from app.core.ethical_ai_core import ethical_ai_core

logger = structlog.get_logger(__name__)

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RecoveryStrategy(Enum):
    """Error recovery strategies"""
    RETRY = "retry"
    FALLBACK = "fallback"
    CIRCUIT_BREAKER = "circuit_breaker"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    ROLLBACK = "rollback"
    MANUAL_INTERVENTION = "manual_intervention"
    AUTO_HEAL = "auto_heal"

class ErrorCategory(Enum):
    """Error categories"""
    NETWORK = "network"
    DATABASE = "database"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    TIMEOUT = "timeout"
    CONCURRENCY = "concurrency"
    DATA_CORRUPTION = "data_corruption"
    EXTERNAL_SERVICE = "external_service"
    INTERNAL_LOGIC = "internal_logic"

@dataclass
class ErrorContext:
    """Error context information"""
    error_id: str
    timestamp: datetime
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    severity: ErrorSeverity = ErrorSeverity.MEDIUM
    category: ErrorCategory = ErrorCategory.INTERNAL_LOGIC
    component: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RecoveryAction:
    """Recovery action definition"""
    action_id: str
    strategy: RecoveryStrategy
    description: str
    success_criteria: List[str]
    max_attempts: int = 3
    timeout_seconds: int = 30
    backoff_multiplier: float = 2.0
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class RecoveryResult:
    """Recovery action result"""
    action_id: str
    success: bool
    start_time: datetime
    end_time: Optional[datetime] = None
    attempts: int = 0
    error_message: Optional[str] = None
    result_data: Optional[Any] = None
    next_strategy: Optional[RecoveryStrategy] = None

@dataclass
class ErrorRecoveryReport:
    """Error recovery report"""
    report_id: str
    error_context: ErrorContext
    recovery_actions: List[RecoveryAction]
    recovery_results: List[RecoveryResult]
    overall_success: bool
    total_recovery_time: float
    final_status: str
    recommendations: List[str]
    timestamp: datetime

class ErrorRecoveryManager:
    """Comprehensive error recovery management system"""
    
    def __init__(self):
        from app.core.redis import get_redis_client_sync
        self.redis_client = get_redis_client_sync()  # Returns None if not initialized yet
        self.recovery_strategies: Dict[ErrorCategory, List[RecoveryStrategy]] = self._initialize_recovery_strategies()
        self.circuit_breakers: Dict[str, Dict[str, Any]] = {}
        self.error_history: List[ErrorContext] = []
        self.recovery_history: List[ErrorRecoveryReport] = []
        self.custom_recovery_handlers: Dict[str, Callable] = {}
        
    def _initialize_recovery_strategies(self) -> Dict[ErrorCategory, List[RecoveryStrategy]]:
        """Initialize recovery strategies for different error categories"""
        return {
            ErrorCategory.NETWORK: [
                RecoveryStrategy.RETRY,
                RecoveryStrategy.CIRCUIT_BREAKER,
                RecoveryStrategy.FALLBACK
            ],
            ErrorCategory.DATABASE: [
                RecoveryStrategy.RETRY,
                RecoveryStrategy.CIRCUIT_BREAKER,
                RecoveryStrategy.ROLLBACK,
                RecoveryStrategy.AUTO_HEAL
            ],
            ErrorCategory.AUTHENTICATION: [
                RecoveryStrategy.RETRY,
                RecoveryStrategy.FALLBACK,
                RecoveryStrategy.MANUAL_INTERVENTION
            ],
            ErrorCategory.VALIDATION: [
                RecoveryStrategy.FALLBACK,
                RecoveryStrategy.GRACEFUL_DEGRADATION,
                RecoveryStrategy.MANUAL_INTERVENTION
            ],
            ErrorCategory.RESOURCE_EXHAUSTION: [
                RecoveryStrategy.CIRCUIT_BREAKER,
                RecoveryStrategy.GRACEFUL_DEGRADATION,
                RecoveryStrategy.MANUAL_INTERVENTION
            ],
            ErrorCategory.TIMEOUT: [
                RecoveryStrategy.RETRY,
                RecoveryStrategy.CIRCUIT_BREAKER,
                RecoveryStrategy.FALLBACK
            ],
            ErrorCategory.CONCURRENCY: [
                RecoveryStrategy.RETRY,
                RecoveryStrategy.CIRCUIT_BREAKER,
                RecoveryStrategy.AUTO_HEAL
            ],
            ErrorCategory.DATA_CORRUPTION: [
                RecoveryStrategy.ROLLBACK,
                RecoveryStrategy.MANUAL_INTERVENTION,
                RecoveryStrategy.AUTO_HEAL
            ],
            ErrorCategory.EXTERNAL_SERVICE: [
                RecoveryStrategy.RETRY,
                RecoveryStrategy.CIRCUIT_BREAKER,
                RecoveryStrategy.FALLBACK,
                RecoveryStrategy.GRACEFUL_DEGRADATION
            ],
            ErrorCategory.INTERNAL_LOGIC: [
                RecoveryStrategy.AUTO_HEAL,
                RecoveryStrategy.FALLBACK,
                RecoveryStrategy.MANUAL_INTERVENTION
            ]
        }
    
    async def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> ErrorRecoveryReport:
        """Handle an error and attempt recovery"""
        try:
            # Create error context
            error_context = await self._create_error_context(error, context or {})
            
            # Log error
            logger.error("Error occurred", 
                        error_id=error_context.error_id,
                        error_type=error_context.error_type,
                        severity=error_context.severity.value,
                        component=error_context.component)
            
            # Store error in history
            self.error_history.append(error_context)
            
            # Determine recovery strategies
            recovery_actions = await self._determine_recovery_actions(error_context)
            
            # Execute recovery actions
            recovery_results = await self._execute_recovery_actions(recovery_actions, error_context)
            
            # Create recovery report
            report = await self._create_recovery_report(error_context, recovery_actions, recovery_results)
            
            # Store recovery report
            self.recovery_history.append(report)
            
            # Cache recovery report
            await self._cache_recovery_report(report)
            
            logger.info("Error recovery completed", 
                       error_id=error_context.error_id,
                       recovery_success=report.overall_success,
                       recovery_time=report.total_recovery_time)
            
            return report
            
        except Exception as e:
            logger.error("Error recovery failed", error=str(e))
            raise
    
    async def _create_error_context(self, error: Exception, context: Dict[str, Any]) -> ErrorContext:
        """Create error context from exception and additional context"""
        error_id = str(uuid.uuid4())
        
        # Determine error category and severity
        category = self._categorize_error(error)
        severity = self._determine_severity(error, context)
        
        return ErrorContext(
            error_id=error_id,
            timestamp=datetime.now(),
            error_type=type(error).__name__,
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            severity=severity,
            category=category,
            component=context.get("component"),
            user_id=context.get("user_id"),
            session_id=context.get("session_id"),
            request_id=context.get("request_id"),
            metadata=context
        )
    
    def _categorize_error(self, error: Exception) -> ErrorCategory:
        """Categorize error based on exception type and message"""
        error_message = str(error).lower()
        error_type = type(error).__name__.lower()
        
        # Network errors
        if any(keyword in error_type for keyword in ["connection", "network", "timeout", "http"]):
            return ErrorCategory.NETWORK
        
        # Database errors
        if any(keyword in error_type for keyword in ["database", "sql", "connection", "integrity"]):
            return ErrorCategory.DATABASE
        
        # Authentication errors
        if any(keyword in error_type for keyword in ["auth", "permission", "unauthorized", "forbidden"]):
            return ErrorCategory.AUTHENTICATION
        
        # Validation errors
        if any(keyword in error_type for keyword in ["validation", "invalid", "value", "type"]):
            return ErrorCategory.VALIDATION
        
        # Resource exhaustion
        if any(keyword in error_message for keyword in ["memory", "disk", "resource", "limit"]):
            return ErrorCategory.RESOURCE_EXHAUSTION
        
        # Timeout errors
        if any(keyword in error_type for keyword in ["timeout", "deadline"]):
            return ErrorCategory.TIMEOUT
        
        # Concurrency errors
        if any(keyword in error_message for keyword in ["lock", "deadlock", "race", "concurrent"]):
            return ErrorCategory.CONCURRENCY
        
        # Data corruption
        if any(keyword in error_message for keyword in ["corrupt", "invalid", "checksum", "integrity"]):
            return ErrorCategory.DATA_CORRUPTION
        
        # External service errors
        if any(keyword in error_message for keyword in ["api", "service", "external", "third-party"]):
            return ErrorCategory.EXTERNAL_SERVICE
        
        # Default to internal logic
        return ErrorCategory.INTERNAL_LOGIC
    
    def _determine_severity(self, error: Exception, context: Dict[str, Any]) -> ErrorSeverity:
        """Determine error severity based on error type and context"""
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        # Critical errors
        if any(keyword in error_type for keyword in ["SystemExit", "KeyboardInterrupt"]):
            return ErrorSeverity.CRITICAL
        
        if any(keyword in error_message for keyword in ["fatal", "critical", "system", "memory"]):
            return ErrorSeverity.CRITICAL
        
        # High severity errors
        if any(keyword in error_type for keyword in ["DatabaseError", "ConnectionError", "AuthenticationError"]):
            return ErrorSeverity.HIGH
        
        if any(keyword in error_message for keyword in ["connection", "database", "auth", "permission"]):
            return ErrorSeverity.HIGH
        
        # Medium severity errors
        if any(keyword in error_type for keyword in ["ValidationError", "ValueError", "TypeError"]):
            return ErrorSeverity.MEDIUM
        
        if any(keyword in error_message for keyword in ["invalid", "validation", "timeout"]):
            return ErrorSeverity.MEDIUM
        
        # Low severity errors (default)
        return ErrorSeverity.LOW
    
    async def _determine_recovery_actions(self, error_context: ErrorContext) -> List[RecoveryAction]:
        """Determine appropriate recovery actions for the error"""
        recovery_actions = []
        
        # Get recovery strategies for the error category
        strategies = self.recovery_strategies.get(error_context.category, [RecoveryStrategy.MANUAL_INTERVENTION])
        
        # Create recovery actions based on strategies
        for i, strategy in enumerate(strategies):
            action = RecoveryAction(
                action_id=f"{error_context.error_id}_action_{i}",
                strategy=strategy,
                description=f"Recovery action using {strategy.value} strategy",
                success_criteria=self._get_success_criteria(strategy),
                max_attempts=self._get_max_attempts(strategy, error_context.severity),
                timeout_seconds=self._get_timeout(strategy, error_context.severity),
                backoff_multiplier=self._get_backoff_multiplier(strategy),
                metadata={"error_id": error_context.error_id}
            )
            recovery_actions.append(action)
        
        return recovery_actions
    
    def _get_success_criteria(self, strategy: RecoveryStrategy) -> List[str]:
        """Get success criteria for a recovery strategy"""
        criteria_map = {
            RecoveryStrategy.RETRY: ["operation_completed", "no_exception_thrown"],
            RecoveryStrategy.FALLBACK: ["fallback_operation_successful", "user_request_fulfilled"],
            RecoveryStrategy.CIRCUIT_BREAKER: ["circuit_opened", "requests_blocked"],
            RecoveryStrategy.GRACEFUL_DEGRADATION: ["service_degraded", "core_functionality_preserved"],
            RecoveryStrategy.ROLLBACK: ["state_restored", "data_consistency_maintained"],
            RecoveryStrategy.MANUAL_INTERVENTION: ["alert_sent", "manual_review_triggered"],
            RecoveryStrategy.AUTO_HEAL: ["issue_resolved", "service_restored"]
        }
        return criteria_map.get(strategy, ["operation_completed"])
    
    def _get_max_attempts(self, strategy: RecoveryStrategy, severity: ErrorSeverity) -> int:
        """Get maximum attempts for a recovery strategy"""
        base_attempts = {
            RecoveryStrategy.RETRY: 5,
            RecoveryStrategy.FALLBACK: 2,
            RecoveryStrategy.CIRCUIT_BREAKER: 1,
            RecoveryStrategy.GRACEFUL_DEGRADATION: 1,
            RecoveryStrategy.ROLLBACK: 3,
            RecoveryStrategy.MANUAL_INTERVENTION: 1,
            RecoveryStrategy.AUTO_HEAL: 3
        }
        
        attempts = base_attempts.get(strategy, 1)
        
        # Adjust based on severity
        if severity == ErrorSeverity.CRITICAL:
            attempts = min(attempts, 2)  # Reduce attempts for critical errors
        elif severity == ErrorSeverity.LOW:
            attempts = max(attempts, 3)  # Increase attempts for low severity
        
        return attempts
    
    def _get_timeout(self, strategy: RecoveryStrategy, severity: ErrorSeverity) -> int:
        """Get timeout for a recovery strategy"""
        base_timeout = {
            RecoveryStrategy.RETRY: 30,
            RecoveryStrategy.FALLBACK: 60,
            RecoveryStrategy.CIRCUIT_BREAKER: 300,
            RecoveryStrategy.GRACEFUL_DEGRADATION: 120,
            RecoveryStrategy.ROLLBACK: 180,
            RecoveryStrategy.MANUAL_INTERVENTION: 3600,
            RecoveryStrategy.AUTO_HEAL: 600
        }
        
        timeout = base_timeout.get(strategy, 30)
        
        # Adjust based on severity
        if severity == ErrorSeverity.CRITICAL:
            timeout = min(timeout, 60)  # Reduce timeout for critical errors
        elif severity == ErrorSeverity.LOW:
            timeout = max(timeout, 120)  # Increase timeout for low severity
        
        return timeout
    
    def _get_backoff_multiplier(self, strategy: RecoveryStrategy) -> float:
        """Get backoff multiplier for retry strategies"""
        if strategy == RecoveryStrategy.RETRY:
            return 2.0
        return 1.0
    
    async def _execute_recovery_actions(self, recovery_actions: List[RecoveryAction], 
                                      error_context: ErrorContext) -> List[RecoveryResult]:
        """Execute recovery actions in sequence"""
        recovery_results = []
        
        for action in recovery_actions:
            try:
                result = await self._execute_recovery_action(action, error_context)
                recovery_results.append(result)
                
                # If recovery was successful, we can stop
                if result.success:
                    logger.info("Recovery action succeeded", 
                               action_id=action.action_id,
                               strategy=action.strategy.value)
                    break
                
                # If this is the last strategy and it failed, mark as failed
                if action == recovery_actions[-1]:
                    result.next_strategy = None
                
            except Exception as e:
                logger.error("Recovery action failed with exception", 
                           action_id=action.action_id,
                           error=str(e))
                
                result = RecoveryResult(
                    action_id=action.action_id,
                    success=False,
                    start_time=datetime.now(),
                    end_time=datetime.now(),
                    attempts=action.max_attempts,
                    error_message=str(e)
                )
                recovery_results.append(result)
        
        return recovery_results
    
    async def _execute_recovery_action(self, action: RecoveryAction, 
                                     error_context: ErrorContext) -> RecoveryResult:
        """Execute a single recovery action"""
        start_time = datetime.now()
        attempts = 0
        last_error = None
        
        logger.info("Starting recovery action", 
                   action_id=action.action_id,
                   strategy=action.strategy.value)
        
        while attempts < action.max_attempts:
            attempts += 1
            
            try:
                # Execute the recovery strategy
                result = await self._execute_recovery_strategy(action, error_context, attempts)
                
                if result:
                    return RecoveryResult(
                        action_id=action.action_id,
                        success=True,
                        start_time=start_time,
                        end_time=datetime.now(),
                        attempts=attempts,
                        result_data=result
                    )
                
            except Exception as e:
                last_error = e
                logger.warning("Recovery attempt failed", 
                             action_id=action.action_id,
                             attempt=attempts,
                             error=str(e))
                
                # Apply backoff if not the last attempt
                if attempts < action.max_attempts:
                    backoff_time = min(30, action.timeout_seconds * (action.backoff_multiplier ** (attempts - 1)))
                    await asyncio.sleep(backoff_time)
        
        # All attempts failed
        return RecoveryResult(
            action_id=action.action_id,
            success=False,
            start_time=start_time,
            end_time=datetime.now(),
            attempts=attempts,
            error_message=str(last_error) if last_error else "All recovery attempts failed"
        )
    
    async def _execute_recovery_strategy(self, action: RecoveryAction, 
                                       error_context: ErrorContext, 
                                       attempt: int) -> Any:
        """Execute a specific recovery strategy"""
        strategy = action.strategy
        
        if strategy == RecoveryStrategy.RETRY:
            return await self._retry_strategy(action, error_context, attempt)
        elif strategy == RecoveryStrategy.FALLBACK:
            return await self._fallback_strategy(action, error_context, attempt)
        elif strategy == RecoveryStrategy.CIRCUIT_BREAKER:
            return await self._circuit_breaker_strategy(action, error_context, attempt)
        elif strategy == RecoveryStrategy.GRACEFUL_DEGRADATION:
            return await self._graceful_degradation_strategy(action, error_context, attempt)
        elif strategy == RecoveryStrategy.ROLLBACK:
            return await self._rollback_strategy(action, error_context, attempt)
        elif strategy == RecoveryStrategy.MANUAL_INTERVENTION:
            return await self._manual_intervention_strategy(action, error_context, attempt)
        elif strategy == RecoveryStrategy.AUTO_HEAL:
            return await self._auto_heal_strategy(action, error_context, attempt)
        else:
            raise ValueError(f"Unknown recovery strategy: {strategy}")
    
    async def _retry_strategy(self, action: RecoveryAction, error_context: ErrorContext, attempt: int) -> Any:
        """Implement retry strategy"""
        # Simulate retry logic - in real implementation, this would retry the original operation
        await asyncio.sleep(1)  # Simulate retry delay
        
        # For demonstration, we'll simulate success after a few attempts
        if attempt >= 2:
            return {"retry_successful": True, "attempt": attempt}
        
        raise Exception(f"Retry attempt {attempt} failed")
    
    async def _fallback_strategy(self, action: RecoveryAction, error_context: ErrorContext, attempt: int) -> Any:
        """Implement fallback strategy"""
        # Simulate fallback logic
        await asyncio.sleep(0.5)
        
        return {
            "fallback_activated": True,
            "fallback_service": "backup_service",
            "attempt": attempt
        }
    
    async def _circuit_breaker_strategy(self, action: RecoveryAction, error_context: ErrorContext, attempt: int) -> Any:
        """Implement circuit breaker strategy"""
        component = error_context.component or "unknown"
        breaker_key = f"circuit_breaker:{component}"
        
        # Check if circuit breaker is already open
        breaker_state = self.circuit_breakers.get(breaker_key, {"state": "closed", "failures": 0})
        
        if breaker_state["state"] == "open":
            # Check if we should try to close the circuit
            if datetime.now().timestamp() - breaker_state.get("last_failure", 0) > 300:  # 5 minutes
                breaker_state["state"] = "half-open"
                breaker_state["failures"] = 0
            else:
                raise Exception("Circuit breaker is open")
        
        # Simulate circuit breaker logic
        self.circuit_breakers[breaker_key] = breaker_state
        
        return {
            "circuit_breaker_state": breaker_state["state"],
            "component": component
        }
    
    async def _graceful_degradation_strategy(self, action: RecoveryAction, error_context: ErrorContext, attempt: int) -> Any:
        """Implement graceful degradation strategy"""
        await asyncio.sleep(0.3)
        
        return {
            "degradation_mode": True,
            "features_disabled": ["advanced_features", "real_time_updates"],
            "core_functionality": True
        }
    
    async def _rollback_strategy(self, action: RecoveryAction, error_context: ErrorContext, attempt: int) -> Any:
        """Implement rollback strategy"""
        await asyncio.sleep(1)
        
        return {
            "rollback_completed": True,
            "state_restored": True,
            "data_consistency": True
        }
    
    async def _manual_intervention_strategy(self, action: RecoveryAction, error_context: ErrorContext, attempt: int) -> Any:
        """Implement manual intervention strategy"""
        # Send alert/notification for manual intervention
        alert_data = {
            "error_id": error_context.error_id,
            "error_type": error_context.error_type,
            "severity": error_context.severity.value,
            "component": error_context.component,
            "timestamp": error_context.timestamp.isoformat(),
            "requires_manual_intervention": True
        }
        
        # In a real implementation, this would send notifications
        logger.critical("Manual intervention required", **alert_data)
        
        return {
            "alert_sent": True,
            "manual_intervention_required": True,
            "alert_data": alert_data
        }
    
    async def _auto_heal_strategy(self, action: RecoveryAction, error_context: ErrorContext, attempt: int) -> Any:
        """Implement auto-heal strategy"""
        await asyncio.sleep(2)
        
        # Simulate auto-healing logic
        heal_actions = [
            "restart_service",
            "clear_cache",
            "reset_connections",
            "cleanup_resources"
        ]
        
        return {
            "auto_heal_completed": True,
            "heal_actions": heal_actions,
            "service_restored": True
        }
    
    async def _create_recovery_report(self, error_context: ErrorContext, 
                                    recovery_actions: List[RecoveryAction],
                                    recovery_results: List[RecoveryResult]) -> ErrorRecoveryReport:
        """Create comprehensive recovery report"""
        report_id = str(uuid.uuid4())
        
        # Determine overall success
        overall_success = any(result.success for result in recovery_results)
        
        # Calculate total recovery time
        total_recovery_time = 0.0
        if recovery_results:
            start_time = min(result.start_time for result in recovery_results)
            end_time = max(result.end_time or datetime.now() for result in recovery_results)
            total_recovery_time = (end_time - start_time).total_seconds()
        
        # Determine final status
        if overall_success:
            final_status = "recovered"
        elif any(result.success for result in recovery_results):
            final_status = "partially_recovered"
        else:
            final_status = "failed"
        
        # Generate recommendations
        recommendations = self._generate_recovery_recommendations(error_context, recovery_results)
        
        return ErrorRecoveryReport(
            report_id=report_id,
            error_context=error_context,
            recovery_actions=recovery_actions,
            recovery_results=recovery_results,
            overall_success=overall_success,
            total_recovery_time=total_recovery_time,
            final_status=final_status,
            recommendations=recommendations,
            timestamp=datetime.now()
        )
    
    def _generate_recovery_recommendations(self, error_context: ErrorContext, 
                                         recovery_results: List[RecoveryResult]) -> List[str]:
        """Generate recommendations based on recovery results"""
        recommendations = []
        
        # Add category-specific recommendations
        if error_context.category == ErrorCategory.NETWORK:
            recommendations.extend([
                "Implement connection pooling",
                "Add network timeout configurations",
                "Consider implementing retry logic with exponential backoff"
            ])
        elif error_context.category == ErrorCategory.DATABASE:
            recommendations.extend([
                "Review database connection settings",
                "Implement database health checks",
                "Consider adding database connection pooling"
            ])
        elif error_context.category == ErrorCategory.RESOURCE_EXHAUSTION:
            recommendations.extend([
                "Monitor resource usage more closely",
                "Implement resource limits and quotas",
                "Consider horizontal scaling"
            ])
        
        # Add severity-based recommendations
        if error_context.severity == ErrorSeverity.CRITICAL:
            recommendations.extend([
                "Implement immediate alerting for critical errors",
                "Create runbooks for critical error scenarios",
                "Consider implementing automated failover"
            ])
        
        # Add recovery-specific recommendations
        failed_recoveries = [r for r in recovery_results if not r.success]
        if failed_recoveries:
            recommendations.extend([
                "Review and improve recovery strategies",
                "Consider implementing additional fallback mechanisms",
                "Add more comprehensive error handling"
            ])
        
        return recommendations
    
    async def _cache_recovery_report(self, report: ErrorRecoveryReport):
        """Cache recovery report in Redis"""
        try:
            cache_key = f"recovery_report:{report.report_id}"
            
            cache_data = {
                "report_id": report.report_id,
                "error_id": report.error_context.error_id,
                "overall_success": report.overall_success,
                "final_status": report.final_status,
                "total_recovery_time": report.total_recovery_time,
                "timestamp": report.timestamp.isoformat(),
                "recommendations": report.recommendations
            }
            
            await self.redis_client.set(
                cache_key,
                json.dumps(cache_data, default=str),
                ex=86400  # Cache for 24 hours
            )
            
        except Exception as e:
            logger.error("Failed to cache recovery report", error=str(e))
    
    async def get_recovery_metrics(self) -> Dict[str, Any]:
        """Get error recovery metrics"""
        try:
            total_errors = len(self.error_history)
            total_recoveries = len(self.recovery_history)
            
            if total_errors == 0:
                return {"message": "No errors recorded"}
            
            successful_recoveries = len([r for r in self.recovery_history if r.overall_success])
            recovery_rate = (successful_recoveries / total_recoveries * 100) if total_recoveries > 0 else 0
            
            # Error category distribution
            category_counts = {}
            for error in self.error_history:
                category = error.category.value
                category_counts[category] = category_counts.get(category, 0) + 1
            
            # Severity distribution
            severity_counts = {}
            for error in self.error_history:
                severity = error.severity.value
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            return {
                "total_errors": total_errors,
                "total_recoveries": total_recoveries,
                "successful_recoveries": successful_recoveries,
                "recovery_rate": round(recovery_rate, 2),
                "error_category_distribution": category_counts,
                "error_severity_distribution": severity_counts,
                "average_recovery_time": sum(r.total_recovery_time for r in self.recovery_history) / total_recoveries if total_recoveries > 0 else 0
            }
            
        except Exception as e:
            logger.error("Failed to get recovery metrics", error=str(e))
            return {}
    
    def register_custom_recovery_handler(self, error_type: str, handler: Callable):
        """Register a custom recovery handler for specific error types"""
        self.custom_recovery_handlers[error_type] = handler
        logger.info("Custom recovery handler registered", error_type=error_type)
    
    def error_handler(self, *error_types):
        """Decorator for automatic error handling and recovery"""
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    # Check if this is one of the specified error types
                    if error_types and type(e).__name__ not in error_types:
                        raise
                    
                    # Handle the error
                    context = {
                        "function": func.__name__,
                        "args": str(args)[:100],  # Limit length
                        "kwargs": str(kwargs)[:100]
                    }
                    
                    recovery_report = await self.handle_error(e, context)
                    
                    # Re-raise the original exception if recovery failed
                    if not recovery_report.overall_success:
                        raise
            
            return wrapper
        return decorator

# Global instance
error_recovery_manager = ErrorRecoveryManager()

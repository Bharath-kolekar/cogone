"""
Consistency Enforcer

This module provides comprehensive consistency enforcement for the Ethical AI system,
including cross-system consistency validation, data integrity checks, and automated consistency maintenance.
"""

import asyncio
import structlog
from typing import Dict, List, Optional, Any, Tuple, Set, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import hashlib
import uuid
from collections import defaultdict

from app.core.redis import get_redis_client
from app.core.ethical_ai_core import ethical_ai_core

logger = structlog.get_logger(__name__)

class ConsistencyLevel(Enum):
    """Consistency enforcement levels"""
    STRICT = "strict"
    MODERATE = "moderate"
    RELAXED = "relaxed"
    CUSTOM = "custom"

class ConsistencyType(Enum):
    """Types of consistency checks"""
    DATA_CONSISTENCY = "data_consistency"
    SCHEMA_CONSISTENCY = "schema_consistency"
    BUSINESS_LOGIC_CONSISTENCY = "business_logic_consistency"
    API_CONSISTENCY = "api_consistency"
    CONFIGURATION_CONSISTENCY = "configuration_consistency"
    SECURITY_CONSISTENCY = "security_consistency"
    PERFORMANCE_CONSISTENCY = "performance_consistency"
    CROSS_SYSTEM_CONSISTENCY = "cross_system_consistency"

class ConsistencyStatus(Enum):
    """Consistency check status"""
    CONSISTENT = "consistent"
    INCONSISTENT = "inconsistent"
    WARNING = "warning"
    ERROR = "error"
    UNKNOWN = "unknown"

@dataclass
class ConsistencyRule:
    """Consistency enforcement rule"""
    rule_id: str
    name: str
    description: str
    consistency_type: ConsistencyType
    level: ConsistencyLevel
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    enabled: bool = True
    priority: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConsistencyViolation:
    """Represents a consistency violation"""
    violation_id: str
    rule_id: str
    violation_type: ConsistencyType
    severity: str
    description: str
    location: Optional[str] = None
    affected_components: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    resolution_method: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConsistencyCheck:
    """Consistency check definition"""
    check_id: str
    name: str
    description: str
    consistency_type: ConsistencyType
    target_components: List[str]
    validation_function: str
    auto_fix_enabled: bool = False
    schedule: Optional[str] = None
    enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ConsistencyReport:
    """Comprehensive consistency report"""
    report_id: str
    timestamp: datetime
    overall_consistency_score: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    warnings: int
    violations: List[ConsistencyViolation]
    recommendations: List[str]
    auto_fixes_applied: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)

class ConsistencyEnforcer:
    """Comprehensive consistency enforcement system"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
        self.consistency_rules: Dict[str, ConsistencyRule] = {}
        self.consistency_checks: Dict[str, ConsistencyCheck] = {}
        self.violations_history: List[ConsistencyViolation] = []
        self.consistency_cache: Dict[str, Any] = {}
        self.auto_fix_handlers: Dict[str, callable] = {}
        
        # Initialize built-in consistency rules and checks
        self._initialize_builtin_rules()
        self._initialize_builtin_checks()
        self._initialize_auto_fix_handlers()
    
    def _initialize_builtin_rules(self):
        """Initialize built-in consistency rules"""
        # Data consistency rules
        data_consistency_rule = ConsistencyRule(
            rule_id="data_format_consistency",
            name="Data Format Consistency",
            description="Ensures consistent data formats across all components",
            consistency_type=ConsistencyType.DATA_CONSISTENCY,
            level=ConsistencyLevel.STRICT,
            conditions=[
                {"field": "data_format", "operator": "equals", "value": "json"},
                {"field": "encoding", "operator": "equals", "value": "utf-8"}
            ],
            actions=[
                {"type": "validate_format", "params": {"format": "json"}},
                {"type": "convert_format", "params": {"target_format": "json"}}
            ],
            priority=1
        )
        self.consistency_rules[data_consistency_rule.rule_id] = data_consistency_rule
        
        # Schema consistency rules
        schema_consistency_rule = ConsistencyRule(
            rule_id="schema_consistency",
            name="Schema Consistency",
            description="Ensures consistent data schemas across all components",
            consistency_type=ConsistencyType.SCHEMA_CONSISTENCY,
            level=ConsistencyLevel.STRICT,
            conditions=[
                {"field": "schema_version", "operator": "equals", "value": "v1.0"},
                {"field": "required_fields", "operator": "contains_all", "value": ["id", "timestamp"]}
            ],
            actions=[
                {"type": "validate_schema", "params": {"schema": "v1.0"}},
                {"type": "migrate_schema", "params": {"target_version": "v1.0"}}
            ],
            priority=1
        )
        self.consistency_rules[schema_consistency_rule.rule_id] = schema_consistency_rule
        
        # API consistency rules
        api_consistency_rule = ConsistencyRule(
            rule_id="api_consistency",
            name="API Consistency",
            description="Ensures consistent API responses and error handling",
            consistency_type=ConsistencyType.API_CONSISTENCY,
            level=ConsistencyLevel.MODERATE,
            conditions=[
                {"field": "response_format", "operator": "equals", "value": "json"},
                {"field": "error_format", "operator": "matches", "value": r"\{.*error.*\}"}
            ],
            actions=[
                {"type": "standardize_response", "params": {"format": "json"}},
                {"type": "standardize_errors", "params": {"format": "standard"}}
            ],
            priority=2
        )
        self.consistency_rules[api_consistency_rule.rule_id] = api_consistency_rule
    
    def _initialize_builtin_checks(self):
        """Initialize built-in consistency checks"""
        # Data consistency checks
        data_check = ConsistencyCheck(
            check_id="data_format_check",
            name="Data Format Check",
            description="Validates data format consistency across components",
            consistency_type=ConsistencyType.DATA_CONSISTENCY,
            target_components=["database", "api", "cache"],
            validation_function="validate_data_formats",
            auto_fix_enabled=True,
            enabled=True
        )
        self.consistency_checks[data_check.check_id] = data_check
        
        # Schema consistency checks
        schema_check = ConsistencyCheck(
            check_id="schema_validation_check",
            name="Schema Validation Check",
            description="Validates schema consistency across data stores",
            consistency_type=ConsistencyType.SCHEMA_CONSISTENCY,
            target_components=["database", "api", "models"],
            validation_function="validate_schemas",
            auto_fix_enabled=True,
            enabled=True
        )
        self.consistency_checks[schema_check.check_id] = schema_check
        
        # Cross-system consistency checks
        cross_system_check = ConsistencyCheck(
            check_id="cross_system_consistency_check",
            name="Cross-System Consistency Check",
            description="Validates consistency across all system components",
            consistency_type=ConsistencyType.CROSS_SYSTEM_CONSISTENCY,
            target_components=["all"],
            validation_function="validate_cross_system_consistency",
            auto_fix_enabled=False,
            enabled=True
        )
        self.consistency_checks[cross_system_check.check_id] = cross_system_check
    
    def _initialize_auto_fix_handlers(self):
        """Initialize auto-fix handlers for different violation types"""
        self.auto_fix_handlers = {
            "data_format_fix": self._fix_data_format_violation,
            "schema_migration": self._fix_schema_violation,
            "api_standardization": self._fix_api_violation,
            "configuration_sync": self._fix_configuration_violation,
            "cache_invalidation": self._fix_cache_violation
        }
    
    async def enforce_consistency(self, target_components: List[str] = None, 
                                 consistency_types: List[ConsistencyType] = None) -> ConsistencyReport:
        """Enforce consistency across specified components and types"""
        try:
            report_id = str(uuid.uuid4())
            
            logger.info("Starting consistency enforcement", 
                       report_id=report_id,
                       target_components=target_components or ["all"],
                       consistency_types=[t.value for t in consistency_types] if consistency_types else ["all"])
            
            # Determine which checks to run
            checks_to_run = self._filter_checks(target_components, consistency_types)
            
            # Run consistency checks
            violations = []
            passed_checks = 0
            failed_checks = 0
            warnings = 0
            auto_fixes_applied = []
            
            for check in checks_to_run:
                try:
                    check_result = await self._run_consistency_check(check)
                    
                    if check_result["status"] == ConsistencyStatus.CONSISTENT:
                        passed_checks += 1
                    elif check_result["status"] == ConsistencyStatus.INCONSISTENT:
                        failed_checks += 1
                        violations.extend(check_result.get("violations", []))
                        
                        # Apply auto-fixes if enabled
                        if check.auto_fix_enabled:
                            fixes = await self._apply_auto_fixes(check_result["violations"])
                            auto_fixes_applied.extend(fixes)
                    elif check_result["status"] == ConsistencyStatus.WARNING:
                        warnings += 1
                        violations.extend(check_result.get("violations", []))
                    
                except Exception as e:
                    logger.error("Consistency check failed", 
                               check_id=check.check_id, 
                               error=str(e))
                    failed_checks += 1
            
            # Calculate overall consistency score
            total_checks = passed_checks + failed_checks + warnings
            overall_score = (passed_checks / total_checks * 100) if total_checks > 0 else 100.0
            
            # Generate recommendations
            recommendations = self._generate_consistency_recommendations(violations)
            
            # Create report
            report = ConsistencyReport(
                report_id=report_id,
                timestamp=datetime.now(),
                overall_consistency_score=overall_score,
                total_checks=total_checks,
                passed_checks=passed_checks,
                failed_checks=failed_checks,
                warnings=warnings,
                violations=violations,
                recommendations=recommendations,
                auto_fixes_applied=auto_fixes_applied,
                metadata={
                    "target_components": target_components or ["all"],
                    "consistency_types": [t.value for t in consistency_types] if consistency_types else ["all"],
                    "enforcement_duration": "calculated_after_completion"
                }
            )
            
            # Store violations in history
            self.violations_history.extend(violations)
            
            # Cache report
            await self._cache_consistency_report(report)
            
            logger.info("Consistency enforcement completed", 
                       report_id=report_id,
                       overall_score=overall_score,
                       total_checks=total_checks,
                       violations_count=len(violations))
            
            return report
            
        except Exception as e:
            logger.error("Consistency enforcement failed", error=str(e))
            raise
    
    def _filter_checks(self, target_components: List[str], 
                      consistency_types: List[ConsistencyType]) -> List[ConsistencyCheck]:
        """Filter checks based on target components and consistency types"""
        filtered_checks = []
        
        for check in self.consistency_checks.values():
            if not check.enabled:
                continue
            
            # Filter by target components
            if target_components:
                if "all" not in target_components and not any(
                    component in check.target_components or "all" in check.target_components
                    for component in target_components
                ):
                    continue
            
            # Filter by consistency types
            if consistency_types:
                if check.consistency_type not in consistency_types:
                    continue
            
            filtered_checks.append(check)
        
        return filtered_checks
    
    async def _run_consistency_check(self, check: ConsistencyCheck) -> Dict[str, Any]:
        """Run a specific consistency check"""
        try:
            # Get validation function
            validation_function = getattr(self, check.validation_function, None)
            if not validation_function:
                raise ValueError(f"Validation function {check.validation_function} not found")
            
            # Run validation
            result = await validation_function(check)
            
            return result
            
        except Exception as e:
            logger.error("Failed to run consistency check", 
                        check_id=check.check_id, 
                        error=str(e))
            
            return {
                "status": ConsistencyStatus.ERROR,
                "violations": [ConsistencyViolation(
                    violation_id=str(uuid.uuid4()),
                    rule_id=check.check_id,
                    violation_type=check.consistency_type,
                    severity="error",
                    description=f"Consistency check failed: {str(e)}",
                    metadata={"check_id": check.check_id}
                )]
            }
    
    async def validate_data_formats(self, check: ConsistencyCheck) -> Dict[str, Any]:
        """Validate data format consistency"""
        violations = []
        
        # Simulate data format validation
        # In a real implementation, this would check actual data formats across components
        
        # Check JSON format consistency
        json_format_consistent = True  # Simulated
        if not json_format_consistent:
            violations.append(ConsistencyViolation(
                violation_id=str(uuid.uuid4()),
                rule_id="data_format_consistency",
                violation_type=ConsistencyType.DATA_CONSISTENCY,
                severity="medium",
                description="Inconsistent JSON formatting detected",
                affected_components=["api", "cache"],
                metadata={"expected_format": "json", "actual_format": "mixed"}
            ))
        
        # Check encoding consistency
        encoding_consistent = True  # Simulated
        if not encoding_consistent:
            violations.append(ConsistencyViolation(
                violation_id=str(uuid.uuid4()),
                rule_id="data_format_consistency",
                violation_type=ConsistencyType.DATA_CONSISTENCY,
                severity="low",
                description="Inconsistent text encoding detected",
                affected_components=["database"],
                metadata={"expected_encoding": "utf-8", "actual_encoding": "ascii"}
            ))
        
        status = ConsistencyStatus.CONSISTENT if not violations else ConsistencyStatus.INCONSISTENT
        
        return {
            "status": status,
            "violations": violations,
            "check_details": {
                "components_checked": check.target_components,
                "validation_method": "format_validation"
            }
        }
    
    async def validate_schemas(self, check: ConsistencyCheck) -> Dict[str, Any]:
        """Validate schema consistency"""
        violations = []
        
        # Simulate schema validation
        # In a real implementation, this would check actual schemas across components
        
        # Check schema version consistency
        schema_versions = {"database": "v1.0", "api": "v1.1", "models": "v1.0"}
        version_consistent = len(set(schema_versions.values())) == 1
        
        if not version_consistent:
            violations.append(ConsistencyViolation(
                violation_id=str(uuid.uuid4()),
                rule_id="schema_consistency",
                violation_type=ConsistencyType.SCHEMA_CONSISTENCY,
                severity="high",
                description="Schema version inconsistency detected",
                affected_components=list(schema_versions.keys()),
                metadata={"schema_versions": schema_versions}
            ))
        
        # Check required fields consistency
        required_fields_consistent = True  # Simulated
        if not required_fields_consistent:
            violations.append(ConsistencyViolation(
                violation_id=str(uuid.uuid4()),
                rule_id="schema_consistency",
                violation_type=ConsistencyType.SCHEMA_CONSISTENCY,
                severity="medium",
                description="Required fields inconsistency detected",
                affected_components=["database", "models"],
                metadata={"missing_fields": ["id", "timestamp"]}
            ))
        
        status = ConsistencyStatus.CONSISTENT if not violations else ConsistencyStatus.INCONSISTENT
        
        return {
            "status": status,
            "violations": violations,
            "check_details": {
                "components_checked": check.target_components,
                "validation_method": "schema_validation"
            }
        }
    
    async def validate_cross_system_consistency(self, check: ConsistencyCheck) -> Dict[str, Any]:
        """Validate cross-system consistency"""
        violations = []
        
        # Simulate cross-system consistency validation
        # In a real implementation, this would check consistency across all system components
        
        # Check configuration consistency
        config_consistent = True  # Simulated
        if not config_consistent:
            violations.append(ConsistencyViolation(
                violation_id=str(uuid.uuid4()),
                rule_id="cross_system_consistency",
                violation_type=ConsistencyType.CROSS_SYSTEM_CONSISTENCY,
                severity="high",
                description="Configuration inconsistency across systems",
                affected_components=["auth", "database", "cache"],
                metadata={"inconsistent_configs": ["timeout", "retry_count"]}
            ))
        
        # Check data synchronization
        sync_consistent = True  # Simulated
        if not sync_consistent:
            violations.append(ConsistencyViolation(
                violation_id=str(uuid.uuid4()),
                rule_id="cross_system_consistency",
                violation_type=ConsistencyType.CROSS_SYSTEM_CONSISTENCY,
                severity="medium",
                description="Data synchronization inconsistency",
                affected_components=["database", "cache"],
                metadata={"sync_delay": "5_minutes"}
            ))
        
        status = ConsistencyStatus.CONSISTENT if not violations else ConsistencyStatus.INCONSISTENT
        
        return {
            "status": status,
            "violations": violations,
            "check_details": {
                "components_checked": check.target_components,
                "validation_method": "cross_system_validation"
            }
        }
    
    async def _apply_auto_fixes(self, violations: List[ConsistencyViolation]) -> List[Dict[str, Any]]:
        """Apply automatic fixes for violations"""
        fixes_applied = []
        
        for violation in violations:
            try:
                # Determine fix handler based on violation type
                fix_handler = self._get_fix_handler(violation)
                if fix_handler:
                    fix_result = await fix_handler(violation)
                    if fix_result["success"]:
                        fixes_applied.append({
                            "violation_id": violation.violation_id,
                            "fix_method": fix_result["method"],
                            "fix_details": fix_result["details"],
                            "applied_at": datetime.now().isoformat()
                        })
                        
                        # Mark violation as resolved
                        violation.resolved_at = datetime.now()
                        violation.resolution_method = fix_result["method"]
                        
                        logger.info("Auto-fix applied", 
                                   violation_id=violation.violation_id,
                                   fix_method=fix_result["method"])
                
            except Exception as e:
                logger.error("Auto-fix failed", 
                           violation_id=violation.violation_id, 
                           error=str(e))
        
        return fixes_applied
    
    def _get_fix_handler(self, violation: ConsistencyViolation) -> Optional[callable]:
        """Get appropriate fix handler for violation"""
        handler_map = {
            ConsistencyType.DATA_CONSISTENCY: "data_format_fix",
            ConsistencyType.SCHEMA_CONSISTENCY: "schema_migration",
            ConsistencyType.API_CONSISTENCY: "api_standardization",
            ConsistencyType.CONFIGURATION_CONSISTENCY: "configuration_sync",
            ConsistencyType.CROSS_SYSTEM_CONSISTENCY: "cache_invalidation"
        }
        
        handler_name = handler_map.get(violation.violation_type)
        return self.auto_fix_handlers.get(handler_name) if handler_name else None
    
    async def _fix_data_format_violation(self, violation: ConsistencyViolation) -> Dict[str, Any]:
        """Fix data format violation"""
        # Simulate data format fix
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "success": True,
            "method": "data_format_standardization",
            "details": {
                "action": "converted_to_json",
                "affected_components": violation.affected_components
            }
        }
    
    async def _fix_schema_violation(self, violation: ConsistencyViolation) -> Dict[str, Any]:
        """Fix schema violation"""
        # Simulate schema migration
        await asyncio.sleep(0.2)  # Simulate processing time
        
        return {
            "success": True,
            "method": "schema_migration",
            "details": {
                "action": "migrated_to_latest_version",
                "target_version": "v1.1"
            }
        }
    
    async def _fix_api_violation(self, violation: ConsistencyViolation) -> Dict[str, Any]:
        """Fix API violation"""
        # Simulate API standardization
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "success": True,
            "method": "api_standardization",
            "details": {
                "action": "standardized_response_format",
                "format": "json"
            }
        }
    
    async def _fix_configuration_violation(self, violation: ConsistencyViolation) -> Dict[str, Any]:
        """Fix configuration violation"""
        # Simulate configuration synchronization
        await asyncio.sleep(0.1)  # Simulate processing time
        
        return {
            "success": True,
            "method": "configuration_sync",
            "details": {
                "action": "synchronized_configurations",
                "components": violation.affected_components
            }
        }
    
    async def _fix_cache_violation(self, violation: ConsistencyViolation) -> Dict[str, Any]:
        """Fix cache violation"""
        # Simulate cache invalidation
        await asyncio.sleep(0.05)  # Simulate processing time
        
        return {
            "success": True,
            "method": "cache_invalidation",
            "details": {
                "action": "invalidated_stale_cache",
                "components": violation.affected_components
            }
        }
    
    def _generate_consistency_recommendations(self, violations: List[ConsistencyViolation]) -> List[str]:
        """Generate recommendations based on violations"""
        recommendations = []
        
        # Group violations by type
        violation_types = defaultdict(list)
        for violation in violations:
            violation_types[violation.violation_type].append(violation)
        
        # Generate type-specific recommendations
        for violation_type, type_violations in violation_types.items():
            if violation_type == ConsistencyType.DATA_CONSISTENCY:
                recommendations.append(f"Standardize data formats across all components ({len(type_violations)} violations)")
                recommendations.append("Implement data format validation middleware")
            elif violation_type == ConsistencyType.SCHEMA_CONSISTENCY:
                recommendations.append(f"Migrate all components to consistent schema version ({len(type_violations)} violations)")
                recommendations.append("Implement automated schema migration")
            elif violation_type == ConsistencyType.API_CONSISTENCY:
                recommendations.append(f"Standardize API response formats ({len(type_violations)} violations)")
                recommendations.append("Implement API versioning strategy")
            elif violation_type == ConsistencyType.CROSS_SYSTEM_CONSISTENCY:
                recommendations.append(f"Implement cross-system synchronization ({len(type_violations)} violations)")
                recommendations.append("Add system-wide configuration management")
        
        # Add general recommendations
        recommendations.extend([
            "Implement automated consistency monitoring",
            "Add consistency checks to CI/CD pipeline",
            "Create consistency documentation and guidelines",
            "Regular consistency audits and reviews"
        ])
        
        return list(set(recommendations))  # Remove duplicates
    
    async def _cache_consistency_report(self, report: ConsistencyReport):
        """Cache consistency report in Redis"""
        try:
            cache_key = f"consistency_report:{report.report_id}"
            
            cache_data = {
                "report_id": report.report_id,
                "timestamp": report.timestamp.isoformat(),
                "overall_consistency_score": report.overall_consistency_score,
                "total_checks": report.total_checks,
                "passed_checks": report.passed_checks,
                "failed_checks": report.failed_checks,
                "warnings": report.warnings,
                "violations": [
                    {
                        "violation_id": v.violation_id,
                        "rule_id": v.rule_id,
                        "violation_type": v.violation_type.value,
                        "severity": v.severity,
                        "description": v.description,
                        "location": v.location,
                        "affected_components": v.affected_components,
                        "detected_at": v.detected_at.isoformat(),
                        "resolved_at": v.resolved_at.isoformat() if v.resolved_at else None,
                        "resolution_method": v.resolution_method,
                        "metadata": v.metadata
                    }
                    for v in report.violations
                ],
                "recommendations": report.recommendations,
                "auto_fixes_applied": report.auto_fixes_applied,
                "metadata": report.metadata
            }
            
            await self.redis_client.set(
                cache_key,
                json.dumps(cache_data, default=str),
                ex=3600  # Cache for 1 hour
            )
            
        except Exception as e:
            logger.error("Failed to cache consistency report", error=str(e))
    
    async def add_consistency_rule(self, rule: ConsistencyRule) -> bool:
        """Add a new consistency rule"""
        try:
            self.consistency_rules[rule.rule_id] = rule
            logger.info("Consistency rule added", rule_id=rule.rule_id, name=rule.name)
            return True
            
        except Exception as e:
            logger.error("Failed to add consistency rule", error=str(e))
            return False
    
    async def add_consistency_check(self, check: ConsistencyCheck) -> bool:
        """Add a new consistency check"""
        try:
            self.consistency_checks[check.check_id] = check
            logger.info("Consistency check added", check_id=check.check_id, name=check.name)
            return True
            
        except Exception as e:
            logger.error("Failed to add consistency check", error=str(e))
            return False
    
    async def get_consistency_metrics(self) -> Dict[str, Any]:
        """Get consistency enforcement metrics"""
        try:
            total_violations = len(self.violations_history)
            resolved_violations = len([v for v in self.violations_history if v.resolved_at])
            
            # Group violations by type
            violation_types = defaultdict(int)
            severity_counts = defaultdict(int)
            
            for violation in self.violations_history:
                violation_types[violation.violation_type.value] += 1
                severity_counts[violation.severity] += 1
            
            return {
                "total_violations": total_violations,
                "resolved_violations": resolved_violations,
                "unresolved_violations": total_violations - resolved_violations,
                "resolution_rate": (resolved_violations / total_violations * 100) if total_violations > 0 else 0,
                "violation_types": dict(violation_types),
                "severity_distribution": dict(severity_counts),
                "active_rules": len([r for r in self.consistency_rules.values() if r.enabled]),
                "active_checks": len([c for c in self.consistency_checks.values() if c.enabled]),
                "auto_fix_handlers": len(self.auto_fix_handlers)
            }
            
        except Exception as e:
            logger.error("Failed to get consistency metrics", error=str(e))
            return {}
    
    async def schedule_consistency_check(self, check_id: str, schedule: str) -> bool:
        """Schedule a consistency check to run periodically"""
        try:
            if check_id in self.consistency_checks:
                self.consistency_checks[check_id].schedule = schedule
                logger.info("Consistency check scheduled", check_id=check_id, schedule=schedule)
                return True
            else:
                logger.error("Consistency check not found", check_id=check_id)
                return False
                
        except Exception as e:
            logger.error("Failed to schedule consistency check", error=str(e))
            return False

# Global instance
consistency_enforcer = ConsistencyEnforcer()


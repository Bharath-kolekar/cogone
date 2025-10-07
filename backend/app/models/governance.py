"""
Enhanced Governance Models - Comprehensive governance data models
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4


class GovernanceSeverity(str, Enum):
    """Governance violation severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class GovernanceStatus(str, Enum):
    """Governance compliance status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    WARNING = "warning"
    ERROR = "error"
    UNKNOWN = "unknown"


class ComplianceLevel(str, Enum):
    """Compliance level definitions"""
    FULLY_COMPLIANT = "fully_compliant"
    MOSTLY_COMPLIANT = "mostly_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    CRITICAL_NON_COMPLIANT = "critical_non_compliant"


class ComplianceCategory(str, Enum):
    """Compliance categories"""
    ETHICAL = "ethical"
    SECURITY = "security"
    PERFORMANCE = "performance"
    QUALITY = "quality"
    BUSINESS = "business"
    REGULATORY = "regulatory"
    OPERATIONAL = "operational"


class PolicyType(str, Enum):
    """Policy types"""
    ACCURACY = "accuracy"
    PERFORMANCE = "performance"
    SECURITY = "security"
    ETHICAL = "ethical"
    QUALITY = "quality"
    BUSINESS = "business"
    REGULATORY = "regulatory"
    OPERATIONAL = "operational"
    CUSTOM = "custom"


class RemediationAction(str, Enum):
    """Remediation action types"""
    RESTART_COMPONENT = "restart_component"
    OPTIMIZE_PERFORMANCE = "optimize_performance"
    SECURITY_SCAN = "security_scan"
    ETHICAL_VALIDATION = "ethical_validation"
    QUALITY_REVIEW = "quality_review"
    UPDATE_POLICIES = "update_policies"
    SCALE_RESOURCES = "scale_resources"
    ENABLE_CACHING = "enable_caching"
    REDUCE_COMPLEXITY = "reduce_complexity"


class GovernanceViolation(BaseModel):
    """Governance violation record"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    component: str = Field(..., description="Component that violated governance")
    rule_id: str = Field(..., description="Rule that was violated")
    severity: GovernanceSeverity = Field(..., description="Severity of violation")
    description: str = Field(..., description="Description of violation")
    context: Dict[str, Any] = Field(default_factory=dict, description="Violation context")
    detected_at: datetime = Field(default_factory=datetime.utcnow, description="When violation was detected")
    resolved_at: Optional[datetime] = Field(None, description="When violation was resolved")
    remediation_actions: List[str] = Field(default_factory=list, description="Actions taken to remediate")
    impact_score: float = Field(default=0.0, description="Impact score of violation")
    user_id: Optional[UUID] = Field(None, description="User who triggered violation")
    session_id: Optional[str] = Field(None, description="Session ID when violation occurred")


class GovernancePolicy(BaseModel):
    """Governance policy definition"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., description="Policy name")
    description: str = Field(..., description="Policy description")
    type: PolicyType = Field(..., description="Policy type")
    rules: Dict[str, Any] = Field(..., description="Policy rules")
    enforcement_level: str = Field(default="strict", description="Enforcement level")
    is_active: bool = Field(default=True, description="Whether policy is active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[UUID] = Field(None, description="User who created policy")


class GovernanceMetrics(BaseModel):
    """Governance performance metrics"""
    overall_score: float = Field(..., description="Overall governance score")
    compliance_rate: float = Field(..., description="Compliance rate percentage")
    violation_count: int = Field(default=0, description="Total violation count")
    critical_violations: int = Field(default=0, description="Critical violation count")
    high_violations: int = Field(default=0, description="High severity violation count")
    medium_violations: int = Field(default=0, description="Medium severity violation count")
    low_violations: int = Field(default=0, description="Low severity violation count")
    avg_remediation_time: float = Field(default=0.0, description="Average remediation time in minutes")
    policy_coverage: float = Field(default=0.0, description="Policy coverage percentage")
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class ComplianceResult(BaseModel):
    """Compliance checking result"""
    category: ComplianceCategory = Field(..., description="Compliance category")
    level: ComplianceLevel = Field(..., description="Compliance level")
    score: float = Field(..., description="Compliance score")
    details: Dict[str, Any] = Field(default_factory=dict, description="Compliance details")
    violations: List[str] = Field(default_factory=list, description="List of violations")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    checked_at: datetime = Field(default_factory=datetime.utcnow)
    next_check: datetime = Field(..., description="When to check next")


class ComplianceReport(BaseModel):
    """Comprehensive compliance report"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    overall_score: float = Field(..., description="Overall compliance score")
    overall_level: ComplianceLevel = Field(..., description="Overall compliance level")
    category_results: Dict[ComplianceCategory, ComplianceResult] = Field(..., description="Category results")
    critical_issues: List[str] = Field(default_factory=list, description="Critical issues")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    valid_until: datetime = Field(..., description="Report validity period")
    operation: str = Field(..., description="Operation that was checked")
    context: Dict[str, Any] = Field(default_factory=dict, description="Check context")


class GovernanceAlert(BaseModel):
    """Governance alert"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    severity: str = Field(..., description="Alert severity")
    title: str = Field(..., description="Alert title")
    message: str = Field(..., description="Alert message")
    component: str = Field(..., description="Component that generated alert")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    acknowledged: bool = Field(default=False, description="Whether alert is acknowledged")
    resolved: bool = Field(default=False, description="Whether alert is resolved")
    acknowledged_by: Optional[UUID] = Field(None, description="User who acknowledged")
    resolved_by: Optional[UUID] = Field(None, description="User who resolved")
    acknowledged_at: Optional[datetime] = Field(None, description="When acknowledged")
    resolved_at: Optional[datetime] = Field(None, description="When resolved")


class DashboardWidget(BaseModel):
    """Dashboard widget configuration"""
    id: str = Field(..., description="Widget ID")
    type: str = Field(..., description="Widget type")
    title: str = Field(..., description="Widget title")
    data: Dict[str, Any] = Field(default_factory=dict, description="Widget data")
    refresh_interval: int = Field(default=30, description="Refresh interval in seconds")
    last_updated: Optional[datetime] = Field(None, description="Last update time")
    is_active: bool = Field(default=True, description="Whether widget is active")


class GovernanceDashboard(BaseModel):
    """Governance dashboard configuration"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., description="Dashboard name")
    description: str = Field(..., description="Dashboard description")
    widgets: List[DashboardWidget] = Field(default_factory=list, description="Dashboard widgets")
    layout: Dict[str, Any] = Field(default_factory=dict, description="Dashboard layout")
    is_public: bool = Field(default=False, description="Whether dashboard is public")
    created_by: Optional[UUID] = Field(None, description="User who created dashboard")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GovernanceRule(BaseModel):
    """Governance rule definition"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str = Field(..., description="Rule name")
    description: str = Field(..., description="Rule description")
    category: ComplianceCategory = Field(..., description="Rule category")
    conditions: Dict[str, Any] = Field(..., description="Rule conditions")
    actions: List[str] = Field(default_factory=list, description="Actions to take when rule is violated")
    severity: GovernanceSeverity = Field(default=GovernanceSeverity.MEDIUM, description="Default severity")
    is_active: bool = Field(default=True, description="Whether rule is active")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class GovernanceAuditLog(BaseModel):
    """Governance audit log entry"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    action: str = Field(..., description="Action performed")
    component: str = Field(..., description="Component that performed action")
    user_id: Optional[UUID] = Field(None, description="User who performed action")
    details: Dict[str, Any] = Field(default_factory=dict, description="Action details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ip_address: Optional[str] = Field(None, description="IP address of user")
    user_agent: Optional[str] = Field(None, description="User agent string")


class GovernanceConfiguration(BaseModel):
    """Governance system configuration"""
    monitoring_enabled: bool = Field(default=True, description="Whether monitoring is enabled")
    compliance_checking_enabled: bool = Field(default=True, description="Whether compliance checking is enabled")
    alerting_enabled: bool = Field(default=True, description="Whether alerting is enabled")
    auto_remediation_enabled: bool = Field(default=True, description="Whether auto-remediation is enabled")
    monitoring_interval: int = Field(default=30, description="Monitoring interval in seconds")
    compliance_check_interval: int = Field(default=300, description="Compliance check interval in seconds")
    alert_threshold: float = Field(default=0.8, description="Alert threshold")
    remediation_timeout: int = Field(default=300, description="Remediation timeout in seconds")
    max_violations_per_hour: int = Field(default=100, description="Maximum violations per hour")
    retention_days: int = Field(default=90, description="Data retention period in days")


class GovernanceRequest(BaseModel):
    """Request to interact with governance system"""
    operation: str = Field(..., description="Operation to perform")
    context: Dict[str, Any] = Field(default_factory=dict, description="Request context")
    user_id: Optional[UUID] = Field(None, description="User making request")
    session_id: Optional[str] = Field(None, description="Session ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class GovernanceResponse(BaseModel):
    """Response from governance system"""
    status: str = Field(..., description="Response status")
    message: str = Field(..., description="Response message")
    data: Dict[str, Any] = Field(default_factory=dict, description="Response data")
    violations: List[GovernanceViolation] = Field(default_factory=list, description="Any violations found")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class GovernanceTrend(BaseModel):
    """Governance trend analysis"""
    period: str = Field(..., description="Trend period")
    trend: str = Field(..., description="Trend direction")
    change: float = Field(..., description="Change percentage")
    forecast: Dict[str, Any] = Field(default_factory=dict, description="Forecast data")
    confidence: float = Field(default=0.0, description="Forecast confidence")
    generated_at: datetime = Field(default_factory=datetime.utcnow)


class GovernanceReport(BaseModel):
    """Governance report"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str = Field(..., description="Report title")
    description: str = Field(..., description="Report description")
    metrics: GovernanceMetrics = Field(..., description="Governance metrics")
    violations: List[GovernanceViolation] = Field(default_factory=list, description="Violations")
    trends: List[GovernanceTrend] = Field(default_factory=list, description="Trends")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    period_start: datetime = Field(..., description="Report period start")
    period_end: datetime = Field(..., description="Report period end")
    generated_by: Optional[UUID] = Field(None, description="User who generated report")

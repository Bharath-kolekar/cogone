"""
Meta AI Orchestrator models for supreme coordination and governance
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from decimal import Decimal


class MetaOrchestrationStatus(str, Enum):
    """Meta orchestration status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class GovernanceLevel(str, Enum):
    """Governance levels"""
    CRITICAL = "critical"      # 100% accuracy required
    HIGH = "high"             # 99%+ accuracy required
    MEDIUM = "medium"         # 95%+ accuracy required
    LOW = "low"              # 90%+ accuracy required


class ComponentStatus(str, Enum):
    """Component status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEGRADED = "degraded"
    FAILED = "failed"
    MAINTENANCE = "maintenance"


class MetaOrchestrationRequest(BaseModel):
    """Meta orchestration request model"""
    orchestration_type: str = Field(..., description="Type of orchestration to perform")
    components: List[str] = Field(default_factory=list, description="Components to orchestrate")
    governance_level: GovernanceLevel = Field(default=GovernanceLevel.HIGH, description="Governance level")
    accuracy_requirement: float = Field(default=99.0, description="Minimum accuracy requirement")
    harmony_requirement: float = Field(default=99.0, description="Minimum harmony requirement")
    priority: int = Field(default=1, description="Orchestration priority (1-10)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class MetaOrchestrationResponse(BaseModel):
    """Meta orchestration response model"""
    orchestration_id: str = Field(..., description="Unique orchestration identifier")
    status: MetaOrchestrationStatus = Field(..., description="Orchestration status")
    total_tasks: int = Field(..., description="Total number of tasks")
    successful_tasks: int = Field(..., description="Number of successful tasks")
    overall_accuracy: float = Field(..., description="Overall accuracy achieved")
    overall_harmony: float = Field(..., description="Overall harmony score")
    governance_compliance: float = Field(..., description="Governance compliance percentage")
    results: List[Dict[str, Any]] = Field(..., description="Detailed results")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class GovernanceRuleRequest(BaseModel):
    """Governance rule request model"""
    name: str = Field(..., description="Rule name")
    description: str = Field(..., description="Rule description")
    level: GovernanceLevel = Field(..., description="Governance level")
    component: str = Field(..., description="Target component")
    condition: str = Field(..., description="Rule condition")
    action: str = Field(..., description="Action to take")
    priority: int = Field(default=5, description="Rule priority (1-10)")
    is_active: bool = Field(default=True, description="Whether rule is active")


class GovernanceRuleResponse(BaseModel):
    """Governance rule response model"""
    rule_id: str = Field(..., description="Unique rule identifier")
    name: str = Field(..., description="Rule name")
    description: str = Field(..., description="Rule description")
    level: GovernanceLevel = Field(..., description="Governance level")
    component: str = Field(..., description="Target component")
    condition: str = Field(..., description="Rule condition")
    action: str = Field(..., description="Action to take")
    priority: int = Field(..., description="Rule priority")
    is_active: bool = Field(..., description="Whether rule is active")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ComponentHealthResponse(BaseModel):
    """Component health response model"""
    component_id: str = Field(..., description="Component identifier")
    name: str = Field(..., description="Component name")
    status: ComponentStatus = Field(..., description="Component status")
    accuracy: float = Field(..., description="Component accuracy")
    performance: float = Field(..., description="Component performance")
    reliability: float = Field(..., description="Component reliability")
    last_check: datetime = Field(..., description="Last health check")
    issues: List[str] = Field(default_factory=list, description="Current issues")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")


class PlatformStatusResponse(BaseModel):
    """Platform status response model"""
    total_components: int = Field(..., description="Total number of components")
    active_components: int = Field(..., description="Number of active components")
    component_health: Dict[str, Any] = Field(..., description="Component health metrics")
    governance: Dict[str, Any] = Field(..., description="Governance metrics")
    harmony_score: float = Field(..., description="Overall harmony score")
    overall_status: str = Field(..., description="Overall platform status")
    last_updated: datetime = Field(..., description="Last update timestamp")


class MetaOrchestrationResult(BaseModel):
    """Meta orchestration result model"""
    task_id: str = Field(..., description="Task identifier")
    task_type: str = Field(..., description="Task type")
    status: str = Field(..., description="Task status")
    accuracy: float = Field(..., description="Task accuracy")
    performance: float = Field(..., description="Task performance")
    governance_compliance: float = Field(..., description="Governance compliance")
    harmony_score: float = Field(..., description="Harmony score")
    results: Dict[str, Any] = Field(..., description="Task results")
    timestamp: datetime = Field(..., description="Task timestamp")


class SmartCodingAccuracyResponse(BaseModel):
    """Smart Coding AI accuracy response model"""
    component: str = Field(..., description="Component name")
    accuracy: float = Field(..., description="Accuracy percentage")
    status: str = Field(..., description="Accuracy status")
    governance_compliance: float = Field(..., description="Governance compliance")
    last_updated: datetime = Field(..., description="Last update timestamp")


class GovernanceComplianceResponse(BaseModel):
    """Governance compliance response model"""
    total_rules: int = Field(..., description="Total governance rules")
    compliant_rules: int = Field(..., description="Number of compliant rules")
    compliance_percentage: float = Field(..., description="Compliance percentage")
    status: str = Field(..., description="Compliance status")
    last_checked: datetime = Field(..., description="Last check timestamp")


class HarmonyScoreResponse(BaseModel):
    """Harmony score response model"""
    harmony_score: float = Field(..., description="Harmony score")
    status: str = Field(..., description="Harmony status")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    last_calculated: datetime = Field(..., description="Last calculation timestamp")


class MetaOrchestrationMetrics(BaseModel):
    """Meta orchestration metrics model"""
    total_orchestrations: int = Field(..., description="Total orchestrations performed")
    successful_orchestrations: int = Field(..., description="Successful orchestrations")
    average_accuracy: float = Field(..., description="Average accuracy")
    average_harmony: float = Field(..., description="Average harmony score")
    governance_compliance: float = Field(..., description="Governance compliance")
    component_health: Dict[str, float] = Field(..., description="Component health metrics")
    performance_trends: Dict[str, List[float]] = Field(..., description="Performance trends")
    last_updated: datetime = Field(..., description="Last update timestamp")


class MetaOrchestrationConfig(BaseModel):
    """Meta orchestration configuration model"""
    auto_orchestration: bool = Field(default=True, description="Enable auto orchestration")
    orchestration_interval: int = Field(default=300, description="Orchestration interval in seconds")
    governance_enforcement: bool = Field(default=True, description="Enable governance enforcement")
    accuracy_threshold: float = Field(default=99.0, description="Accuracy threshold")
    harmony_threshold: float = Field(default=99.0, description="Harmony threshold")
    smart_coding_accuracy: float = Field(default=100.0, description="Smart Coding AI accuracy requirement")
    monitoring_enabled: bool = Field(default=True, description="Enable monitoring")
    alert_threshold: float = Field(default=95.0, description="Alert threshold")
    auto_recovery: bool = Field(default=True, description="Enable auto recovery")
    optimization_enabled: bool = Field(default=True, description="Enable optimization")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

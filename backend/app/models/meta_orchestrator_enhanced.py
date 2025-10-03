"""
Enhanced Meta AI Orchestrator models for escalation system
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
from decimal import Decimal


class EscalationLevel(str, Enum):
    """Escalation levels"""
    NONE = "none"
    COMPONENT_SELF_HEAL = "component_self_heal"
    AI_ORCHESTRATOR_HELP = "ai_orchestrator_help"
    META_AI_INTERVENTION = "meta_ai_intervention"
    CRITICAL_FAILURE = "critical_failure"


class ComponentHealthStatus(str, Enum):
    """Component health status"""
    EXCELLENT = "excellent"
    GOOD = "good"
    DEGRADED = "degraded"
    POOR = "poor"
    CRITICAL = "critical"
    FAILED = "failed"


class PermanentSolutionType(str, Enum):
    """Permanent solution types"""
    COMPONENT_REPLACEMENT = "component_replacement"
    ARCHITECTURE_REDESIGN = "architecture_redesign"
    ALGORITHM_OPTIMIZATION = "algorithm_optimization"
    RESOURCE_REALLOCATION = "resource_reallocation"
    WORKFLOW_RESTRUCTURING = "workflow_restructuring"
    SYSTEM_REBOOT = "system_reboot"
    EMERGENCY_BYPASS = "emergency_bypass"


class ComponentHealthRequest(BaseModel):
    """Component health request model"""
    component_id: str = Field(..., description="Component identifier")
    accuracy: float = Field(..., description="Component accuracy")
    performance: float = Field(..., description="Component performance")
    reliability: float = Field(..., description="Component reliability")
    additional_metrics: Dict[str, Any] = Field(default_factory=dict, description="Additional metrics")


class ComponentHealthResponse(BaseModel):
    """Component health response model"""
    component_id: str = Field(..., description="Component identifier")
    health_status: ComponentHealthStatus = Field(..., description="Health status")
    health_score: float = Field(..., description="Overall health score")
    metrics: Dict[str, Any] = Field(..., description="Health metrics")
    issue_detected: bool = Field(..., description="Whether issue was detected")
    issue: Optional[Dict[str, Any]] = Field(None, description="Issue details if detected")
    timestamp: datetime = Field(..., description="Response timestamp")


class ComponentIssueResponse(BaseModel):
    """Component issue response model"""
    issue_id: str = Field(..., description="Issue identifier")
    component_id: str = Field(..., description="Component identifier")
    issue_type: str = Field(..., description="Issue type")
    severity: str = Field(..., description="Issue severity")
    description: str = Field(..., description="Issue description")
    detected_at: datetime = Field(..., description="Detection timestamp")
    escalation_level: EscalationLevel = Field(..., description="Current escalation level")
    attempts_to_fix: int = Field(..., description="Number of fix attempts")
    max_attempts: int = Field(..., description="Maximum fix attempts")
    permanent_solution: Optional[str] = Field(None, description="Permanent solution ID")
    resolved: bool = Field(..., description="Whether issue is resolved")
    resolved_at: Optional[datetime] = Field(None, description="Resolution timestamp")


class EscalationActionResponse(BaseModel):
    """Escalation action response model"""
    action_id: str = Field(..., description="Action identifier")
    component_id: str = Field(..., description="Component identifier")
    escalation_level: EscalationLevel = Field(..., description="Escalation level")
    action_type: str = Field(..., description="Action type")
    description: str = Field(..., description="Action description")
    success_probability: float = Field(..., description="Success probability")
    execution_time: int = Field(..., description="Execution time in seconds")
    permanent_solution: bool = Field(..., description="Whether it's a permanent solution")
    created_at: datetime = Field(..., description="Creation timestamp")


class EscalationResponse(BaseModel):
    """Escalation response model"""
    issue_id: str = Field(..., description="Issue identifier")
    escalation_action: EscalationActionResponse = Field(..., description="Escalation action")
    success: bool = Field(..., description="Whether escalation was successful")
    escalation_level: str = Field(..., description="Escalation level")
    permanent_solution: bool = Field(..., description="Whether permanent solution was applied")
    timestamp: datetime = Field(..., description="Response timestamp")


class PermanentSolutionResponse(BaseModel):
    """Permanent solution response model"""
    solution_id: str = Field(..., description="Solution identifier")
    component_id: str = Field(..., description="Component identifier")
    solution_type: PermanentSolutionType = Field(..., description="Solution type")
    description: str = Field(..., description="Solution description")
    implementation_steps: List[str] = Field(..., description="Implementation steps")
    success_probability: float = Field(..., description="Success probability")
    execution_time: int = Field(..., description="Execution time in minutes")
    rollback_plan: List[str] = Field(..., description="Rollback plan")
    monitoring_required: bool = Field(..., description="Whether monitoring is required")
    created_at: datetime = Field(..., description="Creation timestamp")


class PlatformHealthSummary(BaseModel):
    """Platform health summary model"""
    total_components: int = Field(..., description="Total number of components")
    active_issues: int = Field(..., description="Number of active issues")
    total_escalations: int = Field(..., description="Total number of escalations")
    successful_escalations: int = Field(..., description="Number of successful escalations")
    escalation_success_rate: float = Field(..., description="Escalation success rate")
    platform_health: str = Field(..., description="Overall platform health")
    last_updated: datetime = Field(..., description="Last update timestamp")


class GodModeStatus(BaseModel):
    """God Mode status model"""
    god_mode: str = Field(..., description="God mode status")
    status: str = Field(..., description="Current status")
    intervention_level: str = Field(..., description="Intervention level")
    total_components: int = Field(..., description="Total components")
    active_issues: int = Field(..., description="Active issues")
    total_escalations: int = Field(..., description="Total escalations")
    successful_escalations: int = Field(..., description="Successful escalations")
    escalation_success_rate: float = Field(..., description="Escalation success rate")
    platform_health: str = Field(..., description="Platform health")
    god_powers: List[str] = Field(..., description="God powers")
    timestamp: datetime = Field(..., description="Status timestamp")


class EscalationLevelInfo(BaseModel):
    """Escalation level information model"""
    level: str = Field(..., description="Escalation level")
    description: str = Field(..., description="Level description")
    success_rate: str = Field(..., description="Success rate")
    execution_time: str = Field(..., description="Execution time")


class PermanentSolutionTypeInfo(BaseModel):
    """Permanent solution type information model"""
    type: str = Field(..., description="Solution type")
    description: str = Field(..., description="Type description")
    success_rate: str = Field(..., description="Success rate")
    execution_time: str = Field(..., description="Execution time")


class ComponentHealthHistory(BaseModel):
    """Component health history model"""
    component_id: str = Field(..., description="Component identifier")
    health_history: List[Dict[str, Any]] = Field(..., description="Health history records")
    total_records: int = Field(..., description="Total history records")
    timestamp: datetime = Field(..., description="Response timestamp")


class EscalationHistory(BaseModel):
    """Escalation history model"""
    escalation_history: List[Dict[str, Any]] = Field(..., description="Escalation history records")
    total_count: int = Field(..., description="Total history count")
    successful_count: int = Field(..., description="Successful escalations count")
    timestamp: datetime = Field(..., description="Response timestamp")


class ActiveIssuesResponse(BaseModel):
    """Active issues response model"""
    active_issues: List[ComponentIssueResponse] = Field(..., description="Active issues")
    total_count: int = Field(..., description="Total active issues count")
    timestamp: datetime = Field(..., description="Response timestamp")


class AllIssuesResponse(BaseModel):
    """All issues response model"""
    all_issues: List[ComponentIssueResponse] = Field(..., description="All issues")
    total_count: int = Field(..., description="Total issues count")
    resolved_count: int = Field(..., description="Resolved issues count")
    active_count: int = Field(..., description="Active issues count")
    timestamp: datetime = Field(..., description="Response timestamp")


class EscalationActionsResponse(BaseModel):
    """Escalation actions response model"""
    escalation_actions: List[EscalationActionResponse] = Field(..., description="Escalation actions")
    total_count: int = Field(..., description="Total actions count")
    timestamp: datetime = Field(..., description="Response timestamp")


class PermanentSolutionsResponse(BaseModel):
    """Permanent solutions response model"""
    permanent_solutions: List[PermanentSolutionResponse] = Field(..., description="Permanent solutions")
    total_count: int = Field(..., description="Total solutions count")
    timestamp: datetime = Field(..., description="Response timestamp")


class EscalationLevelsResponse(BaseModel):
    """Escalation levels response model"""
    escalation_levels: List[EscalationLevelInfo] = Field(..., description="Available escalation levels")
    total_levels: int = Field(..., description="Total escalation levels")
    timestamp: datetime = Field(..., description="Response timestamp")


class PermanentSolutionTypesResponse(BaseModel):
    """Permanent solution types response model"""
    solution_types: List[PermanentSolutionTypeInfo] = Field(..., description="Available solution types")
    total_types: int = Field(..., description="Total solution types")
    timestamp: datetime = Field(..., description="Response timestamp")


class AIOrchestratorHealthResponse(BaseModel):
    """AI Orchestrator health response model"""
    component: str = Field(..., description="Component name")
    health_score: float = Field(..., description="Health score")
    status: str = Field(..., description="Health status")
    can_help: bool = Field(..., description="Whether can help other components")
    timestamp: datetime = Field(..., description="Response timestamp")


class ContinuousMonitoringResponse(BaseModel):
    """Continuous monitoring response model"""
    message: str = Field(..., description="Response message")
    status: str = Field(..., description="Monitoring status")
    timestamp: datetime = Field(..., description="Response timestamp")

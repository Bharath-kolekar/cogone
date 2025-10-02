"""
Goal Integrity models for Voice-to-App SaaS Platform
Maintains goal integrity during system activities and user interactions
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from enum import Enum


class GoalType(str, Enum):
    """Types of goals in the system"""
    USER_OBJECTIVE = "user_objective"
    SYSTEM_GOAL = "system_goal"
    BUSINESS_GOAL = "business_goal"
    TECHNICAL_GOAL = "technical_goal"
    SECURITY_GOAL = "security_goal"
    PERFORMANCE_GOAL = "performance_goal"


class GoalStatus(str, Enum):
    """Status of goal integrity"""
    ACTIVE = "active"
    MAINTAINED = "maintained"
    COMPROMISED = "compromised"
    RECOVERING = "recovering"
    SUSPENDED = "suspended"
    COMPLETED = "completed"


class GoalPriority(str, Enum):
    """Priority levels for goals"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IntegrityLevel(str, Enum):
    """Integrity assurance levels"""
    FULL = "full"
    PARTIAL = "partial"
    MINIMAL = "minimal"
    NONE = "none"


class GoalDefinition(BaseModel):
    """Definition of a system goal"""
    id: str
    name: str
    description: str
    goal_type: GoalType
    priority: GoalPriority
    integrity_level: IntegrityLevel
    success_criteria: Dict[str, Any]
    constraints: Dict[str, Any] = {}
    dependencies: List[str] = []
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


class GoalState(BaseModel):
    """Current state of a goal"""
    goal_id: str
    status: GoalStatus
    integrity_score: float = Field(ge=0.0, le=1.0)
    last_verified: datetime
    violation_count: int = 0
    recovery_attempts: int = 0
    metadata: Dict[str, Any] = {}


class GoalViolation(BaseModel):
    """Record of a goal violation"""
    id: str
    goal_id: str
    violation_type: str
    severity: GoalPriority
    description: str
    context: Dict[str, Any]
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_actions: List[str] = []
    impact_assessment: Dict[str, Any] = {}


class GoalCheckpoint(BaseModel):
    """Checkpoint for goal integrity verification"""
    id: str
    goal_id: str
    checkpoint_name: str
    expected_state: Dict[str, Any]
    actual_state: Dict[str, Any]
    integrity_verified: bool
    timestamp: datetime
    verification_method: str
    metadata: Dict[str, Any] = {}


class GoalRecoveryAction(BaseModel):
    """Action taken to recover goal integrity"""
    id: str
    goal_id: str
    action_type: str
    description: str
    parameters: Dict[str, Any]
    executed_at: datetime
    success: bool
    result: Optional[Dict[str, Any]] = None
    rollback_available: bool = False


class GoalIntegrityReport(BaseModel):
    """Comprehensive goal integrity report"""
    report_id: str
    generated_at: datetime
    time_range: Dict[str, datetime]
    overall_integrity_score: float = Field(ge=0.0, le=1.0)
    goal_summaries: List[Dict[str, Any]]
    violations_summary: Dict[str, int]
    recovery_actions_summary: Dict[str, int]
    recommendations: List[str]
    alerts: List[str] = []


class GoalIntegrityRequest(BaseModel):
    """Request for goal integrity verification"""
    goal_ids: Optional[List[str]] = None
    verify_all: bool = False
    integrity_level: Optional[IntegrityLevel] = None
    priority_filter: Optional[GoalPriority] = None
    include_violations: bool = True
    include_recovery: bool = True


class GoalIntegrityResponse(BaseModel):
    """Response from goal integrity verification"""
    verification_id: str
    timestamp: datetime
    goals_verified: int
    goals_compromised: int
    overall_integrity: float
    violations_found: List[GoalViolation]
    recovery_actions_triggered: List[GoalRecoveryAction]
    recommendations: List[str]


class GoalIntegrityConfig(BaseModel):
    """Configuration for goal integrity system"""
    auto_verification_enabled: bool = True
    verification_interval_minutes: int = 5
    violation_threshold: int = 3
    recovery_timeout_minutes: int = 30
    alert_threshold: float = 0.7
    max_recovery_attempts: int = 5
    checkpoint_retention_days: int = 30
    violation_retention_days: int = 90


class GoalIntegrityMetrics(BaseModel):
    """Metrics for goal integrity monitoring"""
    timestamp: datetime
    total_goals: int
    active_goals: int
    compromised_goals: int
    average_integrity_score: float
    violations_last_hour: int
    recovery_actions_last_hour: int
    system_health_score: float
    uptime_percentage: float


class GoalIntegrityAlert(BaseModel):
    """Alert for goal integrity issues"""
    id: str
    alert_type: str
    severity: GoalPriority
    goal_id: Optional[str] = None
    title: str
    description: str
    triggered_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    escalation_level: int = 0
    metadata: Dict[str, Any] = {}


class GoalIntegrityAuditLog(BaseModel):
    """Audit log for goal integrity activities"""
    id: str
    timestamp: datetime
    action: str
    goal_id: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    details: Dict[str, Any]
    result: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


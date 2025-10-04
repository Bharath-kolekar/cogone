"""
Swarm AI Pydantic Models
Advanced multi-agent system models for 100% accuracy
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# SWARM AI ENUMS
# ============================================================================

class SwarmType(str, Enum):
    """Swarm type enumeration"""
    HUNDRED_PERCENT_ACCURACY = "100_percent_accuracy"
    CREW_AI = "crew_ai"
    AI_TOWN = "ai_town"
    HIERARCHICAL = "hierarchical"
    CONCURRENT = "concurrent"
    ADAPTIVE = "adaptive"


class AgentRole(str, Enum):
    """Agent role enumeration"""
    COORDINATOR = "coordinator"
    VALIDATOR = "validator"
    EXECUTOR = "executor"
    ANALYZER = "analyzer"
    CONSENSUS_BUILDER = "consensus_builder"
    QUALITY_ASSURANCE = "quality_assurance"
    SECURITY_GUARD = "security_guard"
    PERFORMANCE_OPTIMIZER = "performance_optimizer"
    KNOWLEDGE_MANAGER = "knowledge_manager"
    COMMUNICATION_HUB = "communication_hub"


class SwarmArchitecture(str, Enum):
    """Swarm architecture enumeration"""
    HIERARCHICAL = "hierarchical"
    CONCURRENT = "concurrent"
    SEQUENTIAL = "sequential"
    ADAPTIVE = "adaptive"
    CONSENSUS = "consensus"
    CASCADE = "cascade"


class ConsensusLevel(str, Enum):
    """Consensus level enumeration"""
    UNANIMOUS = "unanimous"
    MAJORITY = "majority"
    SUPER_MAJORITY = "super_majority"
    EXPERT_CONSENSUS = "expert_consensus"
    VALIDATED_CONSENSUS = "validated_consensus"


class ValidationMethod(str, Enum):
    """Validation method enumeration"""
    CROSS_VALIDATION = "cross_validation"
    ENSEMBLE_VALIDATION = "ensemble_validation"
    CONSENSUS_VALIDATION = "consensus_validation"
    EXPERT_VALIDATION = "expert_validation"
    MULTI_MODAL_VALIDATION = "multi_modal_validation"
    TEMPORAL_VALIDATION = "temporal_validation"
    CONTEXTUAL_VALIDATION = "contextual_validation"


class TaskStatus(str, Enum):
    """Task status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SwarmStatus(str, Enum):
    """Swarm status enumeration"""
    CREATED = "created"
    ACTIVE = "active"
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    SHUTDOWN = "shutdown"


# ============================================================================
# CORE SWARM AI MODELS
# ============================================================================

class AgentCapabilityModel(BaseModel):
    """Agent capability model"""
    capability_id: str = Field(..., description="Unique capability identifier")
    name: str = Field(..., description="Capability name")
    description: str = Field(..., description="Capability description")
    accuracy_threshold: float = Field(..., ge=0.0, le=1.0, description="Required accuracy threshold")
    validation_methods: List[ValidationMethod] = Field(..., description="Supported validation methods")
    consensus_requirements: ConsensusLevel = Field(..., description="Required consensus level")
    specialization_domain: str = Field(..., description="Specialization domain")
    confidence_level: float = Field(default=0.0, ge=0.0, le=1.0, description="Current confidence level")
    success_rate: float = Field(default=0.0, ge=0.0, le=1.0, description="Success rate")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class SwarmCreateRequest(BaseModel):
    """Request to create a new swarm"""
    swarm_type: SwarmType = Field(..., description="Type of swarm to create")
    name: Optional[str] = Field(None, description="Optional swarm name")
    description: Optional[str] = Field(None, description="Optional swarm description")
    capabilities: List[str] = Field(default_factory=list, description="Required capabilities")
    max_agents: Optional[int] = Field(None, ge=1, le=100, description="Maximum number of agents")
    accuracy_requirement: float = Field(default=0.95, ge=0.0, le=1.0, description="Required accuracy level")
    consensus_level: ConsensusLevel = Field(default=ConsensusLevel.SUPER_MAJORITY, description="Consensus level")
    architecture: SwarmArchitecture = Field(default=SwarmArchitecture.CONSENSUS, description="Swarm architecture")


class SwarmResponse(BaseModel):
    """Swarm response model"""
    swarm_id: str = Field(..., description="Unique swarm identifier")
    swarm_type: str = Field(..., description="Swarm type")
    architecture: str = Field(..., description="Swarm architecture")
    status: SwarmStatus = Field(..., description="Current swarm status")
    created_at: datetime = Field(..., description="Creation timestamp")
    agent_count: int = Field(..., description="Number of agents in swarm")
    capabilities: List[str] = Field(..., description="Swarm capabilities")
    accuracy_requirement: Optional[float] = Field(None, description="Accuracy requirement")
    consensus_level: Optional[str] = Field(None, description="Consensus level")


class SwarmStatusResponse(BaseModel):
    """Swarm status response model"""
    swarm_id: str = Field(..., description="Swarm identifier")
    architecture: str = Field(..., description="Swarm architecture")
    total_agents: int = Field(..., description="Total number of agents")
    active_agents: int = Field(..., description="Number of active agents")
    pending_tasks: int = Field(..., description="Number of pending tasks")
    agent_roles: Dict[str, str] = Field(..., description="Agent roles mapping")
    last_updated: datetime = Field(..., description="Last update timestamp")


class SwarmMetricsResponse(BaseModel):
    """Swarm metrics response model"""
    swarm_id: str = Field(..., description="Swarm identifier")
    total_tasks: int = Field(..., description="Total tasks processed")
    completed_tasks: int = Field(..., description="Completed tasks")
    accuracy_rate: float = Field(..., ge=0.0, le=1.0, description="Overall accuracy rate")
    consensus_rate: float = Field(..., ge=0.0, le=1.0, description="Consensus success rate")
    average_confidence: float = Field(..., ge=0.0, le=1.0, description="Average confidence level")
    agent_utilization: Dict[str, float] = Field(..., description="Agent utilization rates")
    error_rate: float = Field(..., ge=0.0, le=1.0, description="Error rate")
    last_updated: datetime = Field(..., description="Last update timestamp")


# ============================================================================
# TASK MODELS
# ============================================================================

class TaskCreateRequest(BaseModel):
    """Request to create a new task"""
    task_type: str = Field(..., description="Type of task")
    description: str = Field(..., description="Task description")
    complexity_level: int = Field(..., ge=1, le=10, description="Task complexity level")
    accuracy_requirement: float = Field(..., ge=0.0, le=1.0, description="Required accuracy")
    deadline: Optional[datetime] = Field(None, description="Task deadline")
    dependencies: List[str] = Field(default_factory=list, description="Task dependencies")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Task constraints")
    context: Dict[str, Any] = Field(default_factory=dict, description="Task context")
    priority: int = Field(default=1, ge=1, le=10, description="Task priority")


class TaskResponse(BaseModel):
    """Task response model"""
    task_id: str = Field(..., description="Unique task identifier")
    swarm_id: str = Field(..., description="Swarm identifier")
    status: TaskStatus = Field(..., description="Current task status")
    created_at: datetime = Field(..., description="Creation timestamp")
    task_type: str = Field(..., description="Task type")
    complexity_level: int = Field(..., description="Task complexity level")
    accuracy_requirement: float = Field(..., description="Required accuracy")
    deadline: Optional[datetime] = Field(None, description="Task deadline")
    priority: int = Field(..., description="Task priority")


class TaskExecutionRequest(BaseModel):
    """Request to execute a task"""
    task_id: str = Field(..., description="Task identifier")
    execution_mode: str = Field(default="swarm", description="Execution mode")
    validation_level: str = Field(default="high", description="Validation level")
    consensus_requirement: ConsensusLevel = Field(default=ConsensusLevel.SUPER_MAJORITY, description="Consensus requirement")


# ============================================================================
# AGENT MODELS
# ============================================================================

class AgentCreateRequest(BaseModel):
    """Request to create a new agent"""
    agent_id: str = Field(..., description="Unique agent identifier")
    role: AgentRole = Field(..., description="Agent role")
    capabilities: List[AgentCapabilityModel] = Field(..., description="Agent capabilities")
    specialization: Optional[str] = Field(None, description="Agent specialization")
    performance_threshold: float = Field(default=0.9, ge=0.0, le=1.0, description="Performance threshold")


class AgentResponse(BaseModel):
    """Agent response model"""
    agent_id: str = Field(..., description="Agent identifier")
    role: AgentRole = Field(..., description="Agent role")
    status: str = Field(..., description="Agent status")
    capabilities: List[AgentCapabilityModel] = Field(..., description="Agent capabilities")
    performance_metrics: Dict[str, float] = Field(..., description="Performance metrics")
    last_active: datetime = Field(..., description="Last activity timestamp")


class AgentPerformanceMetrics(BaseModel):
    """Agent performance metrics"""
    agent_id: str = Field(..., description="Agent identifier")
    total_tasks: int = Field(..., description="Total tasks processed")
    successful_tasks: int = Field(..., description="Successful tasks")
    accuracy_rate: float = Field(..., ge=0.0, le=1.0, description="Accuracy rate")
    average_confidence: float = Field(..., ge=0.0, le=1.0, description="Average confidence")
    processing_time: float = Field(..., description="Average processing time")
    error_rate: float = Field(..., ge=0.0, le=1.0, description="Error rate")
    last_updated: datetime = Field(..., description="Last update timestamp")


# ============================================================================
# CONSENSUS AND VALIDATION MODELS
# ============================================================================

class ConsensusResultResponse(BaseModel):
    """Consensus result response model"""
    task_id: str = Field(..., description="Task identifier")
    consensus_level: str = Field(..., description="Achieved consensus level")
    agreement_percentage: float = Field(..., ge=0.0, le=100.0, description="Agreement percentage")
    final_result: Any = Field(..., description="Final consensus result")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence")
    accuracy_score: float = Field(..., ge=0.0, le=1.0, description="Accuracy score")
    validation_summary: Dict[str, Any] = Field(..., description="Validation summary")
    dissenting_opinions: List[Dict[str, Any]] = Field(..., description="Dissenting opinions")
    consensus_agents: List[str] = Field(..., description="Agents that reached consensus")
    timestamp: datetime = Field(..., description="Consensus timestamp")


class ValidationResult(BaseModel):
    """Validation result model"""
    validation_method: ValidationMethod = Field(..., description="Validation method used")
    validation_score: float = Field(..., ge=0.0, le=1.0, description="Validation score")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Validation confidence")
    details: Dict[str, Any] = Field(..., description="Validation details")
    timestamp: datetime = Field(..., description="Validation timestamp")


class ConsensusBuildingRequest(BaseModel):
    """Request to build consensus"""
    task_id: str = Field(..., description="Task identifier")
    agent_results: List[Dict[str, Any]] = Field(..., description="Agent results")
    consensus_level: ConsensusLevel = Field(..., description="Required consensus level")
    validation_methods: List[ValidationMethod] = Field(..., description="Validation methods to use")


# ============================================================================
# SWARM CONFIGURATION MODELS
# ============================================================================

class SwarmConfigRequest(BaseModel):
    """Request to configure swarm settings"""
    swarm_id: str = Field(..., description="Swarm identifier")
    accuracy_requirement: Optional[float] = Field(None, ge=0.0, le=1.0, description="Accuracy requirement")
    consensus_level: Optional[ConsensusLevel] = Field(None, description="Consensus level")
    max_agents: Optional[int] = Field(None, ge=1, le=100, description="Maximum agents")
    validation_methods: Optional[List[ValidationMethod]] = Field(None, description="Validation methods")
    performance_threshold: Optional[float] = Field(None, ge=0.0, le=1.0, description="Performance threshold")
    auto_scaling: Optional[bool] = Field(None, description="Enable auto-scaling")
    monitoring_enabled: Optional[bool] = Field(None, description="Enable monitoring")


class SwarmConfigResponse(BaseModel):
    """Swarm configuration response"""
    swarm_id: str = Field(..., description="Swarm identifier")
    configuration: Dict[str, Any] = Field(..., description="Current configuration")
    updated_at: datetime = Field(..., description="Last update timestamp")
    status: str = Field(..., description="Configuration status")


# ============================================================================
# BATCH OPERATION MODELS
# ============================================================================

class BatchTaskRequest(BaseModel):
    """Batch task request"""
    tasks: List[TaskCreateRequest] = Field(..., description="List of tasks to execute")
    execution_mode: str = Field(default="parallel", description="Execution mode")
    consensus_requirement: ConsensusLevel = Field(default=ConsensusLevel.SUPER_MAJORITY, description="Consensus requirement")
    validation_level: str = Field(default="high", description="Validation level")


class BatchTaskResponse(BaseModel):
    """Batch task response"""
    batch_id: str = Field(..., description="Batch identifier")
    total_tasks: int = Field(..., description="Total tasks in batch")
    completed_tasks: int = Field(..., description="Completed tasks")
    failed_tasks: int = Field(..., description="Failed tasks")
    results: List[Dict[str, Any]] = Field(..., description="Task results")
    overall_accuracy: float = Field(..., ge=0.0, le=1.0, description="Overall accuracy")
    processing_time: float = Field(..., description="Total processing time")
    timestamp: datetime = Field(..., description="Batch completion timestamp")


# ============================================================================
# HEALTH AND MONITORING MODELS
# ============================================================================

class SwarmHealthResponse(BaseModel):
    """Swarm health response"""
    swarm_id: str = Field(..., description="Swarm identifier")
    health_status: str = Field(..., description="Health status")
    health_score: float = Field(..., ge=0.0, le=100.0, description="Health score")
    issues: List[str] = Field(..., description="Health issues")
    metrics: Dict[str, Any] = Field(..., description="Health metrics")
    timestamp: datetime = Field(..., description="Health check timestamp")


class SwarmMonitoringConfig(BaseModel):
    """Swarm monitoring configuration"""
    monitoring_enabled: bool = Field(default=True, description="Enable monitoring")
    metrics_collection: bool = Field(default=True, description="Enable metrics collection")
    alerting_enabled: bool = Field(default=True, description="Enable alerting")
    health_check_interval: int = Field(default=60, ge=10, description="Health check interval in seconds")
    performance_threshold: float = Field(default=0.9, ge=0.0, le=1.0, description="Performance threshold")
    accuracy_threshold: float = Field(default=0.95, ge=0.0, le=1.0, description="Accuracy threshold")


# ============================================================================
# UTILITY MODELS
# ============================================================================

class SwarmTypeInfo(BaseModel):
    """Swarm type information"""
    type: str = Field(..., description="Swarm type")
    name: str = Field(..., description="Swarm type name")
    description: str = Field(..., description="Swarm type description")
    architecture: str = Field(..., description="Default architecture")
    agent_count: int = Field(..., description="Default agent count")
    capabilities: List[str] = Field(..., description="Default capabilities")


class ValidationMethodInfo(BaseModel):
    """Validation method information"""
    method: str = Field(..., description="Validation method")
    name: str = Field(..., description="Method name")
    description: str = Field(..., description="Method description")
    accuracy_threshold: float = Field(..., description="Accuracy threshold")
    confidence_requirement: float = Field(..., description="Confidence requirement")


class ConsensusLevelInfo(BaseModel):
    """Consensus level information"""
    level: str = Field(..., description="Consensus level")
    name: str = Field(..., description="Level name")
    description: str = Field(..., description="Level description")
    threshold: int = Field(..., description="Agreement threshold percentage")
    accuracy_requirement: float = Field(..., description="Accuracy requirement")


# ============================================================================
# ERROR MODELS
# ============================================================================

class SwarmError(BaseModel):
    """Swarm error model"""
    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Error message")
    error_details: Dict[str, Any] = Field(..., description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp")
    swarm_id: Optional[str] = Field(None, description="Swarm identifier")
    task_id: Optional[str] = Field(None, description="Task identifier")


class ValidationError(BaseModel):
    """Validation error model"""
    validation_method: ValidationMethod = Field(..., description="Validation method")
    error_type: str = Field(..., description="Error type")
    error_message: str = Field(..., description="Error message")
    confidence: float = Field(..., description="Error confidence")
    suggestions: List[str] = Field(..., description="Improvement suggestions")
    timestamp: datetime = Field(..., description="Error timestamp")

"""
AI Component Orchestrator Models
Data models for advanced Smart Coding AI integration with all AI components
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


class ComponentStatus(str, Enum):
    """AI Component status options"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEGRADED = "degraded"
    ERROR = "error"
    UNKNOWN = "unknown"


class TaskPriority(str, Enum):
    """Task priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class IntegrationMode(str, Enum):
    """Integration mode options"""
    SYNC = "synchronous"
    ASYNC = "asynchronous"
    PARALLEL = "parallel"
    PIPELINE = "pipeline"


# ============================================================================
# COMPONENT MODELS
# ============================================================================

class AIComponentInfo(BaseModel):
    """AI Component information"""
    component_id: str = Field(..., description="Unique component identifier")
    name: str = Field(..., description="Component name")
    status: ComponentStatus = Field(..., description="Current component status")
    capabilities: List[str] = Field(..., description="List of component capabilities")
    error_count: int = Field(0, description="Number of errors encountered")
    success_count: int = Field(0, description="Number of successful operations")
    avg_response_time: float = Field(0.0, description="Average response time in seconds")
    last_health_check: Optional[datetime] = Field(None, description="Last health check timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional component metadata")


class ComponentRegistrationRequest(BaseModel):
    """Request to register an AI component"""
    component_id: str = Field(..., description="Unique component identifier")
    name: str = Field(..., description="Component name")
    capabilities: List[str] = Field(..., description="List of component capabilities")
    health_check_enabled: bool = Field(True, description="Whether health checks are enabled")


class ComponentRegistrationResponse(BaseModel):
    """Response for component registration"""
    success: bool = Field(..., description="Whether registration was successful")
    component_id: str = Field(..., description="Registered component identifier")
    name: str = Field(..., description="Component name")
    capabilities: List[str] = Field(..., description="Registered capabilities")
    registered_by: str = Field(..., description="User who registered the component")
    timestamp: datetime = Field(default_factory=datetime.now, description="Registration timestamp")


# ============================================================================
# TASK ORCHESTRATION MODELS
# ============================================================================

class IntegrationTaskInfo(BaseModel):
    """Integration task information"""
    task_id: str = Field(..., description="Unique task identifier")
    name: str = Field(..., description="Task name")
    description: str = Field(..., description="Task description")
    priority: TaskPriority = Field(..., description="Task priority level")
    mode: IntegrationMode = Field(..., description="Integration execution mode")
    status: str = Field(..., description="Current task status")
    required_components: List[str] = Field(..., description="Required component IDs")
    optional_components: List[str] = Field(default_factory=list, description="Optional component IDs")
    created_at: datetime = Field(..., description="Task creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Task start timestamp")
    completed_at: Optional[datetime] = Field(None, description="Task completion timestamp")
    error_message: Optional[str] = Field(None, description="Error message if task failed")
    retry_count: int = Field(0, description="Number of retries attempted")
    max_retries: int = Field(3, description="Maximum number of retries allowed")


class IntegrationTaskRequest(BaseModel):
    """Request to create an integration task"""
    name: str = Field(..., description="Task name")
    description: str = Field(..., description="Task description")
    priority: TaskPriority = Field(TaskPriority.MEDIUM, description="Task priority")
    mode: IntegrationMode = Field(IntegrationMode.PARALLEL, description="Integration mode")
    required_components: List[str] = Field(..., description="Required component IDs")
    optional_components: List[str] = Field(default_factory=list, description="Optional component IDs")
    input_data: Dict[str, Any] = Field(default_factory=dict, description="Input data for the task")
    timeout_seconds: int = Field(60, description="Task timeout in seconds")
    max_retries: int = Field(3, description="Maximum number of retries")


class IntegrationTaskResponse(BaseModel):
    """Response for integration task execution"""
    success: bool = Field(..., description="Whether task execution was successful")
    task_id: str = Field(..., description="Task identifier")
    task_name: str = Field(..., description="Task name")
    status: str = Field(..., description="Final task status")
    result: Dict[str, Any] = Field(..., description="Task execution result")
    executed_by: str = Field(..., description="User who executed the task")
    timestamp: datetime = Field(default_factory=datetime.now, description="Execution timestamp")


class IntelligentTaskRequest(BaseModel):
    """Request for intelligent task routing"""
    task_description: str = Field(..., description="Description of the task to perform")
    user_context: Dict[str, Any] = Field(default_factory=dict, description="User context information")
    priority: Optional[TaskPriority] = Field(None, description="Task priority (auto-determined if not specified)")


class TaskAnalysis(BaseModel):
    """Task analysis result"""
    capabilities_needed: List[str] = Field(..., description="Required capabilities")
    complexity: str = Field(..., description="Task complexity level")
    estimated_duration: int = Field(..., description="Estimated duration in seconds")
    requires_human_input: bool = Field(False, description="Whether task requires human input")
    data_sensitivity: str = Field("low", description="Data sensitivity level")


class ComponentSelection(BaseModel):
    """Component selection result"""
    required: List[str] = Field(..., description="Required component IDs")
    optional: List[str] = Field(..., description="Optional component IDs")
    capability_match: Dict[str, List[str]] = Field(..., description="Capability matches per component")


class IntelligentTaskResponse(BaseModel):
    """Response for intelligent task routing"""
    success: bool = Field(..., description="Whether task routing was successful")
    task_analysis: TaskAnalysis = Field(..., description="Task analysis result")
    selected_components: ComponentSelection = Field(..., description="Selected components")
    execution_result: Dict[str, Any] = Field(..., description="Task execution result")
    routed_by: str = Field(..., description="User who routed the task")
    timestamp: datetime = Field(default_factory=datetime.now, description="Routing timestamp")


# ============================================================================
# WORKFLOW MODELS
# ============================================================================

class WorkflowStepInfo(BaseModel):
    """Workflow step information"""
    step_id: str = Field(..., description="Unique step identifier")
    name: str = Field(..., description="Step name")
    component_id: str = Field(..., description="Component to execute the step")
    operation: str = Field(..., description="Operation to perform")
    timeout_seconds: int = Field(30, description="Step timeout in seconds")
    status: str = Field("pending", description="Step execution status")


class WorkflowStepRequest(BaseModel):
    """Request to create a workflow step"""
    name: str = Field(..., description="Step name")
    component_id: str = Field(..., description="Component to execute the step")
    operation: str = Field(..., description="Operation to perform")
    input_mapping: Dict[str, str] = Field(default_factory=dict, description="Input data mapping")
    output_mapping: Dict[str, str] = Field(default_factory=dict, description="Output data mapping")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Step execution conditions")
    timeout_seconds: int = Field(30, description="Step timeout in seconds")


class WorkflowInfo(BaseModel):
    """Workflow information"""
    workflow_id: str = Field(..., description="Unique workflow identifier")
    workflow_name: str = Field(..., description="Workflow name")
    steps_count: int = Field(..., description="Number of steps in workflow")
    steps: List[WorkflowStepInfo] = Field(..., description="Workflow steps")


class WorkflowRequest(BaseModel):
    """Request to create a workflow"""
    workflow_name: str = Field(..., description="Name of the workflow")
    steps: List[WorkflowStepRequest] = Field(..., description="List of workflow steps")


class WorkflowResponse(BaseModel):
    """Response for workflow creation"""
    success: bool = Field(..., description="Whether workflow creation was successful")
    workflow_id: str = Field(..., description="Created workflow identifier")
    workflow_name: str = Field(..., description="Workflow name")
    steps_count: int = Field(..., description="Number of steps in workflow")
    created_by: str = Field(..., description="User who created the workflow")
    timestamp: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class WorkflowExecutionRequest(BaseModel):
    """Request to execute a workflow"""
    workflow_id: str = Field(..., description="Workflow identifier to execute")
    input_data: Dict[str, Any] = Field(..., description="Input data for workflow execution")
    context_id: Optional[str] = Field(None, description="Cross-component context ID")


class WorkflowExecutionResponse(BaseModel):
    """Response for workflow execution"""
    success: bool = Field(..., description="Whether workflow execution was successful")
    workflow_id: str = Field(..., description="Executed workflow identifier")
    execution_result: Dict[str, Any] = Field(..., description="Workflow execution result")
    executed_by: str = Field(..., description="User who executed the workflow")
    timestamp: datetime = Field(default_factory=datetime.now, description="Execution timestamp")


# ============================================================================
# CROSS-COMPONENT CONTEXT MODELS
# ============================================================================

class CrossComponentContextInfo(BaseModel):
    """Cross-component context information"""
    context_id: str = Field(..., description="Unique context identifier")
    session_id: str = Field(..., description="Session identifier")
    user_id: str = Field(..., description="User identifier")
    created_at: datetime = Field(..., description="Context creation timestamp")
    last_updated: datetime = Field(..., description="Last update timestamp")
    expires_at: Optional[datetime] = Field(None, description="Context expiration timestamp")
    shared_data_keys: List[str] = Field(default_factory=list, description="Keys of shared data")


class CrossComponentContextRequest(BaseModel):
    """Request to create cross-component context"""
    session_id: str = Field(..., description="Session identifier")
    user_id: str = Field(..., description="User identifier")
    expires_in_seconds: int = Field(3600, description="Context expiration time in seconds")


class CrossComponentContextResponse(BaseModel):
    """Response for cross-component context creation"""
    success: bool = Field(..., description="Whether context creation was successful")
    context_id: str = Field(..., description="Created context identifier")
    session_id: str = Field(..., description="Session identifier")
    user_id: str = Field(..., description="User identifier")
    expires_in_seconds: int = Field(..., description="Context expiration time")
    created_by: str = Field(..., description="User who created the context")
    timestamp: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class DataSharingRequest(BaseModel):
    """Request to share data across components"""
    context_id: str = Field(..., description="Cross-component context ID")
    component_id: str = Field(..., description="Component ID sharing the data")
    data: Dict[str, Any] = Field(..., description="Data to share")


class DataSharingResponse(BaseModel):
    """Response for data sharing"""
    success: bool = Field(..., description="Whether data sharing was successful")
    context_id: str = Field(..., description="Context identifier")
    component_id: str = Field(..., description="Component identifier")
    shared_by: str = Field(..., description="User who shared the data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Sharing timestamp")


class SharedDataResponse(BaseModel):
    """Response for shared data retrieval"""
    success: bool = Field(..., description="Whether data retrieval was successful")
    context_id: str = Field(..., description="Context identifier")
    component_id: Optional[str] = Field(None, description="Component identifier (if specific)")
    shared_data: Dict[str, Any] = Field(..., description="Retrieved shared data")
    retrieved_by: str = Field(..., description="User who retrieved the data")
    timestamp: datetime = Field(default_factory=datetime.now, description="Retrieval timestamp")


# ============================================================================
# ORCHESTRATOR STATUS MODELS
# ============================================================================

class OrchestratorStatistics(BaseModel):
    """Orchestrator statistics"""
    total_tasks: int = Field(0, description="Total number of tasks")
    successful_tasks: int = Field(0, description="Number of successful tasks")
    failed_tasks: int = Field(0, description="Number of failed tasks")
    active_components: int = Field(0, description="Number of active components")
    total_contexts: int = Field(0, description="Total number of contexts")
    avg_task_duration: float = Field(0.0, description="Average task duration in seconds")


class OrchestratorStatus(BaseModel):
    """Orchestrator status information"""
    components: Dict[str, AIComponentInfo] = Field(..., description="Component information")
    active_tasks: int = Field(0, description="Number of active tasks")
    task_history: int = Field(0, description="Number of tasks in history")
    cross_contexts: int = Field(0, description="Number of cross-component contexts")
    workflows: int = Field(0, description="Number of workflows")
    statistics: OrchestratorStatistics = Field(..., description="Orchestrator statistics")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")


class OrchestratorCapabilities(BaseModel):
    """Orchestrator capabilities"""
    component_management: Dict[str, bool] = Field(..., description="Component management capabilities")
    task_orchestration: Dict[str, bool] = Field(..., description="Task orchestration capabilities")
    workflow_management: Dict[str, bool] = Field(..., description="Workflow management capabilities")
    cross_component_features: Dict[str, bool] = Field(..., description="Cross-component features")
    monitoring_analytics: Dict[str, bool] = Field(..., description="Monitoring and analytics capabilities")
    integration_modes: List[str] = Field(..., description="Available integration modes")
    task_priorities: List[str] = Field(..., description="Available task priorities")


class OrchestratorCapabilitiesResponse(BaseModel):
    """Response for orchestrator capabilities"""
    success: bool = Field(True, description="Whether request was successful")
    capabilities: OrchestratorCapabilities = Field(..., description="Orchestrator capabilities")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


# ============================================================================
# ERROR MODELS
# ============================================================================

class OrchestratorError(BaseModel):
    """Orchestrator error information"""
    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Error message")
    component_id: Optional[str] = Field(None, description="Related component ID")
    task_id: Optional[str] = Field(None, description="Related task ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class OrchestratorErrorResponse(BaseModel):
    """Error response for orchestrator operations"""
    success: bool = Field(False, description="Whether the operation was successful")
    error: OrchestratorError = Field(..., description="Error details")
    suggestions: List[str] = Field(default_factory=list, description="Suggested solutions")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error response timestamp")


# ============================================================================
# HEALTH CHECK MODELS
# ============================================================================

class HealthCheckRequest(BaseModel):
    """Request for health check"""
    component_ids: Optional[List[str]] = Field(None, description="Specific components to check (all if not specified)")
    force_check: bool = Field(False, description="Force health check even if recently performed")


class HealthCheckResponse(BaseModel):
    """Response for health check"""
    success: bool = Field(..., description="Whether health check was successful")
    message: str = Field(..., description="Health check message")
    initiated_by: str = Field(..., description="User who initiated the health check")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")


class ComponentHealthStatus(BaseModel):
    """Individual component health status"""
    component_id: str = Field(..., description="Component identifier")
    status: ComponentStatus = Field(..., description="Component health status")
    response_time: float = Field(0.0, description="Health check response time")
    error_message: Optional[str] = Field(None, description="Error message if unhealthy")
    last_check: datetime = Field(..., description="Last health check timestamp")


class HealthStatusResponse(BaseModel):
    """Response for health status"""
    success: bool = Field(True, description="Whether request was successful")
    overall_status: str = Field(..., description="Overall system health status")
    components: List[ComponentHealthStatus] = Field(..., description="Individual component health")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")

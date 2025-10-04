"""
Smart Coding AI Integration Models
Data models for AI component integration
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


class IntegrationStatus(str, Enum):
    """Integration status options"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    INITIALIZING = "initializing"


class OperationType(str, Enum):
    """Operation type options"""
    VOICE_TO_CODE = "voice_to_code"
    AI_ASSISTANT_CHAT = "ai_assistant_chat"
    TASK_ORCHESTRATION = "task_orchestration"
    SESSION_MANAGEMENT = "session_management"
    CODE_GENERATION = "code_generation"
    CODE_ANALYSIS = "code_analysis"


class TaskAction(str, Enum):
    """Task action options"""
    SCAFFOLD = "scaffold"
    IMPLEMENT = "implement"
    OPTIMIZE = "optimize"
    TEST = "test"
    DEBUG = "debug"
    REFACTOR = "refactor"


# ============================================================================
# INTEGRATION CONTEXT MODELS
# ============================================================================

class AIIntegrationContextRequest(BaseModel):
    """Request for AI integration context"""
    user_id: str = Field(..., description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    project_id: Optional[str] = Field(None, description="Project identifier")
    operation_type: Optional[OperationType] = Field(None, description="Type of operation")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class AIIntegrationContextResponse(BaseModel):
    """Response for AI integration context"""
    context_id: str = Field(..., description="Unique context identifier")
    user_id: str = Field(..., description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    project_id: Optional[str] = Field(None, description="Project identifier")
    operation_type: Optional[OperationType] = Field(None, description="Type of operation")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


# ============================================================================
# VOICE-TO-CODE MODELS
# ============================================================================

class VoiceToCodeRequest(BaseModel):
    """Request for voice-to-code processing"""
    audio_data: str = Field(..., description="Base64 encoded audio data")
    language: str = Field("en", description="Audio language code")
    user_id: str = Field(..., description="User identifier")
    project_id: Optional[str] = Field(None, description="Project identifier")
    context_type: str = Field("code_generation", description="Context type for processing")
    include_transcript: bool = Field(True, description="Include transcript in response")
    enhance_with_memory: bool = Field(True, description="Enhance with memory context")


class VoiceToCodeResponse(BaseModel):
    """Response for voice-to-code processing"""
    response_id: str = Field(..., description="Unique response identifier")
    transcript: Optional[str] = Field(None, description="Transcribed text")
    generated_code: str = Field(..., description="Generated code")
    confidence: float = Field(..., description="Confidence score")
    orchestration_plan: Optional[Dict[str, Any]] = Field(None, description="Orchestration plan")
    memory_context: Optional[Dict[str, Any]] = Field(None, description="Memory context used")
    integrity_validation: Optional[Dict[str, Any]] = Field(None, description="Integrity validation result")
    suggestions: List[Dict[str, Any]] = Field(default_factory=list, description="Code suggestions")
    follow_up_questions: List[str] = Field(default_factory=list, description="Follow-up questions")
    integration_metadata: Dict[str, Any] = Field(default_factory=dict, description="Integration metadata")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class TextToCodeRequest(BaseModel):
    """Request for text-to-code processing"""
    transcript: str = Field(..., description="Text transcript to convert to code")
    language: str = Field("en", description="Text language code")
    user_id: str = Field(..., description="User identifier")
    project_id: Optional[str] = Field(None, description="Project identifier")
    context_type: str = Field("code_generation", description="Context type for processing")
    enhance_with_memory: bool = Field(True, description="Enhance with memory context")


class TextToCodeResponse(BaseModel):
    """Response for text-to-code processing"""
    response_id: str = Field(..., description="Unique response identifier")
    generated_code: str = Field(..., description="Generated code")
    confidence: float = Field(..., description="Confidence score")
    orchestration_plan: Optional[Dict[str, Any]] = Field(None, description="Orchestration plan")
    memory_context: Optional[Dict[str, Any]] = Field(None, description="Memory context used")
    suggestions: List[Dict[str, Any]] = Field(default_factory=list, description="Code suggestions")
    follow_up_questions: List[str] = Field(default_factory=list, description="Follow-up questions")
    integration_metadata: Dict[str, Any] = Field(default_factory=dict, description="Integration metadata")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


# ============================================================================
# AI ASSISTANT INTEGRATION MODELS
# ============================================================================

class AIAssistantChatRequest(BaseModel):
    """Request for AI assistant chat"""
    message: str = Field(..., description="Chat message")
    user_id: str = Field(..., description="User identifier")
    session_id: Optional[str] = Field(None, description="Session identifier")
    project_id: Optional[str] = Field(None, description="Project identifier")
    assistant_name: str = Field("SmartCodingAssistant", description="Assistant name")
    include_code_analysis: bool = Field(True, description="Include code analysis if relevant")
    enhance_with_smart_coding: bool = Field(True, description="Enhance with Smart Coding AI")


class AIAssistantChatResponse(BaseModel):
    """Response for AI assistant chat"""
    response_id: str = Field(..., description="Unique response identifier")
    response: str = Field(..., description="Assistant response")
    confidence: float = Field(..., description="Confidence score")
    code_related: bool = Field(..., description="Whether message was code-related")
    code_snippets: List[Dict[str, Any]] = Field(default_factory=list, description="Relevant code snippets")
    follow_up_questions: List[str] = Field(default_factory=list, description="Follow-up questions")
    assistant_enhanced: bool = Field(False, description="Whether enhanced by Smart Coding AI")
    supporting_responses: Dict[str, Any] = Field(default_factory=dict, description="Supporting response data")
    integration_metadata: Dict[str, Any] = Field(default_factory=dict, description="Integration metadata")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


# ============================================================================
# TASK ORCHESTRATION MODELS
# ============================================================================

class CodingTask(BaseModel):
    """Individual coding task"""
    task_id: str = Field(..., description="Unique task identifier")
    action: TaskAction = Field(..., description="Task action type")
    description: str = Field(..., description="Task description")
    confidence: float = Field(..., description="Task confidence score")
    priority: int = Field(1, description="Task priority (1-5)")
    dependencies: List[str] = Field(default_factory=list, description="Task dependencies")
    estimated_duration: Optional[int] = Field(None, description="Estimated duration in seconds")


class TaskOrchestrationRequest(BaseModel):
    """Request for task orchestration"""
    task_description: str = Field(..., description="High-level task description")
    user_id: str = Field(..., description="User identifier")
    project_id: Optional[str] = Field(None, description="Project identifier")
    context_type: str = Field("orchestration", description="Context type")
    max_tasks: int = Field(10, description="Maximum number of tasks to generate")
    include_optimization: bool = Field(True, description="Include optimization tasks")
    include_testing: bool = Field(True, description="Include testing tasks")


class TaskExecutionResult(BaseModel):
    """Result of task execution"""
    task_id: str = Field(..., description="Task identifier")
    action: TaskAction = Field(..., description="Task action")
    result: Dict[str, Any] = Field(..., description="Execution result")
    success: bool = Field(..., description="Whether task succeeded")
    confidence: float = Field(..., description="Result confidence")
    duration: Optional[float] = Field(None, description="Execution duration in seconds")
    error: Optional[str] = Field(None, description="Error message if failed")


class TaskOrchestrationResponse(BaseModel):
    """Response for task orchestration"""
    response_id: str = Field(..., description="Unique response identifier")
    orchestration_plan: Dict[str, Any] = Field(..., description="Original orchestration plan")
    coding_tasks: List[CodingTask] = Field(..., description="Generated coding tasks")
    execution_results: List[TaskExecutionResult] = Field(..., description="Task execution results")
    combined_result: Dict[str, Any] = Field(..., description="Combined execution result")
    success_rate: float = Field(..., description="Overall success rate")
    confidence: float = Field(..., description="Overall confidence score")
    recommendations: List[str] = Field(default_factory=list, description="Recommendations")
    integration_metadata: Dict[str, Any] = Field(default_factory=dict, description="Integration metadata")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


# ============================================================================
# SESSION MANAGEMENT MODELS
# ============================================================================

class IntegrationSessionRequest(BaseModel):
    """Request for integration session"""
    user_id: str = Field(..., description="User identifier")
    project_id: Optional[str] = Field(None, description="Project identifier")
    session_name: Optional[str] = Field(None, description="Custom session name")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Session metadata")


class IntegrationSessionResponse(BaseModel):
    """Response for integration session"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User identifier")
    project_id: Optional[str] = Field(None, description="Project identifier")
    session_name: Optional[str] = Field(None, description="Session name")
    status: IntegrationStatus = Field(IntegrationStatus.ACTIVE, description="Session status")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last activity timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Session metadata")


class SessionUpdateRequest(BaseModel):
    """Request for session update"""
    updates: Dict[str, Any] = Field(..., description="Updates to apply")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class SessionUpdateResponse(BaseModel):
    """Response for session update"""
    session_id: str = Field(..., description="Session identifier")
    updated: bool = Field(..., description="Whether update was successful")
    updated_fields: List[str] = Field(..., description="List of updated fields")
    timestamp: datetime = Field(default_factory=datetime.now, description="Update timestamp")


# ============================================================================
# INTEGRATION STATUS MODELS
# ============================================================================

class ComponentStatus(BaseModel):
    """Status of an integration component"""
    name: str = Field(..., description="Component name")
    status: IntegrationStatus = Field(..., description="Component status")
    performance_score: Optional[float] = Field(None, description="Performance score")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Component metadata")


class IntegrationStatusResponse(BaseModel):
    """Response for integration status"""
    overall_status: IntegrationStatus = Field(..., description="Overall integration status")
    components: List[ComponentStatus] = Field(..., description="Component statuses")
    active_sessions: int = Field(..., description="Number of active sessions")
    performance_metrics: Dict[str, Any] = Field(default_factory=dict, description="Performance metrics")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")


class IntegrationCapability(BaseModel):
    """Integration capability"""
    name: str = Field(..., description="Capability name")
    description: str = Field(..., description="Capability description")
    endpoints: List[str] = Field(..., description="Related API endpoints")
    features: List[str] = Field(..., description="Capability features")
    status: IntegrationStatus = Field(IntegrationStatus.ACTIVE, description="Capability status")


class IntegrationCapabilitiesResponse(BaseModel):
    """Response for integration capabilities"""
    capabilities: List[IntegrationCapability] = Field(..., description="Available capabilities")
    integration_components: List[str] = Field(..., description="Integrated components")
    version: str = Field("1.0.0", description="Integration version")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


# ============================================================================
# ERROR MODELS
# ============================================================================

class IntegrationError(BaseModel):
    """Integration error model"""
    error_id: str = Field(..., description="Unique error identifier")
    error_type: str = Field(..., description="Error type")
    error_message: str = Field(..., description="Error message")
    component: Optional[str] = Field(None, description="Component where error occurred")
    context: Optional[Dict[str, Any]] = Field(None, description="Error context")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")


class IntegrationErrorResponse(BaseModel):
    """Response for integration errors"""
    success: bool = Field(False, description="Whether operation was successful")
    error: IntegrationError = Field(..., description="Error details")
    suggestions: List[str] = Field(default_factory=list, description="Error resolution suggestions")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

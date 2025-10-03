"""
AI Agent Models - Advanced AI Agent System with Zero-Cost Infrastructure
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4


class AgentType(str, Enum):
    """Types of AI Agents"""
    VOICE_ASSISTANT = "voice_assistant"
    CODE_GENERATOR = "code_generator"
    TASK_AUTOMATOR = "task_automator"
    DATA_ANALYZER = "data_analyzer"
    CONTENT_CREATOR = "content_creator"
    CUSTOMER_SUPPORT = "customer_support"
    SYSTEM_MONITOR = "system_monitor"
    PERSONAL_ASSISTANT = "personal_assistant"


class AgentStatus(str, Enum):
    """Agent operational status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRAINING = "training"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AgentCapability(str, Enum):
    """Agent capabilities"""
    VOICE_PROCESSING = "voice_processing"
    NATURAL_LANGUAGE = "natural_language"
    CODE_GENERATION = "code_generation"
    DATA_PROCESSING = "data_processing"
    API_INTEGRATION = "api_integration"
    WEB_SCRAPING = "web_scraping"
    EMAIL_AUTOMATION = "email_automation"
    SCHEDULING = "scheduling"
    ANALYSIS = "analysis"
    CREATIVE_WRITING = "creative_writing"
    TRANSLATION = "translation"
    IMAGE_PROCESSING = "image_processing"
    AUTOMATION = "automation"


class AgentPriority(str, Enum):
    """Agent priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(str, Enum):
    """Task execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskType(str, Enum):
    """Types of tasks agents can perform"""
    VOICE_TO_CODE = "voice_to_code"
    DATA_ANALYSIS = "data_analysis"
    CONTENT_GENERATION = "content_generation"
    API_CALL = "api_call"
    WEB_SEARCH = "web_search"
    EMAIL_SEND = "email_send"
    SCHEDULE_TASK = "schedule_task"
    SYSTEM_CHECK = "system_check"
    USER_QUERY = "user_query"
    AUTOMATION_WORKFLOW = "automation_workflow"


class AgentConfig(BaseModel):
    """Configuration for AI Agents"""
    model_provider: str = Field(default="local", description="AI model provider (local, openai, anthropic, etc.)")
    model_name: str = Field(default="llama-2-7b", description="Specific model to use")
    max_tokens: int = Field(default=2048, description="Maximum tokens for responses")
    temperature: float = Field(default=0.7, description="Creativity level (0-1)")
    system_prompt: str = Field(default="", description="System prompt for the agent")
    memory_limit: int = Field(default=1000, description="Maximum conversation memory")
    response_timeout: int = Field(default=30, description="Response timeout in seconds")
    retry_attempts: int = Field(default=3, description="Number of retry attempts")
    enable_streaming: bool = Field(default=True, description="Enable streaming responses")
    enable_memory: bool = Field(default=True, description="Enable conversation memory")
    enable_learning: bool = Field(default=True, description="Enable learning from interactions")
    custom_instructions: str = Field(default="", description="Custom instructions for the agent")
    safety_guardrails: bool = Field(default=True, description="Enable safety guardrails")
    cost_limits: Dict[str, float] = Field(default_factory=dict, description="Cost limits per operation")


class AgentMemory(BaseModel):
    """Agent memory structure"""
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)
    learned_patterns: List[Dict[str, Any]] = Field(default_factory=list)
    user_preferences: Dict[str, Any] = Field(default_factory=dict)
    context_data: Dict[str, Any] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class AgentMetrics(BaseModel):
    """Agent performance metrics"""
    total_interactions: int = Field(default=0)
    successful_tasks: int = Field(default=0)
    failed_tasks: int = Field(default=0)
    average_response_time: float = Field(default=0.0)
    user_satisfaction: float = Field(default=0.0)
    cost_per_interaction: float = Field(default=0.0)
    total_cost: float = Field(default=0.0)
    last_activity: Optional[datetime] = None
    uptime_percentage: float = Field(default=100.0)


class AgentDefinition(BaseModel):
    """AI Agent definition"""
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    type: AgentType = Field(..., description="Agent type")
    status: AgentStatus = Field(default=AgentStatus.INACTIVE)
    priority: AgentPriority = Field(default=AgentPriority.MEDIUM)
    
    # Capabilities
    capabilities: List[AgentCapability] = Field(default_factory=list)
    
    # Configuration
    config: AgentConfig = Field(default_factory=AgentConfig)
    
    # Memory and Learning
    memory: AgentMemory = Field(default_factory=AgentMemory)
    
    # Performance Metrics
    metrics: AgentMetrics = Field(default_factory=AgentMetrics)
    
    # Ownership and Access
    user_id: Optional[UUID] = None
    team_id: Optional[UUID] = None
    is_public: bool = Field(default=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: Optional[datetime] = None
    
    # Zero-cost infrastructure settings
    use_local_models: bool = Field(default=True)
    fallback_providers: List[str] = Field(default_factory=list)
    resource_limits: Dict[str, Any] = Field(default_factory=dict)
    
    @validator('capabilities')
    def validate_capabilities(cls, v):
        if not v:
            return [AgentCapability.NATURAL_LANGUAGE]
        return v


class TaskDefinition(BaseModel):
    """Task definition for AI Agents"""
    id: UUID = Field(default_factory=uuid4)
    agent_id: UUID = Field(..., description="ID of the agent handling this task")
    user_id: UUID = Field(..., description="ID of the user who created the task")
    
    # Task Details
    type: TaskType = Field(..., description="Type of task")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed task description")
    input_data: Dict[str, Any] = Field(default_factory=dict)
    expected_output: Optional[str] = None
    
    # Execution Details
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    priority: AgentPriority = Field(default=AgentPriority.MEDIUM)
    
    # Timing
    created_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    scheduled_for: Optional[datetime] = None
    
    # Results
    output_data: Dict[str, Any] = Field(default_factory=dict)
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    
    # Zero-cost settings
    use_local_processing: bool = Field(default=True)
    max_cost: float = Field(default=0.0)  # Zero cost by default
    resource_usage: Dict[str, Any] = Field(default_factory=dict)


class AgentInteraction(BaseModel):
    """Record of agent interactions"""
    id: UUID = Field(default_factory=uuid4)
    agent_id: UUID = Field(..., description="ID of the agent")
    user_id: UUID = Field(..., description="ID of the user")
    task_id: Optional[UUID] = None
    
    # Interaction Details
    input_message: str = Field(..., description="User input")
    output_message: str = Field(..., description="Agent response")
    interaction_type: str = Field(default="conversation")
    
    # Context
    context_data: Dict[str, Any] = Field(default_factory=dict)
    session_id: Optional[str] = None
    
    # Performance
    response_time: float = Field(default=0.0)
    tokens_used: int = Field(default=0)
    cost: float = Field(default=0.0)
    
    # Feedback
    user_rating: Optional[int] = None  # 1-5 scale
    user_feedback: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AgentWorkflow(BaseModel):
    """Workflow definition for agent automation"""
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="Workflow name")
    description: str = Field(..., description="Workflow description")
    
    # Workflow Configuration
    trigger_type: str = Field(default="manual")  # manual, scheduled, event
    trigger_config: Dict[str, Any] = Field(default_factory=dict)
    
    # Steps
    steps: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Agent Assignment
    primary_agent_id: UUID = Field(..., description="Primary agent for workflow")
    fallback_agent_ids: List[UUID] = Field(default_factory=list)
    
    # Execution Settings
    max_concurrent: int = Field(default=1)
    timeout: int = Field(default=300)  # 5 minutes
    retry_policy: Dict[str, Any] = Field(default_factory=dict)
    
    # Status
    is_active: bool = Field(default=True)
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    
    # Zero-cost settings
    use_local_agents_only: bool = Field(default=True)
    cost_limit: float = Field(default=0.0)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AgentRequest(BaseModel):
    """Request to interact with an AI Agent"""
    agent_id: UUID = Field(..., description="ID of the agent to interact with")
    message: str = Field(..., description="Message to send to the agent")
    context: Dict[str, Any] = Field(default_factory=dict)
    session_id: Optional[str] = None
    use_streaming: bool = Field(default=True)
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None


class AgentResponse(BaseModel):
    """Response from an AI Agent"""
    success: bool = Field(default=True)
    message: str = Field(..., description="Agent response message")
    agent_id: UUID = Field(..., description="ID of the responding agent")
    interaction_id: UUID = Field(..., description="ID of the interaction record")
    
    # Performance Data
    response_time: float = Field(default=0.0)
    tokens_used: int = Field(default=0)
    cost: float = Field(default=0.0)
    
    # Additional Data
    suggestions: List[str] = Field(default_factory=list)
    follow_up_questions: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Error Handling
    error_code: Optional[str] = None
    error_message: Optional[str] = None


class AgentCreationRequest(BaseModel):
    """Request to create a new AI Agent"""
    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="Agent description")
    type: AgentType = Field(..., description="Agent type")
    capabilities: List[AgentCapability] = Field(default_factory=list)
    config: Optional[AgentConfig] = None
    system_prompt: Optional[str] = None
    custom_instructions: Optional[str] = None
    is_public: bool = Field(default=False)


class AgentUpdateRequest(BaseModel):
    """Request to update an AI Agent"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[AgentStatus] = None
    capabilities: Optional[List[AgentCapability]] = None
    config: Optional[AgentConfig] = None
    system_prompt: Optional[str] = None
    custom_instructions: Optional[str] = None
    is_public: Optional[bool] = None


class AgentListResponse(BaseModel):
    """Response containing list of agents"""
    agents: List[AgentDefinition]
    total: int
    page: int
    limit: int


class TaskListResponse(BaseModel):
    """Response containing list of tasks"""
    tasks: List[TaskDefinition]
    total: int
    page: int
    limit: int


class InteractionListResponse(BaseModel):
    """Response containing list of interactions"""
    interactions: List[AgentInteraction]
    total: int
    page: int
    limit: int


class AgentAnalytics(BaseModel):
    """Analytics data for agents"""
    agent_id: UUID
    period: str  # daily, weekly, monthly
    
    # Usage Statistics
    total_interactions: int = 0
    unique_users: int = 0
    average_response_time: float = 0.0
    
    # Performance Metrics
    success_rate: float = 0.0
    user_satisfaction: float = 0.0
    
    # Cost Analysis
    total_cost: float = 0.0
    cost_per_interaction: float = 0.0
    
    # Capability Usage
    capability_usage: Dict[str, int] = Field(default_factory=dict)
    
    # Zero-cost Metrics
    local_model_usage: int = 0
    cloud_model_usage: int = 0
    cost_savings: float = 0.0


class ZeroCostConfig(BaseModel):
    """Configuration for zero-cost infrastructure"""
    # Local Model Settings
    use_local_llm: bool = Field(default=True)
    local_model_path: str = Field(default="./models/")
    local_model_name: str = Field(default="llama-2-7b-chat")
    
    # Fallback Settings
    enable_fallback: bool = Field(default=False)
    fallback_providers: List[str] = Field(default_factory=list)
    fallback_threshold: float = Field(default=0.1)  # Max cost before fallback
    
    # Resource Management
    max_memory_usage: int = Field(default=2048)  # MB
    max_cpu_usage: float = Field(default=80.0)  # Percentage
    max_storage_usage: int = Field(default=10240)  # MB
    
    # Optimization
    enable_model_caching: bool = Field(default=True)
    enable_response_caching: bool = Field(default=True)
    cache_ttl: int = Field(default=3600)  # seconds
    
    # Monitoring
    track_resource_usage: bool = Field(default=True)
    alert_on_high_usage: bool = Field(default=True)
    usage_thresholds: Dict[str, float] = Field(default_factory=dict)

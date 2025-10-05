"""
Tool Integration Models for CognOmega Platform
Defines data structures for external tool integration management
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, validator
from enum import Enum
from datetime import datetime
import uuid

class ToolType(str, Enum):
    """Types of tools that can be integrated"""
    AI_SERVICE = "ai_service"
    DATABASE = "database"
    API = "api"
    FILE_SYSTEM = "file_system"
    MESSAGE_QUEUE = "message_queue"
    CACHE = "cache"
    AUTHENTICATION = "authentication"
    PAYMENT = "payment"
    EMAIL = "email"
    SMS = "sms"
    VOICE = "voice"
    VIDEO = "video"
    IMAGE = "image"
    DOCUMENT = "document"
    WORKFLOW = "workflow"
    MONITORING = "monitoring"
    ANALYTICS = "analytics"
    CUSTOM = "custom"

class ToolStatus(str, Enum):
    """Status of tool integration"""
    REGISTERED = "registered"
    CONFIGURED = "configured"
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    DISABLED = "disabled"
    MAINTENANCE = "maintenance"

class ToolPriority(str, Enum):
    """Priority level for tool execution"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BACKGROUND = "background"

class AuthenticationType(str, Enum):
    """Types of authentication for tools"""
    API_KEY = "api_key"
    OAUTH = "oauth"
    BASIC_AUTH = "basic_auth"
    BEARER_TOKEN = "bearer_token"
    JWT = "jwt"
    CERTIFICATE = "certificate"
    NONE = "none"

class ToolCapability(str, Enum):
    """Capabilities that tools can provide"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    LIST = "list"
    SEARCH = "search"
    TRANSFORM = "transform"
    VALIDATE = "validate"
    MONITOR = "monitor"
    ANALYZE = "analyze"
    GENERATE = "generate"
    PROCESS = "process"
    STREAM = "stream"
    BATCH = "batch"

class ToolConfiguration(BaseModel):
    """Configuration for a tool"""
    name: str = Field(..., description="Name of the configuration")
    value: Any = Field(..., description="Configuration value")
    encrypted: bool = Field(default=False, description="Whether the value is encrypted")
    required: bool = Field(default=True, description="Whether this configuration is required")
    description: Optional[str] = Field(None, description="Description of the configuration")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ToolAuthentication(BaseModel):
    """Authentication configuration for a tool"""
    auth_type: AuthenticationType = Field(..., description="Type of authentication")
    credentials: Dict[str, Any] = Field(default_factory=dict, description="Authentication credentials")
    encrypted: bool = Field(default=True, description="Whether credentials are encrypted")
    expires_at: Optional[datetime] = Field(None, description="When credentials expire")
    refresh_token: Optional[str] = Field(None, description="Refresh token for OAuth")
    scopes: List[str] = Field(default_factory=list, description="OAuth scopes")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ToolEndpoint(BaseModel):
    """Endpoint configuration for a tool"""
    name: str = Field(..., description="Name of the endpoint")
    url: str = Field(..., description="Endpoint URL")
    method: str = Field(default="GET", description="HTTP method")
    headers: Dict[str, str] = Field(default_factory=dict, description="Default headers")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    retry_count: int = Field(default=3, description="Number of retries")
    rate_limit: Optional[int] = Field(None, description="Rate limit per minute")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ToolMetadata(BaseModel):
    """Metadata for a tool"""
    version: str = Field(default="1.0.0", description="Tool version")
    description: Optional[str] = Field(None, description="Tool description")
    author: Optional[str] = Field(None, description="Tool author")
    license: Optional[str] = Field(None, description="Tool license")
    documentation_url: Optional[str] = Field(None, description="Documentation URL")
    support_url: Optional[str] = Field(None, description="Support URL")
    tags: List[str] = Field(default_factory=list, description="Tool tags")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ToolIntegration(BaseModel):
    """Complete tool integration definition"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique tool ID")
    name: str = Field(..., description="Tool name")
    type: ToolType = Field(..., description="Tool type")
    status: ToolStatus = Field(default=ToolStatus.REGISTERED, description="Tool status")
    priority: ToolPriority = Field(default=ToolPriority.MEDIUM, description="Tool priority")
    
    # Configuration
    configuration: List[ToolConfiguration] = Field(default_factory=list, description="Tool configuration")
    authentication: Optional[ToolAuthentication] = Field(None, description="Authentication configuration")
    endpoints: List[ToolEndpoint] = Field(default_factory=list, description="Tool endpoints")
    
    # Capabilities
    capabilities: List[ToolCapability] = Field(default_factory=list, description="Tool capabilities")
    input_schema: Optional[Dict[str, Any]] = Field(None, description="Input schema")
    output_schema: Optional[Dict[str, Any]] = Field(None, description="Output schema")
    
    # Metadata
    metadata: ToolMetadata = Field(default_factory=ToolMetadata, description="Tool metadata")
    
    # Runtime information
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    last_used: Optional[datetime] = Field(None, description="Last usage timestamp")
    usage_count: int = Field(default=0, description="Usage count")
    
    # Performance metrics
    avg_response_time: Optional[float] = Field(None, description="Average response time in seconds")
    success_rate: Optional[float] = Field(None, description="Success rate percentage")
    error_count: int = Field(default=0, description="Error count")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ToolExecutionRequest(BaseModel):
    """Request for tool execution"""
    tool_id: str = Field(..., description="ID of the tool to execute")
    operation: str = Field(..., description="Operation to perform")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Execution parameters")
    context: Optional[Dict[str, Any]] = Field(None, description="Execution context")
    timeout: Optional[int] = Field(None, description="Execution timeout in seconds")
    priority: Optional[ToolPriority] = Field(None, description="Execution priority")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ToolExecutionResult(BaseModel):
    """Result of tool execution"""
    execution_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Execution ID")
    tool_id: str = Field(..., description="Tool ID")
    operation: str = Field(..., description="Executed operation")
    status: str = Field(..., description="Execution status")
    result: Optional[Any] = Field(None, description="Execution result")
    error: Optional[str] = Field(None, description="Error message if failed")
    
    # Performance metrics
    start_time: datetime = Field(..., description="Execution start time")
    end_time: Optional[datetime] = Field(None, description="Execution end time")
    duration: Optional[float] = Field(None, description="Execution duration in seconds")
    
    # Metadata
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Execution parameters")
    context: Optional[Dict[str, Any]] = Field(None, description="Execution context")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ToolHealthCheck(BaseModel):
    """Health check result for a tool"""
    tool_id: str = Field(..., description="Tool ID")
    status: ToolStatus = Field(..., description="Health status")
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    last_check: datetime = Field(default_factory=datetime.utcnow, description="Last check timestamp")
    error_message: Optional[str] = Field(None, description="Error message if unhealthy")
    details: Dict[str, Any] = Field(default_factory=dict, description="Additional health details")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ToolRegistry(BaseModel):
    """Registry of all tool integrations"""
    tools: Dict[str, ToolIntegration] = Field(default_factory=dict, description="Registered tools")
    categories: Dict[str, List[str]] = Field(default_factory=dict, description="Tools by category")
    capabilities: Dict[str, List[str]] = Field(default_factory=dict, description="Tools by capability")
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last registry update")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ToolIntegrationStats(BaseModel):
    """Statistics for tool integration system"""
    total_tools: int = Field(default=0, description="Total number of tools")
    active_tools: int = Field(default=0, description="Number of active tools")
    tools_by_type: Dict[str, int] = Field(default_factory=dict, description="Tools by type")
    tools_by_status: Dict[str, int] = Field(default_factory=dict, description="Tools by status")
    total_executions: int = Field(default=0, description="Total executions")
    successful_executions: int = Field(default=0, description="Successful executions")
    failed_executions: int = Field(default=0, description="Failed executions")
    avg_response_time: float = Field(default=0.0, description="Average response time")
    success_rate: float = Field(default=0.0, description="Success rate percentage")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Request/Response models for API endpoints
class ToolRegistrationRequest(BaseModel):
    """Request to register a new tool"""
    name: str = Field(..., description="Tool name")
    type: ToolType = Field(..., description="Tool type")
    configuration: List[ToolConfiguration] = Field(default_factory=list, description="Tool configuration")
    authentication: Optional[ToolAuthentication] = Field(None, description="Authentication configuration")
    endpoints: List[ToolEndpoint] = Field(default_factory=list, description="Tool endpoints")
    capabilities: List[ToolCapability] = Field(default_factory=list, description="Tool capabilities")
    metadata: Optional[ToolMetadata] = Field(None, description="Tool metadata")

class ToolUpdateRequest(BaseModel):
    """Request to update a tool"""
    name: Optional[str] = Field(None, description="Tool name")
    status: Optional[ToolStatus] = Field(None, description="Tool status")
    priority: Optional[ToolPriority] = Field(None, description="Tool priority")
    configuration: Optional[List[ToolConfiguration]] = Field(None, description="Tool configuration")
    authentication: Optional[ToolAuthentication] = Field(None, description="Authentication configuration")
    endpoints: Optional[List[ToolEndpoint]] = Field(None, description="Tool endpoints")
    capabilities: Optional[List[ToolCapability]] = Field(None, description="Tool capabilities")
    metadata: Optional[ToolMetadata] = Field(None, description="Tool metadata")

class ToolExecutionResponse(BaseModel):
    """Response for tool execution"""
    execution_id: str = Field(..., description="Execution ID")
    status: str = Field(..., description="Execution status")
    result: Optional[Any] = Field(None, description="Execution result")
    error: Optional[str] = Field(None, description="Error message if failed")
    duration: Optional[float] = Field(None, description="Execution duration")

class ToolListResponse(BaseModel):
    """Response for tool listing"""
    tools: List[ToolIntegration] = Field(..., description="List of tools")
    total: int = Field(..., description="Total number of tools")
    page: int = Field(default=1, description="Current page")
    page_size: int = Field(default=10, description="Page size")

class ToolHealthResponse(BaseModel):
    """Response for tool health check"""
    tools: List[ToolHealthCheck] = Field(..., description="Health check results")
    overall_status: str = Field(..., description="Overall system status")
    healthy_tools: int = Field(..., description="Number of healthy tools")
    unhealthy_tools: int = Field(..., description="Number of unhealthy tools")

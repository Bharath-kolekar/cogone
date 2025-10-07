"""
Tool Integration Router for CognOmega Platform
API endpoints for managing external tool integrations
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

from ..models.tool_integration_models import (
    ToolIntegration, ToolType, ToolStatus, ToolPriority, ToolCapability,
    ToolRegistrationRequest, ToolUpdateRequest, ToolExecutionRequest,
    ToolExecutionResponse, ToolListResponse, ToolHealthResponse,
    ToolIntegrationStats, ToolMetadata
)
from ..services.tool_integration_manager import ToolIntegrationManager, GroqConfig
from ..core.dependencies import get_current_user, require_permission

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tools", tags=["Tool Integration"])

# Global tool integration manager instance
tool_manager: Optional[ToolIntegrationManager] = None

def get_tool_manager() -> ToolIntegrationManager:
    """Get tool integration manager instance"""
    global tool_manager
    if tool_manager is None:
        # Initialize with Groq configuration
        groq_config = GroqConfig(
            api_key="your-groq-api-key",  # This should come from environment
            model="llama3-8b-8192",
            max_tokens=8000,
            temperature=0.7
        )
        tool_manager = ToolIntegrationManager(groq_config)
    return tool_manager

@router.post("/register", response_model=Dict[str, Any])
async def register_tool(
    request: ToolRegistrationRequest,
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Register a new tool integration"""
    try:
        # Create tool integration from request
        tool = ToolIntegration(
            name=request.name,
            type=request.type,
            configuration=request.configuration,
            authentication=request.authentication,
            endpoints=request.endpoints,
            capabilities=request.capabilities,
            metadata=request.metadata or ToolMetadata()
        )
        
        # Register the tool
        success = await manager.register_tool(tool)
        
        if success:
            return {
                "success": True,
                "message": f"Tool '{request.name}' registered successfully",
                "tool_id": tool.id,
                "tool": tool.dict()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to register tool"
            )
            
    except Exception as e:
        logger.error(f"Tool registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool registration failed: {str(e)}"
        )

@router.put("/{tool_id}", response_model=Dict[str, Any])
async def update_tool(
    tool_id: str,
    request: ToolUpdateRequest,
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Update an existing tool integration"""
    try:
        if tool_id not in manager.registry.tools:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_id} not found"
            )
        
        tool = manager.registry.tools[tool_id]
        
        # Update tool fields
        if request.name is not None:
            tool.name = request.name
        if request.status is not None:
            tool.status = request.status
        if request.priority is not None:
            tool.priority = request.priority
        if request.configuration is not None:
            tool.configuration = request.configuration
        if request.authentication is not None:
            tool.authentication = request.authentication
        if request.endpoints is not None:
            tool.endpoints = request.endpoints
        if request.capabilities is not None:
            tool.capabilities = request.capabilities
        if request.metadata is not None:
            tool.metadata = request.metadata
        
        tool.updated_at = datetime.utcnow()
        
        # Perform health check after update
        await manager._perform_health_check(tool_id)
        
        return {
            "success": True,
            "message": f"Tool '{tool.name}' updated successfully",
            "tool": tool.dict()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tool update failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool update failed: {str(e)}"
        )

@router.delete("/{tool_id}", response_model=Dict[str, Any])
async def unregister_tool(
    tool_id: str,
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Unregister a tool integration"""
    try:
        if tool_id not in manager.registry.tools:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_id} not found"
            )
        
        tool_name = manager.registry.tools[tool_id].name
        success = await manager.unregister_tool(tool_id)
        
        if success:
            return {
                "success": True,
                "message": f"Tool '{tool_name}' unregistered successfully"
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to unregister tool"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tool unregistration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool unregistration failed: {str(e)}"
        )

@router.get("/", response_model=ToolListResponse)
async def list_tools(
    tool_type: Optional[ToolType] = Query(None, description="Filter by tool type"),
    status: Optional[ToolStatus] = Query(None, description="Filter by tool status"),
    capability: Optional[ToolCapability] = Query(None, description="Filter by capability"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Page size"),
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """List all tool integrations with optional filtering"""
    try:
        tools = list(manager.registry.tools.values())
        
        # Apply filters
        if tool_type:
            tools = [t for t in tools if t.type == tool_type]
        if status:
            tools = [t for t in tools if t.status == status]
        if capability:
            tools = [t for t in tools if capability in t.capabilities]
        
        # Pagination
        total = len(tools)
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_tools = tools[start_idx:end_idx]
        
        return ToolListResponse(
            tools=paginated_tools,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Tool listing failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool listing failed: {str(e)}"
        )

@router.get("/{tool_id}", response_model=ToolIntegration)
async def get_tool(
    tool_id: str,
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Get a specific tool integration"""
    try:
        if tool_id not in manager.registry.tools:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_id} not found"
            )
        
        return manager.registry.tools[tool_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tool retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool retrieval failed: {str(e)}"
        )

@router.post("/{tool_id}/execute", response_model=ToolExecutionResponse)
async def execute_tool(
    tool_id: str,
    request: ToolExecutionRequest,
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Execute a tool operation"""
    try:
        # Set tool_id from URL parameter
        request.tool_id = tool_id
        
        # Execute the tool
        result = await manager.execute_tool(request)
        
        return ToolExecutionResponse(
            execution_id=result.execution_id,
            status=result.status,
            result=result.result,
            error=result.error,
            duration=result.duration
        )
        
    except Exception as e:
        logger.error(f"Tool execution failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool execution failed: {str(e)}"
        )

@router.get("/{tool_id}/health", response_model=Dict[str, Any])
async def check_tool_health(
    tool_id: str,
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Check health of a specific tool"""
    try:
        if tool_id not in manager.registry.tools:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tool {tool_id} not found"
            )
        
        # Perform health check
        health_check = await manager._perform_health_check(tool_id)
        
        return {
            "tool_id": tool_id,
            "status": health_check.status,
            "response_time": health_check.response_time,
            "last_check": health_check.last_check,
            "error_message": health_check.error_message,
            "details": health_check.details
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Tool health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool health check failed: {str(e)}"
        )

@router.get("/health/all", response_model=ToolHealthResponse)
async def check_all_tools_health(
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Check health of all tools"""
    try:
        health_checks = []
        
        for tool_id in manager.registry.tools:
            health_check = await manager._perform_health_check(tool_id)
            health_checks.append(health_check)
        
        # Calculate overall status
        healthy_count = len([h for h in health_checks if h.status == ToolStatus.ACTIVE])
        unhealthy_count = len(health_checks) - healthy_count
        
        overall_status = "healthy" if unhealthy_count == 0 else "degraded" if healthy_count > 0 else "unhealthy"
        
        return ToolHealthResponse(
            tools=health_checks,
            overall_status=overall_status,
            healthy_tools=healthy_count,
            unhealthy_tools=unhealthy_count
        )
        
    except Exception as e:
        logger.error(f"All tools health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"All tools health check failed: {str(e)}"
        )

@router.get("/capabilities/{capability}", response_model=List[ToolIntegration])
async def get_tools_by_capability(
    capability: ToolCapability,
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Get tools that have a specific capability"""
    try:
        tools = await manager.get_tool_by_capability(capability)
        return tools
        
    except Exception as e:
        logger.error(f"Tools by capability retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tools by capability retrieval failed: {str(e)}"
        )

@router.get("/active", response_model=List[ToolIntegration])
async def get_active_tools(
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Get all active tools"""
    try:
        tools = await manager.get_active_tools()
        return tools
        
    except Exception as e:
        logger.error(f"Active tools retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Active tools retrieval failed: {str(e)}"
        )

@router.get("/stats", response_model=ToolIntegrationStats)
async def get_tool_stats(
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Get tool integration statistics"""
    try:
        stats = await manager.get_tool_stats()
        return stats
        
    except Exception as e:
        logger.error(f"Tool stats retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool stats retrieval failed: {str(e)}"
        )

@router.get("/categories", response_model=Dict[str, List[str]])
async def get_tool_categories(
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Get tools organized by categories"""
    try:
        return manager.registry.categories
        
    except Exception as e:
        logger.error(f"Tool categories retrieval failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool categories retrieval failed: {str(e)}"
        )

@router.post("/ai/generate", response_model=Dict[str, Any])
async def generate_with_ai(
    prompt: str = Query(..., description="Prompt for AI generation"),
    model: Optional[str] = Query(None, description="AI model to use"),
    temperature: Optional[float] = Query(0.7, ge=0.0, le=2.0, description="Temperature for generation"),
    max_tokens: Optional[int] = Query(None, description="Maximum tokens to generate"),
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Generate content using AI service (prioritizes Groq)"""
    try:
        # Prepare parameters
        parameters = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Try Groq first (primary AI service)
        groq_request = ToolExecutionRequest(
            tool_id="groq-ai-service",
            operation="generate",
            parameters=parameters
        )
        
        try:
            result = await manager.execute_tool(groq_request)
            if result.status == "completed":
                return {
                    "success": True,
                    "service": "groq",
                    "model": "llama3-8b-8192",
                    "content": result.result,
                    "execution_time": result.duration
                }
        except Exception as e:
            logger.warning(f"Groq service failed, trying fallback: {str(e)}")
        
        # Fallback to Ollama (local service)
        ollama_request = ToolExecutionRequest(
            tool_id="ollama-service",
            operation="generate",
            parameters=parameters
        )
        
        try:
            result = await manager.execute_tool(ollama_request)
            if result.status == "completed":
                return {
                    "success": True,
                    "service": "ollama",
                    "model": "llama3:8b-instruct-q4_K_M",
                    "content": result.result,
                    "execution_time": result.duration
                }
        except Exception as e:
            logger.warning(f"Ollama service failed: {str(e)}")
        
        # All services failed
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="All AI services are currently unavailable"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI generation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI generation failed: {str(e)}"
        )

@router.post("/ai/chat", response_model=Dict[str, Any])
async def chat_with_ai(
    messages: List[Dict[str, str]] = Body(..., description="Chat messages"),
    model: Optional[str] = Query(None, description="AI model to use"),
    temperature: Optional[float] = Query(0.7, ge=0.0, le=2.0, description="Temperature for generation"),
    current_user: dict = Depends(get_current_user),
    manager: ToolIntegrationManager = Depends(get_tool_manager)
):
    """Chat with AI service using message history"""
    try:
        # Prepare parameters
        parameters = {
            "messages": messages,
            "temperature": temperature
        }
        
        # Try Groq first
        groq_request = ToolExecutionRequest(
            tool_id="groq-ai-service",
            operation="chat",
            parameters=parameters
        )
        
        try:
            result = await manager.execute_tool(groq_request)
            if result.status == "completed":
                return {
                    "success": True,
                    "service": "groq",
                    "model": "llama3-8b-8192",
                    "response": result.result,
                    "execution_time": result.duration
                }
        except Exception as e:
            logger.warning(f"Groq chat failed, trying fallback: {str(e)}")
        
        # Fallback to other services if needed
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI chat service is currently unavailable"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI chat failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI chat failed: {str(e)}"
        )

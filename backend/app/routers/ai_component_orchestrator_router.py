"""
AI Component Orchestrator Router
Advanced API endpoints for deep Smart Coding AI integration with all AI components
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field

from app.services.ai_component_orchestrator import (
    ai_component_orchestrator, IntegrationTask, WorkflowStep,
    TaskPriority, IntegrationMode, ComponentStatus
)
from app.routers.auth import AuthDependencies
from app.models.user import User

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/ai-orchestrator", tags=["AI Component Orchestrator"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ComponentRegistrationRequest(BaseModel):
    """Request to register an AI component"""
    component_id: str = Field(..., description="Unique component identifier")
    name: str = Field(..., description="Component name")
    capabilities: List[str] = Field(..., description="List of component capabilities")
    health_check_enabled: bool = Field(True, description="Whether health checks are enabled")


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


class IntelligentTaskRequest(BaseModel):
    """Request for intelligent task routing"""
    task_description: str = Field(..., description="Description of the task to perform")
    user_context: Dict[str, Any] = Field(default_factory=dict, description="User context information")
    priority: Optional[TaskPriority] = Field(None, description="Task priority (auto-determined if not specified)")


class WorkflowStepRequest(BaseModel):
    """Request to create a workflow step"""
    name: str = Field(..., description="Step name")
    component_id: str = Field(..., description="Component to execute the step")
    operation: str = Field(..., description="Operation to perform")
    input_mapping: Dict[str, str] = Field(default_factory=dict, description="Input data mapping")
    output_mapping: Dict[str, str] = Field(default_factory=dict, description="Output data mapping")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Step execution conditions")
    timeout_seconds: int = Field(30, description="Step timeout in seconds")


class WorkflowRequest(BaseModel):
    """Request to create a workflow"""
    workflow_name: str = Field(..., description="Name of the workflow")
    steps: List[WorkflowStepRequest] = Field(..., description="List of workflow steps")


class CrossComponentContextRequest(BaseModel):
    """Request to create cross-component context"""
    session_id: str = Field(..., description="Session identifier")
    user_id: str = Field(..., description="User identifier")
    expires_in_seconds: int = Field(3600, description="Context expiration time in seconds")


class DataSharingRequest(BaseModel):
    """Request to share data across components"""
    context_id: str = Field(..., description="Cross-component context ID")
    component_id: str = Field(..., description="Component ID sharing the data")
    data: Dict[str, Any] = Field(..., description="Data to share")


# ============================================================================
# COMPONENT MANAGEMENT ENDPOINTS
# ============================================================================

@router.post("/components/register")
async def register_component(
    request: ComponentRegistrationRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Register a new AI component with the orchestrator"""
    try:
        # Register the component
        ai_component_orchestrator._register_component(
            component_id=request.component_id,
            name=request.name,
            capabilities=request.capabilities
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "component_id": request.component_id,
                "name": request.name,
                "capabilities": request.capabilities,
                "registered_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to register component", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register component: {e}"
        )


@router.get("/components")
async def get_components(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get all registered AI components"""
    try:
        components = {}
        for component_id, component in ai_component_orchestrator.components.items():
            components[component_id] = {
                "name": component.name,
                "status": component.status.value,
                "capabilities": component.capabilities,
                "error_count": component.error_count,
                "success_count": component.success_count,
                "avg_response_time": component.avg_response_time,
                "last_health_check": component.last_health_check.isoformat() if component.last_health_check else None,
                "metadata": component.metadata
            }
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "components": components,
                "total_count": len(components),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get components", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get components: {e}"
        )


@router.get("/components/{component_id}/status")
async def get_component_status(
    component_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get status of a specific AI component"""
    try:
        if component_id not in ai_component_orchestrator.components:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Component not found"
            )
        
        component = ai_component_orchestrator.components[component_id]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "component_id": component_id,
                "name": component.name,
                "status": component.status.value,
                "capabilities": component.capabilities,
                "error_count": component.error_count,
                "success_count": component.success_count,
                "avg_response_time": component.avg_response_time,
                "last_health_check": component.last_health_check.isoformat() if component.last_health_check else None,
                "metadata": component.metadata
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get component status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get component status: {e}"
        )


@router.post("/components/health-check")
async def perform_health_check(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Perform health check on all components"""
    try:
        # Start health check in background
        background_tasks.add_task(ai_component_orchestrator._perform_health_checks)
        
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "success": True,
                "message": "Health check initiated",
                "initiated_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to perform health check", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to perform health check: {e}"
        )


# ============================================================================
# TASK ORCHESTRATION ENDPOINTS
# ============================================================================

@router.post("/tasks/execute")
async def execute_integration_task(
    request: IntegrationTaskRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Execute an integration task"""
    try:
        # Create integration task
        task = IntegrationTask(
            task_id=f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{current_user.id[:8]}",
            name=request.name,
            description=request.description,
            priority=request.priority,
            mode=request.mode,
            required_components=request.required_components,
            optional_components=request.optional_components,
            input_data=request.input_data,
            timeout_seconds=request.timeout_seconds,
            max_retries=request.max_retries
        )
        
        # Execute task
        result = await ai_component_orchestrator.execute_integration_task(task)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "task_id": task.task_id,
                "task_name": task.name,
                "status": task.status,
                "result": result,
                "executed_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to execute integration task", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute integration task: {e}"
        )


@router.post("/tasks/intelligent-route")
async def route_task_intelligently(
    request: IntelligentTaskRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Intelligently route and execute a task"""
    try:
        # Add user context
        user_context = request.user_context.copy()
        user_context["user_id"] = current_user.id
        user_context["user_name"] = current_user.username
        
        # Route task intelligently
        result = await ai_component_orchestrator.route_task_intelligently(
            request.task_description,
            user_context
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "task_analysis": result["task_analysis"],
                "selected_components": result["selected_components"],
                "execution_result": result["execution_result"],
                "routed_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to route task intelligently", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to route task intelligently: {e}"
        )


@router.get("/tasks/active")
async def get_active_tasks(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get all active integration tasks"""
    try:
        active_tasks = []
        for task_id, task in ai_component_orchestrator.active_tasks.items():
            active_tasks.append({
                "task_id": task.task_id,
                "name": task.name,
                "description": task.description,
                "priority": task.priority.value,
                "mode": task.mode.value,
                "status": task.status,
                "required_components": task.required_components,
                "optional_components": task.optional_components,
                "created_at": task.created_at.isoformat(),
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "retry_count": task.retry_count,
                "max_retries": task.max_retries
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "active_tasks": active_tasks,
                "total_count": len(active_tasks),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get active tasks", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active tasks: {e}"
        )


@router.get("/tasks/history")
async def get_task_history(
    limit: int = 50,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get task execution history"""
    try:
        history = ai_component_orchestrator.task_history[-limit:]
        
        task_history = []
        for task in history:
            task_history.append({
                "task_id": task.task_id,
                "name": task.name,
                "description": task.description,
                "priority": task.priority.value,
                "mode": task.mode.value,
                "status": task.status,
                "created_at": task.created_at.isoformat(),
                "started_at": task.started_at.isoformat() if task.started_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "error_message": task.error_message,
                "retry_count": task.retry_count
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "task_history": task_history,
                "total_count": len(task_history),
                "limit": limit,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get task history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task history: {e}"
        )


# ============================================================================
# WORKFLOW MANAGEMENT ENDPOINTS
# ============================================================================

@router.post("/workflows/create")
async def create_workflow(
    request: WorkflowRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Create a new workflow"""
    try:
        # Convert workflow step requests to workflow steps
        steps = []
        for step_request in request.steps:
            step = WorkflowStep(
                step_id=f"step_{len(steps)}",
                name=step_request.name,
                component_id=step_request.component_id,
                operation=step_request.operation,
                input_mapping=step_request.input_mapping,
                output_mapping=step_request.output_mapping,
                conditions=step_request.conditions,
                timeout_seconds=step_request.timeout_seconds
            )
            steps.append(step)
        
        # Create workflow
        workflow_id = await ai_component_orchestrator.create_workflow(
            request.workflow_name,
            steps
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "workflow_id": workflow_id,
                "workflow_name": request.workflow_name,
                "steps_count": len(steps),
                "created_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to create workflow", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create workflow: {e}"
        )


@router.post("/workflows/{workflow_id}/execute")
async def execute_workflow(
    workflow_id: str,
    input_data: Dict[str, Any],
    context_id: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Execute a workflow"""
    try:
        # Execute workflow
        result = await ai_component_orchestrator.execute_workflow(
            workflow_id,
            input_data,
            context_id
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "workflow_id": workflow_id,
                "execution_result": result,
                "executed_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to execute workflow", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute workflow: {e}"
        )


@router.get("/workflows")
async def get_workflows(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get all workflows"""
    try:
        workflows = {}
        for workflow_id, steps in ai_component_orchestrator.workflows.items():
            workflows[workflow_id] = {
                "workflow_id": workflow_id,
                "steps_count": len(steps),
                "steps": [
                    {
                        "step_id": step.step_id,
                        "name": step.name,
                        "component_id": step.component_id,
                        "operation": step.operation,
                        "timeout_seconds": step.timeout_seconds
                    }
                    for step in steps
                ]
            }
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "workflows": workflows,
                "total_count": len(workflows),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get workflows", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get workflows: {e}"
        )


# ============================================================================
# CROSS-COMPONENT CONTEXT ENDPOINTS
# ============================================================================

@router.post("/context/create")
async def create_cross_component_context(
    request: CrossComponentContextRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Create cross-component context for data sharing"""
    try:
        context_id = await ai_component_orchestrator.create_cross_component_context(
            request.session_id,
            request.user_id,
            request.expires_in_seconds
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "context_id": context_id,
                "session_id": request.session_id,
                "user_id": request.user_id,
                "expires_in_seconds": request.expires_in_seconds,
                "created_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to create cross-component context", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create cross-component context: {e}"
        )


@router.post("/context/share-data")
async def share_data_across_components(
    request: DataSharingRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Share data across AI components"""
    try:
        success = await ai_component_orchestrator.share_data_across_components(
            request.context_id,
            request.component_id,
            request.data
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to share data across components"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "context_id": request.context_id,
                "component_id": request.component_id,
                "shared_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to share data across components", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to share data across components: {e}"
        )


@router.get("/context/{context_id}/data")
async def get_shared_data(
    context_id: str,
    component_id: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get shared data from cross-component context"""
    try:
        shared_data = await ai_component_orchestrator.get_shared_data(
            context_id,
            component_id
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "context_id": context_id,
                "component_id": component_id,
                "shared_data": shared_data,
                "retrieved_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get shared data", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get shared data: {e}"
        )


# ============================================================================
# ORCHESTRATOR STATUS AND MONITORING ENDPOINTS
# ============================================================================

@router.get("/status")
async def get_orchestrator_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get orchestrator status and statistics"""
    try:
        status_info = await ai_component_orchestrator.get_orchestrator_status()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "orchestrator_status": status_info,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get orchestrator status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get orchestrator status: {e}"
        )


@router.get("/capabilities")
async def get_orchestrator_capabilities(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get orchestrator capabilities and features"""
    try:
        capabilities = {
            "component_management": {
                "register_components": True,
                "health_monitoring": True,
                "status_tracking": True,
                "capability_discovery": True
            },
            "task_orchestration": {
                "intelligent_routing": True,
                "parallel_execution": True,
                "pipeline_processing": True,
                "retry_mechanisms": True,
                "priority_handling": True
            },
            "workflow_management": {
                "workflow_creation": True,
                "step_orchestration": True,
                "conditional_execution": True,
                "data_mapping": True
            },
            "cross_component_features": {
                "context_sharing": True,
                "data_exchange": True,
                "session_management": True,
                "component_coordination": True
            },
            "monitoring_analytics": {
                "performance_tracking": True,
                "error_monitoring": True,
                "statistics_collection": True,
                "health_reporting": True
            },
            "integration_modes": [
                "synchronous",
                "asynchronous", 
                "parallel",
                "pipeline"
            ],
            "task_priorities": [
                "critical",
                "high",
                "medium",
                "low"
            ]
        }
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "capabilities": capabilities,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get orchestrator capabilities", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get orchestrator capabilities: {e}"
        )

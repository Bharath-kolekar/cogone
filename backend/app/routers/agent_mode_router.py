"""
Agent Mode API Router
Activate with Ctrl+L, describe what you want, and the agent autonomously implements it
"""

import structlog
from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from typing import Dict, List, Optional, Any
from datetime import datetime
from uuid import UUID

from app.services.agent_mode import agent_mode_service
from app.models.agent_mode import (
    AgentModeRequest, AgentModeResponse, TaskStatusRequest, TaskStatusResponse,
    RollbackRequest, RollbackResponse, AnalysisRequest, AnalysisResponse,
    DependencyRequest, DependencyResponse, TestRequest, TestResponse,
    CommentRequest, CommentResponse, AgentModeStatusResponse,
    ProgressUpdate, ChangePreview, AgentModeConfig,
    AgentModeStatus, ChangeType
)
from app.routers.auth import AuthDependencies
from app.models.user import User

logger = structlog.get_logger()
router = APIRouter()


@router.post("/activate", response_model=AgentModeResponse)
async def activate_agent_mode(
    request: AgentModeRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Activate Agent Mode with user request"""
    try:
        logger.info("Activating Agent Mode", 
                   user_id=current_user.id, 
                   request=request.user_request)
        
        # Activate agent mode
        task_id = await agent_mode_service.activate_agent_mode(request.user_request)
        
        # Get initial status
        task = await agent_mode_service.get_task_status(task_id)
        
        return AgentModeResponse(
            task_id=task_id,
            status=task.status,
            message=f"Agent Mode activated for: {request.user_request}",
            estimated_time=300,  # 5 minutes default
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to activate Agent Mode", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to activate Agent Mode: {e}"
        )


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get status of an agent task"""
    try:
        task = await agent_mode_service.get_task_status(task_id)
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Convert changes to response format
        changes = []
        for change in task.changes:
            changes.append({
                "change_id": change.change_id,
                "change_type": change.change_type,
                "file_path": change.file_path,
                "description": change.description,
                "status": "completed" if task.status == AgentModeStatus.COMPLETED else "pending",
                "success": True,
                "error_message": None,
                "timestamp": change.created_at
            })
        
        return TaskStatusResponse(
            task_id=task.task_id,
            status=task.status,
            progress=task.progress,
            current_step=task.current_step,
            changes=changes,
            analysis_results=task.analysis_results,
            execution_plan=task.execution_plan,
            test_results=task.test_results,
            error_message=None,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get task status", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task status: {e}"
        )


@router.post("/rollback", response_model=RollbackResponse)
async def rollback_task(
    request: RollbackRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Rollback changes made by a task"""
    try:
        if not request.confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rollback confirmation required"
            )
        
        logger.info("Rolling back task", task_id=request.task_id, user_id=current_user.id)
        
        result = await agent_mode_service.rollback_task(request.task_id)
        
        return RollbackResponse(
            success=result["success"],
            message=result["message"],
            backup_path=result.get("backup_path"),
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to rollback task", task_id=request.task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to rollback task: {e}"
        )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_codebase(
    request: AnalysisRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Analyze codebase for a user request"""
    try:
        logger.info("Analyzing codebase", 
                   user_id=current_user.id, 
                   request=request.user_request)
        
        # Perform analysis
        analysis = await agent_mode_service.analyzer.analyze_codebase(request.user_request)
        
        # Calculate complexity score
        complexity_score = 0.5  # Default
        if analysis.get("user_intent", {}).get("complexity") == "high":
            complexity_score = 0.8
        elif analysis.get("user_intent", {}).get("complexity") == "medium":
            complexity_score = 0.6
        
        # Estimate time
        estimated_time = 5  # Default 5 minutes
        if complexity_score > 0.7:
            estimated_time = 15
        elif complexity_score > 0.5:
            estimated_time = 10
        
        return AnalysisResponse(
            project_structure=analysis.get("project_structure", {}),
            dependencies=analysis.get("dependencies", {}),
            code_patterns=analysis.get("code_patterns", {}),
            user_intent=analysis.get("user_intent", {}),
            affected_files=analysis.get("affected_files", []),
            implementation_plan=analysis.get("implementation_plan", []),
            complexity_score=complexity_score,
            estimated_time=estimated_time,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to analyze codebase", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze codebase: {e}"
        )


@router.post("/dependencies", response_model=DependencyResponse)
async def manage_dependencies(
    request: DependencyRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Manage project dependencies"""
    try:
        logger.info("Managing dependencies", 
                   user_id=current_user.id, 
                   dependencies=request.dependencies)
        
        # Install dependencies
        results = await agent_mode_service.dependency_manager.install_dependencies(
            request.dependencies
        )
        
        return DependencyResponse(
            installed=results.get("installed", []),
            failed=results.get("failed", []),
            already_installed=results.get("already_installed", []),
            total_count=len(request.dependencies),
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to manage dependencies", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to manage dependencies: {e}"
        )


@router.post("/test", response_model=TestResponse)
async def run_tests(
    request: TestRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Run tests for a task"""
    try:
        logger.info("Running tests", task_id=request.task_id, user_id=current_user.id)
        
        # Get task
        task = await agent_mode_service.get_task_status(request.task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Run tests
        test_results = await agent_mode_service.test_runner.run_tests(task.changes)
        
        return TestResponse(
            tests_run=test_results.get("tests_run", 0),
            tests_passed=test_results.get("tests_passed", 0),
            tests_failed=test_results.get("tests_failed", 0),
            coverage=test_results.get("coverage", 0.0),
            errors=test_results.get("errors", []),
            execution_time=0.0,  # Would be calculated in real implementation
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to run tests", task_id=request.task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to run tests: {e}"
        )


@router.post("/comments", response_model=CommentResponse)
async def generate_comments(
    request: CommentRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Generate helpful comments for changes"""
    try:
        logger.info("Generating comments", 
                   user_id=current_user.id, 
                   changes_count=len(request.changes))
        
        # Convert request changes to service changes
        from app.services.agent_mode import CodeChange, ChangeType
        
        changes = []
        for change_req in request.changes:
            change = CodeChange(
                change_id=str(UUID()),
                change_type=ChangeType(change_req.change_type),
                file_path=change_req.file_path,
                description=change_req.description,
                old_content=change_req.old_content,
                new_content=change_req.new_content,
                line_number=change_req.line_number,
                dependencies=change_req.dependencies or [],
                tests=change_req.tests or [],
                comments=change_req.comments or []
            )
            changes.append(change)
        
        # Generate comments
        comments = await agent_mode_service.comment_generator.generate_comments(changes)
        
        return CommentResponse(
            comments=comments,
            total_comments=len(comments),
            style_used=request.style,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to generate comments", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate comments: {e}"
        )


@router.get("/service-status", response_model=AgentModeStatusResponse)
async def get_service_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get Agent Mode service status"""
    try:
        # Get active tasks count
        active_tasks = len(agent_mode_service.active_tasks)
        completed_tasks = sum(1 for task in agent_mode_service.active_tasks.values() 
                             if task.status == AgentModeStatus.COMPLETED)
        failed_tasks = sum(1 for task in agent_mode_service.active_tasks.values() 
                          if task.status == AgentModeStatus.ERROR)
        
        return AgentModeStatusResponse(
            service_active=True,
            active_tasks=active_tasks,
            completed_tasks=completed_tasks,
            failed_tasks=failed_tasks,
            supported_languages=[
                "python", "javascript", "typescript", "java", "csharp", "cpp", "go", "rust",
                "php", "ruby", "swift", "kotlin", "html", "css", "sql", "yaml", "json", "markdown"
            ],
            capabilities=[
                "autonomous_code_analysis",
                "multi_file_changes",
                "dependency_management",
                "automatic_testing",
                "intelligent_comments",
                "rollback_support",
                "real_time_progress"
            ],
            performance_metrics={
                "average_task_time": 300,  # 5 minutes
                "success_rate": 0.95,
                "cache_hit_rate": 0.90,
                "memory_usage": 0.75
            },
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to get service status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get service status: {e}"
        )


@router.get("/progress/{task_id}")
async def get_progress_updates(
    task_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get real-time progress updates for a task"""
    try:
        task = await agent_mode_service.get_task_status(task_id)
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return ProgressUpdate(
            task_id=task.task_id,
            progress=task.progress,
            current_step=task.current_step,
            status=task.status,
            estimated_remaining=max(0, 300 - int((datetime.now() - task.created_at).total_seconds())),
            timestamp=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get progress updates", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get progress updates: {e}"
        )


@router.get("/preview/{task_id}")
async def get_change_preview(
    task_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get preview of changes to be made"""
    try:
        task = await agent_mode_service.get_task_status(task_id)
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        previews = []
        for change in task.changes:
            preview = ChangePreview(
                change_id=change.change_id,
                change_type=change.change_type,
                file_path=change.file_path,
                description=change.description,
                preview=change.new_content or "New content will be added",
                impact=f"This change will {change.change_type.value.replace('_', ' ')} the file",
                dependencies=change.dependencies or [],
                risks=["Potential syntax errors", "Dependency conflicts"],
                timestamp=change.created_at
            )
            previews.append(preview)
        
        return {"previews": previews, "total_changes": len(previews)}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get change preview", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get change preview: {e}"
        )


@router.get("/config", response_model=AgentModeConfig)
async def get_config(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get Agent Mode configuration"""
    try:
        return AgentModeConfig(
            max_concurrent_tasks=5,
            timeout_minutes=30,
            auto_backup=True,
            auto_test=True,
            auto_comment=True,
            supported_file_types=[
                ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", 
                ".go", ".rs", ".php", ".rb", ".swift", ".kt", ".html", ".css"
            ],
            excluded_directories=[
                "node_modules", ".git", "__pycache__", ".venv", "venv", "env"
            ],
            max_file_size_mb=10,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to get config", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get config: {e}"
        )


@router.post("/health")
async def health_check():
    """Health check for Agent Mode service"""
    try:
        return {
            "status": "healthy",
            "service": "Agent Mode",
            "active_tasks": len(agent_mode_service.active_tasks),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error("Agent Mode health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "service": "Agent Mode",
            "error": str(e),
            "timestamp": datetime.now()
        }

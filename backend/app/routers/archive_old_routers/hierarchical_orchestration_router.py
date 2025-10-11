"""
Hierarchical Orchestration API Router
Exposes endpoints for the Hierarchical Orchestration Manager
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import Dict, List, Any, Optional
from datetime import datetime
import structlog

from app.services.hierarchical_orchestration_manager import (
    HierarchicalOrchestrationManager,
    OrchestrationTask,
    TaskComplexity,
    OrchestrationStrategy,
    OrchestrationLevel
)
from app.models.user import User
from app.core.dependencies import AuthDependencies

logger = structlog.get_logger()

router = APIRouter(prefix="/orchestration", tags=["Hierarchical Orchestration"])

# Initialize the hierarchical orchestration manager
hierarchical_manager = HierarchicalOrchestrationManager()


# ============================================================================
# TASK SUBMISSION AND MANAGEMENT
# ============================================================================

@router.post("/submit-task")
async def submit_orchestration_task(
    task_type: str,
    requirements: Dict[str, Any],
    complexity: TaskComplexity = TaskComplexity.MODERATE,
    priority: int = 5,
    user_id: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Submit a task for hierarchical orchestration"""
    try:
        task_id = await hierarchical_manager.submit_task(
            task_type=task_type,
            requirements=requirements,
            complexity=complexity,
            priority=priority,
            user_id=user_id or current_user.id
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Task submitted for hierarchical orchestration",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Task submission failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task submission failed: {e}"
        )


@router.get("/task/{task_id}/result")
async def get_task_result(
    task_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get result for a completed orchestration task"""
    try:
        result = await hierarchical_manager.get_task_result(task_id)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task result not found"
            )
        
        return {
            "success": True,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get task result", task_id=task_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task result: {e}"
        )


# ============================================================================
# ORCHESTRATOR STATUS AND MONITORING
# ============================================================================

@router.get("/status")
async def get_orchestrator_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get comprehensive status of all orchestrators"""
    try:
        status = await hierarchical_manager.get_orchestrator_status()
        
        return {
            "success": True,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get orchestrator status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get orchestrator status: {e}"
        )


@router.get("/optimization-report")
async def get_optimization_report(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get performance optimization report"""
    try:
        report = await hierarchical_manager.optimize_orchestrator_performance()
        
        return {
            "success": True,
            "report": report,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to generate optimization report", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate optimization report: {e}"
        )


@router.post("/emergency-failover/{failed_orchestrator}")
async def trigger_emergency_failover(
    failed_orchestrator: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Trigger emergency failover for a failed orchestrator"""
    try:
        failover_plan = await hierarchical_manager.emergency_failover(failed_orchestrator)
        
        return {
            "success": True,
            "failover_plan": failover_plan,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Emergency failover failed", 
                    failed_orchestrator=failed_orchestrator, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Emergency failover failed: {e}"
        )


# ============================================================================
# TASK DECOMPOSITION ENDPOINTS
# ============================================================================

@router.post("/decompose-task")
async def decompose_complex_task(
    requirement: str,
    context: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Decompose complex requirements into manageable tasks"""
    try:
        # Create a task for decomposition
        task = OrchestrationTask(
            task_type="task_decomposition",
            complexity=TaskComplexity.COMPLEX,
            requirements={"requirement": requirement, "context": context or {}},
            priority=7,
            user_id=current_user.id
        )
        
        # Use the hierarchical manager to route this task
        result = await hierarchical_manager.route_task(task)
        
        return {
            "success": True,
            "decomposition_result": result.result_data if result.success else None,
            "error": result.error_message if not result.success else None,
            "orchestrator_used": result.orchestrator_used,
            "strategy_used": result.strategy_used.value,
            "confidence_score": result.confidence_score,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Task decomposition failed", requirement=requirement, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task decomposition failed: {e}"
        )


# ============================================================================
# ORCHESTRATION STRATEGIES
# ============================================================================

@router.get("/strategies")
async def get_orchestration_strategies(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get available orchestration strategies"""
    try:
        strategies = {
            "single_orchestrator": {
                "description": "Use one orchestrator for simple tasks",
                "best_for": ["simple", "moderate"],
                "execution_time": "fast",
                "reliability": "high"
            },
            "parallel_processing": {
                "description": "Multiple orchestrators work simultaneously",
                "best_for": ["moderate", "complex"],
                "execution_time": "medium",
                "reliability": "very_high"
            },
            "hierarchical_cascade": {
                "description": "Flow through hierarchy levels",
                "best_for": ["complex", "critical"],
                "execution_time": "medium",
                "reliability": "high"
            },
            "consensus_validation": {
                "description": "Multiple orchestrators validate results",
                "best_for": ["critical", "supreme"],
                "execution_time": "slow",
                "reliability": "maximum"
            },
            "adaptive_routing": {
                "description": "Dynamic routing based on load",
                "best_for": ["all"],
                "execution_time": "variable",
                "reliability": "optimized"
            }
        }
        
        return {
            "success": True,
            "strategies": strategies,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get orchestration strategies", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get orchestration strategies: {e}"
        )


@router.get("/orchestrator-levels")
async def get_orchestrator_levels(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get information about orchestrator hierarchy levels"""
    try:
        levels = {
            "strategic": {
                "orchestrator": "UnifiedMetaAIOrchestrator",
                "description": "Supreme governance and policy decisions",
                "capabilities": ["governance", "policy", "strategic_planning", "escalation"],
                "best_for": ["supreme", "critical"]
            },
            "tactical": {
                "orchestrator": "UnifiedAIComponentOrchestrator",
                "description": "Service coordination and workflow management",
                "capabilities": ["service_coordination", "workflow", "resource_allocation", "task_routing"],
                "best_for": ["complex", "moderate"]
            },
            "execution": {
                "orchestrator": "SwarmAIOrchestrator",
                "description": "Multi-agent consensus and execution",
                "capabilities": ["consensus", "parallel_processing", "collective_intelligence", "multi_agent"],
                "best_for": ["complex", "critical"]
            },
            "smarty": {
                "orchestrator": "SmartCodingAIOptimized",
                "description": "Smart Coding AI with photographic memory and code intelligence",
                "capabilities": ["code_completion", "code_generation", "codebase_memory", "pattern_recognition", "multi_language_support", "photographic_memory"],
                "best_for": ["code_completion", "code_generation", "code_analysis", "pattern_recognition", "cross_session_context"]
            },
            "quality": {
                "orchestrator": "AIOrchestrationLayer",
                "description": "Validation and compliance",
                "capabilities": ["validation", "compliance", "quality_assurance", "code_analysis"],
                "best_for": ["all"]
            },
            "operations": {
                "orchestrator": "AIComponentOrchestrator",
                "description": "Basic coordination and monitoring",
                "capabilities": ["basic_coordination", "monitoring", "lifecycle_management", "operations"],
                "best_for": ["simple", "moderate"]
            }
        }
        
        return {
            "success": True,
            "levels": levels,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get orchestrator levels", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get orchestrator levels: {e}"
        )


# ============================================================================
# SMARTY INTEGRATION ENDPOINTS
# ============================================================================

@router.post("/smarty/code-completion")
async def orchestrate_code_completion(
    code: str,
    language: str = "python",
    context: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Orchestrate code completion through Smarty"""
    try:
        task_id = await hierarchical_manager.submit_task(
            task_type="code_completion",
            requirements={
                "code": code,
                "language": language,
                "context": context or ""
            },
            complexity=TaskComplexity.SIMPLE,
            priority=7,
            user_id=current_user.id
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Code completion task submitted to Smarty",
            "smarty_features": ["photographic_memory", "cross_session_context", "pattern_recognition"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Code completion orchestration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code completion orchestration failed: {e}"
        )


@router.post("/smarty/code-generation")
async def orchestrate_code_generation(
    prompt: str,
    language: str = "python",
    context: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Orchestrate code generation through Smarty"""
    try:
        task_id = await hierarchical_manager.submit_task(
            task_type="code_generation",
            requirements={
                "prompt": prompt,
                "language": language,
                "context": context or {}
            },
            complexity=TaskComplexity.MODERATE,
            priority=8,
            user_id=current_user.id
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Code generation task submitted to Smarty",
            "smarty_features": ["photographic_memory", "multi_language_support", "context_awareness"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Code generation orchestration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code generation orchestration failed: {e}"
        )


@router.post("/smarty/codebase-analysis")
async def orchestrate_codebase_analysis(
    project_path: str = ".",
    analysis_depth: str = "comprehensive",
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Orchestrate codebase analysis through Smarty's photographic memory"""
    try:
        task_id = await hierarchical_manager.submit_task(
            task_type="codebase_memory",
            requirements={
                "project_path": project_path,
                "analysis_depth": analysis_depth
            },
            complexity=TaskComplexity.COMPLEX,
            priority=9,
            user_id=current_user.id
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Codebase analysis task submitted to Smarty",
            "smarty_features": ["photographic_memory", "file_structure_analysis", "pattern_recognition", "dependency_tracking"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Codebase analysis orchestration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Codebase analysis orchestration failed: {e}"
        )


@router.post("/smarty/pattern-recognition")
async def orchestrate_pattern_recognition(
    code: str,
    context: Optional[Dict[str, Any]] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Orchestrate pattern recognition through Smarty"""
    try:
        task_id = await hierarchical_manager.submit_task(
            task_type="pattern_recognition",
            requirements={
                "code": code,
                "context": context or {}
            },
            complexity=TaskComplexity.MODERATE,
            priority=6,
            user_id=current_user.id
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Pattern recognition task submitted to Smarty",
            "smarty_features": ["pattern_recognition", "photographic_memory", "cross_session_context"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Pattern recognition orchestration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Pattern recognition orchestration failed: {e}"
        )


@router.get("/smarty/session-context/{session_id}")
async def get_smarty_session_context(
    session_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get Smarty's cross-session context"""
    try:
        task_id = await hierarchical_manager.submit_task(
            task_type="cross_session_context",
            requirements={
                "session_id": session_id,
                "user_id": current_user.id
            },
            complexity=TaskComplexity.SIMPLE,
            priority=5,
            user_id=current_user.id
        )
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Session context retrieval task submitted to Smarty",
            "smarty_features": ["cross_session_context", "photographic_memory", "user_preferences"],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Session context orchestration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Session context orchestration failed: {e}"
        )


@router.get("/smarty/capabilities")
async def get_smarty_capabilities(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get Smarty's capabilities and features"""
    try:
        capabilities = {
            "core_features": [
                "In-line Code Completion",
                "Real-time Suggestions", 
                "Multi-language Support",
                "Context-aware Completions",
                "Intelligent Code Generation"
            ],
            "advanced_features": [
                "Photographic Memory",
                "Cross-session Context Persistence",
                "Pattern Recognition",
                "Dependency Tracking",
                "File Structure Analysis",
                "Coding Pattern Memory"
            ],
            "supported_languages": [
                "Python", "JavaScript", "TypeScript", "Java", "C#", "C++",
                "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin",
                "HTML", "CSS", "SQL", "YAML", "JSON", "Markdown"
            ],
            "integration_features": [
                "Auth & RBAC Integration",
                "OAuth Support (Google, GitHub)",
                "Cache/Queue/Telemetry",
                "State Management",
                "Session Management",
                "Memory Search"
            ],
            "orchestration_level": "SMARTY",
            "specialties": [
                "in_line_completions",
                "context_aware_suggestions", 
                "cross_session_memory",
                "intelligent_code_analysis",
                "real_time_validation"
            ]
        }
        
        return {
            "success": True,
            "capabilities": capabilities,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get Smarty capabilities", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get Smarty capabilities: {e}"
        )


# ============================================================================
# DEMONSTRATION ENDPOINTS
# ============================================================================

@router.post("/demonstrate-advantage")
async def demonstrate_redundancy_advantage(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Demonstrate how orchestrator redundancy becomes strategic advantage"""
    try:
        # Submit multiple tasks to demonstrate orchestration
        demo_tasks = [
            {
                "task_type": "simple_validation",
                "requirements": {"validation_type": "basic"},
                "complexity": TaskComplexity.SIMPLE,
                "priority": 5
            },
            {
                "task_type": "complex_analysis",
                "requirements": {"analysis_type": "comprehensive", "requires_consensus": True},
                "complexity": TaskComplexity.COMPLEX,
                "priority": 8
            },
            {
                "task_type": "strategic_decision",
                "requirements": {"decision_type": "governance"},
                "complexity": TaskComplexity.SUPREME,
                "priority": 10
            }
        ]
        
        submitted_tasks = []
        for task_config in demo_tasks:
            task_id = await hierarchical_manager.submit_task(
                task_type=task_config["task_type"],
                requirements=task_config["requirements"],
                complexity=task_config["complexity"],
                priority=task_config["priority"],
                user_id=current_user.id
            )
            submitted_tasks.append(task_id)
        
        # Get system status
        status = await hierarchical_manager.get_orchestrator_status()
        
        # Get optimization report
        optimization_report = await hierarchical_manager.optimize_orchestrator_performance()
        
        return {
            "success": True,
            "demonstration": {
                "message": "Hierarchical orchestration successfully converts redundancy into strategic advantage",
                "submitted_tasks": submitted_tasks,
                "system_status": status,
                "optimization_recommendations": len(optimization_report.get("recommendations", [])),
                "key_advantages": [
                    "Intelligent Task Routing - Tasks routed to appropriate orchestrator level",
                    "Load Balancing - System distributes load efficiently",
                    "Fault Tolerance - Backup orchestrators available for failover",
                    "Performance Optimization - System analyzes and improves itself",
                    "Strategic Coordination - Multiple orchestrators work together"
                ]
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Demonstration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Demonstration failed: {e}"
        )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check():
    """Health check for hierarchical orchestration system"""
    try:
        # Basic health check
        status = await hierarchical_manager.get_orchestrator_status()
        
        # Check if all orchestrators are operational
        all_healthy = True
        orchestrator_status = {}
        
        for name, metrics in status.get("orchestrators", {}).items():
            is_healthy = metrics.get("success_rate", 0) > 0.8 and metrics.get("current_load", 0) < 0.9
            orchestrator_status[name] = {
                "healthy": is_healthy,
                "success_rate": metrics.get("success_rate", 0),
                "current_load": metrics.get("current_load", 0)
            }
            if not is_healthy:
                all_healthy = False
        
        return {
            "healthy": all_healthy,
            "orchestrators": orchestrator_status,
            "active_tasks": status.get("hierarchical_manager", {}).get("active_tasks", 0),
            "completed_tasks": status.get("hierarchical_manager", {}).get("completed_tasks", 0),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return {
            "healthy": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

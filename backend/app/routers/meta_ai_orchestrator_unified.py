"""
Unified Meta AI Orchestrator - The Supreme God of Cognomega Platform
Combines all functionality from Basic, Optimized, and Enhanced versions
Includes: Core Orchestration, Performance Optimization, Escalation System, and Governance
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from app.services.meta_ai_orchestrator_unified import (
    UnifiedMetaAIOrchestrator, GovernanceLevel, ComponentStatus, EscalationLevel,
    OptimizationLevel, SuccessMetricType, ComponentHealthStatus, PermanentSolutionType
)
from app.models.meta_orchestrator_unified import (
    # Core Orchestration Models
    MetaOrchestrationRequest, MetaOrchestrationResponse, MetaOrchestrationResult,
    # Governance Models
    GovernanceRuleRequest, ComponentHealthResponse, PlatformStatusResponse,
    # Performance Optimization Models
    OptimizedSuccessMetricsResponse, PerformanceOptimizationResponse,
    PredictiveAnalyticsResponse, EnhancedSuccessMetricsResponse,
    # Escalation Models
    ComponentHealthRequest, EscalationResponse, PermanentSolutionResponse,
    PlatformHealthSummary, ComponentIssueResponse, EscalationActionResponse
)

logger = structlog.get_logger()
router = APIRouter()

# Initialize Unified Meta AI Orchestrator
unified_orchestrator = UnifiedMetaAIOrchestrator()


# ============================================================================
# CORE ORCHESTRATION ENDPOINTS (from Basic version)
# ============================================================================

@router.post("/orchestrate", response_model=MetaOrchestrationResponse)
async def start_meta_orchestration(
    request: MetaOrchestrationRequest,
    background_tasks: BackgroundTasks
):
    """Start comprehensive meta orchestration across all AI components"""
    try:
        result = await unified_orchestrator.start_meta_orchestration(request)
        background_tasks.add_task(unified_orchestrator.execute_orchestration_plan, result.orchestration_id)
        
        logger.info("Meta orchestration started", orchestration_id=result.orchestration_id)
        return result
        
    except Exception as e:
        logger.error("Failed to start meta orchestration", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start meta orchestration: {e}"
        )


@router.get("/coordinate/ai-orchestrator")
async def coordinate_ai_orchestrator():
    """Coordinate the main AI orchestrator"""
    try:
        result = await unified_orchestrator.coordinate_ai_orchestrator()
        return {
            "status": "coordinated",
            "ai_orchestrator_status": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to coordinate AI orchestrator", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to coordinate AI orchestrator: {e}"
        )


@router.get("/manage/ai-agents")
async def manage_ai_agents():
    """Manage all AI agents in the system"""
    try:
        result = await unified_orchestrator.manage_ai_agents()
        return {
            "status": "managed",
            "ai_agents_status": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to manage AI agents", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to manage AI agents: {e}"
        )


@router.get("/coordinate/ai-engines")
async def coordinate_ai_engines():
    """Coordinate all AI engines"""
    try:
        result = await unified_orchestrator.coordinate_ai_engines()
        return {
            "status": "coordinated",
            "ai_engines_status": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to coordinate AI engines", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to coordinate AI engines: {e}"
        )


@router.get("/oversee/ai-services")
async def oversee_ai_services():
    """Oversee all AI services"""
    try:
        result = await unified_orchestrator.oversee_ai_services()
        return {
            "status": "overseen",
            "ai_services_status": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to oversee AI services", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to oversee AI services: {e}"
        )


@router.get("/coordinate/smart-coding-ai")
async def coordinate_smart_coding_ai():
    """Coordinate Smart Coding AI system"""
    try:
        result = await unified_orchestrator.coordinate_smart_coding_ai()
        return {
            "status": "coordinated",
            "smart_coding_ai_status": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to coordinate Smart Coding AI", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to coordinate Smart Coding AI: {e}"
        )


@router.get("/orchestration/results")
async def get_orchestration_results():
    """Get all orchestration results"""
    try:
        results = await unified_orchestrator.get_orchestration_results()
        return {
            "results": results,
            "total_count": len(results),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get orchestration results", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get orchestration results: {e}"
        )


@router.get("/orchestration/results/latest")
async def get_latest_orchestration_results(
    limit: int = Query(default=10, ge=1, le=100)
):
    """Get latest orchestration results"""
    try:
        results = await unified_orchestrator.get_latest_orchestration_results(limit)
        return {
            "results": results,
            "count": len(results),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get latest orchestration results", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get latest orchestration results: {e}"
        )


# ============================================================================
# GOVERNANCE ENDPOINTS (from Basic version)
# ============================================================================

@router.get("/enforce/governance")
async def enforce_governance():
    """Enforce governance across the platform"""
    try:
        result = await unified_orchestrator.enforce_governance()
        return {
            "status": "enforced",
            "governance_status": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to enforce governance", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enforce governance: {e}"
        )


@router.get("/ensure/harmony")
async def ensure_harmony():
    """Ensure harmony across all components"""
    try:
        result = await unified_orchestrator.ensure_harmony()
        return {
            "status": "ensured",
            "harmony_status": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to ensure harmony", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ensure harmony: {e}"
        )


@router.get("/governance/rules")
async def get_governance_rules():
    """Get all governance rules"""
    try:
        rules = await unified_orchestrator.get_governance_rules()
        return {
            "rules": rules,
            "total_count": len(rules),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get governance rules", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get governance rules: {e}"
        )


@router.get("/governance/rules/active")
async def get_active_governance_rules():
    """Get active governance rules"""
    try:
        rules = await unified_orchestrator.get_active_governance_rules()
        return {
            "active_rules": rules,
            "count": len(rules),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get active governance rules", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active governance rules: {e}"
        )


@router.post("/governance/rules/{rule_id}/update")
async def update_governance_rule(
    rule_id: str,
    request: GovernanceRuleRequest
):
    """Update a governance rule"""
    try:
        result = await unified_orchestrator.update_governance_rule(rule_id, request)
        return {
            "status": "updated",
            "rule_id": rule_id,
            "result": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to update governance rule", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update governance rule: {e}"
        )


@router.get("/governance/compliance")
async def get_governance_compliance():
    """Get governance compliance status"""
    try:
        compliance = await unified_orchestrator.get_governance_compliance()
        return {
            "compliance": compliance,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get governance compliance", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get governance compliance: {e}"
        )


# ============================================================================
# PERFORMANCE OPTIMIZATION ENDPOINTS (from Optimized version)
# ============================================================================

@router.post("/optimize/success-metrics")
async def optimize_success_metrics():
    """Optimize success metrics across the platform"""
    try:
        result = await unified_orchestrator.optimize_success_metrics()
        return {
            "status": "optimized",
            "optimization_result": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to optimize success metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize success metrics: {e}"
        )


@router.get("/success-metrics/optimized")
async def get_optimized_success_metrics():
    """Get optimized success metrics"""
    try:
        metrics = await unified_orchestrator.get_optimized_success_metrics()
        return metrics
    except Exception as e:
        logger.error("Failed to get optimized success metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get optimized success metrics: {e}"
        )


@router.get("/success-metrics/enhanced")
async def get_enhanced_success_metrics():
    """Get enhanced success metrics"""
    try:
        metrics = await unified_orchestrator.get_enhanced_success_metrics()
        return metrics
    except Exception as e:
        logger.error("Failed to get enhanced success metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get enhanced success metrics: {e}"
        )


@router.post("/optimize/performance/{component_id}")
async def create_performance_optimization(
    component_id: str,
    request: PerformanceOptimizationResponse
):
    """Create performance optimization for a component"""
    try:
        result = await unified_orchestrator.create_performance_optimization(component_id, request)
        return {
            "status": "created",
            "component_id": component_id,
            "optimization_id": result.optimization_id,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to create performance optimization", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create performance optimization: {e}"
        )


@router.get("/optimizations/performance")
async def get_performance_optimizations():
    """Get all performance optimizations"""
    try:
        optimizations = await unified_orchestrator.get_performance_optimizations()
        return {
            "optimizations": optimizations,
            "total_count": len(optimizations),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get performance optimizations", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get performance optimizations: {e}"
        )


@router.post("/analytics/predictive/{component_id}")
async def create_predictive_analytics(component_id: str):
    """Create predictive analytics for a component"""
    try:
        result = await unified_orchestrator.create_predictive_analytics(component_id)
        return {
            "status": "created",
            "component_id": component_id,
            "analytics_id": result.analytics_id,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to create predictive analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create predictive analytics: {e}"
        )


@router.get("/analytics/predictive")
async def get_predictive_analytics():
    """Get all predictive analytics"""
    try:
        analytics = await unified_orchestrator.get_predictive_analytics()
        return {
            "analytics": analytics,
            "total_count": len(analytics),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get predictive analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get predictive analytics: {e}"
        )


@router.get("/optimization/history")
async def get_optimization_history():
    """Get optimization history"""
    try:
        history = await unified_orchestrator.get_optimization_history()
        return {
            "history": history,
            "total_count": len(history),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get optimization history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get optimization history: {e}"
        )


@router.get("/metrics/accuracy")
async def get_accuracy_metrics():
    """Get accuracy metrics"""
    try:
        metrics = await unified_orchestrator.get_accuracy_metrics()
        return metrics
    except Exception as e:
        logger.error("Failed to get accuracy metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get accuracy metrics: {e}"
        )


@router.get("/metrics/performance")
async def get_performance_metrics():
    """Get performance metrics"""
    try:
        metrics = await unified_orchestrator.get_performance_metrics()
        return metrics
    except Exception as e:
        logger.error("Failed to get performance metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get performance metrics: {e}"
        )


@router.get("/metrics/reliability")
async def get_reliability_metrics():
    """Get reliability metrics"""
    try:
        metrics = await unified_orchestrator.get_reliability_metrics()
        return metrics
    except Exception as e:
        logger.error("Failed to get reliability metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get reliability metrics: {e}"
        )


@router.get("/metrics/harmony")
async def get_harmony_metrics():
    """Get harmony metrics"""
    try:
        metrics = await unified_orchestrator.get_harmony_metrics()
        return metrics
    except Exception as e:
        logger.error("Failed to get harmony metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get harmony metrics: {e}"
        )


@router.get("/optimization/levels")
async def get_optimization_levels():
    """Get available optimization levels"""
    try:
        levels = await unified_orchestrator.get_optimization_levels()
        return {
            "levels": levels,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get optimization levels", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get optimization levels: {e}"
        )


@router.get("/success-metrics/summary")
async def get_success_metrics_summary():
    """Get success metrics summary"""
    try:
        summary = await unified_orchestrator.get_success_metrics_summary()
        return summary
    except Exception as e:
        logger.error("Failed to get success metrics summary", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get success metrics summary: {e}"
        )


# ============================================================================
# ESCALATION SYSTEM ENDPOINTS (from Enhanced version)
# ============================================================================

@router.post("/monitor/component-health")
async def monitor_component_health(
    request: ComponentHealthRequest
):
    """Monitor component health and detect issues"""
    try:
        result = await unified_orchestrator.monitor_component_health(request)
        return result
    except Exception as e:
        logger.error("Failed to monitor component health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to monitor component health: {e}"
        )


@router.post("/escalate/issue")
async def escalate_component_issue(
    request: ComponentIssueResponse
):
    """Escalate a component issue"""
    try:
        result = await unified_orchestrator.escalate_component_issue(request)
        return result
    except Exception as e:
        logger.error("Failed to escalate component issue", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to escalate component issue: {e}"
        )


@router.post("/execute/permanent-solution")
async def execute_permanent_solution(
    request: PermanentSolutionResponse
):
    """Execute a permanent solution"""
    try:
        result = await unified_orchestrator.execute_permanent_solution(request)
        return result
    except Exception as e:
        logger.error("Failed to execute permanent solution", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute permanent solution: {e}"
        )


@router.get("/issues/active")
async def get_active_issues():
    """Get all active issues"""
    try:
        issues = await unified_orchestrator.get_active_issues()
        return {
            "issues": issues,
            "count": len(issues),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get active issues", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get active issues: {e}"
        )


@router.get("/issues/all")
async def get_all_issues():
    """Get all issues (active and resolved)"""
    try:
        issues = await unified_orchestrator.get_all_issues()
        return {
            "issues": issues,
            "total_count": len(issues),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get all issues", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get all issues: {e}"
        )


@router.get("/escalations/actions")
async def get_escalation_actions():
    """Get escalation actions"""
    try:
        actions = await unified_orchestrator.get_escalation_actions()
        return {
            "actions": actions,
            "count": len(actions),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get escalation actions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get escalation actions: {e}"
        )


@router.get("/escalations/history")
async def get_escalation_history():
    """Get escalation history"""
    try:
        history = await unified_orchestrator.get_escalation_history()
        return {
            "history": history,
            "total_count": len(history),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get escalation history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get escalation history: {e}"
        )


@router.get("/solutions/permanent")
async def get_permanent_solutions():
    """Get permanent solutions"""
    try:
        solutions = await unified_orchestrator.get_permanent_solutions()
        return {
            "solutions": solutions,
            "count": len(solutions),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get permanent solutions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get permanent solutions: {e}"
        )


@router.get("/health/history/{component_id}")
async def get_component_health_history(component_id: str):
    """Get component health history"""
    try:
        history = await unified_orchestrator.get_component_health_history(component_id)
        return {
            "component_id": component_id,
            "history": history,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get component health history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get component health history: {e}"
        )


@router.get("/platform/health-summary")
async def get_platform_health_summary():
    """Get platform health summary"""
    try:
        summary = await unified_orchestrator.get_platform_health_summary()
        return summary
    except Exception as e:
        logger.error("Failed to get platform health summary", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get platform health summary: {e}"
        )


@router.post("/monitoring/start")
async def start_continuous_monitoring(background_tasks: BackgroundTasks):
    """Start continuous monitoring"""
    try:
        result = await unified_orchestrator.start_continuous_monitoring()
        background_tasks.add_task(unified_orchestrator.run_continuous_monitoring)
        return {
            "status": "started",
            "monitoring_id": result.monitoring_id,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to start continuous monitoring", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start continuous monitoring: {e}"
        )


@router.get("/ai-orchestrator/health")
async def check_ai_orchestrator_health():
    """Check AI orchestrator health"""
    try:
        health = await unified_orchestrator.check_ai_orchestrator_health()
        return {
            "health": health,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to check AI orchestrator health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check AI orchestrator health: {e}"
        )


@router.get("/escalation/levels")
async def get_escalation_levels():
    """Get escalation levels"""
    try:
        levels = await unified_orchestrator.get_escalation_levels()
        return {
            "levels": levels,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get escalation levels", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get escalation levels: {e}"
        )


@router.get("/solutions/types")
async def get_permanent_solution_types():
    """Get permanent solution types"""
    try:
        types = await unified_orchestrator.get_permanent_solution_types()
        return {
            "types": types,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get permanent solution types", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get permanent solution types: {e}"
        )


@router.get("/god-mode/status")
async def get_god_mode_status():
    """Get god mode status - Supreme control over the platform"""
    try:
        status = await unified_orchestrator.get_god_mode_status()
        return {
            "god_mode": status,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get god mode status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get god mode status: {e}"
        )


# ============================================================================
# PLATFORM STATUS ENDPOINTS (Combined from all versions)
# ============================================================================

@router.get("/components/health")
async def get_all_component_health():
    """Get health status of all components"""
    try:
        health = await unified_orchestrator.get_all_component_health()
        return {
            "components": health,
            "total_count": len(health),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get component health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get component health: {e}"
        )


@router.get("/components/health/{component_id}")
async def get_component_health(component_id: str):
    """Get health status of a specific component"""
    try:
        health = await unified_orchestrator.get_component_health(component_id)
        return {
            "component_id": component_id,
            "health": health,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get component health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get component health: {e}"
        )


@router.get("/platform/status")
async def get_platform_status():
    """Get overall platform status"""
    try:
        status = await unified_orchestrator.get_platform_status()
        return status
    except Exception as e:
        logger.error("Failed to get platform status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get platform status: {e}"
        )


@router.get("/smart-coding/accuracy")
async def get_smart_coding_accuracy():
    """Get Smart Coding AI accuracy metrics"""
    try:
        accuracy = await unified_orchestrator.get_smart_coding_accuracy()
        return {
            "accuracy": accuracy,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get Smart Coding accuracy", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get Smart Coding accuracy: {e}"
        )


@router.get("/harmony/score")
async def get_harmony_score():
    """Get harmony score across the platform"""
    try:
        score = await unified_orchestrator.get_harmony_score()
        return {
            "harmony_score": score,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get harmony score", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get harmony score: {e}"
        )

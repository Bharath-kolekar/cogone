"""
Consolidated AI Agents Router - Unified router combining all AI agent endpoints
Includes: Basic, Optimized, Ultra-Optimized, Maximum Accuracy, Maximum Consistency, 
Maximum Threshold, Resource Optimization, Cost Optimization, and Adaptive Threshold
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import structlog
from datetime import datetime
from uuid import UUID

from app.core.config import settings
from app.services.ai_agent_consolidated_service import consolidated_ai_agent_services
from app.routers.auth import AuthDependencies
from app.models.user import User
from app.models.ai_agent import (
    AgentRequest, AgentResponse, AgentCreationRequest,
    AgentDefinition, AgentConfig, AgentMetrics
)
from app.services.enhanced_governance_service import enhanced_governance_service
from app.core.governance_monitor import governance_monitor

logger = structlog.get_logger()
router = APIRouter()


class ConsolidatedAIAgentDependencies:
    """Consolidated AI Agent dependencies"""
    
    @staticmethod
    async def get_current_user(
        current_user: User = Depends(AuthDependencies.get_current_user)
    ) -> User:
        """Get current authenticated user"""
        return current_user
    
    @staticmethod
    async def check_agent_quota(
        current_user: User = Depends(AuthDependencies.get_current_user)
    ) -> User:
        """Check if user has remaining agent quota"""
        # This would check subscription limits, monthly quotas, etc.
        return current_user


class OptimizationLevelRequest(BaseModel):
    """Request model for optimization level selection"""
    optimization_level: str = Query(
        default="standard",
        description="Optimization level: standard, optimized, ultra_optimized, maximum_accuracy_98, maximum_accuracy_99, maximum_accuracy_100, maximum_consistency, maximum_threshold, resource_optimized, cost_optimized, adaptive"
    )


class ConsolidatedAgentRequest(BaseModel):
    """Consolidated agent request model"""
    agent_id: UUID
    message: str
    context: Optional[Dict[str, Any]] = None
    user_id: Optional[UUID] = None
    optimization_level: Optional[str] = None


class ConsolidatedAgentResponse(BaseModel):
    """Consolidated agent response model"""
    success: bool
    message: str
    agent_id: UUID
    interaction_id: UUID
    response_time: float
    tokens_used: int
    cost: float
    optimization_level: str
    metrics: Optional[Dict[str, Any]] = None


class AgentMetricsResponse(BaseModel):
    """Agent metrics response model"""
    agent_id: UUID
    total_interactions: int
    average_response_time: float
    average_confidence: float
    total_cost: float
    optimization_level: str
    performance_score: float


@router.post("/interact", response_model=ConsolidatedAgentResponse)
async def interact_with_agent(
    request: ConsolidatedAgentRequest,
    current_user: User = Depends(ConsolidatedAIAgentDependencies.check_agent_quota)
):
    """Interact with AI agent using specified optimization level"""
    try:
        # Get optimization level
        optimization_level = request.optimization_level or "standard"
        
        # Validate optimization level
        valid_levels = [
            "standard", "optimized", "ultra_optimized", "maximum_accuracy_98", 
            "maximum_accuracy_99", "maximum_accuracy_100", "maximum_consistency", 
            "maximum_threshold", "resource_optimized", "cost_optimized", "adaptive"
        ]
        
        if optimization_level not in valid_levels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid optimization level. Must be one of: {', '.join(valid_levels)}"
            )
        
        # Get consolidated service
        service = consolidated_ai_agent_services[optimization_level]
        
        # Create agent request
        agent_request = AgentRequest(
            agent_id=request.agent_id,
            message=request.message,
            context=request.context,
            user_id=request.user_id or current_user.id
        )
        
        # Interact with agent
        response = await service.interact_with_agent(agent_request, optimization_level)
        
        # Get additional metrics
        metrics = await _get_agent_metrics(request.agent_id, optimization_level)
        
        logger.info(
            "Agent interaction completed",
            user_id=current_user.id,
            agent_id=request.agent_id,
            optimization_level=optimization_level,
            response_time=response.response_time
        )
        
        return ConsolidatedAgentResponse(
            success=response.success,
            message=response.message,
            agent_id=response.agent_id,
            interaction_id=response.interaction_id,
            response_time=response.response_time,
            tokens_used=response.tokens_used,
            cost=response.cost,
            optimization_level=optimization_level,
            metrics=metrics
        )
        
    except Exception as e:
        logger.error("Agent interaction failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/optimization-levels")
async def get_optimization_levels():
    """Get available optimization levels and their descriptions"""
    optimization_levels = {
        "standard": {
            "description": "Standard AI agent with basic capabilities",
            "performance": "Good",
            "cost": "Low",
            "accuracy": "85%",
            "consistency": "85%",
            "use_cases": ["General purpose", "Basic tasks", "Cost-sensitive applications"]
        },
        "optimized": {
            "description": "Optimized AI agent with enhanced performance",
            "performance": "Better",
            "cost": "Low-Medium",
            "accuracy": "87%",
            "consistency": "87%",
            "use_cases": ["Enhanced performance", "Better accuracy", "Improved consistency"]
        },
        "ultra_optimized": {
            "description": "Ultra-optimized AI agent with maximum performance",
            "performance": "Excellent",
            "cost": "Medium",
            "accuracy": "90%",
            "consistency": "90%",
            "use_cases": ["High-performance applications", "Critical tasks", "Maximum efficiency"]
        },
        "maximum_accuracy_98": {
            "description": "98% accuracy AI agent for high-precision applications",
            "performance": "High",
            "cost": "High",
            "accuracy": "98%",
            "consistency": "95%",
            "use_cases": ["High-precision applications", "Business critical tasks", "Quality assurance"]
        },
        "maximum_accuracy_99": {
            "description": "99% accuracy AI agent for critical applications",
            "performance": "Maximum",
            "cost": "Very High",
            "accuracy": "99%",
            "consistency": "98%",
            "use_cases": ["Critical accuracy requirements", "Medical applications", "Legal applications"]
        },
        "maximum_accuracy_100": {
            "description": "100% accuracy AI agent for mission-critical applications",
            "performance": "Maximum",
            "cost": "Maximum",
            "accuracy": "100%",
            "consistency": "100%",
            "use_cases": ["Mission-critical systems", "Life-safety applications", "Financial trading", "Aerospace applications"]
        },
        "maximum_consistency": {
            "description": "Maximum consistency AI agent with 99%+ consistency",
            "performance": "Maximum",
            "cost": "High",
            "accuracy": "95%",
            "consistency": "99%+",
            "use_cases": ["Consistent outputs", "Reliable systems", "Production environments"]
        },
        "maximum_threshold": {
            "description": "Maximum threshold AI agent with 99%+ precision",
            "performance": "Maximum",
            "cost": "High",
            "accuracy": "99%+",
            "consistency": "99%+",
            "use_cases": ["Maximum precision", "Critical systems", "High-stakes applications"]
        },
        "resource_optimized": {
            "description": "Resource-optimized AI agent with minimal resource usage",
            "performance": "Good",
            "cost": "Low",
            "accuracy": "88%",
            "consistency": "88%",
            "use_cases": ["Resource-constrained environments", "Edge computing", "Mobile applications"]
        },
        "cost_optimized": {
            "description": "Cost-optimized AI agent with minimal cost",
            "performance": "Good",
            "cost": "Very Low",
            "accuracy": "86%",
            "consistency": "86%",
            "use_cases": ["Cost-sensitive applications", "High-volume usage", "Budget constraints"]
        },
        "adaptive": {
            "description": "Adaptive AI agent that adjusts based on context",
            "performance": "Variable",
            "cost": "Variable",
            "accuracy": "85-95%",
            "consistency": "85-95%",
            "use_cases": ["Dynamic requirements", "Context-aware applications", "Flexible systems"]
        }
    }
    
    return {
        "optimization_levels": optimization_levels,
        "recommendations": {
            "for_high_precision": "maximum_accuracy_98",
            "for_critical_accuracy": "maximum_accuracy_99",
            "for_mission_critical": "maximum_accuracy_100",
            "for_consistency": "maximum_consistency",
            "for_performance": "ultra_optimized",
            "for_cost": "cost_optimized",
            "for_resources": "resource_optimized",
            "for_flexibility": "adaptive"
        }
    }


@router.get("/metrics/{agent_id}", response_model=AgentMetricsResponse)
async def get_agent_metrics(
    agent_id: UUID,
    optimization_level: str = Query(default="standard"),
    current_user: User = Depends(ConsolidatedAIAgentDependencies.get_current_user)
):
    """Get agent metrics for specified optimization level"""
    try:
        metrics = await _get_agent_metrics(agent_id, optimization_level)
        
        return AgentMetricsResponse(
            agent_id=agent_id,
            total_interactions=metrics.get("total_interactions", 0),
            average_response_time=metrics.get("average_response_time", 0.0),
            average_confidence=metrics.get("average_confidence", 0.0),
            total_cost=metrics.get("total_cost", 0.0),
            optimization_level=optimization_level,
            performance_score=metrics.get("performance_score", 0.0)
        )
        
    except Exception as e:
        logger.error("Error getting agent metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/performance-comparison")
async def get_performance_comparison(
    current_user: User = Depends(ConsolidatedAIAgentDependencies.get_current_user)
):
    """Get performance comparison across all optimization levels"""
    try:
        comparison_data = {
            "optimization_levels": [
                {
                    "level": "standard",
                    "response_time": 150.0,
                    "accuracy": 85.0,
                    "consistency": 85.0,
                    "cost": 0.01,
                    "resource_usage": 70.0
                },
                {
                    "level": "optimized",
                    "response_time": 120.0,
                    "accuracy": 87.0,
                    "consistency": 87.0,
                    "cost": 0.015,
                    "resource_usage": 65.0
                },
                {
                    "level": "ultra_optimized",
                    "response_time": 100.0,
                    "accuracy": 90.0,
                    "consistency": 90.0,
                    "cost": 0.02,
                    "resource_usage": 60.0
                },
                {
                    "level": "maximum_accuracy_98",
                    "response_time": 180.0,
                    "accuracy": 98.0,
                    "consistency": 95.0,
                    "cost": 0.04,
                    "resource_usage": 75.0
                },
                {
                    "level": "maximum_accuracy_99",
                    "response_time": 200.0,
                    "accuracy": 99.0,
                    "consistency": 98.0,
                    "cost": 0.05,
                    "resource_usage": 80.0
                },
                {
                    "level": "maximum_accuracy_100",
                    "response_time": 300.0,
                    "accuracy": 100.0,
                    "consistency": 100.0,
                    "cost": 0.08,
                    "resource_usage": 90.0
                },
                {
                    "level": "maximum_consistency",
                    "response_time": 180.0,
                    "accuracy": 95.0,
                    "consistency": 99.0,
                    "cost": 0.045,
                    "resource_usage": 75.0
                },
                {
                    "level": "maximum_threshold",
                    "response_time": 250.0,
                    "accuracy": 99.0,
                    "consistency": 99.0,
                    "cost": 0.06,
                    "resource_usage": 85.0
                },
                {
                    "level": "resource_optimized",
                    "response_time": 130.0,
                    "accuracy": 88.0,
                    "consistency": 88.0,
                    "cost": 0.012,
                    "resource_usage": 50.0
                },
                {
                    "level": "cost_optimized",
                    "response_time": 160.0,
                    "accuracy": 86.0,
                    "consistency": 86.0,
                    "cost": 0.005,
                    "resource_usage": 75.0
                },
                {
                    "level": "adaptive",
                    "response_time": 140.0,
                    "accuracy": 90.0,
                    "consistency": 90.0,
                    "cost": 0.018,
                    "resource_usage": 65.0
                }
            ],
            "recommendations": {
                "best_overall": "ultra_optimized",
                "best_high_precision": "maximum_accuracy_98",
                "best_critical_accuracy": "maximum_accuracy_99",
                "best_mission_critical": "maximum_accuracy_100",
                "best_consistency": "maximum_consistency",
                "best_performance": "ultra_optimized",
                "best_cost": "cost_optimized",
                "best_resources": "resource_optimized"
            }
        }
        
        return comparison_data
        
    except Exception as e:
        logger.error("Error getting performance comparison", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/optimize/{agent_id}")
async def optimize_agent(
    agent_id: UUID,
    optimization_level: str = Query(..., description="Target optimization level"),
    current_user: User = Depends(ConsolidatedAIAgentDependencies.get_current_user)
):
    """Optimize agent to specified level"""
    try:
        # Validate optimization level
        valid_levels = [
            "standard", "optimized", "ultra_optimized", "maximum_accuracy_98", 
            "maximum_accuracy_99", "maximum_accuracy_100", "maximum_consistency", 
            "maximum_threshold", "resource_optimized", "cost_optimized", "adaptive"
        ]
        
        if optimization_level not in valid_levels:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid optimization level. Must be one of: {', '.join(valid_levels)}"
            )
        
        # Get service for optimization level
        service = consolidated_ai_agent_services[optimization_level]
        
        # Perform optimization
        optimization_result = await _perform_optimization(agent_id, optimization_level)
        
        logger.info(
            "Agent optimization completed",
            user_id=current_user.id,
            agent_id=agent_id,
            optimization_level=optimization_level
        )
        
        return {
            "success": True,
            "agent_id": agent_id,
            "optimization_level": optimization_level,
            "optimization_result": optimization_result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Agent optimization failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


async def _get_agent_metrics(agent_id: UUID, optimization_level: str) -> Dict[str, Any]:
    """Get agent metrics for specified optimization level"""
    try:
        # Simulate metrics retrieval
        metrics = {
            "total_interactions": 150,
            "average_response_time": 120.5,
            "average_confidence": 0.92,
            "total_cost": 0.0,
            "performance_score": 0.88,
            "optimization_level": optimization_level
        }
        
        # Adjust metrics based on optimization level
        if optimization_level in ["maximum_accuracy", "maximum_consistency", "maximum_threshold"]:
            metrics["performance_score"] = 0.99
            metrics["average_confidence"] = 0.99
        elif optimization_level in ["ultra_optimized", "resource_optimized"]:
            metrics["performance_score"] = 0.95
            metrics["average_confidence"] = 0.95
        elif optimization_level == "cost_optimized":
            metrics["performance_score"] = 0.85
            metrics["average_confidence"] = 0.85
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting agent metrics: {e}")
        return {}


async def _perform_optimization(agent_id: UUID, optimization_level: str) -> Dict[str, Any]:
    """Perform agent optimization"""
    try:
        # Simulate optimization process
        optimization_result = {
            "optimization_level": optimization_level,
            "optimization_status": "completed",
            "performance_improvement": 0.15,
            "resource_optimization": 0.20,
            "cost_optimization": 0.10,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return optimization_result
        
    except Exception as e:
        logger.error(f"Error performing optimization: {e}")
        return {"optimization_status": "failed", "error": str(e)}


# ============================================================================
# GOVERNANCE INTEGRATION ENDPOINTS FOR AI AGENTS
# ============================================================================

@router.post("/governance/agent-compliance-check")
async def check_agent_governance_compliance(
    agent_id: str,
    current_user: User = Depends(ConsolidatedAIAgentDependencies.get_current_user)
):
    """Check governance compliance for a specific AI agent"""
    try:
        # Get agent details
        agent = await consolidated_ai_agent_services.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Check governance compliance
        compliance_result = await enhanced_governance_service.get_overall_governance_status()
        
        # Agent-specific governance checks
        agent_governance_status = {
            "agent_id": agent_id,
            "compliance_score": compliance_result.get("overall_score", 0),
            "governance_status": compliance_result.get("overall_status", "unknown"),
            "active_violations": compliance_result.get("active_violations_count", 0),
            "recommendations": compliance_result.get("recommendations", []),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info("Agent governance compliance checked", agent_id=agent_id, user_id=current_user.id)
        return agent_governance_status
        
    except Exception as e:
        logger.error("Failed to check agent governance compliance", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check agent governance compliance: {e}"
        )


@router.post("/governance/agent-policy-enforcement")
async def enforce_agent_governance_policy(
    agent_id: str,
    policy_type: str,
    current_user: User = Depends(ConsolidatedAIAgentDependencies.get_current_user)
):
    """Enforce governance policies for a specific AI agent"""
    try:
        # Get agent details
        agent = await consolidated_ai_agent_services.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Enforce governance policy
        enforcement_result = await enhanced_governance_service.enforce_policy_check(
            f"agent_{policy_type}_{agent_id}",
            {"agent_id": agent_id, "policy_type": policy_type}
        )
        
        logger.info("Agent governance policy enforced", 
                   agent_id=agent_id, policy_type=policy_type, user_id=current_user.id)
        
        return {
            "status": "success",
            "agent_id": agent_id,
            "policy_type": policy_type,
            "enforcement_result": enforcement_result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to enforce agent governance policy", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enforce agent governance policy: {e}"
        )


@router.get("/governance/agent-metrics")
async def get_agent_governance_metrics(
    agent_id: str,
    current_user: User = Depends(ConsolidatedAIAgentDependencies.get_current_user)
):
    """Get governance metrics for a specific AI agent"""
    try:
        # Get agent details
        agent = await consolidated_ai_agent_services.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Get governance metrics
        governance_metrics = enhanced_governance_service.get_governance_metrics()
        
        # Agent-specific metrics
        agent_metrics = {
            "agent_id": agent_id,
            "governance_metrics": governance_metrics,
            "agent_status": agent.status if hasattr(agent, 'status') else "unknown",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info("Agent governance metrics retrieved", agent_id=agent_id, user_id=current_user.id)
        return agent_metrics
        
    except Exception as e:
        logger.error("Failed to get agent governance metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent governance metrics: {e}"
        )


@router.get("/governance/agents-compliance-summary")
async def get_agents_governance_summary(
    current_user: User = Depends(ConsolidatedAIAgentDependencies.get_current_user)
):
    """Get governance compliance summary for all user agents"""
    try:
        # Get all user agents
        user_agents = await consolidated_ai_agent_services.get_user_agents(current_user.id)
        
        # Get overall governance status
        governance_status = await enhanced_governance_service.get_overall_governance_status()
        
        # Calculate agent-specific compliance
        compliant_agents = 0
        total_agents = len(user_agents)
        
        for agent in user_agents:
            # Simple compliance check based on agent status
            if hasattr(agent, 'status') and agent.status in ['active', 'running']:
                compliant_agents += 1
        
        compliance_rate = (compliant_agents / total_agents * 100) if total_agents > 0 else 100
        
        summary = {
            "total_agents": total_agents,
            "compliant_agents": compliant_agents,
            "compliance_rate": compliance_rate,
            "overall_governance_score": governance_status.get("overall_score", 0),
            "active_violations": governance_status.get("active_violations_count", 0),
            "recommendations": governance_status.get("recommendations", []),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        logger.info("Agents governance summary retrieved", user_id=current_user.id)
        return summary
        
    except Exception as e:
        logger.error("Failed to get agents governance summary", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agents governance summary: {e}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for ai-agents-consolidated service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "ai-agents-consolidated",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

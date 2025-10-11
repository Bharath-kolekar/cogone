"""
Smarty AI Orchestrator Router

API endpoints for the Smarty AI Orchestrator integration service.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum
import structlog
from datetime import datetime

from app.services.smarty_ai_orchestrator import (
    smarty_ai_orchestrator,
    OrchestrationMode,
    CodeGenerationStrategy
)

logger = structlog.get_logger(__name__)

router = APIRouter()

class OrchestrationRequest(BaseModel):
    """Request model for orchestration"""
    transcript: str = Field(..., description="Voice transcript or requirements text")
    user_id: str = Field(..., description="User identifier")
    orchestration_mode: OrchestrationMode = Field(
        default=OrchestrationMode.VOICE_TO_APP,
        description="Orchestration mode"
    )
    code_generation_strategy: CodeGenerationStrategy = Field(
        default=CodeGenerationStrategy.ADAPTIVE,
        description="Code generation strategy"
    )
    ethical_validation_level: str = Field(
        default="standard",
        description="Level of ethical validation"
    )

class OrchestrationResponse(BaseModel):
    """Response model for orchestration"""
    plan_id: str
    user_id: str
    status: str
    confidence: float
    estimated_timeline: Dict[str, Any]
    smarty_integration: Dict[str, Any]
    ethical_validation: Dict[str, Any]
    created_at: str

class OrchestrationStatusResponse(BaseModel):
    """Response model for orchestration status"""
    plan_id: str
    status: str
    confidence: float
    created_at: str
    smarty_integration: Dict[str, Any]
    ethical_validation: Dict[str, Any]
    code_generation_strategy: str
    orchestration_mode: str

class OrchestrationMetricsResponse(BaseModel):
    """Response model for orchestration metrics"""
    orchestration_metrics: Dict[str, Any]
    active_plans_count: int
    total_plans_history: int
    code_generation_tasks_count: int

@router.post("/orchestrate", response_model=OrchestrationResponse)
async def orchestrate_with_smarty(request: OrchestrationRequest):
    """Orchestrate a complete plan with Smarty integration"""
    try:
        logger.info(f"Starting orchestration request", 
                   user_id=request.user_id,
                   mode=request.orchestration_mode.value)
        
        orchestration_plan = await smarty_ai_orchestrator.orchestrate_with_smarty(
            transcript=request.transcript,
            user_id=request.user_id,
            orchestration_mode=request.orchestration_mode,
            code_generation_strategy=request.code_generation_strategy,
            ethical_validation_level=request.ethical_validation_level
        )
        
        return OrchestrationResponse(
            plan_id=orchestration_plan.plan_id,
            user_id=orchestration_plan.user_id,
            status=orchestration_plan.status,
            confidence=orchestration_plan.confidence,
            estimated_timeline=orchestration_plan.estimated_timeline,
            smarty_integration=orchestration_plan.smarty_integration,
            ethical_validation=orchestration_plan.ethical_validation,
            created_at=orchestration_plan.created_at
        )
        
    except Exception as e:
        logger.error(f"Orchestration request failed", error=str(e), user_id=request.user_id)
        raise HTTPException(status_code=500, detail=f"Orchestration failed: {str(e)}")

@router.get("/status/{plan_id}", response_model=OrchestrationStatusResponse)
async def get_orchestration_status(plan_id: str):
    """Get status of an orchestration plan"""
    try:
        status = await smarty_ai_orchestrator.get_orchestration_status(plan_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Orchestration plan not found")
        
        return OrchestrationStatusResponse(
            plan_id=status['plan_id'],
            status=status['status'],
            confidence=status['confidence'],
            created_at=status['created_at'],
            smarty_integration=status['smarty_integration'],
            ethical_validation=status['ethical_validation'],
            code_generation_strategy=status['code_generation_strategy'],
            orchestration_mode=status['orchestration_mode']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status retrieval failed", error=str(e), plan_id=plan_id)
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.get("/metrics", response_model=OrchestrationMetricsResponse)
async def get_orchestration_metrics():
    """Get orchestration performance metrics"""
    try:
        metrics = await smarty_ai_orchestrator.get_orchestration_metrics()
        
        return OrchestrationMetricsResponse(
            orchestration_metrics=metrics.get('orchestration_metrics', {}),
            active_plans_count=metrics.get('active_plans_count', 0),
            total_plans_history=metrics.get('total_plans_history', 0),
            code_generation_tasks_count=metrics.get('code_generation_tasks_count', 0)
        )
        
    except Exception as e:
        logger.error(f"Metrics retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@router.delete("/cancel/{plan_id}")
async def cancel_orchestration(plan_id: str):
    """Cancel an ongoing orchestration"""
    try:
        success = await smarty_ai_orchestrator.cancel_orchestration(plan_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Orchestration plan not found")
        
        return {"message": "Orchestration cancelled successfully", "plan_id": plan_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Orchestration cancellation failed", error=str(e), plan_id=plan_id)
        raise HTTPException(status_code=500, detail=f"Cancellation failed: {str(e)}")

@router.get("/modes")
async def get_orchestration_modes():
    """Get available orchestration modes"""
    return {
        "modes": [
            {
                "name": mode.value,
                "description": _get_mode_description(mode)
            }
            for mode in OrchestrationMode
        ]
    }

@router.get("/strategies")
async def get_code_generation_strategies():
    """Get available code generation strategies"""
    return {
        "strategies": [
            {
                "name": strategy.value,
                "description": _get_strategy_description(strategy)
            }
            for strategy in CodeGenerationStrategy
        ]
    }

@router.post("/batch-orchestrate")
async def batch_orchestrate(requests: List[OrchestrationRequest], background_tasks: BackgroundTasks):
    """Execute multiple orchestration requests in batch"""
    try:
        if len(requests) > 10:
            raise HTTPException(status_code=400, detail="Maximum 10 batch requests allowed")
        
        logger.info(f"Starting batch orchestration", count=len(requests))
        
        # Execute orchestration requests
        results = []
        for request in requests:
            try:
                orchestration_plan = await smarty_ai_orchestrator.orchestrate_with_smarty(
                    transcript=request.transcript,
                    user_id=request.user_id,
                    orchestration_mode=request.orchestration_mode,
                    code_generation_strategy=request.code_generation_strategy,
                    ethical_validation_level=request.ethical_validation_level
                )
                
                results.append({
                    "plan_id": orchestration_plan.plan_id,
                    "user_id": orchestration_plan.user_id,
                    "status": orchestration_plan.status,
                    "confidence": orchestration_plan.confidence,
                    "success": True
                })
                
            except Exception as e:
                logger.error(f"Batch orchestration item failed", error=str(e), user_id=request.user_id)
                results.append({
                    "user_id": request.user_id,
                    "status": "failed",
                    "error": str(e),
                    "success": False
                })
        
        successful_count = sum(1 for result in results if result.get('success', False))
        
        return {
            "batch_results": results,
            "successful_count": successful_count,
            "failed_count": len(results) - successful_count,
            "total_count": len(results)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch orchestration failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Batch orchestration failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check if orchestrator is responsive
        metrics = await smarty_ai_orchestrator.get_orchestration_metrics()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "orchestrator_status": "operational",
            "active_plans": metrics.get('active_plans_count', 0),
            "total_plans": metrics.get('total_plans_history', 0)
        }
        
    except Exception as e:
        logger.error(f"Health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

def _get_mode_description(mode: OrchestrationMode) -> str:
    """Get description for orchestration mode"""
    descriptions = {
        OrchestrationMode.VOICE_TO_APP: "Convert voice transcript to complete application",
        OrchestrationMode.REQUIREMENTS_TO_CODE: "Transform requirements into code implementation",
        OrchestrationMode.ARCHITECTURE_TO_IMPLEMENTATION: "Generate implementation from architecture",
        OrchestrationMode.TESTING_TO_DEPLOYMENT: "Handle testing and deployment processes",
        OrchestrationMode.DEBUGGING_TO_OPTIMIZATION: "Debug and optimize existing code"
    }
    return descriptions.get(mode, "Unknown mode")

def _get_strategy_description(strategy: CodeGenerationStrategy) -> str:
    """Get description for code generation strategy"""
    descriptions = {
        CodeGenerationStrategy.INCREMENTAL: "Generate code incrementally with iterative improvements",
        CodeGenerationStrategy.ATOMIC: "Generate complete atomic units of code",
        CodeGenerationStrategy.PARALLEL: "Generate multiple code components in parallel",
        CodeGenerationStrategy.SEQUENTIAL: "Generate code components sequentially",
        CodeGenerationStrategy.ADAPTIVE: "Adaptively choose the best generation strategy"
    }
    return descriptions.get(strategy, "Unknown strategy")

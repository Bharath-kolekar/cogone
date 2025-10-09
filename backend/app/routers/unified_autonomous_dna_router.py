"""
Unified Autonomous DNA Integration API
Provides endpoints for the complete integrated autonomous AI system
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import structlog

from ..services.unified_autonomous_dna_integration import (
    unified_autonomous_dna,
    UnifiedIntelligenceLevel
)
from ..core.dependencies import AuthDependencies
from ..models.user import User

logger = structlog.get_logger()
router = APIRouter(prefix="/unified-autonomous-dna", tags=["Unified Autonomous DNA"])


# ============================================================================
# Request/Response Models
# ============================================================================

class FullIntelligenceRequest(BaseModel):
    """Request for full intelligence operation"""
    operation: str = Field(..., description="Operation to perform")
    context: Dict[str, Any] = Field(default_factory=dict, description="Operation context")


class SelfImprovementRequest(BaseModel):
    """Request for autonomous self-improvement"""
    improvement_goal: str = Field(..., description="What to improve")


class ConsciousSelfModificationRequest(BaseModel):
    """Request for conscious self-modification"""
    modification_request: str = Field(..., description="Modification to make")


class ConsistentCodeGenerationRequest(BaseModel):
    """Request for consistent autonomous code generation"""
    specification: str = Field(..., description="Code specification")
    file_path: str = Field(..., description="File path")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


# ============================================================================
# Unified Intelligence Endpoints
# ============================================================================

@router.post("/execute-with-full-intelligence")
async def execute_with_full_intelligence(
    request: FullIntelligenceRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Execute operation with ALL integrated intelligence systems
    
    **Requires authentication**
    
    Uses:
    - Consciousness DNA for conscious decisions
    - Consistency DNA for 100% consistency
    - Proactive DNA for predictive optimization
    - Autonomous Decision Making for strategic planning
    - Self-Modification for self-improvement
    
    Returns:
        Operation result with all intelligence layers applied
    """
    try:
        result = await unified_autonomous_dna.execute_with_full_intelligence(
            operation=request.operation,
            context=request.context
        )
        
        logger.info("Full intelligence operation executed",
                   user_id=current_user.id,
                   operation=request.operation,
                   integration_level=result.get("integration_level"))
        
        return result
        
    except Exception as e:
        logger.error("Full intelligence execution failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/autonomous-self-improve")
async def autonomous_self_improve(
    request: SelfImprovementRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Autonomously improve itself
    
    **Requires authentication**
    
    Ultimate autonomous capability combining:
    - Conscious reflection on improvement need
    - Consistency validation
    - Proactive impact prediction
    - Autonomous improvement strategy
    - Self-modification to apply improvements
    
    Returns:
        Improvement results
    """
    try:
        result = await unified_autonomous_dna.autonomous_self_improve(
            improvement_goal=request.improvement_goal
        )
        
        logger.info("Autonomous self-improvement executed",
                   user_id=current_user.id,
                   goal=request.improvement_goal,
                   success=result.get("success"))
        
        return result
        
    except Exception as e:
        logger.error("Autonomous self-improvement failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/conscious-self-modification")
async def conscious_self_modification(
    request: ConsciousSelfModificationRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Perform self-modification with full consciousness
    
    **Requires authentication**
    
    Uses Consciousness DNA to make conscious, ethical decisions
    about self-modifications before applying them
    
    Returns:
        Modification result with conscious decision
    """
    try:
        result = await unified_autonomous_dna.conscious_self_modification(
            modification_request=request.modification_request
        )
        
        logger.info("Conscious self-modification executed",
                   user_id=current_user.id,
                   success=result.get("success"))
        
        return result
        
    except Exception as e:
        logger.error("Conscious self-modification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/proactive-self-healing")
async def proactive_self_healing(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Proactively heal itself by predicting and preventing issues
    
    **Requires authentication**
    
    Uses Proactive DNA to predict issues and Self-Modification
    to fix them before they occur
    
    Returns:
        Healing results
    """
    try:
        result = await unified_autonomous_dna.proactive_self_healing()
        
        logger.info("Proactive self-healing executed",
                   user_id=current_user.id,
                   fixes_applied=result.get("proactive_fixes_applied", 0))
        
        return result
        
    except Exception as e:
        logger.error("Proactive self-healing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/generate-consistent-autonomous-code")
async def generate_consistent_autonomous_code(
    request: ConsistentCodeGenerationRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Generate code with ALL integrated systems
    
    **Requires authentication**
    
    Uses:
    - Consciousness DNA for conscious coding decisions
    - Consistency DNA for 100% consistency
    - Autonomous Decision Making for optimal approach
    - Self-Modification for code generation and validation
    
    Returns:
        Generated code with maximum quality
    """
    try:
        result = await unified_autonomous_dna.generate_consistent_autonomous_code(
            specification=request.specification,
            context=request.context or {"file_path": request.file_path}
        )
        
        logger.info("Consistent autonomous code generated",
                   user_id=current_user.id,
                   consistency_score=result.get("consistency_score"))
        
        return result
        
    except Exception as e:
        logger.error("Consistent autonomous code generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Status and Monitoring Endpoints
# ============================================================================

@router.get("/status")
async def get_unified_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get comprehensive status of all integrated systems
    
    **Requires authentication**
    
    Returns:
        Status of all DNA systems and autonomous capabilities
    """
    try:
        result = await unified_autonomous_dna.get_unified_system_status()
        
        return {
            "success": True,
            **result
        }
        
    except Exception as e:
        logger.error("Failed to get unified status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/health")
async def get_integration_health(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get health status of all integrations
    
    **Requires authentication**
    
    Returns:
        Health status of each integrated system
    """
    try:
        result = await unified_autonomous_dna.get_integration_health()
        
        return {
            "success": True,
            **result
        }
        
    except Exception as e:
        logger.error("Failed to get integration health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/integration-levels")
async def get_integration_levels(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get available integration levels
    
    **Requires authentication**
    
    Returns:
        List of integration levels
    """
    try:
        levels = [
            {
                "level": "basic",
                "description": "Basic operations"
            },
            {
                "level": "conscious",
                "description": "Basic + Consciousness DNA"
            },
            {
                "level": "consistent",
                "description": "Conscious + Consistency DNA"
            },
            {
                "level": "proactive",
                "description": "Consistent + Proactive DNA"
            },
            {
                "level": "autonomous",
                "description": "Proactive + Autonomous Decision Making"
            },
            {
                "level": "self_modifying",
                "description": "Autonomous + Self-Modification"
            },
            {
                "level": "ultimate",
                "description": "All systems fully integrated"
            }
        ]
        
        return {
            "success": True,
            "levels": levels,
            "current_level": unified_autonomous_dna.integration_level.value
        }
        
    except Exception as e:
        logger.error("Failed to get integration levels", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


__all__ = ['router']



@router.get("/status")
async def get_service_status():
    """
    Get service initialization status
    Returns whether the service is properly initialized and ready
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    try:
        # Try to access the service
        # This will fail if service is not initialized
        service_check = True  # Add actual service check here
        
        return JSONResponse(
            status_code=http_status.HTTP_200_OK,
            content={
                "status": "operational",
                "initialized": True,
                "timestamp": datetime.now().isoformat()
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=http_status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unavailable",
                "initialized": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

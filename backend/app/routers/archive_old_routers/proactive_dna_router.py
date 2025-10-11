"""
Proactive DNA API Router
Exposes endpoints for proactive intelligence and adaptive learning
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from ..services.proactive_intelligence_core import (
    proactive_intelligence_core,
    ProactivenessLevel,
    ProactiveActionType,
    AdaptiveLearningMode
)
from ..services.smart_coding_ai_optimized import SmartCodingAIOptimized

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/proactive-dna", tags=["Proactive DNA"])

# Initialize Smarty with Proactive DNA
smarty = SmartCodingAIOptimized()

@router.get("/status")
async def get_proactive_dna_status():
    """Get Proactive DNA system status"""
    try:
        status = smarty.get_proactive_dna_status()
        return {
            "success": True,
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting proactive DNA status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-and-prepare")
async def predict_and_prepare_proactively(request: Dict[str, Any]):
    """Predict future events and prepare proactive actions"""
    try:
        context = request.get("context", {})
        
        if not context:
            raise HTTPException(status_code=400, detail="Context is required")
        
        # Predict and prepare proactive actions
        result = await smarty.predict_and_prepare_proactively(context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in proactive prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/adapt-to-patterns")
async def adapt_to_patterns_proactively(request: Dict[str, Any]):
    """Adapt behavior based on feedback and patterns"""
    try:
        feedback = request.get("feedback", {})
        
        if not feedback:
            raise HTTPException(status_code=400, detail="Feedback is required")
        
        # Adapt to patterns proactively
        result = await smarty.adapt_to_patterns_proactively(feedback)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in adaptive learning: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/optimize-proactively")
async def optimize_proactively(request: Dict[str, Any]):
    """Proactively optimize system performance"""
    try:
        system_state = request.get("system_state", {})
        
        if not system_state:
            raise HTTPException(status_code=400, detail="System state is required")
        
        # Optimize proactively
        result = await smarty.optimize_proactively(system_state)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in proactive optimization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/prevent-issues")
async def prevent_issues_proactively(request: Dict[str, Any]):
    """Prevent issues before they occur"""
    try:
        risk_assessment = request.get("risk_assessment", {})
        
        if not risk_assessment:
            raise HTTPException(status_code=400, detail="Risk assessment is required")
        
        # Prevent issues proactively
        result = await smarty.prevent_issues_proactively(risk_assessment)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in preventive intelligence: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enhance-user-experience")
async def enhance_user_experience_proactively(request: Dict[str, Any]):
    """Proactively enhance user experience"""
    try:
        user_context = request.get("user_context", {})
        
        if not user_context:
            raise HTTPException(status_code=400, detail="User context is required")
        
        # Enhance user experience proactively
        result = await smarty.enhance_user_experience_proactively(user_context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in user experience enhancement: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-proactive-code")
async def generate_proactive_code(request: Dict[str, Any]):
    """Generate code with proactive intelligence"""
    try:
        prompt = request.get("prompt", "")
        language = request.get("language", "python")
        context = request.get("context", {})
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Generate code with proactive intelligence
        result = await smarty.generate_proactive_code(prompt, language, context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating proactive code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/proactiveness-levels")
async def get_proactiveness_levels():
    """Get available proactiveness levels"""
    try:
        levels = [level.value for level in ProactivenessLevel]
        return {
            "success": True,
            "data": {
                "proactiveness_levels": levels,
                "current_level": smarty.proactiveness_level.value,
                "descriptions": {
                    "reactive": "Respond to events after they occur",
                    "predictive": "Predict and prepare for likely events",
                    "preventive": "Prevent issues before they occur",
                    "optimizing": "Continuously optimize performance",
                    "adaptive": "Learn and adapt to new patterns"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting proactiveness levels: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/action-types")
async def get_proactive_action_types():
    """Get available proactive action types"""
    try:
        action_types = [action_type.value for action_type in ProactiveActionType]
        return {
            "success": True,
            "data": {
                "action_types": action_types,
                "descriptions": {
                    "preventive_maintenance": "Preventive system maintenance",
                    "resource_optimization": "Optimize resource usage",
                    "security_hardening": "Enhance security measures",
                    "performance_scaling": "Scale performance resources",
                    "capacity_planning": "Plan for capacity needs",
                    "failure_prevention": "Prevent system failures",
                    "user_experience_enhancement": "Enhance user experience",
                    "cost_optimization": "Optimize operational costs",
                    "data_backup": "Perform data backups",
                    "system_health_check": "Check system health"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting action types: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/learning-modes")
async def get_adaptive_learning_modes():
    """Get available adaptive learning modes"""
    try:
        learning_modes = [mode.value for mode in AdaptiveLearningMode]
        return {
            "success": True,
            "data": {
                "learning_modes": learning_modes,
                "current_mode": "reinforcement",  # Default mode
                "descriptions": {
                    "supervised": "Learning from labeled data",
                    "unsupervised": "Learning from patterns",
                    "reinforcement": "Learning from rewards/penalties",
                    "transfer": "Learning from related domains",
                    "meta": "Learning to learn"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting learning modes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/set-proactiveness-level")
async def set_proactiveness_level(request: Dict[str, Any]):
    """Set the proactiveness level"""
    try:
        level = request.get("level", "")
        
        if not level:
            raise HTTPException(status_code=400, detail="Level is required")
        
        if level not in [l.value for l in ProactivenessLevel]:
            raise HTTPException(status_code=400, detail="Invalid proactiveness level")
        
        # Set the proactiveness level
        smarty.proactiveness_level = ProactivenessLevel(level)
        
        return {
            "success": True,
            "message": f"Proactiveness level set to {level}",
            "data": {
                "previous_level": "adaptive",  # Default
                "new_level": level,
                "proactiveness_levels": [l.value for l in ProactivenessLevel]
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error setting proactiveness level: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enable-adaptive-learning")
async def enable_adaptive_learning():
    """Enable adaptive learning"""
    try:
        smarty.adaptive_learning_enabled = True
        
        return {
            "success": True,
            "message": "Adaptive learning enabled",
            "data": {
                "adaptive_learning_enabled": True,
                "proactiveness_level": smarty.proactiveness_level.value
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error enabling adaptive learning: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/disable-adaptive-learning")
async def disable_adaptive_learning():
    """Disable adaptive learning"""
    try:
        smarty.adaptive_learning_enabled = False
        
        return {
            "success": True,
            "message": "Adaptive learning disabled",
            "data": {
                "adaptive_learning_enabled": False,
                "proactiveness_level": smarty.proactiveness_level.value
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error disabling adaptive learning: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_proactive_metrics():
    """Get proactive intelligence metrics"""
    try:
        proactive_status = smarty.get_proactive_dna_status()
        metrics = proactive_status.get("proactive_intelligence_status", {}).get("proactive_metrics", {})
        
        return {
            "success": True,
            "data": {
                "metrics": metrics,
                "proactiveness_level": smarty.proactiveness_level.value,
                "adaptive_learning_enabled": smarty.adaptive_learning_enabled,
                "dna_active": smarty.proactive_dna_active
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting proactive metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def proactive_dna_health_check():
    """Health check for Proactive DNA system"""
    try:
        # Check if all components are working
        dna_status = smarty.get_proactive_dna_status()
        
        health_status = {
            "proactive_dna_active": dna_status.get("proactive_dna_active", False),
            "proactiveness_level": dna_status.get("proactiveness_level", "unknown"),
            "adaptive_learning_enabled": dna_status.get("adaptive_learning_enabled", False),
            "proactive_intelligence_status": dna_status.get("proactive_intelligence_status", {}),
            "status": "healthy" if dna_status.get("proactive_dna_active", False) else "degraded"
        }
        
        return {
            "success": True,
            "data": health_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in proactive DNA health check: {e}")
        return {
            "success": False,
            "error": str(e),
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat()
        }

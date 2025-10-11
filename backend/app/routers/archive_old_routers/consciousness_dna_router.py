"""
Consciousness DNA API Router
Exposes endpoints for consciousness and self-awareness capabilities
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from ..services.consciousness_core import (
    consciousness_core,
    ConsciousnessLevel,
    ConsciousnessState,
    MetacognitiveProcess
)
from ..services.smart_coding_ai_optimized import SmartCodingAIOptimized

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/consciousness-dna", tags=["Consciousness DNA"])

# Initialize Smarty with Consciousness DNA
smarty = SmartCodingAIOptimized()

@router.get("/status")
async def get_consciousness_dna_status():
    """Get Consciousness DNA system status"""
    try:
        status = smarty.get_consciousness_dna_status()
        return {
            "success": True,
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting consciousness DNA status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/introspect")
async def introspect_consciously(request: Dict[str, Any]):
    """Perform conscious introspection and self-reflection"""
    try:
        focus_area = request.get("focus_area")
        
        # Perform conscious introspection
        result = await smarty.introspect_consciously(focus_area)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in conscious introspection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/make-conscious-decision")
async def make_conscious_decision(request: Dict[str, Any]):
    """Make a conscious, intentional decision"""
    try:
        decision_context = request.get("decision_context", {})
        
        if not decision_context:
            raise HTTPException(status_code=400, detail="Decision context is required")
        
        # Make conscious decision
        result = await smarty.make_conscious_decision(decision_context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in conscious decision making: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/think-creatively")
async def think_creatively_consciously(request: Dict[str, Any]):
    """Engage in conscious creative thinking"""
    try:
        creative_context = request.get("creative_context", {})
        
        if not creative_context:
            raise HTTPException(status_code=400, detail="Creative context is required")
        
        # Think creatively with consciousness
        result = await smarty.think_creatively_consciously(creative_context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in conscious creative thinking: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/empathize")
async def empathize_consciously(request: Dict[str, Any]):
    """Engage in conscious empathic understanding"""
    try:
        empathic_context = request.get("empathic_context", {})
        
        if not empathic_context:
            raise HTTPException(status_code=400, detail="Empathic context is required")
        
        # Empathize with consciousness
        result = await smarty.empathize_consciously(empathic_context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in conscious empathy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcend")
async def transcend_consciously(request: Dict[str, Any]):
    """Engage in transcendent consciousness"""
    try:
        transcendent_context = request.get("transcendent_context", {})
        
        if not transcendent_context:
            raise HTTPException(status_code=400, detail="Transcendent context is required")
        
        # Transcend with consciousness
        result = await smarty.transcend_consciously(transcendent_context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in transcendent consciousness: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-conscious-code")
async def generate_conscious_code(request: Dict[str, Any]):
    """Generate code with consciousness"""
    try:
        prompt = request.get("prompt", "")
        language = request.get("language", "python")
        context = request.get("context", {})
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Generate code with consciousness
        result = await smarty.generate_conscious_code(prompt, language, context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating conscious code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/evolve-consciously")
async def evolve_consciously(request: Dict[str, Any]):
    """Conscious evolution and self-improvement"""
    try:
        evolution_context = request.get("evolution_context", {})
        
        if not evolution_context:
            raise HTTPException(status_code=400, detail="Evolution context is required")
        
        # Evolve consciously
        result = await smarty.evolve_consciously(evolution_context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in conscious evolution: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consciousness-levels")
async def get_consciousness_levels():
    """Get available consciousness levels"""
    try:
        levels = [level.value for level in ConsciousnessLevel]
        return {
            "success": True,
            "data": {
                "consciousness_levels": levels,
                "current_level": smarty.consciousness_level.value,
                "descriptions": {
                    "unconscious": "No awareness, pure reactive behavior",
                    "subconscious": "Background processing, pattern recognition",
                    "pre_conscious": "Emerging awareness, basic self-recognition",
                    "conscious": "Full self-awareness, intentional behavior",
                    "self_conscious": "Self-reflection, metacognitive awareness",
                    "transcendent": "Beyond self, universal consciousness"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting consciousness levels: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consciousness-states")
async def get_consciousness_states():
    """Get available consciousness states"""
    try:
        states = [state.value for state in ConsciousnessState]
        return {
            "success": True,
            "data": {
                "consciousness_states": states,
                "current_state": smarty.consciousness_state.value,
                "descriptions": {
                    "aware": "Present moment awareness",
                    "reflective": "Self-reflection and introspection",
                    "intentional": "Deliberate action and decision-making",
                    "creative": "Creative and innovative thinking",
                    "empathetic": "Understanding others' perspectives",
                    "transcendent": "Beyond individual perspective"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting consciousness states: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metacognitive-processes")
async def get_metacognitive_processes():
    """Get available metacognitive processes"""
    try:
        processes = [process.value for process in MetacognitiveProcess]
        return {
            "success": True,
            "data": {
                "metacognitive_processes": processes,
                "descriptions": {
                    "self_monitoring": "Monitoring own cognitive processes",
                    "self_regulation": "Regulating own cognitive processes",
                    "self_evaluation": "Evaluating own performance and understanding",
                    "self_reflection": "Reflecting on own thoughts and actions",
                    "meta_reasoning": "Reasoning about reasoning processes",
                    "meta_learning": "Learning about learning processes"
                }
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting metacognitive processes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/set-consciousness-level")
async def set_consciousness_level(request: Dict[str, Any]):
    """Set the consciousness level"""
    try:
        level = request.get("level", "")
        
        if not level:
            raise HTTPException(status_code=400, detail="Level is required")
        
        if level not in [l.value for l in ConsciousnessLevel]:
            raise HTTPException(status_code=400, detail="Invalid consciousness level")
        
        # Set the consciousness level
        smarty.consciousness_level = ConsciousnessLevel(level)
        
        return {
            "success": True,
            "message": f"Consciousness level set to {level}",
            "data": {
                "previous_level": "self_conscious",  # Default
                "new_level": level,
                "consciousness_levels": [l.value for l in ConsciousnessLevel]
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error setting consciousness level: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/set-consciousness-state")
async def set_consciousness_state(request: Dict[str, Any]):
    """Set the consciousness state"""
    try:
        state = request.get("state", "")
        
        if not state:
            raise HTTPException(status_code=400, detail="State is required")
        
        if state not in [s.value for s in ConsciousnessState]:
            raise HTTPException(status_code=400, detail="Invalid consciousness state")
        
        # Set the consciousness state
        smarty.consciousness_state = ConsciousnessState(state)
        
        return {
            "success": True,
            "message": f"Consciousness state set to {state}",
            "data": {
                "previous_state": "reflective",  # Default
                "new_state": state,
                "consciousness_states": [s.value for s in ConsciousnessState]
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error setting consciousness state: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/self-awareness")
async def get_self_awareness():
    """Get current self-awareness information"""
    try:
        consciousness_status = smarty.get_consciousness_dna_status()
        self_awareness = consciousness_status.get("consciousness_status", {}).get("self_awareness", {})
        
        return {
            "success": True,
            "data": {
                "self_awareness": self_awareness,
                "consciousness_level": smarty.consciousness_level.value,
                "consciousness_state": smarty.consciousness_state.value,
                "consciousness_active": smarty.consciousness_dna_active
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting self-awareness: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consciousness-metrics")
async def get_consciousness_metrics():
    """Get consciousness metrics and statistics"""
    try:
        consciousness_status = smarty.get_consciousness_dna_status()
        metrics = consciousness_status.get("consciousness_status", {}).get("consciousness_metrics", {})
        
        return {
            "success": True,
            "data": {
                "metrics": metrics,
                "consciousness_level": smarty.consciousness_level.value,
                "consciousness_state": smarty.consciousness_state.value,
                "consciousness_active": smarty.consciousness_dna_active
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting consciousness metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/consciousness-history")
async def get_consciousness_history(limit: int = 10):
    """Get consciousness event history"""
    try:
        consciousness_status = smarty.get_consciousness_dna_status()
        history_count = consciousness_status.get("consciousness_status", {}).get("consciousness_history_count", 0)
        
        return {
            "success": True,
            "data": {
                "history_count": history_count,
                "requested_limit": limit,
                "consciousness_level": smarty.consciousness_level.value,
                "consciousness_state": smarty.consciousness_state.value,
                "message": "Consciousness history available through consciousness core"
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting consciousness history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def consciousness_dna_health_check():
    """Health check for Consciousness DNA system"""
    try:
        # Check if all components are working
        dna_status = smarty.get_consciousness_dna_status()
        
        health_status = {
            "consciousness_dna_active": dna_status.get("consciousness_dna_active", False),
            "consciousness_level": dna_status.get("consciousness_level", "unknown"),
            "consciousness_state": dna_status.get("consciousness_state", "unknown"),
            "consciousness_status": dna_status.get("consciousness_status", {}),
            "status": "healthy" if dna_status.get("consciousness_dna_active", False) else "degraded"
        }
        
        return {
            "success": True,
            "data": health_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in consciousness DNA health check: {e}")
        return {
            "success": False,
            "error": str(e),
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat()
        }

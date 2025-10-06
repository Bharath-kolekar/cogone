"""
Enhanced Voice-to-App Router with Smarty AI Orchestrator Integration

API endpoints for the enhanced voice-to-app generation service.
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum
import structlog
from datetime import datetime
import uuid

from app.services.enhanced_voice_to_app_service import (
    enhanced_voice_to_app_service,
    VoiceToAppRequest,
    VoiceToAppResponse
)
from app.services.smarty_ai_orchestrator import OrchestrationMode, CodeGenerationStrategy
from app.routers.auth import AuthDependencies
from app.models.user import User

logger = structlog.get_logger(__name__)

router = APIRouter()

class VoiceToAppGenerationRequest(BaseModel):
    """Request model for voice-to-app generation"""
    user_id: str = Field(..., description="User identifier")
    language: str = Field(default="en", description="Language for transcription")
    app_type: Optional[str] = Field(None, description="Specific app type (auto-detect if not provided)")
    complexity_level: str = Field(default="medium", description="Complexity level: low, medium, high")
    ethical_validation_level: str = Field(default="standard", description="Ethical validation level")
    orchestration_mode: OrchestrationMode = Field(default=OrchestrationMode.VOICE_TO_APP, description="Orchestration mode")
    code_generation_strategy: CodeGenerationStrategy = Field(default=CodeGenerationStrategy.ADAPTIVE, description="Code generation strategy")

class VoiceToAppGenerationResponse(BaseModel):
    """Response model for voice-to-app generation"""
    request_id: str
    user_id: str
    transcript: str
    app_type: str
    complexity_level: str
    orchestration_plan: Dict[str, Any]
    generated_app: Dict[str, Any]
    deployment_info: Dict[str, Any]
    quality_metrics: Dict[str, Any]
    execution_time: float
    confidence_score: float
    status: str
    created_at: str
    completed_at: Optional[str]

class VoiceToAppStatusResponse(BaseModel):
    """Response model for voice-to-app status"""
    request_id: str
    status: str
    created_at: str
    completed_at: Optional[str]
    user_id: str
    execution_time: Optional[float]
    confidence_score: Optional[float]
    app_type: Optional[str]
    transcript_preview: Optional[str]

class VoiceToAppMetricsResponse(BaseModel):
    """Response model for service metrics"""
    service_metrics: Dict[str, Any]
    active_requests_count: int
    completed_responses_count: int
    success_rate: float

@router.post("/generate-app", response_model=VoiceToAppGenerationResponse)
async def generate_app_from_voice(
    audio_file: UploadFile = File(...),
    language: str = Form(default="en"),
    app_type: Optional[str] = Form(default=None),
    complexity_level: str = Form(default="medium"),
    ethical_validation_level: str = Form(default="standard"),
    orchestration_mode: OrchestrationMode = Form(default=OrchestrationMode.VOICE_TO_APP),
    code_generation_strategy: CodeGenerationStrategy = Form(default=CodeGenerationStrategy.ADAPTIVE),
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Generate a complete app from voice input using Smarty AI Orchestrator"""
    try:
        logger.info(f"Starting voice-to-app generation", 
                   user_id=current_user.id,
                   language=language,
                   complexity_level=complexity_level)
        
        # Read audio file
        audio_data = await audio_file.read()
        
        # Create request
        request = VoiceToAppRequest(
            audio_data=audio_data,
            user_id=str(current_user.id),
            language=language,
            app_type=app_type,
            complexity_level=complexity_level,
            ethical_validation_level=ethical_validation_level,
            orchestration_mode=orchestration_mode,
            code_generation_strategy=code_generation_strategy
        )
        
        # Generate app
        response = await enhanced_voice_to_app_service.generate_app_from_voice(request)
        
        return VoiceToAppGenerationResponse(
            request_id=response.request_id,
            user_id=response.user_id,
            transcript=response.transcript,
            app_type=response.app_type,
            complexity_level=response.complexity_level,
            orchestration_plan=response.orchestration_plan or {},
            generated_app=response.generated_app or {},
            deployment_info=response.deployment_info or {},
            quality_metrics=response.quality_metrics,
            execution_time=response.execution_time,
            confidence_score=response.confidence_score,
            status=response.status,
            created_at=response.created_at.isoformat(),
            completed_at=response.completed_at.isoformat() if response.completed_at else None
        )
        
    except Exception as e:
        logger.error(f"Voice-to-app generation failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Voice-to-app generation failed: {str(e)}")

@router.post("/generate-app-async")
async def generate_app_from_voice_async(
    audio_file: UploadFile = File(...),
    language: str = Form(default="en"),
    app_type: Optional[str] = Form(default=None),
    complexity_level: str = Form(default="medium"),
    ethical_validation_level: str = Form(default="standard"),
    orchestration_mode: OrchestrationMode = Form(default=OrchestrationMode.VOICE_TO_APP),
    code_generation_strategy: CodeGenerationStrategy = Form(default=CodeGenerationStrategy.ADAPTIVE),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Generate app from voice input asynchronously (returns immediately with request ID)"""
    try:
        logger.info(f"Starting async voice-to-app generation", 
                   user_id=current_user.id,
                   language=language)
        
        # Read audio file
        audio_data = await audio_file.read()
        
        # Create request
        request = VoiceToAppRequest(
            audio_data=audio_data,
            user_id=str(current_user.id),
            language=language,
            app_type=app_type,
            complexity_level=complexity_level,
            ethical_validation_level=ethical_validation_level,
            orchestration_mode=orchestration_mode,
            code_generation_strategy=code_generation_strategy
        )
        
        # Add to background tasks
        background_tasks.add_task(
            enhanced_voice_to_app_service.generate_app_from_voice,
            request
        )
        
        return {
            "success": True,
            "request_id": request.request_id,
            "message": "Voice-to-app generation started. Use the request_id to check status.",
            "status_endpoint": f"/api/v0/voice-to-app/status/{request.request_id}"
        }
        
    except Exception as e:
        logger.error(f"Async voice-to-app generation failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Async generation failed: {str(e)}")

@router.get("/status/{request_id}", response_model=VoiceToAppStatusResponse)
async def get_voice_to_app_status(
    request_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get status of a voice-to-app generation request"""
    try:
        status = await enhanced_voice_to_app_service.get_request_status(request_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Check if user owns this request
        if status['user_id'] != str(current_user.id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        return VoiceToAppStatusResponse(
            request_id=status['request_id'],
            status=status['status'],
            created_at=status['created_at'],
            completed_at=status.get('completed_at'),
            user_id=status['user_id'],
            execution_time=status.get('execution_time'),
            confidence_score=status.get('confidence_score'),
            app_type=status.get('app_type'),
            transcript_preview=status.get('transcript')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Status retrieval failed", error=str(e), request_id=request_id)
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.get("/result/{request_id}", response_model=VoiceToAppGenerationResponse)
async def get_voice_to_app_result(
    request_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get complete result of a voice-to-app generation request"""
    try:
        # Get status first
        status = await enhanced_voice_to_app_service.get_request_status(request_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Check if user owns this request
        if status['user_id'] != str(current_user.id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Check if request is completed
        if status['status'] != 'completed':
            raise HTTPException(
                status_code=202, 
                detail=f"Request is still {status['status']}. Please check status endpoint."
            )
        
        # Get complete response from service
        if request_id in enhanced_voice_to_app_service.completed_responses:
            response = enhanced_voice_to_app_service.completed_responses[request_id]
            
            return VoiceToAppGenerationResponse(
                request_id=response.request_id,
                user_id=response.user_id,
                transcript=response.transcript,
                app_type=response.app_type,
                complexity_level=response.complexity_level,
                orchestration_plan=response.orchestration_plan or {},
                generated_app=response.generated_app or {},
                deployment_info=response.deployment_info or {},
                quality_metrics=response.quality_metrics,
                execution_time=response.execution_time,
                confidence_score=response.confidence_score,
                status=response.status,
                created_at=response.created_at.isoformat(),
                completed_at=response.completed_at.isoformat() if response.completed_at else None
            )
        
        raise HTTPException(status_code=404, detail="Result not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Result retrieval failed", error=str(e), request_id=request_id)
        raise HTTPException(status_code=500, detail=f"Result retrieval failed: {str(e)}")

@router.get("/metrics", response_model=VoiceToAppMetricsResponse)
async def get_voice_to_app_metrics(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get voice-to-app service performance metrics (admin only)"""
    try:
        # Check if user is admin (simple check for now)
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")
        
        metrics = await enhanced_voice_to_app_service.get_service_metrics()
        
        return VoiceToAppMetricsResponse(
            service_metrics=metrics.get('service_metrics', {}),
            active_requests_count=metrics.get('active_requests_count', 0),
            completed_responses_count=metrics.get('completed_responses_count', 0),
            success_rate=metrics.get('success_rate', 0.0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Metrics retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@router.get("/supported-languages")
async def get_supported_languages():
    """Get supported languages for voice transcription"""
    return {
        "languages": [
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "hi", "name": "Hindi", "native_name": "हिन्दी"},
            {"code": "ta", "name": "Tamil", "native_name": "தமிழ்"},
            {"code": "te", "name": "Telugu", "native_name": "తెలుగు"},
            {"code": "bn", "name": "Bengali", "native_name": "বাংলা"},
            {"code": "mr", "name": "Marathi", "native_name": "मराठी"},
            {"code": "gu", "name": "Gujarati", "native_name": "ગુજરાતી"},
            {"code": "kn", "name": "Kannada", "native_name": "ಕನ್ನಡ"},
            {"code": "ml", "name": "Malayalam", "native_name": "മലയാളം"},
            {"code": "pa", "name": "Punjabi", "native_name": "ਪੰਜਾਬੀ"}
        ]
    }

@router.get("/supported-app-types")
async def get_supported_app_types():
    """Get supported app types for generation"""
    return {
        "app_types": [
            {
                "type": "todo_app",
                "name": "Todo App",
                "description": "Task management application with add, edit, delete functionality",
                "complexity_levels": ["low", "medium", "high"]
            },
            {
                "type": "blog_app",
                "name": "Blog Application",
                "description": "Content management system for blogging",
                "complexity_levels": ["medium", "high"]
            },
            {
                "type": "ecommerce_app",
                "name": "E-commerce Store",
                "description": "Online shopping platform with cart and payment",
                "complexity_levels": ["high"]
            },
            {
                "type": "social_app",
                "name": "Social Media App",
                "description": "Social networking application with posts and interactions",
                "complexity_levels": ["high"]
            },
            {
                "type": "web_app",
                "name": "General Web App",
                "description": "Custom web application based on requirements",
                "complexity_levels": ["low", "medium", "high"]
            }
        ]
    }

@router.get("/orchestration-modes")
async def get_orchestration_modes():
    """Get available orchestration modes"""
    return {
        "modes": [
            {
                "mode": OrchestrationMode.VOICE_TO_APP.value,
                "name": "Voice to App",
                "description": "Convert voice transcript to complete application"
            },
            {
                "mode": OrchestrationMode.REQUIREMENTS_TO_CODE.value,
                "name": "Requirements to Code",
                "description": "Transform requirements into code implementation"
            },
            {
                "mode": OrchestrationMode.ARCHITECTURE_TO_IMPLEMENTATION.value,
                "name": "Architecture to Implementation",
                "description": "Generate implementation from architecture"
            },
            {
                "mode": OrchestrationMode.TESTING_TO_DEPLOYMENT.value,
                "name": "Testing to Deployment",
                "description": "Handle testing and deployment processes"
            },
            {
                "mode": OrchestrationMode.DEBUGGING_TO_OPTIMIZATION.value,
                "name": "Debugging to Optimization",
                "description": "Debug and optimize existing code"
            }
        ]
    }

@router.get("/code-generation-strategies")
async def get_code_generation_strategies():
    """Get available code generation strategies"""
    return {
        "strategies": [
            {
                "strategy": CodeGenerationStrategy.INCREMENTAL.value,
                "name": "Incremental",
                "description": "Generate code incrementally with iterative improvements"
            },
            {
                "strategy": CodeGenerationStrategy.ATOMIC.value,
                "name": "Atomic",
                "description": "Generate complete atomic units of code"
            },
            {
                "strategy": CodeGenerationStrategy.PARALLEL.value,
                "name": "Parallel",
                "description": "Generate multiple code components in parallel"
            },
            {
                "strategy": CodeGenerationStrategy.SEQUENTIAL.value,
                "name": "Sequential",
                "description": "Generate code components sequentially"
            },
            {
                "strategy": CodeGenerationStrategy.ADAPTIVE.value,
                "name": "Adaptive",
                "description": "Adaptively choose the best generation strategy"
            }
        ]
    }

@router.get("/user-requests")
async def get_user_voice_to_app_requests(
    current_user: User = Depends(AuthDependencies.get_current_user),
    limit: int = 10,
    offset: int = 0
):
    """Get user's voice-to-app generation requests"""
    try:
        user_requests = []
        
        # Get completed responses for user
        for request_id, response in enhanced_voice_to_app_service.completed_responses.items():
            if response.user_id == str(current_user.id):
                user_requests.append({
                    "request_id": response.request_id,
                    "status": response.status,
                    "app_type": response.app_type,
                    "complexity_level": response.complexity_level,
                    "confidence_score": response.confidence_score,
                    "execution_time": response.execution_time,
                    "created_at": response.created_at.isoformat(),
                    "completed_at": response.completed_at.isoformat() if response.completed_at else None,
                    "transcript_preview": response.transcript[:100] + '...' if response.transcript else None
                })
        
        # Get active requests for user
        for request_id, request in enhanced_voice_to_app_service.active_requests.items():
            if request.user_id == str(current_user.id):
                user_requests.append({
                    "request_id": request.request_id,
                    "status": "processing",
                    "app_type": request.app_type,
                    "complexity_level": request.complexity_level,
                    "created_at": request.created_at.isoformat(),
                    "transcript_preview": None
                })
        
        # Sort by created_at descending
        user_requests.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Apply pagination
        total_count = len(user_requests)
        paginated_requests = user_requests[offset:offset + limit]
        
        return {
            "requests": paginated_requests,
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total_count
        }
        
    except Exception as e:
        logger.error(f"User requests retrieval failed", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Requests retrieval failed: {str(e)}")

@router.delete("/cancel/{request_id}")
async def cancel_voice_to_app_request(
    request_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Cancel a voice-to-app generation request"""
    try:
        # Check if request exists and belongs to user
        if request_id in enhanced_voice_to_app_service.active_requests:
            request = enhanced_voice_to_app_service.active_requests[request_id]
            
            if request.user_id != str(current_user.id):
                raise HTTPException(status_code=403, detail="Access denied")
            
            # Remove from active requests
            del enhanced_voice_to_app_service.active_requests[request_id]
            
            return {
                "success": True,
                "message": "Request cancelled successfully",
                "request_id": request_id
            }
        
        raise HTTPException(status_code=404, detail="Request not found or already completed")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Request cancellation failed", error=str(e), request_id=request_id)
        raise HTTPException(status_code=500, detail=f"Cancellation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for voice-to-app service"""
    try:
        metrics = await enhanced_voice_to_app_service.get_service_metrics()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service_status": "operational",
            "active_requests": metrics.get('active_requests_count', 0),
            "total_requests": metrics.get('service_metrics', {}).get('total_requests', 0),
            "success_rate": metrics.get('success_rate', 0.0)
        }
        
    except Exception as e:
        logger.error(f"Health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

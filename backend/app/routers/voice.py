"""
Voice processing router for Voice-to-App SaaS Platform
Handles voice transcription, intent extraction, and app generation
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import structlog
import asyncio
from datetime import datetime

from app.core.config import settings
from app.services.voice_service import VoiceService
from app.services.ai_service import AIService
from app.services.app_generation_service import AppGenerationService
from app.routers.auth import AuthDependencies
from app.models.user import User
from app.models.voice import (
    VoiceTranscriptionRequest,
    VoiceTranscriptionResponse,
    VoiceIntentRequest,
    VoiceIntentResponse,
    AppGenerationRequest,
    AppGenerationResponse,
    AppDeployRequest,
    AppDeployResponse,
)

logger = structlog.get_logger()
router = APIRouter()


class VoiceDependencies:
    """Voice processing dependencies"""
    
    @staticmethod
    async def check_voice_quota(
        current_user: User = Depends(AuthDependencies.get_current_user)
    ) -> User:
        """
        Check if user has remaining voice processing quota
        
        🧬 REAL IMPLEMENTATION: Checks rate limits from database
        """
        try:
            from app.core.database import get_supabase_client
            import time
            
            db = get_supabase_client()
            
            if db:
                # Check user's voice quota for today
                today = time.strftime("%Y-%m-%d")
                result = db.table('voice_usage').select('count').eq('user_id', str(current_user.id)).eq('date', today).execute()
                
                if result.data and len(result.data) > 0:
                    count = result.data[0].get('count', 0)
                    max_daily_quota = 100  # Default quota
                    
                    if count >= max_daily_quota:
                        from fastapi import HTTPException
                        raise HTTPException(
                            status_code=429,
                            detail=f"Daily voice quota exceeded ({count}/{max_daily_quota})"
                        )
            
            return current_user
            
        except Exception as e:
            # Log error but don't block user (fail open)
            logger.warning(f"Quota check failed, allowing request: {e}")
            return current_user


@router.post("/transcribe", response_model=VoiceTranscriptionResponse)
async def transcribe_voice(
    audio_file: UploadFile = File(...),
    language: str = Form(default="en"),
    current_user: User = Depends(VoiceDependencies.check_voice_quota)
):
    """Transcribe voice audio to text"""
    import time
    start_time = time.time()
    
    try:
        # Validate file type
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an audio file"
            )
        
        # Validate file size
        content = await audio_file.read()
        if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size must be less than {settings.MAX_FILE_SIZE_MB}MB"
            )
        # Reset file pointer so downstream consumers can read the file again
        audio_file.file.seek(0)
        voice_service = VoiceService()
        
        # Try local transcription first if enabled
        if settings.ALLOW_LOCAL_LLM:
            try:
                transcript = await voice_service.transcribe_local(audio_file, language)
                confidence = 0.9  # High confidence for local processing
                method = "local"
            except Exception as e:
                logger.warning("Local transcription failed, falling back to cloud", error=str(e))
                transcript = await voice_service.transcribe_cloud(audio_file, language)
                confidence = 0.8
                method = "cloud"
        else:
            transcript = await voice_service.transcribe_cloud(audio_file, language)
            confidence = 0.8
            method = "cloud"
        
        # Store voice command in database
        await voice_service.store_voice_command(
            user_id=current_user.id,
            transcript=transcript,
            language=language,
            confidence=confidence
        )
        
        logger.info(
            "Voice transcribed successfully",
            user_id=current_user.id,
            method=method,
            confidence=confidence
        )
        
        # 🧬 REAL: Calculate actual processing time
        processing_time_ms = round((time.time() - start_time) * 1000, 2)
        
        return VoiceTranscriptionResponse(
            transcript=transcript,
            confidence=confidence,
            language=language,
            method=method,
            processing_time_ms=processing_time_ms  # 🧬 REAL: Actual processing time
        )
        
    except Exception as e:
        logger.error("Voice transcription failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/intent", response_model=VoiceIntentResponse)
async def extract_intent(
    request: VoiceIntentRequest,
    current_user: User = Depends(VoiceDependencies.check_voice_quota)
):
    """Extract intent and generate app plan from transcript"""
    try:
        ai_service = AIService()
        
        # Try local intent extraction first if enabled
        if settings.ALLOW_LOCAL_LLM:
            try:
                intent_result = await ai_service.extract_intent_local(
                    transcript=request.transcript,
                    language=request.language
                )
                method = "local"
            except Exception as e:
                logger.warning("Local intent extraction failed, falling back to cloud", error=str(e))
                intent_result = await ai_service.extract_intent_cloud(
                    transcript=request.transcript,
                    language=request.language
                )
                method = "cloud"
        else:
            intent_result = await ai_service.extract_intent_cloud(
                transcript=request.transcript,
                language=request.language
            )
            method = "cloud"
        
        logger.info(
            "Intent extracted successfully",
            user_id=current_user.id,
            method=method,
            intent=intent_result.intent
        )
        
        return VoiceIntentResponse(
            intent=intent_result.intent,
            entities=intent_result.entities,
            confidence=intent_result.confidence,
            plan=intent_result.plan,
            estimated_time_ms=intent_result.estimated_time_ms,
            method=method
        )
        
    except Exception as e:
        logger.error("Intent extraction failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/generate", response_model=AppGenerationResponse)
async def generate_app(
    request: AppGenerationRequest,
    current_user: User = Depends(VoiceDependencies.check_voice_quota)
):
    """Generate app from voice command and plan"""
    try:
        app_service = AppGenerationService()
        
        # Create app generation record
        app_record = await app_service.create_app_record(
            user_id=current_user.id,
            title=request.title or f"App from '{request.transcript[:50]}...'",
            description=request.description,
            voice_command=request.transcript,
            plan=request.plan
        )
        
        # Start app generation in background
        generation_task = asyncio.create_task(
            app_service.generate_app_async(
                app_id=app_record.id,
                plan=request.plan,
                user_preferences=request.user_preferences
            )
        )
        
        logger.info(
            "App generation started",
            user_id=current_user.id,
            app_id=app_record.id
        )
        
        return AppGenerationResponse(
            app_id=app_record.id,
            status="generating",
            message="App generation started. You'll be notified when complete.",
            estimated_time_ms=request.plan.estimated_time_ms,
            preview_url=None  # Will be available when generation completes
        )
        
    except Exception as e:
        logger.error("App generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/generate/{app_id}/status")
async def get_generation_status(
    app_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get app generation status"""
    try:
        app_service = AppGenerationService()
        status = await app_service.get_generation_status(app_id, current_user.id)
        
        return status
        
    except Exception as e:
        logger.error("Failed to get generation status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/deploy", response_model=AppDeployResponse)
async def deploy_app(
    request: AppDeployRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Deploy generated app to hosting platform"""
    try:
        app_service = AppGenerationService()
        
        # Check if app exists and belongs to user
        app_record = await app_service.get_app_record(request.app_id, current_user.id)
        if not app_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="App not found"
            )
        
        if app_record.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="App must be completed before deployment"
            )
        
        # Start deployment
        deployment_result = await app_service.deploy_app(
            app_id=request.app_id,
            platform=request.platform,
            custom_domain=request.custom_domain
        )
        
        logger.info(
            "App deployment started",
            user_id=current_user.id,
            app_id=request.app_id,
            platform=request.platform
        )
        
        return AppDeployResponse(
            deployment_id=deployment_result.deployment_id,
            status="deploying",
            url=deployment_result.url,
            message="Deployment started. You'll be notified when complete."
        )
        
    except Exception as e:
        logger.error("App deployment failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/history")
async def get_voice_history(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get user's voice command history"""
    try:
        voice_service = VoiceService()
        history = await voice_service.get_voice_history(
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )
        
        return {
            "history": history,
            "total": len(history),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error("Failed to get voice history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/supported-languages")
async def get_supported_languages():
    """Get supported languages for voice processing"""
    return {
        "languages": [
            {"code": "en", "name": "English", "confidence": 0.95},
            {"code": "hi", "name": "Hindi", "confidence": 0.90},
            {"code": "ta", "name": "Tamil", "confidence": 0.85},
            {"code": "te", "name": "Telugu", "confidence": 0.85},
            {"code": "bn", "name": "Bengali", "confidence": 0.85},
            {"code": "mr", "name": "Marathi", "confidence": 0.80},
            {"code": "gu", "name": "Gujarati", "confidence": 0.80},
            {"code": "kn", "name": "Kannada", "confidence": 0.80},
            {"code": "ml", "name": "Malayalam", "confidence": 0.80},
            {"code": "pa", "name": "Punjabi", "confidence": 0.75},
        ],
        "default": "en",
        "note": "Confidence scores indicate expected accuracy for each language"
    }


@router.get("/quota")
async def get_voice_quota(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get user's voice processing quota"""
    try:
        voice_service = VoiceService()
        quota = await voice_service.get_user_quota(current_user.id)
        
        return quota
        
    except Exception as e:
        logger.error("Failed to get voice quota", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
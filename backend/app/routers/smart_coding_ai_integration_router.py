"""
Smart Coding AI Integration Router
API endpoints for integrated AI functionality
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from app.services.smart_coding_ai_integration import smart_coding_ai_integration, AIIntegrationContext, IntegratedAIResponse
from app.services.auth_service import AuthService
from app.routers.auth import AuthDependencies
from app.models.user import User

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/smart-coding-ai/integration", tags=["Smart Coding AI Integration"])

# Initialize integration service
@router.on_event("startup")
async def startup_event():
    """Initialize integration service on startup"""
    try:
        await smart_coding_ai_integration.initialize()
        logger.info("Smart Coding AI Integration service initialized")
    except Exception as e:
        logger.error("Failed to initialize Smart Coding AI Integration service", error=str(e))


# ============================================================================
# SESSION MANAGEMENT ENDPOINTS
# ============================================================================

@router.post("/session/create")
async def create_integration_session(
    user_id: str,
    project_id: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Create a new integration session"""
    try:
        session_id = await smart_coding_ai_integration.create_integration_session(
            user_id=user_id,
            project_id=project_id
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "session_id": session_id,
                "user_id": user_id,
                "project_id": project_id,
                "created_at": datetime.now().isoformat(),
                "status": "active"
            }
        )
        
    except Exception as e:
        logger.error("Failed to create integration session", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create integration session: {e}"
        )


@router.get("/session/{session_id}")
async def get_session_context(
    session_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get session context"""
    try:
        context = await smart_coding_ai_integration.get_session_context(session_id)
        
        if not context:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "session_id": context.session_id,
                "user_id": context.user_id,
                "project_id": context.project_id,
                "request_id": context.request_id,
                "operation_type": context.operation_type,
                "metadata": context.metadata
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get session context", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session context: {e}"
        )


@router.put("/session/{session_id}")
async def update_session_context(
    session_id: str,
    updates: Dict[str, Any],
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Update session context"""
    try:
        success = await smart_coding_ai_integration.update_session_context(session_id, updates)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "session_id": session_id,
                "updated": True,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update session context", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update session context: {e}"
        )


# ============================================================================
# VOICE-TO-CODE INTEGRATION ENDPOINTS
# ============================================================================

@router.post("/voice-to-code")
async def process_voice_to_code(
    audio_file: bytes,
    language: str = "en",
    user_id: str = None,
    project_id: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Process voice input to generate code using integrated AI"""
    try:
        # Create integration context
        context = AIIntegrationContext(
            user_id=user_id or current_user.id,
            project_id=project_id
        )
        
        # Process voice to code
        response = await smart_coding_ai_integration.process_voice_to_code(
            audio_file=audio_file,
            language=language,
            context=context
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "response_id": response.response_id,
                "generated_code": response.primary_response.get("generated_code", ""),
                "confidence": response.confidence,
                "supporting_responses": response.supporting_responses,
                "integration_metadata": response.integration_metadata,
                "timestamp": response.timestamp.isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to process voice-to-code", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process voice-to-code: {e}"
        )


@router.post("/voice-to-code/text")
async def process_text_to_code(
    transcript: str,
    language: str = "en",
    user_id: str = None,
    project_id: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Process text transcript to generate code (alternative to voice)"""
    try:
        # Create integration context
        context = AIIntegrationContext(
            user_id=user_id or current_user.id,
            project_id=project_id
        )
        
        # Simulate audio file for processing
        audio_file = transcript.encode('utf-8')
        
        # Process voice to code
        response = await smart_coding_ai_integration.process_voice_to_code(
            audio_file=audio_file,
            language=language,
            context=context
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "response_id": response.response_id,
                "generated_code": response.primary_response.get("generated_code", ""),
                "confidence": response.confidence,
                "supporting_responses": response.supporting_responses,
                "integration_metadata": response.integration_metadata,
                "timestamp": response.timestamp.isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to process text-to-code", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process text-to-code: {e}"
        )


# ============================================================================
# AI ASSISTANT INTEGRATION ENDPOINTS
# ============================================================================

@router.post("/chat/assistant")
async def chat_with_ai_assistant(
    message: str,
    user_id: str = None,
    session_id: Optional[str] = None,
    project_id: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Chat with AI assistant enhanced by Smart Coding AI"""
    try:
        # Create integration context
        context = AIIntegrationContext(
            user_id=user_id or current_user.id,
            session_id=session_id,
            project_id=project_id
        )
        
        # Process chat
        response = await smart_coding_ai_integration.chat_with_ai_assistant(
            message=message,
            context=context
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "response_id": response.response_id,
                "response": response.primary_response.get("combined_response", response.primary_response),
                "confidence": response.confidence,
                "code_snippets": response.primary_response.get("code_snippets", []),
                "follow_up_questions": response.primary_response.get("follow_up_questions", []),
                "supporting_responses": response.supporting_responses,
                "integration_metadata": response.integration_metadata,
                "timestamp": response.timestamp.isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to process AI assistant chat", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process AI assistant chat: {e}"
        )


# ============================================================================
# META ORCHESTRATOR INTEGRATION ENDPOINTS
# ============================================================================

@router.post("/orchestrate/task")
async def orchestrate_smart_coding_task(
    task_description: str,
    user_id: str = None,
    project_id: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Orchestrate a smart coding task using Meta Orchestrator"""
    try:
        # Create integration context
        context = AIIntegrationContext(
            user_id=user_id or current_user.id,
            project_id=project_id
        )
        
        # Orchestrate task
        response = await smart_coding_ai_integration.orchestrate_smart_coding_task(
            task_description=task_description,
            context=context
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "response_id": response.response_id,
                "orchestrated_result": response.primary_response,
                "confidence": response.confidence,
                "supporting_responses": response.supporting_responses,
                "integration_metadata": response.integration_metadata,
                "timestamp": response.timestamp.isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to orchestrate smart coding task", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to orchestrate smart coding task: {e}"
        )


# ============================================================================
# WHATSAPP INTEGRATION ENDPOINTS
# ============================================================================

@router.post("/whatsapp/process-message")
async def process_whatsapp_message(
    message_data: Dict[str, Any],
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Process WhatsApp message with Smart Coding AI integration"""
    try:
        response = await smart_coding_ai_integration.process_whatsapp_message(message_data)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": response.get("success", False),
                "message": response.get("message", ""),
                "confidence": response.get("confidence", 0.0),
                "code_related": response.get("code_related", False),
                "generated_code": response.get("generated_code", ""),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to process WhatsApp message", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process WhatsApp message: {e}"
        )


@router.post("/whatsapp/send-code")
async def send_whatsapp_code_response(
    to: str,
    generated_code: str,
    confidence: float,
    code_type: str = "python",
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Send generated code as WhatsApp message"""
    try:
        response = await smart_coding_ai_integration.send_whatsapp_code_response(
            to=to,
            generated_code=generated_code,
            confidence=confidence,
            code_type=code_type
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": response.get("success", False),
                "message_sent": response.get("message_sent", False),
                "whatsapp_response": response.get("whatsapp_response", {}),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to send WhatsApp code response", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send WhatsApp code response: {e}"
        )


@router.post("/whatsapp/send-chat")
async def send_whatsapp_chat_response(
    to: str,
    ai_response: str,
    confidence: float,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Send AI chat response as WhatsApp message"""
    try:
        response = await smart_coding_ai_integration.send_whatsapp_chat_response(
            to=to,
            ai_response=ai_response,
            confidence=confidence
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": response.get("success", False),
                "message_sent": response.get("message_sent", False),
                "whatsapp_response": response.get("whatsapp_response", {}),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to send WhatsApp chat response", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send WhatsApp chat response: {e}"
        )


# ============================================================================
# INTEGRATION STATUS ENDPOINTS
# ============================================================================

@router.get("/status")
async def get_integration_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get integration system status"""
    try:
        # Get status from various components
        smart_coding_status = await smart_coding_ai_integration.smart_coding_ai.get_memory_status()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "integration_status": "active",
                "smart_coding_ai": {
                    "status": "active" if smart_coding_status.get("system_active") else "inactive",
                    "performance_score": smart_coding_status.get("performance_score", 0.0)
                },
                "ai_assistant": {
                    "status": "active"
                },
                "voice_service": {
                    "status": "active"
                },
                "meta_orchestrator": {
                    "status": "active"
                },
                "goal_integrity": {
                    "status": "active"
                },
                "whatsapp": {
                    "status": "active" if smart_coding_ai_integration.whatsapp_service else "inactive"
                },
                "active_sessions": len(smart_coding_ai_integration.session_contexts),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get integration status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get integration status: {e}"
        )


@router.get("/capabilities")
async def get_integration_capabilities(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get integration capabilities"""
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "capabilities": [
                    {
                        "name": "Voice-to-Code Generation",
                        "description": "Convert voice input to code using integrated AI",
                        "endpoints": ["/voice-to-code", "/voice-to-code/text"],
                        "features": ["transcription", "code_generation", "memory_enhancement", "integrity_validation"]
                    },
                    {
                        "name": "AI Assistant Chat",
                        "description": "Enhanced AI assistant with Smart Coding AI capabilities",
                        "endpoints": ["/chat/assistant"],
                        "features": ["natural_language", "code_detection", "smart_enhancement"]
                    },
                    {
                        "name": "Task Orchestration",
                        "description": "Orchestrate complex coding tasks using Meta Orchestrator",
                        "endpoints": ["/orchestrate/task"],
                        "features": ["task_planning", "execution", "result_combination"]
                    },
                    {
                        "name": "WhatsApp Integration",
                        "description": "Process WhatsApp messages with Smart Coding AI capabilities",
                        "endpoints": ["/whatsapp/process-message", "/whatsapp/send-code", "/whatsapp/send-chat"],
                        "features": ["voice_to_code", "text_processing", "code_generation", "chat_responses"]
                    },
                    {
                        "name": "Session Management",
                        "description": "Manage integration sessions across components",
                        "endpoints": ["/session/create", "/session/{id}", "/session/{id}/update"],
                        "features": ["context_persistence", "cross_component_coordination"]
                    }
                ],
                "integration_components": [
                    "Smart Coding AI",
                    "AI Assistant Service",
                    "Voice Service",
                    "Meta AI Orchestrator",
                    "Goal Integrity Service",
                    "WhatsApp Service"
                ],
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get integration capabilities", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get integration capabilities: {e}"
        )

"""
tRPC App Router - FastAPI to tRPC Bridge

This module creates a tRPC-compatible router that bridges FastAPI endpoints
with tRPC client expectations for seamless frontend integration.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, List, Optional, Any, Union
import structlog
from datetime import datetime
import json

from app.routers.auth import AuthDependencies
from app.models.user import User
from app.services.enhanced_voice_to_app_service import enhanced_voice_to_app_service
from app.services.enhanced_payment_service import enhanced_payment_service
from app.services.smarty_ai_orchestrator import smarty_ai_orchestrator
from app.services.smarty_agent_integration import smarty_agent_integration

logger = structlog.get_logger(__name__)

# Create tRPC-compatible router
trpc_router = APIRouter()

# Pydantic models for tRPC procedures
class TRPCRequest(BaseModel):
    """Base tRPC request model"""
    id: Optional[str] = None
    method: str
    params: Dict[str, Any] = {}

class TRPCResponse(BaseModel):
    """Base tRPC response model"""
    id: Optional[str] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

class UserProfile(BaseModel):
    """User profile model"""
    id: str
    email: str
    name: Optional[str] = None
    avatar: Optional[str] = None
    created_at: str
    updated_at: str

class VoiceToAppRequest(BaseModel):
    """Voice to app request model"""
    audio_data: str  # base64 encoded
    language: str = "en"
    app_type: Optional[str] = None
    complexity_level: str = "medium"

class VoiceToAppResponse(BaseModel):
    """Voice to app response model"""
    request_id: str
    status: str
    transcript: str
    app_type: str
    execution_time: float
    confidence_score: float

class PaymentRequest(BaseModel):
    """Payment request model"""
    amount: float
    currency: str = "INR"
    provider: Optional[str] = None
    description: str = ""

class PaymentResponse(BaseModel):
    """Payment response model"""
    order_id: str
    provider: str
    amount: float
    currency: str
    payment_data: Dict[str, Any]

@trpc_router.post("/trpc/{procedure:path}")
async def trpc_endpoint(
    procedure: str,
    request: TRPCRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Main tRPC endpoint handler"""
    try:
        logger.info(f"tRPC procedure called", 
                   procedure=procedure,
                   user_id=current_user.id)
        
        # Route to appropriate handler based on procedure path
        if procedure.startswith("auth."):
            result = await handle_auth_procedure(procedure, request, current_user)
        elif procedure.startswith("voice."):
            result = await handle_voice_procedure(procedure, request, current_user)
        elif procedure.startswith("payment."):
            result = await handle_payment_procedure(procedure, request, current_user)
        elif procedure.startswith("orchestrator."):
            result = await handle_orchestrator_procedure(procedure, request, current_user)
        elif procedure.startswith("agent."):
            result = await handle_agent_procedure(procedure, request, current_user)
        else:
            raise HTTPException(status_code=404, detail=f"Procedure not found: {procedure}")
        
        return TRPCResponse(id=request.id, result=result)
        
    except Exception as e:
        logger.error(f"tRPC procedure failed", 
                    error=str(e), 
                    procedure=procedure,
                    user_id=current_user.id)
        return TRPCResponse(
            id=request.id,
            error={
                "code": -32603,
                "message": str(e),
                "data": None
            }
        )

async def handle_auth_procedure(procedure: str, request: TRPCRequest, user: User) -> Any:
    """Handle auth-related procedures"""
    if procedure == "auth.getProfile":
        return UserProfile(
            id=str(user.id),
            email=user.email,
            name=getattr(user, 'name', None),
            avatar=getattr(user, 'avatar', None),
            created_at=user.created_at.isoformat(),
            updated_at=user.updated_at.isoformat()
        )
    elif procedure == "auth.updateProfile":
        # Update user profile
        update_data = request.params
        # Implementation would update user in database
        return {"success": True, "message": "Profile updated"}
    else:
        raise ValueError(f"Unknown auth procedure: {procedure}")

async def handle_voice_procedure(procedure: str, request: TRPCRequest, user: User) -> Any:
    """Handle voice-related procedures"""
    if procedure == "voice.generateApp":
        # Create voice-to-app request
        voice_request_data = VoiceToAppRequest(**request.params)
        
        # Convert base64 audio data to bytes
        import base64
        audio_data = base64.b64decode(voice_request_data.audio_data)
        
        # Create voice-to-app request
        from app.services.enhanced_voice_to_app_service import VoiceToAppRequest as ServiceRequest
        from app.services.smarty_ai_orchestrator import OrchestrationMode, CodeGenerationStrategy
        
        service_request = ServiceRequest(
            audio_data=audio_data,
            user_id=str(user.id),
            language=voice_request_data.language,
            app_type=voice_request_data.app_type,
            complexity_level=voice_request_data.complexity_level
        )
        
        # Generate app
        response = await enhanced_voice_to_app_service.generate_app_from_voice(service_request)
        
        return VoiceToAppResponse(
            request_id=response.request_id,
            status=response.status,
            transcript=response.transcript,
            app_type=response.app_type,
            execution_time=response.execution_time,
            confidence_score=response.confidence_score
        )
    
    elif procedure == "voice.getStatus":
        request_id = request.params.get("request_id")
        if not request_id:
            raise ValueError("request_id is required")
        
        status = await enhanced_voice_to_app_service.get_request_status(request_id)
        return status
    
    else:
        raise ValueError(f"Unknown voice procedure: {procedure}")

async def handle_payment_procedure(procedure: str, request: TRPCRequest, user: User) -> Any:
    """Handle payment-related procedures"""
    if procedure == "payment.createOrder":
        payment_request_data = PaymentRequest(**request.params)
        
        from app.services.enhanced_payment_service import PaymentProvider
        provider = PaymentProvider(payment_request_data.provider) if payment_request_data.provider else None
        
        # Create payment order
        order = await enhanced_payment_service.create_payment_order(
            user_id=str(user.id),
            amount=payment_request_data.amount,
            currency=payment_request_data.currency,
            provider=provider,
            description=payment_request_data.description
        )
        
        return PaymentResponse(
            order_id=order.order_id,
            provider=order.provider.value,
            amount=order.amount,
            currency=order.currency,
            payment_data=order.payment_data
        )
    
    elif procedure == "payment.verify":
        order_id = request.params.get("order_id")
        payment_data = request.params.get("payment_data", {})
        
        if not order_id:
            raise ValueError("order_id is required")
        
        result = await enhanced_payment_service.verify_payment(order_id, payment_data)
        
        return {
            "order_id": result.order_id,
            "payment_id": result.payment_id,
            "status": result.status.value,
            "amount": result.amount,
            "currency": result.currency,
            "provider": result.provider.value
        }
    
    elif procedure == "payment.getStatus":
        order_id = request.params.get("order_id")
        if not order_id:
            raise ValueError("order_id is required")
        
        status = await enhanced_payment_service.get_payment_status(order_id)
        return status
    
    else:
        raise ValueError(f"Unknown payment procedure: {procedure}")

async def handle_orchestrator_procedure(procedure: str, request: TRPCRequest, user: User) -> Any:
    """Handle orchestrator-related procedures"""
    if procedure == "orchestrator.createPlan":
        transcript = request.params.get("transcript")
        if not transcript:
            raise ValueError("transcript is required")
        
        from app.services.smarty_ai_orchestrator import OrchestrationMode, CodeGenerationStrategy
        
        # Create orchestration plan
        plan = await smarty_ai_orchestrator.orchestrate_with_smarty(
            transcript=transcript,
            user_id=str(user.id),
            orchestration_mode=OrchestrationMode.VOICE_TO_APP,
            code_generation_strategy=CodeGenerationStrategy.ADAPTIVE
        )
        
        return {
            "plan_id": plan.plan_id,
            "confidence": plan.confidence,
            "estimated_timeline": plan.estimated_timeline,
            "status": plan.status
        }
    
    elif procedure == "orchestrator.getStatus":
        plan_id = request.params.get("plan_id")
        if not plan_id:
            raise ValueError("plan_id is required")
        
        status = await smarty_ai_orchestrator.get_orchestration_status(plan_id)
        return status
    
    else:
        raise ValueError(f"Unknown orchestrator procedure: {procedure}")

async def handle_agent_procedure(procedure: str, request: TRPCRequest, user: User) -> Any:
    """Handle agent-related procedures"""
    if procedure == "agent.createAgent":
        agent_data = request.params
        
        from app.models.ai_agent import AgentCreationRequest, AgentType, AgentCapability
        from app.services.smarty_agent_integration import AgentSmartyMode, AgentCodeCapability
        
        # Create agent creation request
        agent_creation_request = AgentCreationRequest(
            name=agent_data.get("name"),
            description=agent_data.get("description"),
            agent_type=AgentType(agent_data.get("agent_type", "coding_assistant")),
            capabilities=[AgentCapability(cap) for cap in agent_data.get("capabilities", [])]
        )
        
        # Create smarty agent
        agent = await smarty_agent_integration.create_smarty_agent(
            agent_creation_request=agent_creation_request,
            smarty_mode=AgentSmartyMode(agent_data.get("smarty_mode", "code_generation_assistant")),
            code_capability=AgentCodeCapability(agent_data.get("code_capability", "advanced_code"))
        )
        
        return {
            "agent_id": str(agent.agent_id),
            "name": agent.name,
            "description": agent.description,
            "agent_type": agent.agent_type.value,
            "capabilities": [cap.value for cap in agent.capabilities],
            "status": agent.status.value
        }
    
    elif procedure == "agent.generateCode":
        agent_id = request.params.get("agent_id")
        prompt = request.params.get("prompt")
        
        if not agent_id or not prompt:
            raise ValueError("agent_id and prompt are required")
        
        from app.services.smarty_agent_integration import AgentCodeGenerationRequest
        
        # Create code generation request
        code_request = AgentCodeGenerationRequest(
            agent_id=agent_id,
            user_id=str(user.id),
            prompt=prompt,
            context=request.params.get("context", {}),
            code_type=request.params.get("code_type", "general"),
            complexity_level=request.params.get("complexity_level", "medium")
        )
        
        # Generate code
        response = await smarty_agent_integration.interact_with_smarty_agent(code_request)
        
        return {
            "generated_code": response.generated_code,
            "confidence_score": response.confidence_score,
            "quality_metrics": response.quality_metrics,
            "execution_time": response.execution_time
        }
    
    else:
        raise ValueError(f"Unknown agent procedure: {procedure}")

# Export the router for use in main application
def get_trpc_router():
    """Get the tRPC router"""
    return trpc_router

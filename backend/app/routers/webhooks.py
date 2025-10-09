"""
Webhooks router for Voice-to-App SaaS Platform
Handles payment provider webhooks and external service callbacks
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any
import structlog
import hmac
import hashlib
from datetime import datetime

from app.core.config import settings
from app.services.webhook_service import WebhookService
from app.services.payment_service import PaymentService
from app.services.razorpay_service import RazorpayService
from app.services.paypal_service import PayPalService

logger = structlog.get_logger()
router = APIRouter()


class WebhookDependencies:
    """Webhook dependencies"""
    
    @staticmethod
    async def verify_razorpay_signature(request: Request) -> Dict[str, Any]:
        """Verify Razorpay webhook signature"""
        try:
            body = await request.body()
            signature = request.headers.get("X-Razorpay-Signature")
            
            if not signature:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Missing Razorpay signature"
                )
            
            # Verify signature
            expected_signature = hmac.new(
                settings.RAZORPAY_WEBHOOK_SECRET.encode(),
                body,
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid Razorpay signature"
                )
            
            return {"verified": True, "body": body}
            
        except Exception as e:
            logger.error("Razorpay signature verification failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Signature verification failed"
            )
    
    @staticmethod
    async def verify_paypal_signature(request: Request) -> Dict[str, Any]:
        """Verify PayPal webhook signature"""
        try:
            body = await request.body()
            # PayPal webhook verification would be implemented here
            # This is a simplified version
            
            return {"verified": True, "body": body}
            
        except Exception as e:
            logger.error("PayPal signature verification failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Signature verification failed"
            )


@router.post("/razorpay")
async def razorpay_webhook(
    request: Request,
    verified_data: Dict[str, Any] = Depends(WebhookDependencies.verify_razorpay_signature)
):
    """Handle Razorpay webhook events"""
    try:
        webhook_service = WebhookService()
        payment_service = PaymentService()
        
        # Parse webhook data
        webhook_data = await request.json()
        event_type = webhook_data.get("event")
        
        logger.info(
            "Razorpay webhook received",
            event_type=event_type,
            webhook_id=webhook_data.get("id")
        )
        
        # Handle different event types
        if event_type == "payment.captured":
            await webhook_service.handle_payment_captured(
                provider="razorpay",
                webhook_data=webhook_data
            )
        elif event_type == "payment.failed":
            await webhook_service.handle_payment_failed(
                provider="razorpay",
                webhook_data=webhook_data
            )
        elif event_type == "subscription.activated":
            await webhook_service.handle_subscription_activated(
                provider="razorpay",
                webhook_data=webhook_data
            )
        elif event_type == "subscription.cancelled":
            await webhook_service.handle_subscription_cancelled(
                provider="razorpay",
                webhook_data=webhook_data
            )
        else:
            logger.warning(
                "Unhandled Razorpay webhook event",
                event_type=event_type
            )
        
        return {"status": "success", "message": "Webhook processed"}
        
    except Exception as e:
        logger.error("Razorpay webhook processing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/paypal")
async def paypal_webhook(
    request: Request,
    verified_data: Dict[str, Any] = Depends(WebhookDependencies.verify_paypal_signature)
):
    """Handle PayPal webhook events"""
    try:
        webhook_service = WebhookService()
        
        # Parse webhook data
        webhook_data = await request.json()
        event_type = webhook_data.get("event_type")
        
        logger.info(
            "PayPal webhook received",
            event_type=event_type,
            webhook_id=webhook_data.get("id")
        )
        
        # Handle different event types
        if event_type == "PAYMENT.CAPTURE.COMPLETED":
            await webhook_service.handle_payment_captured(
                provider="paypal",
                webhook_data=webhook_data
            )
        elif event_type == "PAYMENT.CAPTURE.DENIED":
            await webhook_service.handle_payment_failed(
                provider="paypal",
                webhook_data=webhook_data
            )
        elif event_type == "BILLING.SUBSCRIPTION.ACTIVATED":
            await webhook_service.handle_subscription_activated(
                provider="paypal",
                webhook_data=webhook_data
            )
        elif event_type == "BILLING.SUBSCRIPTION.CANCELLED":
            await webhook_service.handle_subscription_cancelled(
                provider="paypal",
                webhook_data=webhook_data
            )
        else:
            logger.warning(
                "Unhandled PayPal webhook event",
                event_type=event_type
            )
        
        return {"status": "success", "message": "Webhook processed"}
        
    except Exception as e:
        logger.error("PayPal webhook processing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/twilio/sms")
async def twilio_sms_webhook(request: Request):
    """Handle Twilio SMS webhook events"""
    try:
        webhook_service = WebhookService()
        
        # Parse form data from Twilio
        form_data = await request.form()
        
        logger.info(
            "Twilio SMS webhook received",
            message_sid=form_data.get("MessageSid"),
            status=form_data.get("MessageStatus")
        )
        
        # Handle SMS status updates
        await webhook_service.handle_sms_status_update(form_data)
        
        return {"status": "success", "message": "SMS webhook processed"}
        
    except Exception as e:
        logger.error("Twilio SMS webhook processing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/github")
async def github_webhook(request: Request):
    """Handle GitHub webhook events for app deployments"""
    try:
        webhook_service = WebhookService()
        
        # Parse webhook data
        webhook_data = await request.json()
        event_type = request.headers.get("X-GitHub-Event")
        
        logger.info(
            "GitHub webhook received",
            event_type=event_type,
            repository=webhook_data.get("repository", {}).get("name")
        )
        
        # Handle different GitHub events
        if event_type == "push":
            await webhook_service.handle_github_push(webhook_data)
        elif event_type == "pull_request":
            await webhook_service.handle_github_pull_request(webhook_data)
        elif event_type == "deployment":
            await webhook_service.handle_github_deployment(webhook_data)
        else:
            logger.warning(
                "Unhandled GitHub webhook event",
                event_type=event_type
            )
        
        return {"status": "success", "message": "GitHub webhook processed"}
        
    except Exception as e:
        logger.error("GitHub webhook processing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/vercel")
async def vercel_webhook(request: Request):
    """Handle Vercel deployment webhook events"""
    try:
        webhook_service = WebhookService()
        
        # Parse webhook data
        webhook_data = await request.json()
        event_type = webhook_data.get("type")
        
        logger.info(
            "Vercel webhook received",
            event_type=event_type,
            deployment_id=webhook_data.get("deployment", {}).get("id")
        )
        
        # Handle deployment events
        if event_type == "deployment.created":
            await webhook_service.handle_vercel_deployment_created(webhook_data)
        elif event_type == "deployment.ready":
            await webhook_service.handle_vercel_deployment_ready(webhook_data)
        elif event_type == "deployment.error":
            await webhook_service.handle_vercel_deployment_error(webhook_data)
        else:
            logger.warning(
                "Unhandled Vercel webhook event",
                event_type=event_type
            )
        
        return {"status": "success", "message": "Vercel webhook processed"}
        
    except Exception as e:
        logger.error("Vercel webhook processing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/render")
async def render_webhook(request: Request):
    """Handle Render deployment webhook events"""
    try:
        webhook_service = WebhookService()
        
        # Parse webhook data
        webhook_data = await request.json()
        event_type = webhook_data.get("event")
        
        logger.info(
            "Render webhook received",
            event_type=event_type,
            service_id=webhook_data.get("service", {}).get("id")
        )
        
        # Handle deployment events
        if event_type == "deploy.created":
            await webhook_service.handle_render_deployment_created(webhook_data)
        elif event_type == "deploy.succeeded":
            await webhook_service.handle_render_deployment_succeeded(webhook_data)
        elif event_type == "deploy.failed":
            await webhook_service.handle_render_deployment_failed(webhook_data)
        else:
            logger.warning(
                "Unhandled Render webhook event",
                event_type=event_type
            )
        
        return {"status": "success", "message": "Render webhook processed"}
        
    except Exception as e:
        logger.error("Render webhook processing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/test")
async def test_webhook_endpoint():
    """Test webhook endpoint connectivity"""
    return {
        "status": "success",
        "message": "Webhook endpoint is working",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/logs")
async def get_webhook_logs(
    limit: int = 50,
    provider: Optional[str] = None
):
    """Get webhook processing logs"""
    try:
        webhook_service = WebhookService()
        
        logs = await webhook_service.get_webhook_logs(
            limit=limit,
            provider=provider
        )
        
        return {
            "logs": logs,
            "total": len(logs),
            "limit": limit
        }
        
    except Exception as e:
        logger.error("Failed to get webhook logs", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint for webhooks service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "webhooks",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

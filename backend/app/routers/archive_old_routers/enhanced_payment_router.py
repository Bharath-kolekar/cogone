"""
Enhanced Payment Router with Multi-Provider Integration

API endpoints for the enhanced payment service with Razorpay, PayPal, Google Pay, UPI, and QR code support.
"""

from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum
import structlog
from datetime import datetime

from app.core.config import settings

from app.services.enhanced_payment_service import (
    enhanced_payment_service,
    PaymentProvider,
    PaymentStatus,
    PaymentMethod,
    SubscriptionPlan
)
from app.routers.auth import AuthDependencies
from app.models.user import User

logger = structlog.get_logger(__name__)

router = APIRouter()

class PaymentCreateRequest(BaseModel):
    """Request model for payment creation"""
    amount: float = Field(..., description="Payment amount", gt=0)
    currency: str = Field(default="INR", description="Payment currency")
    provider: Optional[PaymentProvider] = Field(None, description="Preferred payment provider")
    description: str = Field(default="", description="Payment description")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class PaymentCreateResponse(BaseModel):
    """Response model for payment creation"""
    order_id: str
    provider: str
    amount: float
    currency: str
    payment_data: Dict[str, Any]
    qr_code_url: Optional[str] = None
    upi_intent_url: Optional[str] = None
    expires_at: str

class PaymentVerifyRequest(BaseModel):
    """Request model for payment verification"""
    order_id: str = Field(..., description="Order ID to verify")
    payment_data: Dict[str, Any] = Field(..., description="Payment verification data")

class PaymentVerifyResponse(BaseModel):
    """Response model for payment verification"""
    order_id: str
    payment_id: Optional[str]
    status: str
    amount: float
    currency: str
    provider: str
    transaction_data: Dict[str, Any]
    processed_at: str

class PaymentStatusResponse(BaseModel):
    """Response model for payment status"""
    order_id: str
    status: str
    amount: float
    currency: str
    provider: str
    created_at: str
    expires_at: Optional[str] = None
    payment_id: Optional[str] = None
    processed_at: Optional[str] = None

class SubscriptionCreateRequest(BaseModel):
    """Request model for subscription creation"""
    plan: SubscriptionPlan = Field(..., description="Subscription plan")
    provider: Optional[PaymentProvider] = Field(None, description="Preferred payment provider")
    billing_cycle: str = Field(default="monthly", description="Billing cycle: monthly, yearly")

class SubscriptionCreateResponse(BaseModel):
    """Response model for subscription creation"""
    subscription_id: str
    plan: str
    amount: float
    currency: str
    billing_cycle: str
    payment_data: Dict[str, Any]
    status: str

class PaymentMetricsResponse(BaseModel):
    """Response model for payment metrics"""
    service_metrics: Dict[str, Any]
    active_orders_count: int
    completed_payments_count: int
    total_success_rate: float

@router.post("/create-order", response_model=PaymentCreateResponse)
async def create_payment_order(
    request: PaymentCreateRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Create a new payment order"""
    try:
        logger.info(f"Creating payment order", 
                   user_id=current_user.id,
                   amount=request.amount,
                   currency=request.currency,
                   provider=request.provider.value if request.provider else None)
        
        # Create payment order
        order = await enhanced_payment_service.create_payment_order(
            user_id=str(current_user.id),
            amount=request.amount,
            currency=request.currency,
            provider=request.provider,
            description=request.description,
            metadata=request.metadata
        )
        
        # Extract response data
        response_data = {
            "order_id": order.order_id,
            "provider": order.provider.value,
            "amount": order.amount,
            "currency": order.currency,
            "payment_data": order.payment_data,
            "expires_at": order.expires_at.isoformat()
        }
        
        # Add provider-specific URLs
        if order.provider == PaymentProvider.UPI:
            response_data["upi_intent_url"] = order.payment_data.get("upi_url")
        elif order.provider == PaymentProvider.QR_CODE:
            response_data["qr_code_url"] = f"{settings.BASE_URL}/payment/qr/{order.order_id}"
        
        return PaymentCreateResponse(**response_data)
        
    except Exception as e:
        logger.error(f"Payment order creation failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Payment order creation failed: {str(e)}")

@router.post("/verify", response_model=PaymentVerifyResponse)
async def verify_payment(
    request: PaymentVerifyRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Verify a payment"""
    try:
        logger.info(f"Verifying payment", 
                   order_id=request.order_id,
                   user_id=current_user.id)
        
        # Verify payment
        result = await enhanced_payment_service.verify_payment(
            order_id=request.order_id,
            payment_data=request.payment_data
        )
        
        return PaymentVerifyResponse(
            order_id=result.order_id,
            payment_id=result.payment_id,
            status=result.status.value,
            amount=result.amount,
            currency=result.currency,
            provider=result.provider.value,
            transaction_data=result.transaction_data,
            processed_at=result.processed_at.isoformat()
        )
        
    except Exception as e:
        logger.error(f"Payment verification failed", 
                    error=str(e), 
                    order_id=request.order_id)
        raise HTTPException(status_code=500, detail=f"Payment verification failed: {str(e)}")

@router.get("/status/{order_id}", response_model=PaymentStatusResponse)
async def get_payment_status(
    order_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get payment status"""
    try:
        status = await enhanced_payment_service.get_payment_status(order_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Payment order not found")
        
        # Check if user owns this payment
        # In a real implementation, you would verify ownership from the database
        
        return PaymentStatusResponse(
            order_id=status["order_id"],
            status=status["status"],
            amount=status["amount"],
            currency=status["currency"],
            provider=status["provider"],
            created_at=status["created_at"],
            expires_at=status.get("expires_at"),
            payment_id=status.get("payment_id"),
            processed_at=status.get("processed_at")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Payment status retrieval failed", 
                    error=str(e), 
                    order_id=order_id)
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.post("/subscription/create", response_model=SubscriptionCreateResponse)
async def create_subscription(
    request: SubscriptionCreateRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Create a subscription"""
    try:
        logger.info(f"Creating subscription", 
                   user_id=current_user.id,
                   plan=request.plan.value,
                   billing_cycle=request.billing_cycle)
        
        # Define subscription plans
        subscription_plans = {
            SubscriptionPlan.FREE: {"amount": 0.0, "features": ["basic_features"]},
            SubscriptionPlan.BASIC: {"amount": 999.0, "features": ["basic_features", "premium_support"]},
            SubscriptionPlan.PRO: {"amount": 2999.0, "features": ["all_features", "priority_support", "api_access"]},
            SubscriptionPlan.ENTERPRISE: {"amount": 9999.0, "features": ["all_features", "dedicated_support", "custom_integrations"]}
        }
        
        plan_config = subscription_plans[request.plan]
        
        # Calculate amount based on billing cycle
        amount = plan_config["amount"]
        if request.billing_cycle == "yearly":
            amount = amount * 10  # 10 months for yearly (2 months free)
        
        # Create payment order for subscription
        order = await enhanced_payment_service.create_payment_order(
            user_id=str(current_user.id),
            amount=amount,
            currency="INR",
            provider=request.provider,
            description=f"{request.plan.value.title()} subscription - {request.billing_cycle}",
            metadata={
                "subscription_plan": request.plan.value,
                "billing_cycle": request.billing_cycle,
                "features": plan_config["features"]
            }
        )
        
        return SubscriptionCreateResponse(
            subscription_id=order.order_id,
            plan=request.plan.value,
            amount=amount,
            currency="INR",
            billing_cycle=request.billing_cycle,
            payment_data=order.payment_data,
            status=order.status.value
        )
        
    except Exception as e:
        logger.error(f"Subscription creation failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Subscription creation failed: {str(e)}")

@router.get("/providers")
async def get_payment_providers():
    """Get available payment providers"""
    return {
        "providers": [
            {
                "provider": PaymentProvider.RAZORPAY.value,
                "name": "Razorpay",
                "description": "Payment gateway for Indian businesses",
                "supported_methods": ["card", "upi", "net_banking", "wallet", "emi"],
                "supported_currencies": ["INR"],
                "min_amount": 1.0,
                "max_amount": 1000000.0
            },
            {
                "provider": PaymentProvider.PAYPAL.value,
                "name": "PayPal",
                "description": "Global payment platform",
                "supported_methods": ["card", "paypal_balance"],
                "supported_currencies": ["USD", "EUR", "GBP", "INR"],
                "min_amount": 1.0,
                "max_amount": 1000000.0
            },
            {
                "provider": PaymentProvider.GOOGLE_PAY.value,
                "name": "Google Pay",
                "description": "Google's payment platform",
                "supported_methods": ["card", "upi", "wallet"],
                "supported_currencies": ["INR", "USD"],
                "min_amount": 1.0,
                "max_amount": 100000.0
            },
            {
                "provider": PaymentProvider.UPI.value,
                "name": "UPI",
                "description": "Unified Payments Interface",
                "supported_methods": ["upi"],
                "supported_currencies": ["INR"],
                "min_amount": 1.0,
                "max_amount": 100000.0
            },
            {
                "provider": PaymentProvider.QR_CODE.value,
                "name": "QR Code",
                "description": "QR code payment",
                "supported_methods": ["qr_code"],
                "supported_currencies": ["INR"],
                "min_amount": 1.0,
                "max_amount": 100000.0
            }
        ]
    }

@router.get("/subscription-plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    return {
        "plans": [
            {
                "plan": SubscriptionPlan.FREE.value,
                "name": "Free",
                "amount": 0.0,
                "billing_cycle": "monthly",
                "features": ["basic_features"],
                "description": "Basic features for getting started"
            },
            {
                "plan": SubscriptionPlan.BASIC.value,
                "name": "Basic",
                "amount": 999.0,
                "billing_cycle": "monthly",
                "features": ["basic_features", "premium_support"],
                "description": "Enhanced features with premium support"
            },
            {
                "plan": SubscriptionPlan.PRO.value,
                "name": "Pro",
                "amount": 2999.0,
                "billing_cycle": "monthly",
                "features": ["all_features", "priority_support", "api_access"],
                "description": "All features with priority support and API access"
            },
            {
                "plan": SubscriptionPlan.ENTERPRISE.value,
                "name": "Enterprise",
                "amount": 9999.0,
                "billing_cycle": "monthly",
                "features": ["all_features", "dedicated_support", "custom_integrations"],
                "description": "Enterprise features with dedicated support"
            }
        ],
        "billing_cycles": [
            {
                "cycle": "monthly",
                "name": "Monthly",
                "discount": 0.0
            },
            {
                "cycle": "yearly",
                "name": "Yearly",
                "discount": 16.67  # 2 months free
            }
        ]
    }

@router.get("/user-payments")
async def get_user_payments(
    current_user: User = Depends(AuthDependencies.get_current_user),
    limit: int = 10,
    offset: int = 0
):
    """Get user's payment history"""
    try:
        # In a real implementation, this would query the database
        # For now, return a mock response
        user_payments = []
        
        # Get completed payments for user
        for order_id, result in enhanced_payment_service.completed_payments.items():
            if result.amount > 0:  # Mock user check
                user_payments.append({
                    "order_id": result.order_id,
                    "payment_id": result.payment_id,
                    "status": result.status.value,
                    "amount": result.amount,
                    "currency": result.currency,
                    "provider": result.provider.value,
                    "processed_at": result.processed_at.isoformat(),
                    "transaction_data": result.transaction_data
                })
        
        # Sort by processed_at descending
        user_payments.sort(key=lambda x: x["processed_at"], reverse=True)
        
        # Apply pagination
        total_count = len(user_payments)
        paginated_payments = user_payments[offset:offset + limit]
        
        return {
            "payments": paginated_payments,
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total_count
        }
        
    except Exception as e:
        logger.error(f"User payments retrieval failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Payments retrieval failed: {str(e)}")

@router.get("/metrics", response_model=PaymentMetricsResponse)
async def get_payment_metrics(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get payment service metrics (admin only)"""
    try:
        # Check if user is admin (simple check for now)
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")
        
        metrics = await enhanced_payment_service.get_service_metrics()
        
        return PaymentMetricsResponse(
            service_metrics=metrics.get("service_metrics", {}),
            active_orders_count=metrics.get("active_orders_count", 0),
            completed_payments_count=metrics.get("completed_payments_count", 0),
            total_success_rate=metrics.get("total_success_rate", 0.0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Payment metrics retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@router.post("/webhook/razorpay")
async def razorpay_webhook(request: Request):
    """Handle Razorpay webhook"""
    try:
        body = await request.body()
        headers = dict(request.headers)
        
        # Verify webhook signature
        razorpay_signature = headers.get("x-razorpay-signature")
        if not razorpay_signature:
            raise HTTPException(status_code=400, detail="Missing signature")
        
        # Verify signature (simplified for demo)
        # In production, use proper signature verification
        
        webhook_data = await request.json()
        
        logger.info(f"Razorpay webhook received", 
                   event=webhook_data.get("event"),
                   order_id=webhook_data.get("payload", {}).get("payment", {}).get("entity", {}).get("order_id"))
        
        # Process webhook event
        if webhook_data.get("event") == "payment.captured":
            # Payment was captured successfully
            payment_data = webhook_data.get("payload", {}).get("payment", {}).get("entity", {})
            order_id = payment_data.get("order_id")
            
            if order_id:
                # Update payment status
                await enhanced_payment_service.verify_payment(
                    order_id=order_id,
                    payment_data=payment_data
                )
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Razorpay webhook processing failed", error=str(e))
        raise HTTPException(status_code=500, detail="Webhook processing failed")

@router.post("/webhook/paypal")
async def paypal_webhook(request: Request):
    """Handle PayPal webhook"""
    try:
        webhook_data = await request.json()
        
        logger.info(f"PayPal webhook received", 
                   event_type=webhook_data.get("event_type"))
        
        # Process webhook event
        if webhook_data.get("event_type") == "PAYMENT.CAPTURE.COMPLETED":
            # Payment was captured successfully
            resource = webhook_data.get("resource", {})
            order_id = resource.get("custom_id")
            
            if order_id:
                # Update payment status
                await enhanced_payment_service.verify_payment(
                    order_id=order_id,
                    payment_data=resource
                )
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"PayPal webhook processing failed", error=str(e))
        raise HTTPException(status_code=500, detail="Webhook processing failed")

@router.get("/health")
async def health_check():
    """Health check endpoint for payment service"""
    try:
        metrics = await enhanced_payment_service.get_service_metrics()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service_status": "operational",
            "active_orders": metrics.get("active_orders_count", 0),
            "total_orders": metrics.get("service_metrics", {}).get("total_orders", 0),
            "success_rate": metrics.get("total_success_rate", 0.0)
        }
        
    except Exception as e:
        logger.error(f"Payment service health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

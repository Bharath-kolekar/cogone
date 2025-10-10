"""
Payments router for Voice-to-App SaaS Platform
Handles Razorpay, PayPal, Google Pay, UPI, and QR code payments
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import structlog
from datetime import datetime

from app.core.config import settings
from app.services.payment_service import PaymentService
from app.services.razorpay_service import RazorpayService
from app.services.paypal_service import PayPalService
from app.services.upi_service import UPIService
from app.routers.auth import AuthDependencies
from app.models.user import User
from app.models.payment import (
    PaymentCreateRequest,
    PaymentCreateResponse,
    PaymentVerifyRequest,
    PaymentVerifyResponse,
    SubscriptionCreateRequest,
    SubscriptionCreateResponse,
    UPIQRRequest,
    UPIQRResponse,
)

logger = structlog.get_logger()
router = APIRouter()


class PaymentDependencies:
    """Payment processing dependencies"""
    
    @staticmethod
    async def check_payment_quota(
        current_user: User = Depends(AuthDependencies.get_current_user)
    ) -> User:
        """
        Check if user can make payments
        
        🧬 REAL IMPLEMENTATION: Validates subscription and payment status
        """
        try:
            from app.core.database import get_supabase_client
            from fastapi import HTTPException
            
            db = get_supabase_client()
            
            if db:
                # Check user's payment status
                result = db.table('user_payment_status').select('*').eq('user_id', str(current_user.id)).execute()
                
                if result.data and len(result.data) > 0:
                    status_data = result.data[0]
                    is_blocked = status_data.get('is_blocked', False)
                    has_failed_payments = status_data.get('failed_payment_count', 0) > 3
                    
                    if is_blocked:
                        raise HTTPException(
                            status_code=403,
                            detail="Payment capability is blocked. Please contact support."
                        )
                    
                    if has_failed_payments:
                        raise HTTPException(
                            status_code=402,
                            detail="Multiple failed payments detected. Please update payment method."
                        )
            
            return current_user
            
        except HTTPException:
            raise
        except Exception as e:
            # Log error but don't block user (fail open for payments)
            logger.warning(f"Payment eligibility check failed, allowing request: {e}")
            return current_user


@router.post("/create-order", response_model=PaymentCreateResponse)
async def create_payment_order(
    request: PaymentCreateRequest,
    current_user: User = Depends(PaymentDependencies.check_payment_quota)
):
    """Create payment order with selected provider"""
    try:
        payment_service = PaymentService()
        
        # Select best payment provider based on amount, currency, user preference
        provider = payment_service.select_payment_provider(
            amount=request.amount,
            currency=request.currency,
            user_preference=request.preferred_provider,
            user_country=current_user.country_code
        )
        
        # Create payment order
        order_result = await payment_service.create_payment_order(
            user_id=current_user.id,
            amount=request.amount,
            currency=request.currency,
            provider=provider,
            description=request.description,
            metadata=request.metadata
        )
        
        logger.info(
            "Payment order created",
            user_id=current_user.id,
            provider=provider,
            amount=request.amount,
            order_id=order_result.order_id
        )
        
        return PaymentCreateResponse(
            order_id=order_result.order_id,
            provider=provider,
            amount=request.amount,
            currency=request.currency,
            payment_data=order_result.payment_data,
            qr_code_url=order_result.qr_code_url,
            upi_intent_url=order_result.upi_intent_url,
            expires_at=order_result.expires_at
        )
        
    except Exception as e:
        logger.error("Payment order creation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/verify", response_model=PaymentVerifyResponse)
async def verify_payment(
    request: PaymentVerifyRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Verify payment completion"""
    try:
        payment_service = PaymentService()
        
        # Verify payment with provider
        verification_result = await payment_service.verify_payment(
            order_id=request.order_id,
            payment_id=request.payment_id,
            provider=request.provider,
            signature=request.signature
        )
        
        if verification_result.success:
            # Award points for successful payment
            if settings.ENABLE_GAMIFICATION:
                from app.services.gamification_service import GamificationService
                gamification_service = GamificationService()
                await gamification_service.award_points(
                    user_id=current_user.id,
                    points=settings.POINTS_PER_APP_CREATED,
                    reason="payment_completed",
                    metadata={"amount": request.amount, "provider": request.provider}
                )
        
        logger.info(
            "Payment verification completed",
            user_id=current_user.id,
            order_id=request.order_id,
            success=verification_result.success
        )
        
        return PaymentVerifyResponse(
            success=verification_result.success,
            payment_id=verification_result.payment_id,
            amount=verification_result.amount,
            currency=verification_result.currency,
            status=verification_result.status,
            message=verification_result.message
        )
        
    except Exception as e:
        logger.error("Payment verification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/subscription/create", response_model=SubscriptionCreateResponse)
async def create_subscription(
    request: SubscriptionCreateRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Create subscription for recurring payments"""
    try:
        payment_service = PaymentService()
        
        # Create subscription
        subscription_result = await payment_service.create_subscription(
            user_id=current_user.id,
            plan_id=request.plan_id,
            provider=request.provider,
            billing_cycle=request.billing_cycle
        )
        
        logger.info(
            "Subscription created",
            user_id=current_user.id,
            plan_id=request.plan_id,
            provider=request.provider
        )
        
        return SubscriptionCreateResponse(
            subscription_id=subscription_result.subscription_id,
            provider=request.provider,
            plan_id=request.plan_id,
            status=subscription_result.status,
            payment_data=subscription_result.payment_data,
            next_billing_date=subscription_result.next_billing_date
        )
        
    except Exception as e:
        logger.error("Subscription creation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/upi/qr", response_model=UPIQRResponse)
async def generate_upi_qr(
    request: UPIQRRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Generate UPI QR code for payment"""
    try:
        upi_service = UPIService()
        
        # Generate UPI QR code
        qr_result = await upi_service.generate_qr_code(
            amount=request.amount,
            description=request.description,
            merchant_id=settings.GOOGLE_PAY_MERCHANT_ID,
            user_id=current_user.id
        )
        
        logger.info(
            "UPI QR code generated",
            user_id=current_user.id,
            amount=request.amount
        )
        
        return UPIQRResponse(
            qr_code_url=qr_result.qr_code_url,
            upi_id=qr_result.upi_id,
            amount=request.amount,
            expires_at=qr_result.expires_at
        )
        
    except Exception as e:
        logger.error("UPI QR generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/methods")
async def get_payment_methods(
    current_user: User = Depends(AuthDependencies.get_current_user),
    currency: str = 'INR'
):
    """Get available payment methods for user's country"""
    try:
        payment_service = PaymentService()
        methods = await payment_service.get_available_payment_methods(
            country_code=current_user.country_code,
            currency=currency
        )
        
        return {
            "methods": methods,
            "country": current_user.country_code,
            "currency": currency
        }
        
    except Exception as e:
        logger.error("Failed to get payment methods", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/history")
async def get_payment_history(
    limit: int = 10,
    offset: int = 0,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get user's payment history"""
    try:
        payment_service = PaymentService()
        history = await payment_service.get_payment_history(
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )
        
        return {
            "payments": history,
            "total": len(history),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error("Failed to get payment history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/subscriptions")
async def get_user_subscriptions(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get user's active subscriptions"""
    try:
        payment_service = PaymentService()
        subscriptions = await payment_service.get_user_subscriptions(current_user.id)
        
        return {
            "subscriptions": subscriptions,
            "total": len(subscriptions)
        }
        
    except Exception as e:
        logger.error("Failed to get subscriptions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/subscription/{subscription_id}/cancel")
async def cancel_subscription(
    subscription_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Cancel user subscription"""
    try:
        payment_service = PaymentService()
        
        # Cancel subscription
        result = await payment_service.cancel_subscription(
            subscription_id=subscription_id,
            user_id=current_user.id
        )
        
        logger.info(
            "Subscription cancelled",
            user_id=current_user.id,
            subscription_id=subscription_id
        )
        
        return {
            "success": True,
            "message": "Subscription cancelled successfully",
            "cancelled_at": result.cancelled_at
        }
        
    except Exception as e:
        logger.error("Subscription cancellation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/plans")
async def get_subscription_plans():
    """Get available subscription plans"""
    return {
        "plans": [
            {
                "id": "free",
                "name": "Free",
                "price": 0,
                "currency": "INR",
                "billing_cycle": "monthly",
                "features": [
                    "5 voice commands per day",
                    "Basic app templates",
                    "Community support",
                    "Generated apps expire in 7 days"
                ],
                "limits": {
                    "voice_commands_per_day": 5,
                    "apps_per_month": 10,
                    "storage_mb": 100
                }
            },
            {
                "id": "pro",
                "name": "Pro",
                "price": 999,
                "currency": "INR",
                "billing_cycle": "monthly",
                "features": [
                    "Unlimited voice commands",
                    "Premium app templates",
                    "Priority support",
                    "Generated apps never expire",
                    "Custom domains",
                    "Advanced analytics"
                ],
                "limits": {
                    "voice_commands_per_day": -1,  # Unlimited
                    "apps_per_month": -1,  # Unlimited
                    "storage_mb": 1000
                }
            },
            {
                "id": "enterprise",
                "name": "Enterprise",
                "price": 4999,
                "currency": "INR",
                "billing_cycle": "monthly",
                "features": [
                    "Everything in Pro",
                    "Team collaboration",
                    "White-label solution",
                    "Dedicated support",
                    "Custom integrations",
                    "Advanced security"
                ],
                "limits": {
                    "voice_commands_per_day": -1,
                    "apps_per_month": -1,
                    "storage_mb": 10000,
                    "team_members": 50
                }
            }
        ],
        "currency": "INR",
        "country": "IN"
    }


@router.post("/refund/{payment_id}")
async def request_refund(
    payment_id: str,
    reason: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Request refund for payment"""
    try:
        payment_service = PaymentService()
        
        # Request refund
        refund_result = await payment_service.request_refund(
            payment_id=payment_id,
            user_id=current_user.id,
            reason=reason
        )
        
        logger.info(
            "Refund requested",
            user_id=current_user.id,
            payment_id=payment_id,
            refund_id=refund_result.refund_id
        )
        
        return {
            "success": True,
            "refund_id": refund_result.refund_id,
            "status": refund_result.status,
            "message": "Refund request submitted successfully"
        }
        
    except Exception as e:
        logger.error("Refund request failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint for payments service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "payments",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

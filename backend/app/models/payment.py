"""
Payment models for Voice-to-App SaaS Platform
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from decimal import Decimal
from enum import Enum


class PaymentProvider(str, Enum):
    RAZORPAY = "razorpay"
    PAYPAL = "paypal"
    GOOGLE_PAY = "google_pay"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class PaymentCreateRequest(BaseModel):
    amount: Decimal
    currency: str = "INR"
    description: str
    preferred_provider: Optional[PaymentProvider] = None
    metadata: Optional[Dict[str, Any]] = None


class PaymentCreateResponse(BaseModel):
    order_id: str
    provider: PaymentProvider
    amount: Decimal
    currency: str
    payment_data: Dict[str, Any]
    qr_code_url: Optional[str] = None
    upi_intent_url: Optional[str] = None
    expires_at: datetime


class PaymentVerifyRequest(BaseModel):
    order_id: str
    payment_id: str
    provider: PaymentProvider
    signature: Optional[str] = None


class PaymentVerifyResponse(BaseModel):
    success: bool
    payment_id: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    message: str


class SubscriptionCreateRequest(BaseModel):
    plan_id: str
    provider: PaymentProvider
    billing_cycle: str = "monthly"  # "monthly", "yearly"


class SubscriptionCreateResponse(BaseModel):
    subscription_id: str
    provider: PaymentProvider
    plan_id: str
    status: str
    payment_data: Dict[str, Any]
    next_billing_date: Optional[datetime] = None


class UPIQRRequest(BaseModel):
    amount: Decimal
    description: str


class UPIQRResponse(BaseModel):
    qr_code_url: str
    upi_id: str
    amount: Decimal
    expires_at: datetime


class Payment(BaseModel):
    id: str
    user_id: str
    provider: PaymentProvider
    provider_payment_id: str
    amount: Decimal
    currency: str
    status: PaymentStatus
    metadata: Dict[str, Any]
    webhook_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Subscription(BaseModel):
    id: str
    user_id: str
    plan_id: str
    status: str
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None
    razorpay_subscription_id: Optional[str] = None
    paypal_subscription_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
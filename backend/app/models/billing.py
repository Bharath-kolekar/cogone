"""
Billing models for comprehensive subscription and payment management
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
from decimal import Decimal


class SubscriptionTier(str, Enum):
    """Subscription tier options"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class PaymentStatus(str, Enum):
    """Payment status options"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class BillingCycle(str, Enum):
    """Billing cycle options"""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"
    LIFETIME = "lifetime"


class SubscriptionPlan(BaseModel):
    """Subscription plan model"""
    plan_id: str = Field(..., description="Unique plan identifier")
    name: str = Field(..., description="Plan display name")
    tier: SubscriptionTier = Field(..., description="Subscription tier")
    description: str = Field(..., description="Plan description")
    price: Decimal = Field(..., description="Plan price")
    billing_cycle: BillingCycle = Field(..., description="Billing cycle")
    features: List[str] = Field(..., description="Included features")
    limits: Dict[str, Any] = Field(..., description="Usage limits")
    ai_requests_per_month: int = Field(..., description="AI requests per month")
    voice_commands_per_day: int = Field(..., description="Voice commands per day")
    app_generations_per_month: int = Field(..., description="App generations per month")
    storage_gb: int = Field(..., description="Storage in GB")
    api_calls_per_month: int = Field(..., description="API calls per month")
    priority_support: bool = Field(default=False, description="Priority support")
    custom_domain: bool = Field(default=False, description="Custom domain support")
    white_label: bool = Field(default=False, description="White label support")
    advanced_analytics: bool = Field(default=False, description="Advanced analytics")
    team_collaboration: bool = Field(default=False, description="Team collaboration")
    is_active: bool = Field(default=True, description="Plan is active")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class UserSubscription(BaseModel):
    """User subscription model"""
    subscription_id: str = Field(..., description="Unique subscription identifier")
    user_id: str = Field(..., description="User ID")
    plan_id: str = Field(..., description="Plan ID")
    status: str = Field(..., description="Subscription status")
    current_period_start: datetime = Field(..., description="Current period start")
    current_period_end: datetime = Field(..., description="Current period end")
    cancel_at_period_end: bool = Field(default=False, description="Cancel at period end")
    trial_end: Optional[datetime] = Field(default=None, description="Trial end date")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class Payment(BaseModel):
    """Payment model"""
    payment_id: str = Field(..., description="Unique payment identifier")
    user_id: str = Field(..., description="User ID")
    subscription_id: str = Field(..., description="Subscription ID")
    amount: Decimal = Field(..., description="Payment amount")
    currency: str = Field(default="USD", description="Payment currency")
    status: PaymentStatus = Field(..., description="Payment status")
    payment_method: str = Field(..., description="Payment method")
    payment_provider: str = Field(..., description="Payment provider")
    transaction_id: Optional[str] = Field(default=None, description="Transaction ID")
    description: str = Field(..., description="Payment description")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Payment metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class Invoice(BaseModel):
    """Invoice model"""
    invoice_id: str = Field(..., description="Unique invoice identifier")
    user_id: str = Field(..., description="User ID")
    subscription_id: str = Field(..., description="Subscription ID")
    amount: Decimal = Field(..., description="Invoice amount")
    currency: str = Field(default="USD", description="Invoice currency")
    status: str = Field(..., description="Invoice status")
    due_date: datetime = Field(..., description="Due date")
    paid_at: Optional[datetime] = Field(default=None, description="Paid timestamp")
    items: List[Dict[str, Any]] = Field(..., description="Invoice items")
    tax_amount: Decimal = Field(default=Decimal("0.00"), description="Tax amount")
    total_amount: Decimal = Field(..., description="Total amount including tax")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class UsageMetrics(BaseModel):
    """Usage metrics model"""
    user_id: str = Field(..., description="User ID")
    subscription_id: str = Field(..., description="Subscription ID")
    period_start: datetime = Field(..., description="Period start")
    period_end: datetime = Field(..., description="Period end")
    ai_requests_used: int = Field(default=0, description="AI requests used")
    ai_requests_limit: int = Field(..., description="AI requests limit")
    voice_commands_used: int = Field(default=0, description="Voice commands used")
    voice_commands_limit: int = Field(..., description="Voice commands limit")
    app_generations_used: int = Field(default=0, description="App generations used")
    app_generations_limit: int = Field(..., description="App generations limit")
    storage_used_gb: Decimal = Field(default=Decimal("0.00"), description="Storage used in GB")
    storage_limit_gb: int = Field(..., description="Storage limit in GB")
    api_calls_used: int = Field(default=0, description="API calls used")
    api_calls_limit: int = Field(..., description="API calls limit")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class BillingSettings(BaseModel):
    """Billing settings model"""
    user_id: str = Field(..., description="User ID")
    default_payment_method: Optional[str] = Field(default=None, description="Default payment method")
    billing_email: str = Field(..., description="Billing email")
    tax_id: Optional[str] = Field(default=None, description="Tax ID")
    company_name: Optional[str] = Field(default=None, description="Company name")
    billing_address: Dict[str, Any] = Field(default_factory=dict, description="Billing address")
    auto_renew: bool = Field(default=True, description="Auto renew subscription")
    invoice_email: bool = Field(default=True, description="Send invoice emails")
    usage_alerts: bool = Field(default=True, description="Send usage alerts")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class ProfitMetrics(BaseModel):
    """Profit metrics model"""
    period_start: datetime = Field(..., description="Period start")
    period_end: datetime = Field(..., description="Period end")
    total_revenue: Decimal = Field(..., description="Total revenue")
    total_costs: Decimal = Field(..., description="Total costs")
    gross_profit: Decimal = Field(..., description="Gross profit")
    net_profit: Decimal = Field(..., description="Net profit")
    profit_margin: Decimal = Field(..., description="Profit margin percentage")
    customer_count: int = Field(..., description="Total customers")
    average_revenue_per_user: Decimal = Field(..., description="ARPU")
    churn_rate: Decimal = Field(..., description="Customer churn rate")
    lifetime_value: Decimal = Field(..., description="Customer lifetime value")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

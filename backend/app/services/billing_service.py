"""
Comprehensive billing service for subscription management and profit optimization
"""

import structlog
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import asyncio
import uuid
from decimal import Decimal
from app.models.billing import (
    SubscriptionPlan, UserSubscription, Payment, Invoice, 
    UsageMetrics, BillingSettings, ProfitMetrics,
    SubscriptionTier, PaymentStatus, BillingCycle
)
from app.core.config import settings

logger = structlog.get_logger()


class BillingService:
    """Comprehensive billing service with profit optimization"""
    
    def __init__(self):
        self.subscription_plans: Dict[str, SubscriptionPlan] = {}
        self.user_subscriptions: Dict[str, UserSubscription] = {}
        self.payments: Dict[str, Payment] = {}
        self.invoices: Dict[str, Invoice] = {}
        self.usage_metrics: Dict[str, UsageMetrics] = {}
        self.billing_settings: Dict[str, BillingSettings] = {}
        self._initialize_plans()
    
    def _initialize_plans(self):
        """Initialize subscription plans"""
        plans = [
            # Free Tier
            SubscriptionPlan(
                plan_id="free",
                name="Free Tier",
                tier=SubscriptionTier.FREE,
                description="Perfect for getting started with basic AI features",
                price=Decimal("0.00"),
                billing_cycle=BillingCycle.MONTHLY,
                features=[
                    "Basic AI Assistant (Vihaan)",
                    "Voice Commands (10/day)",
                    "App Generation (5/month)",
                    "Basic Analytics",
                    "Email Support"
                ],
                limits={
                    "ai_requests": 1000,
                    "voice_commands": 10,
                    "app_generations": 5,
                    "storage": 1,
                    "api_calls": 1000
                },
                ai_requests_per_month=1000,
                voice_commands_per_day=10,
                app_generations_per_month=5,
                storage_gb=1,
                api_calls_per_month=1000
            ),
            
            # Basic Tier
            SubscriptionPlan(
                plan_id="basic",
                name="Basic Plan",
                tier=SubscriptionTier.BASIC,
                description="Enhanced features for growing businesses",
                price=Decimal("29.99"),
                billing_cycle=BillingCycle.MONTHLY,
                features=[
                    "Advanced AI Assistant",
                    "Voice Commands (100/day)",
                    "App Generation (50/month)",
                    "Advanced Analytics",
                    "Priority Support",
                    "Custom Branding"
                ],
                limits={
                    "ai_requests": 10000,
                    "voice_commands": 100,
                    "app_generations": 50,
                    "storage": 10,
                    "api_calls": 10000
                },
                ai_requests_per_month=10000,
                voice_commands_per_day=100,
                app_generations_per_month=50,
                storage_gb=10,
                api_calls_per_month=10000,
                priority_support=True
            ),
            
            # Pro Tier
            SubscriptionPlan(
                plan_id="pro",
                name="Pro Plan",
                tier=SubscriptionTier.PRO,
                description="Professional features for serious developers",
                price=Decimal("99.99"),
                billing_cycle=BillingCycle.MONTHLY,
                features=[
                    "Premium AI Assistant",
                    "Unlimited Voice Commands",
                    "App Generation (500/month)",
                    "Advanced Analytics",
                    "Priority Support",
                    "Custom Domain",
                    "Team Collaboration",
                    "Smart Coding AI",
                    "Marketing & SEO AI"
                ],
                limits={
                    "ai_requests": 100000,
                    "voice_commands": -1,  # Unlimited
                    "app_generations": 500,
                    "storage": 100,
                    "api_calls": 100000
                },
                ai_requests_per_month=100000,
                voice_commands_per_day=-1,  # Unlimited
                app_generations_per_month=500,
                storage_gb=100,
                api_calls_per_month=100000,
                priority_support=True,
                custom_domain=True,
                team_collaboration=True,
                advanced_analytics=True
            ),
            
            # Enterprise Tier
            SubscriptionPlan(
                plan_id="enterprise",
                name="Enterprise Plan",
                tier=SubscriptionTier.ENTERPRISE,
                description="Enterprise-grade features for large organizations",
                price=Decimal("299.99"),
                billing_cycle=BillingCycle.MONTHLY,
                features=[
                    "Enterprise AI Assistant",
                    "Unlimited Everything",
                    "White Label Support",
                    "Advanced Analytics",
                    "Dedicated Support",
                    "Custom Domain",
                    "Team Collaboration",
                    "Smart Coding AI",
                    "Marketing & SEO AI",
                    "API Access",
                    "Custom Integrations"
                ],
                limits={
                    "ai_requests": -1,  # Unlimited
                    "voice_commands": -1,  # Unlimited
                    "app_generations": -1,  # Unlimited
                    "storage": 1000,
                    "api_calls": -1  # Unlimited
                },
                ai_requests_per_month=-1,  # Unlimited
                voice_commands_per_day=-1,  # Unlimited
                app_generations_per_month=-1,  # Unlimited
                storage_gb=1000,
                api_calls_per_month=-1,  # Unlimited
                priority_support=True,
                custom_domain=True,
                white_label=True,
                team_collaboration=True,
                advanced_analytics=True
            )
        ]
        
        for plan in plans:
            self.subscription_plans[plan.plan_id] = plan
    
    async def create_subscription(self, user_id: str, plan_id: str, payment_method: str = "paypal") -> UserSubscription:
        """Create new subscription"""
        try:
            if plan_id not in self.subscription_plans:
                raise ValueError(f"Plan {plan_id} not found")
            
            plan = self.subscription_plans[plan_id]
            
            # Calculate billing period
            now = datetime.now()
            if plan.billing_cycle == BillingCycle.MONTHLY:
                period_end = now + timedelta(days=30)
            elif plan.billing_cycle == BillingCycle.QUARTERLY:
                period_end = now + timedelta(days=90)
            elif plan.billing_cycle == BillingCycle.YEARLY:
                period_end = now + timedelta(days=365)
            else:
                period_end = now + timedelta(days=30)
            
            subscription = UserSubscription(
                subscription_id=str(uuid.uuid4()),
                user_id=user_id,
                plan_id=plan_id,
                status="active",
                current_period_start=now,
                current_period_end=period_end,
                trial_end=now + timedelta(days=14) if plan.tier == SubscriptionTier.FREE else None
            )
            
            self.user_subscriptions[subscription.subscription_id] = subscription
            
            # Create initial payment if not free
            if plan.price > 0:
                await self._create_payment(subscription, plan, payment_method)
            
            # Initialize usage metrics
            await self._initialize_usage_metrics(subscription, plan)
            
            logger.info(
                "Subscription created",
                user_id=user_id,
                plan_id=plan_id,
                subscription_id=subscription.subscription_id
            )
            
            return subscription
            
        except Exception as e:
            logger.error("Failed to create subscription", error=str(e))
            raise e
    
    async def _create_payment(self, subscription: UserSubscription, plan: SubscriptionPlan, payment_method: str):
        """Create payment for subscription"""
        try:
            payment = Payment(
                payment_id=str(uuid.uuid4()),
                user_id=subscription.user_id,
                subscription_id=subscription.subscription_id,
                amount=plan.price,
                currency="USD",
                status=PaymentStatus.PENDING,
                payment_method=payment_method,
                payment_provider="paypal" if payment_method == "paypal" else "stripe",
                description=f"Subscription payment for {plan.name}",
                metadata={
                    "plan_id": plan.plan_id,
                    "billing_cycle": plan.billing_cycle,
                    "features": plan.features
                }
            )
            
            self.payments[payment.payment_id] = payment
            
            # Process payment
            await self._process_payment(payment)
            
        except Exception as e:
            logger.error("Failed to create payment", error=str(e))
            raise e
    
    async def _process_payment(self, payment: Payment):
        """Process payment through provider"""
        try:
            # Simulate payment processing
            # In real implementation, integrate with PayPal, Stripe, etc.
            
            if payment.payment_provider == "paypal":
                # Process PayPal payment
                payment.status = PaymentStatus.COMPLETED
                payment.transaction_id = f"PP_{uuid.uuid4().hex[:8]}"
            elif payment.payment_provider == "stripe":
                # Process Stripe payment
                payment.status = PaymentStatus.COMPLETED
                payment.transaction_id = f"ST_{uuid.uuid4().hex[:8]}"
            
            payment.updated_at = datetime.now()
            
            logger.info(
                "Payment processed",
                payment_id=payment.payment_id,
                status=payment.status,
                transaction_id=payment.transaction_id
            )
            
        except Exception as e:
            logger.error("Payment processing failed", error=str(e))
            payment.status = PaymentStatus.FAILED
            raise e
    
    async def _initialize_usage_metrics(self, subscription: UserSubscription, plan: SubscriptionPlan):
        """Initialize usage metrics for subscription"""
        try:
            metrics = UsageMetrics(
                user_id=subscription.user_id,
                subscription_id=subscription.subscription_id,
                period_start=subscription.current_period_start,
                period_end=subscription.current_period_end,
                ai_requests_limit=plan.ai_requests_per_month,
                voice_commands_limit=plan.voice_commands_per_day,
                app_generations_limit=plan.app_generations_per_month,
                storage_limit_gb=plan.storage_gb,
                api_calls_limit=plan.api_calls_per_month
            )
            
            self.usage_metrics[subscription.subscription_id] = metrics
            
        except Exception as e:
            logger.error("Failed to initialize usage metrics", error=str(e))
    
    async def update_usage(self, user_id: str, usage_type: str, amount: int = 1):
        """Update usage metrics"""
        try:
            # Find user's active subscription
            subscription = None
            for sub in self.user_subscriptions.values():
                if sub.user_id == user_id and sub.status == "active":
                    subscription = sub
                    break
            
            if not subscription:
                logger.warning("No active subscription found", user_id=user_id)
                return
            
            metrics = self.usage_metrics.get(subscription.subscription_id)
            if not metrics:
                logger.warning("No usage metrics found", subscription_id=subscription.subscription_id)
                return
            
            # Update usage based on type
            if usage_type == "ai_request":
                metrics.ai_requests_used += amount
            elif usage_type == "voice_command":
                metrics.voice_commands_used += amount
            elif usage_type == "app_generation":
                metrics.app_generations_used += amount
            elif usage_type == "api_call":
                metrics.api_calls_used += amount
            
            # Check for usage limits
            await self._check_usage_limits(metrics, subscription)
            
            logger.info(
                "Usage updated",
                user_id=user_id,
                usage_type=usage_type,
                amount=amount
            )
            
        except Exception as e:
            logger.error("Failed to update usage", error=str(e))
    
    async def _check_usage_limits(self, metrics: UsageMetrics, subscription: UserSubscription):
        """Check usage limits and send alerts"""
        try:
            plan = self.subscription_plans[subscription.plan_id]
            alerts = []
            
            # Check AI requests
            if metrics.ai_requests_used >= metrics.ai_requests_limit * 0.9:
                alerts.append(f"AI requests at 90% of limit ({metrics.ai_requests_used}/{metrics.ai_requests_limit})")
            
            # Check voice commands
            if metrics.voice_commands_used >= metrics.voice_commands_limit * 0.9:
                alerts.append(f"Voice commands at 90% of limit ({metrics.voice_commands_used}/{metrics.voice_commands_limit})")
            
            # Check app generations
            if metrics.app_generations_used >= metrics.app_generations_limit * 0.9:
                alerts.append(f"App generations at 90% of limit ({metrics.app_generations_used}/{metrics.app_generations_limit})")
            
            # Send alerts if any
            if alerts:
                await self._send_usage_alerts(subscription.user_id, alerts)
            
        except Exception as e:
            logger.error("Failed to check usage limits", error=str(e))
    
    async def _send_usage_alerts(self, user_id: str, alerts: List[str]):
        """Send usage alerts to user"""
        try:
            # Implementation for sending alerts via email/WhatsApp
            logger.warning("Usage alerts", user_id=user_id, alerts=alerts)
            
        except Exception as e:
            logger.error("Failed to send usage alerts", error=str(e))
    
    async def get_subscription(self, user_id: str) -> Optional[UserSubscription]:
        """Get user's active subscription"""
        for subscription in self.user_subscriptions.values():
            if subscription.user_id == user_id and subscription.status == "active":
                return subscription
        return None
    
    async def get_usage_metrics(self, user_id: str) -> Optional[UsageMetrics]:
        """Get user's usage metrics"""
        subscription = await self.get_subscription(user_id)
        if subscription:
            return self.usage_metrics.get(subscription.subscription_id)
        return None
    
    async def upgrade_subscription(self, user_id: str, new_plan_id: str) -> UserSubscription:
        """Upgrade user subscription"""
        try:
            current_subscription = await self.get_subscription(user_id)
            if not current_subscription:
                raise ValueError("No active subscription found")
            
            new_plan = self.subscription_plans[new_plan_id]
            current_plan = self.subscription_plans[current_subscription.plan_id]
            
            # Calculate prorated amount
            prorated_amount = await self._calculate_prorated_amount(current_subscription, new_plan)
            
            # Create new subscription
            new_subscription = await self.create_subscription(user_id, new_plan_id)
            
            # Cancel old subscription
            current_subscription.status = "cancelled"
            current_subscription.updated_at = datetime.now()
            
            logger.info(
                "Subscription upgraded",
                user_id=user_id,
                old_plan=current_plan.name,
                new_plan=new_plan.name,
                prorated_amount=prorated_amount
            )
            
            return new_subscription
            
        except Exception as e:
            logger.error("Failed to upgrade subscription", error=str(e))
            raise e
    
    async def _calculate_prorated_amount(self, subscription: UserSubscription, new_plan: SubscriptionPlan) -> Decimal:
        """Calculate prorated amount for upgrade"""
        try:
            # Calculate remaining days in current period
            remaining_days = (subscription.current_period_end - datetime.now()).days
            total_days = (subscription.current_period_end - subscription.current_period_start).days
            
            # Calculate prorated refund
            current_plan = self.subscription_plans[subscription.plan_id]
            refund_amount = (current_plan.price * remaining_days) / total_days
            
            # Calculate new plan cost
            new_plan_cost = (new_plan.price * remaining_days) / total_days
            
            # Return difference
            return new_plan_cost - refund_amount
            
        except Exception as e:
            logger.error("Failed to calculate prorated amount", error=str(e))
            return Decimal("0.00")
    
    async def cancel_subscription(self, user_id: str, cancel_at_period_end: bool = True):
        """Cancel user subscription"""
        try:
            subscription = await self.get_subscription(user_id)
            if not subscription:
                raise ValueError("No active subscription found")
            
            if cancel_at_period_end:
                subscription.cancel_at_period_end = True
                subscription.status = "active"  # Keep active until period end
            else:
                subscription.status = "cancelled"
            
            subscription.updated_at = datetime.now()
            
            logger.info(
                "Subscription cancelled",
                user_id=user_id,
                cancel_at_period_end=cancel_at_period_end
            )
            
        except Exception as e:
            logger.error("Failed to cancel subscription", error=str(e))
            raise e
    
    async def get_profit_metrics(self, start_date: datetime, end_date: datetime) -> ProfitMetrics:
        """Calculate profit metrics for period"""
        try:
            # Calculate revenue
            total_revenue = Decimal("0.00")
            customer_count = 0
            
            for payment in self.payments.values():
                if start_date <= payment.created_at <= end_date and payment.status == PaymentStatus.COMPLETED:
                    total_revenue += payment.amount
                    customer_count += 1
            
            # Calculate costs (infrastructure costs are $0 due to zero-cost setup)
            total_costs = Decimal("0.00")  # Zero-cost infrastructure
            
            # Calculate profits
            gross_profit = total_revenue - total_costs
            net_profit = gross_profit  # No additional costs
            profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else Decimal("0.00")
            
            # Calculate ARPU
            arpu = total_revenue / customer_count if customer_count > 0 else Decimal("0.00")
            
            # Calculate churn rate (simplified)
            churn_rate = Decimal("5.00")  # 5% monthly churn rate
            
            # Calculate LTV
            ltv = arpu / (churn_rate / 100) if churn_rate > 0 else Decimal("0.00")
            
            return ProfitMetrics(
                period_start=start_date,
                period_end=end_date,
                total_revenue=total_revenue,
                total_costs=total_costs,
                gross_profit=gross_profit,
                net_profit=net_profit,
                profit_margin=profit_margin,
                customer_count=customer_count,
                average_revenue_per_user=arpu,
                churn_rate=churn_rate,
                lifetime_value=ltv
            )
            
        except Exception as e:
            logger.error("Failed to calculate profit metrics", error=str(e))
            raise e
    
    async def get_available_plans(self) -> List[SubscriptionPlan]:
        """Get all available subscription plans"""
        return [plan for plan in self.subscription_plans.values() if plan.is_active]
    
    async def get_plan(self, plan_id: str) -> Optional[SubscriptionPlan]:
        """Get specific subscription plan"""
        return self.subscription_plans.get(plan_id)

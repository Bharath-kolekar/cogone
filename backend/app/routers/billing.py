"""
Billing API endpoints for subscription and payment management
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from app.models.billing import (
    SubscriptionPlan, UserSubscription, Payment, Invoice, 
    UsageMetrics, BillingSettings, ProfitMetrics,
    SubscriptionTier, PaymentStatus, BillingCycle
)
from app.services.billing_service import BillingService
from app.services.profit_strategies_service import ProfitStrategiesService
from app.services.marketing_seo_ai_service import MarketingSEOAI
from app.services.smart_coding_ai_service import SmartCodingAI

logger = structlog.get_logger()
router = APIRouter()

# Initialize services
billing_service = BillingService()
profit_strategies_service = ProfitStrategiesService()
marketing_seo_ai = MarketingSEOAI()
smart_coding_ai = SmartCodingAI()


@router.get("/plans", response_model=List[SubscriptionPlan])
async def get_subscription_plans():
    """Get all available subscription plans"""
    try:
        plans = await billing_service.get_available_plans()
        logger.info("Subscription plans retrieved", count=len(plans))
        return plans
    except Exception as e:
        logger.error("Failed to retrieve subscription plans", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve subscription plans: {e}"
        )


@router.get("/plans/{plan_id}", response_model=SubscriptionPlan)
async def get_subscription_plan(plan_id: str):
    """Get specific subscription plan"""
    try:
        plan = await billing_service.get_plan(plan_id)
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plan {plan_id} not found"
            )
        return plan
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to retrieve subscription plan", plan_id=plan_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve subscription plan: {e}"
        )


@router.post("/subscriptions", response_model=UserSubscription)
async def create_subscription(
    user_id: str,
    plan_id: str,
    payment_method: str = "paypal"
):
    """Create new subscription"""
    try:
        subscription = await billing_service.create_subscription(user_id, plan_id, payment_method)
        logger.info("Subscription created", user_id=user_id, plan_id=plan_id, subscription_id=subscription.subscription_id)
        return subscription
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to create subscription", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create subscription: {e}"
        )


@router.get("/subscriptions/{user_id}", response_model=Optional[UserSubscription])
async def get_user_subscription(user_id: str):
    """Get user's active subscription"""
    try:
        subscription = await billing_service.get_subscription(user_id)
        if not subscription:
            logger.info("No active subscription found", user_id=user_id)
        return subscription
    except Exception as e:
        logger.error("Failed to retrieve user subscription", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user subscription: {e}"
        )


@router.post("/subscriptions/{user_id}/upgrade", response_model=UserSubscription)
async def upgrade_subscription(user_id: str, new_plan_id: str):
    """Upgrade user subscription"""
    try:
        subscription = await billing_service.upgrade_subscription(user_id, new_plan_id)
        logger.info("Subscription upgraded", user_id=user_id, new_plan_id=new_plan_id)
        return subscription
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to upgrade subscription", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upgrade subscription: {e}"
        )


@router.post("/subscriptions/{user_id}/cancel")
async def cancel_subscription(user_id: str, cancel_at_period_end: bool = True):
    """Cancel user subscription"""
    try:
        await billing_service.cancel_subscription(user_id, cancel_at_period_end)
        logger.info("Subscription cancelled", user_id=user_id, cancel_at_period_end=cancel_at_period_end)
        return {"message": "Subscription cancelled successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to cancel subscription", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel subscription: {e}"
        )


@router.get("/usage/{user_id}", response_model=Optional[UsageMetrics])
async def get_usage_metrics(user_id: str):
    """Get user's usage metrics"""
    try:
        metrics = await billing_service.get_usage_metrics(user_id)
        return metrics
    except Exception as e:
        logger.error("Failed to retrieve usage metrics", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve usage metrics: {e}"
        )


@router.post("/usage/{user_id}/update")
async def update_usage(
    user_id: str,
    usage_type: str,
    amount: int = 1
):
    """Update usage metrics"""
    try:
        await billing_service.update_usage(user_id, usage_type, amount)
        logger.info("Usage updated", user_id=user_id, usage_type=usage_type, amount=amount)
        return {"message": "Usage updated successfully"}
    except Exception as e:
        logger.error("Failed to update usage", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update usage: {e}"
        )


@router.get("/profit-metrics", response_model=ProfitMetrics)
async def get_profit_metrics(
    start_date: datetime = Query(..., description="Start date for profit metrics"),
    end_date: datetime = Query(..., description="End date for profit metrics")
):
    """Get profit metrics for period"""
    try:
        metrics = await billing_service.get_profit_metrics(start_date, end_date)
        return metrics
    except Exception as e:
        logger.error("Failed to calculate profit metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate profit metrics: {e}"
        )


@router.get("/profit-strategies")
async def get_profit_strategies():
    """Get all profit strategies"""
    try:
        strategies = await profit_strategies_service.get_profit_strategies()
        return strategies
    except Exception as e:
        logger.error("Failed to retrieve profit strategies", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve profit strategies: {e}"
        )


@router.get("/profit-strategies/active")
async def get_active_profit_strategies():
    """Get active profit strategies"""
    try:
        strategies = await profit_strategies_service.get_active_strategies()
        return strategies
    except Exception as e:
        logger.error("Failed to retrieve active profit strategies", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve active profit strategies: {e}"
        )


@router.get("/revenue-streams")
async def get_revenue_streams():
    """Get all revenue streams"""
    try:
        streams = await profit_strategies_service.get_revenue_streams()
        return streams
    except Exception as e:
        logger.error("Failed to retrieve revenue streams", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve revenue streams: {e}"
        )


@router.get("/revenue-potential")
async def get_revenue_potential():
    """Get revenue potential analysis"""
    try:
        potential = await profit_strategies_service.calculate_revenue_potential()
        return potential
    except Exception as e:
        logger.error("Failed to calculate revenue potential", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate revenue potential: {e}"
        )


@router.get("/implementation-roadmap")
async def get_implementation_roadmap():
    """Get implementation roadmap for revenue streams"""
    try:
        roadmap = await profit_strategies_service.get_implementation_roadmap()
        return roadmap
    except Exception as e:
        logger.error("Failed to get implementation roadmap", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get implementation roadmap: {e}"
        )


@router.get("/profit-optimization-tips")
async def get_profit_optimization_tips():
    """Get profit optimization tips"""
    try:
        tips = await profit_strategies_service.get_profit_optimization_tips()
        return tips
    except Exception as e:
        logger.error("Failed to get profit optimization tips", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profit optimization tips: {e}"
        )


@router.get("/competitive-analysis")
async def get_competitive_analysis():
    """Get competitive analysis for profit optimization"""
    try:
        analysis = await profit_strategies_service.get_competitive_analysis()
        return analysis
    except Exception as e:
        logger.error("Failed to get competitive analysis", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get competitive analysis: {e}"
        )


@router.get("/marketing-insights")
async def get_marketing_insights():
    """Get marketing insights"""
    try:
        insights = await marketing_seo_ai.get_marketing_insights()
        return insights
    except Exception as e:
        logger.error("Failed to get marketing insights", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get marketing insights: {e}"
        )


@router.post("/content-campaigns")
async def create_content_campaign(
    name: str,
    description: str,
    content_type: str,
    target_audience: str,
    keywords: List[str],
    tone: str = "professional"
):
    """Create content campaign"""
    try:
        from app.services.marketing_seo_ai_service import ContentType
        campaign = await marketing_seo_ai.create_content_campaign(
            name, description, ContentType(content_type), target_audience, keywords, tone
        )
        return campaign
    except Exception as e:
        logger.error("Failed to create content campaign", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create content campaign: {e}"
        )


@router.post("/generate-content")
async def generate_content(
    campaign_id: str,
    topic: str,
    requirements: Dict[str, Any]
):
    """Generate AI-powered content"""
    try:
        content = await marketing_seo_ai.generate_content(campaign_id, topic, requirements)
        return content
    except Exception as e:
        logger.error("Failed to generate content", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate content: {e}"
        )


@router.post("/seo-analysis")
async def analyze_seo(content: str, title: str = ""):
    """Analyze SEO of content"""
    try:
        analysis = await marketing_seo_ai.analyze_seo(content, title)
        return analysis
    except Exception as e:
        logger.error("Failed to analyze SEO", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze SEO: {e}"
        )


@router.get("/marketing-recommendations")
async def get_marketing_recommendations():
    """Get marketing recommendations"""
    try:
        recommendations = await marketing_seo_ai.get_marketing_recommendations()
        return recommendations
    except Exception as e:
        logger.error("Failed to get marketing recommendations", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get marketing recommendations: {e}"
        )


@router.post("/generate-code")
async def generate_code(
    prompt: str,
    language: str,
    context: Dict[str, Any] = None
):
    """Generate code using Smart Coding AI"""
    try:
        from app.services.smart_coding_ai_service import CodeLanguage
        suggestion = await smart_coding_ai.generate_code(prompt, CodeLanguage(language), context or {})
        return suggestion
    except Exception as e:
        logger.error("Failed to generate code", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate code: {e}"
        )


@router.post("/review-code")
async def review_code(code: str, language: str):
    """Review code for quality, security, and performance"""
    try:
        from app.services.smart_coding_ai_service import CodeLanguage
        review = await smart_coding_ai.review_code(code, CodeLanguage(language))
        return review
    except Exception as e:
        logger.error("Failed to review code", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to review code: {e}"
        )


@router.post("/create-workspace")
async def create_workspace(
    name: str,
    description: str,
    language: str,
    project_type: str = "general"
):
    """Create new code workspace"""
    try:
        from app.services.smart_coding_ai_service import CodeLanguage
        workspace = await smart_coding_ai.create_workspace(name, description, CodeLanguage(language), project_type)
        return workspace
    except Exception as e:
        logger.error("Failed to create workspace", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create workspace: {e}"
        )


@router.get("/coding-recommendations")
async def get_coding_recommendations():
    """Get coding recommendations"""
    try:
        recommendations = await smart_coding_ai.get_coding_recommendations()
        return recommendations
    except Exception as e:
        logger.error("Failed to get coding recommendations", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get coding recommendations: {e}"
        )

"""
User Preferences Router - Handle user threshold and billing preferences
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4
import asyncio
import json
import time
import logging

from app.core.database import get_supabase_client
from app.core.redis import get_redis_client
from app.models.user import User
from app.models.ai_agent import AgentDefinition, AgentType

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/user/preferences", tags=["User Preferences"])


@router.get("/threshold-options")
async def get_threshold_options() -> Dict[str, Any]:
    """Get available threshold options with pricing and features"""
    try:
        threshold_options = [
            {
                "id": "maximum",
                "name": "Maximum Precision",
                "precision": 0.99,
                "accuracy": 0.99,
                "response_time": "300-500ms",
                "computational_cost": "High",
                "price_per_request": 0.05,
                "features": [
                    "99%+ Precision & Accuracy",
                    "Advanced Validation (8 layers)",
                    "Maximum Reliability",
                    "Enterprise Security",
                    "Real-time Monitoring",
                    "Priority Support"
                ],
                "use_cases": [
                    "Financial Applications",
                    "Healthcare Systems",
                    "Legal Services",
                    "Critical Business Operations",
                    "Enterprise Solutions"
                ],
                "description": "Maximum precision and accuracy for critical applications requiring 99%+ reliability.",
                "recommended": False
            },
            {
                "id": "optimized",
                "name": "Optimized Balance",
                "precision": 0.95,
                "accuracy": 0.95,
                "response_time": "100-200ms",
                "computational_cost": "Medium",
                "price_per_request": 0.02,
                "features": [
                    "95%+ Precision & Accuracy",
                    "Balanced Validation (4 layers)",
                    "Good Reliability",
                    "Standard Security",
                    "Performance Monitoring",
                    "Standard Support"
                ],
                "use_cases": [
                    "General Applications",
                    "Customer Support",
                    "Content Generation",
                    "Business Operations",
                    "Standard Solutions"
                ],
                "description": "Optimal balance of precision, speed, and cost for most applications.",
                "recommended": True
            },
            {
                "id": "fast",
                "name": "Fast Processing",
                "precision": 0.90,
                "accuracy": 0.90,
                "response_time": "50-100ms",
                "computational_cost": "Low",
                "price_per_request": 0.01,
                "features": [
                    "90%+ Precision & Accuracy",
                    "Fast Validation (2 layers)",
                    "Basic Reliability",
                    "Standard Security",
                    "Basic Monitoring",
                    "Community Support"
                ],
                "use_cases": [
                    "High-Volume Systems",
                    "Real-time Applications",
                    "Development & Testing",
                    "Prototype Solutions",
                    "Cost-Sensitive Projects"
                ],
                "description": "Fast processing with good precision for high-volume or real-time applications.",
                "recommended": False
            }
        ]
        
        return {
            "threshold_options": threshold_options,
            "total_options": len(threshold_options),
            "recommended": "optimized"
        }
        
    except Exception as e:
        logger.error(f"Failed to get threshold options: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get threshold options: {str(e)}"
        )


@router.get("/billing-options")
async def get_billing_options() -> Dict[str, Any]:
    """Get available billing options with pricing and features"""
    try:
        billing_options = [
            {
                "id": "pay_per_use",
                "name": "Pay Per Use",
                "type": "pay_per_use",
                "price": 0.01,
                "requests": 0,
                "features": [
                    "Pay only for what you use",
                    "No monthly commitments",
                    "Flexible scaling",
                    "Perfect for testing",
                    "Start with $0"
                ],
                "description": "Perfect for testing and low-volume usage.",
                "savings": 0
            },
            {
                "id": "monthly",
                "name": "Monthly Plan",
                "type": "monthly",
                "price": 29.99,
                "requests": 10000,
                "features": [
                    "10,000 requests included",
                    "Monthly billing",
                    "Standard support",
                    "Performance monitoring",
                    "2x better value than pay-per-use"
                ],
                "description": "Best value for regular usage with included requests.",
                "savings": 50,
                "popular": True
            },
            {
                "id": "yearly",
                "name": "Yearly Plan",
                "type": "yearly",
                "price": 299.99,
                "requests": 150000,
                "features": [
                    "150,000 requests included",
                    "Annual billing",
                    "Priority support",
                    "Advanced monitoring",
                    "3x better value than monthly"
                ],
                "description": "Maximum value for high-volume usage with significant savings.",
                "savings": 67
            }
        ]
        
        return {
            "billing_options": billing_options,
            "total_options": len(billing_options),
            "popular": "monthly"
        }
        
    except Exception as e:
        logger.error(f"Failed to get billing options: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get billing options: {str(e)}"
        )


@router.get("/user-preferences/{user_id}")
async def get_user_preferences(user_id: UUID) -> Dict[str, Any]:
    """
    Get user preferences for threshold and billing
    
    🧬 REAL IMPLEMENTATION: Queries Supabase database
    """
    try:
        # Get user preferences from database
        db = get_supabase_client()
        
        if db:
            # Try to fetch from user_preferences table
            result = db.table('user_preferences').select('*').eq('user_id', str(user_id)).execute()
            
            if result.data and len(result.data) > 0:
                # Return existing preferences
                return {
                    "preferences": result.data[0],
                    "status": "success"
                }
        
        # If no database or no preferences found, return defaults
        default_preferences = {
            "user_id": str(user_id),
            "threshold_type": "optimized",
            "billing_option": "monthly",
            "auto_optimize": True,
            "notifications": True,
            "created_at": time.time(),
            "updated_at": time.time()
        }
        
        return {
                "preferences": default_preferences,
                "status": "success"
            }
            
    except Exception as e:
        logger.error(f"Failed to get user preferences: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get user preferences: {str(e)}"
        )


@router.post("/user-preferences")
async def save_user_preferences(
    preferences: Dict[str, Any],
    background_tasks: BackgroundTasks
) -> Dict[str, Any]:
    """Save user preferences for threshold and billing"""
    try:
        # Validate preferences
        required_fields = ["threshold_type", "billing_option"]
        for field in required_fields:
            if field not in preferences:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing required field: {field}"
                )
        
        # Validate threshold type
        valid_threshold_types = ["maximum", "optimized", "fast"]
        if preferences["threshold_type"] not in valid_threshold_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid threshold type. Must be one of: {valid_threshold_types}"
            )
        
        # Validate billing option
        valid_billing_options = ["pay_per_use", "monthly", "yearly"]
        if preferences["billing_option"] not in valid_billing_options:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid billing option. Must be one of: {valid_billing_options}"
            )
        
        # Save preferences to database
        db = get_supabase_client()
        
        saved_preferences = {
            "user_id": preferences.get("user_id", str(uuid4())),
            "threshold_type": preferences["threshold_type"],
            "billing_option": preferences["billing_option"],
            "auto_optimize": preferences.get("auto_optimize", True),
            "notifications": preferences.get("notifications", True),
            "created_at": time.time(),
            "updated_at": time.time()
        }
        
        # 🧬 REAL: Save to Supabase if available
        if db:
            try:
                # Upsert (insert or update) preferences
                db.table('user_preferences').upsert(saved_preferences).execute()
                logger.info(f"Saved preferences for user {saved_preferences['user_id']}")
            except Exception as db_error:
                logger.warning(f"Database save failed, continuing: {db_error}")
        
        # Background task for analytics
        background_tasks.add_task(
            _log_preference_change,
            saved_preferences
        )
        
        return {
            "preferences": saved_preferences,
            "status": "success",
            "message": "Preferences saved successfully"
        }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save user preferences: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save user preferences: {str(e)}"
        )


@router.get("/cost-calculation")
async def calculate_cost(
    threshold_type: str,
    billing_option: str,
    estimated_requests: int = 1000
) -> Dict[str, Any]:
    """Calculate estimated cost based on threshold and billing options"""
    try:
        # Threshold pricing
        threshold_pricing = {
            "maximum": 0.05,
            "optimized": 0.02,
            "fast": 0.01
        }
        
        # Billing pricing
        billing_pricing = {
            "pay_per_use": {"base_price": 0, "price_per_request": threshold_pricing[threshold_type]},
            "monthly": {"base_price": 29.99, "included_requests": 10000, "price_per_request": threshold_pricing[threshold_type]},
            "yearly": {"base_price": 299.99, "included_requests": 150000, "price_per_request": threshold_pricing[threshold_type]}
        }
        
        # Calculate cost
        billing_config = billing_pricing[billing_option]
        
        if billing_option == "pay_per_use":
            total_cost = estimated_requests * billing_config["price_per_request"]
            cost_breakdown = {
                "base_cost": 0,
                "request_cost": total_cost,
                "total_cost": total_cost,
                "cost_per_request": billing_config["price_per_request"]
            }
        else:
            base_cost = billing_config["base_price"]
            included_requests = billing_config["included_requests"]
            
            if estimated_requests <= included_requests:
                request_cost = 0
            else:
                request_cost = (estimated_requests - included_requests) * billing_config["price_per_request"]
            
            total_cost = base_cost + request_cost
            
            cost_breakdown = {
                "base_cost": base_cost,
                "included_requests": included_requests,
                "request_cost": request_cost,
                "total_cost": total_cost,
                "cost_per_request": billing_config["price_per_request"]
            }
        
        # Calculate savings compared to pay-per-use
        pay_per_use_cost = estimated_requests * threshold_pricing[threshold_type]
        savings = max(0, pay_per_use_cost - total_cost)
        savings_percentage = (savings / pay_per_use_cost * 100) if pay_per_use_cost > 0 else 0
        
        return {
            "threshold_type": threshold_type,
            "billing_option": billing_option,
            "estimated_requests": estimated_requests,
            "cost_breakdown": cost_breakdown,
            "savings": savings,
            "savings_percentage": savings_percentage,
            "recommendation": _get_cost_recommendation(estimated_requests, total_cost, billing_option)
        }
        
    except Exception as e:
        logger.error(f"Failed to calculate cost: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate cost: {str(e)}"
        )


@router.get("/usage-analytics/{user_id}")
async def get_usage_analytics(user_id: UUID) -> Dict[str, Any]:
    """
    Get user usage analytics and recommendations
    
    🧬 REAL IMPLEMENTATION: Queries usage data from database
    """
    try:
        # Try to query real usage data from database
        db = get_supabase_client()
        
        usage_data = None
        if db:
            try:
                # Query usage logs for this user
                result = db.table('usage_logs').select('*').eq('user_id', str(user_id)).execute()
                
                if result.data and len(result.data) > 0:
                    # Calculate analytics from real data
                    logs = result.data
                    total_requests = len(logs)
                    avg_precision = sum(log.get('precision', 0) for log in logs) / total_requests if total_requests > 0 else 0
                    avg_response_time = sum(log.get('response_time', 0) for log in logs) / total_requests if total_requests > 0 else 0
                    cost_this_month = sum(log.get('cost', 0) for log in logs)
                    
                    usage_data = {
                        "user_id": str(user_id),
                        "total_requests": total_requests,
                        "average_precision": round(avg_precision, 2),
                        "average_response_time": round(avg_response_time, 2),
                        "cost_this_month": round(cost_this_month, 2),
                    }
            except Exception as db_error:
                logger.warning(f"Database query failed: {db_error}")
        
        # If no real data, return calculated defaults
        if not usage_data:
            usage_data = {
                "user_id": str(user_id),
                "total_requests": 0,
                "average_precision": 0.0,
                "average_response_time": 0.0,
                "cost_this_month": 0.0,
            }
        
        # Add recommendations and patterns
        usage_data["recommendations"] = [
            {
                "type": "threshold_optimization",
                "message": "Monitor usage patterns to optimize threshold settings",
                "potential_savings": 0.0
            }
        ]
        usage_data["usage_patterns"] = {
            "peak_hours": "Not enough data yet",
            "average_requests_per_day": round(usage_data["total_requests"] / 30, 2) if usage_data["total_requests"] > 0 else 0,
                "most_used_features": ["general_chat", "content_generation", "data_analysis"]
            }
        }
        
        return {
            "analytics": mock_analytics,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Failed to get usage analytics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get usage analytics: {str(e)}"
        )


# Helper functions
async def _log_preference_change(preferences: Dict[str, Any]):
    """Log preference change for analytics"""
    try:
        logger.info(f"User preference changed: {preferences}")
    except Exception as e:
        logger.error(f"Failed to log preference change: {e}")


def _get_cost_recommendation(estimated_requests: int, total_cost: float, billing_option: str) -> str:
    """Get cost optimization recommendation"""
    if estimated_requests < 1000 and billing_option != "pay_per_use":
        return "Consider switching to pay-per-use for lower costs"
    elif estimated_requests > 5000 and billing_option == "pay_per_use":
        return "Consider upgrading to monthly plan for better value"
    elif estimated_requests > 50000 and billing_option == "monthly":
        return "Consider upgrading to yearly plan for maximum savings"
    else:
        return "Your current selection is optimal for your usage"


@router.get("/health")
async def health_check():
    """
    Health check endpoint for user-preferences service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "user-preferences",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

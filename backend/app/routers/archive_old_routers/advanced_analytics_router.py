"""
Advanced Analytics Router for Cognomega AI
API endpoints for deep performance insights and analytics
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.core.advanced_analytics import (
    advanced_analytics_engine,
    get_comprehensive_analytics,
    get_performance_insights
)
from app.core.ai_optimization_engine import (
    ai_optimization_engine,
    get_ai_optimization_recommendations,
    get_ai_performance_predictions
)
from app.core.predictive_scaling import (
    predictive_scaling_engine,
    get_scaling_recommendations
)
from app.core.dependencies import get_current_user

# Alias for compatibility
get_current_active_user = get_current_user

logger = structlog.get_logger()
router = APIRouter()


@router.get("/comprehensive", response_model=Dict[str, Any], summary="Get Comprehensive Analytics Report")
async def get_comprehensive_analytics_report(current_user: Any = Depends(get_current_user)):
    """
    Get comprehensive analytics report including system health score,
    performance insights, optimization recommendations, and trend analysis.
    Requires authentication.
    """
    try:
        logger.info("Fetching comprehensive analytics report", user_id=current_user.id)
        
        # Get comprehensive analytics
        analytics = await get_comprehensive_analytics()
        
        # Get AI optimization recommendations
        ai_recommendations = await get_ai_optimization_recommendations()
        
        # Get predictive scaling recommendations
        scaling_recommendations = await get_scaling_recommendations()
        
        # Combine all analytics
        comprehensive_report = {
            **analytics,
            "ai_optimization": ai_recommendations,
            "predictive_scaling": scaling_recommendations,
            "generated_at": datetime.now().isoformat(),
            "user_id": current_user.id
        }
        
        return comprehensive_report
        
    except Exception as e:
        logger.error("Comprehensive analytics report error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate comprehensive analytics report: {str(e)}"
        )


@router.get("/insights", response_model=List[Dict[str, Any]], summary="Get Performance Insights")
async def get_performance_insights_endpoint(
    hours: int = Query(6, description="Number of hours to look back for insights"),
    severity: Optional[str] = Query(None, description="Filter by severity level"),
    insight_type: Optional[str] = Query(None, description="Filter by insight type"),
    current_user: Any = Depends(get_current_user)
):
    """
    Get recent performance insights with optional filtering by severity and type.
    Requires authentication.
    """
    try:
        logger.info("Fetching performance insights", 
                   user_id=current_user.id, 
                   hours=hours, 
                   severity=severity, 
                   insight_type=insight_type)
        
        # Get insights
        insights = await get_performance_insights()
        
        # Filter by time window
        cutoff_time = datetime.now() - timedelta(hours=hours)
        filtered_insights = [
            insight for insight in insights 
            if datetime.fromisoformat(insight["timestamp"]) > cutoff_time
        ]
        
        # Filter by severity if provided
        if severity:
            filtered_insights = [
                insight for insight in filtered_insights 
                if insight["severity"] == severity.lower()
            ]
        
        # Filter by insight type if provided
        if insight_type:
            filtered_insights = [
                insight for insight in filtered_insights 
                if insight["type"] == insight_type.lower()
            ]
        
        return filtered_insights
        
    except Exception as e:
        logger.error("Performance insights error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch performance insights: {str(e)}"
        )


@router.get("/health-score", response_model=Dict[str, Any], summary="Get System Health Score")
async def get_system_health_score(current_user: Any = Depends(get_current_active_user)):
    """
    Get current system health score and detailed health metrics.
    Requires authentication.
    """
    try:
        logger.info("Fetching system health score", user_id=current_user.id)
        
        # Get comprehensive analytics
        analytics = await get_comprehensive_analytics()
        
        health_data = {
            "system_health_score": analytics.get("system_health_score", 0),
            "insights_summary": analytics.get("insights_summary", {}),
            "performance_summary": analytics.get("performance_summary", {}),
            "generated_at": datetime.now().isoformat(),
            "user_id": current_user.id
        }
        
        return health_data
        
    except Exception as e:
        logger.error("System health score error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to calculate system health score: {str(e)}"
        )


@router.get("/ai-optimization", response_model=Dict[str, Any], summary="Get AI Optimization Recommendations")
async def get_ai_optimization_endpoint(current_user: Any = Depends(get_current_active_user)):
    """
    Get AI-driven optimization recommendations with confidence scores.
    Requires authentication.
    """
    try:
        logger.info("Fetching AI optimization recommendations", user_id=current_user.id)
        
        recommendations = await get_ai_optimization_recommendations()
        
        return {
            **recommendations,
            "generated_at": datetime.now().isoformat(),
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error("AI optimization recommendations error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch AI optimization recommendations: {str(e)}"
        )


@router.get("/ai-predictions", response_model=Dict[str, Any], summary="Get AI Performance Predictions")
async def get_ai_predictions_endpoint(current_user: Any = Depends(get_current_active_user)):
    """
    Get AI predictions for future performance metrics.
    Requires authentication.
    """
    try:
        logger.info("Fetching AI performance predictions", user_id=current_user.id)
        
        predictions = await get_ai_performance_predictions()
        
        return {
            **predictions,
            "generated_at": datetime.now().isoformat(),
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error("AI performance predictions error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch AI performance predictions: {str(e)}"
        )


@router.get("/predictive-scaling", response_model=Dict[str, Any], summary="Get Predictive Scaling Recommendations")
async def get_predictive_scaling_endpoint(current_user: Any = Depends(get_current_active_user)):
    """
    Get predictive scaling recommendations based on load forecasting.
    Requires authentication.
    """
    try:
        logger.info("Fetching predictive scaling recommendations", user_id=current_user.id)
        
        recommendations = await get_scaling_recommendations()
        
        return {
            **recommendations,
            "generated_at": datetime.now().isoformat(),
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error("Predictive scaling recommendations error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch predictive scaling recommendations: {str(e)}"
        )


@router.get("/trends", response_model=Dict[str, Any], summary="Get Performance Trends")
async def get_performance_trends_endpoint(current_user: Any = Depends(get_current_active_user)):
    """
    Get performance trend analysis for key metrics.
    Requires authentication.
    """
    try:
        logger.info("Fetching performance trends", user_id=current_user.id)
        
        # Get comprehensive analytics
        analytics = await get_comprehensive_analytics()
        
        trends_data = {
            "trend_analysis": analytics.get("trend_analysis", {}),
            "data_points_analyzed": analytics.get("data_points_analyzed", 0),
            "generated_at": datetime.now().isoformat(),
            "user_id": current_user.id
        }
        
        return trends_data
        
    except Exception as e:
        logger.error("Performance trends error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch performance trends: {str(e)}"
        )


@router.get("/anomalies", response_model=List[Dict[str, Any]], summary="Get Detected Anomalies")
async def get_detected_anomalies_endpoint(
    hours: int = Query(24, description="Number of hours to look back for anomalies"),
    current_user: Any = Depends(get_current_user)
):
    """
    Get detected performance anomalies with severity and impact analysis.
    Requires authentication.
    """
    try:
        logger.info("Fetching detected anomalies", user_id=current_user.id, hours=hours)
        
        # Get insights filtered for anomalies
        insights = await get_performance_insights()
        
        # Filter for anomalies in the specified time window
        cutoff_time = datetime.now() - timedelta(hours=hours)
        anomaly_insights = [
            insight for insight in insights 
            if (insight["type"] == "anomaly_detection" and 
                datetime.fromisoformat(insight["timestamp"]) > cutoff_time)
        ]
        
        return anomaly_insights
        
    except Exception as e:
        logger.error("Detected anomalies error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch detected anomalies: {str(e)}"
        )


@router.get("/optimization-opportunities", response_model=List[Dict[str, Any]], summary="Get Optimization Opportunities")
async def get_optimization_opportunities_endpoint(current_user: Any = Depends(get_current_active_user)):
    """
    Get identified optimization opportunities with impact and effort analysis.
    Requires authentication.
    """
    try:
        logger.info("Fetching optimization opportunities", user_id=current_user.id)
        
        # Get insights filtered for optimization opportunities
        insights = await get_performance_insights()
        
        # Filter for optimization opportunities
        optimization_insights = [
            insight for insight in insights 
            if insight["type"] == "optimization_opportunity"
        ]
        
        return optimization_insights
        
    except Exception as e:
        logger.error("Optimization opportunities error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch optimization opportunities: {str(e)}"
        )


@router.get("/performance-summary", response_model=Dict[str, Any], summary="Get Performance Summary")
async def get_performance_summary_endpoint(current_user: Any = Depends(get_current_active_user)):
    """
    Get current performance summary with key metrics.
    Requires authentication.
    """
    try:
        logger.info("Fetching performance summary", user_id=current_user.id)
        
        # Get comprehensive analytics
        analytics = await get_comprehensive_analytics()
        
        summary_data = {
            "performance_metrics": analytics.get("performance_summary", {}),
            "system_health_score": analytics.get("system_health_score", 0),
            "insights_count": analytics.get("insights_summary", {}).get("total_insights", 0),
            "generated_at": datetime.now().isoformat(),
            "user_id": current_user.id
        }
        
        return summary_data
        
    except Exception as e:
        logger.error("Performance summary error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch performance summary: {str(e)}"
        )


@router.post("/trigger-analysis", response_model=Dict[str, Any], summary="Trigger Manual Analysis")
async def trigger_manual_analysis(current_user: Any = Depends(get_current_active_user)):
    """
    Trigger manual analysis to generate fresh insights and recommendations.
    Requires authentication.
    """
    try:
        logger.info("Triggering manual analysis", user_id=current_user.id)
        
        # Trigger insight generation
        await advanced_analytics_engine._generate_insights()
        
        # Get updated analytics
        analytics = await get_comprehensive_analytics()
        
        return {
            "message": "Manual analysis completed successfully",
            "insights_generated": analytics.get("insights_summary", {}).get("total_insights", 0),
            "system_health_score": analytics.get("system_health_score", 0),
            "generated_at": datetime.now().isoformat(),
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error("Manual analysis trigger error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger manual analysis: {str(e)}"
        )


@router.get("/data-points", response_model=Dict[str, Any], summary="Get Analytics Data Points")
async def get_analytics_data_points_endpoint(
    hours: int = Query(24, description="Number of hours of data to retrieve"),
    current_user: Any = Depends(get_current_user)
):
    """
    Get raw analytics data points for custom analysis.
    Requires authentication.
    """
    try:
        logger.info("Fetching analytics data points", user_id=current_user.id, hours=hours)
        
        # Get data points within the specified time window
        cutoff_time = datetime.now() - timedelta(hours=hours)
        filtered_data = [
            dp for dp in advanced_analytics_engine.performance_data
            if datetime.fromisoformat(dp["timestamp"]) > cutoff_time
        ]
        
        return {
            "data_points": filtered_data,
            "count": len(filtered_data),
            "time_window_hours": hours,
            "generated_at": datetime.now().isoformat(),
            "user_id": current_user.id
        }
        
    except Exception as e:
        logger.error("Analytics data points error", user_id=current_user.id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch analytics data points: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint for advanced-analytics service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "advanced-analytics",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

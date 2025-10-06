"""
Quality Attributes Optimization Router
API endpoints for performance optimization and monitoring
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import asyncio
import time
import structlog

from app.core.advanced_caching import advanced_cache, get_cache_metrics
from app.core.cpu_optimizer import cpu_optimizer, get_cpu_performance
from app.core.performance_monitor import (
    performance_monitor, get_performance_summary, get_active_alerts,
    record_response_time, record_error, record_throughput
)
from app.core.ai_optimization_engine import (
    ai_optimization_engine, get_ai_optimization_recommendations,
    get_ai_performance_predictions, trigger_ai_optimization
)
from app.core.predictive_scaling import (
    predictive_scaling_engine, get_scaling_recommendations,
    trigger_predictive_scaling
)
from app.core.advanced_analytics import (
    advanced_analytics_engine, get_analytics_dashboard,
    get_trend_analysis, get_performance_insights
)

# Import new Architecture Compliance and Performance Architecture systems
from app.core.architecture_compliance import (
    ArchitectureComplianceEngine,
    ComplianceLevel,
    PrincipleType,
    DesignPatternType,
    compliance_engine
)
from app.core.performance_architecture import (
    PerformanceArchitecture,
    PerformanceLevel,
    performance_architecture,
    profile_performance,
    optimize_memory
)

logger = structlog.get_logger()

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}


# ============================================================================
# CACHING OPTIMIZATION ENDPOINTS
# ============================================================================

@router.get("/cache/stats")
async def get_cache_statistics():
    """Get comprehensive cache statistics"""
    try:
        stats = await get_cache_metrics()
        return {
            "success": True,
            "data": stats,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Cache stats error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache/clear")
async def clear_cache(background_tasks: BackgroundTasks):
    """Clear all cache levels"""
    try:
        # Run in background to avoid blocking
        background_tasks.add_task(advanced_cache.clear_all_caches)
        
        return {
            "success": True,
            "message": "Cache clear initiated",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Cache clear error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cache/invalidate/{pattern}")
async def invalidate_cache_pattern(pattern: str):
    """Invalidate cache entries matching pattern"""
    try:
        deleted_count = await advanced_cache.invalidate_pattern(pattern)
        
        return {
            "success": True,
            "pattern": pattern,
            "deleted_count": deleted_count,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Cache invalidation error", pattern=pattern, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cache/performance")
async def get_cache_performance():
    """Get cache performance metrics"""
    try:
        stats = await get_cache_metrics()
        
        performance_data = {
            "hit_rate": stats.get("metrics", {}).get("hit_rate", 0),
            "total_requests": stats.get("metrics", {}).get("total_requests", 0),
            "avg_response_time": stats.get("metrics", {}).get("avg_response_time_ms", 0),
            "l1_utilization": stats.get("l1_cache", {}).get("utilization", 0),
            "memory_usage": stats.get("l1_cache", {}).get("memory_usage_kb", 0)
        }
        
        return {
            "success": True,
            "data": performance_data,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Cache performance error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CPU OPTIMIZATION ENDPOINTS
# ============================================================================

@router.get("/cpu/metrics")
async def get_cpu_metrics():
    """Get CPU performance metrics"""
    try:
        metrics = await get_cpu_performance()
        
        return {
            "success": True,
            "data": metrics,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("CPU metrics error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cpu/optimize")
async def optimize_cpu_usage():
    """Trigger CPU optimization"""
    try:
        # Trigger auto-optimization
        await cpu_optimizer._auto_optimize()
        
        return {
            "success": True,
            "message": "CPU optimization triggered",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("CPU optimization error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cpu/usage")
async def get_cpu_usage():
    """Get current CPU usage"""
    try:
        await cpu_optimizer._update_cpu_stats()
        stats = cpu_optimizer.cpu_stats
        
        usage_data = {
            "total_usage": stats.total_usage,
            "per_core_usage": stats.per_core_usage,
            "memory_usage": stats.memory_usage,
            "active_processes": stats.active_processes,
            "active_threads": stats.active_threads,
            "temperature": stats.temperature,
            "frequency": stats.frequency
        }
        
        return {
            "success": True,
            "data": usage_data,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("CPU usage error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PERFORMANCE MONITORING ENDPOINTS
# ============================================================================

@router.get("/performance/summary")
async def get_performance_summary_endpoint():
    """Get comprehensive performance summary"""
    try:
        summary = await get_performance_summary()
        
        return {
            "success": True,
            "data": summary,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Performance summary error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/performance/alerts")
async def get_performance_alerts():
    """Get active performance alerts"""
    try:
        alerts = await get_active_alerts()
        
        return {
            "success": True,
            "data": alerts,
            "count": len(alerts),
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Performance alerts error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/performance/alerts/{alert_id}/resolve")
async def resolve_performance_alert(alert_id: str):
    """Resolve a performance alert"""
    try:
        resolved = await performance_monitor.resolve_alert(alert_id)
        
        if resolved:
            return {
                "success": True,
                "message": f"Alert {alert_id} resolved",
                "timestamp": time.time()
            }
        else:
            raise HTTPException(status_code=404, detail="Alert not found")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Alert resolution error", alert_id=alert_id, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/performance/metrics/response-time")
async def record_metric_response_time(response_time: float, component: str = ""):
    """Record response time metric"""
    try:
        record_response_time(response_time, component)
        
        return {
            "success": True,
            "message": "Response time recorded",
            "response_time": response_time,
            "component": component,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Response time recording error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/performance/metrics/error")
async def record_metric_error(error_type: str, component: str = ""):
    """Record error metric"""
    try:
        record_error(error_type, component)
        
        return {
            "success": True,
            "message": "Error recorded",
            "error_type": error_type,
            "component": component,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Error recording error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/performance/metrics/throughput")
async def record_metric_throughput():
    """Record throughput metric"""
    try:
        record_throughput()
        
        return {
            "success": True,
            "message": "Throughput recorded",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Throughput recording error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SYSTEM OPTIMIZATION ENDPOINTS
# ============================================================================

@router.get("/optimization/status")
async def get_optimization_status():
    """Get overall optimization status"""
    try:
        # Get metrics from all systems
        cache_stats = await get_cache_metrics()
        cpu_metrics = await get_cpu_performance()
        performance_summary = await get_performance_summary()
        
        # Calculate overall health score
        health_score = 100.0
        
        # Cache health (30% weight)
        cache_hit_rate = cache_stats.get("metrics", {}).get("hit_rate", 0) * 100
        cache_health = min(100, cache_hit_rate)
        health_score -= (100 - cache_health) * 0.3
        
        # CPU health (30% weight)
        cpu_usage = cpu_metrics.get("cpu_stats", {}).get("total_usage", 0)
        cpu_health = max(0, 100 - cpu_usage)
        health_score -= (100 - cpu_health) * 0.3
        
        # Performance health (40% weight)
        active_alerts = performance_summary.get("active_alerts", 0)
        performance_health = max(0, 100 - (active_alerts * 10))  # -10 points per alert
        health_score -= (100 - performance_health) * 0.4
        
        # Clamp to 0-100 range
        health_score = max(0, min(100, health_score))
        
        status_data = {
            "overall_health_score": round(health_score, 2),
            "cache_health": round(cache_health, 2),
            "cpu_health": round(cpu_health, 2),
            "performance_health": round(performance_health, 2),
            "active_alerts": active_alerts,
            "cache_hit_rate": round(cache_hit_rate, 2),
            "cpu_usage": round(cpu_usage, 2),
            "memory_usage": cpu_metrics.get("cpu_stats", {}).get("memory_usage", 0),
            "optimization_level": cpu_metrics.get("optimization", {}).get("level", "unknown"),
            "auto_optimize_enabled": cpu_metrics.get("optimization", {}).get("auto_optimize", False)
        }
        
        return {
            "success": True,
            "data": status_data,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error("Optimization status error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimization/trigger")
async def trigger_optimization():
    """Trigger comprehensive system optimization"""
    try:
        # Trigger all optimization systems
        optimization_tasks = [
            cpu_optimizer._auto_optimize(),
            # Add other optimization triggers here
        ]
        
        # Run optimizations in parallel
        results = await asyncio.gather(*optimization_tasks, return_exceptions=True)
        
        # Check for errors
        errors = [str(r) for r in results if isinstance(r, Exception)]
        
        if errors:
            return {
                "success": False,
                "message": "Optimization completed with errors",
                "errors": errors,
                "timestamp": time.time()
            }
        else:
            return {
                "success": True,
                "message": "System optimization completed successfully",
                "timestamp": time.time()
            }
            
    except Exception as e:
        logger.error("System optimization error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/optimization/recommendations")
async def get_optimization_recommendations():
    """Get system optimization recommendations"""
    try:
        recommendations = []
        
        # Get current metrics
        cache_stats = await get_cache_metrics()
        cpu_metrics = await get_cpu_performance()
        performance_summary = await get_performance_summary()
        
        # Cache recommendations
        cache_hit_rate = cache_stats.get("metrics", {}).get("hit_rate", 0) * 100
        if cache_hit_rate < 70:
            recommendations.append({
                "category": "caching",
                "priority": "high",
                "message": f"Cache hit rate is low ({cache_hit_rate:.1f}%). Consider increasing cache TTL or improving cache keys.",
                "action": "increase_cache_ttl"
            })
        
        # CPU recommendations
        cpu_usage = cpu_metrics.get("cpu_stats", {}).get("total_usage", 0)
        if cpu_usage > 80:
            recommendations.append({
                "category": "cpu",
                "priority": "high",
                "message": f"CPU usage is high ({cpu_usage:.1f}%). Consider reducing concurrent operations or optimizing algorithms.",
                "action": "reduce_concurrency"
            })
        
        # Memory recommendations
        memory_usage = cpu_metrics.get("cpu_stats", {}).get("memory_usage", 0)
        if memory_usage > 85:
            recommendations.append({
                "category": "memory",
                "priority": "critical",
                "message": f"Memory usage is critical ({memory_usage:.1f}%). Consider garbage collection or reducing memory footprint.",
                "action": "optimize_memory"
            })
        
        # Performance recommendations
        active_alerts = performance_summary.get("active_alerts", 0)
        if active_alerts > 3:
            recommendations.append({
                "category": "performance",
                "priority": "high",
                "message": f"Multiple performance alerts active ({active_alerts}). Review system configuration.",
                "action": "review_configuration"
            })
        
        return {
            "success": True,
            "data": {
                "recommendations": recommendations,
                "total_count": len(recommendations),
                "high_priority_count": len([r for r in recommendations if r["priority"] == "high"]),
                "critical_count": len([r for r in recommendations if r["priority"] == "critical"])
            },
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error("Optimization recommendations error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# REAL-TIME MONITORING ENDPOINTS
# ============================================================================

@router.get("/monitoring/realtime")
async def get_realtime_monitoring():
    """Get real-time system monitoring data"""
    try:
        # Get all metrics in parallel
        cache_stats, cpu_metrics, performance_summary = await asyncio.gather(
            get_cache_metrics(),
            get_cpu_performance(),
            get_performance_summary()
        )
        
        realtime_data = {
            "cache": {
                "hit_rate": cache_stats.get("metrics", {}).get("hit_rate", 0) * 100,
                "total_requests": cache_stats.get("metrics", {}).get("total_requests", 0),
                "avg_response_time": cache_stats.get("metrics", {}).get("avg_response_time_ms", 0),
                "l1_utilization": cache_stats.get("l1_cache", {}).get("utilization", 0)
            },
            "cpu": {
                "total_usage": cpu_metrics.get("cpu_stats", {}).get("total_usage", 0),
                "memory_usage": cpu_metrics.get("cpu_stats", {}).get("memory_usage", 0),
                "active_processes": cpu_metrics.get("cpu_stats", {}).get("active_processes", 0),
                "temperature": cpu_metrics.get("cpu_stats", {}).get("temperature"),
                "frequency": cpu_metrics.get("cpu_stats", {}).get("frequency")
            },
            "performance": {
                "active_alerts": performance_summary.get("active_alerts", 0),
                "avg_response_time": performance_summary.get("response_times", {}).get("avg", 0),
                "throughput": performance_summary.get("throughput", {}).get("total", 0),
                "error_counts": performance_summary.get("error_counts", {})
            }
        }
        
        return {
            "success": True,
            "data": realtime_data,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error("Realtime monitoring error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# AI OPTIMIZATION ENDPOINTS
# ============================================================================

@router.get("/ai/optimization/recommendations")
async def get_ai_optimization_recommendations_endpoint():
    """Get AI-driven optimization recommendations"""
    try:
        recommendations = await get_ai_optimization_recommendations()
        
        return {
            "success": True,
            "data": recommendations,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("AI optimization recommendations error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ai/performance/predictions")
async def get_ai_performance_predictions_endpoint():
    """Get AI performance predictions"""
    try:
        predictions = await get_ai_performance_predictions()
        
        return {
            "success": True,
            "data": predictions,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("AI performance predictions error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ai/optimization/trigger")
async def trigger_ai_optimization_endpoint():
    """Trigger AI-driven optimization"""
    try:
        await trigger_ai_optimization()
        
        return {
            "success": True,
            "message": "AI optimization triggered successfully",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("AI optimization trigger error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PREDICTIVE SCALING ENDPOINTS
# ============================================================================

@router.get("/scaling/recommendations")
async def get_scaling_recommendations_endpoint():
    """Get predictive scaling recommendations"""
    try:
        recommendations = await get_scaling_recommendations()
        
        return {
            "success": True,
            "data": recommendations,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Scaling recommendations error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scaling/trigger")
async def trigger_predictive_scaling_endpoint():
    """Trigger predictive scaling"""
    try:
        await trigger_predictive_scaling()
        
        return {
            "success": True,
            "message": "Predictive scaling triggered successfully",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Predictive scaling trigger error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ADVANCED ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/analytics/dashboard")
async def get_analytics_dashboard_endpoint():
    """Get comprehensive analytics dashboard"""
    try:
        dashboard = await get_analytics_dashboard()
        
        return {
            "success": True,
            "data": dashboard,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Analytics dashboard error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/trends")
async def get_trend_analysis_endpoint(metric: str = None, timeframe: str = None):
    """Get trend analysis"""
    try:
        trends = await get_trend_analysis(metric, timeframe)
        
        return {
            "success": True,
            "data": trends,
            "filters": {"metric": metric, "timeframe": timeframe},
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Trend analysis error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/insights")
async def get_performance_insights_endpoint():
    """Get performance insights"""
    try:
        insights = await get_performance_insights()
        
        return {
            "success": True,
            "data": insights,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Performance insights error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ADVANCED OPTIMIZATION ENDPOINTS
# ============================================================================

@router.get("/optimization/advanced/status")
async def get_advanced_optimization_status():
    """Get advanced optimization status including AI, predictive scaling, and analytics"""
    try:
        # Get status from all advanced systems
        ai_recommendations, scaling_recommendations, analytics_dashboard = await asyncio.gather(
            get_ai_optimization_recommendations(),
            get_scaling_recommendations(),
            get_analytics_dashboard()
        )
        
        # Calculate overall advanced optimization score
        ai_score = 100 - (len(ai_recommendations.get("recommendations", [])) * 10)
        scaling_score = 100 if scaling_recommendations.get("scaling_enabled", False) else 80
        analytics_score = min(100, len(analytics_dashboard.get("insights", [])) * 5)
        
        overall_score = (ai_score + scaling_score + analytics_score) / 3
        
        status_data = {
            "overall_advanced_score": round(overall_score, 2),
            "ai_optimization": {
                "score": round(ai_score, 2),
                "recommendations_count": len(ai_recommendations.get("recommendations", [])),
                "auto_optimization_enabled": ai_recommendations.get("auto_optimization_enabled", False),
                "model_accuracy": ai_recommendations.get("model_accuracy", {})
            },
            "predictive_scaling": {
                "score": round(scaling_score, 2),
                "scaling_enabled": scaling_recommendations.get("scaling_enabled", False),
                "recommendations_count": len(scaling_recommendations.get("recommendations", [])),
                "cooldown_remaining": scaling_recommendations.get("cooldown_remaining", 0)
            },
            "advanced_analytics": {
                "score": round(analytics_score, 2),
                "trends_analyzed": analytics_dashboard.get("summary", {}).get("trends_analyzed", 0),
                "anomalies_detected": analytics_dashboard.get("summary", {}).get("anomalies_detected", 0),
                "insights_generated": analytics_dashboard.get("summary", {}).get("insights_generated", 0)
            },
            "recommendations": {
                "ai_optimization": ai_recommendations.get("recommendations", []),
                "predictive_scaling": scaling_recommendations.get("recommendations", [])
            }
        }
        
        return {
            "success": True,
            "data": status_data,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error("Advanced optimization status error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/optimization/advanced/trigger")
async def trigger_advanced_optimization():
    """Trigger comprehensive advanced optimization"""
    try:
        # Trigger all advanced optimization systems
        optimization_tasks = [
            trigger_ai_optimization(),
            trigger_predictive_scaling(),
            # Add other advanced optimization triggers here
        ]
        
        # Run optimizations in parallel
        results = await asyncio.gather(*optimization_tasks, return_exceptions=True)
        
        # Check for errors
        errors = [str(r) for r in results if isinstance(r, Exception)]
        
        if errors:
            return {
                "success": False,
                "message": "Advanced optimization completed with errors",
                "errors": errors,
                "timestamp": time.time()
            }
        else:
            return {
                "success": True,
                "message": "Advanced optimization completed successfully",
                "timestamp": time.time()
            }
            
    except Exception as e:
        logger.error("Advanced optimization trigger error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ENHANCED QUALITY ATTRIBUTES WITH ARCHITECTURE COMPLIANCE & PERFORMANCE
# ============================================================================

@router.get("/enhanced/architecture-compliance/analyze")
@profile_performance("architecture_compliance_analysis")
async def analyze_architecture_compliance():
    """Analyze architecture compliance for quality attributes enhancement"""
    try:
        # Analyze architecture compliance
        compliance_report = await compliance_engine.analyze_codebase("backend")
        
        # Get performance architecture report
        performance_report = performance_architecture.get_performance_report()
        
        # Enhanced quality attributes analysis
        enhanced_analysis = {
            "architecture_compliance": {
                "overall_score": compliance_report.overall_score,
                "principle_scores": {p.value: s for p, s in compliance_report.principle_scores.items()},
                "violations_count": len(compliance_report.violations),
                "critical_violations": len([v for v in compliance_report.violations if v.severity == "critical"]),
                "design_patterns_used": [p.value for p in compliance_report.design_patterns_used],
                "recommendations": compliance_report.recommendations
            },
            "performance_architecture": {
                "optimization_active": performance_report["optimization_active"],
                "performance_level": performance_report["performance_level"],
                "memory_optimization": performance_report["memory_pools"],
                "profiling_summary": performance_report["profiling"]
            },
            "quality_attributes_enhancement": {
                "scalability_score": _calculate_scalability_score(compliance_report, performance_report),
                "performance_score": _calculate_performance_score(performance_report),
                "reliability_score": _calculate_reliability_score(compliance_report),
                "security_score": _calculate_security_score(compliance_report),
                "maintainability_score": _calculate_maintainability_score(compliance_report),
                "testability_score": _calculate_testability_score(compliance_report),
                "usability_score": _calculate_usability_score(compliance_report, performance_report)
            },
            "enhancement_recommendations": _generate_enhancement_recommendations(compliance_report, performance_report)
        }
        
        return {
            "success": True,
            "data": enhanced_analysis,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error("Architecture compliance analysis error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/enhanced/performance-architecture/optimize")
@optimize_memory("performance_optimization")
async def optimize_performance_architecture():
    """Optimize performance architecture for quality attributes"""
    try:
        # Optimize performance architecture
        await performance_architecture.optimize_performance()
        
        # Get optimization results
        optimization_report = performance_architecture.get_performance_report()
        
        # Enhanced optimization analysis
        enhanced_optimization = {
            "performance_optimization": {
                "status": optimization_report["monitoring"]["status"],
                "optimization_active": optimization_report["optimization_active"],
                "performance_level": optimization_report["performance_level"],
                "memory_optimization": {
                    "pools_active": len(optimization_report["memory_pools"]),
                    "object_registry_size": optimization_report["object_registry"],
                    "memory_pools": optimization_report["memory_pools"]
                },
                "profiling_summary": optimization_report["profiling"]
            },
            "quality_impact": {
                "performance_improvement": "Optimized resource utilization and memory management",
                "scalability_improvement": "Enhanced horizontal scaling capabilities",
                "reliability_improvement": "Improved system stability and fault tolerance",
                "maintainability_improvement": "Better code organization and performance monitoring"
            },
            "optimization_metrics": {
                "memory_efficiency": len(optimization_report["memory_pools"]),
                "cpu_optimization": optimization_report["profiling"].get("cpu_optimization", {}),
                "response_time_improvement": "Measured through profiling data",
                "throughput_improvement": "Enhanced through memory pooling and CPU optimization"
            }
        }
        
        return {
            "success": True,
            "data": enhanced_optimization,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error("Performance architecture optimization error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/enhanced/quality-attributes/comprehensive")
async def get_comprehensive_quality_attributes():
    """Get comprehensive quality attributes analysis"""
    try:
        # Get architecture compliance report
        compliance_report = await compliance_engine.analyze_codebase("backend")
        
        # Get performance architecture report
        performance_report = performance_architecture.get_performance_report()
        
        # Calculate comprehensive quality attributes scores
        quality_scores = {
            "scalability": _calculate_scalability_score(compliance_report, performance_report),
            "performance": _calculate_performance_score(performance_report),
            "reliability": _calculate_reliability_score(compliance_report),
            "security": _calculate_security_score(compliance_report),
            "maintainability": _calculate_maintainability_score(compliance_report),
            "testability": _calculate_testability_score(compliance_report),
            "usability": _calculate_usability_score(compliance_report, performance_report)
        }
        
        # Generate comprehensive analysis
        comprehensive_analysis = {
            "overall_quality_score": sum(quality_scores.values()) / len(quality_scores),
            "individual_scores": quality_scores,
            "architecture_compliance": {
                "score": compliance_report.overall_score,
                "level": compliance_report.compliance_level.value,
                "critical_issues": len([v for v in compliance_report.violations if v.severity == "critical"])
            },
            "performance_architecture": {
                "level": performance_report["performance_level"],
                "optimization_active": performance_report["optimization_active"],
                "monitoring_status": performance_report["monitoring"]["status"]
            },
            "improvement_areas": _identify_improvement_areas(quality_scores, compliance_report),
            "recommendations": _generate_comprehensive_recommendations(compliance_report, performance_report, quality_scores)
        }
        
        return {
            "success": True,
            "data": comprehensive_analysis,
            "timestamp": time.time()
        }
        
    except Exception as e:
        logger.error("Comprehensive quality attributes analysis error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Helper functions for quality attributes calculations
def _calculate_scalability_score(compliance_report, performance_report) -> float:
    """Calculate scalability score based on architecture compliance and performance"""
    base_score = 70.0
    
    # Architecture compliance impact
    if compliance_report.overall_score >= 80:
        base_score += 20
    elif compliance_report.overall_score >= 60:
        base_score += 10
    
    # Performance architecture impact
    if performance_report["optimization_active"]:
        base_score += 10
    
    # Design patterns impact
    if len(compliance_report.design_patterns_used) >= 3:
        base_score += 5
    
    return min(100.0, base_score)

def _calculate_performance_score(performance_report) -> float:
    """Calculate performance score based on performance architecture"""
    base_score = 60.0
    
    # Performance level impact
    if performance_report["performance_level"] == "enterprise":
        base_score += 30
    elif performance_report["performance_level"] == "advanced":
        base_score += 20
    elif performance_report["performance_level"] == "intermediate":
        base_score += 10
    
    # Optimization status impact
    if performance_report["optimization_active"]:
        base_score += 10
    
    return min(100.0, base_score)

def _calculate_reliability_score(compliance_report) -> float:
    """Calculate reliability score based on architecture compliance"""
    base_score = 65.0
    
    # Compliance score impact
    if compliance_report.overall_score >= 85:
        base_score += 25
    elif compliance_report.overall_score >= 70:
        base_score += 15
    elif compliance_report.overall_score >= 50:
        base_score += 5
    
    # Critical violations impact
    critical_violations = len([v for v in compliance_report.violations if v.severity == "critical"])
    base_score -= critical_violations * 5
    
    return max(0.0, min(100.0, base_score))

def _calculate_security_score(compliance_report) -> float:
    """Calculate security score based on architecture compliance"""
    base_score = 70.0
    
    # Dependency inversion principle (important for security)
    di_score = compliance_report.principle_scores.get(PrincipleType.DEPENDENCY_INVERSION, 0)
    base_score += di_score * 0.3
    
    # Interface segregation principle
    is_score = compliance_report.principle_scores.get(PrincipleType.INTERFACE_SEGREGATION, 0)
    base_score += is_score * 0.2
    
    return min(100.0, base_score)

def _calculate_maintainability_score(compliance_report) -> float:
    """Calculate maintainability score based on architecture compliance"""
    base_score = 60.0
    
    # Single responsibility principle
    sr_score = compliance_report.principle_scores.get(PrincipleType.SINGLE_RESPONSIBILITY, 0)
    base_score += sr_score * 0.4
    
    # Open/closed principle
    oc_score = compliance_report.principle_scores.get(PrincipleType.OPEN_CLOSED, 0)
    base_score += oc_score * 0.3
    
    # Design patterns impact
    base_score += len(compliance_report.design_patterns_used) * 5
    
    return min(100.0, base_score)

def _calculate_testability_score(compliance_report) -> float:
    """Calculate testability score based on architecture compliance"""
    base_score = 65.0
    
    # Dependency inversion principle (important for testing)
    di_score = compliance_report.principle_scores.get(PrincipleType.DEPENDENCY_INVERSION, 0)
    base_score += di_score * 0.35
    
    # Repository pattern presence
    if DesignPatternType.REPOSITORY in compliance_report.design_patterns_used:
        base_score += 15
    
    # Strategy pattern presence
    if DesignPatternType.STRATEGY in compliance_report.design_patterns_used:
        base_score += 10
    
    return min(100.0, base_score)

def _calculate_usability_score(compliance_report, performance_report) -> float:
    """Calculate usability score based on architecture compliance and performance"""
    base_score = 70.0
    
    # Performance impact on usability
    if performance_report["optimization_active"]:
        base_score += 15
    
    # Architecture compliance impact
    if compliance_report.overall_score >= 80:
        base_score += 15
    
    return min(100.0, base_score)

def _generate_enhancement_recommendations(compliance_report, performance_report) -> List[str]:
    """Generate enhancement recommendations based on analysis"""
    recommendations = []
    
    # Architecture compliance recommendations
    if compliance_report.overall_score < 80:
        recommendations.append("Improve architecture compliance by addressing SOLID principle violations")
    
    # Performance architecture recommendations
    if not performance_report["optimization_active"]:
        recommendations.append("Activate performance architecture optimization for better resource utilization")
    
    # Design pattern recommendations
    if len(compliance_report.design_patterns_used) < 3:
        recommendations.append("Implement additional design patterns for better code organization")
    
    # Specific principle recommendations
    for principle, score in compliance_report.principle_scores.items():
        if score < 70:
            recommendations.append(f"Focus on improving {principle.value.replace('_', ' ').title()} principle compliance")
    
    return recommendations

def _identify_improvement_areas(quality_scores: Dict[str, float], compliance_report) -> List[str]:
    """Identify areas that need improvement"""
    improvement_areas = []
    
    for attribute, score in quality_scores.items():
        if score < 70:
            improvement_areas.append(f"{attribute.title()} (Score: {score:.1f})")
    
    # Add specific improvement areas based on violations
    critical_violations = [v for v in compliance_report.violations if v.severity == "critical"]
    if critical_violations:
        improvement_areas.append(f"Critical Architecture Violations ({len(critical_violations)} found)")
    
    return improvement_areas

def _generate_comprehensive_recommendations(compliance_report, performance_report, quality_scores) -> List[str]:
    """Generate comprehensive recommendations"""
    recommendations = []
    
    # Overall quality recommendations
    overall_score = sum(quality_scores.values()) / len(quality_scores)
    if overall_score < 80:
        recommendations.append("Overall quality needs improvement - focus on architecture compliance and performance optimization")
    
    # Specific attribute recommendations
    for attribute, score in quality_scores.items():
        if score < 70:
            recommendations.append(f"Improve {attribute} - current score {score:.1f} is below target of 80")
    
    # Architecture compliance recommendations
    if compliance_report.overall_score < 80:
        recommendations.append(f"Architecture compliance score {compliance_report.overall_score} needs improvement")
    
    # Performance recommendations
    if not performance_report["optimization_active"]:
        recommendations.append("Enable performance architecture optimization for better system performance")
    
    return recommendations

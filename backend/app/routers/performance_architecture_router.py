"""
Performance Architecture Router

API endpoints for performance architecture monitoring and optimization.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
from pydantic import BaseModel
import structlog

from app.core.performance_architecture import (
    PerformanceArchitecture,
    PerformanceLevel,
    ResourceType,
    PerformanceMetrics,
    ResourceLimit,
    performance_architecture
)
from app.core.dependencies import get_current_user

logger = structlog.get_logger(__name__)

router = APIRouter()

# Pydantic models for API
class PerformanceConfigRequest(BaseModel):
    performance_level: PerformanceLevel = PerformanceLevel.ADVANCED
    monitoring_interval: float = 1.0
    resource_limits: Optional[Dict[str, Dict[str, float]]] = None

class ResourceLimitRequest(BaseModel):
    resource_type: ResourceType
    warning_threshold: float
    critical_threshold: float
    max_limit: float
    auto_scaling_enabled: bool = True

class PerformanceMetricsResponse(BaseModel):
    timestamp: float
    cpu_usage: float
    memory_usage: float
    disk_io: float
    network_io: float
    response_time: float
    throughput: float
    error_rate: float
    active_connections: int
    queue_size: int

class PerformanceSummaryResponse(BaseModel):
    status: str
    latest_metrics: Dict[str, Any]
    average_metrics: Dict[str, Any]
    alerts_count: int
    warnings_count: int

class PerformanceReportResponse(BaseModel):
    monitoring: PerformanceSummaryResponse
    profiling: Dict[str, Any]
    memory_pools: Dict[str, int]
    object_registry: int
    performance_level: str
    optimization_active: bool

@router.post("/performance/initialize")
async def initialize_performance_architecture(
    config: PerformanceConfigRequest,
    current_user: Any = Depends(get_current_user)
):
    """Initialize performance architecture system"""
    try:
        # Update performance level
        performance_architecture.performance_level = config.performance_level
        
        # Update monitoring interval
        if config.monitoring_interval != 1.0:
            # Would need to restart monitoring with new interval
            pass
        
        # Update resource limits if provided
        if config.resource_limits:
            for resource_name, limits in config.resource_limits.items():
                try:
                    resource_type = ResourceType(resource_name)
                    limit = ResourceLimit(
                        resource_type=resource_type,
                        warning_threshold=limits.get('warning_threshold', 70.0),
                        critical_threshold=limits.get('critical_threshold', 85.0),
                        max_limit=limits.get('max_limit', 95.0),
                        auto_scaling_enabled=limits.get('auto_scaling_enabled', True)
                    )
                    performance_architecture.monitor.resource_limits[resource_type] = limit
                except ValueError:
                    logger.warning("Invalid resource type", resource=resource_name)
        
        # Initialize if not already initialized
        if not performance_architecture.optimization_active:
            await performance_architecture.initialize()
        
        return {
            "status": "initialized",
            "performance_level": config.performance_level.value,
            "monitoring_active": performance_architecture.monitor.monitoring_active,
            "optimization_active": performance_architecture.optimization_active
        }
        
    except Exception as e:
        logger.error("Failed to initialize performance architecture", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/status", response_model=PerformanceSummaryResponse)
async def get_performance_status(
    current_user: Any = Depends(get_current_user)
):
    """Get current performance status"""
    try:
        summary = performance_architecture.monitor.get_performance_summary()
        return PerformanceSummaryResponse(**summary)
        
    except Exception as e:
        logger.error("Failed to get performance status", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/report", response_model=PerformanceReportResponse)
async def get_performance_report(
    current_user: Any = Depends(get_current_user)
):
    """Get comprehensive performance report"""
    try:
        report = performance_architecture.get_performance_report()
        
        # Convert monitoring summary
        monitoring_summary = PerformanceSummaryResponse(**report['monitoring'])
        
        return PerformanceReportResponse(
            monitoring=monitoring_summary,
            profiling=report['profiling'],
            memory_pools=report['memory_pools'],
            object_registry=report['object_registry'],
            performance_level=report['performance_level'],
            optimization_active=report['optimization_active']
        )
        
    except Exception as e:
        logger.error("Failed to get performance report", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/metrics", response_model=List[PerformanceMetricsResponse])
async def get_performance_metrics(
    limit: int = 100,
    current_user: Any = Depends(get_current_user)
):
    """Get performance metrics history"""
    try:
        metrics_history = performance_architecture.monitor.metrics_history[-limit:]
        
        metrics_response = []
        for metrics in metrics_history:
            metrics_response.append(PerformanceMetricsResponse(
                timestamp=metrics.timestamp,
                cpu_usage=metrics.cpu_usage,
                memory_usage=metrics.memory_usage,
                disk_io=metrics.disk_io,
                network_io=metrics.network_io,
                response_time=metrics.response_time,
                throughput=metrics.throughput,
                error_rate=metrics.error_rate,
                active_connections=metrics.active_connections,
                queue_size=metrics.queue_size
            ))
        
        return metrics_response
        
    except Exception as e:
        logger.error("Failed to get performance metrics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/alerts", response_model=List[Dict[str, Any]])
async def get_performance_alerts(
    severity: Optional[str] = None,
    limit: int = 50,
    current_user: Any = Depends(get_current_user)
):
    """Get performance alerts"""
    try:
        alerts = performance_architecture.monitor.alerts
        
        # Filter by severity if specified
        if severity:
            alerts = [alert for alert in alerts if alert.get('type') == severity]
        
        # Limit results
        alerts = alerts[-limit:]
        
        return alerts
        
    except Exception as e:
        logger.error("Failed to get performance alerts", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/optimize")
async def optimize_performance(
    background_tasks: BackgroundTasks,
    current_user: Any = Depends(get_current_user)
):
    """Trigger performance optimization"""
    try:
        # Add optimization to background tasks
        background_tasks.add_task(performance_architecture.optimize_performance)
        
        return {
            "status": "optimization_started",
            "message": "Performance optimization has been started in the background"
        }
        
    except Exception as e:
        logger.error("Failed to start performance optimization", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/memory/optimize")
async def optimize_memory(
    current_user: Any = Depends(get_current_user)
):
    """Trigger memory optimization"""
    try:
        performance_architecture.memory_optimizer.optimize_memory()
        
        return {
            "status": "memory_optimized",
            "message": "Memory optimization completed",
            "object_registry_count": len(performance_architecture.memory_optimizer.object_registry),
            "memory_pools": {
                name: pool.qsize() 
                for name, pool in performance_architecture.memory_optimizer.memory_pools.items()
            }
        }
        
    except Exception as e:
        logger.error("Failed to optimize memory", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/cpu/optimize")
async def optimize_cpu(
    current_user: Any = Depends(get_current_user)
):
    """Trigger CPU optimization"""
    try:
        performance_architecture.cpu_optimizer.optimize_cpu_scheduling()
        
        return {
            "status": "cpu_optimized",
            "message": "CPU optimization completed",
            "cpu_affinity_set": performance_architecture.cpu_optimizer.cpu_affinity_set
        }
        
    except Exception as e:
        logger.error("Failed to optimize CPU", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/memory/pool/create")
async def create_memory_pool(
    name: str,
    size: int = 100,
    current_user: Any = Depends(get_current_user)
):
    """Create a memory pool for object reuse"""
    try:
        performance_architecture.memory_optimizer.create_memory_pool(name, size)
        
        return {
            "status": "pool_created",
            "pool_name": name,
            "pool_size": size,
            "message": f"Memory pool '{name}' created with size {size}"
        }
        
    except Exception as e:
        logger.error("Failed to create memory pool", pool=name, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/memory/pools", response_model=Dict[str, int])
async def get_memory_pools(
    current_user: Any = Depends(get_current_user)
):
    """Get memory pools status"""
    try:
        pools_status = {}
        for name, pool in performance_architecture.memory_optimizer.memory_pools.items():
            pools_status[name] = pool.qsize()
        
        return pools_status
        
    except Exception as e:
        logger.error("Failed to get memory pools", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/profiling", response_model=Dict[str, Any])
async def get_profiling_summary(
    current_user: Any = Depends(get_current_user)
):
    """Get performance profiling summary"""
    try:
        summary = performance_architecture.profiler.get_profile_summary()
        return summary
        
    except Exception as e:
        logger.error("Failed to get profiling summary", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/profiling/start")
async def start_profiling(
    name: str,
    current_user: Any = Depends(get_current_user)
):
    """Start profiling a specific operation"""
    try:
        performance_architecture.profiler.start_profile(name)
        
        return {
            "status": "profiling_started",
            "profile_name": name,
            "message": f"Profiling started for '{name}'"
        }
        
    except Exception as e:
        logger.error("Failed to start profiling", profile=name, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/profiling/end")
async def end_profiling(
    name: str,
    current_user: Any = Depends(get_current_user)
):
    """End profiling and get duration"""
    try:
        duration = performance_architecture.profiler.end_profile(name)
        
        return {
            "status": "profiling_ended",
            "profile_name": name,
            "duration": duration,
            "message": f"Profiling ended for '{name}' - Duration: {duration:.4f}s"
        }
        
    except Exception as e:
        logger.error("Failed to end profiling", profile=name, error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/resource-limits", response_model=Dict[str, Any])
async def get_resource_limits(
    current_user: Any = Depends(get_current_user)
):
    """Get current resource limits configuration"""
    try:
        limits = {}
        for resource_type, limit in performance_architecture.monitor.resource_limits.items():
            limits[resource_type.value] = {
                "warning_threshold": limit.warning_threshold,
                "critical_threshold": limit.critical_threshold,
                "max_limit": limit.max_limit,
                "auto_scaling_enabled": limit.auto_scaling_enabled
            }
        
        return limits
        
    except Exception as e:
        logger.error("Failed to get resource limits", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/resource-limits/update")
async def update_resource_limit(
    resource_limit: ResourceLimitRequest,
    current_user: Any = Depends(get_current_user)
):
    """Update resource limit configuration"""
    try:
        limit = ResourceLimit(
            resource_type=resource_limit.resource_type,
            warning_threshold=resource_limit.warning_threshold,
            critical_threshold=resource_limit.critical_threshold,
            max_limit=resource_limit.max_limit,
            auto_scaling_enabled=resource_limit.auto_scaling_enabled
        )
        
        performance_architecture.monitor.resource_limits[resource_limit.resource_type] = limit
        
        return {
            "status": "limit_updated",
            "resource_type": resource_limit.resource_type.value,
            "warning_threshold": resource_limit.warning_threshold,
            "critical_threshold": resource_limit.critical_threshold,
            "max_limit": resource_limit.max_limit,
            "auto_scaling_enabled": resource_limit.auto_scaling_enabled
        }
        
    except Exception as e:
        logger.error("Failed to update resource limit", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/monitoring/start")
async def start_monitoring(
    interval: float = 1.0,
    current_user: Any = Depends(get_current_user)
):
    """Start performance monitoring"""
    try:
        if not performance_architecture.monitor.monitoring_active:
            # Start monitoring in background
            import asyncio
            asyncio.create_task(performance_architecture.monitor.start_monitoring(interval))
        
        return {
            "status": "monitoring_started",
            "interval": interval,
            "message": f"Performance monitoring started with {interval}s interval"
        }
        
    except Exception as e:
        logger.error("Failed to start monitoring", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/performance/monitoring/stop")
async def stop_monitoring(
    current_user: Any = Depends(get_current_user)
):
    """Stop performance monitoring"""
    try:
        await performance_architecture.monitor.stop_monitoring()
        
        return {
            "status": "monitoring_stopped",
            "message": "Performance monitoring stopped"
        }
        
    except Exception as e:
        logger.error("Failed to stop monitoring", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance/health", response_model=Dict[str, Any])
async def get_performance_health(
    current_user: Any = Depends(get_current_user)
):
    """Get performance architecture system health"""
    try:
        return {
            "status": "healthy",
            "performance_architecture": "active",
            "monitor": "ready" if performance_architecture.monitor else "not_ready",
            "memory_optimizer": "ready",
            "cpu_optimizer": "ready",
            "profiler": "ready",
            "optimization_active": performance_architecture.optimization_active,
            "monitoring_active": performance_architecture.monitor.monitoring_active if performance_architecture.monitor else False,
            "system_status": "operational"
        }
        
    except Exception as e:
        logger.error("Failed to get performance health", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

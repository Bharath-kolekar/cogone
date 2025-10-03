"""
Hardware Resource Optimization API endpoints
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import Dict, List, Optional, Any
from datetime import datetime
from app.core.hardware_optimization import hardware_optimizer, ResourceType, OptimizationLevel

logger = structlog.get_logger()
router = APIRouter()


@router.get("/resources/current")
async def get_current_resources():
    """Get current system resource usage"""
    try:
        resources = await hardware_optimizer.get_system_resources()
        return {
            "resources": resources,
            "timestamp": datetime.now(),
            "status": "success"
        }
    except Exception as e:
        logger.error("Failed to get current resources", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get current resources: {e}"
        )


@router.get("/resources/cpu")
async def get_cpu_metrics():
    """Get CPU-specific metrics"""
    try:
        resources = await hardware_optimizer.get_system_resources()
        cpu_metrics = resources.get("cpu")
        
        if not cpu_metrics:
            raise HTTPException(status_code=404, detail="CPU metrics not available")
        
        return {
            "cpu_metrics": cpu_metrics,
            "timestamp": datetime.now(),
            "status": "success"
        }
    except Exception as e:
        logger.error("Failed to get CPU metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get CPU metrics: {e}"
        )


@router.get("/resources/memory")
async def get_memory_metrics():
    """Get memory-specific metrics"""
    try:
        resources = await hardware_optimizer.get_system_resources()
        memory_metrics = resources.get("memory")
        
        if not memory_metrics:
            raise HTTPException(status_code=404, detail="Memory metrics not available")
        
        return {
            "memory_metrics": memory_metrics,
            "timestamp": datetime.now(),
            "status": "success"
        }
    except Exception as e:
        logger.error("Failed to get memory metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get memory metrics: {e}"
        )


@router.get("/resources/disk")
async def get_disk_metrics():
    """Get disk-specific metrics"""
    try:
        resources = await hardware_optimizer.get_system_resources()
        disk_metrics = resources.get("disk")
        
        if not disk_metrics:
            raise HTTPException(status_code=404, detail="Disk metrics not available")
        
        return {
            "disk_metrics": disk_metrics,
            "timestamp": datetime.now(),
            "status": "success"
        }
    except Exception as e:
        logger.error("Failed to get disk metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get disk metrics: {e}"
        )


@router.get("/resources/network")
async def get_network_metrics():
    """Get network-specific metrics"""
    try:
        resources = await hardware_optimizer.get_system_resources()
        network_metrics = resources.get("network")
        
        if not network_metrics:
            raise HTTPException(status_code=404, detail="Network metrics not available")
        
        return {
            "network_metrics": network_metrics,
            "timestamp": datetime.now(),
            "status": "success"
        }
    except Exception as e:
        logger.error("Failed to get network metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get network metrics: {e}"
        )


@router.get("/resources/gpu")
async def get_gpu_metrics():
    """Get GPU-specific metrics"""
    try:
        resources = await hardware_optimizer.get_system_resources()
        gpu_metrics = resources.get("gpu")
        
        if not gpu_metrics:
            return {
                "gpu_metrics": None,
                "message": "GPU not available or not monitored",
                "timestamp": datetime.now(),
                "status": "success"
            }
        
        return {
            "gpu_metrics": gpu_metrics,
            "timestamp": datetime.now(),
            "status": "success"
        }
    except Exception as e:
        logger.error("Failed to get GPU metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get GPU metrics: {e}"
        )


@router.post("/optimize/cpu")
async def optimize_cpu():
    """Optimize CPU usage"""
    try:
        optimization = await hardware_optimizer.optimize_cpu_usage()
        return {
            "optimization_completed": True,
            "optimization_id": optimization.optimization_id,
            "improvement_percentage": optimization.improvement_percentage,
            "success_probability": optimization.success_probability,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to optimize CPU", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize CPU: {e}"
        )


@router.post("/optimize/memory")
async def optimize_memory():
    """Optimize memory usage"""
    try:
        optimization = await hardware_optimizer.optimize_memory_usage()
        return {
            "optimization_completed": True,
            "optimization_id": optimization.optimization_id,
            "improvement_percentage": optimization.improvement_percentage,
            "success_probability": optimization.success_probability,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to optimize memory", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize memory: {e}"
        )


@router.post("/optimize/disk")
async def optimize_disk():
    """Optimize disk usage"""
    try:
        optimization = await hardware_optimizer.optimize_disk_usage()
        return {
            "optimization_completed": True,
            "optimization_id": optimization.optimization_id,
            "improvement_percentage": optimization.improvement_percentage,
            "success_probability": optimization.success_probability,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to optimize disk", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize disk: {e}"
        )


@router.post("/optimize/network")
async def optimize_network():
    """Optimize network usage"""
    try:
        optimization = await hardware_optimizer.optimize_network_usage()
        return {
            "optimization_completed": True,
            "optimization_id": optimization.optimization_id,
            "improvement_percentage": optimization.improvement_percentage,
            "success_probability": optimization.success_probability,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to optimize network", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize network: {e}"
        )


@router.post("/optimize/all")
async def optimize_all_resources():
    """Optimize all system resources"""
    try:
        result = await hardware_optimizer.optimize_all_resources()
        return {
            "optimization_completed": True,
            "result": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to optimize all resources", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to optimize all resources: {e}"
        )


@router.post("/garbage-collection")
async def trigger_garbage_collection():
    """Trigger garbage collection"""
    try:
        result = await hardware_optimizer.force_garbage_collection()
        return {
            "garbage_collection_completed": True,
            "result": result,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to trigger garbage collection", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger garbage collection: {e}"
        )


@router.get("/monitoring/status")
async def get_monitoring_status():
    """Get monitoring status"""
    try:
        summary = await hardware_optimizer.get_optimization_summary()
        return {
            "monitoring_active": summary.get("monitoring_active", False),
            "total_optimizations": summary.get("total_optimizations", 0),
            "success_rate": summary.get("success_rate", 0),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get monitoring status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get monitoring status: {e}"
        )


@router.post("/monitoring/start")
async def start_monitoring():
    """Start hardware monitoring"""
    try:
        await hardware_optimizer.start_monitoring()
        return {
            "monitoring_started": True,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to start monitoring", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start monitoring: {e}"
        )


@router.post("/monitoring/stop")
async def stop_monitoring():
    """Stop hardware monitoring"""
    try:
        await hardware_optimizer.stop_monitoring()
        return {
            "monitoring_stopped": True,
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to stop monitoring", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to stop monitoring: {e}"
        )


@router.get("/optimization/summary")
async def get_optimization_summary():
    """Get optimization summary"""
    try:
        summary = await hardware_optimizer.get_optimization_summary()
        return summary
    except Exception as e:
        logger.error("Failed to get optimization summary", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get optimization summary: {e}"
        )


@router.get("/optimization/history")
async def get_optimization_history():
    """Get optimization history"""
    try:
        summary = await hardware_optimizer.get_optimization_summary()
        optimizations = summary.get("optimizations", {})
        
        return {
            "optimization_history": optimizations,
            "total_optimizations": len(optimizations),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to get optimization history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get optimization history: {e}"
        )


@router.get("/health")
async def hardware_health_check():
    """Hardware health check"""
    try:
        resources = await hardware_optimizer.get_system_resources()
        
        # Determine health status
        cpu_usage = resources.get("cpu", {}).get("current_usage", 0)
        memory_usage = resources.get("memory", {}).get("current_usage", 0)
        disk_usage = resources.get("disk", {}).get("current_usage", 0)
        
        health_status = "healthy"
        if cpu_usage > 90 or memory_usage > 95 or disk_usage > 95:
            health_status = "critical"
        elif cpu_usage > 80 or memory_usage > 85 or disk_usage > 90:
            health_status = "degraded"
        
        return {
            "health_status": health_status,
            "resources": {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_usage": disk_usage,
            },
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error("Failed to perform health check", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to perform health check: {e}"
        )

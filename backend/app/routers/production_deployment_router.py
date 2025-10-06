"""
Production Deployment Router

API endpoints for production deployment, monitoring, health checks, and
deployment management for the CognOmega platform.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum
import structlog
from datetime import datetime
import uuid

from app.services.production_deployment_service import (
    production_deployment_service,
    DeploymentEnvironment,
    DeploymentStatus
)
from app.routers.auth import AuthDependencies
from app.models.user import User

logger = structlog.get_logger(__name__)

router = APIRouter()

class DeploymentConfig(BaseModel):
    """Deployment configuration model"""
    version: str = Field(default="latest", description="Deployment version")
    rollback_version: Optional[str] = Field(None, description="Rollback version")
    user_id: str = Field(..., description="User initiating deployment")
    description: Optional[str] = Field(None, description="Deployment description")
    auto_rollback: bool = Field(default=True, description="Enable auto-rollback on failure")
    run_tests: bool = Field(default=True, description="Run tests before deployment")

class DeploymentRequest(BaseModel):
    """Deployment request model"""
    environment: DeploymentEnvironment
    deployment_config: DeploymentConfig

class DeploymentResponse(BaseModel):
    """Deployment response model"""
    deployment_id: str
    environment: str
    status: str
    duration: float
    success: bool
    logs: List[str]
    completed_at: str

class DeploymentStatusResponse(BaseModel):
    """Deployment status response model"""
    deployment_id: str
    environment: str
    status: str
    duration: Optional[float] = None
    success: Optional[bool] = None
    logs: Optional[List[str]] = None
    started_at: str
    completed_at: Optional[str] = None
    error: Optional[str] = None

class SystemHealthResponse(BaseModel):
    """System health response model"""
    overall_status: str
    healthy: bool
    health_checks: List[Dict[str, Any]]
    summary: Dict[str, Any]
    timestamp: str
    uptime: str
    last_deployment: Optional[str] = None

class DeploymentMetricsResponse(BaseModel):
    """Deployment metrics response model"""
    deployment_metrics: Dict[str, Any]
    success_rate: float
    uptime_percentage: float
    active_deployments: int
    deployment_history_count: int

@router.post("/deploy", response_model=DeploymentResponse)
async def deploy_to_environment(
    request: DeploymentRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Deploy to specified environment"""
    try:
        logger.info(f"Starting deployment to {request.environment.value}", 
                   user_id=current_user.id)
        
        # Update deployment config with user info
        deployment_config = request.deployment_config.dict()
        deployment_config["user_id"] = str(current_user.id)
        
        # Execute deployment
        result = await production_deployment_service.deploy_to_environment(
            request.environment,
            deployment_config
        )
        
        return DeploymentResponse(
            deployment_id=result["deployment_id"],
            environment=result["environment"],
            status=result["status"],
            duration=result["duration"],
            success=result["success"],
            logs=result["logs"],
            completed_at=result["completed_at"]
        )
        
    except Exception as e:
        logger.error(f"Deployment failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")

@router.post("/deploy-async")
async def deploy_to_environment_async(
    request: DeploymentRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Deploy to environment asynchronously"""
    try:
        logger.info(f"Starting async deployment to {request.environment.value}", 
                   user_id=current_user.id)
        
        # Update deployment config with user info
        deployment_config = request.deployment_config.dict()
        deployment_config["user_id"] = str(current_user.id)
        
        # Add deployment to background tasks
        background_tasks.add_task(
            production_deployment_service.deploy_to_environment,
            request.environment,
            deployment_config
        )
        
        return {
            "success": True,
            "message": f"Deployment to {request.environment.value} started in background",
            "status_endpoint": f"/api/v0/deployment/status/{{deployment_id}}"
        }
        
    except Exception as e:
        logger.error(f"Async deployment failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Async deployment failed: {str(e)}")

@router.get("/status/{deployment_id}", response_model=DeploymentStatusResponse)
async def get_deployment_status(
    deployment_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get deployment status"""
    try:
        status = await production_deployment_service.get_deployment_status(deployment_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Deployment not found")
        
        # Check if user has access to this deployment
        # In a real implementation, you would check user permissions
        
        return DeploymentStatusResponse(
            deployment_id=status["deployment_id"],
            environment=status["environment"],
            status=status["status"],
            duration=status.get("duration"),
            success=status.get("success"),
            logs=status.get("logs"),
            started_at=status["started_at"],
            completed_at=status.get("completed_at"),
            error=status.get("error")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Deployment status retrieval failed", 
                    error=str(e), 
                    deployment_id=deployment_id)
        raise HTTPException(status_code=500, detail=f"Deployment status retrieval failed: {str(e)}")

@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health():
    """Get comprehensive system health"""
    try:
        health = await production_deployment_service.get_system_health()
        
        return SystemHealthResponse(
            overall_status=health["overall_status"],
            healthy=health["healthy"],
            health_checks=health["health_checks"],
            summary=health["summary"],
            timestamp=health["timestamp"],
            uptime=health["uptime"],
            last_deployment=health.get("last_deployment")
        )
        
    except Exception as e:
        logger.error(f"System health retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"System health retrieval failed: {str(e)}")

@router.get("/metrics", response_model=DeploymentMetricsResponse)
async def get_deployment_metrics(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get deployment metrics"""
    try:
        # Check if user is admin (simple check for now)
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")
        
        metrics = await production_deployment_service.get_deployment_metrics()
        
        return DeploymentMetricsResponse(
            deployment_metrics=metrics.get("deployment_metrics", {}),
            success_rate=metrics.get("success_rate", 0.0),
            uptime_percentage=metrics.get("uptime_percentage", 0.0),
            active_deployments=metrics.get("active_deployments", 0),
            deployment_history_count=metrics.get("deployment_history_count", 0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Deployment metrics retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Deployment metrics retrieval failed: {str(e)}")

@router.get("/environments")
async def get_deployment_environments():
    """Get available deployment environments"""
    return {
        "environments": [
            {
                "environment": DeploymentEnvironment.DEVELOPMENT.value,
                "name": "Development",
                "description": "Development environment for testing and development",
                "url": "https://dev.cogomega.com",
                "auto_deploy": True,
                "run_tests": True,
                "health_checks": True,
                "rollback_enabled": True
            },
            {
                "environment": DeploymentEnvironment.STAGING.value,
                "name": "Staging",
                "description": "Staging environment for pre-production testing",
                "url": "https://staging.cogomega.com",
                "auto_deploy": False,
                "run_tests": True,
                "health_checks": True,
                "rollback_enabled": True
            },
            {
                "environment": DeploymentEnvironment.PRODUCTION.value,
                "name": "Production",
                "description": "Production environment for live users",
                "url": "https://app.cogomega.com",
                "auto_deploy": False,
                "run_tests": True,
                "health_checks": True,
                "rollback_enabled": True
            }
        ]
    }

@router.get("/deployment-history")
async def get_deployment_history(
    current_user: User = Depends(AuthDependencies.get_current_user),
    limit: int = 10,
    offset: int = 0,
    environment: Optional[DeploymentEnvironment] = None
):
    """Get deployment history"""
    try:
        # Get deployment history from service
        history = production_deployment_service.deployment_history
        
        # Filter by environment if specified
        if environment:
            history = [d for d in history if d.environment == environment.value]
        
        # Sort by timestamp descending
        history.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply pagination
        total_count = len(history)
        paginated_history = history[offset:offset + limit]
        
        # Convert to response format
        deployment_history = []
        for deployment in paginated_history:
            deployment_history.append({
                "deployment_id": deployment.deployment_id,
                "environment": deployment.environment,
                "status": deployment.status,
                "duration": deployment.duration,
                "success": deployment.success,
                "timestamp": deployment.timestamp.isoformat()
            })
        
        return {
            "deployments": deployment_history,
            "total_count": total_count,
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < total_count
        }
        
    except Exception as e:
        logger.error(f"Deployment history retrieval failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Deployment history retrieval failed: {str(e)}")

@router.get("/active-deployments")
async def get_active_deployments(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get active deployments"""
    try:
        active_deployments = []
        
        for deployment_id, deployment in production_deployment_service.active_deployments.items():
            active_deployments.append({
                "deployment_id": deployment_id,
                "environment": deployment["environment"],
                "status": deployment["status"],
                "version": deployment.get("version", "latest"),
                "started_at": deployment["started_at"],
                "user_id": deployment.get("user_id")
            })
        
        return {
            "active_deployments": active_deployments,
            "count": len(active_deployments)
        }
        
    except Exception as e:
        logger.error(f"Active deployments retrieval failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Active deployments retrieval failed: {str(e)}")

@router.post("/rollback/{deployment_id}")
async def rollback_deployment(
    deployment_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Rollback a deployment"""
    try:
        # Check if deployment exists
        status = await production_deployment_service.get_deployment_status(deployment_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Deployment not found")
        
        # Check if user has permission to rollback
        # In a real implementation, you would check user permissions
        
        logger.info(f"Initiating rollback for deployment {deployment_id}", 
                   user_id=current_user.id)
        
        # Simulate rollback
        rollback_result = {
            "deployment_id": deployment_id,
            "rollback_id": f"rollback_{uuid.uuid4().hex[:8]}",
            "status": "completed",
            "rolled_back_to": status.get("rollback_version", "previous"),
            "initiated_by": str(current_user.id),
            "initiated_at": datetime.now().isoformat()
        }
        
        return rollback_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rollback failed", 
                    error=str(e), 
                    deployment_id=deployment_id)
        raise HTTPException(status_code=500, detail=f"Rollback failed: {str(e)}")

@router.get("/health-check")
async def run_health_check():
    """Run manual health check"""
    try:
        health = await production_deployment_service.get_system_health()
        
        return {
            "status": "completed",
            "health_result": health,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Health check failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@router.get("/deployment-status")
async def get_deployment_status_summary():
    """Get deployment status summary"""
    try:
        metrics = await production_deployment_service.get_deployment_metrics()
        health = await production_deployment_service.get_system_health()
        
        return {
            "deployment_summary": {
                "total_deployments": metrics.get("deployment_metrics", {}).get("total_deployments", 0),
                "success_rate": metrics.get("success_rate", 0.0),
                "uptime_percentage": metrics.get("uptime_percentage", 0.0),
                "active_deployments": metrics.get("active_deployments", 0)
            },
            "system_health": {
                "overall_status": health["overall_status"],
                "healthy": health["healthy"],
                "last_health_check": health["timestamp"]
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Deployment status summary failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Deployment status summary failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for deployment service"""
    try:
        metrics = await production_deployment_service.get_deployment_metrics()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service_status": "operational",
            "active_deployments": metrics.get("active_deployments", 0),
            "total_deployments": metrics.get("deployment_metrics", {}).get("total_deployments", 0),
            "success_rate": metrics.get("success_rate", 0.0)
        }
        
    except Exception as e:
        logger.error(f"Deployment service health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

"""
Zero-Cost Infrastructure Router

API endpoints for managing zero-cost infrastructure deployments using Cloudflare, Railway, and Neon.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum
import structlog
from datetime import datetime

from app.services.zero_cost_infrastructure_service import (
    zero_cost_service,
    InfrastructureProvider,
    InfrastructureType
)
from app.routers.auth import AuthDependencies
from app.models.user import User

logger = structlog.get_logger(__name__)

router = APIRouter()

class DeploymentConfig(BaseModel):
    """Deployment configuration model"""
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: bool = True
    config: Dict[str, Any] = Field(default_factory=dict)

class StackConfig(BaseModel):
    """Stack configuration model"""
    cloudflare: Dict[str, Any] = Field(default_factory=dict)
    railway: Dict[str, Any] = Field(default_factory=dict)
    neon: Dict[str, Any] = Field(default_factory=dict)

class DeploymentRequest(BaseModel):
    """Deployment request model"""
    provider: InfrastructureProvider
    deployment_type: InfrastructureType
    deployment_config: Dict[str, Any]

class StackDeploymentRequest(BaseModel):
    """Stack deployment request model"""
    stack_config: StackConfig
    description: Optional[str] = None

class DeploymentResponse(BaseModel):
    """Deployment response model"""
    deployment_id: str
    provider: str
    type: str
    status: str
    url: Optional[str] = None
    cost: float
    deployed_at: str

class StackDeploymentResponse(BaseModel):
    """Stack deployment response model"""
    stack_id: str
    deployments: List[DeploymentResponse]
    total_cost: float
    status: str
    created_at: str

class InfrastructureStatusResponse(BaseModel):
    """Infrastructure status response model"""
    stack_id: str
    deployments: List[DeploymentResponse]
    total_cost: float
    status: str
    created_at: str

class InfrastructureMetricsResponse(BaseModel):
    """Infrastructure metrics response model"""
    infrastructure_metrics: Dict[str, Any]
    active_deployments_count: int
    provider_breakdown: Dict[str, Any]
    cost_savings: Dict[str, Any]
    resource_usage: Dict[str, Any]

@router.post("/deploy", response_model=DeploymentResponse)
async def deploy_infrastructure(
    request: DeploymentRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Deploy infrastructure component"""
    try:
        logger.info(f"Deploying infrastructure component", 
                   provider=request.provider.value,
                   type=request.deployment_type.value,
                   user_id=current_user.id)
        
        # Deploy based on provider
        if request.provider == InfrastructureProvider.CLOUDFLARE:
            result = await zero_cost_service.deploy_to_cloudflare(
                request.deployment_type,
                request.deployment_config
            )
        elif request.provider == InfrastructureProvider.RAILWAY:
            result = await zero_cost_service.deploy_to_railway(
                request.deployment_type,
                request.deployment_config
            )
        elif request.provider == InfrastructureProvider.NEON:
            result = await zero_cost_service.deploy_to_neon(
                request.deployment_type,
                request.deployment_config
            )
        else:
            raise ValueError(f"Unsupported provider: {request.provider}")
        
        return DeploymentResponse(
            deployment_id=result["deployment_id"],
            provider=result["provider"],
            type=result["type"],
            status=result["status"],
            url=result.get("url"),
            cost=result["cost"],
            deployed_at=result["deployed_at"]
        )
        
    except Exception as e:
        logger.error(f"Infrastructure deployment failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Deployment failed: {str(e)}")

@router.post("/deploy-stack", response_model=StackDeploymentResponse)
async def deploy_infrastructure_stack(
    request: StackDeploymentRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Deploy complete zero-cost infrastructure stack"""
    try:
        logger.info(f"Deploying zero-cost infrastructure stack", 
                   user_id=current_user.id)
        
        # Deploy stack
        result = await zero_cost_service.deploy_zero_cost_stack(
            request.stack_config.dict()
        )
        
        # Convert deployments to response format
        deployments = []
        for deployment in result["deployments"]:
            deployments.append(DeploymentResponse(
                deployment_id=deployment["deployment_id"],
                provider=deployment["provider"],
                type=deployment["type"],
                status=deployment["status"],
                url=deployment.get("url"),
                cost=deployment["cost"],
                deployed_at=deployment["deployed_at"]
            ))
        
        return StackDeploymentResponse(
            stack_id=result["stack_id"],
            deployments=deployments,
            total_cost=result["total_cost"],
            status=result["status"],
            created_at=result["created_at"]
        )
        
    except Exception as e:
        logger.error(f"Infrastructure stack deployment failed", 
                    error=str(e), 
                    user_id=current_user.id)
        raise HTTPException(status_code=500, detail=f"Stack deployment failed: {str(e)}")

@router.get("/status/{stack_id}", response_model=InfrastructureStatusResponse)
async def get_infrastructure_status(
    stack_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get infrastructure deployment status"""
    try:
        status = await zero_cost_service.get_infrastructure_status(stack_id)
        
        if not status:
            raise HTTPException(status_code=404, detail="Infrastructure stack not found")
        
        # Convert deployments to response format
        deployments = []
        for deployment in status["deployments"]:
            deployments.append(DeploymentResponse(
                deployment_id=deployment["deployment_id"],
                provider=deployment["provider"],
                type=deployment["type"],
                status=deployment["status"],
                url=deployment.get("url"),
                cost=deployment["cost"],
                deployed_at=deployment["deployed_at"]
            ))
        
        return InfrastructureStatusResponse(
            stack_id=status["stack_id"],
            deployments=deployments,
            total_cost=status["total_cost"],
            status=status["status"],
            created_at=status["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Infrastructure status retrieval failed", 
                    error=str(e), 
                    stack_id=stack_id)
        raise HTTPException(status_code=500, detail=f"Status retrieval failed: {str(e)}")

@router.get("/metrics", response_model=InfrastructureMetricsResponse)
async def get_infrastructure_metrics(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get infrastructure performance metrics"""
    try:
        # Check if user is admin (simple check for now)
        if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")
        
        metrics = await zero_cost_service.get_infrastructure_metrics()
        
        return InfrastructureMetricsResponse(
            infrastructure_metrics=metrics.get("infrastructure_metrics", {}),
            active_deployments_count=metrics.get("active_deployments_count", 0),
            provider_breakdown=metrics.get("provider_breakdown", {}),
            cost_savings=metrics.get("cost_savings", {}),
            resource_usage=metrics.get("resource_usage", {})
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Infrastructure metrics retrieval failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Metrics retrieval failed: {str(e)}")

@router.get("/providers")
async def get_available_providers():
    """Get available infrastructure providers"""
    return {
        "providers": [
            {
                "provider": InfrastructureProvider.CLOUDFLARE.value,
                "name": "Cloudflare",
                "description": "Global CDN and edge computing platform",
                "services": ["workers", "pages", "d1", "cdn"],
                "free_tier_limits": {
                    "workers_requests": "100,000/day",
                    "pages_sites": "unlimited",
                    "d1_storage": "5GB",
                    "d1_reads": "25M/month",
                    "bandwidth": "unlimited"
                },
                "cost_savings": "Up to $50/month"
            },
            {
                "provider": InfrastructureProvider.RAILWAY.value,
                "name": "Railway",
                "description": "Modern deployment platform for applications",
                "services": ["services", "databases", "storage"],
                "free_tier_limits": {
                    "usage_credit": "$5/month",
                    "services": "1",
                    "database_storage": "1GB",
                    "bandwidth": "1GB/month"
                },
                "cost_savings": "Up to $20/month"
            },
            {
                "provider": InfrastructureProvider.NEON.value,
                "name": "Neon",
                "description": "Serverless PostgreSQL database platform",
                "services": ["databases", "storage", "compute"],
                "free_tier_limits": {
                    "database_storage": "0.5GB",
                    "connections": "1",
                    "compute": "0.5 vCPU",
                    "bandwidth": "1GB/month"
                },
                "cost_savings": "Up to $25/month"
            }
        ]
    }

@router.get("/deployment-types")
async def get_deployment_types():
    """Get available deployment types"""
    return {
        "deployment_types": [
            {
                "type": InfrastructureType.FRONTEND.value,
                "name": "Frontend",
                "description": "Static site hosting and CDN",
                "providers": ["cloudflare"],
                "use_cases": ["web_apps", "static_sites", "spa_apps"]
            },
            {
                "type": InfrastructureType.BACKEND.value,
                "name": "Backend",
                "description": "API services and serverless functions",
                "providers": ["cloudflare", "railway"],
                "use_cases": ["apis", "microservices", "serverless_functions"]
            },
            {
                "type": InfrastructureType.DATABASE.value,
                "name": "Database",
                "description": "Database hosting and storage",
                "providers": ["cloudflare", "railway", "neon"],
                "use_cases": ["data_storage", "analytics", "user_data"]
            },
            {
                "type": InfrastructureType.WORKERS.value,
                "name": "Workers",
                "description": "Edge computing and serverless execution",
                "providers": ["cloudflare"],
                "use_cases": ["edge_computing", "ai_processing", "api_proxies"]
            },
            {
                "type": InfrastructureType.CDN.value,
                "name": "CDN",
                "description": "Content delivery network",
                "providers": ["cloudflare"],
                "use_cases": ["static_assets", "media_delivery", "global_caching"]
            },
            {
                "type": InfrastructureType.STORAGE.value,
                "name": "Storage",
                "description": "File storage and object storage",
                "providers": ["cloudflare", "railway"],
                "use_cases": ["file_uploads", "media_storage", "backups"]
            }
        ]
    }

@router.get("/cost-calculator")
async def calculate_infrastructure_costs(
    provider: Optional[InfrastructureProvider] = None,
    deployment_type: Optional[InfrastructureType] = None,
    usage_level: str = "basic"
):
    """Calculate infrastructure costs and savings"""
    try:
        # Cost comparison data
        cost_data = {
            "cloudflare": {
                "workers": {"basic": 0.0, "standard": 5.0, "pro": 50.0},
                "pages": {"basic": 0.0, "standard": 0.0, "pro": 0.0},
                "d1": {"basic": 0.0, "standard": 2.5, "pro": 25.0}
            },
            "railway": {
                "service": {"basic": 0.0, "standard": 5.0, "pro": 20.0},
                "database": {"basic": 0.0, "standard": 5.0, "pro": 20.0}
            },
            "neon": {
                "database": {"basic": 0.0, "standard": 19.0, "pro": 99.0}
            }
        }
        
        results = {}
        
        if provider and deployment_type:
            # Calculate for specific provider and type
            if provider.value in cost_data and deployment_type.value in cost_data[provider.value]:
                costs = cost_data[provider.value][deployment_type.value]
                results[provider.value] = {
                    deployment_type.value: {
                        "zero_cost": costs["basic"],
                        "paid_alternative": costs["standard"],
                        "premium_alternative": costs["pro"],
                        "monthly_savings": costs["standard"] - costs["basic"],
                        "annual_savings": (costs["standard"] - costs["basic"]) * 12
                    }
                }
        else:
            # Calculate for all providers
            for provider_name, provider_costs in cost_data.items():
                results[provider_name] = {}
                for service_name, service_costs in provider_costs.items():
                    results[provider_name][service_name] = {
                        "zero_cost": service_costs["basic"],
                        "paid_alternative": service_costs["standard"],
                        "premium_alternative": service_costs["pro"],
                        "monthly_savings": service_costs["standard"] - service_costs["basic"],
                        "annual_savings": (service_costs["standard"] - service_costs["basic"]) * 12
                    }
        
        # Calculate total savings
        total_monthly_savings = 0.0
        for provider_data in results.values():
            for service_data in provider_data.values():
                total_monthly_savings += service_data["monthly_savings"]
        
        return {
            "cost_breakdown": results,
            "total_savings": {
                "monthly": total_monthly_savings,
                "annual": total_monthly_savings * 12
            },
            "usage_level": usage_level,
            "note": "All costs are in USD per month"
        }
        
    except Exception as e:
        logger.error(f"Cost calculation failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Cost calculation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint for zero-cost infrastructure service"""
    try:
        metrics = await zero_cost_service.get_infrastructure_metrics()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service_status": "operational",
            "active_deployments": metrics.get("active_deployments_count", 0),
            "total_deployments": metrics.get("infrastructure_metrics", {}).get("total_deployments", 0),
            "cost_savings": metrics.get("cost_savings", {}).get("total_monthly_savings", 0.0)
        }
        
    except Exception as e:
        logger.error(f"Zero-cost infrastructure health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

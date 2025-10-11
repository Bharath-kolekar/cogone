"""
Admin router for feature management and system configuration
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional, Any
import structlog

from app.models.admin import (
    FeatureConfig, AdminDashboard, FeatureToggleRequest,
    FeatureConfigurationRequest, SystemConfiguration, FeatureCategory
)
from app.services.admin_service import AdminService
from app.models.auth import User
from app.routers.auth import AuthDependencies

router = APIRouter(prefix="/admin", tags=["Admin"])
logger = structlog.get_logger()


class AdminDependencies:
    """Admin dependencies"""
    
    @staticmethod
    async def check_admin_permissions(current_user: User = Depends(AuthDependencies.get_current_user)) -> User:
        """Check if user has admin permissions"""
        if not current_user.is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin permissions required"
            )
        return current_user


@router.get("/dashboard", response_model=AdminDashboard)
async def get_admin_dashboard(
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get admin dashboard data"""
    try:
        admin_service = AdminService()
        dashboard = await admin_service.get_dashboard()
        
        logger.info("Admin dashboard accessed", user_id=current_user.id)
        return dashboard
        
    except Exception as e:
        logger.error("Failed to get admin dashboard", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/features", response_model=List[FeatureConfig])
async def get_all_features(
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get all features"""
    try:
        admin_service = AdminService()
        features = list(admin_service.features.values())
        
        logger.info("Features accessed", user_id=current_user.id, count=len(features))
        return features
        
    except Exception as e:
        logger.error("Failed to get features", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/features/{feature_id}", response_model=FeatureConfig)
async def get_feature(
    feature_id: str,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get specific feature"""
    try:
        admin_service = AdminService()
        feature = await admin_service.get_feature_status(feature_id)
        
        if not feature:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Feature {feature_id} not found"
            )
        
        logger.info("Feature accessed", user_id=current_user.id, feature_id=feature_id)
        return feature
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to get feature", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/features/category/{category}", response_model=List[FeatureConfig])
async def get_features_by_category(
    category: FeatureCategory,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get features by category"""
    try:
        admin_service = AdminService()
        features = await admin_service.get_features_by_category(category)
        
        logger.info("Features by category accessed", user_id=current_user.id, category=category, count=len(features))
        return features
        
    except Exception as e:
        logger.error("Failed to get features by category", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/features/toggle", response_model=FeatureConfig)
async def toggle_feature(
    request: FeatureToggleRequest,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Toggle feature status"""
    try:
        admin_service = AdminService()
        feature = await admin_service.toggle_feature(request)
        
        logger.info(
            "Feature toggled",
            user_id=current_user.id,
            feature_id=request.feature_id,
            status=request.status,
            reason=request.reason
        )
        return feature
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to toggle feature", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/features/configure", response_model=FeatureConfig)
async def configure_feature(
    request: FeatureConfigurationRequest,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Configure feature settings"""
    try:
        admin_service = AdminService()
        feature = await admin_service.configure_feature(request)
        
        logger.info(
            "Feature configured",
            user_id=current_user.id,
            feature_id=request.feature_id,
            configuration=request.configuration,
            reason=request.reason
        )
        return feature
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error("Failed to configure feature", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/system-config", response_model=SystemConfiguration)
async def get_system_configuration(
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get system configuration"""
    try:
        admin_service = AdminService()
        config = await admin_service.get_system_configuration()
        
        logger.info("System configuration accessed", user_id=current_user.id)
        return config
        
    except Exception as e:
        logger.error("Failed to get system configuration", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/system-config", response_model=SystemConfiguration)
async def update_system_configuration(
    config: SystemConfiguration,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Update system configuration"""
    try:
        admin_service = AdminService()
        await admin_service.update_system_configuration(config)
        
        logger.info("System configuration updated", user_id=current_user.id, config=config.dict())
        return config
        
    except Exception as e:
        logger.error("Failed to update system configuration", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/ai-assistant", response_model=Dict[str, Any])
async def get_ai_assistant_config(
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get AI assistant configuration"""
    try:
        admin_service = AdminService()
        config = await admin_service.get_ai_assistant_config()
        
        logger.info("AI assistant configuration accessed", user_id=current_user.id)
        return config
        
    except Exception as e:
        logger.error("Failed to get AI assistant configuration", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/ai-assistant")
async def update_ai_assistant_config(
    name: Optional[str] = None,
    wake_word: Optional[str] = None,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Update AI assistant configuration"""
    try:
        admin_service = AdminService()
        await admin_service.update_ai_assistant_config(name, wake_word)
        
        logger.info(
            "AI assistant configuration updated",
            user_id=current_user.id,
            name=name,
            wake_word=wake_word
        )
        return {"message": "AI assistant configuration updated successfully"}
        
    except Exception as e:
        logger.error("Failed to update AI assistant configuration", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/usage/{feature_id}")
async def update_feature_usage(
    feature_id: str,
    usage_count: int,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Update feature usage count"""
    try:
        admin_service = AdminService()
        await admin_service.update_usage(feature_id, usage_count)
        
        logger.info(
            "Feature usage updated",
            user_id=current_user.id,
            feature_id=feature_id,
            usage_count=usage_count
        )
        return {"message": "Feature usage updated successfully"}
        
    except Exception as e:
        logger.error("Failed to update feature usage", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/alerts")
async def get_active_alerts(
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get active alerts"""
    try:
        admin_service = AdminService()
        alerts = await admin_service._get_active_alerts()
        
        logger.info("Active alerts accessed", user_id=current_user.id, count=len(alerts))
        return {"alerts": alerts}
        
    except Exception as e:
        logger.error("Failed to get active alerts", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
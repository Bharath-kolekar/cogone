"""
Admin router for Voice-to-App SaaS Platform
Handles admin operations, reports, and system management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import structlog
from datetime import datetime, timedelta

from app.core.config import settings
from app.services.admin_service import AdminService
from app.services.analytics_service import AnalyticsService
from app.routers.auth import AuthDependencies
from app.models.user import User
from app.models.admin import (
    AdminStatsRequest,
    AdminStatsResponse,
    UserManagementRequest,
    UserManagementResponse,
    SystemHealthRequest,
    SystemHealthResponse,
)

logger = structlog.get_logger()
router = APIRouter()


class AdminDependencies:
    """Admin dependencies"""
    
    @staticmethod
    async def check_admin_permissions(
        current_user: User = Depends(AuthDependencies.get_current_user)
    ) -> User:
        """Check if user has admin permissions"""
        if current_user.subscription_tier not in ["enterprise"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        return current_user


@router.get("/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    request: AdminStatsRequest,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get comprehensive admin statistics"""
    try:
        admin_service = AdminService()
        analytics_service = AnalyticsService()
        
        # Get various statistics
        user_stats = await admin_service.get_user_statistics(
            time_period=request.time_period
        )
        
        app_stats = await admin_service.get_app_statistics(
            time_period=request.time_period
        )
        
        payment_stats = await admin_service.get_payment_statistics(
            time_period=request.time_period
        )
        
        voice_stats = await admin_service.get_voice_statistics(
            time_period=request.time_period
        )
        
        logger.info(
            "Admin stats retrieved",
            admin_user_id=current_user.id,
            time_period=request.time_period
        )
        
        return AdminStatsResponse(
            time_period=request.time_period,
            users=user_stats,
            apps=app_stats,
            payments=payment_stats,
            voice_commands=voice_stats,
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Failed to get admin stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/users")
async def get_all_users(
    limit: int = 50,
    offset: int = 0,
    search: Optional[str] = None,
    subscription_tier: Optional[str] = None,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get all users with filtering options"""
    try:
        admin_service = AdminService()
        
        users = await admin_service.get_all_users(
            limit=limit,
            offset=offset,
            search=search,
            subscription_tier=subscription_tier
        )
        
        return {
            "users": users,
            "total": len(users),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error("Failed to get users", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/users/{user_id}", response_model=UserManagementResponse)
async def update_user(
    user_id: str,
    request: UserManagementRequest,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Update user details (admin only)"""
    try:
        admin_service = AdminService()
        
        updated_user = await admin_service.update_user(
            user_id=user_id,
            updates=request
        )
        
        logger.info(
            "User updated by admin",
            admin_user_id=current_user.id,
            target_user_id=user_id
        )
        
        return UserManagementResponse(
            user_id=user_id,
            status="updated",
            message="User updated successfully",
            updated_fields=request.dict(exclude_unset=True)
        )
        
    except Exception as e:
        logger.error("User update failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Delete user account (admin only)"""
    try:
        admin_service = AdminService()
        
        await admin_service.delete_user(user_id)
        
        logger.info(
            "User deleted by admin",
            admin_user_id=current_user.id,
            target_user_id=user_id
        )
        
        return {"message": "User deleted successfully"}
        
    except Exception as e:
        logger.error("User deletion failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/health", response_model=SystemHealthResponse)
async def get_system_health(
    request: SystemHealthRequest,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get system health status"""
    try:
        admin_service = AdminService()
        
        health_status = await admin_service.get_system_health()
        
        return SystemHealthResponse(
            status=health_status.status,
            services=health_status.services,
            database=health_status.database,
            redis=health_status.redis,
            external_apis=health_status.external_apis,
            checked_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error("Failed to get system health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/reports/users")
async def get_user_report(
    start_date: datetime,
    end_date: datetime,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Generate user activity report"""
    try:
        analytics_service = AnalyticsService()
        
        report = await analytics_service.generate_user_report(
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            "report": report,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to generate user report", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/reports/apps")
async def get_app_report(
    start_date: datetime,
    end_date: datetime,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Generate app generation report"""
    try:
        analytics_service = AnalyticsService()
        
        report = await analytics_service.generate_app_report(
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            "report": report,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to generate app report", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/reports/payments")
async def get_payment_report(
    start_date: datetime,
    end_date: datetime,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Generate payment report"""
    try:
        analytics_service = AnalyticsService()
        
        report = await analytics_service.generate_payment_report(
            start_date=start_date,
            end_date=end_date
        )
        
        return {
            "report": report,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to generate payment report", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/analytics/dashboard")
async def get_dashboard_analytics(
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get dashboard analytics for admin panel"""
    try:
        analytics_service = AnalyticsService()
        
        dashboard_data = await analytics_service.get_dashboard_data()
        
        return {
            "dashboard": dashboard_data,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get dashboard analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/maintenance/mode")
async def toggle_maintenance_mode(
    enabled: bool,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Toggle maintenance mode"""
    try:
        admin_service = AdminService()
        
        await admin_service.toggle_maintenance_mode(enabled)
        
        logger.info(
            "Maintenance mode toggled",
            admin_user_id=current_user.id,
            enabled=enabled
        )
        
        return {
            "maintenance_mode": enabled,
            "message": f"Maintenance mode {'enabled' if enabled else 'disabled'}"
        }
        
    except Exception as e:
        logger.error("Failed to toggle maintenance mode", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/logs")
async def get_system_logs(
    level: Optional[str] = None,
    limit: int = 100,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Get system logs"""
    try:
        admin_service = AdminService()
        
        logs = await admin_service.get_system_logs(
            level=level,
            limit=limit
        )
        
        return {
            "logs": logs,
            "total": len(logs),
            "limit": limit
        }
        
    except Exception as e:
        logger.error("Failed to get system logs", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/notifications/broadcast")
async def send_broadcast_notification(
    title: str,
    message: str,
    target_users: Optional[List[str]] = None,
    current_user: User = Depends(AdminDependencies.check_admin_permissions)
):
    """Send broadcast notification to users"""
    try:
        admin_service = AdminService()
        
        notification_id = await admin_service.send_broadcast_notification(
            title=title,
            message=message,
            target_users=target_users
        )
        
        logger.info(
            "Broadcast notification sent",
            admin_user_id=current_user.id,
            notification_id=notification_id,
            target_count=len(target_users) if target_users else "all"
        )
        
        return {
            "notification_id": notification_id,
            "message": "Broadcast notification sent successfully"
        }
        
    except Exception as e:
        logger.error("Failed to send broadcast notification", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
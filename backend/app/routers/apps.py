"""
App generation and management router for Voice-to-App SaaS Platform
Handles app creation, templates, marketplace, and collaborative editing
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import structlog
from datetime import datetime

from app.core.config import settings
from app.services.app_generation_service import AppGenerationService
from app.services.template_service import TemplateService
from app.services.collaboration_service import CollaborationService
from app.routers.auth import AuthDependencies
from app.models.user import User
from app.models.app import (
    AppCreateRequest,
    AppCreateResponse,
    AppUpdateRequest,
    AppUpdateResponse,
    AppListRequest,
    AppListResponse,
    TemplateCreateRequest,
    TemplateCreateResponse,
    TemplateListRequest,
    TemplateListResponse,
    CollaborationInviteRequest,
    CollaborationInviteResponse,
)

logger = structlog.get_logger()
router = APIRouter()


class AppDependencies:
    """App management dependencies"""
    
    @staticmethod
    async def check_app_quota(
        current_user: User = Depends(AuthDependencies.get_current_user)
    ) -> User:
        """Check if user has remaining app generation quota"""
        # This would check subscription limits, monthly quotas, etc.
        return current_user


@router.post("/create", response_model=AppCreateResponse)
async def create_app(
    request: AppCreateRequest,
    current_user: User = Depends(AppDependencies.check_app_quota)
):
    """Create a new app from voice command or template"""
    try:
        app_service = AppGenerationService()
        
        # Create app record
        app_record = await app_service.create_app_record(
            user_id=current_user.id,
            title=request.title,
            description=request.description,
            voice_command=request.voice_command,
            template_id=request.template_id,
            metadata=request.metadata
        )
        
        # Start app generation
        if request.voice_command:
            # Generate from voice command
            generation_task = await app_service.generate_from_voice(
                app_id=app_record.id,
                voice_command=request.voice_command,
                user_preferences=request.user_preferences
            )
        elif request.template_id:
            # Generate from template
            generation_task = await app_service.generate_from_template(
                app_id=app_record.id,
                template_id=request.template_id,
                customizations=request.customizations
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either voice_command or template_id must be provided"
            )
        
        logger.info(
            "App creation started",
            user_id=current_user.id,
            app_id=app_record.id,
            method="voice" if request.voice_command else "template"
        )
        
        return AppCreateResponse(
            app_id=app_record.id,
            status="generating",
            message="App generation started",
            estimated_time_ms=generation_task.estimated_time_ms,
            preview_url=None
        )
        
    except Exception as e:
        logger.error("App creation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/list", response_model=AppListResponse)
async def list_user_apps(
    request: AppListRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get user's generated apps"""
    try:
        app_service = AppGenerationService()
        
        apps = await app_service.get_user_apps(
            user_id=current_user.id,
            status=request.status,
            limit=request.limit,
            offset=request.offset,
            sort_by=request.sort_by
        )
        
        return AppListResponse(
            apps=apps,
            total=len(apps),
            limit=request.limit,
            offset=request.offset
        )
        
    except Exception as e:
        logger.error("Failed to list apps", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{app_id}")
async def get_app_details(
    app_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get detailed information about a specific app"""
    try:
        app_service = AppGenerationService()
        
        app_details = await app_service.get_app_details(app_id, current_user.id)
        if not app_details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="App not found"
            )
        
        return app_details
        
    except Exception as e:
        logger.error("Failed to get app details", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{app_id}", response_model=AppUpdateResponse)
async def update_app(
    app_id: str,
    request: AppUpdateRequest,
    current_user: User = Depends(AuthDependencies.check_app_quota)
):
    """Update app details or regenerate"""
    try:
        app_service = AppGenerationService()
        
        # Check if app exists and belongs to user
        app_record = await app_service.get_app_record(app_id, current_user.id)
        if not app_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="App not found"
            )
        
        # Update app
        updated_app = await app_service.update_app(
            app_id=app_id,
            user_id=current_user.id,
            updates=request
        )
        
        logger.info(
            "App updated",
            user_id=current_user.id,
            app_id=app_id
        )
        
        return AppUpdateResponse(
            app_id=app_id,
            status=updated_app.status,
            message="App updated successfully",
            updated_fields=request.dict(exclude_unset=True)
        )
        
    except Exception as e:
        logger.error("App update failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{app_id}")
async def delete_app(
    app_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Delete app and all associated files"""
    try:
        app_service = AppGenerationService()
        
        # Check if app exists and belongs to user
        app_record = await app_service.get_app_record(app_id, current_user.id)
        if not app_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="App not found"
            )
        
        # Delete app
        await app_service.delete_app(app_id, current_user.id)
        
        logger.info(
            "App deleted",
            user_id=current_user.id,
            app_id=app_id
        )
        
        return {"message": "App deleted successfully"}
        
    except Exception as e:
        logger.error("App deletion failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/templates/create", response_model=TemplateCreateResponse)
async def create_template(
    request: TemplateCreateRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Create app template for marketplace"""
    try:
        if not settings.ENABLE_TEMPLATES_MARKETPLACE:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Template marketplace is disabled"
            )
        
        template_service = TemplateService()
        
        # Create template
        template = await template_service.create_template(
            creator_id=current_user.id,
            title=request.title,
            description=request.description,
            category=request.category,
            tags=request.tags,
            template_data=request.template_data,
            is_public=request.is_public
        )
        
        logger.info(
            "Template created",
            user_id=current_user.id,
            template_id=template.id,
            is_public=request.is_public
        )
        
        return TemplateCreateResponse(
            template_id=template.id,
            status="created",
            message="Template created successfully",
            marketplace_url=f"/templates/{template.id}" if request.is_public else None
        )
        
    except Exception as e:
        logger.error("Template creation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/templates/list", response_model=TemplateListResponse)
async def list_templates(
    request: TemplateListRequest
):
    """Get available app templates"""
    try:
        template_service = TemplateService()
        
        templates = await template_service.get_templates(
            category=request.category,
            tags=request.tags,
            is_public=True,
            limit=request.limit,
            offset=request.offset,
            sort_by=request.sort_by
        )
        
        return TemplateListResponse(
            templates=templates,
            total=len(templates),
            limit=request.limit,
            offset=request.offset
        )
        
    except Exception as e:
        logger.error("Failed to list templates", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/templates/{template_id}")
async def get_template_details(
    template_id: str
):
    """Get detailed information about a template"""
    try:
        template_service = TemplateService()
        
        template = await template_service.get_template_details(template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        return template
        
    except Exception as e:
        logger.error("Failed to get template details", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/templates/{template_id}/use")
async def use_template(
    template_id: str,
    customizations: Dict[str, Any],
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Use template to create new app"""
    try:
        template_service = TemplateService()
        app_service = AppGenerationService()
        
        # Get template
        template = await template_service.get_template_details(template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Template not found"
            )
        
        # Create app from template
        app_record = await app_service.create_app_from_template(
            user_id=current_user.id,
            template_id=template_id,
            customizations=customizations
        )
        
        logger.info(
            "App created from template",
            user_id=current_user.id,
            template_id=template_id,
            app_id=app_record.id
        )
        
        return {
            "app_id": app_record.id,
            "status": "generating",
            "message": "App generation started from template"
        }
        
    except Exception as e:
        logger.error("Template usage failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/collaborate/invite", response_model=CollaborationInviteResponse)
async def invite_collaborator(
    request: CollaborationInviteRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Invite collaborator to edit app"""
    try:
        if not settings.ENABLE_COLLABORATIVE_EDITING:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Collaborative editing is disabled"
            )
        
        collaboration_service = CollaborationService()
        
        # Invite collaborator
        invitation = await collaboration_service.invite_collaborator(
            app_id=request.app_id,
            inviter_id=current_user.id,
            collaborator_email=request.collaborator_email,
            permissions=request.permissions
        )
        
        logger.info(
            "Collaborator invited",
            app_id=request.app_id,
            inviter_id=current_user.id,
            collaborator_email=request.collaborator_email
        )
        
        return CollaborationInviteResponse(
            invitation_id=invitation.id,
            status="sent",
            message="Collaboration invitation sent successfully"
        )
        
    except Exception as e:
        logger.error("Collaboration invitation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/collaborate/invitations")
async def get_collaboration_invitations(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get user's collaboration invitations"""
    try:
        if not settings.ENABLE_COLLABORATIVE_EDITING:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Collaborative editing is disabled"
            )
        
        collaboration_service = CollaborationService()
        
        invitations = await collaboration_service.get_user_invitations(current_user.id)
        
        return {
            "invitations": invitations,
            "total": len(invitations)
        }
        
    except Exception as e:
        logger.error("Failed to get collaboration invitations", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/collaborate/accept/{invitation_id}")
async def accept_collaboration_invitation(
    invitation_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Accept collaboration invitation"""
    try:
        if not settings.ENABLE_COLLABORATIVE_EDITING:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Collaborative editing is disabled"
            )
        
        collaboration_service = CollaborationService()
        
        result = await collaboration_service.accept_invitation(
            invitation_id=invitation_id,
            user_id=current_user.id
        )
        
        logger.info(
            "Collaboration invitation accepted",
            invitation_id=invitation_id,
            user_id=current_user.id,
            app_id=result.app_id
        )
        
        return {
            "success": True,
            "app_id": result.app_id,
            "message": "Collaboration invitation accepted successfully"
        }
        
    except Exception as e:
        logger.error("Collaboration acceptance failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/analytics/{app_id}")
async def get_app_analytics(
    app_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get app analytics and usage statistics"""
    try:
        app_service = AppGenerationService()
        
        # Check if app exists and belongs to user
        app_record = await app_service.get_app_record(app_id, current_user.id)
        if not app_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="App not found"
            )
        
        analytics = await app_service.get_app_analytics(app_id)
        
        return analytics
        
    except Exception as e:
        logger.error("Failed to get app analytics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/export/{app_id}")
async def export_app_code(
    app_id: str,
    format: str = "zip",
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Export app code in specified format"""
    try:
        app_service = AppGenerationService()
        
        # Check if app exists and belongs to user
        app_record = await app_service.get_app_record(app_id, current_user.id)
        if not app_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="App not found"
            )
        
        if app_record.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="App must be completed before export"
            )
        
        export_url = await app_service.export_app_code(app_id, format)
        
        logger.info(
            "App code exported",
            user_id=current_user.id,
            app_id=app_id,
            format=format
        )
        
        return {
            "export_url": export_url,
            "format": format,
            "expires_at": datetime.utcnow().isoformat() + "Z"  # 1 hour from now
        }
        
    except Exception as e:
        logger.error("App export failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
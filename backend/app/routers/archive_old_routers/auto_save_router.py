"""
Auto-Save and Keep All Changes Router
API endpoints for auto-save and batch change management
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel

from app.services.auto_save_service import (
    auto_save_service, ChangeRecord, BatchChangeGroup, 
    ChangeType, ChangeStatus
)
from app.routers.auth import AuthDependencies
from app.models.user import User

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v1/auto-save", tags=["Auto-Save & Keep All Changes"])


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ChangeRegistrationRequest(BaseModel):
    """Request to register a change"""
    file_path: str
    change_type: ChangeType
    content_before: Optional[str] = None
    content_after: Optional[str] = None
    change_description: str = ""
    auto_save_enabled: bool = True
    requires_approval: bool = False
    session_id: Optional[str] = None


class BatchChangeRequest(BaseModel):
    """Request for batch change operations"""
    changes: List[ChangeRegistrationRequest]
    group_name: Optional[str] = None
    auto_save_all: bool = True
    requires_approval: bool = False


class ChangeApprovalRequest(BaseModel):
    """Request to approve/reject changes"""
    change_ids: List[str]
    action: str  # "accept" or "reject"
    reason: Optional[str] = None


class AutoSaveConfigRequest(BaseModel):
    """Request to update auto-save configuration"""
    enabled: Optional[bool] = None
    interval_seconds: Optional[int] = None
    max_pending_changes: Optional[int] = None
    auto_approve_safe_changes: Optional[bool] = None
    backup_enabled: Optional[bool] = None
    compression_enabled: Optional[bool] = None


# ============================================================================
# CHANGE REGISTRATION ENDPOINTS
# ============================================================================

@router.post("/register-change")
async def register_change(
    request: ChangeRegistrationRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Register a new change for auto-save or approval"""
    try:
        change_id = auto_save_service.register_change(
            file_path=request.file_path,
            change_type=request.change_type,
            content_before=request.content_before,
            content_after=request.content_after,
            change_description=request.change_description,
            user_id=current_user.id,
            session_id=request.session_id,
            auto_save_enabled=request.auto_save_enabled,
            requires_approval=request.requires_approval
        )
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "change_id": change_id,
                "status": "registered",
                "auto_save_enabled": request.auto_save_enabled,
                "requires_approval": request.requires_approval,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to register change", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register change: {e}"
        )


@router.post("/register-batch-changes")
async def register_batch_changes(
    request: BatchChangeRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Register multiple changes as a batch"""
    try:
        change_ids = []
        
        for change_request in request.changes:
            change_id = auto_save_service.register_change(
                file_path=change_request.file_path,
                change_type=change_request.change_type,
                content_before=change_request.content_before,
                content_after=change_request.content_after,
                change_description=change_request.change_description,
                user_id=current_user.id,
                session_id=change_request.session_id,
                auto_save_enabled=change_request.auto_save_enabled,
                requires_approval=change_request.requires_approval
            )
            change_ids.append(change_id)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "change_ids": change_ids,
                "batch_size": len(change_ids),
                "auto_save_all": request.auto_save_all,
                "requires_approval": request.requires_approval,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to register batch changes", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register batch changes: {e}"
        )


# ============================================================================
# CHANGE APPROVAL ENDPOINTS
# ============================================================================

@router.post("/accept-change/{change_id}")
async def accept_change(
    change_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Accept a specific change"""
    try:
        success = await auto_save_service.accept_change(change_id, current_user.id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Change not found"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "change_id": change_id,
                "status": "accepted",
                "accepted_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to accept change", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to accept change: {e}"
        )


@router.post("/reject-change/{change_id}")
async def reject_change(
    change_id: str,
    reason: str = "",
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Reject a specific change"""
    try:
        success = await auto_save_service.reject_change(change_id, current_user.id, reason)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Change not found"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "change_id": change_id,
                "status": "rejected",
                "rejected_by": current_user.id,
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to reject change", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reject change: {e}"
        )


@router.post("/keep-all-changes")
async def keep_all_changes(
    group_id: Optional[str] = None,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Keep all pending changes (batch operation)"""
    try:
        result = await auto_save_service.keep_all_changes(current_user.id, group_id)
        
        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result.get("error", "Failed to keep all changes")
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "changes_accepted": result["changes_accepted"],
                "change_ids": result["change_ids"],
                "group_id": result.get("group_id"),
                "accepted_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to keep all changes", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to keep all changes: {e}"
        )


@router.post("/reject-all-changes")
async def reject_all_changes(
    reason: str = "",
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Reject all pending changes"""
    try:
        result = await auto_save_service.reject_all_changes(current_user.id, reason)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "changes_rejected": result["changes_rejected"],
                "change_ids": result["change_ids"],
                "rejected_by": current_user.id,
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to reject all changes", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reject all changes: {e}"
        )


# ============================================================================
# STATUS AND QUERY ENDPOINTS
# ============================================================================

@router.get("/pending-changes")
async def get_pending_changes(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get all pending changes for the user"""
    try:
        changes = auto_save_service.get_pending_changes(current_user.id)
        
        # Convert to dict format for JSON response
        changes_data = []
        for change in changes:
            changes_data.append({
                "change_id": change.change_id,
                "file_path": change.file_path,
                "change_type": change.change_type.value,
                "change_description": change.change_description,
                "status": change.status.value,
                "auto_save_enabled": change.auto_save_enabled,
                "requires_approval": change.requires_approval,
                "timestamp": change.timestamp.isoformat(),
                "metadata": change.metadata
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "pending_changes": changes_data,
                "total_count": len(changes_data),
                "user_id": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get pending changes", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get pending changes: {e}"
        )


@router.get("/batch-groups")
async def get_batch_groups(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get all batch groups"""
    try:
        groups = auto_save_service.get_batch_groups()
        
        # Convert to dict format for JSON response
        groups_data = []
        for group in groups:
            changes_data = []
            for change in group.changes:
                changes_data.append({
                    "change_id": change.change_id,
                    "file_path": change.file_path,
                    "change_type": change.change_type.value,
                    "status": change.status.value
                })
            
            groups_data.append({
                "group_id": group.group_id,
                "group_name": group.group_name,
                "changes": changes_data,
                "changes_count": len(changes_data),
                "auto_save_all": group.auto_save_all,
                "requires_approval": group.requires_approval,
                "created_at": group.created_at.isoformat(),
                "metadata": group.metadata
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "batch_groups": groups_data,
                "total_groups": len(groups_data),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get batch groups", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get batch groups: {e}"
        )


@router.get("/change-history")
async def get_change_history(
    limit: int = 100,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get change history"""
    try:
        history = auto_save_service.get_change_history(limit)
        
        # Convert to dict format for JSON response
        history_data = []
        for change in history:
            history_data.append({
                "change_id": change.change_id,
                "file_path": change.file_path,
                "change_type": change.change_type.value,
                "change_description": change.change_description,
                "status": change.status.value,
                "user_id": change.user_id,
                "timestamp": change.timestamp.isoformat(),
                "metadata": change.metadata
            })
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "change_history": history_data,
                "total_count": len(history_data),
                "limit": limit,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get change history", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get change history: {e}"
        )


@router.get("/auto-save-status")
async def get_auto_save_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get auto-save status and configuration"""
    try:
        status_info = auto_save_service.get_auto_save_status()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "auto_save_status": status_info,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to get auto-save status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get auto-save status: {e}"
        )


# ============================================================================
# CONFIGURATION ENDPOINTS
# ============================================================================

@router.put("/config")
async def update_auto_save_config(
    request: AutoSaveConfigRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Update auto-save configuration"""
    try:
        config_updates = {}
        
        if request.enabled is not None:
            config_updates["enabled"] = request.enabled
        if request.interval_seconds is not None:
            config_updates["interval_seconds"] = request.interval_seconds
        if request.max_pending_changes is not None:
            config_updates["max_pending_changes"] = request.max_pending_changes
        if request.auto_approve_safe_changes is not None:
            config_updates["auto_approve_safe_changes"] = request.auto_approve_safe_changes
        if request.backup_enabled is not None:
            config_updates["backup_enabled"] = request.backup_enabled
        if request.compression_enabled is not None:
            config_updates["compression_enabled"] = request.compression_enabled
        
        success = auto_save_service.update_auto_save_config(config_updates)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to update auto-save configuration"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "config_updated": config_updates,
                "updated_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update auto-save config", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update auto-save configuration: {e}"
        )


@router.post("/cleanup")
async def cleanup_old_changes(
    max_age_hours: int = 24,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Clean up old changes from history"""
    try:
        await auto_save_service.cleanup_old_changes(max_age_hours)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "max_age_hours": max_age_hours,
                "cleaned_by": current_user.id,
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error("Failed to cleanup old changes", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cleanup old changes: {e}"
        )

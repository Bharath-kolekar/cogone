"""
Auto-Save and Keep All Changes Models
Data models for auto-save and batch change management
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


class ChangeStatus(str, Enum):
    """Change status options"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    AUTO_SAVED = "auto_saved"


class ChangeType(str, Enum):
    """Change type options"""
    FILE_EDIT = "file_edit"
    FILE_CREATE = "file_create"
    FILE_DELETE = "file_delete"
    CONFIG_UPDATE = "config_update"
    INTEGRATION_UPDATE = "integration_update"
    MODEL_UPDATE = "model_update"
    SERVICE_UPDATE = "service_update"


# ============================================================================
# CORE CHANGE MODELS
# ============================================================================

class ChangeRecord(BaseModel):
    """Record of a change made to the system"""
    change_id: str = Field(..., description="Unique change identifier")
    file_path: str = Field(..., description="Path to the file being changed")
    change_type: ChangeType = Field(..., description="Type of change")
    content_before: Optional[str] = Field(None, description="Content before the change")
    content_after: Optional[str] = Field(None, description="Content after the change")
    change_description: str = Field("", description="Description of the change")
    user_id: Optional[str] = Field(None, description="User who made the change")
    session_id: Optional[str] = Field(None, description="Session identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Change timestamp")
    status: ChangeStatus = Field(ChangeStatus.PENDING, description="Current status of the change")
    auto_save_enabled: bool = Field(True, description="Whether auto-save is enabled for this change")
    requires_approval: bool = Field(False, description="Whether this change requires manual approval")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class BatchChangeGroup(BaseModel):
    """Group of related changes"""
    group_id: str = Field(..., description="Unique group identifier")
    group_name: str = Field(..., description="Name of the batch group")
    changes: List[ChangeRecord] = Field(..., description="Changes in this group")
    created_at: datetime = Field(default_factory=datetime.now, description="Group creation timestamp")
    auto_save_all: bool = Field(True, description="Whether to auto-save all changes in the group")
    requires_approval: bool = Field(False, description="Whether the group requires manual approval")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional group metadata")


# ============================================================================
# REQUEST MODELS
# ============================================================================

class ChangeRegistrationRequest(BaseModel):
    """Request to register a change"""
    file_path: str = Field(..., description="Path to the file being changed")
    change_type: ChangeType = Field(..., description="Type of change")
    content_before: Optional[str] = Field(None, description="Content before the change")
    content_after: Optional[str] = Field(None, description="Content after the change")
    change_description: str = Field("", description="Description of the change")
    auto_save_enabled: bool = Field(True, description="Whether auto-save is enabled")
    requires_approval: bool = Field(False, description="Whether manual approval is required")
    session_id: Optional[str] = Field(None, description="Session identifier")


class BatchChangeRequest(BaseModel):
    """Request for batch change operations"""
    changes: List[ChangeRegistrationRequest] = Field(..., description="List of changes to register")
    group_name: Optional[str] = Field(None, description="Name for the batch group")
    auto_save_all: bool = Field(True, description="Whether to auto-save all changes")
    requires_approval: bool = Field(False, description="Whether the batch requires approval")


class ChangeApprovalRequest(BaseModel):
    """Request to approve/reject changes"""
    change_ids: List[str] = Field(..., description="List of change IDs to approve/reject")
    action: str = Field(..., description="Action to take: 'accept' or 'reject'")
    reason: Optional[str] = Field(None, description="Reason for rejection (if applicable)")


class AutoSaveConfigRequest(BaseModel):
    """Request to update auto-save configuration"""
    enabled: Optional[bool] = Field(None, description="Whether auto-save is enabled")
    interval_seconds: Optional[int] = Field(None, description="Auto-save interval in seconds")
    max_pending_changes: Optional[int] = Field(None, description="Maximum pending changes allowed")
    auto_approve_safe_changes: Optional[bool] = Field(None, description="Whether to auto-approve safe changes")
    backup_enabled: Optional[bool] = Field(None, description="Whether backups are enabled")
    compression_enabled: Optional[bool] = Field(None, description="Whether compression is enabled")


# ============================================================================
# RESPONSE MODELS
# ============================================================================

class ChangeRegistrationResponse(BaseModel):
    """Response for change registration"""
    change_id: str = Field(..., description="Unique change identifier")
    status: str = Field(..., description="Registration status")
    auto_save_enabled: bool = Field(..., description="Whether auto-save is enabled")
    requires_approval: bool = Field(..., description="Whether approval is required")
    timestamp: datetime = Field(default_factory=datetime.now, description="Registration timestamp")


class BatchChangeResponse(BaseModel):
    """Response for batch change operations"""
    change_ids: List[str] = Field(..., description="List of registered change IDs")
    batch_size: int = Field(..., description="Number of changes in the batch")
    auto_save_all: bool = Field(..., description="Whether auto-save is enabled for all")
    requires_approval: bool = Field(..., description="Whether the batch requires approval")
    timestamp: datetime = Field(default_factory=datetime.now, description="Batch creation timestamp")


class ChangeApprovalResponse(BaseModel):
    """Response for change approval operations"""
    change_id: str = Field(..., description="Change identifier")
    status: str = Field(..., description="New status of the change")
    action_by: str = Field(..., description="User who performed the action")
    reason: Optional[str] = Field(None, description="Reason for the action")
    timestamp: datetime = Field(default_factory=datetime.now, description="Action timestamp")


class BatchApprovalResponse(BaseModel):
    """Response for batch approval operations"""
    success: bool = Field(..., description="Whether the operation was successful")
    changes_processed: int = Field(..., description="Number of changes processed")
    change_ids: List[str] = Field(..., description="List of processed change IDs")
    action_by: str = Field(..., description="User who performed the action")
    reason: Optional[str] = Field(None, description="Reason for the action")
    timestamp: datetime = Field(default_factory=datetime.now, description="Action timestamp")


class PendingChangesResponse(BaseModel):
    """Response for pending changes query"""
    pending_changes: List[ChangeRecord] = Field(..., description="List of pending changes")
    total_count: int = Field(..., description="Total number of pending changes")
    user_id: str = Field(..., description="User ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="Query timestamp")


class BatchGroupsResponse(BaseModel):
    """Response for batch groups query"""
    batch_groups: List[BatchChangeGroup] = Field(..., description="List of batch groups")
    total_groups: int = Field(..., description="Total number of batch groups")
    timestamp: datetime = Field(default_factory=datetime.now, description="Query timestamp")


class ChangeHistoryResponse(BaseModel):
    """Response for change history query"""
    change_history: List[ChangeRecord] = Field(..., description="List of historical changes")
    total_count: int = Field(..., description="Total number of historical changes")
    limit: int = Field(..., description="Limit applied to the query")
    timestamp: datetime = Field(default_factory=datetime.now, description="Query timestamp")


class AutoSaveStatusResponse(BaseModel):
    """Response for auto-save status query"""
    enabled: bool = Field(..., description="Whether auto-save is enabled")
    config: Dict[str, Any] = Field(..., description="Auto-save configuration")
    pending_changes: int = Field(..., description="Number of pending changes")
    batch_groups: int = Field(..., description="Number of batch groups")
    total_history: int = Field(..., description="Total number of historical changes")
    auto_save_task_running: bool = Field(..., description="Whether auto-save task is running")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")


class AutoSaveConfigResponse(BaseModel):
    """Response for auto-save configuration update"""
    success: bool = Field(..., description="Whether the update was successful")
    config_updated: Dict[str, Any] = Field(..., description="Configuration values that were updated")
    updated_by: str = Field(..., description="User who updated the configuration")
    timestamp: datetime = Field(default_factory=datetime.now, description="Update timestamp")


class CleanupResponse(BaseModel):
    """Response for cleanup operations"""
    success: bool = Field(..., description="Whether the cleanup was successful")
    max_age_hours: int = Field(..., description="Maximum age of changes that were cleaned up")
    cleaned_by: str = Field(..., description="User who performed the cleanup")
    timestamp: datetime = Field(default_factory=datetime.now, description="Cleanup timestamp")


# ============================================================================
# FEATURE DESCRIPTION MODELS
# ============================================================================

class AutoSaveFeature(BaseModel):
    """Description of auto-save feature"""
    name: str = Field(..., description="Feature name")
    description: str = Field(..., description="Feature description")
    enabled: bool = Field(..., description="Whether the feature is enabled")
    configuration: Dict[str, Any] = Field(..., description="Feature configuration")


class KeepAllChangesFeature(BaseModel):
    """Description of Keep All Changes feature"""
    name: str = Field("Keep All Changes", description="Feature name")
    description: str = Field("Batch operation to accept all pending changes at once", description="Feature description")
    available: bool = Field(..., description="Whether the feature is available")
    pending_count: int = Field(..., description="Number of pending changes")
    batch_groups: int = Field(..., description="Number of batch groups")


class AutoSaveCapabilities(BaseModel):
    """Complete auto-save capabilities"""
    auto_save: AutoSaveFeature = Field(..., description="Auto-save feature")
    keep_all_changes: KeepAllChangesFeature = Field(..., description="Keep All Changes feature")
    change_types: List[ChangeType] = Field(..., description="Supported change types")
    status_options: List[ChangeStatus] = Field(..., description="Available status options")
    endpoints: List[str] = Field(..., description="Available API endpoints")
    timestamp: datetime = Field(default_factory=datetime.now, description="Capabilities timestamp")


# ============================================================================
# ERROR MODELS
# ============================================================================

class AutoSaveError(BaseModel):
    """Error model for auto-save operations"""
    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Error message")
    change_id: Optional[str] = Field(None, description="Related change ID")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class AutoSaveErrorResponse(BaseModel):
    """Error response for auto-save operations"""
    success: bool = Field(False, description="Whether the operation was successful")
    error: AutoSaveError = Field(..., description="Error details")
    suggestions: List[str] = Field(default_factory=list, description="Suggested solutions")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error response timestamp")

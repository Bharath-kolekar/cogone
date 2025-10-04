"""
Auto-Save Service for Smart Coding AI System
Handles automatic saving and batch change management
"""

import structlog
import asyncio
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import os
import uuid

logger = structlog.get_logger()


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


@dataclass
class ChangeRecord:
    """Record of a change made to the system"""
    change_id: str
    file_path: str
    change_type: ChangeType
    content_before: Optional[str] = None
    content_after: Optional[str] = None
    change_description: str = ""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    timestamp: datetime = None
    status: ChangeStatus = ChangeStatus.PENDING
    auto_save_enabled: bool = True
    requires_approval: bool = False
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class BatchChangeGroup:
    """Group of related changes"""
    group_id: str
    group_name: str
    changes: List[ChangeRecord]
    created_at: datetime = None
    auto_save_all: bool = True
    requires_approval: bool = False
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}


class AutoSaveService:
    """Service for managing auto-save and batch changes"""
    
    def __init__(self):
        self.pending_changes: Dict[str, ChangeRecord] = {}
        self.batch_groups: Dict[str, BatchChangeGroup] = {}
        self.auto_save_enabled: bool = True
        self.auto_save_interval: int = 5  # seconds
        self.batch_timeout: int = 30  # seconds
        self.change_history: List[ChangeRecord] = []
        
        # Auto-save configuration
        self.auto_save_config = {
            "enabled": True,
            "interval_seconds": 5,
            "max_pending_changes": 100,
            "auto_approve_safe_changes": True,
            "backup_enabled": True,
            "compression_enabled": False
        }
        
        # Start auto-save background task
        self._auto_save_task = None
        self._start_auto_save_task()
    
    def _start_auto_save_task(self):
        """Start background auto-save task"""
        if self.auto_save_enabled and not self._auto_save_task:
            self._auto_save_task = asyncio.create_task(self._auto_save_loop())
            logger.info("Auto-save background task started")
    
    async def _auto_save_loop(self):
        """Background loop for auto-saving changes"""
        while self.auto_save_enabled:
            try:
                await self._process_auto_save()
                await asyncio.sleep(self.auto_save_interval)
            except Exception as e:
                logger.error("Auto-save loop error", error=str(e))
                await asyncio.sleep(self.auto_save_interval)
    
    async def _process_auto_save(self):
        """Process auto-save for eligible changes"""
        try:
            current_time = datetime.now()
            auto_save_candidates = []
            
            # Find changes eligible for auto-save
            for change_id, change in self.pending_changes.items():
                if (change.status == ChangeStatus.PENDING and 
                    change.auto_save_enabled and
                    not change.requires_approval):
                    
                    # Check if change is old enough for auto-save
                    time_diff = current_time - change.timestamp
                    if time_diff.total_seconds() >= self.auto_save_config["interval_seconds"]:
                        auto_save_candidates.append(change)
            
            # Process auto-save candidates
            for change in auto_save_candidates:
                await self._auto_save_change(change)
                
            logger.debug("Auto-save processed", candidates=len(auto_save_candidates))
            
        except Exception as e:
            logger.error("Failed to process auto-save", error=str(e))
    
    async def _auto_save_change(self, change: ChangeRecord):
        """Auto-save a single change"""
        try:
            # Mark as auto-saved
            change.status = ChangeStatus.AUTO_SAVED
            change.timestamp = datetime.now()
            
            # Add to history
            self.change_history.append(change)
            
            # Remove from pending
            if change.change_id in self.pending_changes:
                del self.pending_changes[change.change_id]
            
            logger.info("Change auto-saved", 
                       change_id=change.change_id,
                       file_path=change.file_path,
                       change_type=change.change_type)
            
        except Exception as e:
            logger.error("Failed to auto-save change", 
                        change_id=change.change_id, error=str(e))
    
    # ============================================================================
    # CHANGE MANAGEMENT
    # ============================================================================
    
    def register_change(self, file_path: str, change_type: ChangeType, 
                       content_before: Optional[str] = None,
                       content_after: Optional[str] = None,
                       change_description: str = "",
                       user_id: Optional[str] = None,
                       session_id: Optional[str] = None,
                       auto_save_enabled: bool = True,
                       requires_approval: bool = False) -> str:
        """Register a new change"""
        try:
            change_id = str(uuid.uuid4())
            
            change = ChangeRecord(
                change_id=change_id,
                file_path=file_path,
                change_type=change_type,
                content_before=content_before,
                content_after=content_after,
                change_description=change_description,
                user_id=user_id,
                session_id=session_id,
                auto_save_enabled=auto_save_enabled,
                requires_approval=requires_approval,
                metadata={
                    "file_hash_before": self._calculate_hash(content_before) if content_before else None,
                    "file_hash_after": self._calculate_hash(content_after) if content_after else None,
                    "change_size": len(content_after or "") - len(content_before or ""),
                    "registered_at": datetime.now().isoformat()
                }
            )
            
            # Add to pending changes
            self.pending_changes[change_id] = change
            
            # Check if we need to create a batch group
            asyncio.create_task(self._check_batch_grouping(change))
            
            logger.info("Change registered", 
                       change_id=change_id,
                       file_path=file_path,
                       change_type=change_type,
                       auto_save_enabled=auto_save_enabled)
            
            return change_id
            
        except Exception as e:
            logger.error("Failed to register change", error=str(e))
            raise
    
    async def _check_batch_grouping(self, change: ChangeRecord):
        """Check if change should be grouped with others"""
        try:
            # Group changes by session and time proximity
            current_time = datetime.now()
            time_window = timedelta(seconds=self.batch_timeout)
            
            # Find existing groups that this change could belong to
            for group_id, group in self.batch_groups.items():
                if (group.auto_save_all and 
                    change.session_id == group.changes[0].session_id and
                    abs((current_time - group.created_at).total_seconds()) <= self.batch_timeout):
                    
                    # Add to existing group
                    group.changes.append(change)
                    logger.info("Change added to existing batch group", 
                               change_id=change.change_id, group_id=group_id)
                    return
            
            # Create new group if this is a batch operation
            if change.metadata.get("is_batch_operation", False):
                group_id = str(uuid.uuid4())
                group_name = f"Batch Changes - {change.change_type.value}"
                
                new_group = BatchChangeGroup(
                    group_id=group_id,
                    group_name=group_name,
                    changes=[change],
                    auto_save_all=change.auto_save_enabled,
                    requires_approval=change.requires_approval
                )
                
                self.batch_groups[group_id] = new_group
                logger.info("New batch group created", 
                           group_id=group_id, change_id=change.change_id)
                
        except Exception as e:
            logger.error("Failed to check batch grouping", error=str(e))
    
    def _calculate_hash(self, content: Optional[str]) -> Optional[str]:
        """Calculate hash of content"""
        if not content:
            return None
        return hashlib.md5(content.encode()).hexdigest()
    
    # ============================================================================
    # APPROVAL MANAGEMENT
    # ============================================================================
    
    async def accept_change(self, change_id: str, user_id: Optional[str] = None) -> bool:
        """Accept a specific change"""
        try:
            if change_id not in self.pending_changes:
                logger.warning("Change not found", change_id=change_id)
                return False
            
            change = self.pending_changes[change_id]
            change.status = ChangeStatus.ACCEPTED
            change.timestamp = datetime.now()
            
            # Add to history
            self.change_history.append(change)
            
            # Remove from pending
            del self.pending_changes[change_id]
            
            logger.info("Change accepted", 
                       change_id=change_id,
                       file_path=change.file_path,
                       user_id=user_id)
            
            return True
            
        except Exception as e:
            logger.error("Failed to accept change", 
                        change_id=change_id, error=str(e))
            return False
    
    async def reject_change(self, change_id: str, user_id: Optional[str] = None, 
                          reason: str = "") -> bool:
        """Reject a specific change"""
        try:
            if change_id not in self.pending_changes:
                logger.warning("Change not found", change_id=change_id)
                return False
            
            change = self.pending_changes[change_id]
            change.status = ChangeStatus.REJECTED
            change.timestamp = datetime.now()
            change.metadata["rejection_reason"] = reason
            change.metadata["rejected_by"] = user_id
            
            # Add to history
            self.change_history.append(change)
            
            # Remove from pending
            del self.pending_changes[change_id]
            
            logger.info("Change rejected", 
                       change_id=change_id,
                       file_path=change.file_path,
                       user_id=user_id,
                       reason=reason)
            
            return True
            
        except Exception as e:
            logger.error("Failed to reject change", 
                        change_id=change_id, error=str(e))
            return False
    
    # ============================================================================
    # BATCH OPERATIONS
    # ============================================================================
    
    async def keep_all_changes(self, user_id: Optional[str] = None, 
                             group_id: Optional[str] = None) -> Dict[str, Any]:
        """Keep all pending changes (batch operation)"""
        try:
            if group_id:
                # Accept all changes in a specific group
                if group_id not in self.batch_groups:
                    return {"success": False, "error": "Group not found"}
                
                group = self.batch_groups[group_id]
                accepted_changes = []
                
                for change in group.changes:
                    if change.status == ChangeStatus.PENDING:
                        change.status = ChangeStatus.ACCEPTED
                        change.timestamp = datetime.now()
                        self.change_history.append(change)
                        accepted_changes.append(change.change_id)
                        
                        if change.change_id in self.pending_changes:
                            del self.pending_changes[change.change_id]
                
                # Remove group
                del self.batch_groups[group_id]
                
                logger.info("Batch group accepted", 
                           group_id=group_id,
                           changes_accepted=len(accepted_changes),
                           user_id=user_id)
                
                return {
                    "success": True,
                    "changes_accepted": len(accepted_changes),
                    "change_ids": accepted_changes,
                    "group_id": group_id
                }
            else:
                # Accept all pending changes
                accepted_changes = []
                
                for change_id, change in list(self.pending_changes.items()):
                    change.status = ChangeStatus.ACCEPTED
                    change.timestamp = datetime.now()
                    self.change_history.append(change)
                    accepted_changes.append(change_id)
                    del self.pending_changes[change_id]
                
                # Clear all batch groups
                self.batch_groups.clear()
                
                logger.info("All pending changes accepted", 
                           changes_accepted=len(accepted_changes),
                           user_id=user_id)
                
                return {
                    "success": True,
                    "changes_accepted": len(accepted_changes),
                    "change_ids": accepted_changes
                }
                
        except Exception as e:
            logger.error("Failed to keep all changes", error=str(e))
            return {"success": False, "error": str(e)}
    
    async def reject_all_changes(self, user_id: Optional[str] = None, 
                               reason: str = "") -> Dict[str, Any]:
        """Reject all pending changes"""
        try:
            rejected_changes = []
            
            for change_id, change in list(self.pending_changes.items()):
                change.status = ChangeStatus.REJECTED
                change.timestamp = datetime.now()
                change.metadata["rejection_reason"] = reason
                change.metadata["rejected_by"] = user_id
                self.change_history.append(change)
                rejected_changes.append(change_id)
                del self.pending_changes[change_id]
            
            # Clear all batch groups
            self.batch_groups.clear()
            
            logger.info("All pending changes rejected", 
                       changes_rejected=len(rejected_changes),
                       user_id=user_id,
                       reason=reason)
            
            return {
                "success": True,
                "changes_rejected": len(rejected_changes),
                "change_ids": rejected_changes
            }
            
        except Exception as e:
            logger.error("Failed to reject all changes", error=str(e))
            return {"success": False, "error": str(e)}
    
    # ============================================================================
    # STATUS AND QUERIES
    # ============================================================================
    
    def get_pending_changes(self, user_id: Optional[str] = None) -> List[ChangeRecord]:
        """Get all pending changes"""
        if user_id:
            return [change for change in self.pending_changes.values() 
                   if change.user_id == user_id]
        return list(self.pending_changes.values())
    
    def get_batch_groups(self) -> List[BatchChangeGroup]:
        """Get all batch groups"""
        return list(self.batch_groups.values())
    
    def get_change_history(self, limit: int = 100) -> List[ChangeRecord]:
        """Get change history"""
        return self.change_history[-limit:]
    
    def get_auto_save_status(self) -> Dict[str, Any]:
        """Get auto-save status and configuration"""
        return {
            "enabled": self.auto_save_enabled,
            "config": self.auto_save_config,
            "pending_changes": len(self.pending_changes),
            "batch_groups": len(self.batch_groups),
            "total_history": len(self.change_history),
            "auto_save_task_running": self._auto_save_task is not None and not self._auto_save_task.done()
        }
    
    # ============================================================================
    # CONFIGURATION
    # ============================================================================
    
    def update_auto_save_config(self, config_updates: Dict[str, Any]) -> bool:
        """Update auto-save configuration"""
        try:
            self.auto_save_config.update(config_updates)
            
            # Update runtime settings
            if "interval_seconds" in config_updates:
                self.auto_save_interval = config_updates["interval_seconds"]
            
            if "enabled" in config_updates:
                self.auto_save_enabled = config_updates["enabled"]
                if self.auto_save_enabled and not self._auto_save_task:
                    self._start_auto_save_task()
                elif not self.auto_save_enabled and self._auto_save_task:
                    self._auto_save_task.cancel()
                    self._auto_save_task = None
            
            logger.info("Auto-save configuration updated", config=config_updates)
            return True
            
        except Exception as e:
            logger.error("Failed to update auto-save config", error=str(e))
            return False
    
    async def cleanup_old_changes(self, max_age_hours: int = 24):
        """Clean up old changes from history"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            
            # Clean up history
            original_count = len(self.change_history)
            self.change_history = [
                change for change in self.change_history 
                if change.timestamp > cutoff_time
            ]
            
            cleaned_count = original_count - len(self.change_history)
            
            logger.info("Old changes cleaned up", 
                       removed_count=cleaned_count,
                       remaining_count=len(self.change_history))
            
        except Exception as e:
            logger.error("Failed to cleanup old changes", error=str(e))


# Global instance
auto_save_service = AutoSaveService()

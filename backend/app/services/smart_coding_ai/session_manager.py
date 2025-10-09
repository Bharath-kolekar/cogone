"""
Session Manager Module
Handles session context management for Smart Coding AI integration

Dependencies: 2 (uuid, ai_integration_types)
Production-grade: Complete implementation with comprehensive error handling
"""

import structlog
import uuid
from typing import Dict, Optional, Any
from datetime import datetime

from app.services.ai_integration_types import AIIntegrationContext

logger = structlog.get_logger(__name__)


class SessionManager:
    """
    Manages integration session contexts
    Provides session creation, retrieval, and update functionality
    """
    
    def __init__(self):
        """Initialize session manager with empty context storage"""
        self.session_contexts: Dict[str, AIIntegrationContext] = {}
        self.session_metadata: Dict[str, Dict[str, Any]] = {}
        logger.info("Session manager initialized")
    
    async def create_session(
        self, 
        user_id: str, 
        project_id: Optional[str] = None,
        initial_metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new integration session
        
        Args:
            user_id: User identifier (required)
            project_id: Optional project identifier
            initial_metadata: Optional initial metadata for the session
            
        Returns:
            str: Unique session identifier
            
        Raises:
            ValueError: If user_id is empty or None
            Exception: For other creation failures (logged but re-raised)
        """
        try:
            # Validate required parameters
            if not user_id:
                logger.error("Cannot create session: user_id is required")
                raise ValueError("user_id is required and cannot be empty")
            
            # Generate unique session ID
            session_id = str(uuid.uuid4())
            
            # Create context with all required fields
            context = AIIntegrationContext(
                user_id=user_id,
                session_id=session_id,
                project_id=project_id,
                metadata=initial_metadata or {}
            )
            
            # Store context
            self.session_contexts[session_id] = context
            
            # Store additional metadata
            self.session_metadata[session_id] = {
                "created_at": datetime.now().isoformat(),
                "last_accessed": datetime.now().isoformat(),
                "access_count": 0,
                "user_id": user_id,
                "project_id": project_id
            }
            
            logger.info("Integration session created", 
                       session_id=session_id, 
                       user_id=user_id,
                       project_id=project_id,
                       total_sessions=len(self.session_contexts))
            
            return session_id
            
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error("Failed to create integration session", 
                        error=str(e),
                        error_type=type(e).__name__,
                        user_id=user_id)
            raise
    
    async def get_context(self, session_id: str) -> Optional[AIIntegrationContext]:
        """
        Get session context by session ID
        
        Args:
            session_id: Session identifier
            
        Returns:
            AIIntegrationContext if found, None otherwise
            
        Raises:
            No exceptions raised - returns None for invalid session
        """
        try:
            if not session_id:
                logger.warning("Attempted to get context with empty session_id")
                return None
            
            context = self.session_contexts.get(session_id)
            
            if context:
                # Update metadata
                if session_id in self.session_metadata:
                    self.session_metadata[session_id]["last_accessed"] = datetime.now().isoformat()
                    self.session_metadata[session_id]["access_count"] += 1
                
                logger.debug("Session context retrieved", 
                           session_id=session_id,
                           user_id=context.user_id)
            else:
                logger.warning("Session context not found", session_id=session_id)
            
            return context
            
        except Exception as e:
            logger.error("Error retrieving session context",
                        error=str(e),
                        error_type=type(e).__name__,
                        session_id=session_id)
            return None
    
    async def update_context(
        self, 
        session_id: str, 
        updates: Dict[str, Any]
    ) -> bool:
        """
        Update session context with new values
        
        Args:
            session_id: Session identifier
            updates: Dictionary of field updates
            
        Returns:
            bool: True if update successful, False otherwise
            
        Raises:
            No exceptions raised - errors logged and False returned
        """
        try:
            # Validate inputs
            if not session_id:
                logger.warning("Attempted to update context with empty session_id")
                return False
            
            if not updates:
                logger.warning("Attempted to update context with no updates", 
                             session_id=session_id)
                return False
            
            # Check if session exists
            if session_id not in self.session_contexts:
                logger.warning("Cannot update: session not found", 
                             session_id=session_id)
                return False
            
            context = self.session_contexts[session_id]
            updated_fields = []
            
            # Update context fields (excluding metadata which is handled separately)
            for key, value in updates.items():
                if key == "metadata":
                    continue  # Handle metadata separately
                
                if hasattr(context, key):
                    setattr(context, key, value)
                    updated_fields.append(key)
                else:
                    logger.warning("Attempted to update non-existent field",
                                 field=key,
                                 session_id=session_id)
            
            # Update metadata if provided
            if "metadata" in updates and isinstance(updates["metadata"], dict):
                context.metadata.update(updates["metadata"])
                updated_fields.append("metadata")
            
            # Update session metadata
            if session_id in self.session_metadata:
                self.session_metadata[session_id]["last_modified"] = datetime.now().isoformat()
            
            logger.info("Session context updated", 
                       session_id=session_id,
                       updated_fields=updated_fields,
                       user_id=context.user_id)
            
            return True
            
        except Exception as e:
            logger.error("Failed to update session context",
                        error=str(e),
                        error_type=type(e).__name__,
                        session_id=session_id)
            return False
    
    async def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and its context
        
        Args:
            session_id: Session identifier
            
        Returns:
            bool: True if deleted, False if not found or error
        """
        try:
            if not session_id:
                logger.warning("Attempted to delete session with empty session_id")
                return False
            
            if session_id in self.session_contexts:
                context = self.session_contexts[session_id]
                del self.session_contexts[session_id]
                
                # Also delete metadata
                if session_id in self.session_metadata:
                    del self.session_metadata[session_id]
                
                logger.info("Session deleted", 
                           session_id=session_id,
                           user_id=context.user_id,
                           remaining_sessions=len(self.session_contexts))
                return True
            else:
                logger.warning("Cannot delete: session not found", 
                             session_id=session_id)
                return False
                
        except Exception as e:
            logger.error("Error deleting session",
                        error=str(e),
                        error_type=type(e).__name__,
                        session_id=session_id)
            return False
    
    def get_active_sessions_count(self) -> int:
        """
        Get count of active sessions
        
        Returns:
            int: Number of active sessions
        """
        return len(self.session_contexts)
    
    def get_user_sessions(self, user_id: str) -> list[str]:
        """
        Get all session IDs for a specific user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of session IDs belonging to the user
        """
        try:
            if not user_id:
                return []
            
            user_sessions = [
                session_id 
                for session_id, context in self.session_contexts.items()
                if context.user_id == user_id
            ]
            
            logger.debug("Retrieved user sessions", 
                        user_id=user_id,
                        session_count=len(user_sessions))
            
            return user_sessions
            
        except Exception as e:
            logger.error("Error retrieving user sessions",
                        error=str(e),
                        user_id=user_id)
            return []
    
    async def cleanup_expired_sessions(
        self, 
        max_age_hours: int = 24
    ) -> int:
        """
        Clean up sessions older than specified age
        
        Args:
            max_age_hours: Maximum session age in hours
            
        Returns:
            int: Number of sessions cleaned up
        """
        try:
            from datetime import timedelta
            
            cleaned_count = 0
            sessions_to_delete = []
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            
            # Identify expired sessions
            for session_id, metadata in self.session_metadata.items():
                created_at_str = metadata.get("created_at")
                if created_at_str:
                    created_at = datetime.fromisoformat(created_at_str)
                    if created_at < cutoff_time:
                        sessions_to_delete.append(session_id)
            
            # Delete expired sessions
            for session_id in sessions_to_delete:
                if await self.delete_session(session_id):
                    cleaned_count += 1
            
            if cleaned_count > 0:
                logger.info("Cleaned up expired sessions",
                           cleaned_count=cleaned_count,
                           max_age_hours=max_age_hours,
                           remaining_sessions=len(self.session_contexts))
            
            return cleaned_count
            
        except Exception as e:
            logger.error("Error during session cleanup",
                        error=str(e),
                        error_type=type(e).__name__)
            return 0
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get session manager status
        
        Returns:
            Dict with status information
        """
        return {
            "active_sessions": len(self.session_contexts),
            "total_metadata_entries": len(self.session_metadata),
            "module": "session_manager",
            "version": "1.0.0"
        }


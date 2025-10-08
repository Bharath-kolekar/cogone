"""
Smart Coding AI Management - Session Memory Manager
Extracted from smart_coding_ai_optimized.py
"""

import structlog
import uuid
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = structlog.get_logger()


class SessionMemoryManager:
    """Manages cross-session context and memory"""
    
    def __init__(self):
        self.session_cache: Dict[str, Dict] = {}
        self.user_contexts: Dict[str, Dict] = {}
        self.project_memories: Dict[str, Dict] = {}
    
    async def create_session_context(self, user_id: str, project_id: str, 
                                   current_file: str, cursor_position: Tuple[int, int],
                                   working_directory: str) -> Dict[str, Any]:
        """Create new session context"""
        session_id = str(uuid.uuid4())
        context = {
            "session_id": session_id,
            "user_id": user_id,
            "project_id": project_id,
            "current_file": current_file,
            "cursor_position": cursor_position,
            "recent_files": [current_file],
            "recent_commands": [],
            "working_directory": working_directory,
            "git_branch": await self._get_git_branch(working_directory),
            "git_commit": await self._get_git_commit(working_directory),
            "last_activity": datetime.now(),
            "session_start": datetime.now()
        }
        
        self.session_cache[session_id] = context
        
        # Update user context
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {}
        self.user_contexts[user_id][session_id] = context
        
        return context
    
    async def update_session_context(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update existing session context"""
        try:
            if session_id in self.session_cache:
                self.session_cache[session_id].update(updates)
                self.session_cache[session_id]["last_activity"] = datetime.now()
                
                # Update user context
                for user_id, sessions in self.user_contexts.items():
                    if session_id in sessions:
                        sessions[session_id].update(updates)
                        break
                
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to update session context: {e}")
            return False
    
    async def get_user_context(self, user_id: str) -> Dict[str, Any]:
        """Get user's current context across all sessions"""
        if user_id in self.user_contexts:
            return self.user_contexts[user_id]
        return {}
    
    async def get_project_memory(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project memory snapshot"""
        return self.project_memories.get(project_id)
    
    async def save_project_memory(self, project_id: str, memory_data: Dict[str, Any]) -> bool:
        """Save project memory snapshot"""
        try:
            self.project_memories[project_id] = memory_data
            return True
        except Exception as e:
            logger.error(f"Failed to save project memory: {e}")
            return False
    
    async def _get_git_branch(self, working_directory: str) -> Optional[str]:
        """Get current git branch"""
        try:
            proc = await asyncio.create_subprocess_exec(
                "git", "branch", "--show-current",
                cwd=working_directory,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=5)
            return stdout.decode().strip() if proc.returncode == 0 else None
        except Exception:
            return None
    
    async def _get_git_commit(self, working_directory: str) -> Optional[str]:
        """Get current git commit hash"""
        try:
            proc = await asyncio.create_subprocess_exec(
                "git", "rev-parse", "HEAD",
                cwd=working_directory,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=5)
            return stdout.decode().strip()[:8] if proc.returncode == 0 else None
        except Exception:
            return None




__all__ = ['SessionMemoryManager']

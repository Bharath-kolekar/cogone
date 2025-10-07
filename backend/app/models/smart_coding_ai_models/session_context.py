"""
SessionContext Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SessionContext(BaseModel):
    """Session context for cross-session memory"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User identifier")
    project_id: str = Field(..., description="Project identifier")
    current_file: str = Field(..., description="Currently active file")
    cursor_position: Tuple[int, int] = Field(..., description="Cursor position (line, column)")
    recent_files: List[str] = Field([], description="Recently accessed files")
    recent_commands: List[str] = Field([], description="Recent commands/actions")
    working_directory: str = Field(..., description="Current working directory")
    git_branch: Optional[str] = Field(None, description="Current git branch")
    git_commit: Optional[str] = Field(None, description="Current git commit")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last activity time")
    session_start: datetime = Field(default_factory=datetime.now, description="Session start time")

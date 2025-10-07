"""
SmartCodingAuthRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SmartCodingAuthRequest(BaseModel):
    """Authentication request for Smart Coding AI operations"""
    user_id: str = Field(..., description="User ID")
    operation: str = Field(..., description="Operation being performed")
    scope: AuthScope = Field(..., description="Authentication scope")
    resource_id: Optional[str] = Field(None, description="Resource ID being accessed")
    project_id: Optional[str] = Field(None, description="Project ID for project-specific operations")
    session_id: Optional[str] = Field(None, description="Session ID for session-specific operations")

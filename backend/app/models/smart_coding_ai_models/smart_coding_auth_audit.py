"""
SmartCodingAuthAudit Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SmartCodingAuthAudit(BaseModel):
    """Authentication audit log for Smart Coding AI"""
    audit_id: str = Field(..., description="Unique audit identifier")
    user_id: str = Field(..., description="User ID")
    operation: str = Field(..., description="Operation performed")
    scope: AuthScope = Field(..., description="Authentication scope")
    resource_id: Optional[str] = Field(None, description="Resource accessed")
    project_id: Optional[str] = Field(None, description="Project ID")
    session_id: Optional[str] = Field(None, description="Session ID")
    authorized: bool = Field(..., description="Whether operation was authorized")
    permission_level: AuthPermission = Field(..., description="Permission level used")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")
    timestamp: datetime = Field(default_factory=datetime.now, description="Operation timestamp")
    duration_ms: Optional[float] = Field(None, description="Operation duration in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if any")

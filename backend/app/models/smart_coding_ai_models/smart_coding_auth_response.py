"""
SmartCodingAuthResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SmartCodingAuthResponse(BaseModel):
    """Authentication response for Smart Coding AI operations"""
    authorized: bool = Field(..., description="Whether operation is authorized")
    permission_level: AuthPermission = Field(..., description="Permission level granted")
    expires_at: datetime = Field(..., description="When authorization expires")
    limitations: Dict[str, Any] = Field(default_factory=dict, description="Operation limitations")
    quota_remaining: Dict[str, int] = Field(default_factory=dict, description="Remaining quota")
    message: Optional[str] = Field(None, description="Authorization message")

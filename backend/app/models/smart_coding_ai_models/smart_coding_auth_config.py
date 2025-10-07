"""
SmartCodingAuthConfig Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SmartCodingAuthConfig(BaseModel):
    """Authentication configuration for Smart Coding AI"""
    user_id: str = Field(..., description="User ID")
    enabled_features: List[str] = Field(default_factory=list, description="Enabled features")
    disabled_features: List[str] = Field(default_factory=list, description="Disabled features")
    permission_overrides: Dict[str, AuthPermission] = Field(default_factory=dict, description="Permission overrides")
    quota_overrides: Dict[str, int] = Field(default_factory=dict, description="Quota overrides")
    session_timeout_minutes: int = Field(60, description="Session timeout in minutes")
    require_2fa_for_admin: bool = Field(True, description="Require 2FA for admin operations")
    allow_api_access: bool = Field(True, description="Allow API access")
    allowed_ip_ranges: List[str] = Field(default_factory=list, description="Allowed IP ranges")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

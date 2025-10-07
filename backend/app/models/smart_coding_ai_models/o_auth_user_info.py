"""
OAuthUserInfo Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OAuthUserInfo(BaseModel):
    """OAuth user information"""
    provider: OAuthProvider = Field(..., description="OAuth provider")
    provider_id: str = Field(..., description="User ID from OAuth provider")
    email: str = Field(..., description="User email")
    name: Optional[str] = Field(None, description="User display name")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    username: Optional[str] = Field(None, description="Username from provider")
    profile_data: Dict[str, Any] = Field(default_factory=dict, description="Additional profile data")

"""
OAuthLoginResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OAuthLoginResponse(BaseModel):
    """OAuth login response"""
    user: User = Field(..., description="User information")
    access_token: str = Field(..., description="Smart Coding AI access token")
    refresh_token: str = Field(..., description="Smart Coding AI refresh token")
    expires_in: int = Field(..., description="Token expiration time")
    oauth_provider: OAuthProvider = Field(..., description="OAuth provider used")
    is_new_user: bool = Field(False, description="Whether this is a new user")
    requires_profile_completion: bool = Field(False, description="Whether profile completion is required")

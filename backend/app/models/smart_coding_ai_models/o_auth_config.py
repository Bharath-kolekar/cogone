"""
OAuthConfig Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OAuthConfig(BaseModel):
    """OAuth configuration for Smart Coding AI"""
    provider: OAuthProvider = Field(..., description="OAuth provider")
    client_id: str = Field(..., description="OAuth client ID")
    client_secret: str = Field(..., description="OAuth client secret")
    redirect_uri: str = Field(..., description="OAuth redirect URI")
    scopes: List[str] = Field(default_factory=list, description="OAuth scopes")
    auth_url: str = Field(..., description="OAuth authorization URL")
    token_url: str = Field(..., description="OAuth token URL")
    user_info_url: str = Field(..., description="OAuth user info URL")
    is_enabled: bool = Field(True, description="Whether OAuth provider is enabled")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

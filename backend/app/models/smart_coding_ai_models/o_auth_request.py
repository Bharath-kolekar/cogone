"""
OAuthRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OAuthRequest(BaseModel):
    """OAuth login request"""
    provider: OAuthProvider = Field(..., description="OAuth provider")
    redirect_uri: Optional[str] = Field(None, description="Redirect URI after authentication")
    state: Optional[str] = Field(None, description="State parameter for security")
    scope: Optional[List[str]] = Field(default_factory=list, description="Requested OAuth scopes")

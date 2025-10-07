"""
OAuthResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OAuthResponse(BaseModel):
    """OAuth response"""
    auth_url: str = Field(..., description="OAuth authorization URL")
    state: str = Field(..., description="State parameter for security")
    expires_at: datetime = Field(..., description="When the auth URL expires")
    provider: OAuthProvider = Field(..., description="OAuth provider")

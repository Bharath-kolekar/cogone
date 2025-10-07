"""
CacheRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheRequest(BaseModel):
    """Cache operation request"""
    operation: CacheOperation = Field(..., description="Cache operation")
    key: Optional[str] = Field(None, description="Cache key")
    value: Optional[Any] = Field(None, description="Value to cache")
    ttl: Optional[int] = Field(None, description="Time to live in seconds")
    namespace: Optional[str] = Field("default", description="Cache namespace")

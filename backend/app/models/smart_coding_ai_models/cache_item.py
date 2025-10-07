"""
CacheItem Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheItem(BaseModel):
    """Cache item"""
    key: str = Field(..., description="Cache key")
    value: Any = Field(..., description="Cached value")
    ttl: Optional[int] = Field(None, description="Time to live in seconds")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    accessed_at: Optional[datetime] = Field(None, description="Last access timestamp")
    access_count: int = Field(0, description="Number of times accessed")
    size_bytes: int = Field(0, description="Size in bytes")

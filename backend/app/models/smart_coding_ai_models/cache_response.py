"""
CacheResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheResponse(BaseModel):
    """Cache operation response"""
    success: bool = Field(..., description="Operation success")
    value: Optional[Any] = Field(None, description="Retrieved value")
    message: str = Field("", description="Response message")
    stats: Optional[CacheStats] = Field(None, description="Cache statistics")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

"""
CacheStats Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheStats(BaseModel):
    """Cache statistics"""
    total_items: int = Field(0, description="Total cached items")
    total_size_bytes: int = Field(0, description="Total cache size in bytes")
    hit_count: int = Field(0, description="Cache hits")
    miss_count: int = Field(0, description="Cache misses")
    hit_rate: float = Field(0.0, description="Cache hit rate")
    eviction_count: int = Field(0, description="Number of evictions")
    memory_usage: float = Field(0.0, description="Memory usage percentage")
    created_at: datetime = Field(default_factory=datetime.now, description="Stats timestamp")

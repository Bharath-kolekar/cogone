"""
QueueStats Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class QueueStats(BaseModel):
    """Queue statistics"""
    queue_name: str = Field(..., description="Queue name")
    total_items: int = Field(0, description="Total items")
    pending_items: int = Field(0, description="Pending items")
    processing_items: int = Field(0, description="Processing items")
    completed_items: int = Field(0, description="Completed items")
    failed_items: int = Field(0, description="Failed items")
    avg_processing_time: float = Field(0.0, description="Average processing time in seconds")
    throughput_per_minute: float = Field(0.0, description="Items processed per minute")
    created_at: datetime = Field(default_factory=datetime.now, description="Stats timestamp")

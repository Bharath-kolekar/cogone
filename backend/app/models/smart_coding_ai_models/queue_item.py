"""
QueueItem Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class QueueItem(BaseModel):
    """Queue item"""
    id: str = Field(..., description="Queue item ID")
    queue_name: str = Field(..., description="Queue name")
    data: Dict[str, Any] = Field(..., description="Queue item data")
    priority: QueuePriority = Field(QueuePriority.NORMAL, description="Item priority")
    status: QueueStatus = Field(QueueStatus.PENDING, description="Item status")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Processing start time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    retry_count: int = Field(0, description="Number of retries")
    max_retries: int = Field(3, description="Maximum retries")
    error_message: Optional[str] = Field(None, description="Error message if failed")

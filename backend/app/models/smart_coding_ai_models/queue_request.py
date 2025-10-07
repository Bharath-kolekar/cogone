"""
QueueRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class QueueRequest(BaseModel):
    """Queue operation request"""
    queue_name: str = Field(..., description="Queue name")
    data: Dict[str, Any] = Field(..., description="Data to queue")
    priority: QueuePriority = Field(QueuePriority.NORMAL, description="Item priority")
    delay: Optional[int] = Field(None, description="Delay in seconds before processing")
    max_retries: int = Field(3, description="Maximum retries")

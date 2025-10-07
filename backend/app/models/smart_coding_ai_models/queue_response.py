"""
QueueResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class QueueResponse(BaseModel):
    """Queue operation response"""
    success: bool = Field(..., description="Operation success")
    item_id: Optional[str] = Field(None, description="Queue item ID")
    message: str = Field("", description="Response message")
    stats: Optional[QueueStats] = Field(None, description="Queue statistics")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

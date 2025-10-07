"""
StreamingCompletionResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class StreamingCompletionResponse(BaseModel):
    """Response for streaming in-line completion"""
    completion_id: str = Field(..., description="Unique completion ID")
    text: str = Field(..., description="Completion text")
    confidence: float = Field(..., description="Confidence score (0-1)")
    is_final: bool = Field(False, description="Whether this is the final completion")
    timestamp: datetime = Field(default_factory=datetime.now, description="Stream timestamp")

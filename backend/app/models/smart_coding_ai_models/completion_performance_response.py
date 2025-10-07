"""
CompletionPerformanceResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CompletionPerformanceResponse(BaseModel):
    """Response for completion performance metrics"""
    response_time: float = Field(..., description="Response time in milliseconds")
    completion_confidence: float = Field(..., description="Completion confidence score")
    completion_accuracy: float = Field(..., description="Completion accuracy score")
    context_relevance: float = Field(..., description="Context relevance score")
    optimizations: Dict[str, Any] = Field(..., description="Performance optimizations")
    cache_hit: bool = Field(..., description="Whether completion was cached")
    memory_usage: float = Field(..., description="Memory usage percentage")
    cpu_usage: float = Field(..., description="CPU usage percentage")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

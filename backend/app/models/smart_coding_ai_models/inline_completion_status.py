"""
InlineCompletionStatus Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class InlineCompletionStatus(BaseModel):
    """Status of in-line completion service"""
    service_active: bool = Field(..., description="Whether service is active")
    supported_languages: List[Language] = Field(..., description="Supported languages")
    completion_count: int = Field(..., description="Total completions generated")
    streaming_completions: int = Field(..., description="Streaming completions active")
    context_aware_completions: int = Field(..., description="Context-aware completions generated")
    intelligent_completions: int = Field(..., description="Intelligent completions generated")
    average_confidence: float = Field(..., description="Average completion confidence")
    average_accuracy: float = Field(..., description="Average completion accuracy")
    cache_size: int = Field(..., description="Completion cache size")
    performance_score: float = Field(..., description="Performance score (0-1)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")

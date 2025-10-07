"""
ContextAwareCompletionResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ContextAwareCompletionResponse(BaseModel):
    """Response for context-aware completions"""
    completions: List[InlineCompletionResponse] = Field(..., description="List of completions")
    total_count: int = Field(..., description="Total number of completions")
    language: str = Field(..., description="Programming language")
    context_analysis: Dict[str, Any] = Field(..., description="Context analysis results")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

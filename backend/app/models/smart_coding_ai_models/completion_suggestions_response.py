"""
CompletionSuggestionsResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CompletionSuggestionsResponse(BaseModel):
    """Response for completion suggestions"""
    suggestions: List[InlineCompletionResponse] = Field(..., description="List of suggestions")
    total_count: int = Field(..., description="Total number of suggestions")
    language: str = Field(..., description="Programming language")
    suggestion_types: List[str] = Field(..., description="Types of suggestions generated")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

"""
IntelligentCompletionResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class IntelligentCompletionResponse(BaseModel):
    """Response for intelligent completion"""
    completion: InlineCompletionResponse = Field(..., description="Intelligent completion")
    context_analysis: Dict[str, Any] = Field(..., description="Context analysis results")
    intelligence_score: float = Field(..., description="Intelligence score (0-1)")
    analysis_depth: str = Field(..., description="Analysis depth used")
    optimization_applied: List[str] = Field(..., description="Optimizations applied")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

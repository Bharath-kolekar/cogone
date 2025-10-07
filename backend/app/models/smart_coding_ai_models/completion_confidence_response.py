"""
CompletionConfidenceResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CompletionConfidenceResponse(BaseModel):
    """Response for completion confidence scoring"""
    confidence_score: float = Field(..., description="Confidence score (0-1)")
    factors: Dict[str, float] = Field(..., description="Confidence factors")
    recommendations: List[str] = Field(..., description="Improvement recommendations")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

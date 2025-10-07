"""
PatternMatch Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PatternMatch(BaseModel):
    """Pattern match model"""
    pattern_type: str
    match_score: float
    confidence: float
    relevance: float
    timestamp: datetime

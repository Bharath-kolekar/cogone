"""
CodeCompletionResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodeCompletionResponse(BaseModel):
    """Code completion response model"""
    completions: List[CodeCompletion]
    total_count: int
    language: Language
    timestamp: datetime

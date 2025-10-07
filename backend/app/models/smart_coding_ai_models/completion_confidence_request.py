"""
CompletionConfidenceRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CompletionConfidenceRequest(BaseModel):
    """Request for completion confidence scoring"""
    completion: InlineCompletionResponse = Field(..., description="Completion to score")
    context: InlineCompletionRequest = Field(..., description="Completion context")

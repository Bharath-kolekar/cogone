"""
IntegratedAIResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class IntegratedAIResponse:
    """Response from integrated AI system"""
    response_id: str
    primary_response: Any
    supporting_responses: Dict[str, Any]
    confidence: float
    integration_metadata: Dict[str, Any]
    timestamp: datetime

"""
MLPrediction Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MLPrediction(BaseModel):
    """ML prediction model"""
    prediction_type: str
    confidence: float
    accuracy: float
    model_version: str
    timestamp: datetime

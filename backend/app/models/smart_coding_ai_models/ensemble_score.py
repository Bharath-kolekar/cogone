"""
EnsembleScore Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class EnsembleScore(BaseModel):
    """Ensemble score model"""
    confidence_weight: float
    accuracy_weight: float
    context_weight: float
    semantic_weight: float
    pattern_weight: float
    ml_weight: float
    total_score: float

"""
OptimizationTrigger Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OptimizationTrigger(BaseModel):
    """Optimization trigger model"""
    optimization_triggered: bool
    optimization_level: AccuracyLevel
    target_accuracy: float
    strategies_activated: int
    timestamp: datetime

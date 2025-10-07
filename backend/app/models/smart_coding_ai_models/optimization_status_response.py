"""
OptimizationStatusResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OptimizationStatusResponse(BaseModel):
    """Optimization status response model"""
    optimization_active: bool
    accuracy_target: float
    current_accuracy: float
    optimization_strategies: List[OptimizationStrategy]
    performance_metrics: Dict[str, float]
    optimization_level: AccuracyLevel
    timestamp: datetime

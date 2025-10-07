"""
EnsembleOptimization Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class EnsembleOptimization(BaseModel):
    """Ensemble optimization model"""
    optimization_id: str
    strategies_combined: List[OptimizationStrategy]
    ensemble_score: float
    accuracy_improvement: float
    performance_improvement: float
    timestamp: datetime

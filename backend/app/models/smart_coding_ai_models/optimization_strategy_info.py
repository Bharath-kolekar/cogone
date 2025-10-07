"""
OptimizationStrategyInfo Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OptimizationStrategyInfo(BaseModel):
    """Optimization strategy information model"""
    strategy: OptimizationStrategy
    description: str
    accuracy_boost: float
    weight: float
    active: bool

"""
OptimizedSuccessMetrics Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OptimizedSuccessMetrics:
    """Optimized success metrics model"""
    metric_id: str
    metric_type: SuccessMetricType
    current_value: float
    target_value: float
    optimization_level: OptimizationLevel
    improvement_potential: float
    optimization_strategy: List[str]
    expected_improvement: float
    created_at: datetime
    updated_at: Optional[datetime] = None

"""
PerformanceMetricsResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PerformanceMetricsResponse(BaseModel):
    """Performance metrics response model"""
    response_times: Dict[str, int]  # milliseconds
    accuracy_metrics: Dict[str, float]
    optimization_metrics: Dict[str, float]
    timestamp: datetime

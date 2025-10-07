"""
PerformanceReport Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PerformanceReport:
    """Performance analysis report"""
    report_id: str
    component_id: str
    period_start: datetime
    period_end: datetime
    total_requests: int
    success_rate: float
    average_response_time: float
    error_rate: float
    throughput: float
    recommendations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

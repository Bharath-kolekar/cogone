"""
SystemHealth Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SystemHealth:
    """System health status"""
    overall_status: ComponentStatus
    component_statuses: Dict[str, ComponentStatus]
    critical_alerts: int
    warnings: int
    uptime_percentage: float
    last_updated: datetime = field(default_factory=datetime.now)
    recommendations: List[str] = field(default_factory=list)

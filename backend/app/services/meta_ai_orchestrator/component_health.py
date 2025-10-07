"""
ComponentHealth Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ComponentHealth:
    """Component health data"""
    component_id: str
    status: ComponentHealthStatus
    health_score: float
    last_check: datetime
    issues: List[str]
    metrics: Dict[str, Any]

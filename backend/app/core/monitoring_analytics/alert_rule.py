"""
AlertRule Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AlertRule:
    """Alert rule configuration"""
    rule_id: str
    name: str
    metric_name: str
    condition: str  # e.g., "value > 100"
    severity: AlertSeverity
    enabled: bool = True
    cooldown_minutes: int = 5
    last_triggered: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

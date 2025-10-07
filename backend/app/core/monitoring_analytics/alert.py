"""
Alert Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class Alert:
    """Alert instance"""
    alert_id: str
    rule_id: str
    component_id: str
    severity: AlertSeverity
    message: str
    metric_value: Union[int, float, str]
    triggered_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

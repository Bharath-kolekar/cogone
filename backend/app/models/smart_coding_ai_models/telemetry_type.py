"""
TelemetryType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TelemetryType(str, Enum):
    """Telemetry types"""
    METRIC = "metric"
    EVENT = "event"
    LOG = "log"
    TRACE = "trace"
    PERFORMANCE = "performance"
    ERROR = "error"

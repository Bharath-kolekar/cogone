"""
TelemetryRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TelemetryRequest(BaseModel):
    """Telemetry request"""
    metrics: List[TelemetryMetric] = Field(default_factory=list, description="Metrics to record")
    events: List[TelemetryEvent] = Field(default_factory=list, description="Events to record")
    batch_size: int = Field(100, description="Batch size for processing")

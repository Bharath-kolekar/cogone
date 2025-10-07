"""
TelemetryMetric Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TelemetryMetric(BaseModel):
    """Telemetry metric"""
    name: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    type: TelemetryType = Field(TelemetryType.METRIC, description="Telemetry type")
    level: TelemetryLevel = Field(TelemetryLevel.INFO, description="Telemetry level")
    tags: Dict[str, str] = Field(default_factory=dict, description="Metric tags")
    timestamp: datetime = Field(default_factory=datetime.now, description="Metric timestamp")
    source: str = Field("smart_coding_ai", description="Source system")
    user_id: Optional[str] = Field(None, description="User ID if applicable")
    session_id: Optional[str] = Field(None, description="Session ID if applicable")

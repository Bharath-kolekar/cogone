"""
TelemetryResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TelemetryResponse(BaseModel):
    """Telemetry response"""
    success: bool = Field(..., description="Operation success")
    metrics_recorded: int = Field(0, description="Number of metrics recorded")
    events_recorded: int = Field(0, description="Number of events recorded")
    message: str = Field("", description="Response message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

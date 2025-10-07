"""
TelemetryEvent Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TelemetryEvent(BaseModel):
    """Telemetry event"""
    event_name: str = Field(..., description="Event name")
    event_data: Dict[str, Any] = Field(..., description="Event data")
    type: TelemetryType = Field(TelemetryType.EVENT, description="Telemetry type")
    level: TelemetryLevel = Field(TelemetryLevel.INFO, description="Telemetry level")
    tags: Dict[str, str] = Field(default_factory=dict, description="Event tags")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")
    source: str = Field("smart_coding_ai", description="Source system")
    user_id: Optional[str] = Field(None, description="User ID if applicable")
    session_id: Optional[str] = Field(None, description="Session ID if applicable")

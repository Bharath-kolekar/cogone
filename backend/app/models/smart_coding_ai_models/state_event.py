"""
StateEvent Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class StateEvent(BaseModel):
    """State event for StateManager"""
    event_id: str = Field(..., description="Unique event identifier")
    entity_id: str = Field(..., description="Entity ID")
    entity_type: str = Field(..., description="Entity type")
    event_type: str = Field(..., description="Event type")
    state_type: StateType = Field(..., description="State type")
    from_state: Optional[str] = Field(None, description="Source state")
    to_state: Optional[str] = Field(None, description="Target state")
    event_data: Dict[str, Any] = Field(default_factory=dict, description="Event data")
    user_id: Optional[str] = Field(None, description="User who triggered the event")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")
    correlation_id: Optional[str] = Field(None, description="Correlation ID for related events")

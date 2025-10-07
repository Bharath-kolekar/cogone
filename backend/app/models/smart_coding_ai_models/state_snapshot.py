"""
StateSnapshot Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class StateSnapshot(BaseModel):
    """State snapshot for StateManager"""
    snapshot_id: str = Field(..., description="Unique snapshot identifier")
    entity_id: str = Field(..., description="Entity ID")
    entity_type: str = Field(..., description="Entity type")
    state_type: StateType = Field(..., description="State type")
    current_state: str = Field(..., description="Current state")
    state_data: Dict[str, Any] = Field(default_factory=dict, description="State data")
    previous_state: Optional[str] = Field(None, description="Previous state")
    status: StateStatus = Field(StateStatus.ACTIVE, description="State status")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")

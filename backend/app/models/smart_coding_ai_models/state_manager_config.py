"""
StateManagerConfig Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class StateManagerConfig(BaseModel):
    """StateManager configuration"""
    config_id: str = Field(..., description="Unique config identifier")
    state_type: StateType = Field(..., description="State type")
    initial_state: str = Field(..., description="Initial state")
    allowed_transitions: List[StateTransition] = Field(default_factory=list, description="Allowed transitions")
    state_timeouts: Dict[str, int] = Field(default_factory=dict, description="State timeouts in seconds")
    persistence_config: Dict[str, Any] = Field(default_factory=dict, description="Persistence configuration")
    notification_config: Dict[str, Any] = Field(default_factory=dict, description="Notification configuration")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

"""
StateTransition Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class StateTransition(BaseModel):
    """State transition definition"""
    transition_id: str = Field(..., description="Unique transition identifier")
    from_state: str = Field(..., description="Source state")
    to_state: str = Field(..., description="Target state")
    condition: str = Field(..., description="Transition condition")
    action: str = Field(..., description="Action to perform during transition")
    permissions_required: List[str] = Field(default_factory=list, description="Required permissions")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

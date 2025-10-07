"""
RBACPolicy Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RBACPolicy(BaseModel):
    """RBAC Policy definition"""
    policy_id: str = Field(..., description="Unique policy identifier")
    policy_name: str = Field(..., description="Policy name")
    description: str = Field(..., description="Policy description")
    rules: List[Dict[str, Any]] = Field(default_factory=list, description="Policy rules")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Policy conditions")
    effect: str = Field("allow", description="Policy effect (allow/deny)")
    priority: int = Field(100, description="Policy priority")
    is_active: bool = Field(True, description="Whether policy is active")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

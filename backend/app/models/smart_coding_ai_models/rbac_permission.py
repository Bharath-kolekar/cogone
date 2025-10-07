"""
RBACPermission Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RBACPermission(BaseModel):
    """RBAC Permission definition"""
    permission_id: str = Field(..., description="Unique permission identifier")
    permission_name: str = Field(..., description="Permission name")
    resource_type: ResourceType = Field(..., description="Resource type")
    action_type: ActionType = Field(..., description="Action type")
    scope: str = Field(..., description="Permission scope")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Permission conditions")
    description: str = Field(..., description="Permission description")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

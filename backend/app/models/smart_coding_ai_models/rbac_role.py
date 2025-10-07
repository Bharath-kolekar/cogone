"""
RBACRole Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RBACRole(BaseModel):
    """RBAC Role definition"""
    role_id: str = Field(..., description="Unique role identifier")
    role_name: str = Field(..., description="Role name")
    role_type: RoleType = Field(..., description="Role type")
    description: str = Field(..., description="Role description")
    permissions: List[str] = Field(default_factory=list, description="Role permissions")
    resource_access: Dict[ResourceType, List[ActionType]] = Field(default_factory=dict, description="Resource access matrix")
    quota_limits: Dict[str, int] = Field(default_factory=dict, description="Quota limits for this role")
    is_system_role: bool = Field(False, description="Whether this is a system-defined role")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

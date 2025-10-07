"""
RBACAssignment Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RBACAssignment(BaseModel):
    """RBAC Role assignment"""
    assignment_id: str = Field(..., description="Unique assignment identifier")
    user_id: str = Field(..., description="User ID")
    role_id: str = Field(..., description="Role ID")
    resource_id: Optional[str] = Field(None, description="Specific resource ID (for resource-specific roles)")
    resource_type: Optional[ResourceType] = Field(None, description="Resource type")
    granted_by: str = Field(..., description="User ID who granted this role")
    granted_at: datetime = Field(default_factory=datetime.now, description="Grant timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    is_active: bool = Field(True, description="Whether assignment is active")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

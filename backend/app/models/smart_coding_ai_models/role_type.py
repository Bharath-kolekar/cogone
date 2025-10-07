"""
RoleType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RoleType(str, Enum):
    """Role types for Smart Coding AI RBAC"""
    VIEWER = "viewer"
    DEVELOPER = "developer"
    ADMIN = "admin"
    OWNER = "owner"
    GUEST = "guest"
    COLLABORATOR = "collaborator"
    AUDITOR = "auditor"

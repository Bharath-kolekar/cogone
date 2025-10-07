"""
ResourceType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ResourceType(str, Enum):
    """Resource types for RBAC"""
    PROJECT = "project"
    FILE = "file"
    SESSION = "session"
    MEMORY = "memory"
    COMPLETION = "completion"
    ANALYSIS = "analysis"
    CONFIG = "config"
    USER = "user"

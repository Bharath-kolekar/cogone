"""
CacheType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheType(str, Enum):
    """Cache types for Smart Coding AI"""
    REDIS = "redis"
    MEMORY = "memory"
    FILE = "file"
    DATABASE = "database"

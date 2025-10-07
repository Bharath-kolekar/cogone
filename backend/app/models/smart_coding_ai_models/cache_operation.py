"""
CacheOperation Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CacheOperation(str, Enum):
    """Cache operations"""
    GET = "get"
    SET = "set"
    DELETE = "delete"
    CLEAR = "clear"
    EXISTS = "exists"
    KEYS = "keys"
    STATS = "stats"

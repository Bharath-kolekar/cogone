"""
AuthScope Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AuthScope(str, Enum):
    """Authentication scopes for Smart Coding AI"""
    COMPLETION = "completion"
    MEMORY = "memory"
    ANALYSIS = "analysis"
    SESSION = "session"
    ADMIN = "admin"

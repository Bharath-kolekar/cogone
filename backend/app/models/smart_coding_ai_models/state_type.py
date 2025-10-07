"""
StateType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class StateType(str, Enum):
    """State types for StateManager"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    SESSION = "session"
    PROJECT = "project"
    MEMORY = "memory"
    COMPLETION = "completion"
    ANALYSIS = "analysis"
    USER_PREFERENCES = "user_preferences"
    SYSTEM_CONFIG = "system_config"

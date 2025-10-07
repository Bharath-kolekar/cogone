"""
AgentModeStatus Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AgentModeStatus(str, Enum):
    """Agent Mode status"""
    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    TESTING = "testing"
    COMPLETED = "completed"
    ERROR = "error"
    ROLLED_BACK = "rolled_back"

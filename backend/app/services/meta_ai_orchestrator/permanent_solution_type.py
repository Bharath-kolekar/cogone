"""
PermanentSolutionType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class PermanentSolutionType(str, Enum):
    """Permanent solution types"""
    CODE_REFACTOR = "code_refactor"
    ARCHITECTURE_IMPROVEMENT = "architecture_improvement"
    RESOURCE_OPTIMIZATION = "resource_optimization"
    PROCESS_ENHANCEMENT = "process_enhancement"
    SYSTEM_UPGRADE = "system_upgrade"

"""
TaskComplexity Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TaskComplexity(str, Enum):
    """Task complexity levels"""
    SIMPLE = "simple"           # Basic operations
    MODERATE = "moderate"       # Standard coordination
    COMPLEX = "complex"         # Multi-component coordination
    CRITICAL = "critical"       # Strategic decisions
    SUPREME = "supreme"         # Meta-level orchestration

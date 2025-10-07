"""
RepairType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RepairType(str, Enum):
    """AI diagram repair types"""
    SYNTAX_FIX = "syntax_fix"
    LOGIC_CORRECTION = "logic_correction"
    OPTIMIZATION = "optimization"
    ENHANCEMENT = "enhancement"
    VALIDATION = "validation"
    COMPLETION = "completion"
    GANTT = "gantt"
    PIE = "pie"
    GITGRAPH = "gitgraph"
    MINDMAP = "mindmap"
    TIMELINE = "timeline"
    QUADRANT = "quadrant"
    REQUIREMENT = "requirement"

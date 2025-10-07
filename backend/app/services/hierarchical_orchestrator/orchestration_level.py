"""
OrchestrationLevel Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OrchestrationLevel(str, Enum):
    """Orchestration hierarchy levels"""
    STRATEGIC = "strategic"      # Meta-level decisions and governance
    TACTICAL = "tactical"        # Service coordination and workflow
    EXECUTION = "execution"      # Multi-agent consensus and execution
    SMARTY = "smarty"            # Smart Coding AI specialized tasks
    QUALITY = "quality"          # Validation and compliance
    OPERATIONS = "operations"    # Basic coordination and monitoring

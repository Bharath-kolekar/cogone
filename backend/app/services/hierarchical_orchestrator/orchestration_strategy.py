"""
OrchestrationStrategy Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OrchestrationStrategy(str, Enum):
    """Orchestration strategies"""
    SINGLE_ORCHESTRATOR = "single"           # Use one orchestrator
    PARALLEL_PROCESSING = "parallel"         # Multiple orchestrators in parallel
    HIERARCHICAL_CASCADE = "cascade"         # Flow through hierarchy levels
    CONSENSUS_VALIDATION = "consensus"       # Multiple orchestrators validate
    ADAPTIVE_ROUTING = "adaptive"            # Dynamic routing based on load

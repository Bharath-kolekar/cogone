"""
LoadBalancingConfig Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class LoadBalancingConfig:
    """Load balancing configuration"""
    max_parallel_tasks: int = 10
    load_threshold: float = 0.8  # Switch to different orchestrator if load > 80%
    performance_window: int = 100  # Tasks to consider for performance metrics
    adaptive_routing_enabled: bool = True
    consensus_required_for_complexity: TaskComplexity = TaskComplexity.COMPLEX

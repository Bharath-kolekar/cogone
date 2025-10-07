"""
OrchestratorMetrics Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OrchestratorMetrics:
    """Performance metrics for each orchestrator"""
    orchestrator_name: str
    level: OrchestrationLevel
    total_tasks: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    average_execution_time: float = 0.0
    average_confidence: float = 0.0
    success_rate: float = 0.0
    last_used: Optional[datetime] = None
    current_load: float = 0.0  # 0.0 to 1.0

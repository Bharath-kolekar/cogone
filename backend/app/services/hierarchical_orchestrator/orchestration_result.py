"""
OrchestrationResult Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OrchestrationResult:
    """Result from hierarchical orchestration"""
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    orchestrator_used: str = ""
    orchestration_level: OrchestrationLevel = OrchestrationLevel.OPERATIONS
    strategy_used: OrchestrationStrategy = OrchestrationStrategy.SINGLE_ORCHESTRATOR
    success: bool = False
    result_data: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    confidence_score: float = 0.0
    validation_passed: bool = False
    consensus_reached: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    error_message: Optional[str] = None

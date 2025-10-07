"""
AgentTask Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AgentTask:
    """Represents an agent task"""
    task_id: str
    user_request: str
    status: AgentModeStatus
    changes: List[CodeChange]
    progress: float
    current_step: str
    analysis_results: Dict[str, Any]
    execution_plan: List[str]
    test_results: Dict[str, Any]
    rollback_data: Dict[str, Any]
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

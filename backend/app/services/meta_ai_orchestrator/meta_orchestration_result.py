"""
MetaOrchestrationResult Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MetaOrchestrationResult:
    """Meta orchestration result"""
    result_id: str
    task_id: str
    component_id: str
    status: str
    success: bool
    metrics: Dict[str, Any]
    execution_time: float
    created_at: datetime
    error_message: Optional[str] = None

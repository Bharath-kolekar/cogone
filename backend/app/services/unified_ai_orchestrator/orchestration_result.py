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
    """Orchestration result structure"""
    result_id: str
    task_id: str
    component_id: str
    status: str
    success: bool
    metrics: Dict[str, Any]
    execution_time: float
    created_at: datetime
    validation_result: Optional[ValidationResult] = None
    error_message: Optional[str] = None

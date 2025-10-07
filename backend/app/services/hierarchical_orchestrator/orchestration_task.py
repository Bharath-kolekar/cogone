"""
OrchestrationTask Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OrchestrationTask:
    """Task for hierarchical orchestration"""
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_type: str = ""
    complexity: TaskComplexity = TaskComplexity.MODERATE
    requirements: Dict[str, Any] = field(default_factory=dict)
    priority: int = 5  # 1-10, 10 being highest
    deadline: Optional[datetime] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

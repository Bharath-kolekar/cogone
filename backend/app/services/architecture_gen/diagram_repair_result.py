"""
DiagramRepairResult Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DiagramRepairResult:
    """Result of AI diagram repair"""
    original_diagram: str
    repaired_diagram: str
    repair_type: RepairType
    issues_found: List[str]
    fixes_applied: List[str]
    improvements: List[str]
    confidence_score: float
    validation_passed: bool
    performance_metrics: Dict[str, float]
    created_at: datetime = field(default_factory=datetime.now)

"""
DiagramRepairRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DiagramRepairRequest:
    """Request for AI diagram repair"""
    diagram_content: str
    diagram_type: DiagramType
    repair_type: RepairType
    issues: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    context: Optional[Dict[str, Any]] = None

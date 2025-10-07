"""
ComponentIssue Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ComponentIssue:
    """Component issue tracking"""
    issue_id: str
    component_id: str
    issue_type: str
    severity: EscalationLevel
    description: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

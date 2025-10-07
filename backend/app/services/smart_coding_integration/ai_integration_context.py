"""
AIIntegrationContext Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AIIntegrationContext:
    """Context for AI integration operations"""
    user_id: str
    session_id: Optional[str] = None
    project_id: Optional[str] = None
    request_id: Optional[str] = None
    operation_type: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.request_id:
            self.request_id = str(uuid.uuid4())

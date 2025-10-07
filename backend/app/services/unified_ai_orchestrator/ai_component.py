"""
AIComponent Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AIComponent:
    """AI Component definition with enhanced capabilities"""
    component_id: str
    name: str
    service_class: Optional[Any] = None
    instance: Optional[Any] = None
    status: ComponentStatus = ComponentStatus.UNKNOWN
    capabilities: List[str] = None
    health_check: Optional[Callable] = None
    last_health_check: Optional[datetime] = None
    error_count: int = 0
    success_count: int = 0
    avg_response_time: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.metadata is None:
            self.metadata = {}

"""
ArchitectureComponent Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ArchitectureComponent:
    """Architecture component definition"""
    component_id: str
    name: str
    component_type: ComponentType
    description: str
    responsibilities: List[str]
    interfaces: List[str]
    dependencies: List[str]
    properties: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    position: Tuple[int, int] = (0, 0)
    created_at: datetime = field(default_factory=datetime.now)

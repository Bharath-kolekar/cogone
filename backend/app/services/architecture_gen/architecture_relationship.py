"""
ArchitectureRelationship Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ArchitectureRelationship:
    """Architecture relationship definition"""
    relationship_id: str
    source_component: str
    target_component: str
    relationship_type: RelationshipType
    description: str
    properties: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

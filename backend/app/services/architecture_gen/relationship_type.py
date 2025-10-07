"""
RelationshipType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RelationshipType(str, Enum):
    """Relationship types"""
    DEPENDS_ON = "depends_on"
    COMMUNICATES_WITH = "communicates_with"
    AGGREGATES = "aggregates"
    COMPOSES = "composes"
    INHERITS = "inherits"
    IMPLEMENTS = "implements"
    USES = "uses"
    CALLS = "calls"
    STORES = "stores"
    CACHES = "caches"
    LOADS = "loads"
    MONITORS = "monitors"
    COORDINATES = "coordinates"
    MANAGES = "manages"
    ROUTES_TO = "routes_to"
    PUBLISHES_TO = "publishes_to"
    STORES_IN = "stores_in"

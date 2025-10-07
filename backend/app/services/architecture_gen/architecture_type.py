"""
ArchitectureType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ArchitectureType(str, Enum):
    """Architecture types"""
    MICROSERVICES = "microservices"
    MONOLITH = "monolith"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    CLEAN_ARCHITECTURE = "clean_architecture"
    DDD = "domain_driven_design"
    CQRS = "cqrs"
    EVENT_SOURCING = "event_sourcing"
    SWARM_AI = "swarm_ai"
    MULTI_AGENT = "multi_agent"

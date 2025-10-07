"""
ComponentType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ComponentType(str, Enum):
    """Component types"""
    SERVICE = "service"
    DATABASE = "database"
    API = "api"
    QUEUE = "queue"
    CACHE = "cache"
    LOAD_BALANCER = "load_balancer"
    GATEWAY = "gateway"
    AUTHENTICATION = "authentication"
    MONITORING = "monitoring"
    LOGGING = "logging"
    AI_AGENT = "ai_agent"
    SWARM = "swarm"
    ORCHESTRATOR = "orchestrator"

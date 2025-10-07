"""
QueueType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class QueueType(str, Enum):
    """Queue types"""
    REDIS = "redis"
    MEMORY = "memory"
    DATABASE = "database"
    RABBITMQ = "rabbitmq"
    SQS = "sqs"

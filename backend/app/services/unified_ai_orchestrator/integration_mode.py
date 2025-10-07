"""
IntegrationMode Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class IntegrationMode(str, Enum):
    """Integration mode options"""
    SYNC = "synchronous"
    ASYNC = "asynchronous"
    PARALLEL = "parallel"
    PIPELINE = "pipeline"

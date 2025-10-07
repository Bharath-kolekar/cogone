"""
ModelStatus Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ModelStatus(BaseModel):
    """Model status model"""
    loaded: bool
    accuracy: float
    last_trained: datetime
    status: str

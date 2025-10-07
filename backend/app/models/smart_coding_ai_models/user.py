"""
User Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


    class User(BaseModel):
        id: str
        email: str
        name: Optional[str] = None

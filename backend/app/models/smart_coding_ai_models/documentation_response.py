"""
DocumentationResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DocumentationResponse(BaseModel):
    """Documentation response model"""
    documentation: Documentation
    language: Language
    timestamp: datetime

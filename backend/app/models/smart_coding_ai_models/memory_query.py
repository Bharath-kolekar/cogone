"""
MemoryQuery Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MemoryQuery(BaseModel):
    """Query for memory system"""
    query_type: str = Field(..., description="Type of query")
    query_text: str = Field(..., description="Query text")
    filters: Dict[str, Any] = Field({}, description="Query filters")
    limit: int = Field(100, description="Maximum results")
    include_context: bool = Field(True, description="Include context in results")

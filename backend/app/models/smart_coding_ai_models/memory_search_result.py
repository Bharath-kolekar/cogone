"""
MemorySearchResult Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MemorySearchResult(BaseModel):
    """Memory search result"""
    result_id: str = Field(..., description="Unique result identifier")
    result_type: str = Field(..., description="Type of result")
    content: str = Field(..., description="Result content")
    file_path: str = Field(..., description="File path")
    line_number: Optional[int] = Field(None, description="Line number")
    confidence: float = Field(..., description="Search confidence")
    context: Dict[str, Any] = Field({}, description="Additional context")
    timestamp: datetime = Field(default_factory=datetime.now, description="Result timestamp")

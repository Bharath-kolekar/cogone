"""
CodingPattern Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodingPattern(BaseModel):
    """Coding pattern representation"""
    pattern_id: str = Field(..., description="Unique pattern identifier")
    pattern_type: str = Field(..., description="Type of pattern (function, class, etc.)")
    pattern_name: str = Field(..., description="Pattern name")
    pattern_code: str = Field(..., description="Pattern code snippet")
    language: str = Field(..., description="Programming language")
    file_path: str = Field(..., description="File where pattern was found")
    line_number: int = Field(..., description="Line number where pattern starts")
    context: str = Field(..., description="Surrounding context")
    frequency: int = Field(1, description="How often this pattern appears")
    complexity: float = Field(..., description="Pattern complexity score")
    dependencies: List[str] = Field([], description="Pattern dependencies")
    related_patterns: List[str] = Field([], description="Related pattern IDs")
    last_seen: datetime = Field(default_factory=datetime.now, description="Last time pattern was seen")
    created_at: datetime = Field(default_factory=datetime.now, description="Pattern creation time")

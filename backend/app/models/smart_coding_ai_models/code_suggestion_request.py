"""
CodeSuggestionRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodeSuggestionRequest(BaseModel):
    """Code suggestion request model"""
    file_path: str
    language: Language
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[str]] = None
    classes: Optional[List[str]] = None
    variables: Optional[List[str]] = None
    max_suggestions: Optional[int] = Field(default=5, ge=1, le=20)

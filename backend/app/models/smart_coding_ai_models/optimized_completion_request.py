"""
OptimizedCompletionRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class OptimizedCompletionRequest(BaseModel):
    """Optimized completion request model"""
    file_path: str
    language: str
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[Dict[str, Any]]] = None
    classes: Optional[List[Dict[str, Any]]] = None
    variables: Optional[List[Dict[str, Any]]] = None
    max_completions: Optional[int] = Field(default=10, ge=1, le=50)

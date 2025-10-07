"""
DocumentationRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DocumentationRequest(BaseModel):
    """Documentation request model"""
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

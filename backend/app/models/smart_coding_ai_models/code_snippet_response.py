"""
CodeSnippetResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodeSnippetResponse(BaseModel):
    """Code snippet response model"""
    snippets: List[CodeSnippet]
    total_count: int
    language: Language
    timestamp: datetime

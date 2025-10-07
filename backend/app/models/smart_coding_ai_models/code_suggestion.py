"""
CodeSuggestion Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodeSuggestion(BaseModel):
    """Code suggestion model"""
    suggestion_id: str
    text: str
    suggestion_type: SuggestionType
    language: Language
    confidence: float = Field(ge=0.0, le=1.0)
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    explanation: str
    severity: str = "info"  # info, warning, error
    created_at: datetime

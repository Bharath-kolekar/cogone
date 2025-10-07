"""
CodebaseChatResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodebaseChatResponse(BaseModel):
    """Response from codebase chat"""
    answer: str = Field(..., description="Natural language answer to the query")
    confidence: float = Field(..., description="Confidence score for the answer")
    code_snippets: List[Dict[str, Any]] = Field([], description="Relevant code snippets")
    related_files: List[str] = Field([], description="Files referenced in the answer")
    analysis_type: str = Field(..., description="Type of analysis performed")
    follow_up_questions: List[str] = Field([], description="Suggested follow-up questions")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

"""
CodebaseChatRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodebaseChatRequest(BaseModel):
    """Request for chatting with codebase"""
    query: str = Field(..., description="Natural language question about the codebase")
    project_id: str = Field(..., description="Project identifier")
    context_type: str = Field("general", description="Type of context: general, debug, flow, component")
    include_code_snippets: bool = Field(True, description="Include code snippets in response")
    max_results: int = Field(10, description="Maximum number of results to return")
    focus_files: Optional[List[str]] = Field(None, description="Specific files to focus on")

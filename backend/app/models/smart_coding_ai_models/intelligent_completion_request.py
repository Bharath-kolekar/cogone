"""
IntelligentCompletionRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class IntelligentCompletionRequest(BaseModel):
    """Request for intelligent completion with advanced AI analysis"""
    file_path: str = Field(..., description="Path to the file being edited")
    language: Language = Field(..., description="Programming language")
    content: str = Field(..., description="Current file content")
    cursor_line: int = Field(..., description="Current cursor line")
    cursor_column: int = Field(..., description="Current cursor column")
    selection: Optional[str] = Field(None, description="Selected text")
    imports: Optional[List[str]] = Field(None, description="File imports")
    functions: Optional[List[str]] = Field(None, description="Available functions")
    classes: Optional[List[str]] = Field(None, description="Available classes")
    variables: Optional[List[str]] = Field(None, description="Available variables")
    recent_changes: Optional[List[str]] = Field(None, description="Recent code changes")
    project_context: Optional[Dict[str, Any]] = Field(None, description="Project context")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    completion_history: Optional[List[str]] = Field(None, description="Completion history")
    intelligence_level: str = Field("high", description="Intelligence level: low, medium, high, expert")
    analysis_depth: str = Field("deep", description="Analysis depth: shallow, medium, deep, comprehensive")

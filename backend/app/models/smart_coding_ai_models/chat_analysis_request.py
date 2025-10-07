"""
ChatAnalysisRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ChatAnalysisRequest(BaseModel):
    """Request for specific chat analysis"""
    query: str = Field(..., description="Analysis query")
    project_id: str = Field(..., description="Project identifier")
    analysis_type: str = Field(..., description="Type of analysis: flow, component, debug, search")
    include_context: bool = Field(True, description="Include additional context")
    max_depth: int = Field(5, description="Maximum analysis depth")

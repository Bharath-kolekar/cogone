"""
MemoryAnalysisResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MemoryAnalysisResponse(BaseModel):
    """Response for memory analysis"""
    analysis_id: str = Field(..., description="Analysis identifier")
    project_id: str = Field(..., description="Project identifier")
    memory_snapshot: MemorySnapshot = Field(..., description="Generated memory snapshot")
    analysis_time: float = Field(..., description="Analysis time in seconds")
    files_analyzed: int = Field(..., description="Number of files analyzed")
    patterns_found: int = Field(..., description="Number of patterns found")
    dependencies_found: int = Field(..., description="Number of dependencies found")
    configs_found: int = Field(..., description="Number of configurations found")
    analysis_summary: Dict[str, Any] = Field(..., description="Analysis summary")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")

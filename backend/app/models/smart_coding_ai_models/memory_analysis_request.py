"""
MemoryAnalysisRequest Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MemoryAnalysisRequest(BaseModel):
    """Request for memory analysis"""
    project_path: str = Field(..., description="Project path to analyze")
    analysis_depth: str = Field("deep", description="Analysis depth: shallow, medium, deep, comprehensive")
    include_patterns: bool = Field(True, description="Include pattern analysis")
    include_dependencies: bool = Field(True, description="Include dependency analysis")
    include_configs: bool = Field(True, description="Include configuration analysis")
    update_existing: bool = Field(False, description="Update existing memory if found")

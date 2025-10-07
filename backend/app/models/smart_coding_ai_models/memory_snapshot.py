"""
MemorySnapshot Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MemorySnapshot(BaseModel):
    """Complete memory snapshot of codebase"""
    snapshot_id: str = Field(..., description="Unique snapshot identifier")
    project_id: str = Field(..., description="Project identifier")
    project_structure: ProjectStructure = Field(..., description="Project structure")
    coding_patterns: List[CodingPattern] = Field([], description="All coding patterns")
    dependencies: List[DependencyInfo] = Field([], description="All dependencies")
    configs: List[ConfigInfo] = Field([], description="All configurations")
    session_context: Optional[SessionContext] = Field(None, description="Current session context")
    memory_size: int = Field(..., description="Total memory size in bytes")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update time")
    version: str = Field("1.0", description="Memory schema version")

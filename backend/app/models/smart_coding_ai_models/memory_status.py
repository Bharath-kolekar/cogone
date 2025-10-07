"""
MemoryStatus Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MemoryStatus(BaseModel):
    """Memory system status"""
    system_active: bool = Field(..., description="Whether memory system is active")
    total_projects: int = Field(..., description="Total projects in memory")
    total_patterns: int = Field(..., description="Total patterns stored")
    total_dependencies: int = Field(..., description="Total dependencies tracked")
    total_configs: int = Field(..., description="Total configurations stored")
    memory_usage: float = Field(..., description="Memory usage percentage")
    last_analysis: Optional[datetime] = Field(None, description="Last analysis time")
    cache_hit_rate: float = Field(..., description="Cache hit rate")
    performance_score: float = Field(..., description="Performance score")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")

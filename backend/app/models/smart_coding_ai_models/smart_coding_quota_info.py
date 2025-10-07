"""
SmartCodingQuotaInfo Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SmartCodingQuotaInfo(BaseModel):
    """Quota information for Smart Coding AI operations"""
    user_id: str = Field(..., description="User ID")
    daily_completions: int = Field(0, description="Daily completion quota")
    daily_memory_operations: int = Field(0, description="Daily memory operation quota")
    daily_analysis_operations: int = Field(0, description="Daily analysis operation quota")
    monthly_storage_mb: int = Field(0, description="Monthly storage quota in MB")
    concurrent_sessions: int = Field(1, description="Concurrent session limit")
    usage_stats: Dict[str, int] = Field(default_factory=dict, description="Current usage statistics")
    reset_date: datetime = Field(..., description="When quotas reset")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

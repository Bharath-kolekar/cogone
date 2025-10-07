"""
ConfigInfo Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ConfigInfo(BaseModel):
    """Configuration information"""
    config_id: str = Field(..., description="Unique config identifier")
    config_type: str = Field(..., description="Type of configuration")
    file_path: str = Field(..., description="Configuration file path")
    config_data: Dict[str, Any] = Field(..., description="Configuration data")
    environment: str = Field("default", description="Environment (dev, prod, test)")
    is_active: bool = Field(True, description="Whether configuration is active")
    last_modified: datetime = Field(default_factory=datetime.now, description="Last modification time")

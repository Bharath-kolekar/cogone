"""
FileStructure Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FileStructure(BaseModel):
    """File structure representation"""
    file_path: str = Field(..., description="File path")
    file_type: str = Field(..., description="File type/extension")
    file_size: int = Field(..., description="File size in bytes")
    directory: str = Field(..., description="Directory path")
    relative_path: str = Field(..., description="Relative path from project root")
    is_directory: bool = Field(False, description="Whether this is a directory")
    children: Optional[List['FileStructure']] = Field(None, description="Child files/directories")
    last_modified: datetime = Field(..., description="Last modification time")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")

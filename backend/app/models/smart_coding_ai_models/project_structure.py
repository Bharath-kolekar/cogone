"""
ProjectStructure Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ProjectStructure(BaseModel):
    """Complete project structure"""
    project_id: str = Field(..., description="Unique project identifier")
    project_name: str = Field(..., description="Project name")
    project_root: str = Field(..., description="Project root directory")
    file_tree: FileStructure = Field(..., description="Root file structure")
    total_files: int = Field(..., description="Total number of files")
    total_directories: int = Field(..., description="Total number of directories")
    languages_used: List[str] = Field(..., description="Programming languages used")
    frameworks: List[str] = Field(..., description="Frameworks detected")
    dependencies: List[str] = Field(..., description="Dependencies detected")
    config_files: List[str] = Field(..., description="Configuration files")
    last_analyzed: datetime = Field(default_factory=datetime.now, description="Last analysis time")

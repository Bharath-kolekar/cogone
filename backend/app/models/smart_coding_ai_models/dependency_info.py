"""
DependencyInfo Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DependencyInfo(BaseModel):
    """Dependency information"""
    dependency_id: str = Field(..., description="Unique dependency identifier")
    name: str = Field(..., description="Dependency name")
    version: str = Field(..., description="Dependency version")
    type: str = Field(..., description="Dependency type (package, library, framework)")
    source: str = Field(..., description="Where dependency is defined")
    usage_count: int = Field(0, description="How many times dependency is used")
    files_using: List[str] = Field([], description="Files that use this dependency")
    import_statements: List[str] = Field([], description="Import statements")
    is_dev_dependency: bool = Field(False, description="Whether it's a dev dependency")
    last_used: datetime = Field(default_factory=datetime.now, description="Last usage time")

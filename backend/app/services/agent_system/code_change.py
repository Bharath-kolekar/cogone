"""
CodeChange Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodeChange:
    """Represents a code change to be made"""
    change_id: str
    change_type: ChangeType
    file_path: str
    description: str
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    line_number: Optional[int] = None
    dependencies: List[str] = None
    tests: List[str] = None
    comments: List[str] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.dependencies is None:
            self.dependencies = []
        if self.tests is None:
            self.tests = []
        if self.comments is None:
            self.comments = []

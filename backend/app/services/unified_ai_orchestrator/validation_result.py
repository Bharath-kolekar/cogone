"""
ValidationResult Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ValidationResult:
    """Validation result structure"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    score: float = 0.0
    details: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.suggestions is None:
            self.suggestions = []
        if self.details is None:
            self.details = {}

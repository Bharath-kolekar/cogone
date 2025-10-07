"""
CommentGenerator Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CommentGenerator:
    """Generates helpful comments for code changes"""
    
    def __init__(self):
        self.comment_templates = {
            "function": "# Function: {name}\n# Description: {description}\n# Parameters: {params}\n# Returns: {returns}",
            "class": "# Class: {name}\n# Description: {description}\n# Methods: {methods}",
            "import": "# Import: {name}\n# Purpose: {purpose}",
            "dependency": "# Dependency: {name}\n# Purpose: {purpose}\n# Version: {version}"
        }
    
    async def generate_comments(self, changes: List[CodeChange]) -> List[str]:
        """Generate helpful comments for changes"""
        comments = []
        
        for change in changes:
            if change.change_type == ChangeType.ADD_FUNCTION:
                comment = self._generate_function_comment(change)
                comments.append(comment)
            elif change.change_type == ChangeType.ADD_CLASS:
                comment = self._generate_class_comment(change)
                comments.append(comment)
            elif change.change_type == ChangeType.ADD_IMPORT:
                comment = self._generate_import_comment(change)
                comments.append(comment)
            elif change.change_type == ChangeType.ADD_DEPENDENCY:
                comment = self._generate_dependency_comment(change)
                comments.append(comment)
        
        return comments
    
    def _generate_function_comment(self, change: CodeChange) -> str:
        """Generate comment for a function"""
        return f"""
# ============================================================================
# Function: {change.description}
# Added by Agent Mode - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ============================================================================
"""
    
    def _generate_class_comment(self, change: CodeChange) -> str:
        """Generate comment for a class"""
        return f"""
# ============================================================================
# Class: {change.description}
# Added by Agent Mode - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ============================================================================
"""
    
    def _generate_import_comment(self, change: CodeChange) -> str:
        """Generate comment for an import"""
        return f"# Import added by Agent Mode for: {change.description}"
    
    def _generate_dependency_comment(self, change: CodeChange) -> str:
        """Generate comment for a dependency"""
        return f"# Dependency added by Agent Mode for: {change.description}"

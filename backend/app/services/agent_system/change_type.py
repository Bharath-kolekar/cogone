"""
ChangeType Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ChangeType(str, Enum):
    """Types of changes the agent can make"""
    CREATE_FILE = "create_file"
    MODIFY_FILE = "modify_file"
    DELETE_FILE = "delete_file"
    ADD_DEPENDENCY = "add_dependency"
    REMOVE_DEPENDENCY = "remove_dependency"
    CREATE_DIRECTORY = "create_directory"
    ADD_IMPORT = "add_import"
    REMOVE_IMPORT = "remove_import"
    ADD_FUNCTION = "add_function"
    MODIFY_FUNCTION = "modify_function"
    ADD_CLASS = "add_class"
    MODIFY_CLASS = "modify_class"

"""
MermaidDiagram Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class MermaidDiagram:
    """Mermaid diagram definition"""
    diagram_id: str
    diagram_type: DiagramType
    title: str
    content: str
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

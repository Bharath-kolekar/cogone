"""
ArchitectureAnalysis Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ArchitectureAnalysis:
    """Architecture analysis result"""
    analysis_id: str
    architecture_id: str
    analysis_type: str
    findings: List[str]
    recommendations: List[str]
    quality_score: float
    complexity_score: float
    maintainability_score: float
    scalability_score: float
    security_score: float
    performance_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

"""
ChatAnalysisResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ChatAnalysisResponse(BaseModel):
    """Response from chat analysis"""
    analysis_result: Dict[str, Any] = Field(..., description="Analysis result")
    confidence: float = Field(..., description="Confidence score")
    related_components: List[ComponentRelationship] = Field([], description="Related components")
    code_flows: List[CodeFlowAnalysis] = Field([], description="Related code flows")
    suggestions: List[str] = Field([], description="Suggestions based on analysis")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")

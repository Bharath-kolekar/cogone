"""
CodeFlowAnalysis Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodeFlowAnalysis(BaseModel):
    """Code flow analysis result"""
    flow_id: str = Field(..., description="Unique flow analysis identifier")
    flow_name: str = Field(..., description="Name of the flow being analyzed")
    flow_type: str = Field(..., description="Type of flow: data, authentication, business_logic")
    entry_points: List[str] = Field(..., description="Entry points to the flow")
    exit_points: List[str] = Field(..., description="Exit points from the flow")
    intermediate_steps: List[Dict[str, Any]] = Field(..., description="Intermediate steps in the flow")
    dependencies: List[str] = Field([], description="Dependencies involved in the flow")
    files_involved: List[str] = Field(..., description="Files involved in the flow")
    complexity_score: float = Field(..., description="Complexity score of the flow")

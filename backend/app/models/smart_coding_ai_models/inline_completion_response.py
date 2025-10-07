"""
InlineCompletionResponse Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class InlineCompletionResponse(BaseModel):
    """Response for in-line code completion"""
    completion_id: str = Field(..., description="Unique completion ID")
    text: str = Field(..., description="Completion text")
    completion_type: str = Field(..., description="Type of completion")
    language: str = Field(..., description="Programming language")
    confidence: float = Field(..., description="Confidence score (0-1)")
    accuracy_score: float = Field(..., description="Accuracy score (0-1)")
    context_relevance: float = Field(..., description="Context relevance score (0-1)")
    semantic_similarity: float = Field(..., description="Semantic similarity score (0-1)")
    pattern_match_score: float = Field(..., description="Pattern match score (0-1)")
    ml_prediction_score: float = Field(..., description="ML prediction score (0-1)")
    ensemble_score: float = Field(..., description="Ensemble score (0-1)")
    start_line: int = Field(..., description="Start line position")
    end_line: int = Field(..., description="End line position")
    start_column: int = Field(..., description="Start column position")
    end_column: int = Field(..., description="End column position")
    description: str = Field(..., description="Completion description")
    documentation: Optional[str] = Field(None, description="Completion documentation")
    parameters: Optional[List[Dict[str, Any]]] = Field(None, description="Function parameters")
    return_type: Optional[str] = Field(None, description="Return type")
    optimization_strategies: Optional[List[OptimizationStrategy]] = Field(None, description="Optimization strategies used")
    is_streaming: bool = Field(False, description="Whether completion is streaming")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")

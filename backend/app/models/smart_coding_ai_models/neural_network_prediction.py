"""
NeuralNetworkPrediction Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class NeuralNetworkPrediction(BaseModel):
    """Neural network prediction model"""
    network_type: str
    prediction_confidence: float
    accuracy_score: float
    model_accuracy: float
    timestamp: datetime

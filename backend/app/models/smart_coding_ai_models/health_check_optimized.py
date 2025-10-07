"""
HealthCheckOptimized Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class HealthCheckOptimized(BaseModel):
    """Optimized health check model"""
    status: str
    service: str
    optimization_active: bool
    accuracy_level: AccuracyLevel
    current_accuracy: float
    completions_working: bool
    optimization_strategies: int
    models_loaded: int
    timestamp: datetime

"""
BenchmarkResults Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class BenchmarkResults(BaseModel):
    """Benchmark results model"""
    accuracy_benchmarks: Dict[str, float]
    performance_benchmarks: Dict[str, float]
    optimization_benchmarks: Dict[str, Dict[str, float]]
    timestamp: datetime

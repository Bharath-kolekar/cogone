"""
Enums for AI Orchestration Layer
Preserves orchestration modes and configurations
"""

from enum import Enum


class OrchestrationMode(str, Enum):
    """Orchestration execution modes"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    ADAPTIVE = "adaptive"


class ValidationLevel(str, Enum):
    """Validation thoroughness levels"""
    BASIC = "basic"  # Quick validation
    STANDARD = "standard"  # Standard 11 validators
    MAXIMUM = "maximum"  # Maximum accuracy validators
    SIX_SIGMA = "six_sigma"  # 99.99966% accuracy


class OrchestrationPriority(str, Enum):
    """Priority levels for orchestration tasks"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class EngineType(str, Enum):
    """Autonomous engine types"""
    LEARNING = "learning"
    OPTIMIZATION = "optimization"
    HEALING = "healing"
    MONITORING = "monitoring"
    DECISION = "decision"
    STRATEGY = "strategy"
    ADAPTATION = "adaptation"
    CREATIVE = "creative"
    INNOVATION = "innovation"

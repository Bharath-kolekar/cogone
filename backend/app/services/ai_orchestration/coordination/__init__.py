"""
Coordination package for AI Orchestration Layer
CRITICAL: Exports components used by other orchestrators
"""

from .task_decomposer import IntelligentTaskDecomposer
from .multi_agent_coordinator import MultiAgentCoordinator

__all__ = [
    'IntelligentTaskDecomposer',  # Used by meta_ai, unified_ai
    'MultiAgentCoordinator'       # Used by meta_ai, unified_ai
]

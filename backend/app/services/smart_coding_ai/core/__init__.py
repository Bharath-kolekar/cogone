"""
Core components for Smart Coding AI Service
Preserves all core business logic and algorithms
"""

from .completion_generator import CompletionGenerator
from .confidence_scorer import ConfidenceScorer
from .performance_optimizer import PerformanceOptimizer

__all__ = [
    'CompletionGenerator',
    'ConfidenceScorer',
    'PerformanceOptimizer'
]

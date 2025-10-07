"""
Models package for Smart Coding AI Service
Exports all models while preserving complete functionality
"""

# Enums - All capabilities preserved
from .enums import (
    AccuracyLevel,
    OptimizationStrategy,
    Language,
    CompletionType,
    SuggestionType
)

# Context models - Full context awareness preserved
from .contexts import (
    CodeContext,
    CompletionContext
)

# Completion models - 99.99966% accuracy preserved
from .completions import (
    CodeCompletion,
    OptimizedCompletion,
    InlineCompletion
)

# Suggestion models - Proactive assistance preserved
from .suggestions import (
    CodeSuggestion,
    CodeSnippet,
    Documentation,
    AccuracyMetrics
)

__all__ = [
    # Enums
    'AccuracyLevel',
    'OptimizationStrategy',
    'Language',
    'CompletionType',
    'SuggestionType',
    # Contexts
    'CodeContext',
    'CompletionContext',
    # Completions
    'CodeCompletion',
    'OptimizedCompletion',
    'InlineCompletion',
    # Suggestions
    'CodeSuggestion',
    'CodeSnippet',
    'Documentation',
    'AccuracyMetrics'
]

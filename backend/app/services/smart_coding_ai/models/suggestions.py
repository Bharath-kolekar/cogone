"""
Suggestion and documentation models for Smart Coding AI Service
Preserves proactive assistance and documentation capabilities
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from .enums import SuggestionType, Language


@dataclass
class CodeSuggestion:
    """
    Code suggestion model
    Preserves proactive error correction and best practices
    """
    suggestion_id: str
    text: str
    suggestion_type: SuggestionType
    language: Language
    confidence: float
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    explanation: str
    severity: str = "info"  # info, warning, error
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CodeSnippet:
    """
    Code snippet model
    Preserves reusable code patterns and templates
    """
    snippet_id: str
    title: str
    description: str
    code: str
    language: Language
    tags: List[str]
    usage_count: int = 0
    rating: float = 0.0
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class Documentation:
    """
    Documentation model
    Preserves comprehensive documentation generation
    """
    doc_id: str
    title: str
    content: str
    language: Language
    code_examples: List[str]
    related_functions: List[str]
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class AccuracyMetrics:
    """
    Accuracy metrics model
    Preserves Six Sigma quality tracking (99.99966% accuracy)
    """
    total_completions: int
    correct_completions: int
    accuracy_percentage: float  # Tracks 99.99966% target
    confidence_threshold: float
    optimization_level: str  # References AccuracyLevel enum
    strategies_used: List[str]  # References OptimizationStrategy enum
    timestamp: datetime
    six_sigma_achieved: bool = False  # Tracks Six Sigma achievement
    seven_sigma_target: bool = False  # Future enhancement to 99.99999%

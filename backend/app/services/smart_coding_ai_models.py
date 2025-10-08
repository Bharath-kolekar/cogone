"""
Smart Coding AI Data Models
Extracted from smart_coding_ai_optimized.py for better organization
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from .smart_coding_ai_enums import (
    Language,
    CompletionType,
    SuggestionType,
    AccuracyLevel,
    OptimizationStrategy
)


@dataclass
class CodeContext:
    """Code context for analysis"""
    file_path: str
    language: Language
    content: str
    cursor_position: Tuple[int, int]
    selection: Optional[str] = None
    imports: List[str] = None
    functions: List[str] = None
    classes: List[str] = None
    variables: List[str] = None
    recent_changes: List[str] = None
    project_context: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.imports is None:
            self.imports = []
        if self.functions is None:
            self.functions = []
        if self.classes is None:
            self.classes = []
        if self.variables is None:
            self.variables = []
        if self.recent_changes is None:
            self.recent_changes = []


@dataclass
class CodeCompletion:
    """Code completion model"""
    completion_id: str
    text: str
    completion_type: CompletionType
    language: Language
    confidence: float
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    documentation: Optional[str] = None
    parameters: Optional[List[Dict[str, Any]]] = None
    return_type: Optional[str] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CodeSuggestion:
    """Code suggestion model"""
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
    """Code snippet model"""
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
    """Documentation model"""
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
    """Accuracy metrics model"""
    total_completions: int
    correct_completions: int
    accuracy_percentage: float
    confidence_threshold: float
    optimization_level: AccuracyLevel
    strategies_used: List[OptimizationStrategy]
    timestamp: datetime


@dataclass
class OptimizedCompletion:
    """Optimized completion model"""
    completion_id: str
    text: str
    completion_type: str
    language: str
    confidence: float
    accuracy_score: float
    context_relevance: float
    semantic_similarity: float
    pattern_match_score: float
    ml_prediction_score: float
    ensemble_score: float
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    documentation: Optional[str] = None
    parameters: Optional[List[Dict]] = None
    return_type: Optional[str] = None
    optimization_strategies: Optional[List[OptimizationStrategy]] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class InlineCompletion:
    """In-line code completion for real-time suggestions"""
    completion_id: str
    text: str
    completion_type: str
    language: str
    confidence: float
    accuracy_score: float
    context_relevance: float
    semantic_similarity: float
    pattern_match_score: float
    ml_prediction_score: float
    ensemble_score: float
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    documentation: Optional[str] = None
    parameters: Optional[List[Dict]] = None
    return_type: Optional[str] = None
    optimization_strategies: Optional[List[OptimizationStrategy]] = None
    is_streaming: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class CompletionContext:
    """Enhanced context for in-line completions"""
    file_path: str
    language: Language
    content: str
    cursor_position: Tuple[int, int]
    selection: Optional[str] = None
    imports: List[str] = None
    functions: List[str] = None
    classes: List[str] = None
    variables: List[str] = None
    recent_changes: List[str] = None
    project_context: Dict[str, Any] = None
    user_preferences: Dict[str, Any] = None
    completion_history: List[str] = None
    typing_speed: float = 0.0
    pause_duration: float = 0.0


__all__ = [
    'CodeContext',
    'CodeCompletion',
    'CodeSuggestion',
    'CodeSnippet',
    'Documentation',
    'AccuracyMetrics',
    'OptimizedCompletion',
    'InlineCompletion',
    'CompletionContext'
]


"""
Smart Coding AI Enums
Extracted from smart_coding_ai_optimized.py for better organization
"""

from enum import Enum


class AccuracyLevel(str, Enum):
    """Accuracy levels"""
    BASIC = "basic"  # 90-95%
    ADVANCED = "advanced"  # 95-98%
    EXPERT = "expert"  # 98-99%
    PERFECT = "perfect"  # 100%


class OptimizationStrategy(str, Enum):
    """Optimization strategies"""
    PATTERN_MATCHING = "pattern_matching"
    MACHINE_LEARNING = "machine_learning"
    CONTEXT_ANALYSIS = "context_analysis"
    SEMANTIC_UNDERSTANDING = "semantic_understanding"
    NEURAL_NETWORKS = "neural_networks"
    ENSEMBLE_METHODS = "ensemble_methods"


class Language(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    CPP = "cpp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    HTML = "html"
    CSS = "css"
    SQL = "sql"
    YAML = "yaml"
    JSON = "json"
    MARKDOWN = "markdown"


class CompletionType(str, Enum):
    """Code completion types"""
    FUNCTION = "function"
    VARIABLE = "variable"
    CLASS = "class"
    IMPORT = "import"
    PARAMETER = "parameter"
    METHOD = "method"
    PROPERTY = "property"
    TYPE = "type"
    KEYWORD = "keyword"
    SNIPPET = "snippet"


class SuggestionType(str, Enum):
    """Suggestion types"""
    COMPLETION = "completion"
    HINT = "hint"
    REFACTOR = "refactor"
    OPTIMIZATION = "optimization"
    BUG_FIX = "bug_fix"
    BEST_PRACTICE = "best_practice"


__all__ = [
    'AccuracyLevel',
    'OptimizationStrategy',
    'Language',
    'CompletionType',
    'SuggestionType'
]


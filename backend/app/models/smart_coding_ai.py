"""
Smart Coding AI Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum


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
    ERROR_FIX = "error_fix"
    REFACTOR = "refactor"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"


class CodeCompletion(BaseModel):
    """Code completion model"""
    completion_id: str
    text: str
    completion_type: CompletionType
    language: Language
    confidence: float = Field(ge=0.0, le=1.0)
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    documentation: Optional[str] = None
    parameters: Optional[List[Dict[str, Any]]] = None
    return_type: Optional[str] = None
    created_at: datetime


class CodeSuggestion(BaseModel):
    """Code suggestion model"""
    suggestion_id: str
    suggestion_type: SuggestionType
    text: str
    language: Language
    confidence: float = Field(ge=0.0, le=1.0)
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    priority: int = Field(ge=1, le=10)
    auto_apply: bool = False
    created_at: datetime


class CodeContext(BaseModel):
    """Code context model"""
    file_path: str
    language: Language
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[Dict[str, Any]]] = None
    classes: Optional[List[Dict[str, Any]]] = None
    variables: Optional[List[Dict[str, Any]]] = None


class CodeCompletionRequest(BaseModel):
    """Code completion request model"""
    file_path: str
    language: Language
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[Dict[str, Any]]] = None
    classes: Optional[List[Dict[str, Any]]] = None
    variables: Optional[List[Dict[str, Any]]] = None
    max_completions: Optional[int] = Field(default=10, ge=1, le=50)


class CodeCompletionResponse(BaseModel):
    """Code completion response model"""
    completions: List[CodeCompletion]
    total_count: int
    language: Language
    timestamp: datetime


class CodeSuggestionRequest(BaseModel):
    """Code suggestion request model"""
    file_path: str
    language: Language
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[Dict[str, Any]]] = None
    classes: Optional[List[Dict[str, Any]]] = None
    variables: Optional[List[Dict[str, Any]]] = None
    max_suggestions: Optional[int] = Field(default=5, ge=1, le=20)


class CodeSuggestionResponse(BaseModel):
    """Code suggestion response model"""
    suggestions: List[CodeSuggestion]
    total_count: int
    language: Language
    timestamp: datetime


class CodeSnippetRequest(BaseModel):
    """Code snippet request model"""
    description: str
    language: Language
    context: Optional[CodeContext] = None


class CodeSnippetResponse(BaseModel):
    """Code snippet response model"""
    snippet: str
    language: Language
    description: str
    timestamp: datetime


class DocumentationRequest(BaseModel):
    """Documentation request model"""
    symbol: str
    language: Language


class DocumentationResponse(BaseModel):
    """Documentation response model"""
    symbol: str
    language: Language
    documentation: Optional[str]
    timestamp: datetime


class SmartCodingAIStatus(BaseModel):
    """Smart Coding AI status model"""
    service_active: bool
    models_loaded: bool
    supported_languages: int
    completion_cache_size: int
    suggestion_cache_size: int
    last_updated: datetime


class LanguageInfo(BaseModel):
    """Language information model"""
    name: str
    value: str
    extensions: List[str]
    description: Optional[str] = None


class CompletionTypeInfo(BaseModel):
    """Completion type information model"""
    name: str
    value: str
    description: str


class SuggestionTypeInfo(BaseModel):
    """Suggestion type information model"""
    name: str
    value: str
    description: str


class SmartCodingAIStats(BaseModel):
    """Smart Coding AI statistics model"""
    completion_cache_size: int
    suggestion_cache_size: int
    supported_languages: int
    completion_types: int
    suggestion_types: int
    service_uptime: str
    timestamp: datetime


class CodeAnalysisRequest(BaseModel):
    """Code analysis request model"""
    file_path: str
    language: Language
    content: str
    analysis_type: str = Field(default="comprehensive")


class CodeAnalysisResponse(BaseModel):
    """Code analysis response model"""
    file_path: str
    language: Language
    analysis_results: Dict[str, Any]
    suggestions: List[CodeSuggestion]
    completions: List[CodeCompletion]
    timestamp: datetime


class CodeRefactorRequest(BaseModel):
    """Code refactor request model"""
    file_path: str
    language: Language
    content: str
    refactor_type: str
    target_lines: Optional[List[int]] = None


class CodeRefactorResponse(BaseModel):
    """Code refactor response model"""
    original_content: str
    refactored_content: str
    changes: List[Dict[str, Any]]
    refactor_type: str
    timestamp: datetime


class CodeOptimizationRequest(BaseModel):
    """Code optimization request model"""
    file_path: str
    language: Language
    content: str
    optimization_type: str = Field(default="performance")


class CodeOptimizationResponse(BaseModel):
    """Code optimization response model"""
    original_content: str
    optimized_content: str
    optimizations: List[Dict[str, Any]]
    performance_improvement: Optional[float] = None
    optimization_type: str
    timestamp: datetime


class CodeDocumentationRequest(BaseModel):
    """Code documentation request model"""
    file_path: str
    language: Language
    content: str
    documentation_style: str = Field(default="standard")


class CodeDocumentationResponse(BaseModel):
    """Code documentation response model"""
    original_content: str
    documented_content: str
    documentation_added: List[Dict[str, Any]]
    documentation_style: str
    timestamp: datetime


class CodeErrorFixRequest(BaseModel):
    """Code error fix request model"""
    file_path: str
    language: Language
    content: str
    error_message: str
    error_line: Optional[int] = None


class CodeErrorFixResponse(BaseModel):
    """Code error fix response model"""
    original_content: str
    fixed_content: str
    fixes_applied: List[Dict[str, Any]]
    error_message: str
    timestamp: datetime


class CodeMetrics(BaseModel):
    """Code metrics model"""
    lines_of_code: int
    functions_count: int
    classes_count: int
    complexity_score: float
    maintainability_index: float
    technical_debt: float
    code_quality_score: float
    timestamp: datetime


class CodeQualityRequest(BaseModel):
    """Code quality request model"""
    file_path: str
    language: Language
    content: str
    quality_checks: Optional[List[str]] = None


class CodeQualityResponse(BaseModel):
    """Code quality response model"""
    file_path: str
    language: Language
    quality_score: float
    metrics: CodeMetrics
    issues: List[Dict[str, Any]]
    recommendations: List[str]
    timestamp: datetime

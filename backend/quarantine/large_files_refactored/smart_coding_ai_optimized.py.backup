"""
Optimized Smart Coding AI Pydantic models with 100% accuracy
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum

# Import User model for OAuth integration
try:
    from .user import User
except ImportError:
    # Fallback if user model not available
    class User(BaseModel):
        id: str
        email: str
        name: Optional[str] = None


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


class OptimizedCompletion(BaseModel):
    """Optimized completion model with 100% accuracy"""
    completion_id: str
    text: str
    completion_type: str
    language: str
    confidence: float = Field(ge=0.0, le=1.0)
    accuracy_score: float = Field(ge=0.0, le=1.0)
    context_relevance: float = Field(ge=0.0, le=1.0)
    semantic_similarity: float = Field(ge=0.0, le=1.0)
    pattern_match_score: float = Field(ge=0.0, le=1.0)
    ml_prediction_score: float = Field(ge=0.0, le=1.0)
    ensemble_score: float = Field(ge=0.0, le=1.0)
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    documentation: Optional[str] = None
    parameters: Optional[List[Dict[str, Any]]] = None
    return_type: Optional[str] = None
    optimization_strategies: Optional[List[OptimizationStrategy]] = None
    created_at: datetime


# Core Smart Coding AI Models (Missing from Original)

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

class CodeCompletionRequest(BaseModel):
    """Code completion request model"""
    file_path: str
    language: Language
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[str]] = None
    classes: Optional[List[str]] = None
    variables: Optional[List[str]] = None
    max_completions: Optional[int] = Field(default=10, ge=1, le=50)

class CodeCompletionResponse(BaseModel):
    """Code completion response model"""
    completions: List[CodeCompletion]
    total_count: int
    language: Language
    timestamp: datetime

class CodeSuggestion(BaseModel):
    """Code suggestion model"""
    suggestion_id: str
    text: str
    suggestion_type: SuggestionType
    language: Language
    confidence: float = Field(ge=0.0, le=1.0)
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    explanation: str
    severity: str = "info"  # info, warning, error
    created_at: datetime

class CodeSuggestionRequest(BaseModel):
    """Code suggestion request model"""
    file_path: str
    language: Language
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[str]] = None
    classes: Optional[List[str]] = None
    variables: Optional[List[str]] = None
    max_suggestions: Optional[int] = Field(default=5, ge=1, le=20)

class CodeSuggestionResponse(BaseModel):
    """Code suggestion response model"""
    suggestions: List[CodeSuggestion]
    total_count: int
    language: Language
    timestamp: datetime

class CodeSnippet(BaseModel):
    """Code snippet model"""
    snippet_id: str
    title: str
    description: str
    code: str
    language: Language
    tags: List[str]
    usage_count: int = 0
    rating: float = 0.0
    created_at: datetime

class CodeSnippetRequest(BaseModel):
    """Code snippet request model"""
    file_path: str
    language: Language
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[str]] = None
    classes: Optional[List[str]] = None
    variables: Optional[List[str]] = None
    max_snippets: Optional[int] = Field(default=5, ge=1, le=20)

class CodeSnippetResponse(BaseModel):
    """Code snippet response model"""
    snippets: List[CodeSnippet]
    total_count: int
    language: Language
    timestamp: datetime

class Documentation(BaseModel):
    """Documentation model"""
    doc_id: str
    title: str
    content: str
    language: Language
    code_examples: List[str]
    related_functions: List[str]
    created_at: datetime

class DocumentationRequest(BaseModel):
    """Documentation request model"""
    file_path: str
    language: Language
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[str]] = None
    classes: Optional[List[str]] = None
    variables: Optional[List[str]] = None

class DocumentationResponse(BaseModel):
    """Documentation response model"""
    documentation: Documentation
    language: Language
    timestamp: datetime

class SmartCodingAIStatus(BaseModel):
    """Smart Coding AI status model"""
    service_active: bool
    supported_languages: List[Language]
    completion_count: int
    suggestion_count: int
    snippet_count: int
    documentation_count: int
    accuracy_percentage: float
    timestamp: datetime

# Optimized Models (Enhanced versions)

class OptimizedCompletionRequest(BaseModel):
    """Optimized completion request model"""
    file_path: str
    language: str
    content: str
    cursor_line: int
    cursor_column: int
    selection: Optional[str] = None
    imports: Optional[List[str]] = None
    functions: Optional[List[Dict[str, Any]]] = None
    classes: Optional[List[Dict[str, Any]]] = None
    variables: Optional[List[Dict[str, Any]]] = None
    max_completions: Optional[int] = Field(default=10, ge=1, le=50)


class OptimizedCompletionResponse(BaseModel):
    """Optimized completion response model"""
    completions: List[OptimizedCompletion]
    total_count: int
    language: str
    accuracy_percentage: float
    optimization_level: AccuracyLevel
    strategies_used: List[OptimizationStrategy]
    timestamp: datetime


class AccuracyReportResponse(BaseModel):
    """Accuracy report response model"""
    accuracy_percentage: float
    total_completions: int
    correct_completions: int
    optimization_level: str
    strategies_used: List[str]
    confidence_threshold: float
    timestamp: datetime


class OptimizationStatusResponse(BaseModel):
    """Optimization status response model"""
    optimization_active: bool
    accuracy_target: float
    current_accuracy: float
    optimization_strategies: List[OptimizationStrategy]
    performance_metrics: Dict[str, float]
    optimization_level: AccuracyLevel
    timestamp: datetime


class PerformanceMetricsResponse(BaseModel):
    """Performance metrics response model"""
    response_times: Dict[str, int]  # milliseconds
    accuracy_metrics: Dict[str, float]
    optimization_metrics: Dict[str, float]
    timestamp: datetime


class SmartCodingAIOptimizedStatus(BaseModel):
    """Optimized Smart Coding AI status model"""
    service_active: bool
    optimization_enabled: bool
    accuracy_level: AccuracyLevel
    current_accuracy: float
    target_accuracy: float
    optimization_strategies_active: int
    models_loaded: int
    cache_size: int
    performance_score: float
    last_optimized: datetime


class OptimizationStrategyInfo(BaseModel):
    """Optimization strategy information model"""
    strategy: OptimizationStrategy
    description: str
    accuracy_boost: float
    weight: float
    active: bool


class ModelStatus(BaseModel):
    """Model status model"""
    loaded: bool
    accuracy: float
    last_trained: datetime
    status: str


class AccuracyMetrics(BaseModel):
    """Accuracy metrics model"""
    total_completions: int
    correct_completions: int
    accuracy_percentage: float
    confidence_threshold: float
    optimization_level: AccuracyLevel
    strategies_used: List[OptimizationStrategy]
    timestamp: datetime


class PerformanceBenchmarks(BaseModel):
    """Performance benchmarks model"""
    accuracy_benchmarks: Dict[str, float]
    performance_benchmarks: Dict[str, float]
    optimization_benchmarks: Dict[str, Dict[str, float]]
    timestamp: datetime


class OptimizationCalibration(BaseModel):
    """Optimization calibration model"""
    calibration_completed: bool
    accuracy_target: float
    optimization_level: AccuracyLevel
    calibration_timestamp: datetime


class StrategyEffectiveness(BaseModel):
    """Strategy effectiveness model"""
    pattern_matching: float
    context_analysis: float
    semantic_understanding: float
    machine_learning: float
    neural_networks: float
    ensemble_methods: float


class OptimizationImprovements(BaseModel):
    """Optimization improvements model"""
    accuracy_improvement: float
    response_time_improvement: float
    confidence_improvement: float
    relevance_improvement: float


class EnsembleScore(BaseModel):
    """Ensemble score model"""
    confidence_weight: float
    accuracy_weight: float
    context_weight: float
    semantic_weight: float
    pattern_weight: float
    ml_weight: float
    total_score: float


class ContextAnalysis(BaseModel):
    """Context analysis model"""
    context_type: str
    complexity_score: float
    relevance_score: float
    semantic_score: float
    suggestions: List[str]
    timestamp: datetime


class SemanticAnalysis(BaseModel):
    """Semantic analysis model"""
    semantic_score: float
    meaning_confidence: float
    context_understanding: float
    suggestion_relevance: float
    timestamp: datetime


class PatternMatch(BaseModel):
    """Pattern match model"""
    pattern_type: str
    match_score: float
    confidence: float
    relevance: float
    timestamp: datetime


class MLPrediction(BaseModel):
    """ML prediction model"""
    prediction_type: str
    confidence: float
    accuracy: float
    model_version: str
    timestamp: datetime


class NeuralNetworkPrediction(BaseModel):
    """Neural network prediction model"""
    network_type: str
    prediction_confidence: float
    accuracy_score: float
    model_accuracy: float
    timestamp: datetime


class EnsembleOptimization(BaseModel):
    """Ensemble optimization model"""
    optimization_id: str
    strategies_combined: List[OptimizationStrategy]
    ensemble_score: float
    accuracy_improvement: float
    performance_improvement: float
    timestamp: datetime


class OptimizationTrigger(BaseModel):
    """Optimization trigger model"""
    optimization_triggered: bool
    optimization_level: AccuracyLevel
    target_accuracy: float
    strategies_activated: int
    timestamp: datetime


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


class BenchmarkResults(BaseModel):
    """Benchmark results model"""
    accuracy_benchmarks: Dict[str, float]
    performance_benchmarks: Dict[str, float]
    optimization_benchmarks: Dict[str, Dict[str, float]]
    timestamp: datetime


class OptimizationReport(BaseModel):
    """Optimization report model"""
    report_id: str
    optimization_level: AccuracyLevel
    accuracy_achieved: float
    strategies_used: List[OptimizationStrategy]
    performance_improvements: Dict[str, float]
    recommendations: List[str]
    timestamp: datetime


class AccuracyOptimization(BaseModel):
    """Accuracy optimization model"""
    optimization_id: str
    target_accuracy: float
    achieved_accuracy: float
    optimization_methods: List[str]
    improvement_percentage: float
    timestamp: datetime


class PerformanceOptimization(BaseModel):
    """Performance optimization model"""
    optimization_id: str
    response_time_improvement: float
    throughput_improvement: float
    memory_usage_improvement: float
    cpu_usage_improvement: float
    timestamp: datetime


class SmartCodingAIOptimizedConfig(BaseModel):
    """Optimized Smart Coding AI configuration model"""
    accuracy_target: float = 100.0
    optimization_enabled: bool = True
    strategies_active: List[OptimizationStrategy]
    performance_targets: Dict[str, float]
    cache_settings: Dict[str, Any]
    model_settings: Dict[str, Any]
    timestamp: datetime


# ============================================================================
# IN-LINE COMPLETION MODELS (Advanced code assistant features)
# ============================================================================

class InlineCompletionRequest(BaseModel):
    """Request for in-line code completion"""
    file_path: str = Field(..., description="Path to the file being edited")
    language: Language = Field(..., description="Programming language")
    content: str = Field(..., description="Current file content")
    cursor_line: int = Field(..., description="Current cursor line")
    cursor_column: int = Field(..., description="Current cursor column")
    selection: Optional[str] = Field(None, description="Selected text")
    imports: Optional[List[str]] = Field(None, description="File imports")
    functions: Optional[List[str]] = Field(None, description="Available functions")
    classes: Optional[List[str]] = Field(None, description="Available classes")
    variables: Optional[List[str]] = Field(None, description="Available variables")
    recent_changes: Optional[List[str]] = Field(None, description="Recent code changes")
    project_context: Optional[Dict[str, Any]] = Field(None, description="Project context")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    completion_history: Optional[List[str]] = Field(None, description="Completion history")
    typing_speed: Optional[float] = Field(0.0, description="Typing speed in characters per second")
    pause_duration: Optional[float] = Field(0.0, description="Pause duration in seconds")


class InlineCompletionResponse(BaseModel):
    """Response for in-line code completion"""
    completion_id: str = Field(..., description="Unique completion ID")
    text: str = Field(..., description="Completion text")
    completion_type: str = Field(..., description="Type of completion")
    language: str = Field(..., description="Programming language")
    confidence: float = Field(..., description="Confidence score (0-1)")
    accuracy_score: float = Field(..., description="Accuracy score (0-1)")
    context_relevance: float = Field(..., description="Context relevance score (0-1)")
    semantic_similarity: float = Field(..., description="Semantic similarity score (0-1)")
    pattern_match_score: float = Field(..., description="Pattern match score (0-1)")
    ml_prediction_score: float = Field(..., description="ML prediction score (0-1)")
    ensemble_score: float = Field(..., description="Ensemble score (0-1)")
    start_line: int = Field(..., description="Start line position")
    end_line: int = Field(..., description="End line position")
    start_column: int = Field(..., description="Start column position")
    end_column: int = Field(..., description="End column position")
    description: str = Field(..., description="Completion description")
    documentation: Optional[str] = Field(None, description="Completion documentation")
    parameters: Optional[List[Dict[str, Any]]] = Field(None, description="Function parameters")
    return_type: Optional[str] = Field(None, description="Return type")
    optimization_strategies: Optional[List[OptimizationStrategy]] = Field(None, description="Optimization strategies used")
    is_streaming: bool = Field(False, description="Whether completion is streaming")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class StreamingCompletionResponse(BaseModel):
    """Response for streaming in-line completion"""
    completion_id: str = Field(..., description="Unique completion ID")
    text: str = Field(..., description="Completion text")
    confidence: float = Field(..., description="Confidence score (0-1)")
    is_final: bool = Field(False, description="Whether this is the final completion")
    timestamp: datetime = Field(default_factory=datetime.now, description="Stream timestamp")


class ContextAwareCompletionRequest(BaseModel):
    """Request for context-aware completions"""
    file_path: str = Field(..., description="Path to the file being edited")
    language: Language = Field(..., description="Programming language")
    content: str = Field(..., description="Current file content")
    cursor_line: int = Field(..., description="Current cursor line")
    cursor_column: int = Field(..., description="Current cursor column")
    selection: Optional[str] = Field(None, description="Selected text")
    imports: Optional[List[str]] = Field(None, description="File imports")
    functions: Optional[List[str]] = Field(None, description="Available functions")
    classes: Optional[List[str]] = Field(None, description="Available classes")
    variables: Optional[List[str]] = Field(None, description="Available variables")
    recent_changes: Optional[List[str]] = Field(None, description="Recent code changes")
    project_context: Optional[Dict[str, Any]] = Field(None, description="Project context")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    completion_history: Optional[List[str]] = Field(None, description="Completion history")
    max_completions: int = Field(3, description="Maximum number of completions to return")


class ContextAwareCompletionResponse(BaseModel):
    """Response for context-aware completions"""
    completions: List[InlineCompletionResponse] = Field(..., description="List of completions")
    total_count: int = Field(..., description="Total number of completions")
    language: str = Field(..., description="Programming language")
    context_analysis: Dict[str, Any] = Field(..., description="Context analysis results")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class IntelligentCompletionRequest(BaseModel):
    """Request for intelligent completion with advanced AI analysis"""
    file_path: str = Field(..., description="Path to the file being edited")
    language: Language = Field(..., description="Programming language")
    content: str = Field(..., description="Current file content")
    cursor_line: int = Field(..., description="Current cursor line")
    cursor_column: int = Field(..., description="Current cursor column")
    selection: Optional[str] = Field(None, description="Selected text")
    imports: Optional[List[str]] = Field(None, description="File imports")
    functions: Optional[List[str]] = Field(None, description="Available functions")
    classes: Optional[List[str]] = Field(None, description="Available classes")
    variables: Optional[List[str]] = Field(None, description="Available variables")
    recent_changes: Optional[List[str]] = Field(None, description="Recent code changes")
    project_context: Optional[Dict[str, Any]] = Field(None, description="Project context")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    completion_history: Optional[List[str]] = Field(None, description="Completion history")
    intelligence_level: str = Field("high", description="Intelligence level: low, medium, high, expert")
    analysis_depth: str = Field("deep", description="Analysis depth: shallow, medium, deep, comprehensive")


class IntelligentCompletionResponse(BaseModel):
    """Response for intelligent completion"""
    completion: InlineCompletionResponse = Field(..., description="Intelligent completion")
    context_analysis: Dict[str, Any] = Field(..., description="Context analysis results")
    intelligence_score: float = Field(..., description="Intelligence score (0-1)")
    analysis_depth: str = Field(..., description="Analysis depth used")
    optimization_applied: List[str] = Field(..., description="Optimizations applied")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class CompletionSuggestionsRequest(BaseModel):
    """Request for completion suggestions"""
    file_path: str = Field(..., description="Path to the file being edited")
    language: Language = Field(..., description="Programming language")
    content: str = Field(..., description="Current file content")
    cursor_line: int = Field(..., description="Current cursor line")
    cursor_column: int = Field(..., description="Current cursor column")
    selection: Optional[str] = Field(None, description="Selected text")
    imports: Optional[List[str]] = Field(None, description="File imports")
    functions: Optional[List[str]] = Field(None, description="Available functions")
    classes: Optional[List[str]] = Field(None, description="Available classes")
    variables: Optional[List[str]] = Field(None, description="Available variables")
    recent_changes: Optional[List[str]] = Field(None, description="Recent code changes")
    project_context: Optional[Dict[str, Any]] = Field(None, description="Project context")
    user_preferences: Optional[Dict[str, Any]] = Field(None, description="User preferences")
    completion_history: Optional[List[str]] = Field(None, description="Completion history")
    suggestion_types: Optional[List[str]] = Field(None, description="Types of suggestions to generate")
    max_suggestions: int = Field(5, description="Maximum number of suggestions")


class CompletionSuggestionsResponse(BaseModel):
    """Response for completion suggestions"""
    suggestions: List[InlineCompletionResponse] = Field(..., description="List of suggestions")
    total_count: int = Field(..., description="Total number of suggestions")
    language: str = Field(..., description="Programming language")
    suggestion_types: List[str] = Field(..., description="Types of suggestions generated")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class CompletionConfidenceRequest(BaseModel):
    """Request for completion confidence scoring"""
    completion: InlineCompletionResponse = Field(..., description="Completion to score")
    context: InlineCompletionRequest = Field(..., description="Completion context")


class CompletionConfidenceResponse(BaseModel):
    """Response for completion confidence scoring"""
    confidence_score: float = Field(..., description="Confidence score (0-1)")
    factors: Dict[str, float] = Field(..., description="Confidence factors")
    recommendations: List[str] = Field(..., description="Improvement recommendations")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class CompletionPerformanceRequest(BaseModel):
    """Request for completion performance metrics"""
    file_path: str = Field(..., description="Path to the file being edited")
    language: Language = Field(..., description="Programming language")
    content: str = Field(..., description="Current file content")
    cursor_line: int = Field(..., description="Current cursor line")
    cursor_column: int = Field(..., description="Current cursor column")


class CompletionPerformanceResponse(BaseModel):
    """Response for completion performance metrics"""
    response_time: float = Field(..., description="Response time in milliseconds")
    completion_confidence: float = Field(..., description="Completion confidence score")
    completion_accuracy: float = Field(..., description="Completion accuracy score")
    context_relevance: float = Field(..., description="Context relevance score")
    optimizations: Dict[str, Any] = Field(..., description="Performance optimizations")
    cache_hit: bool = Field(..., description="Whether completion was cached")
    memory_usage: float = Field(..., description="Memory usage percentage")
    cpu_usage: float = Field(..., description="CPU usage percentage")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class InlineCompletionStatus(BaseModel):
    """Status of in-line completion service"""
    service_active: bool = Field(..., description="Whether service is active")
    supported_languages: List[Language] = Field(..., description="Supported languages")
    completion_count: int = Field(..., description="Total completions generated")
    streaming_completions: int = Field(..., description="Streaming completions active")
    context_aware_completions: int = Field(..., description="Context-aware completions generated")
    intelligent_completions: int = Field(..., description="Intelligent completions generated")
    average_confidence: float = Field(..., description="Average completion confidence")
    average_accuracy: float = Field(..., description="Average completion accuracy")
    cache_size: int = Field(..., description="Completion cache size")
    performance_score: float = Field(..., description="Performance score (0-1)")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")


# ============================================================================
# CODEBASE-AWARE AI MEMORY SYSTEM MODELS
# ============================================================================

class FileStructure(BaseModel):
    """File structure representation"""
    file_path: str = Field(..., description="File path")
    file_type: str = Field(..., description="File type/extension")
    file_size: int = Field(..., description="File size in bytes")
    directory: str = Field(..., description="Directory path")
    relative_path: str = Field(..., description="Relative path from project root")
    is_directory: bool = Field(False, description="Whether this is a directory")
    children: Optional[List['FileStructure']] = Field(None, description="Child files/directories")
    last_modified: datetime = Field(..., description="Last modification time")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")


class ProjectStructure(BaseModel):
    """Complete project structure"""
    project_id: str = Field(..., description="Unique project identifier")
    project_name: str = Field(..., description="Project name")
    project_root: str = Field(..., description="Project root directory")
    file_tree: FileStructure = Field(..., description="Root file structure")
    total_files: int = Field(..., description="Total number of files")
    total_directories: int = Field(..., description="Total number of directories")
    languages_used: List[str] = Field(..., description="Programming languages used")
    frameworks: List[str] = Field(..., description="Frameworks detected")
    dependencies: List[str] = Field(..., description="Dependencies detected")
    config_files: List[str] = Field(..., description="Configuration files")
    last_analyzed: datetime = Field(default_factory=datetime.now, description="Last analysis time")


class CodingPattern(BaseModel):
    """Coding pattern representation"""
    pattern_id: str = Field(..., description="Unique pattern identifier")
    pattern_type: str = Field(..., description="Type of pattern (function, class, etc.)")
    pattern_name: str = Field(..., description="Pattern name")
    pattern_code: str = Field(..., description="Pattern code snippet")
    language: str = Field(..., description="Programming language")
    file_path: str = Field(..., description="File where pattern was found")
    line_number: int = Field(..., description="Line number where pattern starts")
    context: str = Field(..., description="Surrounding context")
    frequency: int = Field(1, description="How often this pattern appears")
    complexity: float = Field(..., description="Pattern complexity score")
    dependencies: List[str] = Field([], description="Pattern dependencies")
    related_patterns: List[str] = Field([], description="Related pattern IDs")
    last_seen: datetime = Field(default_factory=datetime.now, description="Last time pattern was seen")
    created_at: datetime = Field(default_factory=datetime.now, description="Pattern creation time")


class DependencyInfo(BaseModel):
    """Dependency information"""
    dependency_id: str = Field(..., description="Unique dependency identifier")
    name: str = Field(..., description="Dependency name")
    version: str = Field(..., description="Dependency version")
    type: str = Field(..., description="Dependency type (package, library, framework)")
    source: str = Field(..., description="Where dependency is defined")
    usage_count: int = Field(0, description="How many times dependency is used")
    files_using: List[str] = Field([], description="Files that use this dependency")
    import_statements: List[str] = Field([], description="Import statements")
    is_dev_dependency: bool = Field(False, description="Whether it's a dev dependency")
    last_used: datetime = Field(default_factory=datetime.now, description="Last usage time")


class ConfigInfo(BaseModel):
    """Configuration information"""
    config_id: str = Field(..., description="Unique config identifier")
    config_type: str = Field(..., description="Type of configuration")
    file_path: str = Field(..., description="Configuration file path")
    config_data: Dict[str, Any] = Field(..., description="Configuration data")
    environment: str = Field("default", description="Environment (dev, prod, test)")
    is_active: bool = Field(True, description="Whether configuration is active")
    last_modified: datetime = Field(default_factory=datetime.now, description="Last modification time")


class SessionContext(BaseModel):
    """Session context for cross-session memory"""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: str = Field(..., description="User identifier")
    project_id: str = Field(..., description="Project identifier")
    current_file: str = Field(..., description="Currently active file")
    cursor_position: Tuple[int, int] = Field(..., description="Cursor position (line, column)")
    recent_files: List[str] = Field([], description="Recently accessed files")
    recent_commands: List[str] = Field([], description="Recent commands/actions")
    working_directory: str = Field(..., description="Current working directory")
    git_branch: Optional[str] = Field(None, description="Current git branch")
    git_commit: Optional[str] = Field(None, description="Current git commit")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last activity time")
    session_start: datetime = Field(default_factory=datetime.now, description="Session start time")


class MemorySnapshot(BaseModel):
    """Complete memory snapshot of codebase"""
    snapshot_id: str = Field(..., description="Unique snapshot identifier")
    project_id: str = Field(..., description="Project identifier")
    project_structure: ProjectStructure = Field(..., description="Project structure")
    coding_patterns: List[CodingPattern] = Field([], description="All coding patterns")
    dependencies: List[DependencyInfo] = Field([], description="All dependencies")
    configs: List[ConfigInfo] = Field([], description="All configurations")
    session_context: Optional[SessionContext] = Field(None, description="Current session context")
    memory_size: int = Field(..., description="Total memory size in bytes")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update time")
    version: str = Field("1.0", description="Memory schema version")


class MemoryQuery(BaseModel):
    """Query for memory system"""
    query_type: str = Field(..., description="Type of query")
    query_text: str = Field(..., description="Query text")
    filters: Dict[str, Any] = Field({}, description="Query filters")
    limit: int = Field(100, description="Maximum results")
    include_context: bool = Field(True, description="Include context in results")


class MemorySearchResult(BaseModel):
    """Memory search result"""
    result_id: str = Field(..., description="Unique result identifier")
    result_type: str = Field(..., description="Type of result")
    content: str = Field(..., description="Result content")
    file_path: str = Field(..., description="File path")
    line_number: Optional[int] = Field(None, description="Line number")
    confidence: float = Field(..., description="Search confidence")
    context: Dict[str, Any] = Field({}, description="Additional context")
    timestamp: datetime = Field(default_factory=datetime.now, description="Result timestamp")


class MemoryAnalysisRequest(BaseModel):
    """Request for memory analysis"""
    project_path: str = Field(..., description="Project path to analyze")
    analysis_depth: str = Field("deep", description="Analysis depth: shallow, medium, deep, comprehensive")
    include_patterns: bool = Field(True, description="Include pattern analysis")
    include_dependencies: bool = Field(True, description="Include dependency analysis")
    include_configs: bool = Field(True, description="Include configuration analysis")
    update_existing: bool = Field(False, description="Update existing memory if found")


class MemoryAnalysisResponse(BaseModel):
    """Response for memory analysis"""
    analysis_id: str = Field(..., description="Analysis identifier")
    project_id: str = Field(..., description="Project identifier")
    memory_snapshot: MemorySnapshot = Field(..., description="Generated memory snapshot")
    analysis_time: float = Field(..., description="Analysis time in seconds")
    files_analyzed: int = Field(..., description="Number of files analyzed")
    patterns_found: int = Field(..., description="Number of patterns found")
    dependencies_found: int = Field(..., description="Number of dependencies found")
    configs_found: int = Field(..., description="Number of configurations found")
    analysis_summary: Dict[str, Any] = Field(..., description="Analysis summary")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")


class MemoryStatus(BaseModel):
    """Memory system status"""
    system_active: bool = Field(..., description="Whether memory system is active")
    total_projects: int = Field(..., description="Total projects in memory")
    total_patterns: int = Field(..., description="Total patterns stored")
    total_dependencies: int = Field(..., description="Total dependencies tracked")
    total_configs: int = Field(..., description="Total configurations stored")
    memory_usage: float = Field(..., description="Memory usage percentage")
    last_analysis: Optional[datetime] = Field(None, description="Last analysis time")
    cache_hit_rate: float = Field(..., description="Cache hit rate")
    performance_score: float = Field(..., description="Performance score")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")


# ============================================================================
# AUTHENTICATION MODELS FOR SMART CODING AI
# ============================================================================

class AuthPermission(str, Enum):
    """Authentication permission levels for Smart Coding AI"""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"
    OWNER = "owner"


class AuthScope(str, Enum):
    """Authentication scopes for Smart Coding AI"""
    COMPLETION = "completion"
    MEMORY = "memory"
    ANALYSIS = "analysis"
    SESSION = "session"
    ADMIN = "admin"


class SmartCodingAuthRequest(BaseModel):
    """Authentication request for Smart Coding AI operations"""
    user_id: str = Field(..., description="User ID")
    operation: str = Field(..., description="Operation being performed")
    scope: AuthScope = Field(..., description="Authentication scope")
    resource_id: Optional[str] = Field(None, description="Resource ID being accessed")
    project_id: Optional[str] = Field(None, description="Project ID for project-specific operations")
    session_id: Optional[str] = Field(None, description="Session ID for session-specific operations")


class SmartCodingAuthResponse(BaseModel):
    """Authentication response for Smart Coding AI operations"""
    authorized: bool = Field(..., description="Whether operation is authorized")
    permission_level: AuthPermission = Field(..., description="Permission level granted")
    expires_at: datetime = Field(..., description="When authorization expires")
    limitations: Dict[str, Any] = Field(default_factory=dict, description="Operation limitations")
    quota_remaining: Dict[str, int] = Field(default_factory=dict, description="Remaining quota")
    message: Optional[str] = Field(None, description="Authorization message")


class SmartCodingQuotaInfo(BaseModel):
    """Quota information for Smart Coding AI operations"""
    user_id: str = Field(..., description="User ID")
    daily_completions: int = Field(0, description="Daily completion quota")
    daily_memory_operations: int = Field(0, description="Daily memory operation quota")
    daily_analysis_operations: int = Field(0, description="Daily analysis operation quota")
    monthly_storage_mb: int = Field(0, description="Monthly storage quota in MB")
    concurrent_sessions: int = Field(1, description="Concurrent session limit")
    usage_stats: Dict[str, int] = Field(default_factory=dict, description="Current usage statistics")
    reset_date: datetime = Field(..., description="When quotas reset")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class SmartCodingAuthAudit(BaseModel):
    """Authentication audit log for Smart Coding AI"""
    audit_id: str = Field(..., description="Unique audit identifier")
    user_id: str = Field(..., description="User ID")
    operation: str = Field(..., description="Operation performed")
    scope: AuthScope = Field(..., description="Authentication scope")
    resource_id: Optional[str] = Field(None, description="Resource accessed")
    project_id: Optional[str] = Field(None, description="Project ID")
    session_id: Optional[str] = Field(None, description="Session ID")
    authorized: bool = Field(..., description="Whether operation was authorized")
    permission_level: AuthPermission = Field(..., description="Permission level used")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")
    timestamp: datetime = Field(default_factory=datetime.now, description="Operation timestamp")
    duration_ms: Optional[float] = Field(None, description="Operation duration in milliseconds")
    error_message: Optional[str] = Field(None, description="Error message if any")


class SmartCodingAuthConfig(BaseModel):
    """Authentication configuration for Smart Coding AI"""
    user_id: str = Field(..., description="User ID")
    enabled_features: List[str] = Field(default_factory=list, description="Enabled features")
    disabled_features: List[str] = Field(default_factory=list, description="Disabled features")
    permission_overrides: Dict[str, AuthPermission] = Field(default_factory=dict, description="Permission overrides")
    quota_overrides: Dict[str, int] = Field(default_factory=dict, description="Quota overrides")
    session_timeout_minutes: int = Field(60, description="Session timeout in minutes")
    require_2fa_for_admin: bool = Field(True, description="Require 2FA for admin operations")
    allow_api_access: bool = Field(True, description="Allow API access")
    allowed_ip_ranges: List[str] = Field(default_factory=list, description="Allowed IP ranges")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


# ============================================================================
# RBAC (ROLE-BASED ACCESS CONTROL) MODELS
# ============================================================================

class RoleType(str, Enum):
    """Role types for Smart Coding AI RBAC"""
    VIEWER = "viewer"
    DEVELOPER = "developer"
    ADMIN = "admin"
    OWNER = "owner"
    GUEST = "guest"
    COLLABORATOR = "collaborator"
    AUDITOR = "auditor"


class ResourceType(str, Enum):
    """Resource types for RBAC"""
    PROJECT = "project"
    FILE = "file"
    SESSION = "session"
    MEMORY = "memory"
    COMPLETION = "completion"
    ANALYSIS = "analysis"
    CONFIG = "config"
    USER = "user"


class ActionType(str, Enum):
    """Action types for RBAC"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    ADMIN = "admin"
    AUDIT = "audit"


class RBACRole(BaseModel):
    """RBAC Role definition"""
    role_id: str = Field(..., description="Unique role identifier")
    role_name: str = Field(..., description="Role name")
    role_type: RoleType = Field(..., description="Role type")
    description: str = Field(..., description="Role description")
    permissions: List[str] = Field(default_factory=list, description="Role permissions")
    resource_access: Dict[ResourceType, List[ActionType]] = Field(default_factory=dict, description="Resource access matrix")
    quota_limits: Dict[str, int] = Field(default_factory=dict, description="Quota limits for this role")
    is_system_role: bool = Field(False, description="Whether this is a system-defined role")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


class RBACPermission(BaseModel):
    """RBAC Permission definition"""
    permission_id: str = Field(..., description="Unique permission identifier")
    permission_name: str = Field(..., description="Permission name")
    resource_type: ResourceType = Field(..., description="Resource type")
    action_type: ActionType = Field(..., description="Action type")
    scope: str = Field(..., description="Permission scope")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Permission conditions")
    description: str = Field(..., description="Permission description")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class RBACAssignment(BaseModel):
    """RBAC Role assignment"""
    assignment_id: str = Field(..., description="Unique assignment identifier")
    user_id: str = Field(..., description="User ID")
    role_id: str = Field(..., description="Role ID")
    resource_id: Optional[str] = Field(None, description="Specific resource ID (for resource-specific roles)")
    resource_type: Optional[ResourceType] = Field(None, description="Resource type")
    granted_by: str = Field(..., description="User ID who granted this role")
    granted_at: datetime = Field(default_factory=datetime.now, description="Grant timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")
    is_active: bool = Field(True, description="Whether assignment is active")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class RBACPolicy(BaseModel):
    """RBAC Policy definition"""
    policy_id: str = Field(..., description="Unique policy identifier")
    policy_name: str = Field(..., description="Policy name")
    description: str = Field(..., description="Policy description")
    rules: List[Dict[str, Any]] = Field(default_factory=list, description="Policy rules")
    conditions: Dict[str, Any] = Field(default_factory=dict, description="Policy conditions")
    effect: str = Field("allow", description="Policy effect (allow/deny)")
    priority: int = Field(100, description="Policy priority")
    is_active: bool = Field(True, description="Whether policy is active")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


# ============================================================================
# STATE MANAGER MODELS
# ============================================================================

class StateType(str, Enum):
    """State types for StateManager"""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    SESSION = "session"
    PROJECT = "project"
    MEMORY = "memory"
    COMPLETION = "completion"
    ANALYSIS = "analysis"
    USER_PREFERENCES = "user_preferences"
    SYSTEM_CONFIG = "system_config"


class StateStatus(str, Enum):
    """State status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    PENDING = "pending"
    ERROR = "error"


class StateTransition(BaseModel):
    """State transition definition"""
    transition_id: str = Field(..., description="Unique transition identifier")
    from_state: str = Field(..., description="Source state")
    to_state: str = Field(..., description="Target state")
    condition: str = Field(..., description="Transition condition")
    action: str = Field(..., description="Action to perform during transition")
    permissions_required: List[str] = Field(default_factory=list, description="Required permissions")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")


class StateSnapshot(BaseModel):
    """State snapshot for StateManager"""
    snapshot_id: str = Field(..., description="Unique snapshot identifier")
    entity_id: str = Field(..., description="Entity ID")
    entity_type: str = Field(..., description="Entity type")
    state_type: StateType = Field(..., description="State type")
    current_state: str = Field(..., description="Current state")
    state_data: Dict[str, Any] = Field(default_factory=dict, description="State data")
    previous_state: Optional[str] = Field(None, description="Previous state")
    status: StateStatus = Field(StateStatus.ACTIVE, description="State status")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    expires_at: Optional[datetime] = Field(None, description="Expiration timestamp")


class StateEvent(BaseModel):
    """State event for StateManager"""
    event_id: str = Field(..., description="Unique event identifier")
    entity_id: str = Field(..., description="Entity ID")
    entity_type: str = Field(..., description="Entity type")
    event_type: str = Field(..., description="Event type")
    state_type: StateType = Field(..., description="State type")
    from_state: Optional[str] = Field(None, description="Source state")
    to_state: Optional[str] = Field(None, description="Target state")
    event_data: Dict[str, Any] = Field(default_factory=dict, description="Event data")
    user_id: Optional[str] = Field(None, description="User who triggered the event")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")
    correlation_id: Optional[str] = Field(None, description="Correlation ID for related events")


class StateManagerConfig(BaseModel):
    """StateManager configuration"""
    config_id: str = Field(..., description="Unique config identifier")
    state_type: StateType = Field(..., description="State type")
    initial_state: str = Field(..., description="Initial state")
    allowed_transitions: List[StateTransition] = Field(default_factory=list, description="Allowed transitions")
    state_timeouts: Dict[str, int] = Field(default_factory=dict, description="State timeouts in seconds")
    persistence_config: Dict[str, Any] = Field(default_factory=dict, description="Persistence configuration")
    notification_config: Dict[str, Any] = Field(default_factory=dict, description="Notification configuration")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


# ============================================================================
# OAUTH MODELS FOR SMART CODING AI
# ============================================================================

class OAuthProvider(str, Enum):
    """OAuth providers supported by Smart Coding AI"""
    GOOGLE = "google"
    GITHUB = "github"
    MICROSOFT = "microsoft"
    APPLE = "apple"


class OAuthRequest(BaseModel):
    """OAuth login request"""
    provider: OAuthProvider = Field(..., description="OAuth provider")
    redirect_uri: Optional[str] = Field(None, description="Redirect URI after authentication")
    state: Optional[str] = Field(None, description="State parameter for security")
    scope: Optional[List[str]] = Field(default_factory=list, description="Requested OAuth scopes")


class OAuthResponse(BaseModel):
    """OAuth response"""
    auth_url: str = Field(..., description="OAuth authorization URL")
    state: str = Field(..., description="State parameter for security")
    expires_at: datetime = Field(..., description="When the auth URL expires")
    provider: OAuthProvider = Field(..., description="OAuth provider")


class OAuthCallbackRequest(BaseModel):
    """OAuth callback request"""
    code: str = Field(..., description="Authorization code from OAuth provider")
    state: str = Field(..., description="State parameter for security")
    provider: OAuthProvider = Field(..., description="OAuth provider")


class OAuthTokenResponse(BaseModel):
    """OAuth token response"""
    access_token: str = Field(..., description="OAuth access token")
    refresh_token: Optional[str] = Field(None, description="OAuth refresh token")
    token_type: str = Field("Bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    scope: Optional[str] = Field(None, description="Token scope")
    provider: OAuthProvider = Field(..., description="OAuth provider")


class OAuthUserInfo(BaseModel):
    """OAuth user information"""
    provider: OAuthProvider = Field(..., description="OAuth provider")
    provider_id: str = Field(..., description="User ID from OAuth provider")
    email: str = Field(..., description="User email")
    name: Optional[str] = Field(None, description="User display name")
    avatar_url: Optional[str] = Field(None, description="User avatar URL")
    username: Optional[str] = Field(None, description="Username from provider")
    profile_data: Dict[str, Any] = Field(default_factory=dict, description="Additional profile data")


class OAuthLoginResponse(BaseModel):
    """OAuth login response"""
    user: User = Field(..., description="User information")
    access_token: str = Field(..., description="Smart Coding AI access token")
    refresh_token: str = Field(..., description="Smart Coding AI refresh token")
    expires_in: int = Field(..., description="Token expiration time")
    oauth_provider: OAuthProvider = Field(..., description="OAuth provider used")
    is_new_user: bool = Field(False, description="Whether this is a new user")
    requires_profile_completion: bool = Field(False, description="Whether profile completion is required")


class OAuthConfig(BaseModel):
    """OAuth configuration for Smart Coding AI"""
    provider: OAuthProvider = Field(..., description="OAuth provider")
    client_id: str = Field(..., description="OAuth client ID")
    client_secret: str = Field(..., description="OAuth client secret")
    redirect_uri: str = Field(..., description="OAuth redirect URI")
    scopes: List[str] = Field(default_factory=list, description="OAuth scopes")
    auth_url: str = Field(..., description="OAuth authorization URL")
    token_url: str = Field(..., description="OAuth token URL")
    user_info_url: str = Field(..., description="OAuth user info URL")
    is_enabled: bool = Field(True, description="Whether OAuth provider is enabled")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")


# ============================================================================
# CACHE/QUEUE/TELEMETRY INFRASTRUCTURE MODELS
# ============================================================================

class CacheType(str, Enum):
    """Cache types for Smart Coding AI"""
    REDIS = "redis"
    MEMORY = "memory"
    FILE = "file"
    DATABASE = "database"


class CacheStrategy(str, Enum):
    """Cache strategies"""
    LRU = "lru"  # Least Recently Used
    LFU = "lfu"  # Least Frequently Used
    TTL = "ttl"  # Time To Live
    WRITE_THROUGH = "write_through"
    WRITE_BACK = "write_back"


class CacheOperation(str, Enum):
    """Cache operations"""
    GET = "get"
    SET = "set"
    DELETE = "delete"
    CLEAR = "clear"
    EXISTS = "exists"
    KEYS = "keys"
    STATS = "stats"


class CacheItem(BaseModel):
    """Cache item"""
    key: str = Field(..., description="Cache key")
    value: Any = Field(..., description="Cached value")
    ttl: Optional[int] = Field(None, description="Time to live in seconds")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    accessed_at: Optional[datetime] = Field(None, description="Last access timestamp")
    access_count: int = Field(0, description="Number of times accessed")
    size_bytes: int = Field(0, description="Size in bytes")


class CacheStats(BaseModel):
    """Cache statistics"""
    total_items: int = Field(0, description="Total cached items")
    total_size_bytes: int = Field(0, description="Total cache size in bytes")
    hit_count: int = Field(0, description="Cache hits")
    miss_count: int = Field(0, description="Cache misses")
    hit_rate: float = Field(0.0, description="Cache hit rate")
    eviction_count: int = Field(0, description="Number of evictions")
    memory_usage: float = Field(0.0, description="Memory usage percentage")
    created_at: datetime = Field(default_factory=datetime.now, description="Stats timestamp")


class CacheRequest(BaseModel):
    """Cache operation request"""
    operation: CacheOperation = Field(..., description="Cache operation")
    key: Optional[str] = Field(None, description="Cache key")
    value: Optional[Any] = Field(None, description="Value to cache")
    ttl: Optional[int] = Field(None, description="Time to live in seconds")
    namespace: Optional[str] = Field("default", description="Cache namespace")


class CacheResponse(BaseModel):
    """Cache operation response"""
    success: bool = Field(..., description="Operation success")
    value: Optional[Any] = Field(None, description="Retrieved value")
    message: str = Field("", description="Response message")
    stats: Optional[CacheStats] = Field(None, description="Cache statistics")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class QueueType(str, Enum):
    """Queue types"""
    REDIS = "redis"
    MEMORY = "memory"
    DATABASE = "database"
    RABBITMQ = "rabbitmq"
    SQS = "sqs"


class QueuePriority(str, Enum):
    """Queue priorities"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class QueueStatus(str, Enum):
    """Queue status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY = "retry"
    CANCELLED = "cancelled"


class QueueItem(BaseModel):
    """Queue item"""
    id: str = Field(..., description="Queue item ID")
    queue_name: str = Field(..., description="Queue name")
    data: Dict[str, Any] = Field(..., description="Queue item data")
    priority: QueuePriority = Field(QueuePriority.NORMAL, description="Item priority")
    status: QueueStatus = Field(QueueStatus.PENDING, description="Item status")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Processing start time")
    completed_at: Optional[datetime] = Field(None, description="Completion time")
    retry_count: int = Field(0, description="Number of retries")
    max_retries: int = Field(3, description="Maximum retries")
    error_message: Optional[str] = Field(None, description="Error message if failed")


class QueueStats(BaseModel):
    """Queue statistics"""
    queue_name: str = Field(..., description="Queue name")
    total_items: int = Field(0, description="Total items")
    pending_items: int = Field(0, description="Pending items")
    processing_items: int = Field(0, description="Processing items")
    completed_items: int = Field(0, description="Completed items")
    failed_items: int = Field(0, description="Failed items")
    avg_processing_time: float = Field(0.0, description="Average processing time in seconds")
    throughput_per_minute: float = Field(0.0, description="Items processed per minute")
    created_at: datetime = Field(default_factory=datetime.now, description="Stats timestamp")


class QueueRequest(BaseModel):
    """Queue operation request"""
    queue_name: str = Field(..., description="Queue name")
    data: Dict[str, Any] = Field(..., description="Data to queue")
    priority: QueuePriority = Field(QueuePriority.NORMAL, description="Item priority")
    delay: Optional[int] = Field(None, description="Delay in seconds before processing")
    max_retries: int = Field(3, description="Maximum retries")


class QueueResponse(BaseModel):
    """Queue operation response"""
    success: bool = Field(..., description="Operation success")
    item_id: Optional[str] = Field(None, description="Queue item ID")
    message: str = Field("", description="Response message")
    stats: Optional[QueueStats] = Field(None, description="Queue statistics")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class TelemetryType(str, Enum):
    """Telemetry types"""
    METRIC = "metric"
    EVENT = "event"
    LOG = "log"
    TRACE = "trace"
    PERFORMANCE = "performance"
    ERROR = "error"


class TelemetryLevel(str, Enum):
    """Telemetry levels"""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class TelemetryMetric(BaseModel):
    """Telemetry metric"""
    name: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    type: TelemetryType = Field(TelemetryType.METRIC, description="Telemetry type")
    level: TelemetryLevel = Field(TelemetryLevel.INFO, description="Telemetry level")
    tags: Dict[str, str] = Field(default_factory=dict, description="Metric tags")
    timestamp: datetime = Field(default_factory=datetime.now, description="Metric timestamp")
    source: str = Field("smart_coding_ai", description="Source system")
    user_id: Optional[str] = Field(None, description="User ID if applicable")
    session_id: Optional[str] = Field(None, description="Session ID if applicable")


class TelemetryEvent(BaseModel):
    """Telemetry event"""
    event_name: str = Field(..., description="Event name")
    event_data: Dict[str, Any] = Field(..., description="Event data")
    type: TelemetryType = Field(TelemetryType.EVENT, description="Telemetry type")
    level: TelemetryLevel = Field(TelemetryLevel.INFO, description="Telemetry level")
    tags: Dict[str, str] = Field(default_factory=dict, description="Event tags")
    timestamp: datetime = Field(default_factory=datetime.now, description="Event timestamp")
    source: str = Field("smart_coding_ai", description="Source system")
    user_id: Optional[str] = Field(None, description="User ID if applicable")
    session_id: Optional[str] = Field(None, description="Session ID if applicable")


class TelemetryRequest(BaseModel):
    """Telemetry request"""
    metrics: List[TelemetryMetric] = Field(default_factory=list, description="Metrics to record")
    events: List[TelemetryEvent] = Field(default_factory=list, description="Events to record")
    batch_size: int = Field(100, description="Batch size for processing")


class TelemetryResponse(BaseModel):
    """Telemetry response"""
    success: bool = Field(..., description="Operation success")
    metrics_recorded: int = Field(0, description="Number of metrics recorded")
    events_recorded: int = Field(0, description="Number of events recorded")
    message: str = Field("", description="Response message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


# ============================================================================
# CHAT WITH YOUR CODEBASE MODELS
# ============================================================================

class CodebaseChatRequest(BaseModel):
    """Request for chatting with codebase"""
    query: str = Field(..., description="Natural language question about the codebase")
    project_id: str = Field(..., description="Project identifier")
    context_type: str = Field("general", description="Type of context: general, debug, flow, component")
    include_code_snippets: bool = Field(True, description="Include code snippets in response")
    max_results: int = Field(10, description="Maximum number of results to return")
    focus_files: Optional[List[str]] = Field(None, description="Specific files to focus on")

class CodebaseChatResponse(BaseModel):
    """Response from codebase chat"""
    answer: str = Field(..., description="Natural language answer to the query")
    confidence: float = Field(..., description="Confidence score for the answer")
    code_snippets: List[Dict[str, Any]] = Field([], description="Relevant code snippets")
    related_files: List[str] = Field([], description="Files referenced in the answer")
    analysis_type: str = Field(..., description="Type of analysis performed")
    follow_up_questions: List[str] = Field([], description="Suggested follow-up questions")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")

class CodeFlowAnalysis(BaseModel):
    """Code flow analysis result"""
    flow_id: str = Field(..., description="Unique flow analysis identifier")
    flow_name: str = Field(..., description="Name of the flow being analyzed")
    flow_type: str = Field(..., description="Type of flow: data, authentication, business_logic")
    entry_points: List[str] = Field(..., description="Entry points to the flow")
    exit_points: List[str] = Field(..., description="Exit points from the flow")
    intermediate_steps: List[Dict[str, Any]] = Field(..., description="Intermediate steps in the flow")
    dependencies: List[str] = Field([], description="Dependencies involved in the flow")
    files_involved: List[str] = Field(..., description="Files involved in the flow")
    complexity_score: float = Field(..., description="Complexity score of the flow")

class ComponentRelationship(BaseModel):
    """Component relationship analysis"""
    component_id: str = Field(..., description="Unique component identifier")
    component_name: str = Field(..., description="Name of the component")
    component_type: str = Field(..., description="Type of component: class, function, module")
    file_path: str = Field(..., description="File containing the component")
    dependencies: List[str] = Field([], description="Components this depends on")
    dependents: List[str] = Field([], description="Components that depend on this")
    relationships: List[Dict[str, Any]] = Field([], description="Detailed relationship information")
    usage_frequency: int = Field(0, description="How often this component is used")
    last_modified: datetime = Field(..., description="Last modification time")

class ChatAnalysisRequest(BaseModel):
    """Request for specific chat analysis"""
    query: str = Field(..., description="Analysis query")
    project_id: str = Field(..., description="Project identifier")
    analysis_type: str = Field(..., description="Type of analysis: flow, component, debug, search")
    include_context: bool = Field(True, description="Include additional context")
    max_depth: int = Field(5, description="Maximum analysis depth")

class ChatAnalysisResponse(BaseModel):
    """Response from chat analysis"""
    analysis_result: Dict[str, Any] = Field(..., description="Analysis result")
    confidence: float = Field(..., description="Confidence score")
    related_components: List[ComponentRelationship] = Field([], description="Related components")
    code_flows: List[CodeFlowAnalysis] = Field([], description="Related code flows")
    suggestions: List[str] = Field([], description="Suggestions based on analysis")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
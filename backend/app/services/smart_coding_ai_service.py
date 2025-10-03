"""
Smart Coding AI Service with in-editor code completion
Provides real-time code suggestions, completions, and intelligent assistance
"""

import structlog
import asyncio
import json
import re
from typing import Dict, List, Optional, Any, Tuple, Union
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import uuid

logger = structlog.get_logger()


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


class SuggestionType(str, Enum):
    """Suggestion types"""
    COMPLETION = "completion"
    HINT = "hint"
    ERROR_FIX = "error_fix"
    REFACTOR = "refactor"
    OPTIMIZATION = "optimization"
    DOCUMENTATION = "documentation"


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
    parameters: Optional[List[Dict]] = None
    return_type: Optional[str] = None
    created_at: datetime


@dataclass
class CodeSuggestion:
    """Code suggestion model"""
    suggestion_id: str
    suggestion_type: SuggestionType
    text: str
    language: Language
    confidence: float
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    description: str
    priority: int  # 1-10, higher is more important
    auto_apply: bool = False
    created_at: datetime


@dataclass
class CodeContext:
    """Code context model"""
    file_path: str
    language: Language
    content: str
    cursor_position: Tuple[int, int]  # (line, column)
    selection: Optional[str] = None
    imports: List[str] = None
    functions: List[Dict] = None
    classes: List[Dict] = None
    variables: List[Dict] = None


class SmartCodingAI:
    """Smart Coding AI service with in-editor code completion"""
    
    def __init__(self):
        self.completion_cache: Dict[str, List[CodeCompletion]] = {}
        self.suggestion_cache: Dict[str, List[CodeSuggestion]] = {}
        self.language_patterns = self._initialize_language_patterns()
        self.completion_templates = self._initialize_completion_templates()
        self._initialize_ai_models()
    
    def _initialize_language_patterns(self) -> Dict[Language, Dict[str, str]]:
        """Initialize language-specific patterns"""
        return {
            Language.PYTHON: {
                "function": r"def\s+(\w+)\s*\(",
                "class": r"class\s+(\w+)\s*[\(:]",
                "variable": r"(\w+)\s*=",
                "import": r"(?:from\s+(\w+)\s+)?import\s+(\w+)",
                "method": r"def\s+(\w+)\s*\(",
                "property": r"@property\s*\n\s*def\s+(\w+)\s*\(",
            },
            Language.JAVASCRIPT: {
                "function": r"function\s+(\w+)\s*\(",
                "class": r"class\s+(\w+)\s*[{\s]",
                "variable": r"(?:const|let|var)\s+(\w+)\s*=",
                "import": r"import\s+(?:\{([^}]+)\}\s+from\s+)?['\"]([^'\"]+)['\"]",
                "method": r"(\w+)\s*:\s*function\s*\(",
                "property": r"(\w+)\s*:\s*",
            },
            Language.TYPESCRIPT: {
                "function": r"function\s+(\w+)\s*\(",
                "class": r"class\s+(\w+)\s*[{\s]",
                "variable": r"(?:const|let|var)\s+(\w+)\s*:",
                "import": r"import\s+(?:\{([^}]+)\}\s+from\s+)?['\"]([^'\"]+)['\"]",
                "method": r"(\w+)\s*:\s*\([^)]*\)\s*=>",
                "property": r"(\w+)\s*:\s*",
                "type": r"type\s+(\w+)\s*=",
                "interface": r"interface\s+(\w+)\s*[{\s]",
            },
            Language.JAVA: {
                "function": r"(?:public|private|protected)?\s*(?:static\s+)?\s*(?:void|\w+)\s+(\w+)\s*\(",
                "class": r"(?:public\s+)?class\s+(\w+)\s*[{\s]",
                "variable": r"(?:public|private|protected)?\s*(?:static\s+)?\s*(?:final\s+)?\s*(\w+)\s+(\w+)\s*=",
                "import": r"import\s+([^;]+);",
                "method": r"(?:public|private|protected)?\s*(?:static\s+)?\s*(?:void|\w+)\s+(\w+)\s*\(",
                "property": r"(?:public|private|protected)?\s*(?:static\s+)?\s*(?:final\s+)?\s*(\w+)\s+(\w+)\s*;",
            },
            Language.CSHARP: {
                "function": r"(?:public|private|protected)?\s*(?:static\s+)?\s*(?:void|\w+)\s+(\w+)\s*\(",
                "class": r"(?:public\s+)?class\s+(\w+)\s*[{\s]",
                "variable": r"(?:public|private|protected)?\s*(?:static\s+)?\s*(?:readonly\s+)?\s*(\w+)\s+(\w+)\s*=",
                "import": r"using\s+([^;]+);",
                "method": r"(?:public|private|protected)?\s*(?:static\s+)?\s*(?:void|\w+)\s+(\w+)\s*\(",
                "property": r"(?:public|private|protected)?\s*(?:static\s+)?\s*(?:readonly\s+)?\s*(\w+)\s+(\w+)\s*{\s*get;\s*set;\s*}",
            },
        }
    
    def _initialize_completion_templates(self) -> Dict[Language, Dict[str, List[str]]]:
        """Initialize completion templates for each language"""
        return {
            Language.PYTHON: {
                "function": [
                    "def {name}({params}):\n    \"\"\"{description}\"\"\"\n    {body}",
                    "async def {name}({params}):\n    \"\"\"{description}\"\"\"\n    {body}",
                ],
                "class": [
                    "class {name}:\n    \"\"\"{description}\"\"\"\n    \n    def __init__(self{params}):\n        {body}",
                    "class {name}({base}):\n    \"\"\"{description}\"\"\"\n    \n    def __init__(self{params}):\n        super().__init__()\n        {body}",
                ],
                "import": [
                    "import {module}",
                    "from {module} import {item}",
                    "from {module} import {item} as {alias}",
                ],
            },
            Language.JAVASCRIPT: {
                "function": [
                    "function {name}({params}) {\n    {body}\n}",
                    "const {name} = ({params}) => {\n    {body}\n};",
                    "async function {name}({params}) {\n    {body}\n}",
                ],
                "class": [
                    "class {name} {\n    constructor({params}) {\n        {body}\n    }\n}",
                    "class {name} extends {base} {\n    constructor({params}) {\n        super();\n        {body}\n    }\n}",
                ],
                "import": [
                    "import { {item} } from '{module}';",
                    "import {item} from '{module}';",
                    "import * as {alias} from '{module}';",
                ],
            },
            Language.TYPESCRIPT: {
                "function": [
                    "function {name}({params}): {return_type} {\n    {body}\n}",
                    "const {name} = ({params}): {return_type} => {\n    {body}\n};",
                    "async function {name}({params}): Promise<{return_type}> {\n    {body}\n}",
                ],
                "class": [
                    "class {name} {\n    constructor({params}) {\n        {body}\n    }\n}",
                    "class {name} extends {base} {\n    constructor({params}) {\n        super();\n        {body}\n    }\n}",
                ],
                "interface": [
                    "interface {name} {\n    {properties}\n}",
                ],
                "type": [
                    "type {name} = {definition};",
                ],
            },
        }
    
    def _initialize_ai_models(self):
        """Initialize AI models for code completion"""
        # This would integrate with actual AI models
        # For now, we'll use pattern-based completion
        self.models_initialized = True
        logger.info("AI models initialized for code completion")
    
    async def get_code_completions(
        self, 
        context: CodeContext, 
        max_completions: int = 10
    ) -> List[CodeCompletion]:
        """Get code completions for the given context"""
        try:
            cache_key = f"{context.file_path}:{context.cursor_position[0]}:{context.cursor_position[1]}"
            
            # Check cache first
            if cache_key in self.completion_cache:
                return self.completion_cache[cache_key][:max_completions]
            
            completions = []
            
            # Get completions based on language
            if context.language == Language.PYTHON:
                completions = await self._get_python_completions(context)
            elif context.language == Language.JAVASCRIPT:
                completions = await self._get_javascript_completions(context)
            elif context.language == Language.TYPESCRIPT:
                completions = await self._get_typescript_completions(context)
            elif context.language == Language.JAVA:
                completions = await self._get_java_completions(context)
            elif context.language == Language.CSHARP:
                completions = await self._get_csharp_completions(context)
            else:
                completions = await self._get_generic_completions(context)
            
            # Sort by confidence
            completions.sort(key=lambda x: x.confidence, reverse=True)
            
            # Cache results
            self.completion_cache[cache_key] = completions
            
            logger.info("Code completions generated", 
                       count=len(completions), 
                       language=context.language.value)
            
            return completions[:max_completions]
            
        except Exception as e:
            logger.error("Failed to get code completions", error=str(e))
            return []
    
    async def _get_python_completions(self, context: CodeContext) -> List[CodeCompletion]:
        """Get Python-specific completions"""
        completions = []
        
        # Built-in functions
        builtin_functions = [
            "print", "len", "str", "int", "float", "bool", "list", "dict", "set", "tuple",
            "range", "enumerate", "zip", "map", "filter", "sorted", "reversed", "sum", "max", "min",
            "abs", "round", "pow", "divmod", "bin", "hex", "oct", "chr", "ord", "ascii",
            "repr", "eval", "exec", "compile", "hash", "id", "type", "isinstance", "issubclass",
            "hasattr", "getattr", "setattr", "delattr", "dir", "vars", "locals", "globals",
            "open", "input", "raw_input", "file", "help", "quit", "exit", "copyright", "credits", "license"
        ]
        
        for func in builtin_functions:
            if func.startswith(context.content.split()[-1] if context.content.split() else ""):
                completions.append(CodeCompletion(
                    completion_id=str(uuid.uuid4()),
                    text=func,
                    completion_type=CompletionType.FUNCTION,
                    language=Language.PYTHON,
                    confidence=0.9,
                    start_line=context.cursor_position[0],
                    end_line=context.cursor_position[0],
                    start_column=context.cursor_position[1],
                    end_column=context.cursor_position[1] + len(func),
                    description=f"Built-in function: {func}",
                    documentation=f"Python built-in function: {func}",
                    return_type="Any"
                ))
        
        # Common patterns
        if "import" in context.content:
            # Suggest common modules
            common_modules = [
                "os", "sys", "json", "datetime", "time", "random", "math", "re", "collections",
                "itertools", "functools", "operator", "string", "io", "pathlib", "typing"
            ]
            
            for module in common_modules:
                completions.append(CodeCompletion(
                    completion_id=str(uuid.uuid4()),
                    text=module,
                    completion_type=CompletionType.IMPORT,
                    language=Language.PYTHON,
                    confidence=0.8,
                    start_line=context.cursor_position[0],
                    end_line=context.cursor_position[0],
                    start_column=context.cursor_position[1],
                    end_column=context.cursor_position[1] + len(module),
                    description=f"Import module: {module}",
                    documentation=f"Python standard library module: {module}"
                ))
        
        return completions
    
    async def _get_javascript_completions(self, context: CodeContext) -> List[CodeCompletion]:
        """Get JavaScript-specific completions"""
        completions = []
        
        # Built-in methods
        builtin_methods = [
            "console.log", "console.error", "console.warn", "console.info",
            "JSON.stringify", "JSON.parse", "parseInt", "parseFloat", "isNaN", "isFinite",
            "encodeURIComponent", "decodeURIComponent", "encodeURI", "decodeURI",
            "setTimeout", "setInterval", "clearTimeout", "clearInterval",
            "Promise.resolve", "Promise.reject", "Promise.all", "Promise.race",
            "Array.from", "Array.isArray", "Object.keys", "Object.values", "Object.entries",
            "Object.assign", "Object.create", "Object.freeze", "Object.seal"
        ]
        
        for method in builtin_methods:
            if method.startswith(context.content.split()[-1] if context.content.split() else ""):
                completions.append(CodeCompletion(
                    completion_id=str(uuid.uuid4()),
                    text=method,
                    completion_type=CompletionType.METHOD,
                    language=Language.JAVASCRIPT,
                    confidence=0.9,
                    start_line=context.cursor_position[0],
                    end_line=context.cursor_position[0],
                    start_column=context.cursor_position[1],
                    end_column=context.cursor_position[1] + len(method),
                    description=f"Built-in method: {method}",
                    documentation=f"JavaScript built-in method: {method}"
                ))
        
        return completions
    
    async def _get_typescript_completions(self, context: CodeContext) -> List[CodeCompletion]:
        """Get TypeScript-specific completions"""
        completions = []
        
        # TypeScript types
        types = [
            "string", "number", "boolean", "object", "any", "void", "null", "undefined",
            "never", "unknown", "Array", "Promise", "Function", "Date", "RegExp",
            "Error", "Map", "Set", "WeakMap", "WeakSet", "Symbol", "BigInt"
        ]
        
        for type_name in types:
            if type_name.startswith(context.content.split()[-1] if context.content.split() else ""):
                completions.append(CodeCompletion(
                    completion_id=str(uuid.uuid4()),
                    text=type_name,
                    completion_type=CompletionType.TYPE,
                    language=Language.TYPESCRIPT,
                    confidence=0.9,
                    start_line=context.cursor_position[0],
                    end_line=context.cursor_position[0],
                    start_column=context.cursor_position[1],
                    end_column=context.cursor_position[1] + len(type_name),
                    description=f"TypeScript type: {type_name}",
                    documentation=f"TypeScript built-in type: {type_name}"
                ))
        
        return completions
    
    async def _get_java_completions(self, context: CodeContext) -> List[CodeCompletion]:
        """Get Java-specific completions"""
        completions = []
        
        # Java keywords and common classes
        java_keywords = [
            "public", "private", "protected", "static", "final", "abstract", "interface",
            "class", "extends", "implements", "import", "package", "new", "this", "super",
            "if", "else", "for", "while", "do", "switch", "case", "break", "continue",
            "return", "try", "catch", "finally", "throw", "throws", "synchronized", "volatile"
        ]
        
        for keyword in java_keywords:
            if keyword.startswith(context.content.split()[-1] if context.content.split() else ""):
                completions.append(CodeCompletion(
                    completion_id=str(uuid.uuid4()),
                    text=keyword,
                    completion_type=CompletionType.KEYWORD,
                    language=Language.JAVA,
                    confidence=0.9,
                    start_line=context.cursor_position[0],
                    end_line=context.cursor_position[0],
                    start_column=context.cursor_position[1],
                    end_column=context.cursor_position[1] + len(keyword),
                    description=f"Java keyword: {keyword}",
                    documentation=f"Java language keyword: {keyword}"
                ))
        
        return completions
    
    async def _get_csharp_completions(self, context: CodeContext) -> List[CodeCompletion]:
        """Get C#-specific completions"""
        completions = []
        
        # C# keywords
        csharp_keywords = [
            "public", "private", "protected", "internal", "static", "readonly", "const",
            "class", "struct", "interface", "enum", "namespace", "using", "new", "this", "base",
            "if", "else", "for", "foreach", "while", "do", "switch", "case", "break", "continue",
            "return", "try", "catch", "finally", "throw", "async", "await", "var", "dynamic"
        ]
        
        for keyword in csharp_keywords:
            if keyword.startswith(context.content.split()[-1] if context.content.split() else ""):
                completions.append(CodeCompletion(
                    completion_id=str(uuid.uuid4()),
                    text=keyword,
                    completion_type=CompletionType.KEYWORD,
                    language=Language.CSHARP,
                    confidence=0.9,
                    start_line=context.cursor_position[0],
                    end_line=context.cursor_position[0],
                    start_column=context.cursor_position[1],
                    end_column=context.cursor_position[1] + len(keyword),
                    description=f"C# keyword: {keyword}",
                    documentation=f"C# language keyword: {keyword}"
                ))
        
        return completions
    
    async def _get_generic_completions(self, context: CodeContext) -> List[CodeCompletion]:
        """Get generic completions for any language"""
        completions = []
        
        # Common patterns
        common_patterns = [
            "function", "class", "import", "export", "const", "let", "var", "if", "else",
            "for", "while", "return", "try", "catch", "finally", "public", "private"
        ]
        
        for pattern in common_patterns:
            if pattern.startswith(context.content.split()[-1] if context.content.split() else ""):
                completions.append(CodeCompletion(
                    completion_id=str(uuid.uuid4()),
                    text=pattern,
                    completion_type=CompletionType.KEYWORD,
                    language=context.language,
                    confidence=0.7,
                    start_line=context.cursor_position[0],
                    end_line=context.cursor_position[0],
                    start_column=context.cursor_position[1],
                    end_column=context.cursor_position[1] + len(pattern),
                    description=f"Common pattern: {pattern}",
                    documentation=f"Common programming pattern: {pattern}"
                ))
        
        return completions
    
    async def get_code_suggestions(
        self, 
        context: CodeContext, 
        max_suggestions: int = 5
    ) -> List[CodeSuggestion]:
        """Get code suggestions for improvements, fixes, and optimizations"""
        try:
            suggestions = []
            
            # Analyze code for suggestions
            if context.language == Language.PYTHON:
                suggestions = await self._analyze_python_code(context)
            elif context.language == Language.JAVASCRIPT:
                suggestions = await self._analyze_javascript_code(context)
            elif context.language == Language.TYPESCRIPT:
                suggestions = await self._analyze_typescript_code(context)
            else:
                suggestions = await self._analyze_generic_code(context)
            
            # Sort by priority
            suggestions.sort(key=lambda x: x.priority, reverse=True)
            
            logger.info("Code suggestions generated", 
                       count=len(suggestions), 
                       language=context.language.value)
            
            return suggestions[:max_suggestions]
            
        except Exception as e:
            logger.error("Failed to get code suggestions", error=str(e))
            return []
    
    async def _analyze_python_code(self, context: CodeContext) -> List[CodeSuggestion]:
        """Analyze Python code for suggestions"""
        suggestions = []
        
        # Check for common Python issues
        if "print(" in context.content and "logging" not in context.content:
            suggestions.append(CodeSuggestion(
                suggestion_id=str(uuid.uuid4()),
                suggestion_type=SuggestionType.OPTIMIZATION,
                text="Consider using logging instead of print statements",
                language=Language.PYTHON,
                confidence=0.8,
                start_line=context.cursor_position[0],
                end_line=context.cursor_position[0],
                start_column=context.cursor_position[1],
                end_column=context.cursor_position[1],
                description="Replace print statements with proper logging",
                priority=7,
                auto_apply=False
            ))
        
        # Check for missing type hints
        if "def " in context.content and ":" not in context.content:
            suggestions.append(CodeSuggestion(
                suggestion_id=str(uuid.uuid4()),
                suggestion_type=SuggestionType.OPTIMIZATION,
                text="Add type hints to function parameters and return type",
                language=Language.PYTHON,
                confidence=0.9,
                start_line=context.cursor_position[0],
                end_line=context.cursor_position[0],
                start_column=context.cursor_position[1],
                end_column=context.cursor_position[1],
                description="Add type hints for better code documentation and IDE support",
                priority=8,
                auto_apply=False
            ))
        
        return suggestions
    
    async def _analyze_javascript_code(self, context: CodeContext) -> List[CodeSuggestion]:
        """Analyze JavaScript code for suggestions"""
        suggestions = []
        
        # Check for var usage
        if "var " in context.content:
            suggestions.append(CodeSuggestion(
                suggestion_id=str(uuid.uuid4()),
                suggestion_type=SuggestionType.OPTIMIZATION,
                text="Consider using 'const' or 'let' instead of 'var'",
                language=Language.JAVASCRIPT,
                confidence=0.9,
                start_line=context.cursor_position[0],
                end_line=context.cursor_position[0],
                start_column=context.cursor_position[1],
                end_column=context.cursor_position[1],
                description="Use const/let for better block scoping",
                priority=8,
                auto_apply=False
            ))
        
        return suggestions
    
    async def _analyze_typescript_code(self, context: CodeContext) -> List[CodeSuggestion]:
        """Analyze TypeScript code for suggestions"""
        suggestions = []
        
        # Check for missing types
        if "function " in context.content and ":" not in context.content:
            suggestions.append(CodeSuggestion(
                suggestion_id=str(uuid.uuid4()),
                suggestion_type=SuggestionType.OPTIMIZATION,
                text="Add TypeScript type annotations",
                language=Language.TYPESCRIPT,
                confidence=0.9,
                start_line=context.cursor_position[0],
                end_line=context.cursor_position[0],
                start_column=context.cursor_position[1],
                end_column=context.cursor_position[1],
                description="Add type annotations for better type safety",
                priority=9,
                auto_apply=False
            ))
        
        return suggestions
    
    async def _analyze_generic_code(self, context: CodeContext) -> List[CodeSuggestion]:
        """Analyze generic code for suggestions"""
        suggestions = []
        
        # Generic suggestions
        if len(context.content.split('\n')) > 50:
            suggestions.append(CodeSuggestion(
                suggestion_id=str(uuid.uuid4()),
                suggestion_type=SuggestionType.REFACTOR,
                text="Consider breaking this into smaller functions",
                language=context.language,
                confidence=0.7,
                start_line=context.cursor_position[0],
                end_line=context.cursor_position[0],
                start_column=context.cursor_position[1],
                end_column=context.cursor_position[1],
                description="Large functions should be broken into smaller, more manageable pieces",
                priority=6,
                auto_apply=False
            ))
        
        return suggestions
    
    async def generate_code_snippet(
        self, 
        description: str, 
        language: Language,
        context: Optional[CodeContext] = None
    ) -> str:
        """Generate code snippet based on description"""
        try:
            # This would integrate with AI models for code generation
            # For now, we'll use template-based generation
            
            if language == Language.PYTHON:
                if "function" in description.lower():
                    return "def example_function():\n    \"\"\"Example function\"\"\"\n    pass"
                elif "class" in description.lower():
                    return "class ExampleClass:\n    \"\"\"Example class\"\"\"\n    \n    def __init__(self):\n        pass"
                else:
                    return "# Generated code snippet\npass"
            
            elif language == Language.JAVASCRIPT:
                if "function" in description.lower():
                    return "function exampleFunction() {\n    // Example function\n    return null;\n}"
                elif "class" in description.lower():
                    return "class ExampleClass {\n    constructor() {\n        // Constructor\n    }\n}"
                else:
                    return "// Generated code snippet\nnull;"
            
            elif language == Language.TYPESCRIPT:
                if "function" in description.lower():
                    return "function exampleFunction(): void {\n    // Example function\n    return;\n}"
                elif "class" in description.lower():
                    return "class ExampleClass {\n    constructor() {\n        // Constructor\n    }\n}"
                else:
                    return "// Generated code snippet\nnull;"
            
            else:
                return f"// Generated {language.value} code snippet\n// {description}"
                
        except Exception as e:
            logger.error("Failed to generate code snippet", error=str(e))
            return f"// Error generating code snippet: {e}"
    
    async def get_documentation(
        self, 
        symbol: str, 
        language: Language
    ) -> Optional[str]:
        """Get documentation for a symbol"""
        try:
            # This would integrate with language servers or documentation APIs
            # For now, we'll provide basic documentation
            
            if language == Language.PYTHON:
                python_docs = {
                    "print": "Print values to stdout",
                    "len": "Return the length of an object",
                    "str": "Convert object to string",
                    "int": "Convert to integer",
                    "float": "Convert to float",
                    "list": "Create a list",
                    "dict": "Create a dictionary",
                }
                return python_docs.get(symbol, f"Documentation for {symbol}")
            
            elif language == Language.JAVASCRIPT:
                js_docs = {
                    "console.log": "Print to console",
                    "JSON.stringify": "Convert object to JSON string",
                    "JSON.parse": "Parse JSON string to object",
                    "setTimeout": "Execute function after delay",
                    "setInterval": "Execute function repeatedly",
                }
                return js_docs.get(symbol, f"Documentation for {symbol}")
            
            else:
                return f"Documentation for {symbol} in {language.value}"
                
        except Exception as e:
            logger.error("Failed to get documentation", error=str(e))
            return None
    
    async def clear_cache(self):
        """Clear completion and suggestion caches"""
        self.completion_cache.clear()
        self.suggestion_cache.clear()
        logger.info("Smart Coding AI cache cleared")


# Global service instance
smart_coding_ai = SmartCodingAI()
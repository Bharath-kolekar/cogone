"""
Smart Coding AI API endpoints
Provides in-editor code completion, suggestions, and intelligent assistance
"""

import structlog
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from typing import Dict, List, Optional, Any
from datetime import datetime
from app.services.smart_coding_ai_service import (
    smart_coding_ai, CodeContext, Language, CompletionType, SuggestionType
)
from app.models.smart_coding_ai import (
    CodeCompletionRequest, CodeCompletionResponse,
    CodeSuggestionRequest, CodeSuggestionResponse,
    CodeSnippetRequest, CodeSnippetResponse,
    DocumentationRequest, DocumentationResponse,
    SmartCodingAIStatus
)

logger = structlog.get_logger()
router = APIRouter()


@router.post("/completions", response_model=CodeCompletionResponse)
async def get_code_completions(request: CodeCompletionRequest):
    """Get code completions for the given context"""
    try:
        # Create code context
        context = CodeContext(
            file_path=request.file_path,
            language=request.language,
            content=request.content,
            cursor_position=(request.cursor_line, request.cursor_column),
            selection=request.selection,
            imports=request.imports or [],
            functions=request.functions or [],
            classes=request.classes or [],
            variables=request.variables or []
        )
        
        # Get completions
        completions = await smart_coding_ai.get_code_completions(
            context, 
            max_completions=request.max_completions or 10
        )
        
        return CodeCompletionResponse(
            completions=completions,
            total_count=len(completions),
            language=request.language,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to get code completions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get code completions: {e}"
        )


@router.post("/suggestions", response_model=CodeSuggestionResponse)
async def get_code_suggestions(request: CodeSuggestionRequest):
    """Get code suggestions for improvements and fixes"""
    try:
        # Create code context
        context = CodeContext(
            file_path=request.file_path,
            language=request.language,
            content=request.content,
            cursor_position=(request.cursor_line, request.cursor_column),
            selection=request.selection,
            imports=request.imports or [],
            functions=request.functions or [],
            classes=request.classes or [],
            variables=request.variables or []
        )
        
        # Get suggestions
        suggestions = await smart_coding_ai.get_code_suggestions(
            context,
            max_suggestions=request.max_suggestions or 5
        )
        
        return CodeSuggestionResponse(
            suggestions=suggestions,
            total_count=len(suggestions),
            language=request.language,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to get code suggestions", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get code suggestions: {e}"
        )


@router.post("/snippet", response_model=CodeSnippetResponse)
async def generate_code_snippet(request: CodeSnippetRequest):
    """Generate code snippet based on description"""
    try:
        # Generate snippet
        snippet = await smart_coding_ai.generate_code_snippet(
            description=request.description,
            language=request.language,
            context=request.context
        )
        
        return CodeSnippetResponse(
            snippet=snippet,
            language=request.language,
            description=request.description,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to generate code snippet", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate code snippet: {e}"
        )


@router.post("/documentation", response_model=DocumentationResponse)
async def get_documentation(request: DocumentationRequest):
    """Get documentation for a symbol"""
    try:
        # Get documentation
        documentation = await smart_coding_ai.get_documentation(
            symbol=request.symbol,
            language=request.language
        )
        
        return DocumentationResponse(
            symbol=request.symbol,
            language=request.language,
            documentation=documentation,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to get documentation", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get documentation: {e}"
        )


@router.get("/languages")
async def get_supported_languages():
    """Get list of supported programming languages"""
    try:
        languages = [
            {"name": "Python", "value": "python", "extensions": [".py", ".pyw"]},
            {"name": "JavaScript", "value": "javascript", "extensions": [".js", ".mjs"]},
            {"name": "TypeScript", "value": "typescript", "extensions": [".ts", ".tsx"]},
            {"name": "Java", "value": "java", "extensions": [".java"]},
            {"name": "C#", "value": "csharp", "extensions": [".cs"]},
            {"name": "C++", "value": "cpp", "extensions": [".cpp", ".cc", ".cxx"]},
            {"name": "Go", "value": "go", "extensions": [".go"]},
            {"name": "Rust", "value": "rust", "extensions": [".rs"]},
            {"name": "PHP", "value": "php", "extensions": [".php"]},
            {"name": "Ruby", "value": "ruby", "extensions": [".rb"]},
            {"name": "Swift", "value": "swift", "extensions": [".swift"]},
            {"name": "Kotlin", "value": "kotlin", "extensions": [".kt", ".kts"]},
            {"name": "HTML", "value": "html", "extensions": [".html", ".htm"]},
            {"name": "CSS", "value": "css", "extensions": [".css"]},
            {"name": "SQL", "value": "sql", "extensions": [".sql"]},
            {"name": "YAML", "value": "yaml", "extensions": [".yml", ".yaml"]},
            {"name": "JSON", "value": "json", "extensions": [".json"]},
            {"name": "Markdown", "value": "markdown", "extensions": [".md", ".markdown"]},
        ]
        
        return {
            "languages": languages,
            "total_count": len(languages),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error("Failed to get supported languages", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get supported languages: {e}"
        )


@router.get("/completion-types")
async def get_completion_types():
    """Get list of completion types"""
    try:
        completion_types = [
            {"name": "Function", "value": "function", "description": "Function definitions and calls"},
            {"name": "Variable", "value": "variable", "description": "Variable declarations and references"},
            {"name": "Class", "value": "class", "description": "Class definitions and instantiations"},
            {"name": "Import", "value": "import", "description": "Import statements and modules"},
            {"name": "Parameter", "value": "parameter", "description": "Function parameters and arguments"},
            {"name": "Method", "value": "method", "description": "Method definitions and calls"},
            {"name": "Property", "value": "property", "description": "Property definitions and access"},
            {"name": "Type", "value": "type", "description": "Type definitions and annotations"},
            {"name": "Keyword", "value": "keyword", "description": "Language keywords and reserved words"},
            {"name": "Snippet", "value": "snippet", "description": "Code snippets and templates"},
        ]
        
        return {
            "completion_types": completion_types,
            "total_count": len(completion_types),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error("Failed to get completion types", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get completion types: {e}"
        )


@router.get("/suggestion-types")
async def get_suggestion_types():
    """Get list of suggestion types"""
    try:
        suggestion_types = [
            {"name": "Completion", "value": "completion", "description": "Code completion suggestions"},
            {"name": "Hint", "value": "hint", "description": "Helpful hints and tips"},
            {"name": "Error Fix", "value": "error_fix", "description": "Error fixes and corrections"},
            {"name": "Refactor", "value": "refactor", "description": "Code refactoring suggestions"},
            {"name": "Optimization", "value": "optimization", "description": "Performance optimization suggestions"},
            {"name": "Documentation", "value": "documentation", "description": "Documentation improvements"},
        ]
        
        return {
            "suggestion_types": suggestion_types,
            "total_count": len(suggestion_types),
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error("Failed to get suggestion types", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get suggestion types: {e}"
        )


@router.get("/status", response_model=SmartCodingAIStatus)
async def get_smart_coding_ai_status():
    """Get Smart Coding AI service status"""
    try:
        return SmartCodingAIStatus(
            service_active=True,
            models_loaded=True,
            supported_languages=18,
            completion_cache_size=len(smart_coding_ai.completion_cache),
            suggestion_cache_size=len(smart_coding_ai.suggestion_cache),
            last_updated=datetime.now()
        )
        
    except Exception as e:
        logger.error("Failed to get Smart Coding AI status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get Smart Coding AI status: {e}"
        )


@router.post("/cache/clear")
async def clear_cache():
    """Clear Smart Coding AI cache"""
    try:
        await smart_coding_ai.clear_cache()
        
        return {
            "cache_cleared": True,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error("Failed to clear cache", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cache: {e}"
        )


@router.get("/health")
async def health_check():
    """Smart Coding AI health check"""
    try:
        # Test basic functionality
        test_context = CodeContext(
            file_path="test.py",
            language=Language.PYTHON,
            content="def test():",
            cursor_position=(1, 10)
        )
        
        # Get test completions
        completions = await smart_coding_ai.get_code_completions(test_context, max_completions=1)
        
        return {
            "status": "healthy",
            "service": "Smart Coding AI",
            "completions_working": len(completions) > 0,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error("Smart Coding AI health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "service": "Smart Coding AI",
            "error": str(e),
            "timestamp": datetime.now()
        }


@router.get("/stats")
async def get_usage_stats():
    """Get Smart Coding AI usage statistics"""
    try:
        return {
            "completion_cache_size": len(smart_coding_ai.completion_cache),
            "suggestion_cache_size": len(smart_coding_ai.suggestion_cache),
            "supported_languages": 18,
            "completion_types": 10,
            "suggestion_types": 6,
            "service_uptime": "Active",
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error("Failed to get usage stats", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get usage stats: {e}"
        )

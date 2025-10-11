"""
Reality Check DNA Router

API endpoints for the Reality Check DNA system that detects "delusional AI" patterns.
"""

from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import structlog

from ..services.reality_check_dna import (
    reality_check_dna,
    RealityCheckResult,
    HallucinationDetection,
    HallucinationSeverity,
    HallucinationPattern
)

logger = structlog.get_logger()

router = APIRouter(prefix="/reality-check-dna", tags=["Reality Check DNA"])


class CodeCheckRequest(BaseModel):
    """Request to check code for hallucination patterns"""
    code: str
    file_path: Optional[str] = "api_request.py"
    check_imports: bool = True
    check_external_calls: bool = True


class FileCheckRequest(BaseModel):
    """Request to check a file"""
    file_path: str


class DirectoryCheckRequest(BaseModel):
    """Request to check a directory"""
    directory: str
    extensions: List[str] = ['.py']
    recursive: bool = True


class HallucinationResponse(BaseModel):
    """Response model for hallucination detection"""
    pattern: str
    severity: str
    file_path: str
    line_number: int
    function_name: str
    code_snippet: str
    explanation: str
    suggestion: str
    confidence: float


class RealityCheckResponse(BaseModel):
    """Response model for reality check"""
    is_real: bool
    hallucinations: List[HallucinationResponse]
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    reality_score: float
    summary: str


@router.post("/check-code", response_model=RealityCheckResponse)
async def check_code(request: CodeCheckRequest):
    """
    Check code for hallucination patterns
    
    Detects:
    - Fake data returns
    - Hardcoded values
    - Stubs without warnings
    - Comments instead of code
    - Perfect structure but no implementation
    - Mock implementations without real API calls
    """
    try:
        result = await reality_check_dna.check_code_reality(
            code=request.code,
            file_path=request.file_path,
            check_imports=request.check_imports,
            check_external_calls=request.check_external_calls
        )
        
        return _convert_result(result)
    
    except Exception as e:
        logger.error("Error checking code reality", error=str(e))
        raise HTTPException(status_code=500, detail=f"Reality check failed: {str(e)}")


@router.post("/check-file", response_model=RealityCheckResponse)
async def check_file(request: FileCheckRequest):
    """
    Check a specific file for hallucination patterns
    """
    try:
        result = await reality_check_dna.check_file(request.file_path)
        return _convert_result(result)
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {request.file_path}")
    except Exception as e:
        logger.error("Error checking file", file_path=request.file_path, error=str(e))
        raise HTTPException(status_code=500, detail=f"Reality check failed: {str(e)}")


@router.post("/check-directory")
async def check_directory(request: DirectoryCheckRequest):
    """
    Check all files in a directory for hallucination patterns
    
    Returns summary statistics and details for suspicious files
    """
    try:
        results = await reality_check_dna.check_directory(
            directory=request.directory,
            extensions=request.extensions,
            recursive=request.recursive
        )
        
        # Convert results
        converted_results = {
            file_path: _convert_result(result)
            for file_path, result in results.items()
        }
        
        # Generate statistics
        total_files = len(results)
        real_files = sum(1 for r in results.values() if r.is_real)
        fake_files = total_files - real_files
        total_issues = sum(r.total_issues for r in results.values())
        avg_score = sum(r.reality_score for r in results.values()) / total_files if total_files > 0 else 0
        
        # Find worst offenders
        suspicious_files = [
            (path, result) for path, result in results.items()
            if not result.is_real or result.critical_count > 0
        ]
        suspicious_files.sort(key=lambda x: (x[1].critical_count, x[1].high_count), reverse=True)
        
        return {
            "summary": {
                "total_files": total_files,
                "real_files": real_files,
                "fake_suspicious_files": fake_files,
                "total_issues": total_issues,
                "average_reality_score": round(avg_score, 2)
            },
            "suspicious_files": [
                {
                    "file_path": path,
                    "reality_score": result.reality_score,
                    "issues": result.total_issues,
                    "critical": result.critical_count,
                    "high": result.high_count
                }
                for path, result in suspicious_files[:10]  # Top 10 worst
            ],
            "detailed_results": converted_results
        }
    
    except Exception as e:
        logger.error("Error checking directory", directory=request.directory, error=str(e))
        raise HTTPException(status_code=500, detail=f"Directory check failed: {str(e)}")


@router.get("/health")
async def health_check():
    """Health check for Reality Check DNA system"""
    return {
        "status": "healthy",
        "system": "Reality Check DNA",
        "description": "Anti-hallucination system for detecting fake AI-generated code",
        "capabilities": [
            "Fake data detection",
            "Hardcoded value detection",
            "Stub pattern recognition",
            "Comment-only implementations",
            "Missing external API calls",
            "Perfect structure without implementation"
        ]
    }


@router.get("/patterns")
async def list_patterns():
    """List all detectable hallucination patterns"""
    return {
        "patterns": [
            {
                "name": pattern.value,
                "description": _get_pattern_description(pattern)
            }
            for pattern in HallucinationPattern
        ],
        "severities": [
            {
                "level": severity.value,
                "description": _get_severity_description(severity)
            }
            for severity in HallucinationSeverity
        ]
    }


def _convert_result(result: RealityCheckResult) -> RealityCheckResponse:
    """Convert internal result to API response"""
    return RealityCheckResponse(
        is_real=result.is_real,
        hallucinations=[
            HallucinationResponse(
                pattern=h.pattern.value,
                severity=h.severity.value,
                file_path=h.file_path,
                line_number=h.line_number,
                function_name=h.function_name,
                code_snippet=h.code_snippet,
                explanation=h.explanation,
                suggestion=h.suggestion,
                confidence=h.confidence
            )
            for h in result.hallucinations
        ],
        total_issues=result.total_issues,
        critical_count=result.critical_count,
        high_count=result.high_count,
        medium_count=result.medium_count,
        low_count=result.low_count,
        reality_score=result.reality_score,
        summary=result.summary
    )


def _get_pattern_description(pattern: HallucinationPattern) -> str:
    """Get human-readable description for pattern"""
    descriptions = {
        HallucinationPattern.FAKE_DATA_RETURN: "Functions return fake/hardcoded data instead of real values",
        HallucinationPattern.HARDCODED_VALUES: "Credentials or config hardcoded instead of from environment",
        HallucinationPattern.STUB_WITHOUT_WARNING: "Stub implementation without proper warnings",
        HallucinationPattern.COMMENT_INSTEAD_OF_CODE: "Comments describe what should happen but no implementation",
        HallucinationPattern.TODO_IN_PRODUCTION: "TODO comments indicating incomplete implementation",
        HallucinationPattern.MOCK_WITHOUT_REAL_API: "Code mentions APIs but makes no actual calls",
        HallucinationPattern.ALWAYS_RETURNS_TRUE: "Function always returns True without validation",
        HallucinationPattern.RETURNS_EMPTY_DICT: "Function returns empty dict/list as placeholder",
        HallucinationPattern.NO_ERROR_HANDLING: "No error handling for operations that can fail",
        HallucinationPattern.FAKE_HASH_AS_ID: "Uses hash() to generate fake IDs instead of database",
        HallucinationPattern.LITERAL_PLACEHOLDER: "Contains literal placeholder text (dev-, test-, your-)",
        HallucinationPattern.PERFECT_STRUCTURE_NO_IMPL: "Perfect types/docs but trivial implementation"
    }
    return descriptions.get(pattern, "Unknown pattern")


def _get_severity_description(severity: HallucinationSeverity) -> str:
    """Get human-readable description for severity"""
    descriptions = {
        HallucinationSeverity.CRITICAL: "Definitely fake/broken - will not work in production",
        HallucinationSeverity.HIGH: "Very likely fake - needs immediate attention",
        HallucinationSeverity.MEDIUM: "Suspicious patterns - should investigate",
        HallucinationSeverity.LOW: "Minor concerns - low priority",
        HallucinationSeverity.INFO: "Informational only - no action needed"
    }
    return descriptions.get(severity, "Unknown severity")


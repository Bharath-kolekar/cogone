"""
Code Intelligence API Router
Implements REST endpoints for Code Intelligence capabilities (3, 4, 7-10)
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import structlog

from ..services.capability_factory import get_capability_factory

logger = structlog.get_logger()
router = APIRouter(prefix="/code-intelligence", tags=["Code Intelligence"])

# Get capabilities from factory
factory = get_capability_factory()
capabilities = factory.get_all_capabilities()


# ============================================================================
# Request/Response Models
# ============================================================================

class AlgorithmImplementationRequest(BaseModel):
    """Request to implement an algorithm"""
    algorithm_name: str = Field(..., description="Name of algorithm to implement")
    constraints: Optional[Dict[str, Any]] = Field(default=None, description="Performance constraints")
    language: str = Field(default="python", description="Programming language")


class APIIntegrationRequest(BaseModel):
    """Request to generate API integration code"""
    api_spec: Dict[str, Any] = Field(..., description="API specification (OpenAPI/Swagger)")
    framework: str = Field(default="requests", description="HTTP client framework")


class DataStructureRequest(BaseModel):
    """Request to select optimal data structure"""
    use_case: str = Field(..., description="Description of use case")
    operations: List[str] = Field(..., description="Required operations")
    constraints: Optional[Dict[str, Any]] = Field(default=None, description="Constraints")


class ErrorHandlingRequest(BaseModel):
    """Request to generate error handling code"""
    code: str = Field(..., description="Code to add error handling to")
    error_types: Optional[List[str]] = Field(default=None, description="Expected error types")


class LoggingRequest(BaseModel):
    """Request to implement logging"""
    code: str = Field(..., description="Code to add logging to")
    log_level: str = Field(default="info", description="Default log level")
    framework: str = Field(default="structlog", description="Logging framework")


# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/implement-algorithm")
async def implement_algorithm(request: AlgorithmImplementationRequest):
    """
    Capability #3: Algorithm Implementation
    Implements specified algorithms with optimal performance
    """
    try:
        result = await capabilities['algorithm_implementer'].implement_algorithm(
            algorithm_name=request.algorithm_name,
            constraints=request.constraints,
            language=request.language
        )
        return result
    except Exception as e:
        logger.error("Algorithm implementation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-api-integration")
async def generate_api_integration(request: APIIntegrationRequest):
    """
    Capability #4: API Integration Code Generation
    Generates code to integrate with third-party APIs
    """
    try:
        result = await capabilities['api_integration_code_generator'].generate_api_integration(
            api_spec=request.api_spec,
            framework=request.framework
        )
        return result
    except Exception as e:
        logger.error("API integration generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/select-data-structure")
async def select_data_structure(request: DataStructureRequest):
    """
    Capability #7: Data Structure Selection
    Recommends optimal data structures for use cases
    """
    try:
        result = await capabilities['data_structure_selector'].select_data_structure(
            use_case=request.use_case,
            operations=request.operations,
            constraints=request.constraints
        )
        return result
    except Exception as e:
        logger.error("Data structure selection failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-error-handling")
async def generate_error_handling(request: ErrorHandlingRequest):
    """
    Capability #8: Error Handling Generation
    Generates comprehensive error handling code
    """
    try:
        result = await capabilities['error_handling_generator'].generate_error_handling(
            code=request.code,
            error_types=request.error_types
        )
        return result
    except Exception as e:
        logger.error("Error handling generation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/implement-logging")
async def implement_logging(request: LoggingRequest):
    """
    Capability #9: Logging Implementation
    Implements structured logging throughout code
    """
    try:
        result = await capabilities['logging_implementer'].implement_logging(
            code=request.code,
            log_level=request.log_level,
            framework=request.framework
        )
        return result
    except Exception as e:
        logger.error("Logging implementation failed", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities")
async def list_code_intelligence_capabilities():
    """List all Code Intelligence capabilities and their status"""
    return {
        "category": "Code Intelligence",
        "capabilities": [
            {"id": 3, "name": "Algorithm Implementation", "status": "implemented"},
            {"id": 4, "name": "API Integration Code", "status": "implemented"},
            {"id": 7, "name": "Data Structure Selection", "status": "implemented"},
            {"id": 8, "name": "Error Handling Generation", "status": "implemented"},
            {"id": 9, "name": "Logging Implementation", "status": "implemented"},
        ],
        "total": 5,
        "implemented": 5,
        "completion_percentage": 100
    }


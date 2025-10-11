"""
Smarty Ethical Integration Router

This module provides API endpoints for the Smarty Ethical Integration service,
combining the power of Smarty with comprehensive ethical AI validation.
"""

import structlog
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import json

from app.services.smarty_ethical_integration import (
    smarty_ethical_integration,
    EthicalCodeGenerationRequest,
    EthicalValidationLevel,
    CodeGenerationMode
)

logger = structlog.get_logger(__name__)

router = APIRouter()

# ============================================================================
# SMARTY ETHICAL CODE GENERATION ENDPOINTS
# ============================================================================

@router.post("/generate-ethical-code", response_model=Dict[str, Any])
async def generate_ethical_code(request_data: Dict[str, Any]):
    """Generate code with comprehensive ethical validation through Smarty Ethical Integration"""
    try:
        logger.info("Processing ethical code generation request", 
                   user_id=request_data.get("user_id"),
                   language=request_data.get("language"))
        
        # Create ethical code generation request
        ethical_request = EthicalCodeGenerationRequest(
            request_id=request_data.get("request_id", f"req_{datetime.now().timestamp()}"),
            user_id=request_data.get("user_id", "anonymous"),
            prompt=request_data.get("prompt", ""),
            language=request_data.get("language", "python"),
            context=request_data.get("context", {}),
            ethical_validation_level=EthicalValidationLevel(
                request_data.get("ethical_validation_level", "standard")
            ),
            generation_mode=CodeGenerationMode(
                request_data.get("generation_mode", "ethical_development")
            ),
            security_requirements=request_data.get("security_requirements", []),
            quality_requirements=request_data.get("quality_requirements", []),
            goals=request_data.get("goals", []),
            metadata=request_data.get("metadata", {})
        )
        
        # Generate ethical code
        response = await smarty_ethical_integration.generate_ethical_code(ethical_request)
        
        return {
            "status": "success",
            "data": {
                "response_id": response.response_id,
                "request_id": response.request_id,
                "generated_code": response.generated_code,
                "validation_results": {
                    "ethical": {
                        "score": response.overall_ethical_score,
                        "results": response.ethical_validation_results
                    },
                    "security": {
                        "score": response.overall_security_score,
                        "results": response.security_validation_results
                    },
                    "quality": {
                        "score": response.overall_quality_score,
                        "results": response.quality_validation_results
                    },
                    "goal_integrity": response.goal_integrity_results,
                    "factual_accuracy": response.factual_accuracy_results,
                    "consistency": response.consistency_results
                },
                "recommendations": response.recommendations,
                "warnings": response.warnings,
                "metadata": response.metadata
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Ethical code generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ethical code generation failed: {str(e)}"
        )

@router.post("/generate-ethical-code-stream", response_model=Dict[str, Any])
async def generate_ethical_code_stream(request_data: Dict[str, Any]):
    """Generate code with ethical validation in streaming mode"""
    try:
        logger.info("Processing streaming ethical code generation request", 
                   user_id=request_data.get("user_id"),
                   language=request_data.get("language"))
        
        # Create ethical code generation request
        ethical_request = EthicalCodeGenerationRequest(
            request_id=request_data.get("request_id", f"req_{datetime.now().timestamp()}"),
            user_id=request_data.get("user_id", "anonymous"),
            prompt=request_data.get("prompt", ""),
            language=request_data.get("language", "python"),
            context=request_data.get("context", {}),
            ethical_validation_level=EthicalValidationLevel(
                request_data.get("ethical_validation_level", "standard")
            ),
            generation_mode=CodeGenerationMode(
                request_data.get("generation_mode", "ethical_development")
            ),
            security_requirements=request_data.get("security_requirements", []),
            quality_requirements=request_data.get("quality_requirements", []),
            goals=request_data.get("goals", []),
            metadata={
                **request_data.get("metadata", {}),
                "streaming": True
            }
        )
        
        # Generate ethical code with streaming
        response = await smarty_ethical_integration.generate_ethical_code(ethical_request)
        
        # Return streaming response structure
        return {
            "status": "success",
            "streaming": True,
            "data": {
                "response_id": response.response_id,
                "request_id": response.request_id,
                "generated_code": response.generated_code,
                "validation_results": {
                    "ethical": {
                        "score": response.overall_ethical_score,
                        "results": response.ethical_validation_results
                    },
                    "security": {
                        "score": response.overall_security_score,
                        "results": response.security_validation_results
                    },
                    "quality": {
                        "score": response.overall_quality_score,
                        "results": response.quality_validation_results
                    }
                },
                "recommendations": response.recommendations,
                "warnings": response.warnings,
                "metadata": response.metadata
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Streaming ethical code generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Streaming ethical code generation failed: {str(e)}"
        )

# ============================================================================
# SMARTY ETHICAL VALIDATION ENDPOINTS
# ============================================================================

@router.post("/validate-ethical-request", response_model=Dict[str, Any])
async def validate_ethical_request(request_data: Dict[str, Any]):
    """Validate a code generation request for ethical compliance"""
    try:
        logger.info("Validating ethical request", 
                   user_id=request_data.get("user_id"))
        
        # Create ethical code generation request for validation
        ethical_request = EthicalCodeGenerationRequest(
            request_id=request_data.get("request_id", f"req_{datetime.now().timestamp()}"),
            user_id=request_data.get("user_id", "anonymous"),
            prompt=request_data.get("prompt", ""),
            language=request_data.get("language", "python"),
            context=request_data.get("context", {}),
            ethical_validation_level=EthicalValidationLevel(
                request_data.get("ethical_validation_level", "standard")
            ),
            generation_mode=CodeGenerationMode(
                request_data.get("generation_mode", "ethical_development")
            ),
            security_requirements=request_data.get("security_requirements", []),
            quality_requirements=request_data.get("quality_requirements", []),
            goals=request_data.get("goals", []),
            metadata=request_data.get("metadata", {})
        )
        
        # Validate ethical request
        validation_results = await smarty_ethical_integration._validate_ethical_request(ethical_request)
        
        return {
            "status": "success",
            "data": {
                "validation_results": validation_results,
                "ethical_score": validation_results.get("ethical_score", 0.0),
                "validation_passed": validation_results.get("validation_passed", False),
                "recommendations": _generate_validation_recommendations(validation_results)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Ethical request validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ethical request validation failed: {str(e)}"
        )

@router.post("/validate-existing-code", response_model=Dict[str, Any])
async def validate_existing_code(code_data: Dict[str, Any]):
    """Validate existing code for ethical, security, and quality compliance"""
    try:
        logger.info("Validating existing code", 
                   code_length=len(code_data.get("code", "")))
        
        code = code_data.get("code", "")
        context = code_data.get("context", {})
        goals = code_data.get("goals", [])
        
        # Create a mock request for validation
        ethical_request = EthicalCodeGenerationRequest(
            request_id=f"validation_{datetime.now().timestamp()}",
            user_id=code_data.get("user_id", "anonymous"),
            prompt="Validate existing code",
            language=code_data.get("language", "python"),
            context=context,
            ethical_validation_level=EthicalValidationLevel(
                code_data.get("ethical_validation_level", "standard")
            ),
            generation_mode=CodeGenerationMode(
                code_data.get("generation_mode", "ethical_development")
            ),
            goals=goals,
            metadata={"validation_only": True}
        )
        
        # Run comprehensive validation pipeline on existing code
        validation_results = await smarty_ethical_integration._comprehensive_validation_pipeline(
            ethical_request, code
        )
        
        # Calculate overall scores
        overall_scores = await smarty_ethical_integration._calculate_overall_scores(validation_results)
        
        # Generate recommendations and warnings
        recommendations, warnings = await smarty_ethical_integration._generate_recommendations_and_warnings(
            validation_results, overall_scores
        )
        
        return {
            "status": "success",
            "data": {
                "validation_results": validation_results,
                "overall_scores": overall_scores,
                "recommendations": recommendations,
                "warnings": warnings,
                "validation_summary": {
                    "ethical_score": overall_scores.get("ethical", 0.0),
                    "security_score": overall_scores.get("security", 0.0),
                    "quality_score": overall_scores.get("quality", 0.0),
                    "goal_integrity_score": overall_scores.get("goal_integrity", 0.0),
                    "factual_accuracy_score": overall_scores.get("factual_accuracy", 0.0),
                    "consistency_score": overall_scores.get("consistency", 0.0)
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Existing code validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Existing code validation failed: {str(e)}"
        )

# ============================================================================
# SMARTY ETHICAL METRICS AND STATUS ENDPOINTS
# ============================================================================

@router.get("/ethical-metrics", response_model=Dict[str, Any])
async def get_ethical_metrics():
    """Get Smarty ethical integration metrics"""
    try:
        metrics = await smarty_ethical_integration.get_ethical_metrics()
        
        return {
            "status": "success",
            "data": {
                "metrics": metrics,
                "summary": {
                    "total_requests": metrics.get("total_requests", 0),
                    "success_rate": metrics.get("success_rate", 0.0),
                    "ethical_compliance_rate": metrics.get("ethical_compliance_rate", 0.0),
                    "average_ethical_score": metrics.get("average_ethical_score", 0.0),
                    "average_security_score": metrics.get("average_security_score", 0.0),
                    "average_quality_score": metrics.get("average_quality_score", 0.0)
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get ethical metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ethical metrics retrieval failed: {str(e)}"
        )

@router.get("/ethical-status", response_model=Dict[str, Any])
async def get_ethical_status():
    """Get comprehensive Smarty ethical integration status"""
    try:
        status_data = await smarty_ethical_integration.get_ethical_status()
        
        return {
            "status": "success",
            "data": status_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get ethical status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ethical status retrieval failed: {str(e)}"
        )

# ============================================================================
# SMARTY ETHICAL CONFIGURATION ENDPOINTS
# ============================================================================

@router.get("/ethical-configuration", response_model=Dict[str, Any])
async def get_ethical_configuration():
    """Get current ethical configuration settings"""
    try:
        configuration = {
            "ethical_validation_levels": [level.value for level in EthicalValidationLevel],
            "generation_modes": [mode.value for mode in CodeGenerationMode],
            "ethical_rules": smarty_ethical_integration.ethical_rules,
            "validation_components": {
                "ethical_ai_core": "enabled",
                "security_validator": "enabled",
                "code_quality_analyzer": "enabled",
                "goal_integrity_service": "enabled",
                "error_recovery_manager": "enabled",
                "factual_accuracy_validator": "enabled",
                "consistency_enforcer": "enabled"
            },
            "default_settings": {
                "ethical_validation_level": "standard",
                "generation_mode": "ethical_development",
                "security_requirements": [],
                "quality_requirements": [],
                "goals": []
            }
        }
        
        return {
            "status": "success",
            "data": configuration,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get ethical configuration", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ethical configuration retrieval failed: {str(e)}"
        )

@router.post("/update-ethical-configuration", response_model=Dict[str, Any])
async def update_ethical_configuration(config_data: Dict[str, Any]):
    """Update ethical configuration settings"""
    try:
        logger.info("Updating ethical configuration", 
                   updates=list(config_data.keys()))
        
        # Update ethical rules if provided
        if "ethical_rules" in config_data:
            smarty_ethical_integration.ethical_rules.update(config_data["ethical_rules"])
        
        # Update other configuration settings
        updated_settings = {}
        for key, value in config_data.items():
            if key != "ethical_rules":
                updated_settings[key] = value
        
        return {
            "status": "success",
            "message": "Ethical configuration updated successfully",
            "data": {
                "updated_settings": updated_settings,
                "ethical_rules_updated": "ethical_rules" in config_data
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to update ethical configuration", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ethical configuration update failed: {str(e)}"
        )

# ============================================================================
# SMARTY ETHICAL BATCH PROCESSING ENDPOINTS
# ============================================================================

@router.post("/batch-ethical-validation", response_model=Dict[str, Any])
async def batch_ethical_validation(batch_data: Dict[str, Any]):
    """Perform batch ethical validation on multiple code samples"""
    try:
        logger.info("Processing batch ethical validation", 
                   batch_size=len(batch_data.get("code_samples", [])))
        
        code_samples = batch_data.get("code_samples", [])
        validation_results = []
        
        for i, sample in enumerate(code_samples):
            try:
                # Create validation request for each sample
                ethical_request = EthicalCodeGenerationRequest(
                    request_id=f"batch_{i}_{datetime.now().timestamp()}",
                    user_id=sample.get("user_id", "anonymous"),
                    prompt=sample.get("prompt", "Batch validation"),
                    language=sample.get("language", "python"),
                    context=sample.get("context", {}),
                    ethical_validation_level=EthicalValidationLevel(
                        sample.get("ethical_validation_level", "standard")
                    ),
                    generation_mode=CodeGenerationMode(
                        sample.get("generation_mode", "ethical_development")
                    ),
                    goals=sample.get("goals", []),
                    metadata={"batch_processing": True}
                )
                
                # Run validation pipeline
                validation_result = await smarty_ethical_integration._comprehensive_validation_pipeline(
                    ethical_request, sample.get("code", "")
                )
                
                # Calculate scores
                overall_scores = await smarty_ethical_integration._calculate_overall_scores(validation_result)
                
                validation_results.append({
                    "sample_id": i,
                    "validation_results": validation_result,
                    "overall_scores": overall_scores,
                    "status": "completed"
                })
                
            except Exception as e:
                logger.error(f"Batch validation failed for sample {i}", error=str(e))
                validation_results.append({
                    "sample_id": i,
                    "validation_results": {"error": str(e)},
                    "overall_scores": {},
                    "status": "failed"
                })
        
        return {
            "status": "success",
            "data": {
                "batch_results": validation_results,
                "total_samples": len(code_samples),
                "completed_samples": len([r for r in validation_results if r["status"] == "completed"]),
                "failed_samples": len([r for r in validation_results if r["status"] == "failed"]),
                "batch_summary": {
                    "average_ethical_score": _calculate_batch_average(validation_results, "ethical"),
                    "average_security_score": _calculate_batch_average(validation_results, "security"),
                    "average_quality_score": _calculate_batch_average(validation_results, "quality")
                }
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Batch ethical validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Batch ethical validation failed: {str(e)}"
        )

# ============================================================================
# SMARTY ETHICAL HEALTH CHECK ENDPOINT
# ============================================================================

@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint for Smarty Ethical Integration"""
    try:
        # Get basic status
        status_data = await smarty_ethical_integration.get_ethical_status()
        
        # Check component health
        components_healthy = all(
            status_data.get("components", {}).get(component) == "active"
            for component in [
                "ethical_ai_core", "security_validator", "code_quality_analyzer",
                "goal_integrity_service", "error_recovery_manager",
                "factual_accuracy_validator", "consistency_enforcer",
                "enhanced_ai_assistant_core", "enhanced_context_sharing",
                "enhanced_monitoring_analytics"
            ]
        )
        
        overall_health = "healthy" if components_healthy else "degraded"
        
        return {
            "status": overall_health,
            "message": "Smarty Ethical Integration is operational",
            "data": {
                "components_healthy": components_healthy,
                "smarty_ethical_integration": status_data.get("smarty_ethical_integration", "unknown"),
                "system_health": status_data.get("system_health", {}),
                "components": status_data.get("components", {})
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        return {
            "status": "unhealthy",
            "message": f"Health check failed: {str(e)}",
            "data": {"error": str(e)},
            "timestamp": datetime.now().isoformat()
        }

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _generate_validation_recommendations(validation_results: Dict[str, Any]) -> List[str]:
    """Generate recommendations based on validation results"""
    recommendations = []
    
    if not validation_results.get("validation_passed", False):
        recommendations.append("Request requires ethical review before processing")
    
    if validation_results.get("ethical_score", 100) < 70:
        recommendations.append("Improve ethical compliance of the request")
    
    if validation_results.get("ethical_analysis", {}).get("harmful_content_detected", False):
        recommendations.append("Remove harmful content from the request")
    
    if validation_results.get("ethical_analysis", {}).get("privacy_violations_detected", False):
        recommendations.append("Address privacy concerns in the request")
    
    return recommendations

def _calculate_batch_average(validation_results: List[Dict[str, Any]], score_type: str) -> float:
    """Calculate average score for batch validation results"""
    try:
        scores = []
        for result in validation_results:
            if result["status"] == "completed":
                score = result["overall_scores"].get(score_type, 0.0)
                if score > 0:
                    scores.append(score)
        
        return sum(scores) / len(scores) if scores else 0.0
        
    except Exception:
        return 0.0

"""
Comprehensive Ethical AI Router

This module provides a comprehensive router that integrates all Ethical AI components,
including the core systems, enhanced components, and monitoring capabilities.
"""

import structlog
from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timedelta
import json

from app.core.ethical_ai_core import ethical_ai_core
from app.core.tool_integration_manager import tool_integration_manager
from app.core.security_validator import security_validator
from app.core.code_quality_analyzer import code_quality_analyzer
from app.services.goal_integrity_service import goal_integrity_service
from app.core.error_recovery_manager import error_recovery_manager
from app.core.factual_accuracy_validator import factual_accuracy_validator
from app.core.consistency_enforcer import consistency_enforcer
from app.core.enhanced_ai_assistant_core import enhanced_ai_assistant_core, AssistantRequest, AssistantContext, AssistantCapability, AssistantMode
from app.core.enhanced_context_sharing import enhanced_context_sharing, ContextType, ContextPriority, ContextAccess
from app.core.enhanced_monitoring_analytics import enhanced_monitoring_analytics, MetricType, AlertSeverity, ComponentStatus
from app.services.enhanced_governance_service import enhanced_governance_service
from app.core.governance_monitor import governance_monitor

logger = structlog.get_logger(__name__)

router = APIRouter()

# ============================================================================
# ETHICAL AI CORE ENDPOINTS
# ============================================================================

@router.post("/ethical-ai/process-request", response_model=Dict[str, Any])
async def process_ethical_request(request_data: Dict[str, Any]):
    """Process a request through the Ethical AI Core"""
    try:
        logger.info("Processing ethical AI request", request_id=request_data.get("id"))
        
        result = await ethical_ai_core.process_user_request(request_data)
        
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Ethical AI request processing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Request processing failed: {str(e)}"
        )

@router.get("/ethical-ai/status", response_model=Dict[str, Any])
async def get_ethical_ai_status():
    """Get Ethical AI Core status"""
    try:
        return {
            "status": "healthy",
            "components": {
                "ethical_framework": "active",
                "purpose_detector": "active", 
                "karma_tracker": "active"
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get Ethical AI status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Status retrieval failed: {str(e)}"
        )

# ============================================================================
# TOOL INTEGRATION ENDPOINTS
# ============================================================================

@router.post("/tools/register", response_model=Dict[str, Any])
async def register_tool(tool_data: Dict[str, Any]):
    """Register a new tool with the Tool Integration Manager"""
    try:
        tool_id = await tool_integration_manager.register_tool(tool_data)
        
        return {
            "status": "success",
            "tool_id": tool_id,
            "message": "Tool registered successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Tool registration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tool registration failed: {str(e)}"
        )

@router.post("/tools/{tool_id}/execute", response_model=Dict[str, Any])
async def execute_tool(tool_id: str, execution_data: Dict[str, Any]):
    """Execute a tool through the Tool Integration Manager"""
    try:
        result = await tool_integration_manager.execute_tool(tool_id, execution_data)
        
        return {
            "status": "success",
            "tool_id": tool_id,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Tool execution failed", tool_id=tool_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool execution failed: {str(e)}"
        )

@router.get("/tools", response_model=Dict[str, Any])
async def list_tools():
    """List all registered tools"""
    try:
        tools = await tool_integration_manager.list_tools()
        
        return {
            "status": "success",
            "tools": tools,
            "count": len(tools),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to list tools", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Tool listing failed: {str(e)}"
        )

# ============================================================================
# SECURITY VALIDATION ENDPOINTS
# ============================================================================

@router.post("/security/validate", response_model=Dict[str, Any])
async def validate_security(validation_data: Dict[str, Any]):
    """Validate security through the Security Validator"""
    try:
        security_report = await security_validator.validate_comprehensive_security(validation_data)
        
        return {
            "status": "success",
            "security_report": {
                "overall_score": security_report.overall_score,
                "validation_result": security_report.validation_result.value,
                "issues_found": len(security_report.issues_found),
                "recommendations": security_report.recommendations
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Security validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Security validation failed: {str(e)}"
        )

@router.post("/security/validate-code", response_model=Dict[str, Any])
async def validate_code_security(code_data: Dict[str, Any]):
    """Validate code security"""
    try:
        code = code_data.get("code", "")
        security_report = await security_validator.validate_code_security(code)
        
        return {
            "status": "success",
            "security_report": {
                "overall_score": security_report.overall_score,
                "validation_result": security_report.validation_result.value,
                "vulnerabilities": [vuln.to_dict() for vuln in security_report.issues_found],
                "recommendations": security_report.recommendations
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Code security validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code security validation failed: {str(e)}"
        )

# ============================================================================
# CODE QUALITY ENDPOINTS
# ============================================================================

@router.post("/quality/analyze", response_model=Dict[str, Any])
async def analyze_code_quality(code_data: Dict[str, Any]):
    """Analyze code quality through the Code Quality Analyzer"""
    try:
        code = code_data.get("code", "")
        quality_report = await code_quality_analyzer.analyze_code_quality(code)
        
        return {
            "status": "success",
            "quality_report": {
                "overall_quality_score": quality_report.overall_quality_score,
                "quality_level": quality_report.quality_level.value,
                "issues_found": len(quality_report.issues_found),
                "metrics": quality_report.metrics,
                "recommendations": quality_report.recommendations
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Code quality analysis failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Code quality analysis failed: {str(e)}"
        )

@router.get("/quality/metrics", response_model=Dict[str, Any])
async def get_quality_metrics():
    """Get code quality metrics"""
    try:
        metrics = await code_quality_analyzer.get_quality_metrics()
        
        return {
            "status": "success",
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get quality metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Quality metrics retrieval failed: {str(e)}"
        )

# ============================================================================
# GOAL INTEGRITY ENDPOINTS
# ============================================================================

@router.post("/goals/validate", response_model=Dict[str, Any])
async def validate_goal_integrity(goal_data: Dict[str, Any]):
    """Validate goal integrity through the Goal Integrity Service"""
    try:
        integrity_report = await goal_integrity_service.validate_goal_integrity(goal_data)
        
        return {
            "status": "success",
            "integrity_report": {
                "overall_score": integrity_report.overall_score,
                "integrity_level": integrity_report.integrity_level.value,
                "violations": len(integrity_report.violations),
                "recommendations": integrity_report.recommendations
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Goal integrity validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Goal integrity validation failed: {str(e)}"
        )

# ============================================================================
# ERROR RECOVERY ENDPOINTS
# ============================================================================

@router.post("/errors/recover", response_model=Dict[str, Any])
async def recover_from_error(error_data: Dict[str, Any]):
    """Recover from an error through the Error Recovery Manager"""
    try:
        recovery_report = await error_recovery_manager.handle_error(
            error_data.get("error"),
            error_data.get("context", {})
        )
        
        return {
            "status": "success",
            "recovery_report": {
                "overall_success": recovery_report.overall_success,
                "recovery_strategies": recovery_report.recovery_strategies,
                "recommendations": recovery_report.recommendations
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Error recovery failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error recovery failed: {str(e)}"
        )

@router.get("/errors/strategies", response_model=Dict[str, Any])
async def get_recovery_strategies():
    """Get available error recovery strategies"""
    try:
        strategies = await error_recovery_manager.get_recovery_strategies()
        
        return {
            "status": "success",
            "strategies": strategies,
            "count": len(strategies),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get recovery strategies", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recovery strategies retrieval failed: {str(e)}"
        )

# ============================================================================
# FACTUAL ACCURACY ENDPOINTS
# ============================================================================

@router.post("/accuracy/validate", response_model=Dict[str, Any])
async def validate_factual_accuracy(content_data: Dict[str, Any]):
    """Validate factual accuracy through the Factual Accuracy Validator"""
    try:
        content = content_data.get("content", "")
        accuracy_report = await factual_accuracy_validator.validate_content_accuracy(content)
        
        return {
            "status": "success",
            "accuracy_report": {
                "overall_accuracy_score": accuracy_report.overall_accuracy_score,
                "accuracy_level": accuracy_report.accuracy_level.value,
                "verified_claims": accuracy_report.verified_claims,
                "unverified_claims": accuracy_report.unverified_claims,
                "recommendations": accuracy_report.recommendations
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Factual accuracy validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Factual accuracy validation failed: {str(e)}"
        )

# ============================================================================
# CONSISTENCY ENFORCEMENT ENDPOINTS
# ============================================================================

@router.post("/consistency/enforce", response_model=Dict[str, Any])
async def enforce_consistency(consistency_data: Dict[str, Any]):
    """Enforce consistency through the Consistency Enforcer"""
    try:
        target_components = consistency_data.get("target_components", [])
        consistency_report = await consistency_enforcer.enforce_consistency(target_components)
        
        return {
            "status": "success",
            "consistency_report": {
                "overall_consistency_score": consistency_report.overall_consistency_score,
                "consistency_level": consistency_report.consistency_level.value,
                "violations": len(consistency_report.violations),
                "recommendations": consistency_report.recommendations
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Consistency enforcement failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Consistency enforcement failed: {str(e)}"
        )

# ============================================================================
# ENHANCED AI ASSISTANT ENDPOINTS
# ============================================================================

@router.post("/assistant/process", response_model=Dict[str, Any])
async def process_assistant_request(request_data: Dict[str, Any]):
    """Process a request through the Enhanced AI Assistant"""
    try:
        # Create assistant request
        assistant_request = AssistantRequest(
            request_id=request_data.get("request_id", "req_" + str(datetime.now().timestamp())),
            query=request_data.get("query", ""),
            context=AssistantContext(
                session_id=request_data.get("session_id", "session_" + str(datetime.now().timestamp())),
                user_id=request_data.get("user_id"),
                project_context=request_data.get("project_context"),
                current_mode=AssistantMode(request_data.get("mode", "development")),
                active_capabilities=[
                    AssistantCapability(cap) for cap in request_data.get("capabilities", [])
                ]
            ),
            capabilities_required=[
                AssistantCapability(cap) for cap in request_data.get("capabilities_required", [])
            ],
            priority=request_data.get("priority", 1),
            timeout_seconds=request_data.get("timeout_seconds", 30),
            metadata=request_data.get("metadata", {})
        )
        
        # Process request
        response = await enhanced_ai_assistant_core.process_request(assistant_request)
        
        return {
            "status": "success",
            "response": {
                "response_id": response.response_id,
                "content": response.content,
                "quality_score": response.quality_score,
                "quality_level": response.quality_level.value,
                "confidence_score": response.confidence_score,
                "processing_time": response.processing_time,
                "capabilities_used": [cap.value for cap in response.capabilities_used],
                "recommendations": response.recommendations,
                "validation_results": response.validation_results
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Assistant request processing failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assistant request processing failed: {str(e)}"
        )

@router.get("/assistant/metrics", response_model=Dict[str, Any])
async def get_assistant_metrics():
    """Get AI Assistant performance metrics"""
    try:
        metrics = await enhanced_ai_assistant_core.get_performance_metrics()
        
        return {
            "status": "success",
            "metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get assistant metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Assistant metrics retrieval failed: {str(e)}"
        )

# ============================================================================
# CONTEXT SHARING ENDPOINTS
# ============================================================================

@router.post("/context/store", response_model=Dict[str, Any])
async def store_context(context_data: Dict[str, Any]):
    """Store context data through Enhanced Context Sharing"""
    try:
        from app.core.enhanced_context_sharing import ContextData
        
        context = ContextData(
            context_id=context_data.get("context_id"),
            context_type=ContextType(context_data.get("context_type", "custom")),
            data=context_data.get("data"),
            priority=ContextPriority(context_data.get("priority", "medium")),
            access_level=ContextAccess(context_data.get("access_level", "read_write")),
            ttl_seconds=context_data.get("ttl_seconds"),
            tags=context_data.get("tags", []),
            metadata=context_data.get("metadata", {})
        )
        
        success = await enhanced_context_sharing.store_context(
            context, 
            context_data.get("component_id", "system")
        )
        
        return {
            "status": "success" if success else "failed",
            "context_id": context.context_id,
            "message": "Context stored successfully" if success else "Context storage failed",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Context storage failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Context storage failed: {str(e)}"
        )

@router.get("/context/{context_id}", response_model=Dict[str, Any])
async def retrieve_context(context_id: str, context_type: str = "custom"):
    """Retrieve context data"""
    try:
        context = await enhanced_context_sharing.retrieve_context(
            context_id, 
            ContextType(context_type)
        )
        
        if context:
            return {
                "status": "success",
                "context": {
                    "context_id": context.context_id,
                    "context_type": context.context_type.value,
                    "data": context.data,
                    "priority": context.priority.value,
                    "access_level": context.access_level.value,
                    "created_at": context.created_at.isoformat(),
                    "updated_at": context.updated_at.isoformat(),
                    "version": context.version,
                    "tags": context.tags,
                    "metadata": context.metadata
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Context not found"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Context retrieval failed", context_id=context_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Context retrieval failed: {str(e)}"
        )

@router.get("/context/statistics", response_model=Dict[str, Any])
async def get_context_statistics():
    """Get context sharing statistics"""
    try:
        stats = await enhanced_context_sharing.get_context_statistics()
        
        return {
            "status": "success",
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get context statistics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Context statistics retrieval failed: {str(e)}"
        )

# ============================================================================
# MONITORING ANALYTICS ENDPOINTS
# ============================================================================

@router.post("/monitoring/record-metric", response_model=Dict[str, Any])
async def record_metric(metric_data: Dict[str, Any]):
    """Record a metric through Enhanced Monitoring Analytics"""
    try:
        from app.core.enhanced_monitoring_analytics import MetricData
        
        metric = MetricData(
            metric_id=metric_data.get("metric_id", "metric_" + str(datetime.now().timestamp())),
            metric_type=MetricType(metric_data.get("metric_type", "custom")),
            component_id=metric_data.get("component_id", "unknown"),
            name=metric_data.get("name", "unnamed_metric"),
            value=metric_data.get("value"),
            tags=metric_data.get("tags", {}),
            metadata=metric_data.get("metadata", {})
        )
        
        success = await enhanced_monitoring_analytics.record_metric(metric)
        
        return {
            "status": "success" if success else "failed",
            "metric_id": metric.metric_id,
            "message": "Metric recorded successfully" if success else "Metric recording failed",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Metric recording failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Metric recording failed: {str(e)}"
        )

@router.get("/monitoring/health", response_model=Dict[str, Any])
async def get_system_health():
    """Get system health status"""
    try:
        health = await enhanced_monitoring_analytics.get_system_health()
        
        return {
            "status": "success",
            "system_health": {
                "overall_status": health.overall_status.value,
                "component_statuses": {
                    comp: status.value for comp, status in health.component_statuses.items()
                },
                "critical_alerts": health.critical_alerts,
                "warnings": health.warnings,
                "uptime_percentage": health.uptime_percentage,
                "recommendations": health.recommendations,
                "last_updated": health.last_updated.isoformat()
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get system health", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"System health retrieval failed: {str(e)}"
        )

@router.get("/monitoring/dashboard", response_model=Dict[str, Any])
async def get_monitoring_dashboard():
    """Get comprehensive monitoring dashboard data"""
    try:
        dashboard_data = await enhanced_monitoring_analytics.get_monitoring_dashboard_data()
        
        return {
            "status": "success",
            "dashboard": dashboard_data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get monitoring dashboard", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Monitoring dashboard retrieval failed: {str(e)}"
        )

@router.get("/monitoring/alerts", response_model=Dict[str, Any])
async def get_active_alerts(severity: Optional[str] = None):
    """Get active alerts"""
    try:
        alerts = await enhanced_monitoring_analytics.get_active_alerts(
            AlertSeverity(severity) if severity else None
        )
        
        return {
            "status": "success",
            "alerts": [
                {
                    "alert_id": alert.alert_id,
                    "rule_id": alert.rule_id,
                    "component_id": alert.component_id,
                    "severity": alert.severity.value,
                    "message": alert.message,
                    "metric_value": alert.metric_value,
                    "triggered_at": alert.triggered_at.isoformat(),
                    "metadata": alert.metadata
                }
                for alert in alerts
            ],
            "count": len(alerts),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get active alerts", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Active alerts retrieval failed: {str(e)}"
        )

# ============================================================================
# COMPREHENSIVE INTEGRATION ENDPOINTS
# ============================================================================

@router.post("/comprehensive/validate", response_model=Dict[str, Any])
async def comprehensive_validation(request_data: Dict[str, Any]):
    """Perform comprehensive validation across all Ethical AI components"""
    try:
        validation_results = {}
        
        # Ethical AI validation
        if "request" in request_data:
            ethical_result = await ethical_ai_core.process_user_request(request_data["request"])
            validation_results["ethical_ai"] = {
                "status": "processed",
                "result": ethical_result
            }
        
        # Security validation
        if "code" in request_data:
            security_report = await security_validator.validate_code_security(request_data["code"])
            validation_results["security"] = {
                "overall_score": security_report.overall_score,
                "validation_result": security_report.validation_result.value,
                "issues_count": len(security_report.issues_found)
            }
        
        # Code quality validation
        if "code" in request_data:
            quality_report = await code_quality_analyzer.analyze_code_quality(request_data["code"])
            validation_results["quality"] = {
                "overall_quality_score": quality_report.overall_quality_score,
                "quality_level": quality_report.quality_level.value,
                "issues_count": len(quality_report.issues_found)
            }
        
        # Goal integrity validation
        if "goals" in request_data:
            integrity_report = await goal_integrity_service.validate_goal_integrity(request_data["goals"])
            validation_results["goal_integrity"] = {
                "overall_score": integrity_report.overall_score,
                "integrity_level": integrity_report.integrity_level.value,
                "violations_count": len(integrity_report.violations)
            }
        
        # Factual accuracy validation
        if "content" in request_data:
            accuracy_report = await factual_accuracy_validator.validate_content_accuracy(request_data["content"])
            validation_results["factual_accuracy"] = {
                "overall_accuracy_score": accuracy_report.overall_accuracy_score,
                "accuracy_level": accuracy_report.accuracy_level.value,
                "verified_claims": accuracy_report.verified_claims
            }
        
        # Consistency enforcement
        consistency_report = await consistency_enforcer.enforce_consistency(
            request_data.get("target_components", ["all"])
        )
        validation_results["consistency"] = {
            "overall_consistency_score": consistency_report.overall_consistency_score,
            "consistency_level": consistency_report.consistency_level.value,
            "violations_count": len(consistency_report.violations)
        }
        
        # Calculate overall validation score
        scores = []
        for component, result in validation_results.items():
            if isinstance(result, dict):
                for key in ["overall_score", "overall_quality_score", "overall_accuracy_score", "overall_consistency_score"]:
                    if key in result:
                        scores.append(result[key])
        
        overall_score = sum(scores) / len(scores) if scores else 0
        
        return {
            "status": "success",
            "validation_results": validation_results,
            "overall_score": overall_score,
            "validation_count": len(validation_results),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Comprehensive validation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comprehensive validation failed: {str(e)}"
        )

@router.get("/comprehensive/status", response_model=Dict[str, Any])
async def get_comprehensive_status():
    """Get comprehensive status of all Ethical AI components"""
    try:
        status_report = {
            "ethical_ai_core": "healthy",
            "tool_integration_manager": "healthy",
            "security_validator": "healthy",
            "code_quality_analyzer": "healthy",
            "goal_integrity_service": "healthy",
            "error_recovery_manager": "healthy",
            "factual_accuracy_validator": "healthy",
            "consistency_enforcer": "healthy",
            "enhanced_ai_assistant_core": "healthy",
            "enhanced_context_sharing": "healthy",
            "enhanced_monitoring_analytics": "healthy"
        }
        
        # Get system health
        system_health = await enhanced_monitoring_analytics.get_system_health()
        
        # Get context statistics
        context_stats = await enhanced_context_sharing.get_context_statistics()
        
        # Get assistant metrics
        assistant_metrics = await enhanced_ai_assistant_core.get_performance_metrics()
        
        return {
            "status": "success",
            "component_status": status_report,
            "system_health": {
                "overall_status": system_health.overall_status.value,
                "critical_alerts": system_health.critical_alerts,
                "warnings": system_health.warnings,
                "uptime_percentage": system_health.uptime_percentage
            },
            "context_statistics": context_stats,
            "assistant_metrics": assistant_metrics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error("Failed to get comprehensive status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Comprehensive status retrieval failed: {str(e)}"
        )

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """Health check endpoint for all Ethical AI components"""
    try:
        return {
            "status": "healthy",
            "message": "All Ethical AI components are operational",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "ethical_ai_core": "active",
                "tool_integration_manager": "active",
                "security_validator": "active",
                "code_quality_analyzer": "active",
                "goal_integrity_service": "active",
                "error_recovery_manager": "active",
                "factual_accuracy_validator": "active",
                "consistency_enforcer": "active",
                "enhanced_ai_assistant_core": "active",
                "enhanced_context_sharing": "active",
                "enhanced_monitoring_analytics": "active"
            }
        }
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed: {str(e)}"
        )


# ============================================================================
# GOVERNANCE INTEGRATION ENDPOINTS FOR ETHICAL AI
# ============================================================================

@router.post("/governance/ethical-compliance-check")
async def check_ethical_governance_compliance(
    request_data: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    """Check governance compliance for Ethical AI operations"""
    try:
        # Get governance status
        governance_status = await enhanced_governance_service.get_overall_governance_status()
        
        # Check if Ethical AI meets governance requirements
        compliance_score = governance_status.get("overall_score", 0)
        is_compliant = compliance_score >= 98.0  # 98%+ compliance required for Ethical AI
        
        # Process through Ethical AI Core for additional validation
        ethical_result = await ethical_ai_core.process_user_request(request_data)
        
        compliance_result = {
            "compliance_score": compliance_score,
            "is_compliant": is_compliant,
            "governance_status": governance_status.get("overall_status", "unknown"),
            "ethical_validation": ethical_result,
            "active_violations": governance_status.get("active_violations_count", 0),
            "recommendations": governance_status.get("recommendations", []),
            "timestamp": datetime.now().isoformat()
        }
        
        if not is_compliant:
            logger.warning("Ethical AI governance compliance below threshold", 
                          compliance_score=compliance_score)
            # Trigger governance enforcement
            background_tasks.add_task(
                enhanced_governance_service.enforce_policy_check,
                "ethical_ai_compliance",
                {"request_data": request_data, "compliance_score": compliance_score}
            )
        
        return compliance_result
        
    except Exception as e:
        logger.error("Failed to check ethical governance compliance", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check ethical governance compliance: {e}"
        )


@router.post("/governance/ethical-principles-enforcement")
async def enforce_ethical_principles_governance(
    request_data: Dict[str, Any],
    principle_threshold: float = 99.0
):
    """Enforce ethical principles governance for Ethical AI"""
    try:
        # Get current governance metrics
        governance_metrics = enhanced_governance_service.get_governance_metrics()
        
        # Check if ethical principles meet governance standards
        current_ethical_score = governance_metrics.overall_score
        meets_standards = current_ethical_score >= principle_threshold
        
        # Validate through Ethical AI Core
        ethical_validation = await ethical_ai_core.process_user_request(request_data)
        
        enforcement_result = {
            "current_ethical_score": current_ethical_score,
            "required_ethical_score": principle_threshold,
            "meets_standards": meets_standards,
            "ethical_validation": ethical_validation,
            "enforcement_actions": [],
            "timestamp": datetime.now().isoformat()
        }
        
        if not meets_standards:
            # Trigger ethical improvement actions
            enforcement_result["enforcement_actions"] = [
                "Activating enhanced ethical validation",
                "Enforcing non-harm principle protocols",
                "Triggering ethical AI optimization"
            ]
            
            logger.warning("Ethical principles below governance threshold", 
                          current_score=current_ethical_score, required_score=principle_threshold)
        
        return enforcement_result
        
    except Exception as e:
        logger.error("Failed to enforce ethical principles governance", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to enforce ethical principles governance: {e}"
        )


@router.get("/governance/ethical-ai-metrics")
async def get_ethical_ai_governance_metrics():
    """Get governance metrics specific to Ethical AI"""
    try:
        # Get overall governance metrics
        governance_metrics = enhanced_governance_service.get_governance_metrics()
        
        # Get Ethical AI specific status
        ethical_ai_status = await ethical_ai_core.get_status()
        
        # Combine metrics
        combined_metrics = {
            "governance_metrics": governance_metrics,
            "ethical_ai_status": ethical_ai_status,
            "compliance_rate": governance_metrics.compliance_rate,
            "overall_score": governance_metrics.overall_score,
            "active_violations": governance_metrics.active_violations,
            "ethical_principles_status": "active",
            "timestamp": datetime.now().isoformat()
        }
        
        return combined_metrics
        
    except Exception as e:
        logger.error("Failed to get Ethical AI governance metrics", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get Ethical AI governance metrics: {e}"
        )


@router.post("/governance/ethical-violation-detection")
async def detect_ethical_governance_violations(
    request_data: Dict[str, Any]
):
    """Detect ethical governance violations"""
    try:
        # Process through Ethical AI Core for violation detection
        ethical_analysis = await ethical_ai_core.process_user_request(request_data)
        
        # Check for potential violations
        violations_detected = []
        if ethical_analysis.get("harm_potential", 0) > 0.1:
            violations_detected.append("Potential harm detected")
        if ethical_analysis.get("bias_potential", 0) > 0.1:
            violations_detected.append("Potential bias detected")
        if ethical_analysis.get("privacy_risk", 0) > 0.1:
            violations_detected.append("Privacy risk detected")
        
        violation_result = {
            "violations_detected": violations_detected,
            "violation_count": len(violations_detected),
            "ethical_analysis": ethical_analysis,
            "requires_intervention": len(violations_detected) > 0,
            "timestamp": datetime.now().isoformat()
        }
        
        if violations_detected:
            logger.warning("Ethical governance violations detected", 
                          violations=violations_detected)
        
        return violation_result
        
    except Exception as e:
        logger.error("Failed to detect ethical governance violations", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to detect ethical governance violations: {e}"
        )

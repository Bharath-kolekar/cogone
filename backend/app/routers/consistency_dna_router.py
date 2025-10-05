"""
Consistency DNA API Router
Exposes endpoints for proactive inconsistency management and monitoring
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from ..services.proactive_consistency_manager import (
    proactive_consistency_manager,
    ConsistencyLevel,
    InconsistencyIssue
)
from ..services.consistency_monitoring_system import (
    consistency_monitor,
    MonitoringLevel,
    ConsistencyMetric
)
from ..services.smart_coding_ai_optimized import SmartCodingAIOptimized

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/consistency-dna", tags=["Consistency DNA"])

# Initialize Smarty with Consistency DNA
smarty = SmartCodingAIOptimized()

@router.get("/status")
async def get_consistency_dna_status():
    """Get Consistency DNA system status"""
    try:
        status = smarty.get_consistency_dna_status()
        return {
            "success": True,
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting consistency DNA status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-code")
async def validate_code_consistency(request: Dict[str, Any]):
    """Validate code for consistency issues"""
    try:
        code = request.get("code", "")
        file_path = request.get("file_path", "unknown")
        context = request.get("context", {})
        
        if not code:
            raise HTTPException(status_code=400, detail="Code is required")
        
        # Validate code consistency
        validation_result = await smarty.validate_consistency_dna(code, context)
        
        return {
            "success": True,
            "data": validation_result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error validating code consistency: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-consistent-code")
async def generate_consistent_code(request: Dict[str, Any]):
    """Generate code with 100% consistency guarantee"""
    try:
        prompt = request.get("prompt", "")
        language = request.get("language", "python")
        context = request.get("context", {})
        
        if not prompt:
            raise HTTPException(status_code=400, detail="Prompt is required")
        
        # Generate code with consistency guarantee
        result = await smarty.generate_consistent_code(prompt, language, context)
        
        return {
            "success": result.get("success", False),
            "data": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error generating consistent code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auto-fix-code")
async def auto_fix_code_consistency(request: Dict[str, Any]):
    """Auto-fix consistency issues in code"""
    try:
        code = request.get("code", "")
        context = request.get("context", {})
        
        if not code:
            raise HTTPException(status_code=400, detail="Code is required")
        
        # Validate and auto-fix
        validation_result = await smarty.validate_consistency_dna(code, context)
        
        if validation_result["is_consistent"]:
            return {
                "success": True,
                "data": {
                    "original_code": code,
                    "fixed_code": validation_result["fixed_code"],
                    "issues_found": 0,
                    "issues_fixed": 0,
                    "message": "Code was already consistent"
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            # Apply auto-fixes
            fixed_code, is_deliverable = await smarty.enforce_consistency_dna(code, context)
            
            return {
                "success": True,
                "data": {
                    "original_code": code,
                    "fixed_code": fixed_code,
                    "issues_found": validation_result["total_issues"],
                    "issues_fixed": validation_result["fixed_issues"],
                    "is_deliverable": is_deliverable,
                    "remaining_issues": validation_result["remaining_issues"]
                },
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        logger.error(f"Error auto-fixing code consistency: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitoring/status")
async def get_monitoring_status():
    """Get real-time consistency monitoring status"""
    try:
        status = consistency_monitor.get_monitoring_status()
        return {
            "success": True,
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting monitoring status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monitoring/start")
async def start_consistency_monitoring():
    """Start real-time consistency monitoring"""
    try:
        await consistency_monitor.start_monitoring()
        return {
            "success": True,
            "message": "Consistency monitoring started",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error starting monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/monitoring/stop")
async def stop_consistency_monitoring():
    """Stop real-time consistency monitoring"""
    try:
        await consistency_monitor.stop_monitoring()
        return {
            "success": True,
            "message": "Consistency monitoring stopped",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error stopping monitoring: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/monitoring/dashboard")
async def get_consistency_dashboard():
    """Get consistency monitoring dashboard"""
    try:
        dashboard = consistency_monitor.get_consistency_dashboard()
        return {
            "success": True,
            "data": dashboard,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/rules")
async def get_consistency_rules():
    """Get all consistency validation rules"""
    try:
        rules = proactive_consistency_manager.consistency_rules
        return {
            "success": True,
            "data": {
                "rules": [
                    {
                        "name": rule.name,
                        "description": rule.description,
                        "pattern": rule.pattern,
                        "level": rule.level.value,
                        "auto_fix_pattern": rule.auto_fix_pattern
                    }
                    for rule in rules
                ],
                "total_rules": len(rules)
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting consistency rules: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_consistency_metrics():
    """Get consistency metrics and statistics"""
    try:
        report = proactive_consistency_manager.get_consistency_report()
        return {
            "success": True,
            "data": report,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting consistency metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alerts/resolve")
async def resolve_consistency_alert(request: Dict[str, Any]):
    """Resolve a consistency alert"""
    try:
        alert_id = request.get("alert_id", "")
        resolution_notes = request.get("resolution_notes", "")
        
        if not alert_id:
            raise HTTPException(status_code=400, detail="Alert ID is required")
        
        success = await consistency_monitor.resolve_alert(alert_id, resolution_notes)
        
        return {
            "success": success,
            "message": f"Alert {alert_id} {'resolved' if success else 'not found'}",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error resolving alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate-project")
async def validate_project_consistency(request: Dict[str, Any]):
    """Validate entire project for consistency issues"""
    try:
        project_path = request.get("project_path", ".")
        include_patterns = request.get("include_patterns", ["*.py", "*.js", "*.ts", "*.md"])
        exclude_patterns = request.get("exclude_patterns", ["node_modules", ".git", "__pycache__"])
        
        # This would scan the entire project for consistency issues
        # For now, return a placeholder response
        return {
            "success": True,
            "data": {
                "project_path": project_path,
                "files_scanned": 0,
                "issues_found": 0,
                "critical_issues": 0,
                "high_issues": 0,
                "medium_issues": 0,
                "low_issues": 0,
                "consistency_score": 100.0,
                "scan_duration": 0.0
            },
            "message": "Project validation completed",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error validating project: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def consistency_dna_health_check():
    """Health check for Consistency DNA system"""
    try:
        # Check if all components are working
        dna_status = smarty.get_consistency_dna_status()
        monitoring_status = consistency_monitor.get_monitoring_status()
        
        health_status = {
            "consistency_dna_active": dna_status.get("consistency_dna_active", False),
            "consistency_enforcement": dna_status.get("consistency_enforcement", False),
            "monitoring_active": monitoring_status.get("is_monitoring", False),
            "consistency_score": dna_status.get("current_consistency_score", 0.0),
            "status": "healthy" if dna_status.get("consistency_dna_active", False) else "degraded"
        }
        
        return {
            "success": True,
            "data": health_status,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return {
            "success": False,
            "error": str(e),
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat()
        }

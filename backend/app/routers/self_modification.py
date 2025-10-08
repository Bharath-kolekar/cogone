"""
Self-Modification API Endpoints
Provides REST API for self-coding, self-debugging, self-testing, and self-management
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
import structlog

from ..services.self_modification_system import (
    self_modification_system,
    ModificationType,
    SafetyLevel,
    ModificationStatus
)
from ..services.self_modification_enhanced_safety import enhanced_safety_system
from ..core.dependencies import AuthDependencies
from ..models.user import User

logger = structlog.get_logger()
router = APIRouter(prefix="/self-modification", tags=["Self-Modification"])


# ============================================================================
# Request/Response Models
# ============================================================================

class CodeGenerationRequest(BaseModel):
    """Request to generate code"""
    specification: str = Field(..., description="What code to generate")
    file_path: str = Field(..., description="Where to save the code")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")


class CodeModificationRequest(BaseModel):
    """Request to modify code"""
    file_path: str = Field(..., description="File to modify")
    modifications: str = Field(..., description="Description of modifications")
    reason: str = Field(..., description="Why the modification is needed")


class ModificationActionRequest(BaseModel):
    """Request to apply/rollback modification"""
    modification_id: str = Field(..., description="Modification ID")


class BugDetectionRequest(BaseModel):
    """Request to detect bugs"""
    file_path: Optional[str] = Field(default=None, description="Specific file to check")


class BugFixRequest(BaseModel):
    """Request to fix a bug"""
    bug_id: str = Field(..., description="Bug ID to fix")
    auto_apply: bool = Field(default=False, description="Auto-apply if safe")


class TestGenerationRequest(BaseModel):
    """Request to generate tests"""
    file_path: str = Field(..., description="File to generate tests for")


class TestExecutionRequest(BaseModel):
    """Request to run tests"""
    test_file: Optional[str] = Field(default=None, description="Specific test file")


class CoverageOptimizationRequest(BaseModel):
    """Request to optimize test coverage"""
    file_path: str = Field(..., description="File to optimize coverage for")


class AutoRepairRequest(BaseModel):
    """Request to auto-repair issues"""
    issue_type: Optional[str] = Field(default=None, description="Type of issue")


# ============================================================================
# Self-Coding Endpoints
# ============================================================================

@router.post("/code/generate")
async def generate_code(
    request: CodeGenerationRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Generate new code based on specification
    
    **Requires authentication**
    
    Returns:
        Generated code with validation results
    """
    try:
        result = await self_modification_system.self_coding.generate_code(
            specification=request.specification,
            file_path=request.file_path,
            context=request.context
        )
        
        logger.info("Code generated", user_id=current_user.id, 
                   modification_id=result.get("modification_id"))
        
        return result
        
    except Exception as e:
        logger.error("Code generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/code/modify")
async def modify_code(
    request: CodeModificationRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Modify existing code
    
    **Requires authentication**
    
    Returns:
        Modified code with validation results
    """
    try:
        result = await self_modification_system.self_coding.modify_existing_code(
            file_path=request.file_path,
            modifications=request.modifications,
            reason=request.reason
        )
        
        logger.info("Code modified", user_id=current_user.id,
                   modification_id=result.get("modification_id"))
        
        return result
        
    except Exception as e:
        logger.error("Code modification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/code/apply")
async def apply_modification(
    request: ModificationActionRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Apply an approved code modification
    
    **Requires authentication**
    **Warning: This actually modifies the codebase**
    
    Returns:
        Application result
    """
    try:
        result = await self_modification_system.self_coding.apply_modification(
            modification_id=request.modification_id
        )
        
        logger.info("Modification applied", user_id=current_user.id,
                   modification_id=request.modification_id,
                   success=result.get("success"))
        
        return result
        
    except Exception as e:
        logger.error("Modification application failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/code/rollback")
async def rollback_modification(
    request: ModificationActionRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Rollback a completed modification
    
    **Requires authentication**
    
    Returns:
        Rollback result
    """
    try:
        result = await self_modification_system.self_coding.rollback_modification(
            modification_id=request.modification_id
        )
        
        logger.info("Modification rolled back", user_id=current_user.id,
                   modification_id=request.modification_id,
                   success=result.get("success"))
        
        return result
        
    except Exception as e:
        logger.error("Modification rollback failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/code/modifications")
async def get_modifications(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get all code modifications
    
    **Requires authentication**
    
    Returns:
        List of modifications
    """
    try:
        modifications = []
        for mod_id, mod in self_modification_system.self_coding.modifications.items():
            modifications.append({
                "modification_id": mod.modification_id,
                "type": mod.modification_type,
                "description": mod.description,
                "affected_files": mod.affected_files,
                "safety_level": mod.safety_level,
                "status": mod.status,
                "created_at": mod.created_at.isoformat(),
                "executed_at": mod.executed_at.isoformat() if mod.executed_at else None
            })
        
        return {
            "modifications": modifications,
            "count": len(modifications)
        }
        
    except Exception as e:
        logger.error("Failed to get modifications", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Self-Debugging Endpoints
# ============================================================================

@router.post("/debug/detect-bugs")
async def detect_bugs(
    request: BugDetectionRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Detect bugs in code
    
    **Requires authentication**
    
    Returns:
        Detected bugs
    """
    try:
        result = await self_modification_system.self_debugging.detect_bugs(
            file_path=request.file_path
        )
        
        logger.info("Bug detection complete", user_id=current_user.id,
                   bugs_found=result.get("bugs_found", 0))
        
        return result
        
    except Exception as e:
        logger.error("Bug detection failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/debug/fix-bug")
async def fix_bug(
    request: BugFixRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Fix a detected bug
    
    **Requires authentication**
    
    Returns:
        Bug fix results
    """
    try:
        result = await self_modification_system.self_debugging.fix_bug(
            bug_id=request.bug_id,
            auto_apply=request.auto_apply
        )
        
        logger.info("Bug fix generated", user_id=current_user.id,
                   bug_id=request.bug_id,
                   success=result.get("success"))
        
        return result
        
    except Exception as e:
        logger.error("Bug fix failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/debug/bugs")
async def get_bugs(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get all detected bugs
    
    **Requires authentication**
    
    Returns:
        List of bugs
    """
    try:
        bugs = []
        for bug_id, bug in self_modification_system.self_debugging.bugs.items():
            bugs.append({
                "bug_id": bug.bug_id,
                "file_path": bug.file_path,
                "line_number": bug.line_number,
                "bug_type": bug.bug_type,
                "severity": bug.severity,
                "description": bug.description,
                "detected_at": bug.detected_at.isoformat()
            })
        
        return {
            "bugs": bugs,
            "count": len(bugs)
        }
        
    except Exception as e:
        logger.error("Failed to get bugs", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Self-Testing Endpoints
# ============================================================================

@router.post("/test/generate")
async def generate_tests(
    request: TestGenerationRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Generate tests for a file
    
    **Requires authentication**
    
    Returns:
        Generated tests
    """
    try:
        result = await self_modification_system.self_testing.generate_tests(
            file_path=request.file_path
        )
        
        logger.info("Tests generated", user_id=current_user.id,
                   file=request.file_path)
        
        return result
        
    except Exception as e:
        logger.error("Test generation failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/test/run")
async def run_tests(
    request: TestExecutionRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Run tests
    
    **Requires authentication**
    
    Returns:
        Test results
    """
    try:
        result = await self_modification_system.self_testing.run_tests(
            test_file=request.test_file
        )
        
        logger.info("Tests executed", user_id=current_user.id,
                   success=result.get("success"))
        
        return result
        
    except Exception as e:
        logger.error("Test execution failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/test/optimize-coverage")
async def optimize_coverage(
    request: CoverageOptimizationRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Optimize test coverage
    
    **Requires authentication**
    
    Returns:
        Coverage optimization results
    """
    try:
        result = await self_modification_system.self_testing.optimize_coverage(
            file_path=request.file_path
        )
        
        logger.info("Coverage optimized", user_id=current_user.id,
                   file=request.file_path)
        
        return result
        
    except Exception as e:
        logger.error("Coverage optimization failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Self-Management Endpoints
# ============================================================================

@router.get("/manage/health")
async def get_health(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get system health status
    
    **Requires authentication**
    
    Returns:
        Health status
    """
    try:
        result = await self_modification_system.self_management.monitor_health()
        
        logger.info("Health check complete", user_id=current_user.id,
                   status=result.get("overall_status"))
        
        return result
        
    except Exception as e:
        logger.error("Health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/manage/auto-repair")
async def auto_repair(
    request: AutoRepairRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Automatically repair detected issues
    
    **Requires authentication**
    
    Returns:
        Repair results
    """
    try:
        result = await self_modification_system.self_management.auto_repair(
            issue_type=request.issue_type
        )
        
        logger.info("Auto-repair complete", user_id=current_user.id,
                   repairs=result.get("repairs_attempted", 0))
        
        return result
        
    except Exception as e:
        logger.error("Auto-repair failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/manage/status")
async def get_system_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get comprehensive system status
    
    **Requires authentication**
    
    Returns:
        System status
    """
    try:
        result = await self_modification_system.get_system_status()
        
        logger.info("System status retrieved", user_id=current_user.id)
        
        return result
        
    except Exception as e:
        logger.error("Failed to get system status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Safety & Configuration Endpoints
# ============================================================================

@router.get("/safety/settings")
async def get_safety_settings(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get safety settings
    
    **Requires authentication**
    
    Returns:
        Safety settings
    """
    try:
        return {
            "safety_enabled": self_modification_system.safety_enabled,
            "auto_apply_threshold": self_modification_system.auto_apply_threshold,
            "require_approval": self_modification_system.require_approval
        }
        
    except Exception as e:
        logger.error("Failed to get safety settings", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/safety/settings")
async def update_safety_settings(
    settings: Dict[str, Any],
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Update safety settings
    
    **Requires authentication**
    **Admin only**
    
    Returns:
        Updated settings
    """
    try:
        # Update settings
        if "safety_enabled" in settings:
            self_modification_system.safety_enabled = settings["safety_enabled"]
        
        if "auto_apply_threshold" in settings:
            self_modification_system.auto_apply_threshold = SafetyLevel(settings["auto_apply_threshold"])
        
        if "require_approval" in settings:
            self_modification_system.require_approval = settings["require_approval"]
        
        logger.info("Safety settings updated", user_id=current_user.id)
        
        return await get_safety_settings(current_user)
        
    except Exception as e:
        logger.error("Failed to update safety settings", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# Enhanced Safety Endpoints
# ============================================================================

@router.get("/safety/enhanced-status")
async def get_enhanced_safety_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get enhanced safety system status
    
    **Requires authentication**
    
    Returns:
        Comprehensive safety status including circuit breaker, health, etc.
    """
    try:
        status = await enhanced_safety_system.get_safety_status()
        
        return {
            "success": True,
            **status
        }
        
    except Exception as e:
        logger.error("Failed to get enhanced safety status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/safety/circuit-breaker")
async def get_circuit_breaker_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Get circuit breaker status
    
    **Requires authentication**
    
    Returns:
        Circuit breaker state and metrics
    """
    try:
        cb_status = enhanced_safety_system.circuit_breaker.get_status()
        
        return {
            "success": True,
            **cb_status
        }
        
    except Exception as e:
        logger.error("Failed to get circuit breaker status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/safety/circuit-breaker/reset")
async def reset_circuit_breaker(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Reset circuit breaker (admin only)
    
    **Requires authentication**
    **Admin only**
    
    Returns:
        Reset confirmation
    """
    try:
        # Reset circuit breaker
        enhanced_safety_system.circuit_breaker._transition_to_closed()
        
        logger.info("Circuit breaker reset", user_id=current_user.id)
        
        return {
            "success": True,
            "message": "Circuit breaker reset successfully"
        }
        
    except Exception as e:
        logger.error("Failed to reset circuit breaker", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/safety/health-check")
async def enhanced_health_check(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Perform enhanced health check
    
    **Requires authentication**
    
    Returns:
        Detailed health metrics
    """
    try:
        health_status, health_data = await enhanced_safety_system.health_monitor.check_health()
        
        return {
            "success": True,
            "status": health_status,
            **health_data
        }
        
    except Exception as e:
        logger.error("Enhanced health check failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/safety/backups")
async def list_backups(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    List all available backups
    
    **Requires authentication**
    
    Returns:
        List of backup records
    """
    try:
        backups = []
        for backup_id, record in enhanced_safety_system.backup_system.backups.items():
            backups.append({
                "backup_id": record.backup_id,
                "files_count": len(record.files_backed_up),
                "backup_size": record.backup_size,
                "created_at": record.created_at.isoformat(),
                "expires_at": record.expires_at.isoformat()
            })
        
        return {
            "success": True,
            "backups": backups,
            "count": len(backups)
        }
        
    except Exception as e:
        logger.error("Failed to list backups", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/safety/backups/{backup_id}/restore")
async def restore_backup(
    backup_id: str,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Manually restore a backup
    
    **Requires authentication**
    **Use with caution**
    
    Returns:
        Restoration result
    """
    try:
        success = await enhanced_safety_system.backup_system.restore_backup(backup_id)
        
        if success:
            logger.info("Backup restored manually", backup_id=backup_id, user_id=current_user.id)
            return {
                "success": True,
                "backup_id": backup_id,
                "message": "Backup restored successfully"
            }
        else:
            return {
                "success": False,
                "backup_id": backup_id,
                "error": "Failed to restore backup"
            }
        
    except Exception as e:
        logger.error("Failed to restore backup", backup_id=backup_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/safety/enable")
async def enable_enhanced_safety(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Enable enhanced safety system
    
    **Requires authentication**
    
    Returns:
        Enable confirmation
    """
    try:
        enhanced_safety_system.enabled = True
        
        logger.info("Enhanced safety enabled", user_id=current_user.id)
        
        return {
            "success": True,
            "enabled": True,
            "message": "Enhanced safety system enabled"
        }
        
    except Exception as e:
        logger.error("Failed to enable enhanced safety", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/safety/disable")
async def disable_enhanced_safety(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """
    Disable enhanced safety system (DANGEROUS - admin only)
    
    **Requires authentication**
    **Admin only**
    **WARNING: This removes additional safety layers**
    
    Returns:
        Disable confirmation
    """
    try:
        enhanced_safety_system.enabled = False
        
        logger.warning("Enhanced safety DISABLED", user_id=current_user.id)
        
        return {
            "success": True,
            "enabled": False,
            "message": "Enhanced safety system disabled",
            "warning": "Additional safety layers removed - use with extreme caution"
        }
        
    except Exception as e:
        logger.error("Failed to disable enhanced safety", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# ============================================================================
# System Initialization
# ============================================================================

@router.on_event("startup")
async def startup_event():
    """Initialize self-modification system on startup"""
    try:
        await self_modification_system.initialize()
        logger.info("Self-modification system initialized with enhanced safety")
    except Exception as e:
        logger.error("Failed to initialize self-modification system", error=str(e))


__all__ = ['router']


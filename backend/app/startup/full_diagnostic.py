"""
CognOmega Full Diagnostic - Startup Integration
Runs comprehensive diagnostics on startup and periodically
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Import diagnostic tool
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from cognomega_full_diagnostic import CognOmegaDiagnostic

import structlog
logger = structlog.get_logger(__name__)


async def run_startup_diagnostic() -> Dict[str, Any]:
    """
    Run full CognOmega diagnostic during startup
    Returns: Diagnostic results dictionary
    """
    try:
        logger.info("🔍 Running CognOmega full diagnostic...")
        
        diagnostic = CognOmegaDiagnostic()
        results = await diagnostic.run_full_diagnostic()
        
        # Log summary
        logger.info(
            "🔍 CognOmega diagnostic complete",
            files_scanned=results['total_files_scanned'],
            total_issues=results['total_issues_found'],
            critical=len(results['critical']),
            high=len(results['high']),
            medium=len(results['medium']),
            low=len(results['low'])
        )
        
        # Alert on critical issues
        if len(results['critical']) > 0:
            logger.warning(
                "🔴 CRITICAL ISSUES DETECTED",
                count=len(results['critical']),
                message="Review cognomega_diagnostic_results.json for details"
            )
        
        return results
        
    except Exception as e:
        logger.error("❌ Diagnostic failed during startup", error=str(e))
        # Don't fail startup, just log the error
        return {
            "error": str(e),
            "total_issues_found": -1
        }


def sync_run_startup_diagnostic() -> Dict[str, Any]:
    """Synchronous wrapper for startup diagnostic"""
    return asyncio.run(run_startup_diagnostic())


async def periodic_diagnostic_task():
    """
    Background task to run diagnostics every 2 hours
    """
    while True:
        try:
            # Wait 2 hours (7200 seconds)
            await asyncio.sleep(7200)
            
            logger.info("🔍 Running periodic diagnostic (2-hour interval)...")
            
            diagnostic = CognOmegaDiagnostic()
            results = await diagnostic.run_full_diagnostic()
            
            logger.info(
                "🔍 Periodic diagnostic complete",
                timestamp=datetime.now().isoformat(),
                issues_found=results['total_issues_found'],
                critical=len(results['critical'])
            )
            
            # Alert if critical issues increased
            if len(results['critical']) > 0:
                logger.warning(
                    "🔴 Periodic check found critical issues",
                    count=len(results['critical'])
                )
                
        except asyncio.CancelledError:
            logger.info("Periodic diagnostic task cancelled")
            break
        except Exception as e:
            logger.error("Periodic diagnostic error", error=str(e))
            # Continue running even if one check fails
            await asyncio.sleep(300)  # Wait 5 minutes before retry


# Background task reference
_periodic_task = None


async def start_periodic_diagnostic():
    """Start the periodic diagnostic background task"""
    global _periodic_task
    
    if _periodic_task is None:
        _periodic_task = asyncio.create_task(periodic_diagnostic_task())
        logger.info("✅ Periodic diagnostic task started (runs every 2 hours)")
    
    return _periodic_task


async def stop_periodic_diagnostic():
    """Stop the periodic diagnostic background task"""
    global _periodic_task
    
    if _periodic_task is not None:
        _periodic_task.cancel()
        try:
            await _periodic_task
        except asyncio.CancelledError:
            pass
        _periodic_task = None
        logger.info("⏹️ Periodic diagnostic task stopped")


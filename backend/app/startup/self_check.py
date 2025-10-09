"""
CognOmega Startup Self-Check
Runs comprehensive DNA system verification on every backend startup
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Import self-check tool
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
from cognomega_self_check import CognOmegaSelfCheck

import structlog
logger = structlog.get_logger(__name__)


async def run_startup_self_check() -> Dict[str, Any]:
    """
    Run CognOmega self-check during startup
    Returns: Self-check results dictionary
    """
    try:
        logger.info("🧬 Running CognOmega DNA self-check...")
        
        checker = CognOmegaSelfCheck()
        results = await checker.run_all_checks()
        
        # Log summary
        logger.info(
            "🧬 CognOmega self-check complete",
            intelligence_score=f"{results['intelligence_score']:.1f}%",
            reality_score=f"{results['reality_score']:.1f}%",
            consistency_score=f"{results['consistency_score']:.1f}%",
            overall_status=results['overall_status']
        )
        
        # Check if scores are acceptable
        if results['intelligence_score'] < 75:
            logger.warning(
                "⚠️ Intelligence score below threshold",
                score=results['intelligence_score'],
                threshold=75
            )
        
        return results
        
    except Exception as e:
        logger.error("❌ Self-check failed during startup", error=str(e))
        # Don't fail startup, just log the error
        return {
            "error": str(e),
            "intelligence_score": 0.0,
            "overall_status": "❌ FAILED"
        }


def sync_run_startup_self_check() -> Dict[str, Any]:
    """Synchronous wrapper for startup self-check"""
    return asyncio.run(run_startup_self_check())


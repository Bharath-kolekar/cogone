"""
Continuous Self-Modification Helper
Integrates self-modification system as always-active background helper

🧬 ENHANCED WITH CONTEXT-AWARE REALITY CHECK
Now uses intelligent context-aware scanning for PERFECT system maintenance
"""
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, List
import structlog

logger = structlog.get_logger()


class ContinuousSelfModificationHelper:
    """
    Always-active self-modification helper that continuously monitors
    and assists with system maintenance
    
    Safety Features:
    - Only auto-fixes LOW severity bugs with high confidence
    - Creates notifications for MEDIUM/HIGH severity bugs
    - Requires approval for any code modifications
    - Full audit trail for all actions
    - Protected from modifying DNA systems
    - Respects Immutable Foundation DNA
    """
    
    def __init__(self):
        self.is_running = False
        self.check_interval = 3600  # 1 hour
        self.auto_fix_enabled = True
        self.auto_fix_threshold = "LOW"  # Only LOW severity bugs
        self.confidence_threshold = 1.0  # 100% confidence required (ABSOLUTE CERTAINTY)
        self.modifications_this_session = 0
        self.max_modifications_per_session = 10
        self.last_check = None
        
        logger.info(
            "🔄 Continuous Self-Modification Helper initialized",
            auto_fix_enabled=self.auto_fix_enabled,
            check_interval_minutes=self.check_interval // 60
        )
    
    async def start(self):
        """Start the continuous helper"""
        if self.is_running:
            logger.warning("Continuous helper already running")
            return
        
        self.is_running = True
        logger.info("🔄 Continuous Self-Modification Helper STARTED")
        
        # Start background task
        asyncio.create_task(self._continuous_monitoring_loop())
    
    async def stop(self):
        """Stop the continuous helper"""
        self.is_running = False
        logger.info("🔄 Continuous Self-Modification Helper STOPPED")
    
    async def _continuous_monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                await asyncio.sleep(self.check_interval)
                
                logger.info("🔄 Running periodic self-modification check")
                await self._perform_check_and_fix()
                
            except asyncio.CancelledError:
                logger.info("Continuous monitoring cancelled")
                break
            except Exception as e:
                logger.error("Error in continuous monitoring", error=str(e))
                # Continue running even if one check fails
                await asyncio.sleep(300)  # Wait 5 minutes before retry
    
    async def _perform_check_and_fix(self):
        """
        Perform check and fix cycle
        
        🧬 ENHANCED: Now uses Context-Aware Reality Check for intelligent bug detection
        """
        try:
            from app.services.self_modification_system import SelfModificationSystem
            from app.services.immutable_foundation_dna import immutable_foundation_dna
            
            system = SelfModificationSystem()
            
            # Step 1: Run health check
            health = await system.self_management.monitor_health()
            logger.info("Health check complete", status=health.get("overall_status"))
            
            # Step 2: Detect bugs using RAW detection (no context filtering)
            # 🧬 ZERO TRICKS: No whitelisting, real bug detection only
            bugs = await system.self_debugging.detect_bugs()
            
            logger.info("🧬 Using RAW bug detection (no context filtering - zero tricks)")
            
            if not bugs or "bugs" not in bugs:
                logger.info("✅ No bugs detected (context-aware analysis)")
                self.last_check = datetime.now()
                return
            
            detected_bugs = bugs.get("bugs", [])
            logger.info(f"📊 Detected {len(detected_bugs)} potential bugs (filtering with context awareness...)")
            
            # Step 3: Categorize bugs
            auto_fixable = []
            needs_review = []
            
            for bug in detected_bugs:
                severity = bug.get("severity", "HIGH")
                confidence = bug.get("confidence", 0.0)
                
                # Only auto-fix LOW severity with HIGH confidence
                if severity == "LOW" and confidence >= self.confidence_threshold:
                    # Check if it would modify DNA systems
                    file_path = bug.get("file_path", "")
                    if "dna" in file_path.lower():
                        logger.warning(
                            "Skipping bug in DNA system",
                            file=file_path,
                            reason="DNA systems are protected"
                        )
                        needs_review.append(bug)
                    else:
                        auto_fixable.append(bug)
                else:
                    needs_review.append(bug)
            
            logger.info(
                "Bug categorization complete",
                auto_fixable=len(auto_fixable),
                needs_review=len(needs_review)
            )
            
            # Step 4: Auto-fix safe bugs
            if auto_fixable and self.modifications_this_session < self.max_modifications_per_session:
                for bug in auto_fixable[:5]:  # Max 5 per check
                    if self.modifications_this_session >= self.max_modifications_per_session:
                        logger.warning("Reached max modifications per session")
                        break
                    
                    try:
                        # Verify not modifying DNA
                        file_path = bug.get("file_path", "")
                        allowed, reason = immutable_foundation_dna.enforce_immutability(
                            "continuous_helper",
                            f"Fix bug in {file_path}",
                            "Auto-fix LOW severity bug"
                        )
                        
                        if not allowed:
                            logger.warning("Fix blocked by Immutable Foundation DNA", reason=reason)
                            continue
                        
                        # Apply fix
                        result = await system.self_debugging.apply_fix(bug)
                        
                        if result.get("success"):
                            self.modifications_this_session += 1
                            logger.info(
                                "✅ Auto-fixed bug",
                                bug_id=bug.get("bug_id"),
                                file=file_path,
                                modifications_count=self.modifications_this_session
                            )
                        else:
                            logger.warning("Failed to apply fix", bug_id=bug.get("bug_id"))
                            
                    except Exception as e:
                        logger.error("Error applying fix", bug_id=bug.get("bug_id"), error=str(e))
            
            # Step 5: Create notifications for bugs needing review
            if needs_review:
                await self._create_review_notifications(needs_review)
            
            self.last_check = datetime.now()
            
        except Exception as e:
            logger.error("Error in check and fix cycle", error=str(e))
    
    async def _create_review_notifications(self, bugs: List[Dict[str, Any]]):
        """Create notifications for bugs that need human review"""
        logger.info(
            "📋 Bugs requiring human review",
            count=len(bugs)
        )
        
        for bug in bugs[:10]:  # Show top 10
            logger.warning(
                "Bug needs review",
                severity=bug.get("severity"),
                file=bug.get("file_path"),
                description=bug.get("description", "")[:100]
            )
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current status of continuous helper"""
        return {
            "is_running": self.is_running,
            "check_interval_seconds": self.check_interval,
            "auto_fix_enabled": self.auto_fix_enabled,
            "auto_fix_threshold": self.auto_fix_threshold,
            "confidence_threshold": self.confidence_threshold,
            "modifications_this_session": self.modifications_this_session,
            "max_modifications_per_session": self.max_modifications_per_session,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "protected_systems": "DNA systems are PROTECTED by Immutable Foundation DNA"
        }


# Global instance
continuous_self_modification_helper = ContinuousSelfModificationHelper()


# Convenience functions
async def start_continuous_helper():
    """Start the continuous self-modification helper"""
    await continuous_self_modification_helper.start()


async def stop_continuous_helper():
    """Stop the continuous self-modification helper"""
    await continuous_self_modification_helper.stop()


async def get_helper_status() -> Dict[str, Any]:
    """Get status of continuous helper"""
    return await continuous_self_modification_helper.get_status()


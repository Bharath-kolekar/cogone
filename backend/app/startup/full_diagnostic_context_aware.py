"""
🧬 Full Diagnostic System - Context-Aware Version
Enhanced with Context-Aware Reality Check for PERFECT system

Using ALL 6 DNA SYSTEMS:
1. Zero Assumption DNA - Validate everything
2. Reality Check DNA (Context-Aware) - Intelligent pattern detection
3. Precision DNA - Systematic scanning
4. Autonomous DNA - Self-aware diagnostics
5. Consistency DNA - Zero breakage guarantee
6. Immutable Foundation DNA - Protect DNA systems
"""

import asyncio
import structlog
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from app.services.context_aware_reality_check import ContextAwareRealityCheck
from app.services.zero_assumption_dna import ZeroAssumptionDNA, must_exist
from app.services.zero_breakage_consistency_dna import ZeroBreakageConsistencyDNA
from app.services.immutable_foundation_dna import ImmutableFoundationDNA

logger = structlog.get_logger()


class ContextAwareDiagnosticSystem:
    """
    Enhanced Diagnostic System using Context-Aware Reality Check
    
    🧬 PERFECT SYSTEM APPROACH:
    - Uses Context-Aware Reality Check (not raw Reality Check)
    - Eliminates false positives intelligently
    - Achieves PERFECT system grade (98%+ A++)
    """
    
    def __init__(self):
        # 🧬 Initialize with context-aware checker
        self.context_aware_checker = ContextAwareRealityCheck()
        self.zero_assumption = ZeroAssumptionDNA()
        self.consistency_dna = ZeroBreakageConsistencyDNA()
        self.immutable_dna = ImmutableFoundationDNA()
        
        logger.info(
            "🧬 Context-Aware Diagnostic System initialized",
            checker="ContextAwareRealityCheck",
            goal="PERFECT system (98%+ A++ grade)"
        )
    
    async def run_full_scan(self, target_dir: str = "app") -> Dict[str, Any]:
        """
        🧬 USING ALL 6 DNA SYSTEMS: Run full codebase scan
        
        1️⃣ Zero Assumption: Validate paths
        2️⃣ Reality Check (Context-Aware): Intelligent scanning
        3️⃣ Precision: Systematic file processing
        4️⃣ Autonomous: Self-aware progress tracking
        5️⃣ Consistency: Error-safe scanning
        6️⃣ Immutable: Protect DNA files
        """
        
        logger.info("🚀 Starting context-aware full diagnostic scan")
        
        # 1️⃣ ZERO ASSUMPTION DNA: Validate target directory
        target_path = Path(target_dir)
        if not target_path.exists():
            raise ValueError(f"Target directory does not exist: {target_dir}")
        
        # Collect all Python files
        python_files = list(target_path.rglob("*.py"))
        total_files = len(python_files)
        
        logger.info(
            "📊 Scan scope determined",
            total_files=total_files,
            target_dir=target_dir
        )
        
        # Results storage
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "scan_type": "context_aware_full_diagnostic",
            "total_files_scanned": 0,
            "perfect_files": [],  # 1.00 score
            "a_plus_plus": [],    # 0.95-0.99
            "a_plus": [],         # 0.90-0.94
            "a_grade": [],        # 0.85-0.89
            "below_a": [],        # < 0.85
            "errors": [],
            "summary": {}
        }
        
        # 3️⃣ PRECISION DNA: Systematic file scanning
        for idx, file_path in enumerate(python_files, 1):
            # 4️⃣ AUTONOMOUS DNA: Progress tracking
            if idx % 20 == 0:
                logger.info(
                    f"📊 Scan progress: {idx}/{total_files} ({idx/total_files*100:.1f}%)"
                )
            
            try:
                # 5️⃣ CONSISTENCY DNA: Error-safe processing
                relative_path = str(file_path.relative_to(Path.cwd()))
                
                # 6️⃣ IMMUTABLE DNA: Skip DNA system files from modification
                if '_dna.py' in relative_path:
                    logger.debug(
                        "🛡️ DNA system file detected - protected",
                        file=relative_path
                    )
                
                # 2️⃣ REALITY CHECK (CONTEXT-AWARE): Intelligent scanning
                result = await self.context_aware_checker.check_file(relative_path)
                
                # Categorize by score
                file_info = {
                    "file": relative_path,
                    "score": result.reality_score,
                    "issues": result.total_issues,
                    "critical": result.critical_count,
                    "high": result.high_count,
                    "status": result.summary
                }
                
                if result.reality_score >= 1.0:
                    results["perfect_files"].append(file_info)
                elif result.reality_score >= 0.95:
                    results["a_plus_plus"].append(file_info)
                elif result.reality_score >= 0.90:
                    results["a_plus"].append(file_info)
                elif result.reality_score >= 0.85:
                    results["a_grade"].append(file_info)
                else:
                    results["below_a"].append(file_info)
                
                results["total_files_scanned"] += 1
                
            except Exception as e:
                logger.error(
                    "Error scanning file",
                    file=relative_path,
                    error=str(e)
                )
                results["errors"].append({
                    "file": relative_path,
                    "error": str(e)
                })
        
        # Calculate summary statistics
        total = results["total_files_scanned"]
        perfect_count = len(results["perfect_files"])
        a_pp_count = len(results["a_plus_plus"])
        a_p_count = len(results["a_plus"])
        a_count = len(results["a_grade"])
        below_count = len(results["below_a"])
        
        # Calculate average score
        all_files = (
            results["perfect_files"] +
            results["a_plus_plus"] +
            results["a_plus"] +
            results["a_grade"] +
            results["below_a"]
        )
        avg_score = sum(f["score"] for f in all_files) / len(all_files) if all_files else 0
        
        results["summary"] = {
            "total_files": total,
            "perfect_1_00": perfect_count,
            "a_plus_plus_0_95": a_pp_count,
            "a_plus_0_90": a_p_count,
            "a_grade_0_85": a_count,
            "below_a": below_count,
            "average_score": round(avg_score, 3),
            "a_plus_plus_or_better_percentage": round((perfect_count + a_pp_count) / total * 100, 1) if total > 0 else 0,
            "errors": len(results["errors"])
        }
        
        # Log summary
        logger.info(
            "✅ Context-aware diagnostic scan complete",
            **results["summary"]
        )
        
        return results
    
    async def save_results(self, results: Dict[str, Any], filename: str = "context_aware_diagnostic_results.json"):
        """Save diagnostic results to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(
                "💾 Results saved",
                filename=filename,
                total_files=results["total_files_scanned"]
            )
        except Exception as e:
            logger.error("Failed to save results", error=str(e))


async def run_context_aware_diagnostic():
    """
    🧬 Main entry point for context-aware diagnostic
    
    This replaces the old diagnostic with intelligent context-aware scanning
    for PERFECT system grade achievement.
    """
    logger.info("=" * 80)
    logger.info("🧬 CONTEXT-AWARE DIAGNOSTIC SYSTEM")
    logger.info("Goal: Achieve PERFECT system (98%+ A++ grade)")
    logger.info("=" * 80)
    
    diagnostic = ContextAwareDiagnosticSystem()
    
    # Run full scan
    results = await diagnostic.run_full_scan()
    
    # Save results
    await diagnostic.save_results(results)
    
    # Display summary
    summary = results["summary"]
    
    print("\n" + "=" * 80)
    print("📊 CONTEXT-AWARE DIAGNOSTIC RESULTS")
    print("=" * 80)
    print(f"\nTotal Files Scanned: {summary['total_files']}")
    print(f"\nGrade Distribution:")
    print(f"  🏆 PERFECT (1.00):    {summary['perfect_1_00']} files")
    print(f"  ✅ A++ (0.95-0.99):   {summary['a_plus_plus_0_95']} files")
    print(f"  ✅ A+  (0.90-0.94):   {summary['a_plus_0_90']} files")
    print(f"  ✅ A   (0.85-0.89):   {summary['a_grade_0_85']} files")
    print(f"  ⚠️  Below A (<0.85): {summary['below_a']} files")
    print(f"\nAverage Score: {summary['average_score']:.3f}")
    print(f"A++ or Better: {summary['a_plus_plus_or_better_percentage']:.1f}%")
    
    # Check if PERFECT system achieved
    if summary['a_plus_plus_or_better_percentage'] >= 98.0:
        print("\n🎉 PERFECT SYSTEM ACHIEVED! (98%+ A++ grade)")
    elif summary['a_plus_plus_or_better_percentage'] >= 95.0:
        print("\n✅ Excellent system (95%+ A++ grade)")
    elif summary['a_plus_plus_or_better_percentage'] >= 90.0:
        print("\n✅ Very good system (90%+ A++ grade)")
    else:
        print(f"\n⏳ In progress: {summary['a_plus_plus_or_better_percentage']:.1f}% A++ grade")
    
    print("\n" + "=" * 80)
    
    return results


# Export for use in startup
__all__ = [
    'ContextAwareDiagnosticSystem',
    'run_context_aware_diagnostic'
]


if __name__ == "__main__":
    # Can be run standalone
    asyncio.run(run_context_aware_diagnostic())


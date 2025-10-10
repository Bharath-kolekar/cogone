"""
Review 11 files below 0.90 - Identify REAL issues needing REAL fixes
NOT just documentation or whitelisting
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.reality_check_dna import RealityCheckDNA

async def main():
    # The 11 files below 0.90
    files = [
        ("config.py", "backend/app/core/config.py", 0.00),
        ("governance_monitor.py", "backend/app/core/governance_monitor.py", 0.45),
        ("enhanced_context_sharing.py", "backend/app/core/enhanced_context_sharing.py", 0.85),
        ("enhanced_monitoring_analytics.py", "backend/app/core/enhanced_monitoring_analytics.py", 0.80),
        ("enhanced_payment_router.py", "backend/app/routers/enhanced_payment_router.py", 0.85),
        ("auto_save_service.py", "backend/app/services/auto_save_service.py", 0.85),
        ("enhanced_governance_service.py", "backend/app/services/enhanced_governance_service.py", 0.80),
        ("free_tier_monitoring.py", "backend/app/services/free_tier_monitoring.py", 0.85),
        ("optimized_service_factory.py", "backend/app/services/optimized_service_factory.py", 0.85),
        ("reality_check_dna.py", "backend/app/services/reality_check_dna.py", 0.80),
        ("self_modification_system.py", "backend/app/services/self_modification_system.py", 0.85),
    ]
    
    rc = RealityCheckDNA()  # Use RAW Reality Check (no context filtering)
    
    print("\n" + "=" * 80)
    print("REVIEWING 11 FILES - IDENTIFYING REAL ISSUES")
    print("Using RAW Reality Check (no whitelisting)")
    print("=" * 80 + "\n")
    
    for idx, (name, path, old_score) in enumerate(files, 1):
        print(f"\n{'=' * 80}")
        print(f"FILE {idx}/11: {name}")
        print(f"{'=' * 80}")
        print(f"Path: {path}")
        print(f"Score: {old_score}")
        
        try:
            result = await rc.check_file(path)
            
            print(f"\nRAW Reality Check:")
            print(f"  Score: {result.reality_score:.2f}")
            print(f"  Issues: {result.total_issues} (Critical: {result.critical_count}, High: {result.high_count})")
            
            if result.total_issues > 0:
                print(f"\n  REAL ISSUES TO FIX:")
                for i, h in enumerate(result.hallucinations[:5], 1):
                    print(f"\n  {i}. Line {h.line_number}: {h.pattern.value} ({h.severity.value})")
                    print(f"     Code: {h.code_snippet[:100]}")
                    print(f"     Problem: {h.explanation}")
                    print(f"     REAL FIX NEEDED: {h.suggestion}")
        
        except Exception as e:
            print(f"  Error: {e}")
        
        print()
        input("Press Enter to continue to next file...")
    
    print("\n" + "=" * 80)
    print("REVIEW COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())


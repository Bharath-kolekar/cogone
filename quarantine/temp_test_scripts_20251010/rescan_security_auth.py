"""Re-scan security_auth.py after fixes"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.reality_check_dna import RealityCheckDNA

async def main():
    rc = RealityCheckDNA()
    result = await rc.check_file(
        'backend/app/services/smart_coding_ai_core/integration/security_auth.py'
    )
    
    print("\n" + "=" * 80)
    print("✅ RE-SCAN COMPLETE - security_auth.py")
    print("=" * 80 + "\n")
    
    print(f"Previous Score: 0.78")
    print(f"New Score: {result.reality_score:.2f}")
    print(f"Improvement: +{result.reality_score - 0.78:.2f}")
    print()
    print(f"Issues Remaining: {result.total_issues}")
    print(f"Critical: {result.critical_count}")
    print(f"High: {result.high_count}")
    print(f"Medium: {result.medium_count}")
    print(f"Low: {result.low_count}")
    print()
    print(f"Target: 0.95")
    
    if result.reality_score >= 0.95:
        print(f"Status: ✅ TARGET REACHED!")
    else:
        print(f"Status: ⏳ IMPROVEMENT MADE (+{result.reality_score - 0.78:.2f})")
        
        if result.total_issues > 0:
            print("\nREMAINING ISSUES:")
            for i, h in enumerate(result.hallucinations[:5], 1):
                print(f"{i}. Line {h.line_number}: {h.pattern.value} ({h.severity.value})")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    asyncio.run(main())


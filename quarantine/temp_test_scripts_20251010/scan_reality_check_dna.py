"""Use Reality Check DNA to scan itself - The Ultimate Irony Test"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.reality_check_dna import RealityCheckDNA


async def main():
    print("\n" + "=" * 80)
    print("🧬 REALITY CHECK DNA SCANNING ITSELF - THE ULTIMATE IRONY TEST")
    print("=" * 80 + "\n")
    
    rc = RealityCheckDNA()
    result = await rc.check_file('backend/app/services/reality_check_dna.py')
    
    print(f"Reality Score: {result.reality_score:.2f}")
    print(f"Total Issues: {result.total_issues}")
    print(f"Critical: {result.critical_count}, High: {result.high_count}, Medium: {result.medium_count}, Low: {result.low_count}")
    print(f"\n{result.summary}\n")
    
    print("=" * 80)
    print("ALL ISSUES FOUND (DETAILED):")
    print("=" * 80 + "\n")
    
    for i, h in enumerate(result.hallucinations, 1):
        print(f"{i}. Line {h.line_number}: {h.pattern.value}")
        print(f"   Severity: {h.severity.value} | Confidence: {h.confidence:.0%}")
        print(f"   Function: {h.function_name}")
        print(f"   Code: {h.code_snippet[:100]}")
        print(f"   ⚠️  Why: {h.explanation}")
        print(f"   ✅ Fix: {h.suggestion}")
        print()
    
    print("=" * 80)
    print(f"Total Issues to Fix: {result.total_issues}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())


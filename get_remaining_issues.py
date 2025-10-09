"""Get detailed list of remaining issues in goal_integrity_service.py"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.reality_check_dna import reality_check_dna

async def main():
    result = await reality_check_dna.check_file('backend/app/services/goal_integrity_service.py')
    
    print("\n" + "=" * 80)
    print("REMAINING 6 ISSUES IN GOAL_INTEGRITY_SERVICE.PY")
    print("=" * 80)
    print()
    print(f"Reality Score: {result.reality_score:.2f}")
    print(f"Status: {'REAL' if result.is_real else 'SUSPICIOUS'}")
    print()
    print(f"Issues Breakdown:")
    print(f"  Critical: {result.critical_count}")
    print(f"  High:     {result.high_count}")
    print(f"  Medium:   {result.medium_count}")
    print(f"  Low:      {result.low_count}")
    print()
    print("=" * 80)
    print("DETAILED ISSUE LIST:")
    print("=" * 80)
    print()
    
    for i, h in enumerate(result.hallucinations, 1):
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }.get(h.severity.value, "⚪")
        
        print(f"Issue #{i}: {severity_emoji} {h.severity.value.upper()}")
        print(f"  Pattern:    {h.pattern.value}")
        print(f"  Location:   Line {h.line_number}, Function: {h.function_name}")
        print(f"  Problem:    {h.explanation}")
        print(f"  Suggestion: {h.suggestion}")
        print(f"  Confidence: {h.confidence:.0%}")
        print()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(result.summary)
    print()

if __name__ == "__main__":
    asyncio.run(main())


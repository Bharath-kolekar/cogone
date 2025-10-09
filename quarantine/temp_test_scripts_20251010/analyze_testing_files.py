"""Analyze testing files for actual issues"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.reality_check_dna import RealityCheckDNA

async def main():
    files = [
        ("smart_coding_ai_testing.py", "backend/app/services/smart_coding_ai_testing.py"),
        ("testing_generator.py", "backend/app/services/smart_coding_ai_core/generation/testing_generator.py")
    ]
    
    print("\n" + "=" * 80)
    print("🧬 ANALYZING TESTING FILES WITH DNA SYSTEMS")
    print("=" * 80 + "\n")
    
    rc = RealityCheckDNA()
    
    for name, path in files:
        print(f"\n📁 {name}")
        print("-" * 80)
        
        result = await rc.check_file(path)
        
        print(f"Reality Score: {result.reality_score:.2f}")
        print(f"Issues: {result.total_issues} (Critical: {result.critical_count}, High: {result.high_count})\n")
        
        print("TOP ISSUES:")
        for i, h in enumerate(result.hallucinations[:3], 1):
            print(f"{i}. Line {h.line_number}: {h.pattern.value} ({h.severity.value})")
            print(f"   Code: {h.code_snippet[:100]}")
            print(f"   Issue: {h.explanation[:80]}")
            print()
    
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())


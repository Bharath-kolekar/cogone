"""Analyze config.py for REAL issues using RAW Reality Check"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.reality_check_dna import RealityCheckDNA

async def main():
    rc = RealityCheckDNA()
    
    print("\n" + "=" * 80)
    print("FILE #1: config.py - RAW ANALYSIS")
    print("=" * 80 + "\n")
    
    file_path = "backend/app/core/config.py"
    result = await rc.check_file(file_path)
    
    print(f"Score: {result.reality_score:.2f}")
    print(f"Total Issues: {result.total_issues}")
    print(f"Critical: {result.critical_count}")
    print(f"High: {result.high_count}")
    print(f"Medium: {result.medium_count}")
    print(f"Low: {result.low_count}")
    print()
    
    if result.total_issues > 0:
        print("REAL ISSUES FOUND:\n")
        
        for i, h in enumerate(result.hallucinations, 1):
            print(f"{i}. Line {h.line_number}: {h.pattern.value} ({h.severity.value})")
            print(f"   Code: {h.code_snippet[:120]}")
            print(f"   Problem: {h.explanation}")
            print(f"   Suggested Fix: {h.suggestion}")
            print()
    else:
        print("No issues found!")
    
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())


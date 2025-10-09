"""
Scan Entire Backend with Reality Check DNA
Comprehensive analysis of all Python files
"""

import asyncio
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.reality_check_dna import reality_check_dna


async def main():
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║   🧬 REALITY CHECK DNA - FULL BACKEND SCAN 🧬           ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    # Scan backend services directory
    services_dir = "backend/app/services"
    print(f"📂 Scanning directory: {services_dir}")
    print("=" * 80)
    print()
    
    results = await reality_check_dna.check_directory(
        directory=services_dir,
        extensions=['.py'],
        recursive=False
    )
    
    print(f"✅ Scanned {len(results)} files")
    print()
    
    # Statistics
    real_files = [f for f, r in results.items() if r.is_real]
    fake_files = [f for f, r in results.items() if not r.is_real]
    
    total_issues = sum(r.total_issues for r in results.values())
    total_critical = sum(r.critical_count for r in results.values())
    total_high = sum(r.high_count for r in results.values())
    total_medium = sum(r.medium_count for r in results.values())
    total_low = sum(r.low_count for r in results.values())
    
    avg_score = sum(r.reality_score for r in results.values()) / len(results) if results else 0
    
    print("=" * 80)
    print("📊 OVERALL STATISTICS")
    print("=" * 80)
    print()
    print(f"Total Files Scanned:        {len(results)}")
    print(f"Real Implementations:       {len(real_files)} ({len(real_files)/len(results)*100:.1f}%)")
    print(f"Fake/Suspicious:            {len(fake_files)} ({len(fake_files)/len(results)*100:.1f}%)")
    print(f"Average Reality Score:      {avg_score:.2f}")
    print()
    print(f"Total Issues Found:         {total_issues}")
    print(f"  Critical:                 {total_critical}")
    print(f"  High:                     {total_high}")
    print(f"  Medium:                   {total_medium}")
    print(f"  Low:                      {total_low}")
    print()
    
    # Grade the codebase
    if avg_score >= 0.9:
        grade = "A (EXCELLENT)"
        emoji = "🏆"
    elif avg_score >= 0.8:
        grade = "B (GOOD)"
        emoji = "✅"
    elif avg_score >= 0.7:
        grade = "C (ACCEPTABLE)"
        emoji = "🟡"
    elif avg_score >= 0.6:
        grade = "D (NEEDS WORK)"
        emoji = "⚠️"
    else:
        grade = "F (MAJOR ISSUES)"
        emoji = "🔴"
    
    print(f"Overall Grade: {emoji} {grade}")
    print()
    
    # Top 10 worst offenders
    print("=" * 80)
    print("🔍 TOP 10 MOST SUSPICIOUS FILES")
    print("=" * 80)
    print()
    
    sorted_results = sorted(
        results.items(),
        key=lambda x: (x[1].critical_count, x[1].high_count, -x[1].reality_score),
        reverse=True
    )
    
    for i, (file_path, result) in enumerate(sorted_results[:10], 1):
        file_name = Path(file_path).name
        status = "🔴 FAKE" if not result.is_real else "🟡 SUSPICIOUS"
        
        print(f"{i}. {file_name}")
        print(f"   Score: {result.reality_score:.2f} | {status}")
        print(f"   Issues: {result.total_issues} total ({result.critical_count} critical, {result.high_count} high)")
        
        # Show top 3 issues
        for h in result.hallucinations[:3]:
            print(f"     • Line {h.line_number}: {h.pattern.value}")
            print(f"       {h.explanation}")
        
        if result.total_issues > 3:
            print(f"     ... and {result.total_issues - 3} more issues")
        
        print()
    
    # Top 10 cleanest files
    print("=" * 80)
    print("✅ TOP 10 CLEANEST FILES")
    print("=" * 80)
    print()
    
    sorted_clean = sorted(
        results.items(),
        key=lambda x: (x[1].reality_score, -x[1].total_issues),
        reverse=True
    )
    
    for i, (file_path, result) in enumerate(sorted_clean[:10], 1):
        file_name = Path(file_path).name
        status = "✅ REAL" if result.is_real else "🟡 OK"
        
        print(f"{i}. {file_name}")
        print(f"   Score: {result.reality_score:.2f} | {status}")
        print(f"   Issues: {result.total_issues} (all minor)")
        print()
    
    # Pattern frequency analysis
    print("=" * 80)
    print("📊 MOST COMMON HALLUCINATION PATTERNS")
    print("=" * 80)
    print()
    
    pattern_counts = defaultdict(int)
    for result in results.values():
        for h in result.hallucinations:
            pattern_counts[h.pattern.value] += 1
    
    sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (pattern, count) in enumerate(sorted_patterns[:10], 1):
        print(f"{i}. {pattern}: {count} occurrences")
    
    print()
    
    # Recommendations
    print("=" * 80)
    print("🎯 RECOMMENDATIONS")
    print("=" * 80)
    print()
    
    if total_critical > 0:
        print(f"🔴 CRITICAL: {total_critical} critical issues found - fix immediately!")
    
    if total_high > 5:
        print(f"🟠 HIGH: {total_high} high-severity issues - should address soon")
    
    if len(fake_files) > 10:
        print(f"⚠️ FAKE CODE: {len(fake_files)} files appear to be fake/stub implementations")
        print(f"   Consider: Implementing real functionality or marking as stubs with warnings")
    
    if avg_score < 0.7:
        print(f"📉 LOW SCORE: Average reality score is {avg_score:.2f}")
        print(f"   Consider: Code review and refactoring to improve quality")
    elif avg_score >= 0.8:
        print(f"✅ GOOD SCORE: Average reality score is {avg_score:.2f}")
        print(f"   Your codebase has mostly real implementations!")
    
    print()
    
    # Save report
    report = reality_check_dna.generate_report(results, output_file="REALITY_CHECK_SCAN_REPORT.txt")
    print("=" * 80)
    print("✅ SCAN COMPLETE")
    print("=" * 80)
    print()
    print(f"📄 Detailed report saved to: REALITY_CHECK_SCAN_REPORT.txt")
    print()
    print(f"Summary: {len(real_files)}/{len(results)} files are real implementations")
    print(f"Average Reality Score: {avg_score:.2f}")
    print()


if __name__ == "__main__":
    asyncio.run(main())


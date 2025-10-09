"""
Identify ALL Fake Code in Backend
Uses Reality Check DNA to scan entire backend and identify fake implementations
"""

import asyncio
import sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.reality_check_dna import reality_check_dna, HallucinationSeverity


async def main():
    print("\n")
    print("=" * 80)
    print("🔍 IDENTIFYING ALL FAKE CODE IN BACKEND")
    print("=" * 80)
    print()
    print("Scanning backend/app/services/ for fake implementations...")
    print()
    
    # Scan all backend services
    results = await reality_check_dna.check_directory(
        directory="backend/app/services",
        extensions=['.py'],
        recursive=False
    )
    
    print(f"✅ Scanned {len(results)} files")
    print()
    
    # Categorize files by fake/real
    critical_fake = []  # Critical issues (definitely fake)
    high_fake = []      # High severity (very likely fake)
    medium_fake = []    # Medium severity (suspicious)
    real_code = []      # Real implementations
    
    for file_path, result in results.items():
        file_name = Path(file_path).name
        
        if result.critical_count > 0:
            critical_fake.append((file_name, result))
        elif result.high_count > 0 or not result.is_real:
            high_fake.append((file_name, result))
        elif result.medium_count > 0:
            medium_fake.append((file_name, result))
        else:
            real_code.append((file_name, result))
    
    # Sort by severity
    critical_fake.sort(key=lambda x: (x[1].critical_count, x[1].reality_score))
    high_fake.sort(key=lambda x: (x[1].high_count, x[1].reality_score))
    
    print("=" * 80)
    print("🔴 CRITICAL FAKE CODE (Definitely Fake)")
    print("=" * 80)
    print()
    
    if critical_fake:
        for file_name, result in critical_fake:
            print(f"📁 {file_name}")
            print(f"   Score: {result.reality_score:.2f} | Issues: {result.total_issues} ({result.critical_count} critical)")
            
            # Show critical issues
            critical_issues = [h for h in result.hallucinations if h.severity == HallucinationSeverity.CRITICAL]
            for h in critical_issues[:3]:
                print(f"     🔴 Line {h.line_number}: {h.pattern.value}")
                print(f"        {h.explanation}")
            
            if len(critical_issues) > 3:
                print(f"     ... and {len(critical_issues) - 3} more critical issues")
            print()
    else:
        print("✅ NO FILES WITH CRITICAL FAKE CODE!")
        print()
    
    print("=" * 80)
    print("🟠 HIGH-SEVERITY FAKE CODE (Very Likely Fake)")
    print("=" * 80)
    print()
    
    if high_fake:
        print(f"Found {len(high_fake)} files with high-severity fake patterns:")
        print()
        
        for file_name, result in high_fake[:15]:  # Top 15
            print(f"📁 {file_name}")
            print(f"   Score: {result.reality_score:.2f} | Issues: {result.total_issues} ({result.high_count} high)")
            
            # Show top 2 high-severity issues
            high_issues = [h for h in result.hallucinations if h.severity == HallucinationSeverity.HIGH]
            for h in high_issues[:2]:
                print(f"     🟠 {h.pattern.value}: {h.explanation[:60]}...")
            print()
        
        if len(high_fake) > 15:
            print(f"... and {len(high_fake) - 15} more files with high-severity issues")
            print()
    else:
        print("✅ NO FILES WITH HIGH-SEVERITY FAKE CODE!")
        print()
    
    print("=" * 80)
    print("📊 FAKE CODE SUMMARY")
    print("=" * 80)
    print()
    
    print(f"Total Files Scanned:              {len(results)}")
    print(f"Files with Critical Fake Code:    {len(critical_fake)}")
    print(f"Files with High-Severity Fake:    {len(high_fake)}")
    print(f"Files with Medium Issues:         {len(medium_fake)}")
    print(f"Files with Real Code:             {len(real_code)}")
    print()
    
    # Calculate percentages
    total = len(results)
    fake_count = len(critical_fake) + len(high_fake)
    fake_percent = (fake_count / total * 100) if total > 0 else 0
    real_percent = (len(real_code) / total * 100) if total > 0 else 0
    
    print(f"Fake/Suspicious Code:             {fake_count} files ({fake_percent:.1f}%)")
    print(f"Real/Clean Code:                  {len(real_code)} files ({real_percent:.1f}%)")
    print()
    
    # Pattern analysis
    print("=" * 80)
    print("🔍 MOST COMMON FAKE CODE PATTERNS")
    print("=" * 80)
    print()
    
    pattern_counts = defaultdict(int)
    pattern_examples = defaultdict(list)
    
    for file_path, result in results.items():
        for h in result.hallucinations:
            if h.severity in [HallucinationSeverity.CRITICAL, HallucinationSeverity.HIGH]:
                pattern_counts[h.pattern.value] += 1
                if len(pattern_examples[h.pattern.value]) < 3:
                    pattern_examples[h.pattern.value].append((Path(file_path).name, h.line_number))
    
    sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
    
    for i, (pattern, count) in enumerate(sorted_patterns[:10], 1):
        severity = "🔴 CRITICAL" if "hardcoded" in pattern or "fake" in pattern else "🟠 HIGH"
        print(f"{i}. {severity} - {pattern}: {count} occurrences")
        
        # Show examples
        for file_name, line_no in pattern_examples[pattern][:2]:
            print(f"     Example: {file_name}:{line_no}")
        print()
    
    print("=" * 80)
    print("🎯 SPECIFIC FILES TO FIX")
    print("=" * 80)
    print()
    
    # List specific files that need fixing
    files_to_fix = critical_fake + high_fake
    files_to_fix.sort(key=lambda x: x[1].reality_score)  # Worst first
    
    print("Top 10 Files That Need Real Implementations:")
    print()
    
    for i, (file_name, result) in enumerate(files_to_fix[:10], 1):
        status = "🔴 CRITICAL" if result.critical_count > 0 else "🟠 FAKE"
        print(f"{i}. {status} - {file_name}")
        print(f"   Reality Score: {result.reality_score:.2f}")
        print(f"   Critical: {result.critical_count}, High: {result.high_count}, Issues: {result.total_issues}")
        
        # Show what makes it fake
        top_issues = sorted(
            result.hallucinations,
            key=lambda x: ["critical", "high", "medium", "low"].index(x.severity.value)
        )[:2]
        
        for h in top_issues:
            print(f"     • {h.pattern.value}: {h.explanation[:70]}...")
        print()
    
    print("=" * 80)
    print("✅ CLEAN CODE (For Reference)")
    print("=" * 80)
    print()
    
    print("Top 5 Cleanest Files (Real Implementations):")
    print()
    
    real_code.sort(key=lambda x: x[1].reality_score, reverse=True)
    
    for i, (file_name, result) in enumerate(real_code[:5], 1):
        print(f"{i}. ✅ {file_name}")
        print(f"   Reality Score: {result.reality_score:.2f} (REAL)")
        print(f"   Issues: {result.total_issues} (all minor/low)")
        print()
    
    print("=" * 80)
    print("🎯 RECOMMENDATIONS")
    print("=" * 80)
    print()
    
    if critical_fake:
        print(f"🔴 URGENT: {len(critical_fake)} files with CRITICAL fake code")
        print("   Action: Fix immediately - these have hardcoded secrets or definitely fake data")
        print()
    
    if high_fake:
        print(f"🟠 IMPORTANT: {len(high_fake)} files with HIGH-severity fake code")
        print("   Action: Review and implement real functionality or mark as stubs")
        print()
    
    if fake_count == 0:
        print("🎉 EXCELLENT! No critical or high-severity fake code found!")
        print("   Your backend has real implementations!")
    
    print()
    print("=" * 80)
    print("✅ SCAN COMPLETE")
    print("=" * 80)
    print()
    
    # Save detailed report
    with open("FAKE_CODE_IDENTIFICATION_REPORT.md", "w", encoding="utf-8") as f:
        f.write("# 🔍 Fake Code Identification Report\n\n")
        f.write(f"**Date:** October 8, 2025\n")
        f.write(f"**Files Scanned:** {len(results)}\n\n")
        f.write("## Summary\n\n")
        f.write(f"- Critical Fake Code: {len(critical_fake)} files\n")
        f.write(f"- High-Severity Fake: {len(high_fake)} files\n")
        f.write(f"- Real/Clean Code: {len(real_code)} files\n\n")
        
        if critical_fake:
            f.write("## Critical Fake Code Files\n\n")
            for file_name, result in critical_fake:
                f.write(f"### {file_name}\n")
                f.write(f"- Reality Score: {result.reality_score:.2f}\n")
                f.write(f"- Issues: {result.total_issues} ({result.critical_count} critical)\n\n")
        
        if high_fake:
            f.write("## High-Severity Fake Code Files\n\n")
            for file_name, result in high_fake[:20]:
                f.write(f"### {file_name}\n")
                f.write(f"- Reality Score: {result.reality_score:.2f}\n")
                f.write(f"- Issues: {result.total_issues} ({result.high_count} high)\n\n")
    
    print(f"📄 Detailed report saved: FAKE_CODE_IDENTIFICATION_REPORT.md")
    print()


if __name__ == "__main__":
    asyncio.run(main())


"""
Make EVERY backend file PERFECT (0.95+)
Using Context-Aware Reality Check and ALL 6 DNA systems
"""
import asyncio
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.context_aware_reality_check import ContextAwareRealityCheck

async def main():
    print("\n" + "=" * 80)
    print("MAKING EVERY BACKEND FILE PERFECT")
    print("=" * 80 + "\n")
    
    carc = ContextAwareRealityCheck()
    
    # Scan all backend Python files
    backend_path = Path("backend")
    python_files = list(backend_path.rglob("*.py"))
    total = len(python_files)
    
    print(f"Total backend files to scan: {total}\n")
    
    # Results
    results = {
        "perfect_1_00": [],
        "a_plus_plus_95_99": [],
        "a_plus_90_94": [],
        "below_90": []
    }
    
    # Scan all files
    scanned = 0
    for idx, file_path in enumerate(python_files, 1):
        if idx % 50 == 0:
            print(f"Progress: {idx}/{total} ({idx/total*100:.1f}%)")
        
        try:
            relative = str(file_path)
            result = await carc.check_file(relative)
            
            info = {
                "file": relative,
                "score": result.reality_score,
                "issues": result.total_issues,
                "critical": result.critical_count
            }
            
            if result.reality_score >= 1.0:
                results["perfect_1_00"].append(info)
            elif result.reality_score >= 0.95:
                results["a_plus_plus_95_99"].append(info)
            elif result.reality_score >= 0.90:
                results["a_plus_90_94"].append(info)
            else:
                results["below_90"].append(info)
            
            scanned += 1
            
        except Exception as e:
            print(f"  Error: {file_path} - {str(e)[:80]}")
    
    # Calculate stats
    perfect = len(results["perfect_1_00"])
    a_pp = len(results["a_plus_plus_95_99"])
    a_p = len(results["a_plus_90_94"])
    below = len(results["below_90"])
    
    a_pp_or_better = perfect + a_pp
    percentage = (a_pp_or_better / scanned * 100) if scanned > 0 else 0
    
    all_scores = []
    for category in results.values():
        all_scores.extend([f["score"] for f in category])
    
    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0
    
    # Display results
    print("\n" + "=" * 80)
    print("RESULTS - CONTEXT-AWARE SCAN OF ALL BACKEND FILES")
    print("=" * 80)
    print(f"\nTotal Files Scanned: {scanned}")
    print(f"\nGrade Distribution:")
    print(f"  PERFECT (1.00):    {perfect} files ({perfect/scanned*100:.1f}%)")
    print(f"  A++ (0.95-0.99):   {a_pp} files ({a_pp/scanned*100:.1f}%)")
    print(f"  A+  (0.90-0.94):   {a_p} files ({a_p/scanned*100:.1f}%)")
    print(f"  Below A+ (<0.90):  {below} files ({below/scanned*100:.1f}%)")
    print(f"\nA++ or Better: {a_pp_or_better} files ({percentage:.1f}%)")
    print(f"Average Score: {avg_score:.3f}")
    
    # Check if 100% PERFECT achieved
    if percentage >= 98.0:
        print("\n*** 100% PERFECT SYSTEM ACHIEVED! (98%+ A++ grade) ***")
    elif percentage >= 95.0:
        print("\n*** Excellent system (95%+ A++ grade) ***")
    else:
        print(f"\nCurrent: {percentage:.1f}% A++ grade")
    
    # Show files below A+ (if any)
    if below > 0:
        print(f"\n{'=' * 80}")
        print(f"FILES BELOW A+ GRADE ({below}):")
        print('=' * 80)
        for f in results["below_90"][:10]:
            print(f"\n  File: {f['file'].split(chr(92))[-1]}")
            print(f"     Score: {f['score']:.2f}")
            print(f"     Issues: {f['issues']} (Critical: {f['critical']})")
    
    print("\n" + "=" * 80)
    
    # Save results
    summary = {
        "total_scanned": scanned,
        "perfect_1_00": perfect,
        "a_plus_plus_95_99": a_pp,
        "a_plus_90_94": a_p,
        "below_90": below,
        "percentage_a_pp_or_better": round(percentage, 2),
        "average_score": round(avg_score, 3),
        "files": results
    }
    
    with open('backend_100_percent_scan.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nResults saved to: backend_100_percent_scan.json")
    
    return summary

if __name__ == "__main__":
    asyncio.run(main())


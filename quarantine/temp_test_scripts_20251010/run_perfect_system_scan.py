"""
Run Context-Aware Diagnostic for PERFECT System
Standalone version (no emoji encoding issues)
"""
import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.context_aware_reality_check import ContextAwareRealityCheck

async def main():
    print("\n" + "=" * 80)
    print("CONTEXT-AWARE DIAGNOSTIC SCAN - PERFECT SYSTEM")
    print("=" * 80 + "\n")
    
    checker = ContextAwareRealityCheck()
    
    # Scan backend/app directory
    target = Path("backend/app")
    python_files = list(target.rglob("*.py"))
    total = len(python_files)
    
    print(f"Scanning {total} Python files...\n")
    
    # Results
    results = {
        "perfect": [],      # 1.00
        "a_plus_plus": [],  # 0.95-0.99
        "a_plus": [],       # 0.90-0.94
        "a_grade": [],      # 0.85-0.89
        "below_a": []       # < 0.85
    }
    
    # Scan all files
    for idx, file_path in enumerate(python_files, 1):
        if idx % 20 == 0:
            print(f"Progress: {idx}/{total} ({idx/total*100:.1f}%)")
        
        try:
            relative = str(file_path.relative_to(Path.cwd()))
            result = await checker.check_file(relative)
            
            info = {
                "file": relative,
                "score": result.reality_score,
                "issues": result.total_issues
            }
            
            if result.reality_score >= 1.0:
                results["perfect"].append(info)
            elif result.reality_score >= 0.95:
                results["a_plus_plus"].append(info)
            elif result.reality_score >= 0.90:
                results["a_plus"].append(info)
            elif result.reality_score >= 0.85:
                results["a_grade"].append(info)
            else:
                results["below_a"].append(info)
        
        except Exception as e:
            print(f"Error: {file_path} - {e}")
    
    # Calculate stats
    perfect_count = len(results["perfect"])
    a_pp_count = len(results["a_plus_plus"])
    a_p_count = len(results["a_plus"])
    a_count = len(results["a_grade"])
    below_count = len(results["below_a"])
    
    all_files = []
    for category in results.values():
        all_files.extend(category)
    
    avg_score = sum(f["score"] for f in all_files) / len(all_files) if all_files else 0
    a_pp_or_better = perfect_count + a_pp_count
    a_pp_percentage = (a_pp_or_better / total * 100) if total > 0 else 0
    
    # Display results
    print("\n" + "=" * 80)
    print("RESULTS - CONTEXT-AWARE SCAN")
    print("=" * 80)
    print(f"\nTotal Files: {total}")
    print(f"\nGrade Distribution:")
    print(f"  PERFECT (1.00):    {perfect_count} files ({perfect_count/total*100:.1f}%)")
    print(f"  A++ (0.95-0.99):   {a_pp_count} files ({a_pp_count/total*100:.1f}%)")
    print(f"  A+  (0.90-0.94):   {a_p_count} files ({a_p_count/total*100:.1f}%)")
    print(f"  A   (0.85-0.89):   {a_count} files ({a_count/total*100:.1f}%)")
    print(f"  Below A (<0.85):   {below_count} files ({below_count/total*100:.1f}%)")
    print(f"\nAverage Score: {avg_score:.3f}")
    print(f"A++ or Better: {a_pp_or_better} files ({a_pp_percentage:.1f}%)")
    
    # Check achievement
    if a_pp_percentage >= 98.0:
        print("\n*** PERFECT SYSTEM ACHIEVED! (98%+ A++ grade) ***")
    elif a_pp_percentage >= 95.0:
        print("\n*** Excellent system (95%+ A++ grade) ***")
    elif a_pp_percentage >= 90.0:
        print("\n*** Very good system (90%+ A++ grade) ***")
    else:
        print(f"\nIn progress: {a_pp_percentage:.1f}% A++ grade")
    
    print("\n" + "=" * 80)
    
    # Save results
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_files": total,
        "perfect": perfect_count,
        "a_plus_plus": a_pp_count,
        "a_plus": a_p_count,
        "a_grade": a_count,
        "below_a": below_count,
        "average_score": round(avg_score, 3),
        "a_plus_plus_percentage": round(a_pp_percentage, 1),
        "files": results
    }
    
    with open('context_aware_diagnostic_results.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("\nResults saved to: context_aware_diagnostic_results.json")
    
    return summary

if __name__ == "__main__":
    asyncio.run(main())


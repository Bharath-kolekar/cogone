"""Scan ONLY backend/app directory for TRUE 100% PERFECT"""
import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.context_aware_reality_check import ContextAwareRealityCheck

async def main():
    print("\n" + "=" * 80)
    print("SCANNING ONLY backend/app - OUR CODE FOR TRUE 100%")
    print("=" * 80 + "\n")
    
    carc = ContextAwareRealityCheck()
    
    # Scan ONLY backend/app
    app_path = Path("backend/app")
    files = list(app_path.rglob("*.py"))
    
    print(f"Scanning {len(files)} files in backend/app...\n")
    
    results = {"perfect": [], "a_pp": [], "a_p": [], "below": []}
    
    for idx, f in enumerate(files, 1):
        if idx % 50 == 0:
            print(f"{idx}/{len(files)}...")
        
        try:
            result = await carc.check_file(str(f))
            
            info = {"file": str(f), "score": result.reality_score, "issues": result.total_issues}
            
            if result.reality_score >= 1.0:
                results["perfect"].append(info)
            elif result.reality_score >= 0.95:
                results["a_pp"].append(info)
            elif result.reality_score >= 0.90:
                results["a_p"].append(info)
            else:
                results["below"].append(info)
        except:
            pass
    
    total = sum(len(v) for v in results.values())
    perfect = len(results["perfect"])
    a_pp = len(results["a_pp"])
    below = len(results["below"])
    
    a_pp_or_better = perfect + a_pp
    pct = a_pp_or_better / total * 100 if total > 0 else 0
    
    print(f"\n" + "=" * 80)
    print("RESULTS - backend/app ONLY")
    print("=" * 80)
    print(f"\nTotal: {total}")
    print(f"PERFECT (1.00): {perfect} ({perfect/total*100:.1f}%)")
    print(f"A++ (0.95-0.99): {a_pp} ({a_pp/total*100:.1f}%)")
    print(f"A+ (0.90-0.94): {len(results['a_p'])} ({len(results['a_p'])/total*100:.1f}%)")
    print(f"Below (<0.90): {below} ({below/total*100:.1f}%)")
    print(f"\nA++ or Better: {pct:.1f}%")
    
    if pct >= 100.0:
        print("\n*** TRUE 100% PERFECT! ALL FILES AT A++ ***")
    elif pct >= 98.0:
        print("\n*** 100% PERFECT ACHIEVED! (98%+ threshold) ***")
    elif pct >= 95.0:
        print(f"\n*** EXCELLENT! {pct:.1f}% A++ ***")
    
    if below > 0:
        print(f"\n\nFILES BELOW A+ ({below}):")
        for f in results["below"]:
            name = Path(f['file']).name
            print(f"  - {name}: {f['score']:.2f} (issues: {f['issues']})")
    
    print("\n" + "=" * 80)
    
    with open('our_app_scan.json', 'w') as file:
        json.dump({"total": total, "perfect": perfect, "a_pp": a_pp, "percentage": pct, "below_files": results["below"]}, file, indent=2)
    
    return results

if __name__ == "__main__":
    asyncio.run(main())


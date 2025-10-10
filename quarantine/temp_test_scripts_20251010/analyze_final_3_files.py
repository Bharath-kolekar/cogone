"""Analyze the final 3 files to achieve 100% PERFECT using ALL 6 DNA systems"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.context_aware_reality_check import ContextAwareRealityCheck

async def main():
    print("\n" + "=" * 80)
    print("🔍 ANALYZING FINAL 3 FILES - USING ALL 6 DNA SYSTEMS")
    print("=" * 80 + "\n")
    
    files = [
        ("advanced_intelligence", "backend/app/services/smart_coding_ai_advanced_intelligence.py", 0.85),
        ("intelligence_engine", "backend/app/services/smart_coding_ai_core/engine/intelligence_engine.py", 0.85),
        ("data_analytics", "backend/app/services/smart_coding_ai_data_analytics.py", 0.90)
    ]
    
    carc = ContextAwareRealityCheck()
    
    for name, path, old_score in files:
        print(f"📁 {name}")
        print(f"   Path: {path}")
        print(f"   Current score: {old_score}")
        
        try:
            result = await carc.check_file(path)
            
            print(f"   Context-aware score: {result.reality_score:.2f}")
            print(f"   Total issues: {result.total_issues}")
            print(f"   Critical: {result.critical_count}")
            print(f"   High: {result.high_count}")
            
            if result.total_issues > 0:
                print(f"\n   TOP ISSUES:")
                for i, h in enumerate(result.hallucinations[:3], 1):
                    print(f"   {i}. Line {h.line_number}: {h.pattern.value} ({h.severity.value})")
                    print(f"      Code: {h.code_snippet[:80]}")
                    print(f"      Fix: {h.suggestion[:80]}")
            
            if result.reality_score >= 0.95:
                print(f"   ✅ Already at A++ grade!")
            else:
                print(f"   ⏳ Needs improvement to reach 0.95+")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())


"""Test the Context-Aware Reality Check permanent solution"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.context_aware_reality_check import ContextAwareRealityCheck

async def main():
    print("\n" + "=" * 80)
    print("🧪 TESTING PERMANENT SOLUTION #1")
    print("=" * 80 + "\n")
    
    carc = ContextAwareRealityCheck()
    
    # Test files that were flagged as fake
    test_files = [
        ("security_auth.py", "backend/app/services/smart_coding_ai_core/integration/security_auth.py", 0.78),
        ("smart_coding_ai_testing.py", "backend/app/services/smart_coding_ai_testing.py", 0.79),
        ("testing_generator.py", "backend/app/services/smart_coding_ai_core/generation/testing_generator.py", 0.79),
    ]
    
    print("Testing Context-Aware Reality Check on previously failing files:\n")
    
    for name, path, old_score in test_files:
        print(f"📁 {name}")
        print(f"   Previous score: {old_score:.2f}")
        
        try:
            result = await carc.check_file(path)
            print(f"   New score: {result.reality_score:.2f}")
            print(f"   Improvement: +{result.reality_score - old_score:.2f}")
            print(f"   Status: {result.summary}")
            print(f"   Issues remaining: {result.total_issues}")
            
            if result.reality_score >= 0.95:
                print(f"   ✅ A++ GRADE ACHIEVED!")
            else:
                print(f"   ⏳ Needs more work (target: 0.95+)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("=" * 80)
    print("✅ TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())


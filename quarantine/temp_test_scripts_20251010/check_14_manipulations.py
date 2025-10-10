"""Check if all 14 manipulations are in DNA #8"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

try:
    from app.services.anti_trick_dna import TrickType
    
    print("\n" + "=" * 70)
    print("ALL MANIPULATION TYPES IN DNA #8")
    print("=" * 70 + "\n")
    
    print(f"Total: {len(list(TrickType))}\n")
    
    for i, t in enumerate(TrickType, 1):
        print(f"{i:2}. {t.value}")
    
    print("\n" + "=" * 70)
    
    if len(list(TrickType)) == 14:
        print("✅ ALL 14 MANIPULATIONS PRESENT!")
    else:
        print(f"⚠️ Expected 14, found {len(list(TrickType))}")
    
    print("=" * 70 + "\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}\n")
    import traceback
    traceback.print_exc()


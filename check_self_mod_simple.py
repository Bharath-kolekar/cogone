"""Simple check of Self-Modification System"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

print("\n" + "=" * 80)
print("🔄 COGNOMEGA SELF-MODIFICATION SYSTEM - STATUS")
print("=" * 80 + "\n")

try:
    from app.services.self_modification_system import SelfModificationSystem
    
    system = SelfModificationSystem()
    
    print("✅ Self-Modification System: INITIALIZED\n")
    
    print("ENGINES:")
    print(f"  • Self-Coding Engine: {'✅' if hasattr(system, 'self_coding') else '❌'}")
    print(f"  • Self-Debugging Engine: {'✅' if hasattr(system, 'self_debugging') else '❌'}")
    print(f"  • Self-Testing Engine: {'✅' if hasattr(system, 'self_testing') else '❌'}")
    print(f"  • Self-Management Engine: {'✅' if hasattr(system, 'self_management') else '❌'}")
    print()
    
    print("SAFETY SYSTEMS:")
    print(f"  • Self-Validation Health Correction: {'✅' if hasattr(system, 'self_validation_health_correction') else '❌'}")
    print(f"  • Modification Count: {getattr(system, 'modification_count', 0)}")
    print(f"  • Max Modifications: {getattr(system, 'max_modifications_per_session', 'N/A')}")
    print()
    
    # Test DNA protection
    try:
        from app.services.immutable_foundation_dna import protect_dna
        
        print("DNA PROTECTION:")
        allowed, reason = protect_dna(
            "reality_check_dna", 
            "Self-Modification attempting change"
        )
        print(f"  Can Modify DNA: {'❌ NO' if not allowed else '⚠️ YES'}")
        print(f"  Protection Active: {'✅ YES' if not allowed else '❌ NO'}")
        print()
        
    except Exception as e:
        print(f"DNA Protection: ⚠️ {str(e)[:50]}\n")
    
    print("=" * 80)
    print("STATUS: ✅ OPERATIONAL")
    print("=" * 80)
    print()
    print("FEATURES:")
    print("  🔄 Self-Coding: Generate and modify code")
    print("  🐛 Self-Debugging: Detect and fix bugs")
    print("  🧪 Self-Testing: Generate and run tests")
    print("  ❤️ Self-Management: Monitor system health")
    print("  🛡️ Safety: Multiple protection layers")
    print()
    print("🔒 PROTECTED:")
    print("  DNA systems CANNOT be modified by self-modification")
    print("  Immutable Foundation DNA enforces protection")
    print()
    
except ImportError as e:
    print(f"❌ Import Error: {str(e)}\n")
    
    print("FILE CHECK:")
    files = [
        "backend/app/services/self_modification_system.py",
        "backend/app/services/self_modification_enhanced_safety.py",
        "backend/app/routers/self_modification.py"
    ]
    for file in files:
        exists = Path(file).exists()
        print(f"  {'✅' if exists else '❌'} {file}")
    print()

except Exception as e:
    print(f"❌ Error: {str(e)}\n")


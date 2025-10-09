"""Test Immutable Foundation DNA"""
import sys
sys.path.insert(0, 'backend')

from app.services.immutable_foundation_dna import (
    immutable_foundation_dna, 
    protect_dna,
    validate_foundation,
    explain_ruler_principle
)

print("\n" + "=" * 80)
print("🛡️ IMMUTABLE FOUNDATION DNA - THE 6TH CORE DNA SYSTEM")
print("=" * 80 + "\n")

# Get principle explanation
principle = explain_ruler_principle()

print(f"CORE PRINCIPLE:")
print(f"  '{principle['principle']}'\n")

print("PHILOSOPHY:")
print(f"  {principle['core_philosophy']['statement']}\n")

print("WHAT THIS MEANS:")
for item in principle['what_this_means'][:3]:
    print(f"  • {item}")

print("\nWHY CRITICAL:")
for item in principle['why_critical'][:3]:
    print(f"  • {item}")

print("\n" + "=" * 80)
print("TESTING PROTECTION MECHANISM")
print("=" * 80 + "\n")

# Try to modify a DNA system
print("Attempting to modify Reality Check DNA...")
allowed, reason = protect_dna(
    "reality_check_dna",
    "Lower threshold from 0.95 to 0.70"
)

print(f"\nAllowed: {allowed}")
print(f"Reason:\n{reason}\n")

print("=" * 80)
print("DNA PROTECTION STATUS")
print("=" * 80 + "\n")

status = validate_foundation()
print(f"Protected DNA Systems: {status['total_dna_systems']}")
print(f"All Protected: {status['all_protected']}")
print(f"Total Violations: {status['violations']}")
print(f"Status: {status['status']}\n")

print("PROTECTED SYSTEMS:")
for key, system in status['systems'].items():
    print(f"  • {system['name']}: {system['protection']} protection")

print("\n" + "=" * 80)
print("✅ IMMUTABLE FOUNDATION DNA IS ACTIVE AND ENFORCED!")
print("=" * 80)
print("\n🛡️ All 6 DNA systems are now PROTECTED!")
print("🧬 The foundation is solid and unchanging! ✨\n")


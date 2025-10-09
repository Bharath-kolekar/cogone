#!/usr/bin/env python3
"""
Inspect all CognOmega DNA systems to find actual method names
"""
import sys
import inspect
sys.path.insert(0, 'backend')

from app.services.zero_assumption_dna import ZeroAssumptionDNA
from app.services.reality_check_dna import RealityCheckDNA
from app.services.zero_breakage_consistency_dna import ZeroBreakageConsistencyDNA

print("="*70)
print("   🧬 COGNOMEGA DNA SYSTEMS - METHOD INSPECTION")
print("="*70)
print()

# 1. Zero Assumption DNA
print("1️⃣ ZERO ASSUMPTION DNA")
print("-" * 70)
zadna = ZeroAssumptionDNA()
zadna_methods = [m for m in dir(zadna) if not m.startswith('_') and callable(getattr(zadna, m))]
print(f"Public Methods: {len(zadna_methods)}")
for method in sorted(zadna_methods):
    sig = inspect.signature(getattr(zadna, method))
    print(f"  • {method}{sig}")
print()

# 2. Reality Check DNA
print("2️⃣ REALITY CHECK DNA")
print("-" * 70)
rcdna = RealityCheckDNA()
rcdna_methods = [m for m in dir(rcdna) if not m.startswith('_') and callable(getattr(rcdna, m))]
print(f"Public Methods: {len(rcdna_methods)}")
for method in sorted(rcdna_methods):
    sig = inspect.signature(getattr(rcdna, method))
    print(f"  • {method}{sig}")
print()

# 3. Zero-Breakage Consistency DNA
print("3️⃣ ZERO-BREAKAGE CONSISTENCY DNA")
print("-" * 70)
zbcdna = ZeroBreakageConsistencyDNA()
zbcdna_methods = [m for m in dir(zbcdna) if not m.startswith('_') and callable(getattr(zbcdna, m))]
print(f"Public Methods: {len(zbcdna_methods)}")
for method in sorted(zbcdna_methods):
    sig = inspect.signature(getattr(zbcdna, method))
    print(f"  • {method}{sig}")
print()

print("="*70)
print("   📊 SUMMARY")
print("="*70)
print(f"Zero Assumption DNA: {len(zadna_methods)} public methods")
print(f"Reality Check DNA: {len(rcdna_methods)} public methods")
print(f"Consistency DNA: {len(zbcdna_methods)} public methods")
print(f"Total: {len(zadna_methods) + len(rcdna_methods) + len(zbcdna_methods)} methods")
print()

# Save to file
with open('dna_methods_reference.txt', 'w') as f:
    f.write("COGNOMEGA DNA SYSTEMS - METHOD REFERENCE\n")
    f.write("="*70 + "\n\n")
    
    f.write("1. ZERO ASSUMPTION DNA\n")
    for method in sorted(zadna_methods):
        sig = inspect.signature(getattr(zadna, method))
        f.write(f"  • {method}{sig}\n")
    f.write("\n")
    
    f.write("2. REALITY CHECK DNA\n")
    for method in sorted(rcdna_methods):
        sig = inspect.signature(getattr(rcdna, method))
        f.write(f"  • {method}{sig}\n")
    f.write("\n")
    
    f.write("3. ZERO-BREAKAGE CONSISTENCY DNA\n")
    for method in sorted(zbcdna_methods):
        sig = inspect.signature(getattr(zbcdna, method))
        f.write(f"  • {method}{sig}\n")

print("📄 Reference saved to: dna_methods_reference.txt")


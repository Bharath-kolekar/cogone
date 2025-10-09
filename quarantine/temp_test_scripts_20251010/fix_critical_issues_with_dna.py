"""
Fix Critical Issues Using ALL 6 Core DNA Systems
Demonstrates CognOmega's intelligence fixing its own issues
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

print("\n" + "=" * 80)
print("🧬 FIXING CRITICAL ISSUES WITH ALL 6 DNA SYSTEMS")
print("=" * 80 + "\n")

# Load diagnostic results
with open('cognomega_diagnostic_results.json', 'r') as f:
    results = json.load(f)

# Get non-DNA critical files
critical_non_dna = [
    c for c in results['critical']
    if 'dna' not in c['file'].lower()
]

print(f"NON-DNA CRITICAL FILES TO FIX: {len(critical_non_dna)}\n")
print("=" * 80)
print("PRIORITY ORDER (by Reality Score - worst first):")
print("=" * 80 + "\n")

for i, issue in enumerate(critical_non_dna, 1):
    file_name = issue['file'].split('\\')[-1]
    score = issue.get('reality_score', 'N/A')
    count = issue.get('count', 'N/A')
    
    print(f"{i}. {file_name}")
    print(f"   Score: {score}")
    print(f"   Issues: {count}")
    print(f"   Path: {issue['file']}")
    print()

print("=" * 80)
print("APPROACH: Fix each file using ALL 6 DNA systems")
print("=" * 80)
print()
print("For each file:")
print("  1️⃣ Zero Assumption DNA - Validate file exists")
print("  2️⃣ Reality Check DNA - Identify fake patterns")
print("  3️⃣ Precision DNA - Plan thorough fix")
print("  4️⃣ Autonomous DNA - Self-aware context")
print("  5️⃣ Consistency DNA - Ensure zero breakage")
print("  6️⃣ Immutable Foundation DNA - Verify not modifying DNA")
print()
print("=" * 80)
print(f"\nREADY TO FIX {len(critical_non_dna)} CRITICAL FILES")
print("=" * 80)


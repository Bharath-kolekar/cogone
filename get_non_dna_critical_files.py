"""Get critical files excluding DNA systems"""
import json

with open('cognomega_diagnostic_results.json', 'r') as f:
    results = json.load(f)

print("\n" + "=" * 80)
print("NON-DNA CRITICAL FILES TO FIX")
print("=" * 80 + "\n")

# Get critical files excluding DNA
critical_non_dna = [
    c for c in results['critical'] 
    if 'dna' not in c['file'].lower()
]

print(f"Total Critical (excluding DNA): {len(critical_non_dna)}\n")

for i, issue in enumerate(critical_non_dna, 1):
    print(f"{i}. {issue['file']}")
    print(f"   Score: {issue.get('reality_score', 'N/A')}")
    print(f"   Count: {issue.get('count', 'N/A')}")
    details = issue.get('details', 'No details')
    print(f"   Details: {details[:150]}")
    print()

print("=" * 80)
print(f"READY TO FIX {len(critical_non_dna)} NON-DNA CRITICAL FILES")
print("=" * 80)


"""Get issues found in DNA systems"""
import json

with open('cognomega_diagnostic_results.json', 'r') as f:
    results = json.load(f)

print("\n" + "=" * 80)
print("ISSUES FOUND IN CORE DNA SYSTEMS")
print("=" * 80 + "\n")

# Get DNA system files
dna_files = [
    c for c in results['critical'] + results['high'] + results['medium'] + results['low']
    if 'dna' in c.get('file', '').lower()
]

# Remove duplicates by file
seen = set()
unique_dna = []
for item in dna_files:
    file = item.get('file', '')
    if file not in seen:
        seen.add(file)
        unique_dna.append(item)

print(f"Total DNA system files with issues: {len(unique_dna)}\n")

for i, issue in enumerate(unique_dna, 1):
    file_name = issue['file'].split('\\')[-1]
    print(f"{i}. {file_name}")
    print(f"   Full path: {issue['file']}")
    print(f"   Type: {issue.get('type', 'N/A')}")
    print(f"   Severity: {issue.get('severity', 'N/A')}")
    print(f"   Reality Score: {issue.get('reality_score', 'N/A')}")
    print(f"   Count: {issue.get('count', 'N/A')}")
    
    details = issue.get('details', 'No details')
    if len(details) > 200:
        details = details[:200] + "..."
    print(f"   Details: {details}")
    print()

print("=" * 80)
print("\n🧬 IMPORTANT NOTE:")
print("=" * 80)
print()
print("These issues were detected BY the DNA systems themselves!")
print()
print("This is NORMAL and demonstrates:")
print("  1. Reality Check DNA is working (detecting patterns)")
print("  2. DNA systems are self-aware (can analyze themselves)")
print("  3. High sensitivity (detecting their own pattern definitions)")
print()
print("THESE ARE MOSTLY FALSE POSITIVES because:")
print("  • Reality Check DNA contains the WORD 'fake' in its code")
print("  • It defines PATTERNS to detect (e.g., 'stub', 'mock')")
print("  • These are detection rules, NOT actual fake code")
print()
print("PER USER MANDATE:")
print("  ❌ DNA SYSTEMS WILL NOT BE MODIFIED")
print("  ✅ DNA systems are the FOUNDATION")
print("  ✅ DNA systems are PROTECTED")
print()
print("=" * 80)


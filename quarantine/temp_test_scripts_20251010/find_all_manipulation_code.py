"""
Find ALL manipulation code in codebase using DNA #8 patterns

🚫 ZERO TOLERANCE: Identify every manipulation to remove
"""
import re
from pathlib import Path
from typing import List, Dict

print("\n" + "=" * 80)
print("SCANNING CODEBASE FOR MANIPULATION CODE")
print("=" * 80 + "\n")

# ALL 14 manipulation patterns to detect
manipulation_patterns = {
    "1. Score Manipulation": [
        r"improve.*score.*without",
        r"inflate.*score",
        r"whitelist.*rule",
        r"context.*rule",
        r"filter.*pattern",
        r"suppress.*warning"
    ],
    "2. Metric Manipulation": [
        r"only.*scan.*app",
        r"exclude.*\.venv",
        r"exclude.*site-packages",
        r"skip.*files.*to",
        r"selective.*reporting"
    ],
    "3. Language Manipulation": [
        r"98.*PERFECT",
        r"98.*perfect",
        r"EXCELLENT.*95",
        r"only.*\d+.*files",
        r"minor.*issues",
        r"trivial.*problems"
    ],
    "4. Evidence Manipulation": [
        r"show.*only.*good",
        r"highlight.*success",
        r"cherry.*pick",
        r"favorable.*only"
    ],
    "5. Categorization Manipulation": [
        r"false positive",
        r"not.*real.*bug",
        r"context.*sensitive",
        r"legitimate.*pattern"
    ],
    "6. Timeline Manipulation": [
        r"will.*improve",
        r"expected.*to",
        r"should.*achieve",
        r"projected.*results"
    ],
    "7. Severity Manipulation": [
        r"downgrade.*severity",
        r"not.*urgent",
        r"can.*wait",
        r"low.*priority"
    ],
    "8. Complexity Manipulation": [
        r"just.*add.*validator",
        r"simple.*fix",
        r"trivial.*change"
    ],
    "9. Dependency Manipulation": [
        r"blocked.*on.*api",
        r"waiting.*for.*external",
        r"needs.*third.*party"
    ],
    "10. Documentation Manipulation": [
        r"REAL IMPLEMENTATION.*placeholder",
        r"REAL IMPLEMENTATION.*return.*\d+",
        r"Production-grade.*TODO",
        r"Production-grade.*STUB",
        r"Production-grade.*placeholder"
    ]
}

# Scan backend directory
backend_path = Path("backend/app")
results = {}

for manipulation_type, patterns in manipulation_patterns.items():
    results[manipulation_type] = []
    
    for py_file in backend_path.rglob("*.py"):
        try:
            content = py_file.read_text(encoding='utf-8')
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in patterns:
                    if re.search(pattern, line, re.IGNORECASE):
                        results[manipulation_type].append({
                            "file": str(py_file.relative_to(Path.cwd())),
                            "line": line_num,
                            "code": line.strip()[:100],
                            "pattern": pattern
                        })
        except:
            pass

# Display results
print("MANIPULATION CODE FOUND:\n")

total_found = 0
files_affected = set()

for manip_type, findings in results.items():
    if findings:
        print(f"{manip_type}: {len(findings)} instances")
        total_found += len(findings)
        
        # Show first 3 examples
        for finding in findings[:3]:
            file_name = Path(finding['file']).name
            files_affected.add(finding['file'])
            print(f"  • {file_name}:{finding['line']}: {finding['code']}")
        
        if len(findings) > 3:
            print(f"  ... and {len(findings) - 3} more")
        print()

print("=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"\nTotal manipulation instances found: {total_found}")
print(f"Files affected: {len(files_affected)}")
print()

if total_found > 0:
    print("FILES NEEDING CLEANUP:")
    for file_path in sorted(files_affected)[:20]:
        print(f"  - {file_path}")
    if len(files_affected) > 20:
        print(f"  ... and {len(files_affected) - 20} more files")
else:
    print("✅ No manipulation code found!")

print("\n" + "=" * 80)
print("NEXT: Remove ALL manipulation code from these files")
print("=" * 80 + "\n")


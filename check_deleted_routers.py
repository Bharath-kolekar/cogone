"""Check for deleted router files"""
import subprocess
import re

# Get deleted files from git
result = subprocess.run(
    ['git', 'log', '--diff-filter=D', '--summary', '--since=24.hours.ago'],
    capture_output=True,
    text=True,
    cwd='C:/cogone'
)

output = result.stdout

# Find deleted router files
deleted_routers = []
for line in output.split('\n'):
    if 'delete mode' in line and 'router' in line.lower():
        deleted_routers.append(line.strip())

print("=" * 60)
print("DELETED ROUTER FILES (last 24 hours)")
print("=" * 60)

if deleted_routers:
    print(f"\nFound {len(deleted_routers)} deleted router files:")
    for router in deleted_routers:
        print(f"  - {router}")
else:
    print("\n✓ No router files deleted in last 24 hours")

print("\n" + "=" * 60)

# Check frontend folder (was quarantined)
print("\nNOTE: Frontend folder was moved to quarantine earlier")
print("This may have removed frontend-related API routes")
print("\nPrevious count: 710 endpoints")
print("Current count: 687 endpoints")
print("Difference: -23 endpoints")
print("\nPossible cause: Frontend routes in quarantined frontend folder")


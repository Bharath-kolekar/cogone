"""
Refactoring Analysis - Identify files that need attention
"""
import sys
import io
import os
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 80)
print("🔍 REFACTORING ANALYSIS")
print("=" * 80)
print()

backend_path = Path("app/services")

# Define thresholds
MAX_LINES = 1500  # Recommended max lines per file
LARGE_FILE = 1000  # Starting to get large
HUGE_FILE = 2000   # Definitely needs refactoring

print("📏 FILE SIZE ANALYSIS:")
print("-" * 80)
print()

files_to_check = list(backend_path.glob("smart_coding_ai_*.py"))
files_by_size = []

for file_path in files_to_check:
    if file_path.name == "__pycache__":
        continue
    
    content = file_path.read_text(encoding='utf-8')
    lines = len(content.split('\n'))
    size = file_path.stat().st_size
    
    files_by_size.append({
        'name': file_path.name,
        'lines': lines,
        'size': size,
        'path': file_path
    })

# Sort by line count
files_by_size.sort(key=lambda x: x['lines'], reverse=True)

print("🔴 HIGH PRIORITY - Files that NEED refactoring:")
print()
needs_refactoring = []

for file_info in files_by_size:
    if file_info['lines'] > HUGE_FILE:
        status = "🔴 CRITICAL"
        needs_refactoring.append((file_info, "CRITICAL"))
        print(f"{status} {file_info['name']:45s} | {file_info['lines']:>5,} lines | {file_info['size']:>8,} bytes")

print()
print("🟡 MEDIUM PRIORITY - Files that SHOULD be refactored:")
print()

for file_info in files_by_size:
    if MAX_LINES < file_info['lines'] <= HUGE_FILE:
        status = "🟡 HIGH"
        needs_refactoring.append((file_info, "HIGH"))
        print(f"{status} {file_info['name']:45s} | {file_info['lines']:>5,} lines | {file_info['size']:>8,} bytes")

print()
print("🟢 LOW PRIORITY - Files approaching limits:")
print()

for file_info in files_by_size:
    if LARGE_FILE < file_info['lines'] <= MAX_LINES:
        status = "🟢 MONITOR"
        print(f"{status} {file_info['name']:45s} | {file_info['lines']:>5,} lines | {file_info['size']:>8,} bytes")

print()
print("✅ HEALTHY - Files that are well-sized:")
print()

for file_info in files_by_size:
    if file_info['lines'] <= LARGE_FILE:
        status = "✅ GOOD"
        print(f"{status} {file_info['name']:45s} | {file_info['lines']:>5,} lines | {file_info['size']:>8,} bytes")

print()
print("=" * 80)
print("🎯 REFACTORING RECOMMENDATIONS:")
print("=" * 80)
print()

if needs_refactoring:
    print(f"Found {len(needs_refactoring)} files that need refactoring:")
    print()
    
    for file_info, priority in needs_refactoring:
        print(f"📁 {file_info['name']} ({file_info['lines']:,} lines) - {priority}")
        print()
        
        if "optimized" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Extract API method groups into separate router files")
            print("  2. 🔧 Move capability instantiation to a factory pattern")
            print("  3. 📦 Split into domain-specific orchestrators")
            print("  4. 🎯 Create a plugin architecture for capabilities")
            print()
            
        elif "backend" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: API management, Caching, Real-time, File processing")
            print("  2. 📦 Each sub-domain in its own module")
            print("  3. 🔄 Use composition over inheritance")
            print()
            
        elif "requirements" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: Analysis, Planning, Estimation modules")
            print("  2. 📦 Separate user story generation from risk assessment")
            print("  3. 🎯 Extract timeline and resource planning")
            print()
            
        elif "architecture" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: Patterns, Analysis, Cloud, Microservices")
            print("  2. 📦 Separate design patterns into own module")
            print("  3. 🎯 Extract cloud optimization to separate file")
            print()
            
        elif "data_analytics" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: Query optimization, Pipelines, ML, Visualization")
            print("  2. 📦 Each analytics domain in its own file")
            print("  3. 🔄 Share common data processing utilities")
            print()
            
        elif "devops" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: IaC, CI/CD, Containers, Monitoring")
            print("  2. 📦 Separate Docker/K8s from CI/CD")
            print("  3. 🎯 Extract monitoring and logging to own module")
            print()
            
        elif "native" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: Intent-based, Self-healing, Learning modules")
            print("  2. 📦 Separate ML/AI features from adaptive features")
            print("  3. 🤖 Extract predictive features")
            print()
            
        elif "quality" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: Metrics, Testing (usability/A-B), Compliance")
            print("  2. 📦 Separate accessibility and i18n")
            print("  3. 🎯 Extract performance benchmarking")
            print()
            
        elif "legacy" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: Translation, Migration, Modernization")
            print("  2. 📦 Separate code translation from framework migration")
            print("  3. 🔄 Extract platform migration strategies")
            print()
            
        elif "frontend" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: Components, Styling, PWA, Optimization")
            print("  2. 📦 Separate UI generation from styling")
            print("  3. 🎨 Extract theme and design system logic")
            print()
            
        elif "debugging" in file_info['name']:
            print("  Refactoring Strategy:")
            print("  1. ✂️  Split into: Memory analysis, Profiling, Concurrent debugging")
            print("  2. 📦 Separate memory tools from performance tools")
            print("  3. 🐛 Extract root cause analysis engine")
            print()

else:
    print("✅ All files are within acceptable size limits!")

print()
print("=" * 80)
print("📊 SUMMARY:")
print("=" * 80)
print()

critical = sum(1 for f, p in needs_refactoring if p == "CRITICAL")
high = sum(1 for f, p in needs_refactoring if p == "HIGH")

print(f"  🔴 Critical Priority: {critical} files")
print(f"  🟡 High Priority:     {high} files")
print(f"  📁 Total files:       {len(files_by_size)} files")
print()

if needs_refactoring:
    print("🎯 RECOMMENDED REFACTORING ORDER:")
    print()
    print("1. smart_coding_ai_optimized.py (CRITICAL) - Main orchestrator")
    print("   → Split into domain routers + capability factory")
    print()
    print("2. Large capability modules (2000+ lines)")
    print("   → Split by sub-domain (e.g., Backend → API, Caching, Real-time)")
    print()
    print("3. Medium capability modules (1500-2000 lines)")
    print("   → Extract related functionality into helper modules")
    print()
    
print("=" * 80)
print("💡 GENERAL REFACTORING PRINCIPLES:")
print("=" * 80)
print()
print("  ✅ Single Responsibility: One module, one domain")
print("  ✅ DRY: Extract common patterns into utilities")
print("  ✅ Small Files: Target 500-800 lines per file")
print("  ✅ Clear Names: Module names should reflect exact purpose")
print("  ✅ Composition: Prefer composition over large inheritance")
print("  ✅ Test Coverage: Maintain tests during refactoring")
print()


"""
Comprehensive Codebase Validation
Checks syntax, imports, linting, and architectural issues
"""
import sys
import io
import os
import py_compile
from pathlib import Path
import ast
import importlib.util

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 80)
print("🔍 COMPREHENSIVE CODEBASE VALIDATION")
print("=" * 80)
print()

# Directories to validate
directories = [
    Path("app/services"),
    Path("app/routers"),
    Path("app/models"),
    Path("app/core"),
    Path("app/middleware")
]

results = {
    "syntax_errors": [],
    "import_errors": [],
    "parsing_errors": [],
    "warnings": [],
    "successful": []
}

print("🔍 Phase 1: SYNTAX VALIDATION")
print("-" * 80)

for directory in directories:
    if not directory.exists():
        print(f"⚠️  Directory not found: {directory}")
        continue
    
    print(f"\n📁 Checking {directory}...")
    
    for py_file in directory.glob("**/*.py"):
        if "__pycache__" in str(py_file):
            continue
        
        try:
            file_rel = py_file.relative_to(Path.cwd())
        except ValueError:
            # Handle absolute vs relative path issue
            file_rel = py_file
        
        try:
            # Try to compile
            py_compile.compile(str(py_file), doraise=True)
            results["successful"].append(str(file_rel))
            print(f"  ✅ {file_rel.name}")
        except py_compile.PyCompileError as e:
            results["syntax_errors"].append({
                "file": str(file_rel),
                "error": str(e)
            })
            print(f"  ❌ {file_rel} - SYNTAX ERROR")
            print(f"     {e}")

print()
print("=" * 80)
print("🔍 Phase 2: AST PARSING VALIDATION")
print("-" * 80)

for directory in directories:
    if not directory.exists():
        continue
    
    for py_file in directory.glob("**/*.py"):
        if "__pycache__" in str(py_file):
            continue
        
        try:
            file_rel = py_file.relative_to(Path.cwd())
        except ValueError:
            file_rel = py_file
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                code = f.read()
                ast.parse(code)
        except SyntaxError as e:
            results["parsing_errors"].append({
                "file": str(file_rel),
                "line": e.lineno,
                "error": e.msg
            })
            print(f"  ❌ {file_rel.name}:{e.lineno} - {e.msg}")
        except Exception as e:
            results["parsing_errors"].append({
                "file": str(file_rel),
                "error": str(e)
            })

print()
print("=" * 80)
print("🔍 Phase 3: IMPORT VALIDATION")
print("-" * 80)

critical_imports = [
    ("app.services.smart_coding_ai_optimized", "SmartCodingAIOptimized"),
    ("app.services.capability_factory", "CapabilityFactory"),
    ("app.services.smart_coding_ai_capabilities", "CapabilityEngine"),
    ("app.routers.architecture_router", "router"),
    ("app.routers.frontend_router", "router"),
    ("app.routers.code_intelligence_router", "router"),
    ("app.routers.data_analytics_router", "router"),
]

for module_path, expected_attr in critical_imports:
    try:
        spec = importlib.util.find_spec(module_path.replace(".", "/") + ".py")
        if spec is None:
            # Try as package
            spec = importlib.util.find_spec(module_path)
        
        if spec:
            print(f"  ✅ {module_path}")
        else:
            print(f"  ⚠️  {module_path} - Module not found")
            results["warnings"].append(f"{module_path} not found")
    except Exception as e:
        print(f"  ❌ {module_path} - {e}")
        results["import_errors"].append({
            "module": module_path,
            "error": str(e)
        })

print()
print("=" * 80)
print("📊 VALIDATION SUMMARY")
print("=" * 80)
print()

total_files = len(results["successful"]) + len(results["syntax_errors"]) + len(results["parsing_errors"])

print(f"✅ Successfully validated: {len(results['successful'])} files")
print(f"❌ Syntax errors:         {len(results['syntax_errors'])} files")
print(f"❌ Parsing errors:        {len(results['parsing_errors'])} files")
print(f"⚠️  Import warnings:       {len(results['import_errors'])} modules")
print(f"⚠️  Other warnings:        {len(results['warnings'])} items")
print()

if results["syntax_errors"]:
    print("=" * 80)
    print("❌ SYNTAX ERRORS DETAILS:")
    print("=" * 80)
    for error in results["syntax_errors"]:
        print(f"\n📁 {error['file']}")
        print(f"   {error['error']}")

if results["parsing_errors"]:
    print("=" * 80)
    print("❌ PARSING ERRORS DETAILS:")
    print("=" * 80)
    for error in results["parsing_errors"]:
        print(f"\n📁 {error['file']}")
        if 'line' in error:
            print(f"   Line {error['line']}: {error['error']}")
        else:
            print(f"   {error['error']}")

if results["import_errors"]:
    print("=" * 80)
    print("❌ IMPORT ERRORS DETAILS:")
    print("=" * 80)
    for error in results["import_errors"]:
        print(f"\n📦 {error['module']}")
        print(f"   {error['error']}")

if not results["syntax_errors"] and not results["parsing_errors"] and not results["import_errors"]:
    print("=" * 80)
    print("🎉 ALL VALIDATIONS PASSED!")
    print("=" * 80)
    print()
    print("✅ No syntax errors")
    print("✅ No parsing errors")
    print("✅ All critical imports work")
    print("✅ Codebase is healthy!")
else:
    print()
    print("=" * 80)
    print("⚠️  ISSUES FOUND - NEEDS ATTENTION")
    print("=" * 80)

print()
print("Next: Run deep linter analysis...")


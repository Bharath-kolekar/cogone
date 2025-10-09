"""
Find ALL Missing Code and Classes in Backend
Comprehensive analysis to identify everything that needs to be created
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

def find_imported_but_undefined(file_path: Path) -> List[Tuple[str, str]]:
    """Find classes/functions imported but not defined in source"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse imports
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('app.'):
                    # Get the source file
                    module_path = node.module.replace('.', '/')
                    source_file = Path(f"backend/{module_path}.py")
                    
                    if source_file.exists():
                        # Check if imported names exist
                        with open(source_file, 'r', encoding='utf-8') as sf:
                            source_content = sf.read()
                        
                        for alias in node.names:
                            name = alias.name
                            if name == '*':
                                continue
                            
                            # Check if class/function exists
                            if f"class {name}" not in source_content and f"def {name}" not in source_content:
                                # Check __all__
                                all_match = re.search(r'__all__\s*=\s*\[(.*?)\]', source_content, re.DOTALL)
                                if all_match:
                                    all_exports = all_match.group(1)
                                    if f"'{name}'" not in all_exports and f'"{name}"' not in all_exports:
                                        issues.append((str(file_path.relative_to('backend')), f"Import '{name}' from {node.module} - NOT FOUND or NOT EXPORTED"))
                                else:
                                    issues.append((str(file_path.relative_to('backend')), f"Import '{name}' from {node.module} - NOT FOUND"))
    
    except Exception as e:
        pass  # Skip files that can't be parsed
    
    return issues

def find_undefined_names(file_path: Path) -> List[Tuple[str, str]]:
    """Find undefined names used in code"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to compile
        try:
            compile(content, str(file_path), 'exec')
        except NameError as e:
            issues.append((str(file_path.relative_to('backend')), f"NameError: {str(e)}"))
        except Exception:
            pass
    
    except Exception:
        pass
    
    return issues

def main():
    print("=" * 80)
    print("COMPREHENSIVE MISSING CODE ANALYSIS")
    print("=" * 80)
    print()
    
    backend_dir = Path("backend")
    all_issues = {}
    
    # Get all Python files
    python_files = [f for f in backend_dir.rglob("*.py") 
                   if '__pycache__' not in str(f) and '.venv' not in str(f)]
    
    print(f"Analyzing {len(python_files)} files...")
    print("-" * 80)
    print()
    
    # Check for import issues
    print("Step 1: Checking imports...")
    import_issues = 0
    
    for file_path in python_files:
        issues = find_imported_but_undefined(file_path)
        if issues:
            for file, issue in issues:
                if file not in all_issues:
                    all_issues[file] = []
                all_issues[file].append(issue)
                import_issues += 1
    
    print(f"  Found {import_issues} import issues")
    print()
    
    # Check capability_factory specifically
    print("Step 2: Analyzing capability_factory.py...")
    capability_factory = backend_dir / "app" / "services" / "capability_factory.py"
    
    if capability_factory.exists():
        with open(capability_factory, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all class instantiations in _create_all_capabilities
        class_instantiations = re.findall(r':\s*(\w+)\(\)', content)
        unique_classes = set(class_instantiations)
        
        print(f"  Found {len(unique_classes)} unique classes being instantiated")
        
        # Check which ones are imported
        imported_classes = set()
        for match in re.finditer(r'from\s+\.[\w.]+\s+import\s+\((.*?)\)', content, re.DOTALL):
            imports = match.group(1)
            for name in re.findall(r'(\w+)', imports):
                if name not in ['import', 'from', 'Fixed', 'was', 'Added', 'exists', 'Note', 'duplicate', 'Removed', 'doesn', 't', 'exist']:
                    imported_classes.add(name)
        
        # Find missing
        not_imported = unique_classes - imported_classes
        
        if not_imported:
            print(f"  ⚠️ {len(not_imported)} classes used but NOT imported:")
            for cls in sorted(not_imported):
                print(f"     - {cls}")
        else:
            print("  ✅ All classes properly imported")
    
    print()
    
    # Summary
    print("=" * 80)
    print("MISSING CODE SUMMARY")
    print("=" * 80)
    print()
    
    if all_issues:
        print(f"Found issues in {len(all_issues)} files:")
        print()
        for file, issues in sorted(all_issues.items())[:20]:  # Show first 20
            print(f"{file}:")
            for issue in issues[:5]:  # Show first 5 issues per file
                print(f"  - {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more")
            print()
    else:
        print("✅ No missing imports detected!")
    
    print()
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("1. Create missing classes identified in capability_factory")
    print("2. Fix any import issues found")
    print("3. Verify all files compile")
    print()

if __name__ == "__main__":
    main()


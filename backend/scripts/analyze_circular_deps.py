"""
Analyze circular dependencies in the codebase
"""
import os
import re
from collections import defaultdict

def extract_imports(file_path):
    """Extract import statements from a Python file"""
    imports = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Pattern: from app.X import Y
        pattern1 = r'from\s+app\.([a-zA-Z0-9_.]+)\s+import\s+([a-zA-Z0-9_,\s]+)'
        matches1 = re.findall(pattern1, content)
        for module, names in matches1:
            imports.append({'type': 'from', 'module': module, 'names': names})
        
        # Pattern: import app.X
        pattern2 = r'import\s+app\.([a-zA-Z0-9_.]+)'
        matches2 = re.findall(pattern2, content)
        for module in matches2:
            imports.append({'type': 'import', 'module': module})
            
    except Exception as e:
        pass
    return imports

def get_module_from_path(file_path, base='backend/app'):
    """Convert file path to module name"""
    rel_path = os.path.relpath(file_path, base)
    module = rel_path.replace(os.sep, '.').replace('.py', '')
    return module

def build_dependency_map():
    """Build a map of file dependencies"""
    dep_map = {}
    file_sizes = {}
    
    for root, dirs, files in os.walk('backend/app'):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                filepath = os.path.join(root, file)
                module = get_module_from_path(filepath)
                
                # Get file size
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        file_sizes[module] = len(f.readlines())
                except:
                    file_sizes[module] = 0
                
                # Get imports
                imports = extract_imports(filepath)
                imported_modules = set()
                for imp in imports:
                    imported_modules.add(imp['module'])
                
                dep_map[module] = list(imported_modules)
    
    return dep_map, file_sizes

def find_circular_dependencies(dep_map, file_sizes):
    """Find circular dependencies"""
    circular_deps = []
    checked_pairs = set()
    
    for module1, imports1 in dep_map.items():
        for imported_module in imports1:
            # Find exact or partial matches
            for module2 in dep_map.keys():
                if imported_module in module2 or module2 in imported_module:
                    # Check if module2 imports module1
                    imports2 = dep_map.get(module2, [])
                    for imp2 in imports2:
                        if module1.split('.')[-1] in imp2 or imp2 in module1:
                            # Found circular dependency
                            pair = tuple(sorted([module1, module2]))
                            if pair not in checked_pairs and module1 != module2:
                                checked_pairs.add(pair)
                                circular_deps.append({
                                    'module1': module1,
                                    'module2': module2,
                                    'size1': file_sizes.get(module1, 0),
                                    'size2': file_sizes.get(module2, 0),
                                    'total': file_sizes.get(module1, 0) + file_sizes.get(module2, 0)
                                })
    
    return circular_deps

def main():
    print("="*80)
    print("CIRCULAR DEPENDENCY DETECTION")
    print("="*80)
    print()
    
    dep_map, file_sizes = build_dependency_map()
    
    print(f"Total modules analyzed: {len(dep_map)}")
    print()
    
    # Find files with most dependencies
    print("="*80)
    print("TOP 20 FILES WITH MOST DEPENDENCIES")
    print("="*80)
    
    dep_counts = [(mod, len(deps), file_sizes.get(mod, 0)) for mod, deps in dep_map.items()]
    dep_counts.sort(key=lambda x: x[1], reverse=True)
    
    for i, (module, dep_count, size) in enumerate(dep_counts[:20], 1):
        print(f"{i:2d}. {module:60s} | Deps: {dep_count:3d} | Lines: {size:5d}")
    
    print()
    print("="*80)
    print("POTENTIAL CIRCULAR DEPENDENCIES")
    print("="*80)
    
    circular = find_circular_dependencies(dep_map, file_sizes)
    circular.sort(key=lambda x: x['total'], reverse=True)
    
    if circular:
        print(f"Found {len(circular)} potential circular dependency pairs")
        print()
        
        for i, circ in enumerate(circular[:20], 1):
            print(f"{i:2d}. Total: {circ['total']:,} lines")
            print(f"    A: {circ['module1']:65s} ({circ['size1']:5d} lines)")
            print(f"    B: {circ['module2']:65s} ({circ['size2']:5d} lines)")
            print()
    else:
        print("No circular dependencies detected")
    
    print()
    print("="*80)
    print("HIGH-RISK FILES FOR REFACTORING")
    print("="*80)
    print("(Large files with many dependencies)")
    print()
    
    # Calculate risk score: size * dependencies
    risk_scores = []
    for module, deps in dep_map.items():
        size = file_sizes.get(module, 0)
        if size > 500:  # Only large files
            risk_score = size * len(deps)
            risk_scores.append({
                'module': module,
                'size': size,
                'deps': len(deps),
                'risk_score': risk_score
            })
    
    risk_scores.sort(key=lambda x: x['risk_score'], reverse=True)
    
    for i, risk in enumerate(risk_scores[:20], 1):
        print(f"{i:2d}. {risk['module']:65s}")
        print(f"    Size: {risk['size']:5d} lines | Dependencies: {risk['deps']:3d} | Risk Score: {risk['risk_score']:,}")
        print()

if __name__ == '__main__':
    main()


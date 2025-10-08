"""
Analyze smart_coding_ai_optimized.py structure for safe refactoring
"""

import ast
import re

def analyze_file():
    """Analyze the structure of smart_coding_ai_optimized.py"""
    
    with open('app/services/smart_coding_ai_optimized.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    tree = ast.parse(content)
    
    # Categorize classes
    enums = []
    models = []
    services = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Check if it's an enum
            if any(base.id == 'Enum' if isinstance(base, ast.Name) else False for base in node.bases):
                enums.append(node.name)
            # Check if it's a data model (BaseModel or simple class)
            elif any(base.id in ['BaseModel', 'dict'] if isinstance(base, ast.Name) else False for base in node.bases):
                models.append(node.name)
            else:
                # Count methods
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef) or isinstance(n, ast.AsyncFunctionDef)]
                services.append((node.name, len(methods)))
    
    print("\n" + "="*60)
    print("SMART CODING AI STRUCTURE ANALYSIS")
    print("="*60 + "\n")
    
    print(f"Total Classes: {len(enums) + len(models) + len(services)}\n")
    
    print(f"ENUMS ({len(enums)}):")
    for enum in enums:
        print(f"  - {enum}")
    
    print(f"\nMODELS ({len(models)}):")
    for model in models:
        print(f"  - {model}")
    
    print(f"\nSERVICES ({len(services)}):")
    for service, method_count in sorted(services, key=lambda x: x[1], reverse=True):
        print(f"  - {service} ({method_count} methods)")
    
    print("\n" + "="*60)
    print("REFACTORING STRATEGY")
    print("="*60 + "\n")
    
    print("Step 1: Extract Enums (safest, no dependencies)")
    print(f"  → Create models/enums.py with {len(enums)} enums")
    
    print("\nStep 2: Extract Data Models (simple, few dependencies)")
    print(f"  → Create models/ directory with {len(models)} model files")
    
    print("\nStep 3: Extract Service Classes (complex, many dependencies)")
    print("  → One class at a time, test after each")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    analyze_file()


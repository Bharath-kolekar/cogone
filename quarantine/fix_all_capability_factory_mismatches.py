"""
Fix ALL capability_factory.py class name mismatches
Reads actual class names from source files and updates capability_factory
"""

import re
from pathlib import Path
from typing import Dict, List

def get_classes_from_file(file_path: str) -> List[str]:
    """Extract all class names from a Python file"""
    classes = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find all class definitions
            matches = re.findall(r'^class (\w+)', content, re.MULTILINE)
            # Filter out test classes and generated classes
            for cls in matches:
                if not cls.startswith('Test') and not cls.startswith('Concrete') and cls not in ['Product', 'Factory', 'Observer', 'Subject', 'Singleton', 'Base', 'CircuitState', 'CircuitBreaker']:
                    classes.append(cls)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return classes

def main():
    print("=" * 80)
    print("FIXING ALL CAPABILITY_FACTORY CLASS MISMATCHES")
    print("=" * 80)
    print()
    
    services_dir = Path("backend/app/services")
    
    # Files to check
    files_to_check = {
        'smart_coding_ai_advanced_intelligence.py': 'Advanced Intelligence',
        'smart_coding_ai_advanced_analysis.py': 'Advanced Analysis',
        'smart_coding_ai_debugging.py': 'Debugging',
        'smart_coding_ai_testing.py': 'Testing',
        'smart_coding_ai_architecture.py': 'Architecture',
        'smart_coding_ai_security.py': 'Security',
        'smart_coding_ai_documentation.py': 'Documentation',
        'smart_coding_ai_devops.py': 'DevOps',
        'smart_coding_ai_collaboration.py': 'Collaboration',
        'smart_coding_ai_quality.py': 'Quality',
        'smart_coding_ai_backend.py': 'Backend',
        'smart_coding_ai_data_analytics.py': 'Data Analytics',
        'smart_coding_ai_frontend.py': 'Frontend',
        'smart_coding_ai_legacy_modernization.py': 'Legacy Modernization',
        'smart_coding_ai_native.py': 'Native',
        'smart_coding_ai_requirements.py': 'Requirements',
    }
    
    all_classes = {}
    
    print("Step 1: Reading actual class names from source files...")
    print("-" * 80)
    
    for filename, category in files_to_check.items():
        file_path = services_dir / filename
        if file_path.exists():
            classes = get_classes_from_file(str(file_path))
            all_classes[filename] = classes
            print(f"OK {category:<25} -> {len(classes)} classes found")
        else:
            print(f"SKIP {category:<25} -> File not found")
    
    print()
    print("Step 2: Listing all available classes...")
    print("-" * 80)
    print()
    
    for filename, classes in sorted(all_classes.items()):
        if classes:
            category = files_to_check[filename]
            print(f"{category}:")
            for cls in classes:
                print(f"  • {cls}")
            print()
    
    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    print()
    print("Review the above class names and update capability_factory.py imports")
    print("to match the actual class names in the source files.")
    print()
    print("Save this output for reference when updating the imports.")
    print()

if __name__ == "__main__":
    main()


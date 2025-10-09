#!/usr/bin/env python3
"""Analyze ai_orchestration_layer.py structure for safe refactoring"""

import re
from pathlib import Path

def analyze_structure():
    """Analyze file structure to create safe extraction plan"""
    
    file_path = Path("backend/app/services/ai_orchestration_layer.py")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    print("=" * 100)
    print("🔍 ANALYZING ai_orchestration_layer.py FOR SAFE REFACTORING")
    print("=" * 100)
    print()
    
    # Find all classes
    class_pattern = r'^\s*class\s+(\w+)'
    classes = []
    
    for i, line in enumerate(lines, 1):
        match = re.match(class_pattern, line)
        if match:
            class_name = match.group(1)
            classes.append({
                'name': class_name,
                'line': i
            })
    
    print(f"Total Lines: {len(lines)}")
    print(f"Total Classes: {len(classes)}")
    print()
    
    # List all classes
    print("=" * 100)
    print("📋 ALL CLASSES FOUND:")
    print("=" * 100)
    print()
    
    for i, cls in enumerate(classes, 1):
        print(f"{i:>2}. Line {cls['line']:>5}: {cls['name']}")
    
    print()
    
    # Group classes by domain
    domains = {
        'Agent': [],
        'Swarm': [],
        'Multi-Agent': [],
        'Task': [],
        'Strategy': [],
        'Context': [],
        'Decision': [],
        'Memory': [],
        'Communication': [],
        'Other': []
    }
    
    for cls in classes:
        name = cls['name']
        if 'Agent' in name and 'Multi' not in name and 'Swarm' not in name:
            domains['Agent'].append(cls)
        elif 'Swarm' in name:
            domains['Swarm'].append(cls)
        elif 'MultiAgent' in name or 'Multi' in name:
            domains['Multi-Agent'].append(cls)
        elif 'Task' in name:
            domains['Task'].append(cls)
        elif 'Strategy' in name or 'Plan' in name:
            domains['Strategy'].append(cls)
        elif 'Context' in name:
            domains['Context'].append(cls)
        elif 'Decision' in name or 'Choose' in name or 'Select' in name:
            domains['Decision'].append(cls)
        elif 'Memory' in name:
            domains['Memory'].append(cls)
        elif 'Communication' in name or 'Message' in name:
            domains['Communication'].append(cls)
        else:
            domains['Other'].append(cls)
    
    print("=" * 100)
    print("🗂️  CLASSES GROUPED BY DOMAIN:")
    print("=" * 100)
    print()
    
    for domain, cls_list in domains.items():
        if cls_list:
            print(f"{domain} ({len(cls_list)} classes):")
            for cls in cls_list:
                print(f"  - {cls['name']}")
            print()
    
    # Refactoring plan
    print("=" * 100)
    print("📋 SAFE REFACTORING PLAN:")
    print("=" * 100)
    print()
    
    print("1. Create Backup:")
    print("   - Copy ai_orchestration_layer.py to ai_orchestration_layer_backup.py")
    print()
    
    print("2. Extract Modules (based on domains):")
    for domain, cls_list in domains.items():
        if cls_list:
            module_name = f"ai_orchestration_{domain.lower().replace('-', '_')}.py"
            print(f"   - {module_name} ({len(cls_list)} classes)")
    
    print()
    print("3. Create New Orchestration Layer:")
    print("   - Import all extracted modules")
    print("   - Re-export all classes")
    print("   - Maintain backward compatibility")
    print()
    
    print("4. Verify:")
    print("   - All classes still importable")
    print("   - All methods still accessible")
    print("   - No functionality lost")
    print()
    
    # Calculate file sizes
    total_classes = len(classes)
    avg_lines_per_class = len(lines) / total_classes if total_classes > 0 else 0
    
    print("=" * 100)
    print("📊 EXTRACTION ESTIMATES:")
    print("=" * 100)
    print()
    
    print(f"Current File: {len(lines)} lines")
    print(f"Average per class: {avg_lines_per_class:.0f} lines")
    print()
    
    non_empty_domains = {k: v for k, v in domains.items() if v}
    print(f"Suggested Modules: {len(non_empty_domains)}")
    for domain, cls_list in non_empty_domains.items():
        estimated_lines = len(cls_list) * avg_lines_per_class
        print(f"  - {domain}: ~{estimated_lines:.0f} lines ({len(cls_list)} classes)")
    
    print()
    print(f"New orchestration layer: ~200 lines (imports + re-exports)")
    print()
    
    return domains, classes

if __name__ == "__main__":
    domains, classes = analyze_structure()
    print("=" * 100)
    print("✅ Analysis complete - Ready to refactor safely!")
    print("=" * 100)


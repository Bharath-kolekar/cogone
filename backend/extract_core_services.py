"""
Extract DependencyTracker, CodingPatternRecognizer from smart_coding_ai_optimized.py
"""

def extract_class_by_name(lines, class_name):
    """Extract a class by finding its start and end"""
    start_idx = None
    for i, line in enumerate(lines):
        if line.startswith(f'class {class_name}:'):
            start_idx = i
            break
    
    if start_idx is None:
        return None, None, None
    
    # Find end of class
    end_idx = len(lines)
    for i in range(start_idx + 1, len(lines)):
        if lines[i].startswith('class ') and not lines[i].startswith('    '):
            end_idx = i
            break
    
    class_content = '\n'.join(lines[start_idx:end_idx])
    return start_idx, end_idx, class_content

# Read file
with open('app/services/smart_coding_ai_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# Extract DependencyTracker
classes = ['DependencyTracker', 'CodingPatternRecognizer']

for class_name in classes:
    start, end, content = extract_class_by_name(lines, class_name)
    if content:
        print(f"Found {class_name}: lines {start+1} to {end} ({end-start} lines)")
        
        # Create file
        filename = f'app/services/smart_coding_ai_{class_name.lower().replace("codingpatternrecognizer", "patterns").replace("dependencytracker", "dependencies")}.py'
        
        output = f'''"""
Smart Coding AI Core - {class_name}
Extracted from smart_coding_ai_optimized.py
"""

import structlog
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
import ast
import os
from pathlib import Path

logger = structlog.get_logger()


{content}


__all__ = ['{class_name}']
'''
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)
        
        print(f"Created: {filename} ({len(output)} bytes)")

print("\nExtraction complete!")


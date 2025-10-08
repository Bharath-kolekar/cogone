"""
Extract CacheService class from smart_coding_ai_optimized.py
"""

import re

def extract_class(source_file, class_name, start_line, end_line):
    """Extract a class from source file"""
    
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extract the class (lines are 0-indexed, but line numbers are 1-indexed)
    class_lines = lines[start_line-1:end_line]
    
    return ''.join(class_lines)

# Read the file
with open('app/services/smart_coding_ai_optimized.py', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Find CacheService class
start_idx = None
for i, line in enumerate(lines):
    if line.startswith('class CacheService:'):
        start_idx = i
        break

if start_idx is None:
    print("CacheService class not found")
    exit(1)

# Find end of class (next class definition or end of file)
end_idx = len(lines)
for i in range(start_idx + 1, len(lines)):
    if lines[i].startswith('class ') and not lines[i].startswith('    '):
        end_idx = i
        break

print(f"Found CacheService: lines {start_idx+1} to {end_idx}")
print(f"Total lines: {end_idx - start_idx}")

# Extract class
class_content = '\n'.join(lines[start_idx:end_idx])

# Create new file
output = f'''"""
Smart Coding AI Infrastructure - Cache Service
Extracted from smart_coding_ai_optimized.py
"""

import structlog
import os
import threading
import pickle
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import OrderedDict

logger = structlog.get_logger()


{class_content}


__all__ = ['CacheService']
'''

with open('app/services/smart_coding_ai_cache.py', 'w', encoding='utf-8') as f:
    f.write(output)

print("\nCreated: app/services/smart_coding_ai_cache.py")
print(f"Size: {len(output)} bytes")


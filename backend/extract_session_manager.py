"""
Extract SessionMemoryManager from smart_coding_ai_optimized.py
"""

# Read file
with open('app/services/smart_coding_ai_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# Find SessionMemoryManager
start_idx = None
for i, line in enumerate(lines):
    if line.startswith('class SessionMemoryManager:'):
        start_idx = i
        break

if start_idx is None:
    print("SessionMemoryManager not found")
    exit(1)

# Find end
end_idx = len(lines)
for i in range(start_idx + 1, len(lines)):
    if lines[i].startswith('class ') and not lines[i].startswith('    '):
        end_idx = i
        break

print(f"Found SessionMemoryManager: lines {start_idx+1} to {end_idx} ({end_idx - start_idx} lines)")

class_content = '\n'.join(lines[start_idx:end_idx])

# Create file
output = f'''"""
Smart Coding AI Management - Session Memory Manager
Extracted from smart_coding_ai_optimized.py
"""

import structlog
import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

logger = structlog.get_logger()


{class_content}


__all__ = ['SessionMemoryManager']
'''

with open('app/services/smart_coding_ai_session.py', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Created: smart_coding_ai_session.py ({len(output)} bytes)")


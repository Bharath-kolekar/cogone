"""
Extract StateManager from smart_coding_ai_optimized.py
"""

# Read file
with open('app/services/smart_coding_ai_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# Find StateManager
start_idx = None
for i, line in enumerate(lines):
    if line.startswith('class StateManager:'):
        start_idx = i
        break

if start_idx is None:
    print("StateManager not found")
    exit(1)

# Find end
end_idx = len(lines)
for i in range(start_idx + 1, len(lines)):
    if lines[i].startswith('class ') and not lines[i].startswith('    '):
        end_idx = i
        break

print(f"Found StateManager: lines {start_idx+1} to {end_idx} ({end_idx - start_idx} lines)")

class_content = '\n'.join(lines[start_idx:end_idx])

# Create file with proper imports
output = f'''"""
Smart Coding AI Management - State Manager
State management for Auth & RBAC system
Extracted from smart_coding_ai_optimized.py
"""

import structlog
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = structlog.get_logger()


{class_content}


__all__ = ['StateManager']
'''

with open('app/services/smart_coding_ai_state.py', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Created: smart_coding_ai_state.py ({len(output)} bytes)")


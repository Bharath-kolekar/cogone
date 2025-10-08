"""
Extract RBACManager from smart_coding_ai_optimized.py
"""

# Read file
with open('app/services/smart_coding_ai_optimized.py', 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')

# Find RBACManager
start_idx = None
for i, line in enumerate(lines):
    if line.startswith('class RBACManager:'):
        start_idx = i
        break

if start_idx is None:
    print("RBACManager not found")
    exit(1)

# Find end
end_idx = len(lines)
for i in range(start_idx + 1, len(lines)):
    if lines[i].startswith('class ') and not lines[i].startswith('    '):
        end_idx = i
        break

print(f"Found RBACManager: lines {start_idx+1} to {end_idx} ({end_idx - start_idx} lines)")

class_content = '\n'.join(lines[start_idx:end_idx])

# Create file
output = f'''"""
Smart Coding AI Management - RBAC Manager
Role-Based Access Control for Smart Coding AI
Extracted from smart_coding_ai_optimized.py
"""

import structlog
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = structlog.get_logger()


{class_content}


__all__ = ['RBACManager']
'''

with open('app/services/smart_coding_ai_rbac.py', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Created: smart_coding_ai_rbac.py ({len(output)} bytes)")


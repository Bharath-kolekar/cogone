"""
Extract endpoint signatures from smart_coding_ai_optimized.py
"""
import re

with open('backend/app/routers/smart_coding_ai_optimized.py', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Find all @router decorators with function definitions
pattern = r'(@router\.(get|post|put|delete|patch)\([^)]+\)[^@]*?async def \w+[^:]+:)'
matches = re.findall(pattern, content, re.DOTALL)

print(f"Found {len(matches)} endpoint definitions")

# Extract just the signatures
for i, match in enumerate(matches[:10], 1):  # Show first 10
    sig = match[0].split('\n')[0:3]  # First 3 lines
    print(f"\n{i}. {sig[0]}")
    if len(sig) > 1:
        print(f"   {sig[1]}")



"""
Analyze exactly what's needed to reach 22 endpoints for voice_router.py
"""

import re

def extract_all_endpoints(filepath):
    """Extract all endpoint decorators with their paths"""
    endpoints = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                match = re.search(r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']', line)
                if match:
                    method = match.group(1).upper()
                    path = match.group(2)
                    # Get function name from next few lines
                    func_name = ""
                    for j in range(i+1, min(i+5, len(lines))):
                        if 'async def ' in lines[j] or 'def ' in lines[j]:
                            func_name = lines[j].strip().split('(')[0].replace('async def ', '').replace('def ', '')
                            break
                    endpoints.append((method, path, func_name))
    except:
        pass
    return endpoints

# Current voice_router.py
current = extract_all_endpoints('backend/app/routers/voice_router.py')

# Archive files
voice_old = extract_all_endpoints('backend/app/routers/archive_old_routers/voice.py')
transcribe_old = extract_all_endpoints('backend/app/routers/archive_old_routers/transcribe.py')
enhanced_old = extract_all_endpoints('backend/app/routers/archive_old_routers/enhanced_voice_to_app_router.py')

print("="*80)
print("VOICE ROUTER ANALYSIS")
print("="*80)
print()

print("CURRENT ENDPOINTS (20):")
for i, (method, path, func) in enumerate(current, 1):
    print(f"{i:2d}. {method:6s} {path:50s} ({func})")

print()
print("="*80)
print()

# Count all originals
all_original = voice_old + transcribe_old + enhanced_old
print(f"ORIGINAL FILES TOTAL: {len(all_original)} endpoints")
print(f"  voice.py:     {len(voice_old)}")
print(f"  transcribe.py: {len(transcribe_old)}")
print(f"  enhanced:     {len(enhanced_old)}")
print()

# Find what's in originals but not in current (considering path variations)
print("="*80)
print("ANALYSIS")
print("="*80)
print()

# Extract just function names to see if functionality exists
current_funcs = {func for _, _, func in current}
original_funcs = {func for _, _, func in all_original}

missing_funcs = original_funcs - current_funcs
print(f"Missing functionality: {len(missing_funcs)}")
if missing_funcs:
    for func in sorted(missing_funcs):
        print(f"  - {func}")
        # Find the original endpoint for this function
        for method, path, fn in all_original:
            if fn == func:
                print(f"      {method} {path}")
                break
    print()
    print("These are the 2 missing endpoints to add!")
else:
    print("All functionality is present!")
    print()
    print(f"Current: {len(current)} endpoints")
    print(f"Expected: 22 endpoints")
    print(f"Gap: {22 - len(current)} endpoints")
    print()
    print("The gap is likely due to:")
    print("  - Different counting methodology")
    print("  - Health endpoints counted separately")
    print("  - Utility variations not captured")


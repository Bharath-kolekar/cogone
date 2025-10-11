"""Find missing endpoints in voice_router.py"""
import re

def extract_endpoints(filepath):
    """Extract endpoints from a router file"""
    endpoints = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find all @router.METHOD("PATH") patterns
            pattern = r'@router\.(get|post|put|delete|patch)\(["\']([^"\']+)["\']'
            matches = re.findall(pattern, content)
            endpoints = [(method.upper(), path) for method, path in matches]
    except:
        pass
    return endpoints

# Get endpoints from original files
voice_py = extract_endpoints('backend/app/routers/archive_old_routers/voice.py')
transcribe_py = extract_endpoints('backend/app/routers/archive_old_routers/transcribe.py')
enhanced_py = extract_endpoints('backend/app/routers/archive_old_routers/enhanced_voice_to_app_router.py')

# Get endpoints from consolidated router
current = extract_endpoints('backend/app/routers/voice_router.py')

print("="*80)
print("VOICE ROUTER - ENDPOINT COMPARISON")
print("="*80)
print()

print(f"voice.py:                    {len(voice_py)} endpoints")
print(f"transcribe.py:               {len(transcribe_py)} endpoints")
print(f"enhanced_voice_to_app:       {len(enhanced_py)} endpoints")
print(f"Current voice_router.py:     {len(current)} endpoints")
print()

# Combine all original endpoints
all_original = []
all_original.extend(voice_py)
all_original.extend(transcribe_py)
all_original.extend(enhanced_py)

# Remove duplicates
unique_original = list(set(all_original))
unique_original.sort()

print(f"Total original (with duplicates): {len(all_original)}")
print(f"Total original (unique):          {len(unique_original)}")
print()

# Find missing endpoints
current_set = set(current)
original_set = set(unique_original)
missing = original_set - current_set

print("="*80)
print("MISSING ENDPOINTS")
print("="*80)
print()

if missing:
    print(f"Found {len(missing)} missing endpoints:")
    print()
    for method, path in sorted(missing):
        print(f"  {method:6s} {path}")
        
        # Find which file it's from
        for file, endpoints in [('voice.py', voice_py), ('transcribe.py', transcribe_py), ('enhanced', enhanced_py)]:
            if (method, path) in endpoints:
                print(f"         ↳ From: {file}")
                break
else:
    print("✅ No missing endpoints! Current router has all unique endpoints.")
    print()
    print("Note: Current router has", len(current), "endpoints")
    print("      Original had", len(unique_original), "unique endpoints")
    
    if len(current) > len(unique_original):
        extra = current_set - original_set
        print()
        print(f"✨ Current router has {len(extra)} ADDITIONAL endpoints:")
        for method, path in sorted(extra):
            print(f"  {method:6s} {path}")

print()
print("="*80)


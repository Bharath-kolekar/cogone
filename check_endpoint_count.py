"""Check endpoint count in backend"""
import requests
import json

try:
    # Get OpenAPI schema
    response = requests.get("http://localhost:8000/openapi.json", timeout=5)
    schema = response.json()
    
    paths = schema.get("paths", {})
    total_endpoints = len(paths)
    
    print("=" * 60)
    print("ENDPOINT COUNT ANALYSIS")
    print("=" * 60)
    print(f"\nTotal endpoints: {total_endpoints}")
    print(f"\nBreakdown by prefix:")
    
    # Count by prefix
    prefixes = {}
    for path in paths.keys():
        parts = path.split("/")
        if len(parts) > 2:
            prefix = f"/{parts[1]}/{parts[2]}" if len(parts) > 2 else f"/{parts[1]}"
        else:
            prefix = path
        prefixes[prefix] = prefixes.get(prefix, 0) + 1
    
    # Sort and display
    for prefix, count in sorted(prefixes.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  {prefix:50s} : {count:3d} endpoints")
    
    print("\n" + "=" * 60)
    
    # Check if any routers seem missing
    print("\nChecking for common patterns:")
    smart_coding_endpoints = [p for p in paths.keys() if 'smart' in p.lower() or 'coding' in p.lower()]
    print(f"  Smart Coding AI related: {len(smart_coding_endpoints)}")
    
    voice_endpoints = [p for p in paths.keys() if 'voice' in p.lower()]
    print(f"  Voice related: {len(voice_endpoints)}")
    
    ai_endpoints = [p for p in paths.keys() if '/ai' in p.lower() or '/ai-' in p.lower()]
    print(f"  AI related: {len(ai_endpoints)}")
    
except Exception as e:
    print(f"Error: {e}")
    exit(1)


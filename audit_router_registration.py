"""
Task 1: Audit Router Registration
Check which routers are registered in main.py and with what prefixes
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple

def get_routers_with_health_endpoints() -> List[str]:
    """Get list of all router files that have health endpoints"""
    routers_dir = Path("backend/app/routers")
    routers_with_health = []
    
    for router_file in routers_dir.glob("*.py"):
        if router_file.name.startswith("__"):
            continue
        
        try:
            with open(router_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if '@router.get("/health")' in content or '@router.post("/health")' in content:
                    routers_with_health.append(router_file.name)
        except:
            pass
    
    return sorted(routers_with_health)

def analyze_main_py() -> Dict[str, Tuple[bool, str]]:
    """Analyze main.py to see which routers are imported and included"""
    main_file = Path("backend/app/main.py")
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all imports from app.routers
    import_pattern = r'from app\.routers import \((.*?)\)'
    imports_match = re.search(import_pattern, content, re.DOTALL)
    
    imported_routers = []
    if imports_match:
        imports_text = imports_match.group(1)
        # Split by comma and clean up
        imported_routers = [r.strip() for r in imports_text.split(',') if r.strip()]
    
    # Also check for individual imports
    individual_imports = re.findall(r'from app\.routers import (\w+)', content)
    imported_routers.extend(individual_imports)
    
    # Find all app.include_router calls
    include_pattern = r'app\.include_router\(\s*(\w+)\.router\s*,\s*prefix=["\']([^"\']+)["\']'
    includes = re.findall(include_pattern, content)
    
    # Also check for includes without .router
    include_pattern2 = r'app\.include_router\(\s*(\w+)\s*,\s*prefix=["\']([^"\']+)["\']'
    includes2 = re.findall(include_pattern2, content)
    includes.extend(includes2)
    
    # Build result dict
    result = {}
    for router_name in imported_routers:
        # Check if it's included
        included = False
        prefix = ""
        for inc_name, inc_prefix in includes:
            if inc_name == router_name or inc_name == router_name.replace('_router', ''):
                included = True
                prefix = inc_prefix
                break
        result[router_name] = (included, prefix)
    
    return result

def main():
    print("=" * 80)
    print("PHASE 1.5 - TASK 1: ROUTER REGISTRATION AUDIT")
    print("=" * 80)
    print()
    
    # Step 1: Get routers with health endpoints
    print("Step 1: Finding routers with health endpoints...")
    print("-" * 80)
    routers_with_health = get_routers_with_health_endpoints()
    print(f"Found {len(routers_with_health)} routers with health endpoints:")
    for router in routers_with_health:
        print(f"  • {router}")
    print()
    
    # Step 2: Analyze main.py
    print("Step 2: Analyzing main.py router registration...")
    print("-" * 80)
    registration_status = analyze_main_py()
    
    # Step 3: Check status of each router with health endpoint
    print("Step 3: Registration status of routers with health endpoints...")
    print("-" * 80)
    print()
    
    registered = []
    not_imported = []
    imported_not_included = []
    
    for router_file in routers_with_health:
        router_name = router_file.replace('.py', '')
        
        # Check if imported
        found = False
        for imported_name, (included, prefix) in registration_status.items():
            if router_name in imported_name or imported_name in router_name:
                found = True
                if included:
                    registered.append((router_file, imported_name, prefix))
                    print(f"✅ {router_file:<50} → {prefix}")
                else:
                    imported_not_included.append((router_file, imported_name))
                    print(f"⚠️  {router_file:<50} → IMPORTED but NOT INCLUDED")
                break
        
        if not found:
            not_imported.append(router_file)
            print(f"❌ {router_file:<50} → NOT IMPORTED")
    
    # Summary
    print()
    print("=" * 80)
    print("AUDIT SUMMARY")
    print("=" * 80)
    print()
    print(f"Total routers with health endpoints: {len(routers_with_health)}")
    print(f"✅ Registered and included: {len(registered)}")
    print(f"⚠️  Imported but not included: {len(imported_not_included)}")
    print(f"❌ Not imported at all: {len(not_imported)}")
    print()
    
    if imported_not_included:
        print("⚠️  ROUTERS TO INCLUDE:")
        print("-" * 80)
        for router_file, imported_name in imported_not_included:
            print(f"  • {imported_name} (from {router_file})")
        print()
    
    if not_imported:
        print("❌ ROUTERS TO IMPORT AND INCLUDE:")
        print("-" * 80)
        for router_file in not_imported:
            router_name = router_file.replace('.py', '')
            suggested_prefix = f"/api/v0/{router_name.replace('_', '-')}"
            print(f"  • {router_name}")
            print(f"    Suggested: from app.routers import {router_name}")
            print(f"    Suggested: app.include_router({router_name}.router, prefix='{suggested_prefix}', tags=['{router_name}'])")
        print()
    
    # Step 4: Check for registered routers
    if registered:
        print("✅ PROPERLY REGISTERED ROUTERS:")
        print("-" * 80)
        for router_file, imported_name, prefix in registered:
            # Construct expected health path
            health_path = f"{prefix}/health"
            print(f"  • {router_file:<40} → {health_path}")
        print()
    
    print("=" * 80)
    print("NEXT STEPS:")
    print("=" * 80)
    print()
    print("1. Add missing imports to main.py")
    print("2. Add missing app.include_router() calls")
    print("3. Verify path prefixes are correct")
    print("4. Test health endpoints after changes")
    print()

if __name__ == "__main__":
    main()


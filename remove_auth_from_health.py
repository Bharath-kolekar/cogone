"""
Task 3: Remove Authentication from Health Endpoints
Health checks should always be public and not require authentication
"""

import re
from pathlib import Path

def remove_auth_from_health_endpoint(file_path: str) -> bool:
    """Remove auth dependencies from health endpoint in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Pattern 1: Health endpoint with current_user dependency
        # @router.get("/health")
        # async def health_check(current_user: User = Depends(...)):
        pattern1 = r'(@router\.get\(["\']/?health["\']\)[^\n]*\n\s*async def \w+\([^)]*current_user[^)]*\):)'
        
        def replace1(match):
            # Remove current_user parameter
            text = match.group(0)
            # Replace with no parameters
            func_def = re.sub(r'\([^)]*current_user[^)]*\)', '()', text)
            return func_def
        
        new_content = re.sub(pattern1, replace1, content, flags=re.MULTILINE)
        
        # Pattern 2: Depends(AuthDependencies.get_current_user) or similar
        # Remove entire parameter if it's the only one
        pattern2 = r'async def (\w*health\w*)\(\s*current_user[^)]+\)\s*:'
        new_content = re.sub(pattern2, r'async def \1():', new_content)
        
        # Pattern 3: Remove trailing comma if current_user was first param
        pattern3 = r'async def (\w*health\w*)\(\s*,\s*'
        new_content = re.sub(pattern3, r'async def \1(', new_content)
        
        if new_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def find_health_with_auth() -> list:
    """Find health endpoints that have auth dependencies"""
    routers_dir = Path("backend/app/routers")
    files_with_auth = []
    
    for router_file in routers_dir.glob("*.py"):
        if router_file.name.startswith("__"):
            continue
        
        try:
            with open(router_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check if has health endpoint
                if '@router.get("/health")' not in content and '@router.post("/health")' not in content:
                    continue
                
                # Check if health endpoint has auth
                # Look for current_user or Depends in health endpoint
                health_match = re.search(r'@router\.(get|post)\(["\']/?health["\']\).*?async def.*?\(.*?\):', content, re.DOTALL)
                if health_match:
                    if 'current_user' in health_match.group(0) or 'Depends' in health_match.group(0):
                        files_with_auth.append(str(router_file))
                        
        except:
            pass
    
    return files_with_auth

def main():
    print("=" * 80)
    print("PHASE 1.5 - TASK 3: REMOVE AUTH FROM HEALTH ENDPOINTS")
    print("=" * 80)
    print()
    
    # Step 1: Find health endpoints with auth
    print("Step 1: Finding health endpoints with authentication...")
    print("-" * 80)
    files_with_auth = find_health_with_auth()
    
    if not files_with_auth:
        print("✅ No health endpoints with authentication found!")
        print()
        return
    
    print(f"Found {len(files_with_auth)} files with authenticated health endpoints:")
    for file in files_with_auth:
        print(f"  • {Path(file).name}")
    print()
    
    # Step 2: Remove auth from health endpoints
    print("Step 2: Removing authentication from health endpoints...")
    print("-" * 80)
    
    fixed_count = 0
    for file_path in files_with_auth:
        if remove_auth_from_health_endpoint(file_path):
            fixed_count += 1
            print(f"✅ Fixed {Path(file_path).name}")
        else:
            print(f"⏭️  Skipped {Path(file_path).name} (manual review needed)")
    
    print()
    print("=" * 80)
    print("AUTH REMOVAL SUMMARY")
    print("=" * 80)
    print()
    print(f"Files with auth health endpoints: {len(files_with_auth)}")
    print(f"✅ Fixed: {fixed_count}")
    print(f"⏭️  Needs manual review: {len(files_with_auth) - fixed_count}")
    print()
    print("ℹ️  Health endpoints are now public (no authentication required)")
    print()

if __name__ == "__main__":
    main()


"""
Fix Empty Results Handling - Phase 1 Critical Fix
Change endpoints that return 404 for empty data to return 200 with empty arrays
"""

import os
import re
from pathlib import Path

def fix_empty_results_in_file(file_path: str) -> int:
    """Fix empty results handling in a router file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_made = 0
        
        # Pattern 1: if not results: raise HTTPException(404)
        # Replace with: if not results: return []
        pattern1 = r'if\s+not\s+(\w+):\s*\n\s+raise\s+HTTPException\(\s*status_code\s*=\s*(?:status\.)?HTTP_404_NOT_FOUND'
        
        def replace1(match):
            var_name = match.group(1)
            indent = re.search(r'\n(\s+)raise', match.group(0))
            indent_str = indent.group(1) if indent else '    '
            return f'if not {var_name}:\n{indent_str}return []'
        
        new_content = re.sub(pattern1, replace1, content)
        if new_content != content:
            fixes_made += content.count('raise HTTPException') - new_content.count('raise HTTPException')
            content = new_content
        
        # Pattern 2: if len(items) == 0: raise HTTPException(404)
        pattern2 = r'if\s+len\((\w+)\)\s*==\s*0:\s*\n\s+raise\s+HTTPException\(\s*status_code\s*=\s*(?:status\.)?HTTP_404_NOT_FOUND'
        
        def replace2(match):
            var_name = match.group(1)
            indent = re.search(r'\n(\s+)raise', match.group(0))
            indent_str = indent.group(1) if indent else '    '
            return f'if len({var_name}) == 0:\n{indent_str}return []'
        
        new_content = re.sub(pattern2, replace2, content)
        if new_content != content:
            fixes_made += 1
            content = new_content
        
        # Pattern 3: return None -> return []
        # Only for list endpoints
        if 'list' in file_path.lower() or 'List' in content:
            pattern3 = r'return\s+None\s*(?=\n|\s*$)'
            new_content = re.sub(pattern3, 'return []', content)
            if new_content != content:
                fixes_made += content.count('return None') - new_content.count('return None')
                content = new_content
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return fixes_made
        
        return 0
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return 0

def main():
    print("=" * 80)
    print("FIXING EMPTY RESULTS HANDLING - PHASE 1")
    print("=" * 80)
    print()
    
    routers_dir = Path("backend/app/routers")
    total_fixes = 0
    files_fixed = 0
    
    # Get all Python router files
    for router_file in routers_dir.glob("*.py"):
        if router_file.name.startswith("__"):
            continue
        
        file_path = str(router_file)
        fixes = fix_empty_results_in_file(file_path)
        
        if fixes > 0:
            files_fixed += 1
            total_fixes += fixes
            print(f"✅ Fixed {fixes} empty result handlers in {router_file.name}")
    
    print()
    print("=" * 80)
    print("EMPTY RESULTS FIX SUMMARY")
    print("=" * 80)
    print(f"✅ Files Fixed: {files_fixed}")
    print(f"✅ Total Fixes: {total_fixes}")
    print()
    print("ℹ️  Empty results now return 200 with [] instead of 404")
    print()

if __name__ == "__main__":
    main()


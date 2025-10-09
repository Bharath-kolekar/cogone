"""
Fix Syntax Errors from Empty Results Handling
The regex replacement broke some code by leaving orphaned lines
"""

import os
import re
from pathlib import Path

def fix_broken_replacements(file_path: str) -> int:
    """Fix syntax errors from broken regex replacements"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        fixes_made = 0
        
        # Pattern 1: return [], followed by orphaned detail= or status_code= lines
        # Example:
        #   return [],
        #       detail="Something"
        #   )
        pattern1 = r'return \[\],\s*\n\s+detail=.*?\n\s+\)'
        
        def replace1(match):
            # Just return empty array properly
            return 'return []'
        
        new_content = re.sub(pattern1, replace1, content)
        if new_content != content:
            fixes_made += 1
            content = new_content
        
        # Pattern 2: return [], with orphaned closing parenthesis
        pattern2 = r'return \[\],\s*\n\s+(?:detail|status_code)='
        
        while pattern2 in content or re.search(pattern2, content):
            # Find the pattern
            match = re.search(pattern2, content)
            if not match:
                break
            
            # Find the matching closing parenthesis
            start = match.start()
            paren_start = content.find('(', start - 100, start)
            if paren_start == -1:
                break
            
            # Find closing parenthesis after detail=
            paren_end = content.find(')', match.end())
            if paren_end == -1:
                break
            
            # Replace entire section with just return []
            content = content[:match.start()] + 'return []' + content[paren_end + 1:]
            fixes_made += 1
        
        # Pattern 3: Clean up any remaining orphaned HTTPException parts
        pattern3 = r',\s*\n\s+detail=.*?\n\s+\)'
        new_content = re.sub(pattern3, '', content)
        if new_content != content:
            fixes_made += 1
            content = new_content
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return fixes_made
        
        return 0
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        import traceback
        traceback.print_exc()
        return 0

def verify_syntax(file_path: str) -> bool:
    """Verify Python syntax is valid"""
    try:
        import ast
        with open(file_path, 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {Path(file_path).name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Could not verify {Path(file_path).name}: {e}")
        return True  # Assume OK if we can't parse

def main():
    print("=" * 80)
    print("FIXING SYNTAX ERRORS FROM EMPTY RESULTS HANDLING")
    print("=" * 80)
    print()
    
    routers_dir = Path("backend/app/routers")
    total_fixes = 0
    files_fixed = 0
    syntax_errors = []
    
    # Get all Python router files
    for router_file in routers_dir.glob("*.py"):
        if router_file.name.startswith("__"):
            continue
        
        file_path = str(router_file)
        
        # First check for syntax errors
        if not verify_syntax(file_path):
            syntax_errors.append(router_file.name)
            
            # Try to fix
            fixes = fix_broken_replacements(file_path)
            
            if fixes > 0:
                files_fixed += 1
                total_fixes += fixes
                
                # Verify fix worked
                if verify_syntax(file_path):
                    print(f"✅ Fixed {fixes} syntax errors in {router_file.name}")
                    syntax_errors.remove(router_file.name)
                else:
                    print(f"⚠️  Partially fixed {router_file.name}, may need manual review")
    
    print()
    print("=" * 80)
    print("SYNTAX ERROR FIX SUMMARY")
    print("=" * 80)
    print(f"✅ Files Fixed: {files_fixed}")
    print(f"✅ Total Fixes: {total_fixes}")
    
    if syntax_errors:
        print(f"\n⚠️  {len(syntax_errors)} files still have syntax errors:")
        for file in syntax_errors:
            print(f"   - {file}")
        print("\nThese need manual review.")
    else:
        print("\n🎉 All syntax errors fixed!")
    
    print()

if __name__ == "__main__":
    main()


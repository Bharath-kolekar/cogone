"""
Check ALL backend Python files for syntax and indentation errors
"""

import ast
import sys
from pathlib import Path
from typing import List, Tuple

def check_file_syntax(file_path: Path) -> Tuple[bool, str]:
    """Check if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        return True, "OK"
    except SyntaxError as e:
        return False, f"SyntaxError at line {e.lineno}: {e.msg}"
    except IndentationError as e:
        return False, f"IndentationError at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def scan_backend():
    """Scan all backend Python files"""
    print("=" * 80)
    print("BACKEND SYNTAX & INDENTATION CHECK")
    print("=" * 80)
    print()
    
    backend_dir = Path("backend")
    
    # Find all Python files
    python_files = list(backend_dir.rglob("*.py"))
    
    total_files = 0
    files_ok = 0
    files_error = 0
    errors = []
    
    print(f"Scanning {len(python_files)} Python files...")
    print("-" * 80)
    print()
    
    for file_path in sorted(python_files):
        # Skip __pycache__ and .venv
        if '__pycache__' in str(file_path) or '.venv' in str(file_path):
            continue
        
        total_files += 1
        is_ok, message = check_file_syntax(file_path)
        
        if is_ok:
            files_ok += 1
        else:
            files_error += 1
            rel_path = file_path.relative_to(Path("backend"))
            errors.append((str(rel_path), message))
            print(f"ERROR: {rel_path}")
            print(f"  {message}")
            print()
    
    # Summary
    print("=" * 80)
    print("SYNTAX CHECK SUMMARY")
    print("=" * 80)
    print()
    print(f"Total Files Scanned: {total_files}")
    print(f"OK: {files_ok}")
    print(f"ERRORS: {files_error}")
    print()
    
    if files_error > 0:
        print("-" * 80)
        print("FILES WITH ERRORS:")
        print("-" * 80)
        for file_path, error in errors:
            print(f"  {file_path}")
            print(f"    {error}")
        print()
        return False
    else:
        print("ALL FILES OK!")
        return True

if __name__ == "__main__":
    success = scan_backend()
    sys.exit(0 if success else 1)


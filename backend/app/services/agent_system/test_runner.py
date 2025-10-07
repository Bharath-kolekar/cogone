"""
TestRunner Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class TestRunner:
    """Runs tests to verify implementation"""
    
    def __init__(self):
        self.project_root = Path.cwd()
    
    async def run_tests(self, changes: List[CodeChange]) -> Dict[str, Any]:
        """Run tests to verify the implementation"""
        results = {
            "tests_run": 0,
            "tests_passed": 0,
            "tests_failed": 0,
            "coverage": 0.0,
            "errors": []
        }
        
        try:
            # Run pytest if available
            if (self.project_root / "pytest.ini").exists() or (self.project_root / "pyproject.toml").exists():
                proc = await asyncio.create_subprocess_exec(
                    "python", "-m", "pytest", "-v",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                try:
                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=300)
                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.wait()
                    stdout, stderr = b"", b"timeout"
                out_text = (stdout or b"").decode(errors='ignore')
                results["tests_run"] = self._count_tests_run(out_text)
                results["tests_passed"] = self._count_tests_passed(out_text)
                results["tests_failed"] = self._count_tests_failed(out_text)
                if proc.returncode != 0:
                    results["errors"].append((stderr or b"").decode(errors='ignore'))
            
            # Run basic syntax checks
            await self._run_syntax_checks(changes, results)
            
        except Exception as e:
            results["errors"].append(str(e))
        
        return results
    
    def _count_tests_run(self, output: str) -> int:
        """Count total tests run"""
        return len(re.findall(r'::', output))
    
    def _count_tests_passed(self, output: str) -> int:
        """Count tests that passed"""
        return len(re.findall(r'PASSED', output))
    
    def _count_tests_failed(self, output: str) -> int:
        """Count tests that failed"""
        return len(re.findall(r'FAILED', output))
    
    async def _run_syntax_checks(self, changes: List[CodeChange], results: Dict[str, Any]):
        """Run basic syntax checks on modified files"""
        for change in changes:
            if change.file_path.endswith('.py'):
                try:
                    with open(change.file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Try to parse the file
                    ast.parse(content)
                    
                except SyntaxError as e:
                    results["errors"].append(f"Syntax error in {change.file_path}: {e}")

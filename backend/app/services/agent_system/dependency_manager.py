"""
DependencyManager Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DependencyManager:
    """Manages project dependencies"""
    
    def __init__(self):
        self.project_root = Path.cwd()
    
    async def analyze_required_dependencies(self, user_request: str, analysis: Dict[str, Any]) -> List[str]:
        """Analyze what dependencies are needed for the request"""
        required_deps = []
        
        # Authentication dependencies
        if any(word in user_request.lower() for word in ["auth", "login", "signup", "authentication"]):
            required_deps.extend([
                "supabase",
                "python-jose[cryptography]",
                "passlib[bcrypt]",
                "python-multipart"
            ])
        
        # Database dependencies
        if any(word in user_request.lower() for word in ["database", "db", "model", "sql"]):
            required_deps.extend([
                "sqlalchemy",
                "alembic",
                "psycopg2-binary"
            ])
        
        # API dependencies
        if any(word in user_request.lower() for word in ["api", "endpoint", "route", "rest"]):
            required_deps.extend([
                "fastapi",
                "uvicorn",
                "pydantic"
            ])
        
        # Frontend dependencies
        if any(word in user_request.lower() for word in ["frontend", "ui", "component", "react"]):
            required_deps.extend([
                "react",
                "next",
                "typescript"
            ])
        
        return list(set(required_deps))
    
    async def install_dependencies(self, dependencies: List[str]) -> Dict[str, Any]:
        """Install dependencies"""
        results = {
            "installed": [],
            "failed": [],
            "already_installed": []
        }
        
        for dep in dependencies:
            try:
                # Check if already installed
                if await self._is_dependency_installed(dep):
                    results["already_installed"].append(dep)
                    continue
                
                # Install dependency
                proc = await asyncio.create_subprocess_exec(
                    "pip", "install", dep,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                try:
                    stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=60)
                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.wait()
                    stdout, stderr = b"", b"timeout"
                
                if proc.returncode == 0:
                    results["installed"].append(dep)
                else:
                    results["failed"].append({
                        "dependency": dep,
                        "error": (stderr or b"").decode(errors='ignore')
                    })
                    
            except Exception as e:
                results["failed"].append({
                    "dependency": dep,
                    "error": str(e)
                })
        
        return results
    
    async def _is_dependency_installed(self, dependency: str) -> bool:
        """Check if a dependency is already installed"""
        try:
            proc = await asyncio.create_subprocess_exec(
                "pip", "show", dependency,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            return proc.returncode == 0
        except:
            return False

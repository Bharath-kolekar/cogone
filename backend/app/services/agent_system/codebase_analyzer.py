"""
CodebaseAnalyzer Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class CodebaseAnalyzer:
    """Analyzes the codebase to understand structure and dependencies"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.analysis_cache = {}
    
    async def analyze_codebase(self, user_request: str) -> Dict[str, Any]:
        """Analyze the entire codebase for the given request"""
        try:
            logger.info("Starting codebase analysis", request=user_request)
            
            analysis = {
                "project_structure": await self._analyze_project_structure(),
                "dependencies": await self._analyze_dependencies(),
                "code_patterns": await self._analyze_code_patterns(),
                "user_intent": await self._analyze_user_intent(user_request),
                "affected_files": await self._identify_affected_files(user_request),
                "implementation_plan": await self._create_implementation_plan(user_request)
            }
            
            logger.info("Codebase analysis completed", 
                       files_analyzed=len(analysis["affected_files"]),
                       patterns_found=len(analysis["code_patterns"]))
            
            return analysis
            
        except Exception as e:
            logger.error("Failed to analyze codebase", error=str(e))
            raise
    
    async def _analyze_project_structure(self) -> Dict[str, Any]:
        """Analyze project structure"""
        structure = {
            "root_files": [],
            "directories": [],
            "file_types": {},
            "total_files": 0,
            "total_lines": 0
        }
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip heavy directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.venv', '.tox', '.mypy_cache', '.pytest_cache'}]
            for file in files:
                file_path = Path(root) / file
                relative_path = file_path.relative_to(self.project_root)
                
                structure["root_files"].append(str(relative_path))
                structure["total_files"] += 1
                
                # Count lines
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        structure["total_lines"] += lines
                except:
                    pass
                
                # File type analysis
                ext = file_path.suffix.lower()
                if ext not in structure["file_types"]:
                    structure["file_types"][ext] = 0
                structure["file_types"][ext] += 1
        
        return structure
    
    async def _analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies"""
        dependencies = {
            "python": [],
            "node": [],
            "system": []
        }
        
        # Python dependencies
        requirements_files = [
            "requirements.txt",
            "pyproject.toml",
            "setup.py",
            "Pipfile"
        ]
        
        for req_file in requirements_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                try:
                    with open(req_path, 'r') as f:
                        content = f.read()
                        dependencies["python"].extend(self._parse_python_dependencies(content))
                except:
                    pass
        
        # Node.js dependencies
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    package_data = json.load(f)
                    if "dependencies" in package_data:
                        dependencies["node"].extend(list(package_data["dependencies"].keys()))
            except:
                pass
        
        return dependencies
    
    async def _analyze_code_patterns(self) -> Dict[str, Any]:
        """Analyze code patterns and architecture"""
        patterns = {
            "frameworks": [],
            "patterns": [],
            "architecture": "unknown",
            "complexity": "low"
        }
        
        # Detect frameworks
        framework_indicators = {
            "fastapi": ["from fastapi import", "import fastapi"],
            "django": ["from django import", "import django"],
            "flask": ["from flask import", "import flask"],
            "react": ["import React", "from react"],
            "next": ["import next", "from next"],
            "vue": ["import vue", "from vue"],
            "angular": ["import angular", "from angular"]
        }
        
        for root, dirs, files in os.walk(self.project_root):
            # Skip heavy directories
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'dist', 'build', '.venv', '.tox', '.mypy_cache', '.pytest_cache'}]
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                    file_path = Path(root) / file
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            for framework, indicators in framework_indicators.items():
                                if any(indicator in content for indicator in indicators):
                                    if framework not in patterns["frameworks"]:
                                        patterns["frameworks"].append(framework)
                    except:
                        pass
        
        return patterns
    
    async def _analyze_user_intent(self, user_request: str) -> Dict[str, Any]:
        """Analyze user intent from the request"""
        intent = {
            "action": "unknown",
            "scope": "unknown",
            "complexity": "low",
            "files_affected": [],
            "dependencies_needed": []
        }
        
        # Analyze action type
        if any(word in user_request.lower() for word in ["add", "create", "implement"]):
            intent["action"] = "create"
        elif any(word in user_request.lower() for word in ["modify", "update", "change"]):
            intent["action"] = "modify"
        elif any(word in user_request.lower() for word in ["remove", "delete"]):
            intent["action"] = "delete"
        
        # Analyze scope
        if any(word in user_request.lower() for word in ["authentication", "auth", "login", "signup"]):
            intent["scope"] = "authentication"
            intent["files_affected"] = ["auth", "login", "signup", "user"]
            intent["dependencies_needed"] = ["supabase", "jwt", "bcrypt"]
        elif any(word in user_request.lower() for word in ["database", "db", "model"]):
            intent["scope"] = "database"
            intent["files_affected"] = ["models", "database", "schema"]
        elif any(word in user_request.lower() for word in ["api", "endpoint", "route"]):
            intent["scope"] = "api"
            intent["files_affected"] = ["routes", "api", "endpoints"]
        
        # Analyze complexity
        if len(user_request.split()) > 20:
            intent["complexity"] = "high"
        elif len(user_request.split()) > 10:
            intent["complexity"] = "medium"
        
        return intent
    
    async def _identify_affected_files(self, user_request: str) -> List[str]:
        """Identify files that will be affected by the changes"""
        affected_files = []
        
        # Simple heuristic based on keywords
        keywords = {
            "auth": ["auth", "login", "signup", "user", "authentication"],
            "api": ["api", "routes", "endpoints", "controllers"],
            "models": ["models", "database", "schema", "db"],
            "frontend": ["components", "pages", "views", "ui"],
            "config": ["config", "settings", "environment"]
        }
        
        for category, words in keywords.items():
            if any(word in user_request.lower() for word in words):
                # Find files matching this category
                for root, dirs, files in os.walk(self.project_root):
                    for file in files:
                        if any(word in file.lower() for word in words):
                            file_path = Path(root) / file
                            relative_path = file_path.relative_to(self.project_root)
                            affected_files.append(str(relative_path))
        
        return list(set(affected_files))
    
    async def _create_implementation_plan(self, user_request: str) -> List[str]:
        """Create a step-by-step implementation plan"""
        plan = [
            "Analyze user request and codebase",
            "Identify required dependencies",
            "Plan file changes and modifications",
            "Generate implementation code",
            "Add necessary imports and dependencies",
            "Create or modify files",
            "Add tests for new functionality",
            "Verify implementation works correctly",
            "Add helpful comments and documentation"
        ]
        
        return plan
    
    def _parse_python_dependencies(self, content: str) -> List[str]:
        """Parse Python dependencies from requirements file"""
        dependencies = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                # Extract package name (before ==, >=, etc.)
                package = re.split(r'[>=<!=]', line)[0].strip()
                if package:
                    dependencies.append(package)
        return dependencies

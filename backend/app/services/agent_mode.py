"""
Agent Mode Service - Autonomous Code Analysis and Implementation
Activate with Ctrl+L, describe what you want, and the agent autonomously implements it
"""

import asyncio
import json
import os
import re
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import uuid
import hashlib
from pathlib import Path
import ast
import importlib.util

from app.core.config import get_settings
from app.services.smart_coding_ai_optimized import smart_coding_ai_optimized

logger = get_settings().logger


class AgentModeStatus(str, Enum):
    """Agent Mode status"""
    IDLE = "idle"
    ANALYZING = "analyzing"
    PLANNING = "planning"
    EXECUTING = "executing"
    TESTING = "testing"
    COMPLETED = "completed"
    ERROR = "error"
    ROLLED_BACK = "rolled_back"


class ChangeType(str, Enum):
    """Types of changes the agent can make"""
    CREATE_FILE = "create_file"
    MODIFY_FILE = "modify_file"
    DELETE_FILE = "delete_file"
    ADD_DEPENDENCY = "add_dependency"
    REMOVE_DEPENDENCY = "remove_dependency"
    CREATE_DIRECTORY = "create_directory"
    ADD_IMPORT = "add_import"
    REMOVE_IMPORT = "remove_import"
    ADD_FUNCTION = "add_function"
    MODIFY_FUNCTION = "modify_function"
    ADD_CLASS = "add_class"
    MODIFY_CLASS = "modify_class"


@dataclass
class CodeChange:
    """Represents a code change to be made"""
    change_id: str
    change_type: ChangeType
    file_path: str
    description: str
    old_content: Optional[str] = None
    new_content: Optional[str] = None
    line_number: Optional[int] = None
    dependencies: List[str] = None
    tests: List[str] = None
    comments: List[str] = None
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.dependencies is None:
            self.dependencies = []
        if self.tests is None:
            self.tests = []
        if self.comments is None:
            self.comments = []


@dataclass
class AgentTask:
    """Represents an agent task"""
    task_id: str
    user_request: str
    status: AgentModeStatus
    changes: List[CodeChange]
    progress: float
    current_step: str
    analysis_results: Dict[str, Any]
    execution_plan: List[str]
    test_results: Dict[str, Any]
    rollback_data: Dict[str, Any]
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


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


class ChangeExecutor:
    """Executes code changes autonomously"""
    
    def __init__(self):
        self.backup_dir = Path("agent_mode_backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    async def execute_changes(self, changes: List[CodeChange], task_id: str) -> Dict[str, Any]:
        """Execute a list of code changes"""
        try:
            logger.info("Executing changes", task_id=task_id, changes_count=len(changes))
            
            # Create backup
            backup_path = await self._create_backup(task_id)
            
            results = {
                "successful_changes": [],
                "failed_changes": [],
                "backup_path": str(backup_path),
                "total_changes": len(changes)
            }
            
            for change in changes:
                try:
                    await self._execute_change(change)
                    results["successful_changes"].append(change.change_id)
                    logger.info("Change executed successfully", change_id=change.change_id)
                except Exception as e:
                    results["failed_changes"].append({
                        "change_id": change.change_id,
                        "error": str(e)
                    })
                    logger.error("Failed to execute change", change_id=change.change_id, error=str(e))
            
            return results
            
        except Exception as e:
            logger.error("Failed to execute changes", error=str(e))
            raise
    
    async def _create_backup(self, task_id: str) -> Path:
        """Create backup of current state"""
        backup_path = self.backup_dir / f"backup_{task_id}_{int(time.time())}"
        backup_path.mkdir(exist_ok=True)
        
        # Copy all files to backup
        for root, dirs, files in os.walk(Path.cwd()):
            for file in files:
                if not str(Path(root) / file).startswith(str(self.backup_dir)):
                    src = Path(root) / file
                    rel_path = src.relative_to(Path.cwd())
                    dst = backup_path / rel_path
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    
                    try:
                        import shutil
                        shutil.copy2(src, dst)
                    except:
                        pass
        
        return backup_path
    
    async def _execute_change(self, change: CodeChange):
        """Execute a single change"""
        if change.change_type == ChangeType.CREATE_FILE:
            await self._create_file(change)
        elif change.change_type == ChangeType.MODIFY_FILE:
            await self._modify_file(change)
        elif change.change_type == ChangeType.DELETE_FILE:
            await self._delete_file(change)
        elif change.change_type == ChangeType.ADD_DEPENDENCY:
            await self._add_dependency(change)
        elif change.change_type == ChangeType.ADD_IMPORT:
            await self._add_import(change)
        elif change.change_type == ChangeType.ADD_FUNCTION:
            await self._add_function(change)
        elif change.change_type == ChangeType.ADD_CLASS:
            await self._add_class(change)
    
    async def _create_file(self, change: CodeChange):
        """Create a new file"""
        file_path = Path(change.file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(change.new_content)
    
    async def _modify_file(self, change: CodeChange):
        """Modify an existing file"""
        file_path = Path(change.file_path)
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple replacement for now
            if change.old_content and change.new_content:
                content = content.replace(change.old_content, change.new_content)
            elif change.new_content:
                content += "\n" + change.new_content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    async def _delete_file(self, change: CodeChange):
        """Delete a file"""
        file_path = Path(change.file_path)
        if file_path.exists():
            file_path.unlink()
    
    async def _add_dependency(self, change: CodeChange):
        """Add a dependency to requirements.txt"""
        requirements_file = Path("requirements.txt")
        
        if requirements_file.exists():
            with open(requirements_file, 'r') as f:
                content = f.read()
        else:
            content = ""
        
        for dep in change.dependencies:
            if dep not in content:
                content += f"\n{dep}"
        
        with open(requirements_file, 'w') as f:
            f.write(content)
    
    async def _add_import(self, change: CodeChange):
        """Add an import to a file"""
        file_path = Path(change.file_path)
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add import at the top
            imports = change.dependencies
            import_lines = [f"import {imp}" for imp in imports]
            new_imports = "\n".join(import_lines)
            
            # Find the right place to insert imports
            lines = content.split('\n')
            insert_index = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    insert_index = i + 1
                elif line.strip() and not line.strip().startswith('#'):
                    break
            
            lines.insert(insert_index, new_imports)
            content = '\n'.join(lines)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    async def _add_function(self, change: CodeChange):
        """Add a function to a file"""
        file_path = Path(change.file_path)
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add function at the end
            content += "\n\n" + change.new_content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    async def _add_class(self, change: CodeChange):
        """Add a class to a file"""
        file_path = Path(change.file_path)
        
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add class at the end
            content += "\n\n" + change.new_content
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)


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
                result = subprocess.run(
                    ["pip", "install", dep],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode == 0:
                    results["installed"].append(dep)
                else:
                    results["failed"].append({
                        "dependency": dep,
                        "error": result.stderr
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
            result = subprocess.run(
                ["pip", "show", dependency],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False


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
                result = subprocess.run(
                    ["python", "-m", "pytest", "-v"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                results["tests_run"] = self._count_tests_run(result.stdout)
                results["tests_passed"] = self._count_tests_passed(result.stdout)
                results["tests_failed"] = self._count_tests_failed(result.stdout)
                
                if result.returncode != 0:
                    results["errors"].append(result.stderr)
            
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


class CommentGenerator:
    """Generates helpful comments for code changes"""
    
    def __init__(self):
        self.comment_templates = {
            "function": "# Function: {name}\n# Description: {description}\n# Parameters: {params}\n# Returns: {returns}",
            "class": "# Class: {name}\n# Description: {description}\n# Methods: {methods}",
            "import": "# Import: {name}\n# Purpose: {purpose}",
            "dependency": "# Dependency: {name}\n# Purpose: {purpose}\n# Version: {version}"
        }
    
    async def generate_comments(self, changes: List[CodeChange]) -> List[str]:
        """Generate helpful comments for changes"""
        comments = []
        
        for change in changes:
            if change.change_type == ChangeType.ADD_FUNCTION:
                comment = self._generate_function_comment(change)
                comments.append(comment)
            elif change.change_type == ChangeType.ADD_CLASS:
                comment = self._generate_class_comment(change)
                comments.append(comment)
            elif change.change_type == ChangeType.ADD_IMPORT:
                comment = self._generate_import_comment(change)
                comments.append(comment)
            elif change.change_type == ChangeType.ADD_DEPENDENCY:
                comment = self._generate_dependency_comment(change)
                comments.append(comment)
        
        return comments
    
    def _generate_function_comment(self, change: CodeChange) -> str:
        """Generate comment for a function"""
        return f"""
# ============================================================================
# Function: {change.description}
# Added by Agent Mode - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ============================================================================
"""
    
    def _generate_class_comment(self, change: CodeChange) -> str:
        """Generate comment for a class"""
        return f"""
# ============================================================================
# Class: {change.description}
# Added by Agent Mode - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# ============================================================================
"""
    
    def _generate_import_comment(self, change: CodeChange) -> str:
        """Generate comment for an import"""
        return f"# Import added by Agent Mode for: {change.description}"
    
    def _generate_dependency_comment(self, change: CodeChange) -> str:
        """Generate comment for a dependency"""
        return f"# Dependency added by Agent Mode for: {change.description}"


class AgentModeService:
    """Main Agent Mode service that orchestrates all components"""
    
    def __init__(self):
        self.analyzer = CodebaseAnalyzer()
        self.executor = ChangeExecutor()
        self.dependency_manager = DependencyManager()
        self.test_runner = TestRunner()
        self.comment_generator = CommentGenerator()
        self.active_tasks: Dict[str, AgentTask] = {}
    
    async def activate_agent_mode(self, user_request: str) -> str:
        """Activate Agent Mode with user request"""
        try:
            task_id = str(uuid.uuid4())
            
            # Create initial task
            task = AgentTask(
                task_id=task_id,
                user_request=user_request,
                status=AgentModeStatus.ANALYZING,
                changes=[],
                progress=0.0,
                current_step="Analyzing codebase...",
                analysis_results={},
                execution_plan=[],
                test_results={},
                rollback_data={}
            )
            
            self.active_tasks[task_id] = task
            
            # Start analysis in background
            asyncio.create_task(self._process_task(task_id))
            
            logger.info("Agent Mode activated", task_id=task_id, request=user_request)
            return task_id
            
        except Exception as e:
            logger.error("Failed to activate Agent Mode", error=str(e))
            raise
    
    async def get_task_status(self, task_id: str) -> Optional[AgentTask]:
        """Get status of an agent task"""
        return self.active_tasks.get(task_id)
    
    async def rollback_task(self, task_id: str) -> Dict[str, Any]:
        """Rollback changes made by a task"""
        try:
            task = self.active_tasks.get(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Restore from backup
            backup_path = Path(task.rollback_data.get("backup_path"))
            if backup_path.exists():
                # Restore files from backup
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        src = Path(root) / file
                        rel_path = src.relative_to(backup_path)
                        dst = Path.cwd() / rel_path
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        
                        import shutil
                        shutil.copy2(src, dst)
                
                task.status = AgentModeStatus.ROLLED_BACK
                task.current_step = "Changes rolled back successfully"
                
                logger.info("Task rolled back", task_id=task_id)
                return {"success": True, "message": "Changes rolled back successfully"}
            else:
                return {"success": False, "message": "Backup not found"}
                
        except Exception as e:
            logger.error("Failed to rollback task", task_id=task_id, error=str(e))
            return {"success": False, "message": str(e)}
    
    async def _process_task(self, task_id: str):
        """Process an agent task"""
        try:
            task = self.active_tasks[task_id]
            
            # Step 1: Analyze codebase
            task.current_step = "Analyzing codebase..."
            task.progress = 10.0
            analysis = await self.analyzer.analyze_codebase(task.user_request)
            task.analysis_results = analysis
            
            # Step 2: Plan changes
            task.current_step = "Planning changes..."
            task.progress = 30.0
            changes = await self._plan_changes(task.user_request, analysis)
            task.changes = changes
            
            # Step 3: Manage dependencies
            task.current_step = "Managing dependencies..."
            task.progress = 50.0
            required_deps = await self.dependency_manager.analyze_required_dependencies(
                task.user_request, analysis
            )
            dep_results = await self.dependency_manager.install_dependencies(required_deps)
            
            # Step 4: Execute changes
            task.current_step = "Executing changes..."
            task.progress = 70.0
            execution_results = await self.executor.execute_changes(changes, task_id)
            task.rollback_data = {"backup_path": execution_results["backup_path"]}
            
            # Step 5: Run tests
            task.current_step = "Running tests..."
            task.progress = 90.0
            test_results = await self.test_runner.run_tests(changes)
            task.test_results = test_results
            
            # Step 6: Generate comments
            task.current_step = "Adding comments..."
            task.progress = 95.0
            comments = await self.comment_generator.generate_comments(changes)
            
            # Complete
            task.current_step = "Completed successfully!"
            task.progress = 100.0
            task.status = AgentModeStatus.COMPLETED
            
            logger.info("Task completed", task_id=task_id, changes=len(changes))
            
        except Exception as e:
            task = self.active_tasks[task_id]
            task.status = AgentModeStatus.ERROR
            task.current_step = f"Error: {str(e)}"
            logger.error("Task failed", task_id=task_id, error=str(e))
    
    async def _plan_changes(self, user_request: str, analysis: Dict[str, Any]) -> List[CodeChange]:
        """Plan the changes needed to fulfill the user request"""
        changes = []
        
        # Example: Add authentication with Supabase
        if "authentication" in user_request.lower() or "auth" in user_request.lower():
            # Create auth service
            auth_service_content = '''
# Authentication service
from supabase import create_client, Client
import os
from typing import Optional

class AuthService:
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
    
    async def signup(self, email: str, password: str) -> dict:
        """Sign up a new user"""
        try:
            result = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            return {"success": True, "user": result.user}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def login(self, email: str, password: str) -> dict:
        """Login a user"""
        try:
            result = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {"success": True, "user": result.user}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def logout(self) -> dict:
        """Logout current user"""
        try:
            self.supabase.auth.sign_out()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
'''
            
            changes.append(CodeChange(
                change_id=str(uuid.uuid4()),
                change_type=ChangeType.CREATE_FILE,
                file_path="app/services/auth_service.py",
                description="Create authentication service with Supabase",
                new_content=auth_service_content,
                dependencies=["supabase"],
                tests=["test_auth_service.py"],
                comments=["Authentication service for user management"]
            ))
            
            # Create auth router
            auth_router_content = '''
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

class SignupRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
async def signup(request: SignupRequest):
    """Sign up a new user"""
    result = await auth_service.signup(request.email, request.password)
    if result["success"]:
        return {"message": "User created successfully", "user": result["user"]}
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@router.post("/login")
async def login(request: LoginRequest):
    """Login a user"""
    result = await auth_service.login(request.email, request.password)
    if result["success"]:
        return {"message": "Login successful", "user": result["user"]}
    else:
        raise HTTPException(status_code=401, detail=result["error"])

@router.post("/logout")
async def logout():
    """Logout current user"""
    result = await auth_service.logout()
    if result["success"]:
        return {"message": "Logout successful"}
    else:
        raise HTTPException(status_code=400, detail=result["error"])
'''
            
            changes.append(CodeChange(
                change_id=str(uuid.uuid4()),
                change_type=ChangeType.CREATE_FILE,
                file_path="app/routers/auth_router.py",
                description="Create authentication router with endpoints",
                new_content=auth_router_content,
                dependencies=["fastapi", "pydantic"],
                tests=["test_auth_router.py"],
                comments=["Authentication endpoints for login, signup, logout"]
            ))
            
            # Create test file
            test_content = '''
import pytest
from app.services.auth_service import AuthService

class TestAuthService:
    def test_signup(self):
        """Test user signup"""
        auth_service = AuthService()
        # Add test implementation
        pass
    
    def test_login(self):
        """Test user login"""
        auth_service = AuthService()
        # Add test implementation
        pass
    
    def test_logout(self):
        """Test user logout"""
        auth_service = AuthService()
        # Add test implementation
        pass
'''
            
            changes.append(CodeChange(
                change_id=str(uuid.uuid4()),
                change_type=ChangeType.CREATE_FILE,
                file_path="tests/test_auth_service.py",
                description="Create tests for authentication service",
                new_content=test_content,
                dependencies=["pytest"],
                tests=[],
                comments=["Tests for authentication functionality"]
            ))
        
        return changes


# Global agent mode service instance
agent_mode_service = AgentModeService()

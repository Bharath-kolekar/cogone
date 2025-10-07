"""
AgentModeService Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


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

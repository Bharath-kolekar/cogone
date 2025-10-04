"""
Agent Mode Pydantic models
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


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


class AgentModeRequest(BaseModel):
    """Request to activate Agent Mode"""
    user_request: str = Field(..., description="Natural language description of what the user wants")
    project_path: Optional[str] = Field(None, description="Path to the project directory")
    options: Optional[Dict[str, Any]] = Field(None, description="Additional options for the agent")


class AgentModeResponse(BaseModel):
    """Response from Agent Mode activation"""
    task_id: str = Field(..., description="Unique task ID")
    status: AgentModeStatus = Field(..., description="Current status")
    message: str = Field(..., description="Status message")
    estimated_time: Optional[int] = Field(None, description="Estimated completion time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class CodeChangeRequest(BaseModel):
    """Request for a code change"""
    change_type: ChangeType = Field(..., description="Type of change to make")
    file_path: str = Field(..., description="Path to the file to modify")
    description: str = Field(..., description="Description of the change")
    old_content: Optional[str] = Field(None, description="Old content to replace")
    new_content: Optional[str] = Field(None, description="New content to add")
    line_number: Optional[int] = Field(None, description="Line number for the change")
    dependencies: Optional[List[str]] = Field(None, description="Dependencies needed")
    tests: Optional[List[str]] = Field(None, description="Tests to add")
    comments: Optional[List[str]] = Field(None, description="Comments to add")


class CodeChangeResponse(BaseModel):
    """Response for a code change"""
    change_id: str = Field(..., description="Unique change ID")
    change_type: ChangeType = Field(..., description="Type of change")
    file_path: str = Field(..., description="Path to the file")
    description: str = Field(..., description="Description of the change")
    status: str = Field(..., description="Status of the change")
    success: bool = Field(..., description="Whether the change was successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Change timestamp")


class TaskStatusRequest(BaseModel):
    """Request for task status"""
    task_id: str = Field(..., description="Task ID to check status for")


class TaskStatusResponse(BaseModel):
    """Response for task status"""
    task_id: str = Field(..., description="Task ID")
    status: AgentModeStatus = Field(..., description="Current status")
    progress: float = Field(..., description="Progress percentage (0-100)")
    current_step: str = Field(..., description="Current step being executed")
    changes: List[CodeChangeResponse] = Field(..., description="List of changes made")
    analysis_results: Dict[str, Any] = Field(..., description="Analysis results")
    execution_plan: List[str] = Field(..., description="Execution plan")
    test_results: Dict[str, Any] = Field(..., description="Test results")
    error_message: Optional[str] = Field(None, description="Error message if any")
    created_at: datetime = Field(..., description="Task creation time")
    updated_at: datetime = Field(..., description="Last update time")


class RollbackRequest(BaseModel):
    """Request to rollback changes"""
    task_id: str = Field(..., description="Task ID to rollback")
    confirm: bool = Field(False, description="Confirmation to proceed with rollback")


class RollbackResponse(BaseModel):
    """Response for rollback operation"""
    success: bool = Field(..., description="Whether rollback was successful")
    message: str = Field(..., description="Rollback result message")
    backup_path: Optional[str] = Field(None, description="Path to backup files")
    timestamp: datetime = Field(default_factory=datetime.now, description="Rollback timestamp")


class AnalysisRequest(BaseModel):
    """Request for codebase analysis"""
    user_request: str = Field(..., description="User request to analyze")
    project_path: Optional[str] = Field(None, description="Project path to analyze")
    deep_analysis: bool = Field(False, description="Whether to perform deep analysis")


class AnalysisResponse(BaseModel):
    """Response for codebase analysis"""
    project_structure: Dict[str, Any] = Field(..., description="Project structure analysis")
    dependencies: Dict[str, Any] = Field(..., description="Dependencies analysis")
    code_patterns: Dict[str, Any] = Field(..., description="Code patterns analysis")
    user_intent: Dict[str, Any] = Field(..., description="User intent analysis")
    affected_files: List[str] = Field(..., description="Files that will be affected")
    implementation_plan: List[str] = Field(..., description="Step-by-step implementation plan")
    complexity_score: float = Field(..., description="Complexity score (0-1)")
    estimated_time: int = Field(..., description="Estimated implementation time in minutes")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")


class DependencyRequest(BaseModel):
    """Request for dependency management"""
    dependencies: List[str] = Field(..., description="List of dependencies to install")
    project_path: Optional[str] = Field(None, description="Project path")
    force_install: bool = Field(False, description="Force install even if already present")


class DependencyResponse(BaseModel):
    """Response for dependency management"""
    installed: List[str] = Field(..., description="Successfully installed dependencies")
    failed: List[Dict[str, str]] = Field(..., description="Failed installations")
    already_installed: List[str] = Field(..., description="Dependencies already installed")
    total_count: int = Field(..., description="Total dependencies processed")
    timestamp: datetime = Field(default_factory=datetime.now, description="Installation timestamp")


class TestRequest(BaseModel):
    """Request for running tests"""
    task_id: str = Field(..., description="Task ID to run tests for")
    test_files: Optional[List[str]] = Field(None, description="Specific test files to run")
    coverage: bool = Field(False, description="Whether to run coverage analysis")


class TestResponse(BaseModel):
    """Response for test execution"""
    tests_run: int = Field(..., description="Number of tests run")
    tests_passed: int = Field(..., description="Number of tests passed")
    tests_failed: int = Field(..., description="Number of tests failed")
    coverage: float = Field(..., description="Code coverage percentage")
    errors: List[str] = Field(..., description="Test errors")
    execution_time: float = Field(..., description="Test execution time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Test timestamp")


class CommentRequest(BaseModel):
    """Request for generating comments"""
    changes: List[CodeChangeRequest] = Field(..., description="Changes to generate comments for")
    style: str = Field("detailed", description="Comment style: brief, detailed, comprehensive")
    language: str = Field("en", description="Comment language")


class CommentResponse(BaseModel):
    """Response for comment generation"""
    comments: List[str] = Field(..., description="Generated comments")
    total_comments: int = Field(..., description="Total number of comments generated")
    style_used: str = Field(..., description="Comment style used")
    timestamp: datetime = Field(default_factory=datetime.now, description="Comment generation timestamp")


class AgentModeStatusResponse(BaseModel):
    """Response for Agent Mode service status"""
    service_active: bool = Field(..., description="Whether Agent Mode service is active")
    active_tasks: int = Field(..., description="Number of active tasks")
    completed_tasks: int = Field(..., description="Number of completed tasks")
    failed_tasks: int = Field(..., description="Number of failed tasks")
    supported_languages: List[str] = Field(..., description="Supported programming languages")
    capabilities: List[str] = Field(..., description="Agent Mode capabilities")
    performance_metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    timestamp: datetime = Field(default_factory=datetime.now, description="Status timestamp")


class ProgressUpdate(BaseModel):
    """Real-time progress update"""
    task_id: str = Field(..., description="Task ID")
    progress: float = Field(..., description="Progress percentage (0-100)")
    current_step: str = Field(..., description="Current step")
    status: AgentModeStatus = Field(..., description="Current status")
    estimated_remaining: Optional[int] = Field(None, description="Estimated remaining time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now, description="Update timestamp")


class ChangePreview(BaseModel):
    """Preview of changes to be made"""
    change_id: str = Field(..., description="Change ID")
    change_type: ChangeType = Field(..., description="Type of change")
    file_path: str = Field(..., description="File path")
    description: str = Field(..., description="Change description")
    preview: str = Field(..., description="Preview of the change")
    impact: str = Field(..., description="Impact description")
    dependencies: List[str] = Field(..., description="Dependencies needed")
    risks: List[str] = Field(..., description="Potential risks")
    timestamp: datetime = Field(default_factory=datetime.now, description="Preview timestamp")


class AgentModeConfig(BaseModel):
    """Configuration for Agent Mode"""
    max_concurrent_tasks: int = Field(5, description="Maximum concurrent tasks")
    timeout_minutes: int = Field(30, description="Task timeout in minutes")
    auto_backup: bool = Field(True, description="Automatically create backups")
    auto_test: bool = Field(True, description="Automatically run tests")
    auto_comment: bool = Field(True, description="Automatically add comments")
    supported_file_types: List[str] = Field(
        default=[".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c", ".go", ".rs", ".php", ".rb", ".swift", ".kt"],
        description="Supported file types"
    )
    excluded_directories: List[str] = Field(
        default=["node_modules", ".git", "__pycache__", ".venv", "venv", "env"],
        description="Directories to exclude from analysis"
    )
    max_file_size_mb: int = Field(10, description="Maximum file size to process in MB")
    timestamp: datetime = Field(default_factory=datetime.now, description="Configuration timestamp")

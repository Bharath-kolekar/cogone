"""
Orchestration models for AI Orchestration Layer
Preserves request/response and orchestration data structures
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Any
from .enums import OrchestrationMode, ValidationLevel, OrchestrationPriority


@dataclass
class OrchestrationRequest:
    """Request for AI orchestration"""
    request_id: str
    code: str
    language: str
    validation_level: ValidationLevel = ValidationLevel.STANDARD
    orchestration_mode: OrchestrationMode = OrchestrationMode.HIERARCHICAL
    priority: OrchestrationPriority = OrchestrationPriority.NORMAL
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class OrchestrationResponse:
    """Response from AI orchestration"""
    request_id: str
    validation_results: Dict[str, Any]
    optimized_code: Optional[str] = None
    suggestions: Optional[List[Dict[str, Any]]] = None
    errors: Optional[List[str]] = None
    warnings: Optional[List[str]] = None
    metrics: Optional[Dict[str, Any]] = None
    overall_score: float = 0.0
    passed: bool = False
    processing_time: float = 0.0
    completed_at: datetime = None
    
    def __post_init__(self):
        if self.completed_at is None:
            self.completed_at = datetime.now()


@dataclass
class ValidationResult:
    """Result from a validation category"""
    category: str
    passed: bool
    score: float
    issues: List[str]
    suggestions: List[str]
    metrics: Dict[str, Any]
    processing_time: float
    validator_name: str
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

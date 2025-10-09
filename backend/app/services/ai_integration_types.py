"""
Shared types for AI Integration
Extracted to break circular dependencies between services
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Any
from datetime import datetime
import uuid


@dataclass
class AIIntegrationContext:
    """Context for AI integration operations"""
    user_id: str
    session_id: Optional[str] = None
    project_id: Optional[str] = None
    request_id: Optional[str] = None
    operation_type: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if not self.request_id:
            self.request_id = str(uuid.uuid4())


@dataclass
class IntegratedAIResponse:
    """Response from integrated AI system"""
    response_id: str
    primary_response: Any
    supporting_responses: Dict[str, Any]
    confidence: float
    integration_metadata: Dict[str, Any]
    timestamp: datetime


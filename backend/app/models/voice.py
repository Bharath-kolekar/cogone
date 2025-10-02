"""
Voice processing models for Voice-to-App SaaS Platform
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class VoiceTranscriptionRequest(BaseModel):
    audio_file: bytes
    language: str = "en"


class VoiceTranscriptionResponse(BaseModel):
    transcript: str
    confidence: float
    language: str
    method: str  # "local" or "cloud"
    processing_time_ms: int


class VoiceIntentRequest(BaseModel):
    transcript: str
    language: str = "en"


class IntentEntity(BaseModel):
    entity: str
    value: str
    confidence: float


class AppPlan(BaseModel):
    steps: List[str]
    estimated_time_ms: int
    complexity: str  # "simple", "medium", "complex"
    technologies: List[str]
    features: List[str]


class VoiceIntentResponse(BaseModel):
    intent: str
    entities: List[IntentEntity]
    confidence: float
    plan: AppPlan
    estimated_time_ms: int
    method: str  # "local" or "cloud"


class AppGenerationRequest(BaseModel):
    transcript: str
    title: Optional[str] = None
    description: Optional[str] = None
    plan: AppPlan
    user_preferences: Optional[Dict[str, Any]] = None


class AppGenerationResponse(BaseModel):
    app_id: str
    status: str  # "generating", "completed", "failed"
    message: str
    estimated_time_ms: int
    preview_url: Optional[str] = None


class AppDeployRequest(BaseModel):
    app_id: str
    platform: str = "vercel"  # "vercel", "render", "netlify"
    custom_domain: Optional[str] = None


class AppDeployResponse(BaseModel):
    deployment_id: str
    status: str  # "deploying", "completed", "failed"
    url: Optional[str] = None
    message: str


class VoiceCommand(BaseModel):
    id: str
    user_id: str
    transcript: str
    language: str
    confidence: Optional[float] = None
    intent: Optional[Dict[str, Any]] = None
    processed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
"""
App generation models for Voice-to-App SaaS Platform
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class AppStatus(str, Enum):
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    DEPLOYED = "deployed"


class AppCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None
    voice_command: Optional[str] = None
    template_id: Optional[str] = None
    user_preferences: Optional[Dict[str, Any]] = None
    customizations: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AppCreateResponse(BaseModel):
    app_id: str
    status: AppStatus
    message: str
    estimated_time_ms: int
    preview_url: Optional[str] = None


class AppUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    regenerate: bool = False


class AppUpdateResponse(BaseModel):
    app_id: str
    status: AppStatus
    message: str
    updated_fields: Dict[str, Any]


class GeneratedApp(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str] = None
    voice_command: str
    repo_url: Optional[str] = None
    zip_url: Optional[str] = None
    preview_url: Optional[str] = None
    status: AppStatus
    metadata: Dict[str, Any]
    generation_time_ms: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AppListRequest(BaseModel):
    status: Optional[AppStatus] = None
    limit: int = 10
    offset: int = 0
    sort_by: str = "created_at"  # "created_at", "title", "status"


class AppListResponse(BaseModel):
    apps: List[GeneratedApp]
    total: int
    limit: int
    offset: int


class TemplateCreateRequest(BaseModel):
    title: str
    description: str
    category: str
    tags: List[str]
    template_data: Dict[str, Any]
    is_public: bool = False


class TemplateCreateResponse(BaseModel):
    template_id: str
    status: str
    message: str
    marketplace_url: Optional[str] = None


class AppTemplate(BaseModel):
    id: str
    creator_id: str
    title: str
    description: str
    category: str
    tags: List[str]
    template_data: Dict[str, Any]
    is_public: bool
    download_count: int
    rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True




class TemplateListRequest(BaseModel):
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    limit: int = 10
    offset: int = 0
    sort_by: str = "download_count"  # "download_count", "rating", "created_at"


class TemplateListResponse(BaseModel):
    templates: List[AppTemplate]
    total: int
    limit: int
    offset: int


class CollaborationInviteRequest(BaseModel):
    app_id: str
    collaborator_email: str
    permissions: List[str]  # ["read", "write", "admin"]


class CollaborationInviteResponse(BaseModel):
    invitation_id: str
    status: str
    message: str


class AppTemplate(BaseModel):
    id: str
    creator_id: str
    title: str
    description: str
    category: str
    tags: List[str]
    preview_image_url: Optional[str] = None
    template_data: Dict[str, Any]
    is_public: bool
    is_featured: bool
    download_count: int
    rating: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TemplateReview(BaseModel):
    id: str
    template_id: str
    user_id: str
    rating: int
    review_text: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CollaborationInvitation(BaseModel):
    id: str
    app_id: str
    inviter_id: str
    collaborator_email: str
    permissions: List[str]
    status: str  # "pending", "accepted", "declined"
    created_at: datetime

    class Config:
        from_attributes = True


class AppAnalytics(BaseModel):
    app_id: str
    views: int
    downloads: int
    shares: int
    deployment_views: int
    last_accessed: Optional[datetime] = None
    created_at: datetime
"""
Admin models for feature management and system configuration
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class FeatureStatus(str, Enum):
    """Feature status options"""
    ENABLED = "enabled"
    DISABLED = "disabled"
    MAINTENANCE = "maintenance"


class FeatureCategory(str, Enum):
    """Feature categories"""
    AI_SERVICES = "ai_services"
    COMMUNICATION = "communication"
    PAYMENT = "payment"
    MONITORING = "monitoring"
    STORAGE = "storage"
    PROCESSING = "processing"


class FeatureConfig(BaseModel):
    """Feature configuration model"""
    feature_id: str = Field(..., description="Unique feature identifier")
    name: str = Field(..., description="Feature display name")
    description: str = Field(..., description="Feature description")
    category: FeatureCategory = Field(..., description="Feature category")
    status: FeatureStatus = Field(default=FeatureStatus.DISABLED, description="Feature status")
    cost_per_request: float = Field(default=0.0, description="Cost per request in USD")
    free_tier_limit: Optional[int] = Field(default=None, description="Free tier request limit")
    current_usage: int = Field(default=0, description="Current usage count")
    usage_percentage: float = Field(default=0.0, description="Usage percentage of free tier")
    dependencies: List[str] = Field(default_factory=list, description="Feature dependencies")
    configuration: Dict[str, Any] = Field(default_factory=dict, description="Feature configuration")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last update timestamp")
    updated_by: str = Field(default="system", description="Last updated by")


class AdminDashboard(BaseModel):
    """Admin dashboard model"""
    total_features: int = Field(..., description="Total number of features")
    enabled_features: int = Field(..., description="Number of enabled features")
    disabled_features: int = Field(..., description="Number of disabled features")
    maintenance_features: int = Field(..., description="Number of features in maintenance")
    total_cost: float = Field(default=0.0, description="Total monthly cost")
    free_tier_usage: Dict[str, float] = Field(default_factory=dict, description="Free tier usage by service")
    alerts: List[str] = Field(default_factory=list, description="Active alerts")
    last_updated: datetime = Field(default_factory=datetime.now, description="Last dashboard update")


class FeatureToggleRequest(BaseModel):
    """Request to toggle feature status"""
    feature_id: str = Field(..., description="Feature ID to toggle")
    status: FeatureStatus = Field(..., description="New status")
    reason: Optional[str] = Field(default=None, description="Reason for change")


class FeatureConfigurationRequest(BaseModel):
    """Request to update feature configuration"""
    feature_id: str = Field(..., description="Feature ID to configure")
    configuration: Dict[str, Any] = Field(..., description="New configuration")
    reason: Optional[str] = Field(default=None, description="Reason for change")


class UsageAlert(BaseModel):
    """Usage alert model"""
    service_name: str = Field(..., description="Service name")
    current_usage: int = Field(..., description="Current usage")
    limit: int = Field(..., description="Usage limit")
    percentage: float = Field(..., description="Usage percentage")
    alert_level: str = Field(..., description="Alert level (warning, critical)")
    message: str = Field(..., description="Alert message")
    created_at: datetime = Field(default_factory=datetime.now, description="Alert creation time")


class SystemConfiguration(BaseModel):
    """System configuration model"""
    ai_assistant_name: str = Field(default="Vihaan", description="Default AI assistant name")
    wake_word: str = Field(default="Hey Vihaan", description="Wake word for AI assistant")
    chat_consolidation_enabled: bool = Field(default=True, description="Enable chat consolidation")
    nlp_enhancement_enabled: bool = Field(default=True, description="Enable NLP enhancement")
    monitoring_enabled: bool = Field(default=True, description="Enable system monitoring")
    email_service: str = Field(default="privateemail", description="Email service provider")
    email_domain: str = Field(default="cognomega.com", description="Email domain")
    primary_ai_provider: str = Field(default="groq", description="Primary AI provider")
    secondary_ai_provider: str = Field(default="together", description="Secondary AI provider")
    disabled_ai_providers: List[str] = Field(default_factory=lambda: ["huggingface"], description="Disabled AI providers")
    storage_provider: str = Field(default="cloudflare_d1", description="Storage provider")
    cache_provider: str = Field(default="cloudflare_d1", description="Cache provider")
    monitoring_provider: str = Field(default="sentry", description="Monitoring provider")
    analytics_provider: str = Field(default="cloudflare", description="Analytics provider")
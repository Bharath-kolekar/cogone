"""
Admin models for Voice-to-App SaaS Platform
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class AdminStatsRequest(BaseModel):
    time_period: str = "30d"  # "7d", "30d", "90d", "1y", "all"


class UserStatistics(BaseModel):
    total_users: int
    new_users: int
    active_users: int
    subscription_distribution: Dict[str, int]
    user_growth_rate: float


class AppStatistics(BaseModel):
    total_apps: int
    apps_generated: int
    apps_deployed: int
    success_rate: float
    avg_generation_time_ms: int
    popular_categories: List[Dict[str, Any]]


class PaymentStatistics(BaseModel):
    total_revenue: float
    revenue_growth_rate: float
    payment_method_distribution: Dict[str, int]
    subscription_revenue: float
    one_time_payments: float
    refund_rate: float


class VoiceStatistics(BaseModel):
    total_commands: int
    commands_per_day: int
    language_distribution: Dict[str, int]
    avg_confidence: float
    processing_method_distribution: Dict[str, int]


class AdminStatsResponse(BaseModel):
    time_period: str
    users: UserStatistics
    apps: AppStatistics
    payments: PaymentStatistics
    voice_commands: VoiceStatistics
    generated_at: datetime


class UserManagementRequest(BaseModel):
    subscription_tier: Optional[str] = None
    subscription_status: Optional[str] = None
    points: Optional[int] = None
    level: Optional[int] = None
    is_active: Optional[bool] = None


class UserManagementResponse(BaseModel):
    user_id: str
    status: str
    message: str
    updated_fields: Dict[str, Any]


class SystemHealthRequest(BaseModel):
    include_external: bool = True


class ServiceHealth(BaseModel):
    name: str
    status: str  # "healthy", "degraded", "down"
    response_time_ms: Optional[int] = None
    last_check: datetime
    error_message: Optional[str] = None


class DatabaseHealth(BaseModel):
    status: str
    connection_pool_size: int
    active_connections: int
    response_time_ms: int
    last_check: datetime


class RedisHealth(BaseModel):
    status: str
    memory_usage: int
    connected_clients: int
    response_time_ms: int
    last_check: datetime


class ExternalAPIHealth(BaseModel):
    name: str
    status: str
    response_time_ms: Optional[int] = None
    last_check: datetime
    error_message: Optional[str] = None


class SystemHealthResponse(BaseModel):
    status: str  # "healthy", "degraded", "down"
    services: List[ServiceHealth]
    database: DatabaseHealth
    redis: RedisHealth
    external_apis: List[ExternalAPIHealth]
    checked_at: datetime


class UserReport(BaseModel):
    period: Dict[str, str]
    total_users: int
    new_registrations: int
    active_users: int
    user_retention_rate: float
    top_countries: List[Dict[str, Any]]
    subscription_trends: List[Dict[str, Any]]
    user_activity_patterns: Dict[str, Any]


class AppReport(BaseModel):
    period: Dict[str, str]
    total_apps: int
    successful_generations: int
    failed_generations: int
    avg_generation_time: int
    popular_app_types: List[Dict[str, Any]]
    generation_trends: List[Dict[str, Any]]
    deployment_stats: Dict[str, Any]


class PaymentReport(BaseModel):
    period: Dict[str, str]
    total_revenue: float
    total_transactions: int
    successful_payments: int
    failed_payments: int
    refund_amount: float
    payment_method_breakdown: Dict[str, Any]
    revenue_trends: List[Dict[str, Any]]
    subscription_metrics: Dict[str, Any]


class DashboardData(BaseModel):
    overview: Dict[str, Any]
    charts: List[Dict[str, Any]]
    alerts: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
    system_metrics: Dict[str, Any]
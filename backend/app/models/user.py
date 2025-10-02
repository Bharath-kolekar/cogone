"""
User models for Voice-to-App SaaS Platform
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class SubscriptionTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    PENDING = "pending"


class OAuthProvider(str, Enum):
    GOOGLE = "google"
    GITHUB = "github"
    FACEBOOK = "facebook"


class UserBase(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferred_language: str = "en"
    country_code: str = "IN"
    timezone: str = "Asia/Kolkata"


class UserCreate(UserBase):
    password: Optional[str] = None
    signup_via: OAuthProvider = OAuthProvider.GOOGLE


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    preferred_language: Optional[str] = None
    country_code: Optional[str] = None
    timezone: Optional[str] = None


class User(UserBase):
    id: str
    signup_via: OAuthProvider
    subscription_tier: SubscriptionTier
    subscription_status: SubscriptionStatus
    points: int = 0
    level: int = 1
    referral_code: Optional[str] = None
    referred_by: Optional[str] = None
    is_active: bool = True
    last_login_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserStats(BaseModel):
    total_apps: int = 0
    total_payments: int = 0
    total_referrals: int = 0
    total_points_earned: int = 0
    current_streak: int = 0
    longest_streak: int = 0
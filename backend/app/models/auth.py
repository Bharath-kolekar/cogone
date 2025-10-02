"""
Authentication models for Voice-to-App SaaS Platform
"""

from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class OTPType(str, Enum):
    EMAIL = "email"
    MOBILE = "mobile"


class LoginRequest(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    otp_code: Optional[str] = None
    otp_type: Optional[OTPType] = None


class LoginResponse(BaseModel):
    user: "User"
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"


class OTPRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    otp_type: OTPType


class OTPVerifyRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    otp_type: OTPType
    otp_code: str


class OTPVerifyResponse(BaseModel):
    user: "User"
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: str
    email: str
    subscription_tier: str
    exp: datetime


# Import User here to avoid circular imports
from app.models.user import User

# Update forward references
LoginResponse.model_rebuild()
OTPVerifyResponse.model_rebuild()
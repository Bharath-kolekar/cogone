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
    two_factor_code: Optional[str] = None


class LoginResponse(BaseModel):
    user: Optional["User"] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: str = "bearer"
    requires_2fa: bool = False
    message: Optional[str] = None


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


class TwoFactorSetupRequest(BaseModel):
    """Request to setup 2FA"""
    pass


class TwoFactorSetupResponse(BaseModel):
    """Response for 2FA setup"""
    secret: str
    qr_code: str
    backup_codes: list[str]
    manual_entry_key: str


class TwoFactorVerifyRequest(BaseModel):
    """Request to verify 2FA setup"""
    code: str


class TwoFactorVerifyResponse(BaseModel):
    """Response for 2FA verification"""
    success: bool
    message: str


class TwoFactorLoginRequest(BaseModel):
    """Request for 2FA during login"""
    user_id: str
    code: str


class TwoFactorLoginResponse(BaseModel):
    """Response for 2FA login"""
    success: bool
    requires_2fa: bool = False
    message: Optional[str] = None


class TwoFactorStatusResponse(BaseModel):
    """Response for 2FA status"""
    enabled: bool
    backup_codes_count: int
    verified_at: Optional[datetime] = None
    created_at: Optional[datetime] = None


class BackupCodesResponse(BaseModel):
    """Response for backup codes"""
    backup_codes: list[str]


# Import User here to avoid circular imports
from app.models.user import User

# Update forward references
LoginResponse.model_rebuild()
OTPVerifyResponse.model_rebuild()
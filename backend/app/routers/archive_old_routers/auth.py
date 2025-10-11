"""
Authentication router for Voice-to-App SaaS Platform
Handles OAuth, OTP (mobile/email), and user management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
import structlog
from datetime import datetime, timedelta
import random
import string

from app.core.config import settings
from app.core.database import get_supabase_client
from app.services.auth_service import AuthService
from app.services.otp_service import OTPService
from app.services.sms_service import SMSService
from app.services.totp_service import TOTPService
from app.models.user import User, UserCreate, UserUpdate
from app.models.auth import (
    LoginRequest,
    LoginResponse,
    OTPRequest,
    OTPVerifyRequest,
    OTPVerifyResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    TwoFactorSetupRequest,
    TwoFactorSetupResponse,
    TwoFactorVerifyRequest,
    TwoFactorVerifyResponse,
    TwoFactorLoginRequest,
    TwoFactorLoginResponse,
    TwoFactorStatusResponse,
    BackupCodesResponse,
)

logger = structlog.get_logger()
router = APIRouter()
security = HTTPBearer()


class AuthDependencies:
    """Authentication dependencies"""
    
    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        """Get current authenticated user"""
        try:
            auth_service = AuthService()
            user = await auth_service.get_user_from_token(credentials.credentials)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )
            return user
        except Exception as e:
            logger.error("Authentication failed", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    
    @staticmethod
    async def check_app_quota(
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ) -> User:
        """Check if user has app quota available"""
        # Get current user first
        current_user = await AuthDependencies.get_current_user(credentials)
        # Simplified quota check - in production, check against database
        return current_user


@router.post("/register", response_model=LoginResponse)
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        auth_service = AuthService()
        result = await auth_service.register_user(user_data)
        
        logger.info("User registered successfully", user_id=result.user.id)
        return result
        
    except Exception as e:
        logger.error("Registration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    """Login user with email/password or OAuth"""
    try:
        auth_service = AuthService()
        result = await auth_service.login_user(login_data)
        
        logger.info("User logged in successfully", user_id=result.user.id)
        return result
        
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/otp/request", response_model=Dict[str, str])
async def request_otp(otp_request: OTPRequest):
    """Request OTP for mobile or email verification"""
    try:
        otp_service = OTPService()
        
        # Generate 6-digit OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        if otp_request.otp_type == "mobile":
            # Send SMS OTP
            sms_service = SMSService()
            await sms_service.send_otp(otp_request.phone, otp_code)
            message = "OTP sent to your mobile number"
        else:
            # Send Email OTP
            await otp_service.send_email_otp(otp_request.email, otp_code)
            message = "OTP sent to your email address"
        
        # Store OTP in database with expiration
        await otp_service.store_otp(
            email=otp_request.email,
            phone=otp_request.phone,
            otp_type=otp_request.otp_type,
            otp_code=otp_code
        )
        
        logger.info("OTP requested", type=otp_request.otp_type)
        return {"message": message, "status": "success"}
        
    except Exception as e:
        logger.error("OTP request failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/otp/verify", response_model=OTPVerifyResponse)
async def verify_otp(otp_verify: OTPVerifyRequest):
    """Verify OTP and complete authentication"""
    try:
        otp_service = OTPService()
        
        # Verify OTP
        is_valid = await otp_service.verify_otp(
            email=otp_verify.email,
            phone=otp_verify.phone,
            otp_type=otp_verify.otp_type,
            otp_code=otp_verify.otp_code
        )
        
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired OTP"
            )
        
        # Create or get user
        auth_service = AuthService()
        user = await auth_service.get_or_create_user_from_otp(otp_verify)
        
        # Generate tokens
        tokens = await auth_service.generate_tokens(user)
        
        logger.info("OTP verified successfully", user_id=user.id)
        return OTPVerifyResponse(
            user=user,
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            expires_in=tokens["expires_in"]
        )
        
    except Exception as e:
        logger.error("OTP verification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(refresh_request: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    try:
        auth_service = AuthService()
        tokens = await auth_service.refresh_tokens(refresh_request.refresh_token)
        
        logger.info("Token refreshed successfully")
        return tokens
        
    except Exception as e:
        logger.error("Token refresh failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/logout")
async def logout(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Logout user and invalidate tokens"""
    try:
        auth_service = AuthService()
        await auth_service.logout_user(current_user.id)
        
        logger.info("User logged out", user_id=current_user.id)
        return {"message": "Logged out successfully"}
        
    except Exception as e:
        logger.error("Logout failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=User)
async def get_current_user_profile(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=User)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Update current user profile"""
    try:
        auth_service = AuthService()
        updated_user = await auth_service.update_user(current_user.id, user_update)
        
        logger.info("User profile updated", user_id=current_user.id)
        return updated_user
        
    except Exception as e:
        logger.error("Profile update failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/me")
async def delete_current_user_account(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Delete current user account"""
    try:
        auth_service = AuthService()
        await auth_service.delete_user(current_user.id)
        
        logger.info("User account deleted", user_id=current_user.id)
        return {"message": "Account deleted successfully"}
        
    except Exception as e:
        logger.error("Account deletion failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/oauth/{provider}")
async def oauth_login(provider: str):
    """Initiate OAuth login with provider (Google, GitHub)"""
    try:
        auth_service = AuthService()
        auth_url = await auth_service.get_oauth_url(provider)
        
        return {"auth_url": auth_url}
        
    except Exception as e:
        logger.error("OAuth login failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/oauth/{provider}/callback")
async def oauth_callback(provider: str, code: str):
    """Handle OAuth callback"""
    try:
        auth_service = AuthService()
        result = await auth_service.handle_oauth_callback(provider, code)
        
        logger.info("OAuth callback successful", provider=provider, user_id=result.user.id)
        return result
        
    except Exception as e:
        logger.error("OAuth callback failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/language-toggle")
async def get_supported_languages():
    """Get supported languages for the app"""
    return {
        "languages": [
            {"code": "en", "name": "English", "native_name": "English"},
            {"code": "hi", "name": "Hindi", "native_name": "हिन्दी"},
            {"code": "ta", "name": "Tamil", "native_name": "தமிழ்"},
            {"code": "te", "name": "Telugu", "native_name": "తెలుగు"},
            {"code": "bn", "name": "Bengali", "native_name": "বাংলা"},
            {"code": "mr", "name": "Marathi", "native_name": "मराठी"},
            {"code": "gu", "name": "Gujarati", "native_name": "ગુજરાતી"},
            {"code": "kn", "name": "Kannada", "native_name": "ಕನ್ನಡ"},
            {"code": "ml", "name": "Malayalam", "native_name": "മലയാളം"},
            {"code": "pa", "name": "Punjabi", "native_name": "ਪੰਜਾਬੀ"},
        ],
        "default": "en"
    }


# ===== Two-Factor Authentication Endpoints =====

@router.post("/2fa/setup", response_model=TwoFactorSetupResponse)
async def setup_2fa(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Setup 2FA for authenticated user"""
    try:
        totp_service = TOTPService()
        
        # Check if 2FA is already enabled
        status = await totp_service.get_2fa_status(current_user.id)
        if status["enabled"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="2FA is already enabled for this user"
            )
        
        # Setup 2FA
        result = await totp_service.setup_2fa(current_user.id, current_user.email)
        
        logger.info("2FA setup initiated", user_id=current_user.id)
        return TwoFactorSetupResponse(**result)
        
    except Exception as e:
        logger.error("2FA setup failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/2fa/verify", response_model=TwoFactorVerifyResponse)
async def verify_2fa_setup(
    verify_request: TwoFactorVerifyRequest,
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Verify 2FA setup with TOTP code"""
    try:
        totp_service = TOTPService()
        
        # Verify and enable 2FA
        success = await totp_service.verify_and_enable_2fa(current_user.id, verify_request.code)
        
        if success:
            logger.info("2FA verified and enabled", user_id=current_user.id)
            return TwoFactorVerifyResponse(
                success=True,
                message="2FA has been successfully enabled"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid TOTP code"
            )
        
    except Exception as e:
        logger.error("2FA verification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/2fa/status", response_model=TwoFactorStatusResponse)
async def get_2fa_status(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Get 2FA status for authenticated user"""
    try:
        totp_service = TOTPService()
        status = await totp_service.get_2fa_status(current_user.id)
        
        return TwoFactorStatusResponse(**status)
        
    except Exception as e:
        logger.error("Failed to get 2FA status", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/2fa/disable")
async def disable_2fa(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Disable 2FA for authenticated user"""
    try:
        totp_service = TOTPService()
        
        # Disable 2FA
        success = await totp_service.disable_2fa(current_user.id)
        
        if success:
            logger.info("2FA disabled", user_id=current_user.id)
            return {"message": "2FA has been disabled"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to disable 2FA"
            )
        
    except Exception as e:
        logger.error("2FA disable failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/2fa/backup-codes", response_model=BackupCodesResponse)
async def regenerate_backup_codes(
    current_user: User = Depends(AuthDependencies.get_current_user)
):
    """Regenerate backup codes for authenticated user"""
    try:
        totp_service = TOTPService()
        
        # Regenerate backup codes
        new_codes = await totp_service.regenerate_backup_codes(current_user.id)
        
        logger.info("Backup codes regenerated", user_id=current_user.id)
        return BackupCodesResponse(backup_codes=new_codes)
        
    except Exception as e:
        logger.error("Backup codes regeneration failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/2fa/verify-login", response_model=TwoFactorLoginResponse)
async def verify_2fa_login(login_request: TwoFactorLoginRequest):
    """Verify 2FA code during login"""
    try:
        totp_service = TOTPService()
        
        # Verify 2FA code
        is_valid = await totp_service.verify_2fa_code(login_request.user_id, login_request.code)
        
        if is_valid:
            # Get user and generate tokens
            auth_service = AuthService()
            user_profile = auth_service.supabase.table("users").select("*").eq("id", login_request.user_id).execute()
            
            if user_profile.data:
                user = User(**user_profile.data[0])
                tokens = await auth_service.generate_tokens(type('User', (), {"id": user.id, "email": user.email})())
                
                return TwoFactorLoginResponse(
                    success=True,
                    message="2FA verification successful"
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
        else:
            return TwoFactorLoginResponse(
                success=False,
                message="Invalid 2FA code"
            )
        
    except Exception as e:
        logger.error("2FA login verification failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint for auth service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "auth",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

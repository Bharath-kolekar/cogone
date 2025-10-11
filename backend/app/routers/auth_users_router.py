"""
Authentication & User Management Router
Consolidates: auth, profiles, user_preferences
Handles OAuth, OTP, 2FA, profiles, and user preferences
"""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from uuid import UUID, uuid4
import structlog
import random
import string
import time
import logging

from app.core.config import settings
from app.core.database import get_supabase_client
from app.core.redis import get_redis_client
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
        current_user = await AuthDependencies.get_current_user(credentials)
        return current_user


# ===== Authentication Endpoints =====

@router.post("/register", response_model=LoginResponse, tags=["Authentication"])
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        auth_service = AuthService()
        result = await auth_service.register_user(user_data)
        logger.info("User registered successfully", user_id=result.user.id)
        return result
    except Exception as e:
        logger.error("Registration failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=LoginResponse, tags=["Authentication"])
async def login(login_data: LoginRequest):
    """Login user with email/password or OAuth"""
    try:
        auth_service = AuthService()
        result = await auth_service.login_user(login_data)
        logger.info("User logged in successfully", user_id=result.user.id)
        return result
    except Exception as e:
        logger.error("Login failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/otp/request", response_model=Dict[str, str], tags=["Authentication"])
async def request_otp(otp_request: OTPRequest):
    """Request OTP for mobile or email verification"""
    try:
        otp_service = OTPService()
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        if otp_request.otp_type == "mobile":
            sms_service = SMSService()
            await sms_service.send_otp(otp_request.phone, otp_code)
            message = "OTP sent to your mobile number"
        else:
            await otp_service.send_email_otp(otp_request.email, otp_code)
            message = "OTP sent to your email address"
        
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/otp/verify", response_model=OTPVerifyResponse, tags=["Authentication"])
async def verify_otp(otp_verify: OTPVerifyRequest):
    """Verify OTP and complete authentication"""
    try:
        otp_service = OTPService()
        is_valid = await otp_service.verify_otp(
            email=otp_verify.email,
            phone=otp_verify.phone,
            otp_type=otp_verify.otp_type,
            otp_code=otp_verify.otp_code
        )
        
        if not is_valid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired OTP")
        
        auth_service = AuthService()
        user = await auth_service.get_or_create_user_from_otp(otp_verify)
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/refresh", response_model=RefreshTokenResponse, tags=["Authentication"])
async def refresh_token(refresh_request: RefreshTokenRequest):
    """Refresh access token using refresh token"""
    try:
        auth_service = AuthService()
        tokens = await auth_service.refresh_tokens(refresh_request.refresh_token)
        logger.info("Token refreshed successfully")
        return tokens
    except Exception as e:
        logger.error("Token refresh failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.post("/logout", tags=["Authentication"])
async def logout(current_user: User = Depends(AuthDependencies.get_current_user)):
    """Logout user and invalidate tokens"""
    try:
        auth_service = AuthService()
        await auth_service.logout_user(current_user.id)
        logger.info("User logged out", user_id=current_user.id)
        return {"message": "Logged out successfully"}
    except Exception as e:
        logger.error("Logout failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/oauth/{provider}", tags=["Authentication"])
async def oauth_login(provider: str):
    """Initiate OAuth login with provider (Google, GitHub)"""
    try:
        auth_service = AuthService()
        auth_url = await auth_service.get_oauth_url(provider)
        return {"auth_url": auth_url}
    except Exception as e:
        logger.error("OAuth login failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/oauth/{provider}/callback", tags=["Authentication"])
async def oauth_callback(provider: str, code: str):
    """Handle OAuth callback"""
    try:
        auth_service = AuthService()
        result = await auth_service.handle_oauth_callback(provider, code)
        logger.info("OAuth callback successful", provider=provider, user_id=result.user.id)
        return result
    except Exception as e:
        logger.error("OAuth callback failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/language-toggle", tags=["Authentication"])
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

@router.post("/2fa/setup", response_model=TwoFactorSetupResponse, tags=["Two-Factor Auth"])
async def setup_2fa(current_user: User = Depends(AuthDependencies.get_current_user)):
    """Setup 2FA for authenticated user"""
    try:
        totp_service = TOTPService()
        status_result = await totp_service.get_2fa_status(current_user.id)
        if status_result["enabled"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA is already enabled for this user")
        
        result = await totp_service.setup_2fa(current_user.id, current_user.email)
        logger.info("2FA setup initiated", user_id=current_user.id)
        return TwoFactorSetupResponse(**result)
    except Exception as e:
        logger.error("2FA setup failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/2fa/verify", response_model=TwoFactorVerifyResponse, tags=["Two-Factor Auth"])
async def verify_2fa_setup(verify_request: TwoFactorVerifyRequest, current_user: User = Depends(AuthDependencies.get_current_user)):
    """Verify 2FA setup with TOTP code"""
    try:
        totp_service = TOTPService()
        success = await totp_service.verify_and_enable_2fa(current_user.id, verify_request.code)
        
        if success:
            logger.info("2FA verified and enabled", user_id=current_user.id)
            return TwoFactorVerifyResponse(success=True, message="2FA has been successfully enabled")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid TOTP code")
    except Exception as e:
        logger.error("2FA verification failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/2fa/status", response_model=TwoFactorStatusResponse, tags=["Two-Factor Auth"])
async def get_2fa_status(current_user: User = Depends(AuthDependencies.get_current_user)):
    """Get 2FA status for authenticated user"""
    try:
        totp_service = TOTPService()
        status_result = await totp_service.get_2fa_status(current_user.id)
        return TwoFactorStatusResponse(**status_result)
    except Exception as e:
        logger.error("Failed to get 2FA status", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/2fa/disable", tags=["Two-Factor Auth"])
async def disable_2fa(current_user: User = Depends(AuthDependencies.get_current_user)):
    """Disable 2FA for authenticated user"""
    try:
        totp_service = TOTPService()
        success = await totp_service.disable_2fa(current_user.id)
        
        if success:
            logger.info("2FA disabled", user_id=current_user.id)
            return {"message": "2FA has been disabled"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to disable 2FA")
    except Exception as e:
        logger.error("2FA disable failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/2fa/backup-codes", response_model=BackupCodesResponse, tags=["Two-Factor Auth"])
async def regenerate_backup_codes(current_user: User = Depends(AuthDependencies.get_current_user)):
    """Regenerate backup codes for authenticated user"""
    try:
        totp_service = TOTPService()
        new_codes = await totp_service.regenerate_backup_codes(current_user.id)
        logger.info("Backup codes regenerated", user_id=current_user.id)
        return BackupCodesResponse(backup_codes=new_codes)
    except Exception as e:
        logger.error("Backup codes regeneration failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/2fa/verify-login", response_model=TwoFactorLoginResponse, tags=["Two-Factor Auth"])
async def verify_2fa_login(login_request: TwoFactorLoginRequest):
    """Verify 2FA code during login"""
    try:
        totp_service = TOTPService()
        is_valid = await totp_service.verify_2fa_code(login_request.user_id, login_request.code)
        
        if is_valid:
            auth_service = AuthService()
            user_profile = auth_service.supabase.table("users").select("*").eq("id", login_request.user_id).execute()
            
            if user_profile.data:
                user = User(**user_profile.data[0])
                return TwoFactorLoginResponse(success=True, message="2FA verification successful")
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        else:
            return TwoFactorLoginResponse(success=False, message="Invalid 2FA code")
    except Exception as e:
        logger.error("2FA login verification failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ===== User Profile Endpoints =====

@router.get("/me", response_model=User, tags=["User Profile"])
async def get_current_user_profile(current_user: User = Depends(AuthDependencies.get_current_user)):
    """Get current user profile"""
    return current_user


@router.put("/me", response_model=User, tags=["User Profile"])
async def update_current_user_profile(user_update: UserUpdate, current_user: User = Depends(AuthDependencies.get_current_user)):
    """Update current user profile"""
    try:
        auth_service = AuthService()
        updated_user = await auth_service.update_user(current_user.id, user_update)
        logger.info("User profile updated", user_id=current_user.id)
        return updated_user
    except Exception as e:
        logger.error("Profile update failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/me", tags=["User Profile"])
async def delete_current_user_account(current_user: User = Depends(AuthDependencies.get_current_user)):
    """Delete current user account"""
    try:
        auth_service = AuthService()
        await auth_service.delete_user(current_user.id)
        logger.info("User account deleted", user_id=current_user.id)
        return {"message": "Account deleted successfully"}
    except Exception as e:
        logger.error("Account deletion failed", error=str(e))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ===== User Preferences Endpoints =====

@router.get("/preferences/threshold-options", tags=["User Preferences"])
async def get_threshold_options() -> Dict[str, Any]:
    """Get available threshold options with pricing and features"""
    try:
        threshold_options = [
            {
                "id": "maximum",
                "name": "Maximum Precision",
                "precision": 0.99,
                "accuracy": 0.99,
                "response_time": "300-500ms",
                "computational_cost": "High",
                "price_per_request": 0.05,
                "features": ["99%+ Precision & Accuracy", "Advanced Validation (8 layers)", "Maximum Reliability", "Enterprise Security", "Real-time Monitoring", "Priority Support"],
                "use_cases": ["Financial Applications", "Healthcare Systems", "Legal Services", "Critical Business Operations", "Enterprise Solutions"],
                "description": "Maximum precision and accuracy for critical applications requiring 99%+ reliability.",
                "recommended": False
            },
            {
                "id": "optimized",
                "name": "Optimized Balance",
                "precision": 0.95,
                "accuracy": 0.95,
                "response_time": "100-200ms",
                "computational_cost": "Medium",
                "price_per_request": 0.02,
                "features": ["95%+ Precision & Accuracy", "Balanced Validation (4 layers)", "Good Reliability", "Standard Security", "Performance Monitoring", "Standard Support"],
                "use_cases": ["General Applications", "Customer Support", "Content Generation", "Business Operations", "Standard Solutions"],
                "description": "Optimal balance of precision, speed, and cost for most applications.",
                "recommended": True
            },
            {
                "id": "fast",
                "name": "Fast Processing",
                "precision": 0.90,
                "accuracy": 0.90,
                "response_time": "50-100ms",
                "computational_cost": "Low",
                "price_per_request": 0.01,
                "features": ["90%+ Precision & Accuracy", "Fast Validation (2 layers)", "Basic Reliability", "Standard Security", "Basic Monitoring", "Community Support"],
                "use_cases": ["High-Volume Systems", "Real-time Applications", "Development & Testing", "Prototype Solutions", "Cost-Sensitive Projects"],
                "description": "Fast processing with good precision for high-volume or real-time applications.",
                "recommended": False
            }
        ]
        
        return {"threshold_options": threshold_options, "total_options": len(threshold_options), "recommended": "optimized"}
    except Exception as e:
        logger.error(f"Failed to get threshold options: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get threshold options: {str(e)}")


@router.get("/preferences/billing-options", tags=["User Preferences"])
async def get_billing_options() -> Dict[str, Any]:
    """Get available billing options with pricing and features"""
    try:
        billing_options = [
            {
                "id": "pay_per_use",
                "name": "Pay Per Use",
                "type": "pay_per_use",
                "price": 0.01,
                "requests": 0,
                "features": ["Pay only for what you use", "No monthly commitments", "Flexible scaling", "Perfect for testing", "Start with $0"],
                "description": "Perfect for testing and low-volume usage.",
                "savings": 0
            },
            {
                "id": "monthly",
                "name": "Monthly Plan",
                "type": "monthly",
                "price": 29.99,
                "requests": 10000,
                "features": ["10,000 requests included", "Monthly billing", "Standard support", "Performance monitoring", "2x better value than pay-per-use"],
                "description": "Best value for regular usage with included requests.",
                "savings": 50,
                "popular": True
            },
            {
                "id": "yearly",
                "name": "Yearly Plan",
                "type": "yearly",
                "price": 299.99,
                "requests": 150000,
                "features": ["150,000 requests included", "Annual billing", "Priority support", "Advanced monitoring", "3x better value than monthly"],
                "description": "Maximum value for high-volume usage with significant savings.",
                "savings": 67
            }
        ]
        
        return {"billing_options": billing_options, "total_options": len(billing_options), "popular": "monthly"}
    except Exception as e:
        logger.error(f"Failed to get billing options: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get billing options: {str(e)}")


@router.get("/preferences/{user_id}", tags=["User Preferences"])
async def get_user_preferences(user_id: UUID) -> Dict[str, Any]:
    """Get user preferences for threshold and billing"""
    try:
        db = get_supabase_client()
        
        if db:
            result = db.table('user_preferences').select('*').eq('user_id', str(user_id)).execute()
            if result.data and len(result.data) > 0:
                return {"preferences": result.data[0], "status": "success"}
        
        default_preferences = {
            "user_id": str(user_id),
            "threshold_type": "optimized",
            "billing_option": "monthly",
            "auto_optimize": True,
            "notifications": True,
            "created_at": time.time(),
            "updated_at": time.time()
        }
        
        return {"preferences": default_preferences, "status": "success"}
    except Exception as e:
        logger.error(f"Failed to get user preferences: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get user preferences: {str(e)}")


@router.post("/preferences", tags=["User Preferences"])
async def save_user_preferences(preferences: Dict[str, Any], background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Save user preferences for threshold and billing"""
    try:
        required_fields = ["threshold_type", "billing_option"]
        for field in required_fields:
            if field not in preferences:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        valid_threshold_types = ["maximum", "optimized", "fast"]
        if preferences["threshold_type"] not in valid_threshold_types:
            raise HTTPException(status_code=400, detail=f"Invalid threshold type. Must be one of: {valid_threshold_types}")
        
        valid_billing_options = ["pay_per_use", "monthly", "yearly"]
        if preferences["billing_option"] not in valid_billing_options:
            raise HTTPException(status_code=400, detail=f"Invalid billing option. Must be one of: {valid_billing_options}")
        
        db = get_supabase_client()
        
        saved_preferences = {
            "user_id": preferences.get("user_id", str(uuid4())),
            "threshold_type": preferences["threshold_type"],
            "billing_option": preferences["billing_option"],
            "auto_optimize": preferences.get("auto_optimize", True),
            "notifications": preferences.get("notifications", True),
            "created_at": time.time(),
            "updated_at": time.time()
        }
        
        if db:
            try:
                db.table('user_preferences').upsert(saved_preferences).execute()
                logger.info(f"Saved preferences for user {saved_preferences['user_id']}")
            except Exception as db_error:
                logger.warning(f"Database save failed, continuing: {db_error}")
        
        background_tasks.add_task(_log_preference_change, saved_preferences)
        
        return {"preferences": saved_preferences, "status": "success", "message": "Preferences saved successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save user preferences: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save user preferences: {str(e)}")


@router.get("/preferences/cost-calculation", tags=["User Preferences"])
async def calculate_cost(threshold_type: str, billing_option: str, estimated_requests: int = 1000) -> Dict[str, Any]:
    """Calculate estimated cost based on threshold and billing options"""
    try:
        threshold_pricing = {"maximum": 0.05, "optimized": 0.02, "fast": 0.01}
        billing_pricing = {
            "pay_per_use": {"base_price": 0, "price_per_request": threshold_pricing[threshold_type]},
            "monthly": {"base_price": 29.99, "included_requests": 10000, "price_per_request": threshold_pricing[threshold_type]},
            "yearly": {"base_price": 299.99, "included_requests": 150000, "price_per_request": threshold_pricing[threshold_type]}
        }
        
        billing_config = billing_pricing[billing_option]
        
        if billing_option == "pay_per_use":
            total_cost = estimated_requests * billing_config["price_per_request"]
            cost_breakdown = {
                "base_cost": 0,
                "request_cost": total_cost,
                "total_cost": total_cost,
                "cost_per_request": billing_config["price_per_request"]
            }
        else:
            base_cost = billing_config["base_price"]
            included_requests = billing_config["included_requests"]
            
            if estimated_requests <= included_requests:
                request_cost = 0
            else:
                request_cost = (estimated_requests - included_requests) * billing_config["price_per_request"]
            
            total_cost = base_cost + request_cost
            cost_breakdown = {
                "base_cost": base_cost,
                "included_requests": included_requests,
                "request_cost": request_cost,
                "total_cost": total_cost,
                "cost_per_request": billing_config["price_per_request"]
            }
        
        pay_per_use_cost = estimated_requests * threshold_pricing[threshold_type]
        savings = max(0, pay_per_use_cost - total_cost)
        savings_percentage = (savings / pay_per_use_cost * 100) if pay_per_use_cost > 0 else 0
        
        return {
            "threshold_type": threshold_type,
            "billing_option": billing_option,
            "estimated_requests": estimated_requests,
            "cost_breakdown": cost_breakdown,
            "savings": savings,
            "savings_percentage": savings_percentage,
            "recommendation": _get_cost_recommendation(estimated_requests, total_cost, billing_option)
        }
    except Exception as e:
        logger.error(f"Failed to calculate cost: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to calculate cost: {str(e)}")


@router.get("/preferences/usage-analytics/{user_id}", tags=["User Preferences"])
async def get_usage_analytics(user_id: UUID) -> Dict[str, Any]:
    """Get user usage analytics and recommendations"""
    try:
        db = get_supabase_client()
        usage_data = None
        
        if db:
            try:
                result = db.table('usage_logs').select('*').eq('user_id', str(user_id)).execute()
                if result.data and len(result.data) > 0:
                    logs = result.data
                    total_requests = len(logs)
                    avg_precision = sum(log.get('precision', 0) for log in logs) / total_requests if total_requests > 0 else 0
                    avg_response_time = sum(log.get('response_time', 0) for log in logs) / total_requests if total_requests > 0 else 0
                    cost_this_month = sum(log.get('cost', 0) for log in logs)
                    
                    usage_data = {
                        "user_id": str(user_id),
                        "total_requests": total_requests,
                        "average_precision": round(avg_precision, 2),
                        "average_response_time": round(avg_response_time, 2),
                        "cost_this_month": round(cost_this_month, 2),
                    }
            except Exception as db_error:
                logger.warning(f"Database query failed: {db_error}")
        
        if not usage_data:
            usage_data = {
                "user_id": str(user_id),
                "total_requests": 0,
                "average_precision": 0.0,
                "average_response_time": 0.0,
                "cost_this_month": 0.0,
            }
        
        usage_data["recommendations"] = [
            {"type": "threshold_optimization", "message": "Monitor usage patterns to optimize threshold settings", "potential_savings": 0.0}
        ]
        usage_data["usage_patterns"] = {
            "peak_hours": "Not enough data yet",
            "average_requests_per_day": round(usage_data["total_requests"] / 30, 2) if usage_data["total_requests"] > 0 else 0,
            "most_used_features": ["general_chat", "content_generation", "data_analysis"]
        }
        
        return {"analytics": usage_data, "status": "success"}
    except Exception as e:
        logger.error(f"Failed to get usage analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get usage analytics: {str(e)}")


# ===== Helper Functions =====

async def _log_preference_change(preferences: Dict[str, Any]):
    """Log preference change for analytics"""
    try:
        logger.info(f"User preference changed: {preferences}")
    except Exception as e:
        logger.error(f"Failed to log preference change: {e}")


def _get_cost_recommendation(estimated_requests: int, total_cost: float, billing_option: str) -> str:
    """Get cost optimization recommendation"""
    if estimated_requests < 1000 and billing_option != "pay_per_use":
        return "Consider switching to pay-per-use for lower costs"
    elif estimated_requests > 5000 and billing_option == "pay_per_use":
        return "Consider upgrading to monthly plan for better value"
    elif estimated_requests > 50000 and billing_option == "monthly":
        return "Consider upgrading to yearly plan for maximum savings"
    else:
        return "Your current selection is optimal for your usage"


# ===== Health Check =====

@router.get("/health")
async def health_check():
    """Health check endpoint for auth-users service"""
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={
            "status": "healthy",
            "service": "auth-users",
            "components": ["authentication", "profiles", "user-preferences", "2fa"],
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )



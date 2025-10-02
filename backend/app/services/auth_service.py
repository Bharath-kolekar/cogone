"""
Authentication service for Voice-to-App SaaS Platform
"""

import structlog
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.database import get_supabase_client
from app.models.user import User, UserCreate, UserUpdate
from app.models.auth import LoginRequest, LoginResponse, TokenData

logger = structlog.get_logger()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
    
    async def register_user(self, user_data: UserCreate) -> LoginResponse:
        """Register a new user"""
        try:
            # Hash password if provided
            if user_data.password:
                hashed_password = pwd_context.hash(user_data.password)
            else:
                hashed_password = None
            
            # Create user in Supabase
            auth_response = self.supabase.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password,
                "options": {
                    "data": {
                        "full_name": user_data.full_name,
                        "phone": user_data.phone,
                        "signup_via": user_data.signup_via.value,
                        "preferred_language": user_data.preferred_language,
                        "country_code": user_data.country_code,
                        "timezone": user_data.timezone,
                    }
                }
            })
            
            if auth_response.user:
                # Create user profile
                user_profile = {
                    "id": auth_response.user.id,
                    "email": user_data.email,
                    "phone": user_data.phone,
                    "full_name": user_data.full_name,
                    "signup_via": user_data.signup_via.value,
                    "preferred_language": user_data.preferred_language,
                    "country_code": user_data.country_code,
                    "timezone": user_data.timezone,
                    "subscription_tier": "free",
                    "subscription_status": "active",
                    "points": 0,
                    "level": 1,
                    "is_active": True,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }
                
                self.supabase.table("users").insert(user_profile).execute()
                
                # Generate tokens
                tokens = await self.generate_tokens(auth_response.user)
                
                return LoginResponse(
                    user=User(**user_profile),
                    access_token=tokens["access_token"],
                    refresh_token=tokens["refresh_token"],
                    expires_in=tokens["expires_in"]
                )
            else:
                raise Exception("Failed to create user")
                
        except Exception as e:
            logger.error("User registration failed", error=str(e))
            raise e
    
    async def login_user(self, login_data: LoginRequest) -> LoginResponse:
        """Login user with email/password or OTP"""
        try:
            if login_data.password:
                # Password login
                auth_response = self.supabase.auth.sign_in_with_password({
                    "email": login_data.email,
                    "password": login_data.password
                })
            elif login_data.otp_code:
                # OTP login
                auth_response = self.supabase.auth.verify_otp({
                    "email": login_data.email,
                    "token": login_data.otp_code,
                    "type": "email"
                })
            else:
                raise Exception("Either password or OTP code is required")
            
            if auth_response.user:
                # Get user profile
                user_profile = self.supabase.table("users").select("*").eq("id", auth_response.user.id).execute()
                
                if user_profile.data:
                    user = User(**user_profile.data[0])
                    
                    # Update last login
                    self.supabase.table("users").update({
                        "last_login_at": datetime.utcnow().isoformat()
                    }).eq("id", user.id).execute()
                    
                    # Generate tokens
                    tokens = await self.generate_tokens(auth_response.user)
                    
                    return LoginResponse(
                        user=user,
                        access_token=tokens["access_token"],
                        refresh_token=tokens["refresh_token"],
                        expires_in=tokens["expires_in"]
                    )
                else:
                    raise Exception("User profile not found")
            else:
                raise Exception("Login failed")
                
        except Exception as e:
            logger.error("User login failed", error=str(e))
            raise e
    
    async def generate_tokens(self, user) -> Dict[str, Any]:
        """Generate JWT tokens"""
        try:
            now = datetime.utcnow()
            access_exp = now + timedelta(hours=1)
            refresh_exp = now + timedelta(days=30)
            
            # Access token payload
            access_payload = {
                "user_id": user.id,
                "email": user.email,
                "exp": access_exp,
                "iat": now,
                "type": "access"
            }
            
            # Refresh token payload
            refresh_payload = {
                "user_id": user.id,
                "email": user.email,
                "exp": refresh_exp,
                "iat": now,
                "type": "refresh"
            }
            
            # Generate tokens
            access_token = jwt.encode(access_payload, settings.JWT_SECRET, algorithm="HS256")
            refresh_token = jwt.encode(refresh_payload, settings.JWT_SECRET, algorithm="HS256")
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_in": 3600,
                "token_type": "bearer"
            }
            
        except Exception as e:
            logger.error("Token generation failed", error=str(e))
            raise e
    
    async def refresh_tokens(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        try:
            # Decode refresh token
            payload = jwt.decode(refresh_token, settings.JWT_SECRET, algorithms=["HS256"])
            
            if payload.get("type") != "refresh":
                raise Exception("Invalid token type")
            
            # Get user
            user_id = payload.get("user_id")
            user_profile = self.supabase.table("users").select("*").eq("id", user_id).execute()
            
            if user_profile.data:
                user = user_profile.data[0]
                
                # Generate new tokens
                tokens = await self.generate_tokens(type('User', (), user)())
                
                return {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "expires_in": tokens["expires_in"],
                    "token_type": "bearer"
                }
            else:
                raise Exception("User not found")
                
        except Exception as e:
            logger.error("Token refresh failed", error=str(e))
            raise e
    
    async def get_user_from_token(self, token: str) -> Optional[User]:
        """Get user from JWT token"""
        try:
            # Decode token
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
            
            if payload.get("type") != "access":
                return None
            
            # Get user profile
            user_id = payload.get("user_id")
            user_profile = self.supabase.table("users").select("*").eq("id", user_id).execute()
            
            if user_profile.data:
                return User(**user_profile.data[0])
            else:
                return None
                
        except Exception as e:
            logger.error("Token validation failed", error=str(e))
            return None
    
    async def logout_user(self, user_id: str) -> bool:
        """Logout user and invalidate tokens"""
        try:
            # In a real implementation, you would add tokens to a blacklist
            # For now, we'll just log the logout
            logger.info("User logged out", user_id=user_id)
            return True
            
        except Exception as e:
            logger.error("Logout failed", error=str(e))
            return False
    
    async def update_user(self, user_id: str, user_update: UserUpdate) -> User:
        """Update user profile"""
        try:
            # Update user profile
            update_data = user_update.dict(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            result = self.supabase.table("users").update(update_data).eq("id", user_id).execute()
            
            if result.data:
                return User(**result.data[0])
            else:
                raise Exception("User update failed")
                
        except Exception as e:
            logger.error("User update failed", error=str(e))
            raise e
    
    async def delete_user(self, user_id: str) -> bool:
        """Delete user account"""
        try:
            # Delete user profile
            self.supabase.table("users").delete().eq("id", user_id).execute()
            
            # Delete auth user
            self.supabase.auth.admin.delete_user(user_id)
            
            logger.info("User account deleted", user_id=user_id)
            return True
            
        except Exception as e:
            logger.error("User deletion failed", error=str(e))
            return False
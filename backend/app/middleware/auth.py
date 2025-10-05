"""
Authentication Middleware for CognOmega Platform
Provides JWT token validation and user authentication
"""

import jwt
import time
from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

class AuthMiddleware:
    """Authentication middleware for JWT token validation"""
    
    def __init__(
        self,
        secret_key: str = "your-secret-key",
        algorithm: str = "HS256",
        token_expire_minutes: int = 30,
        refresh_token_expire_days: int = 7
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expire_minutes = token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        
        # Token blacklist for logout
        self.blacklisted_tokens: set = set()
        
        # User sessions
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
    
    async def __call__(self, request: Request, call_next):
        """Main middleware function"""
        try:
            # Skip auth for public endpoints
            if self._is_public_endpoint(request.url.path):
                return await call_next(request)
            
            # Extract token
            token = await self._extract_token(request)
            
            if not token:
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "Authentication required",
                        "message": "No authentication token provided"
                    }
                )
            
            # Validate token
            user_data = await self._validate_token(token)
            
            if not user_data:
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "Invalid token",
                        "message": "Authentication token is invalid or expired"
                    }
                )
            
            # Add user data to request state
            request.state.user = user_data
            
            # Process request
            response = await call_next(request)
            
            return response
            
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"error": e.detail}
            )
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Authentication error",
                    "message": "Internal server error during authentication"
                }
            )
    
    def _is_public_endpoint(self, path: str) -> bool:
        """Check if endpoint is public (doesn't require authentication)"""
        public_paths = [
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/health",
            "/auth/login",
            "/auth/register",
            "/auth/oauth",
            "/auth/refresh"
        ]
        
        # Check exact matches
        if path in public_paths:
            return True
        
        # Check if path starts with public prefixes
        public_prefixes = ["/static", "/public", "/api/health"]
        return any(path.startswith(prefix) for prefix in public_prefixes)
    
    async def _extract_token(self, request: Request) -> Optional[str]:
        """Extract JWT token from request"""
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        
        # Check cookies
        token_cookie = request.cookies.get("access_token")
        if token_cookie:
            return token_cookie
        
        return None
    
    async def _validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token and return user data"""
        try:
            # Check if token is blacklisted
            if token in self.blacklisted_tokens:
                logger.warning("Blacklisted token used")
                return None
            
            # Decode token
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            # Check expiration
            exp = payload.get("exp")
            if exp and exp < time.time():
                logger.warning("Expired token used")
                return None
            
            # Extract user data
            user_data = {
                "user_id": payload.get("sub"),
                "email": payload.get("email"),
                "username": payload.get("username"),
                "role": payload.get("role", "user"),
                "permissions": payload.get("permissions", []),
                "session_id": payload.get("session_id"),
                "iat": payload.get("iat"),
                "exp": payload.get("exp")
            }
            
            # Validate session
            if not await self._validate_session(user_data["session_id"]):
                logger.warning(f"Invalid session: {user_data['session_id']}")
                return None
            
            return user_data
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            return None
    
    async def _validate_session(self, session_id: str) -> bool:
        """Validate user session"""
        if not session_id:
            return False
        
        # Check if session exists and is active
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        # Check if session is expired
        if session.get("expires_at", 0) < time.time():
            # Remove expired session
            del self.active_sessions[session_id]
            return False
        
        # Update last activity
        session["last_activity"] = time.time()
        
        return True
    
    def create_access_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT access token"""
        now = time.time()
        payload = {
            "sub": user_data.get("user_id"),
            "email": user_data.get("email"),
            "username": user_data.get("username"),
            "role": user_data.get("role", "user"),
            "permissions": user_data.get("permissions", []),
            "session_id": user_data.get("session_id"),
            "iat": now,
            "exp": now + (self.token_expire_minutes * 60)
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_data: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        now = time.time()
        payload = {
            "sub": user_data.get("user_id"),
            "type": "refresh",
            "iat": now,
            "exp": now + (self.refresh_token_expire_days * 24 * 60 * 60)
        }
        
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    async def create_session(self, user_data: Dict[str, Any]) -> str:
        """Create user session"""
        session_id = f"session_{int(time.time())}_{user_data.get('user_id')}"
        
        self.active_sessions[session_id] = {
            "user_id": user_data.get("user_id"),
            "email": user_data.get("email"),
            "username": user_data.get("username"),
            "role": user_data.get("role", "user"),
            "created_at": time.time(),
            "last_activity": time.time(),
            "expires_at": time.time() + (self.token_expire_minutes * 60),
            "ip_address": None,  # Will be set by request context
            "user_agent": None   # Will be set by request context
        }
        
        return session_id
    
    async def invalidate_session(self, session_id: str):
        """Invalidate user session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    async def blacklist_token(self, token: str):
        """Add token to blacklist"""
        self.blacklisted_tokens.add(token)
    
    async def cleanup_expired_sessions(self):
        """Clean up expired sessions and tokens"""
        now = time.time()
        
        # Clean expired sessions
        expired_sessions = [
            session_id for session_id, session in self.active_sessions.items()
            if session.get("expires_at", 0) < now
        ]
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")

# Dependency for getting current user
async def get_current_user(request: Request) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    if not hasattr(request.state, 'user'):
        raise HTTPException(status_code=401, detail="Authentication required")
    
    return request.state.user

# Dependency for getting current user (optional)
async def get_current_user_optional(request: Request) -> Optional[Dict[str, Any]]:
    """Dependency to get current authenticated user (optional)"""
    return getattr(request.state, 'user', None)

# Role-based access control
def require_role(required_role: str):
    """Decorator to require specific role"""
    def role_checker(request: Request):
        user = getattr(request.state, 'user', None)
        if not user:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        user_role = user.get("role", "user")
        if user_role != required_role and user_role != "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return user
    
    return role_checker

# Permission-based access control
def require_permission(required_permission: str):
    """Decorator to require specific permission"""
    def permission_checker(request: Request):
        user = getattr(request.state, 'user', None)
        if not user:
            raise HTTPException(status_code=401, detail="Authentication required")
        
        user_permissions = user.get("permissions", [])
        if required_permission not in user_permissions and "admin" not in user_permissions:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        
        return user
    
    return permission_checker

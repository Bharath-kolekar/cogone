"""
Core Dependencies for CognOmega Platform
Provides dependency injection and authentication utilities
"""

from typing import Optional, Dict, Any, List
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import time
import logging

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer(auto_error=False)

class AuthDependencies:
    """Authentication dependencies for FastAPI"""
    
    def __init__(self, secret_key: str = "your-secret-key"):
        self.secret_key = secret_key
        self.algorithm = "HS256"
    
    async def get_current_user(
        self,
        request: Request,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> Dict[str, Any]:
        """Get current authenticated user"""
        # Check if user is already in request state (from middleware)
        if hasattr(request.state, 'user') and request.state.user:
            return request.state.user
        
        # Fallback to manual token validation
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            payload = jwt.decode(
                credentials.credentials,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return {
                "user_id": user_id,
                "email": payload.get("email"),
                "username": payload.get("username"),
                "role": payload.get("role", "user"),
                "permissions": payload.get("permissions", [])
            }
            
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    async def get_current_user_optional(
        self,
        request: Request,
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> Optional[Dict[str, Any]]:
        """Get current authenticated user (optional)"""
        try:
            return await self.get_current_user(request, credentials)
        except HTTPException:
            return None
    
    def require_role(self, required_role: str):
        """Dependency factory for role-based access control"""
        async def role_checker(
            current_user: Dict[str, Any] = Depends(self.get_current_user)
        ) -> Dict[str, Any]:
            user_role = current_user.get("role", "user")
            if user_role != required_role and user_role != "admin":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required role: {required_role}"
                )
            return current_user
        
        return role_checker
    
    def require_permission(self, required_permission: str):
        """Dependency factory for permission-based access control"""
        async def permission_checker(
            current_user: Dict[str, Any] = Depends(self.get_current_user)
        ) -> Dict[str, Any]:
            user_permissions = current_user.get("permissions", [])
            if required_permission not in user_permissions and "admin" not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required permission: {required_permission}"
                )
            return current_user
        
        return permission_checker
    
    def require_any_permission(self, required_permissions: List[str]):
        """Dependency factory for any-of permissions"""
        async def any_permission_checker(
            current_user: Dict[str, Any] = Depends(self.get_current_user)
        ) -> Dict[str, Any]:
            user_permissions = current_user.get("permissions", [])
            
            # Admin has all permissions
            if "admin" in user_permissions:
                return current_user
            
            # Check if user has any of the required permissions
            if not any(perm in user_permissions for perm in required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required one of: {', '.join(required_permissions)}"
                )
            return current_user
        
        return any_permission_checker
    
    def require_all_permissions(self, required_permissions: List[str]):
        """Dependency factory for all-of permissions"""
        async def all_permission_checker(
            current_user: Dict[str, Any] = Depends(self.get_current_user)
        ) -> Dict[str, Any]:
            user_permissions = current_user.get("permissions", [])
            
            # Admin has all permissions
            if "admin" in user_permissions:
                return current_user
            
            # Check if user has all required permissions
            if not all(perm in user_permissions for perm in required_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions. Required all of: {', '.join(required_permissions)}"
                )
            return current_user
        
        return all_permission_checker

# Global instance
auth_dependencies = AuthDependencies()

# Convenience functions
async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """Get current authenticated user"""
    return await auth_dependencies.get_current_user(request, credentials)

async def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[Dict[str, Any]]:
    """Get current authenticated user (optional)"""
    return await auth_dependencies.get_current_user_optional(request, credentials)

def require_role(required_role: str):
    """Require specific role"""
    return auth_dependencies.require_role(required_role)

def require_permission(required_permission: str):
    """Require specific permission"""
    return auth_dependencies.require_permission(required_permission)

def require_any_permission(required_permissions: List[str]):
    """Require any of the specified permissions"""
    return auth_dependencies.require_any_permission(required_permissions)

def require_all_permissions(required_permissions: List[str]):
    """Require all of the specified permissions"""
    return auth_dependencies.require_all_permissions(required_permissions)

# Common role dependencies
require_admin = require_role("admin")
require_moderator = require_role("moderator")
require_user = require_role("user")

# Common permission dependencies
require_read = require_permission("read")
require_write = require_permission("write")
require_execute = require_permission("execute")
require_admin_access = require_permission("admin")

# Smart Coding AI specific permissions
require_code_read = require_permission("code:read")
require_code_write = require_permission("code:write")
require_code_execute = require_permission("code:execute")
require_memory_access = require_permission("memory:access")
require_analysis_access = require_permission("analysis:access")

# OAuth dependencies
async def get_oauth_user(request: Request) -> Optional[Dict[str, Any]]:
    """Get OAuth user from request state"""
    return getattr(request.state, 'oauth_user', None)

async def require_oauth_user(request: Request) -> Dict[str, Any]:
    """Require OAuth user"""
    oauth_user = await get_oauth_user(request)
    if not oauth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="OAuth authentication required"
        )
    return oauth_user

# Rate limiting dependencies
async def get_rate_limit_status(request: Request) -> Dict[str, Any]:
    """Get rate limit status from request state"""
    return getattr(request.state, 'rate_limit_status', {})

# Request context dependencies
async def get_request_id(request: Request) -> str:
    """Get request ID from request state"""
    return getattr(request.state, 'request_id', 'unknown')

async def get_client_ip(request: Request) -> str:
    """Get client IP address"""
    # Check for forwarded headers first
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct connection
    return request.client.host if request.client else "unknown"

# Session dependencies
async def get_session_id(request: Request) -> Optional[str]:
    """Get session ID from request state"""
    user = getattr(request.state, 'user', None)
    if user:
        return user.get("session_id")
    return None

# Audit dependencies
async def get_audit_context(request: Request) -> Dict[str, Any]:
    """Get audit context for logging"""
    user = getattr(request.state, 'user', None)
    return {
        "user_id": user.get("user_id") if user else None,
        "username": user.get("username") if user else None,
        "role": user.get("role") if user else None,
        "request_id": getattr(request.state, 'request_id', 'unknown'),
        "client_ip": await get_client_ip(request),
        "user_agent": request.headers.get("User-Agent", ""),
        "timestamp": time.time()
    }

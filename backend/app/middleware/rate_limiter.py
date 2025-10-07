"""
Rate Limiting Middleware for CognOmega Platform
Provides rate limiting capabilities for API endpoints
"""

import time
from typing import Dict, Optional
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import asyncio
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)

class RateLimitMiddleware:
    """Rate limiting middleware with configurable limits"""
    
    def __init__(
        self,
        app,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        requests_per_day: int = 10000,
        burst_limit: int = 10
    ):
        self.app = app
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.requests_per_day = requests_per_day
        self.burst_limit = burst_limit
        
        # Store request timestamps for each IP
        self.request_history: Dict[str, Dict[str, deque]] = defaultdict(
            lambda: {
                'minute': deque(),
                'hour': deque(),
                'day': deque(),
                'burst': deque()
            }
        )
        
        # Cleanup task
        self._cleanup_task = None
        
    async def __call__(self, request: Request, call_next):
        """Main middleware function"""
        try:
            # Get client IP
            client_ip = self._get_client_ip(request)
            
            # Check rate limits
            if not await self._check_rate_limits(client_ip):
                return JSONResponse(
                    status_code=429,
                    content={
                        "error": "Rate limit exceeded",
                        "message": "Too many requests. Please try again later.",
                        "retry_after": 60
                    },
                    headers={"Retry-After": "60"}
                )
            
            # Record request
            await self._record_request(client_ip)
            
            # Process request
            response = await call_next(request)
            
            # Add rate limit headers
            response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
            response.headers["X-RateLimit-Remaining"] = str(
                max(0, self.requests_per_minute - len(self.request_history[client_ip]['minute']))
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Rate limiting error: {str(e)}")
            # Continue with request if rate limiting fails
            return await call_next(request)
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address"""
        # Check for forwarded headers first
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"
    
    async def _check_rate_limits(self, client_ip: str) -> bool:
        """Check if client has exceeded rate limits"""
        now = time.time()
        history = self.request_history[client_ip]
        
        # Clean old entries
        await self._cleanup_old_entries(client_ip, now)
        
        # Check burst limit (last 10 seconds)
        burst_cutoff = now - 10
        recent_requests = sum(1 for timestamp in history['burst'] if timestamp > burst_cutoff)
        if recent_requests >= self.burst_limit:
            logger.warning(f"Burst limit exceeded for IP: {client_ip}")
            return False
        
        # Check minute limit
        if len(history['minute']) >= self.requests_per_minute:
            logger.warning(f"Minute limit exceeded for IP: {client_ip}")
            return False
        
        # Check hour limit
        if len(history['hour']) >= self.requests_per_hour:
            logger.warning(f"Hour limit exceeded for IP: {client_ip}")
            return False
        
        # Check day limit
        if len(history['day']) >= self.requests_per_day:
            logger.warning(f"Day limit exceeded for IP: {client_ip}")
            return False
        
        return True
    
    async def _record_request(self, client_ip: str):
        """Record a request for rate limiting"""
        now = time.time()
        history = self.request_history[client_ip]
        
        # Add to all time windows
        history['burst'].append(now)
        history['minute'].append(now)
        history['hour'].append(now)
        history['day'].append(now)
    
    async def _cleanup_old_entries(self, client_ip: str, now: float):
        """Clean up old entries from history"""
        history = self.request_history[client_ip]
        
        # Remove entries older than respective time windows
        minute_cutoff = now - 60
        hour_cutoff = now - 3600
        day_cutoff = now - 86400
        burst_cutoff = now - 10
        
        # Clean minute window
        while history['minute'] and history['minute'][0] <= minute_cutoff:
            history['minute'].popleft()
        
        # Clean hour window
        while history['hour'] and history['hour'][0] <= hour_cutoff:
            history['hour'].popleft()
        
        # Clean day window
        while history['day'] and history['day'][0] <= day_cutoff:
            history['day'].popleft()
        
        # Clean burst window
        while history['burst'] and history['burst'][0] <= burst_cutoff:
            history['burst'].popleft()
    
    async def get_rate_limit_status(self, client_ip: str) -> Dict[str, int]:
        """Get current rate limit status for a client"""
        now = time.time()
        await self._cleanup_old_entries(client_ip, now)
        
        history = self.request_history[client_ip]
        
        return {
            "requests_per_minute": len(history['minute']),
            "requests_per_hour": len(history['hour']),
            "requests_per_day": len(history['day']),
            "burst_requests": len(history['burst']),
            "minute_limit": self.requests_per_minute,
            "hour_limit": self.requests_per_hour,
            "day_limit": self.requests_per_day,
            "burst_limit": self.burst_limit
        }
    
    def cleanup_expired_clients(self):
        """Remove clients with no recent activity"""
        now = time.time()
        expired_clients = []
        
        for client_ip, history in self.request_history.items():
            # If no requests in the last hour, consider expired
            if not any(timestamp > now - 3600 for timestamp in history['day']):
                expired_clients.append(client_ip)
        
        for client_ip in expired_clients:
            del self.request_history[client_ip]
        
        if expired_clients:
            logger.info(f"Cleaned up {len(expired_clients)} expired clients")
    
    async def __call__(self, scope, receive, send):
        """ASGI interface for middleware"""
        if scope["type"] == "http":
            # Handle HTTP requests
            await self.app(scope, receive, send)
        else:
            # Pass through other types
            await self.app(scope, receive, send)

"""
Logging Middleware for CognOmega Platform
Provides comprehensive request/response logging and monitoring
"""

import time
import json
import uuid
from typing import Dict, Any, Optional
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
import logging
import asyncio
from datetime import datetime
import sys
import traceback

# Configure logger
logger = logging.getLogger(__name__)

class LoggingMiddleware:
    """Comprehensive logging middleware for requests and responses"""
    
    def __init__(
        self,
        log_level: str = "INFO",
        log_requests: bool = True,
        log_responses: bool = True,
        log_body: bool = False,
        log_headers: bool = False,
        max_body_size: int = 1024,
        exclude_paths: list = None
    ):
        self.log_level = getattr(logging, log_level.upper())
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_body = log_body
        self.log_headers = log_headers
        self.max_body_size = max_body_size
        self.exclude_paths = exclude_paths or ["/health", "/metrics", "/favicon.ico"]
        
        # Performance tracking
        self.request_stats: Dict[str, Dict[str, Any]] = {}
        
    async def __call__(self, request: Request, call_next):
        """Main middleware function"""
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Check if path should be excluded
        if self._should_exclude_path(request.url.path):
            return await call_next(request)
        
        # Start timing
        start_time = time.time()
        
        # Log request
        await self._log_request(request, request_id, start_time)
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration = time.time() - start_time
            
            # Log response
            await self._log_response(request, response, request_id, duration, start_time)
            
            # Update stats
            self._update_stats(request, response, duration)
            
            # Add headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration:.4f}s"
            
            return response
            
        except Exception as e:
            # Log error
            duration = time.time() - start_time
            await self._log_error(request, e, request_id, duration, start_time)
            
            # Re-raise the exception
            raise
    
    def _should_exclude_path(self, path: str) -> bool:
        """Check if path should be excluded from logging"""
        return any(path.startswith(exclude_path) for exclude_path in self.exclude_paths)
    
    async def _log_request(self, request: Request, request_id: str, start_time: float):
        """Log incoming request"""
        if not self.log_requests:
            return
        
        try:
            # Extract request data
            request_data = {
                "request_id": request_id,
                "timestamp": datetime.fromtimestamp(start_time).isoformat(),
                "method": request.method,
                "url": str(request.url),
                "path": request.url.path,
                "query_params": dict(request.query_params),
                "client_ip": self._get_client_ip(request),
                "user_agent": request.headers.get("User-Agent", ""),
                "content_type": request.headers.get("Content-Type", ""),
                "content_length": request.headers.get("Content-Length", "0")
            }
            
            # Add headers if requested
            if self.log_headers:
                request_data["headers"] = dict(request.headers)
            
            # Add body if requested and not too large
            if self.log_body and request.method in ["POST", "PUT", "PATCH"]:
                body = await self._get_request_body(request)
                if body and len(body) <= self.max_body_size:
                    request_data["body"] = body
                elif body:
                    request_data["body"] = f"[Body too large: {len(body)} bytes]"
            
            # Add user info if available
            if hasattr(request.state, 'user') and request.state.user:
                request_data["user_id"] = request.state.user.get("user_id")
                request_data["username"] = request.state.user.get("username")
                request_data["user_role"] = request.state.user.get("role")
            
            logger.info(f"REQUEST: {json.dumps(request_data, default=str)}")
            
        except Exception as e:
            logger.error(f"Error logging request {request_id}: {str(e)}")
    
    async def _log_response(self, request: Request, response: Response, request_id: str, duration: float, start_time: float):
        """Log outgoing response"""
        if not self.log_responses:
            return
        
        try:
            # Extract response data
            response_data = {
                "request_id": request_id,
                "timestamp": datetime.fromtimestamp(time.time()).isoformat(),
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
                "content_type": response.headers.get("Content-Type", ""),
                "content_length": response.headers.get("Content-Length", "0")
            }
            
            # Add headers if requested
            if self.log_headers:
                response_data["headers"] = dict(response.headers)
            
            # Add response body for streaming responses
            if isinstance(response, StreamingResponse) and self.log_body:
                response_data["body"] = "[Streaming Response]"
            
            # Determine log level based on status code
            if response.status_code >= 500:
                log_level = logging.ERROR
            elif response.status_code >= 400:
                log_level = logging.WARNING
            else:
                log_level = logging.INFO
            
            logger.log(log_level, f"RESPONSE: {json.dumps(response_data, default=str)}")
            
        except Exception as e:
            logger.error(f"Error logging response {request_id}: {str(e)}")
    
    async def _log_error(self, request: Request, error: Exception, request_id: str, duration: float, start_time: float):
        """Log error details"""
        try:
            error_data = {
                "request_id": request_id,
                "timestamp": datetime.fromtimestamp(time.time()).isoformat(),
                "method": request.method,
                "path": request.url.path,
                "error_type": type(error).__name__,
                "error_message": str(error),
                "duration_ms": round(duration * 1000, 2),
                "traceback": traceback.format_exc()
            }
            
            logger.error(f"ERROR: {json.dumps(error_data, default=str)}")
            
        except Exception as e:
            logger.error(f"Error logging error {request_id}: {str(e)}")
    
    async def _get_request_body(self, request: Request) -> Optional[str]:
        """Safely extract request body"""
        try:
            body = await request.body()
            if body:
                # Try to decode as JSON
                try:
                    return json.loads(body.decode('utf-8'))
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Return as string if not valid JSON
                    return body.decode('utf-8', errors='ignore')
            return None
        except Exception:
            return None
    
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
    
    def _update_stats(self, request: Request, response: Response, duration: float):
        """Update request statistics"""
        try:
            path = request.url.path
            method = request.method
            
            # Initialize path stats if not exists
            if path not in self.request_stats:
                self.request_stats[path] = {
                    "total_requests": 0,
                    "total_duration": 0.0,
                    "avg_duration": 0.0,
                    "min_duration": float('inf'),
                    "max_duration": 0.0,
                    "status_codes": {},
                    "methods": set()
                }
            
            stats = self.request_stats[path]
            
            # Update counters
            stats["total_requests"] += 1
            stats["total_duration"] += duration
            stats["avg_duration"] = stats["total_duration"] / stats["total_requests"]
            stats["min_duration"] = min(stats["min_duration"], duration)
            stats["max_duration"] = max(stats["max_duration"], duration)
            
            # Update status code counts
            status_code = str(response.status_code)
            stats["status_codes"][status_code] = stats["status_codes"].get(status_code, 0) + 1
            
            # Update methods
            stats["methods"].add(method)
            
        except Exception as e:
            logger.error(f"Error updating stats: {str(e)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get request statistics"""
        # Convert sets to lists for JSON serialization
        stats = {}
        for path, path_stats in self.request_stats.items():
            stats[path] = {
                **path_stats,
                "methods": list(path_stats["methods"])
            }
        
        return {
            "total_paths": len(self.request_stats),
            "total_requests": sum(s["total_requests"] for s in self.request_stats.values()),
            "avg_duration": sum(s["avg_duration"] for s in self.request_stats.values()) / len(self.request_stats) if self.request_stats else 0,
            "paths": stats
        }
    
    def clear_stats(self):
        """Clear request statistics"""
        self.request_stats.clear()
    
    async def health_check(self) -> Dict[str, Any]:
        """Health check for logging middleware"""
        return {
            "status": "healthy",
            "log_level": self.log_level,
            "log_requests": self.log_requests,
            "log_responses": self.log_responses,
            "total_paths_monitored": len(self.request_stats),
            "total_requests_logged": sum(s["total_requests"] for s in self.request_stats.values())
        }

"""
Voice-to-App SaaS Platform - FastAPI Backend
Main application entry point with all routers and middleware
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import structlog
import time
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db
from app.core.redis import init_redis
from app.routers import (
    auth,
    voice,
    payments,
    gamification,
    apps,
    admin,
    webhooks,
)
from app.middleware.rate_limiter import RateLimitMiddleware
from app.middleware.auth import AuthMiddleware
from app.middleware.logging import LoggingMiddleware

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Voice-to-App SaaS Platform")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize Redis
    await init_redis()
    logger.info("Redis initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Voice-to-App SaaS Platform")


# Create FastAPI application
app = FastAPI(
    title="Voice-to-App SaaS Platform",
    description="Convert voice commands to working apps in 30 seconds",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Security middleware
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v0/auth", tags=["Authentication"])
app.include_router(voice.router, prefix="/api/v0/voice", tags=["Voice Processing"])
app.include_router(payments.router, prefix="/api/v0/payments", tags=["Payments"])
app.include_router(gamification.router, prefix="/api/v0/gamification", tags=["Gamification"])
app.include_router(apps.router, prefix="/api/v0/apps", tags=["App Generation"])
app.include_router(admin.router, prefix="/api/v0/admin", tags=["Admin"])
app.include_router(webhooks.router, prefix="/api/v0/webhooks", tags=["Webhooks"])

# Static files for generated apps
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time to response headers"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    logger.error(
        "HTTP exception occurred",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path,
        method=request.method,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "path": request.url.path,
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler"""
    logger.error(
        "Unhandled exception occurred",
        error=str(exc),
        path=request.url.path,
        method=request.method,
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500,
            "path": request.url.path,
        }
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Voice-to-App SaaS Platform API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0",
    }


@app.get("/api/v0/status")
async def api_status():
    """API status endpoint"""
    return {
        "api": "Voice-to-App SaaS Platform",
        "version": "1.0.0",
        "status": "operational",
        "features": {
            "voice_processing": True,
            "app_generation": True,
            "payments": True,
            "gamification": True,
            "local_ai": settings.ALLOW_LOCAL_LLM,
            "cloud_ai": bool(settings.HF_API_KEY or settings.TOGETHER_API_KEY or settings.GROQ_API_KEY),
        },
        "endpoints": {
            "auth": "/api/v0/auth",
            "voice": "/api/v0/voice",
            "payments": "/api/v0/payments",
            "apps": "/api/v0/apps",
            "admin": "/api/v0/admin",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )
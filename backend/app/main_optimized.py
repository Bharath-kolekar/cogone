"""
Optimized Voice-to-App SaaS Platform - FastAPI Backend
Hardware resource optimized version with maximum efficiency
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import structlog
import time
import gc
import psutil
import asyncio
from contextlib import asynccontextmanager
from typing import Dict, Any

from app.core.config import settings
from app.core.database import init_db
from app.core.redis import init_redis
from app.core.hardware_optimization import hardware_optimizer
from app.routers import (
    auth,
    voice,
    payments,
    gamification,
    apps,
    admin,
    webhooks,
)

# Configure structured logging with hardware optimization
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
    """Optimized application lifespan events with hardware monitoring"""
    # Startup
    logger.info("Starting Optimized Voice-to-App SaaS Platform")
    
    # Initialize hardware optimization
    await hardware_optimizer.start_monitoring()
    logger.info("Hardware optimization monitoring started")
    
    # Initialize database with connection pooling
    await init_db()
    logger.info("Database initialized with connection pooling")
    
    # Initialize Redis with optimized settings
    await init_redis()
    logger.info("Redis initialized with optimized settings")
    
    # Force initial garbage collection
    gc.collect()
    logger.info("Initial garbage collection completed")
    
    # Log system resources
    resources = await hardware_optimizer.get_system_resources()
    logger.info("System resources monitored", resources=resources)
    
    yield
    
    # Shutdown
    logger.info("Shutting down Optimized Voice-to-App SaaS Platform")
    
    # Stop hardware monitoring
    await hardware_optimizer.stop_monitoring()
    logger.info("Hardware monitoring stopped")
    
    # Final garbage collection
    gc.collect()
    logger.info("Final garbage collection completed")


# Create optimized FastAPI application
app = FastAPI(
    title="Optimized Voice-to-App SaaS Platform",
    description="Hardware-optimized platform for converting voice commands to working apps",
    version="2.0.0",
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

# CORS middleware with optimized settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests
)

# GZip compression middleware for bandwidth optimization
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers with optimized prefixes
app.include_router(auth.router, prefix="/api/v0/auth", tags=["Authentication"])
app.include_router(voice.router, prefix="/api/v0/voice", tags=["Voice Processing"])
app.include_router(payments.router, prefix="/api/v0/payments", tags=["Payments"])
app.include_router(gamification.router, prefix="/api/v0/gamification", tags=["Gamification"])
app.include_router(apps.router, prefix="/api/v0/apps", tags=["App Generation"])
app.include_router(admin.router, prefix="/api/v0/admin", tags=["Admin"])
app.include_router(webhooks.router, prefix="/api/v0/webhooks", tags=["Webhooks"])

# Static files for generated apps with optimized serving
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time and resource usage to response headers"""
    start_time = time.time()
    start_memory = psutil.virtual_memory().used
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    end_memory = psutil.virtual_memory().used
    memory_used = end_memory - start_memory
    
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Memory-Used"] = str(memory_used)
    response.headers["X-CPU-Usage"] = str(psutil.cpu_percent())
    
    return response


@app.middleware("http")
async def resource_optimization_middleware(request: Request, call_next):
    """Resource optimization middleware"""
    # Check system resources before processing
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    
    # If resources are high, trigger optimization
    if cpu_usage > 80 or memory_usage > 85:
        logger.warning("High resource usage detected", 
                      cpu_usage=cpu_usage, 
                      memory_usage=memory_usage)
        
        # Trigger garbage collection
        gc.collect()
        
        # Trigger hardware optimization
        await hardware_optimizer.optimize_all_resources()
    
    response = await call_next(request)
    return response


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Optimized HTTP exception handler"""
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
    """Optimized general exception handler"""
    logger.error(
        "Unhandled exception occurred",
        error=str(exc),
        path=request.url.path,
        method=request.method,
        exc_info=True,
    )
    
    # Trigger garbage collection on errors
    gc.collect()
    
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
    """Optimized root endpoint with resource information"""
    resources = await hardware_optimizer.get_system_resources()
    
    return {
        "message": "Optimized Voice-to-App SaaS Platform API",
        "version": "2.0.0",
        "status": "healthy",
        "optimization": "enabled",
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
        "resources": {
            "cpu_usage": resources.get("cpu", {}).get("current_usage", 0),
            "memory_usage": resources.get("memory", {}).get("current_usage", 0),
            "disk_usage": resources.get("disk", {}).get("current_usage", 0),
        }
    }


@app.get("/health")
async def health_check():
    """Enhanced health check with resource monitoring"""
    resources = await hardware_optimizer.get_system_resources()
    
    # Determine health status based on resource usage
    cpu_usage = resources.get("cpu", {}).get("current_usage", 0)
    memory_usage = resources.get("memory", {}).get("current_usage", 0)
    
    health_status = "healthy"
    if cpu_usage > 90 or memory_usage > 95:
        health_status = "critical"
    elif cpu_usage > 80 or memory_usage > 85:
        health_status = "degraded"
    
    return {
        "status": health_status,
        "timestamp": time.time(),
        "version": "2.0.0",
        "optimization": "enabled",
        "resources": {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": resources.get("disk", {}).get("current_usage", 0),
        }
    }


@app.get("/api/v0/status")
async def api_status():
    """Enhanced API status with optimization information"""
    resources = await hardware_optimizer.get_system_resources()
    optimization_summary = await hardware_optimizer.get_optimization_summary()
    
    return {
        "api": "Optimized Voice-to-App SaaS Platform",
        "version": "2.0.0",
        "status": "operational",
        "optimization": {
            "enabled": True,
            "monitoring_active": optimization_summary.get("monitoring_active", False),
            "total_optimizations": optimization_summary.get("total_optimizations", 0),
            "success_rate": optimization_summary.get("success_rate", 0),
        },
        "features": {
            "voice_processing": True,
            "app_generation": True,
            "payments": True,
            "gamification": True,
            "local_ai": settings.ALLOW_LOCAL_LLM,
            "cloud_ai": bool(settings.HF_API_KEY or settings.TOGETHER_API_KEY or settings.GROQ_API_KEY),
            "hardware_optimization": True,
        },
        "endpoints": {
            "auth": "/api/v0/auth",
            "voice": "/api/v0/voice",
            "payments": "/api/v0/payments",
            "apps": "/api/v0/apps",
            "admin": "/api/v0/admin",
            "optimization": "/api/v0/optimization",
        },
        "resources": {
            "cpu_usage": resources.get("cpu", {}).get("current_usage", 0),
            "memory_usage": resources.get("memory", {}).get("current_usage", 0),
            "disk_usage": resources.get("disk", {}).get("current_usage", 0),
        }
    }


@app.get("/api/v0/optimization/resources")
async def get_resource_metrics():
    """Get current resource metrics"""
    try:
        resources = await hardware_optimizer.get_system_resources()
        return {
            "resources": resources,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Failed to get resource metrics", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get resource metrics")


@app.post("/api/v0/optimization/optimize")
async def trigger_optimization():
    """Trigger hardware optimization"""
    try:
        result = await hardware_optimizer.optimize_all_resources()
        return {
            "optimization_completed": True,
            "result": result,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Failed to trigger optimization", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to trigger optimization")


@app.post("/api/v0/optimization/garbage-collection")
async def trigger_garbage_collection():
    """Trigger garbage collection"""
    try:
        result = await hardware_optimizer.force_garbage_collection()
        return {
            "garbage_collection_completed": True,
            "result": result,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error("Failed to trigger garbage collection", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to trigger garbage collection")


@app.get("/api/v0/optimization/summary")
async def get_optimization_summary():
    """Get optimization summary"""
    try:
        summary = await hardware_optimizer.get_optimization_summary()
        return summary
    except Exception as e:
        logger.error("Failed to get optimization summary", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get optimization summary")


if __name__ == "__main__":
    import uvicorn
    
    # Optimized uvicorn configuration
    uvicorn.run(
        "app.main_optimized:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
        workers=1,  # Single worker for resource optimization
        loop="asyncio",  # Use asyncio loop
        http="httptools",  # Use httptools for better performance
        access_log=False,  # Disable access logs for performance
    )

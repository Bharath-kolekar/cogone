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

# Initialize Sentry for error tracking (optional)
try:
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[FastApiIntegration()],
            traces_sample_rate=1.0,
            environment=settings.ENVIRONMENT
        )
except ImportError:
    pass  # Sentry not installed
from app.core.database import init_db
from app.core.redis import init_redis
from app.core.async_task_manager import async_task_manager
from app.routers import (
    auth,
    voice,
    payments,
    gamification,
    apps,
    admin,
    webhooks,
    smart_coding_ai_optimized,
    capabilities_router,
    ai_agents_consolidated,
    meta_ai_orchestrator_unified,
    swarm_ai_router,
    architecture_generator_router,
    agent_mode_router,
    smart_coding_ai_integration_router,
    auto_save_router,
    ai_component_orchestrator_router,
    unified_ai_orchestrator_router,
    hierarchical_orchestration_router,
    multi_agent_coordinator_router,
    tool_integration_router,
    consistency_dna_router,
    proactive_dna_router,
    consciousness_dna_router,
    quality_optimization_router,
    advanced_analytics_router,
    architecture_compliance_router,
    performance_architecture_router,
    optimized_services_router,
    ethical_ai_router,
    ethical_ai_comprehensive_router,
    smarty_ethical_router,
    smarty_ai_orchestrator_router,
    smarty_agent_integration_router,
    enhanced_voice_to_app_router,
    enhanced_payment_router,
    zero_cost_infrastructure_router,
    advanced_features_router,
    production_deployment_router,
    code_processing,
    self_modification,
    unified_autonomous_dna_router,
    reality_check_dna_router,
)
from app.trpc.app_router import get_trpc_router
from app.middleware.rate_limiter import RateLimitMiddleware
from app.middleware.auth import AuthMiddleware
from app.middleware.logging import LoggingMiddleware
from app.routers.smart_coding_ai_status import router as smart_coding_ai_status_router

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
    
    # Start all async tasks
    await async_task_manager.start_all_tasks()
    logger.info("All async tasks started")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Voice-to-App SaaS Platform")
    
    # Stop all async tasks
    await async_task_manager.stop_all_tasks()
    logger.info("All async tasks stopped")


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
# app.add_middleware(LoggingMiddleware)  # Temporarily disabled for debugging
app.add_middleware(RateLimitMiddleware)
# Enable AuthMiddleware only when configured (prefer dependency-based auth)
if settings.ENABLE_AUTH_MIDDLEWARE:
    app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/v0/auth", tags=["Authentication"])
app.include_router(voice.router, prefix="/api/v0/voice", tags=["Voice Processing"])
app.include_router(payments.router, prefix="/api/v0/payments", tags=["Payments"])
app.include_router(gamification.router, prefix="/api/v0/gamification", tags=["Gamification"])
app.include_router(apps.router, prefix="/api/v0/apps", tags=["App Generation"])
app.include_router(admin.router, prefix="/api/v0/admin", tags=["Admin"])
app.include_router(webhooks.router, prefix="/api/v0/webhooks", tags=["Webhooks"])
app.include_router(smart_coding_ai_optimized.router, prefix="/api/v0/smart-coding-ai", tags=["Smart Coding AI"])
app.include_router(capabilities_router.router, prefix="/api/v0/ai-capabilities", tags=["AI Capabilities"])
app.include_router(smart_coding_ai_integration_router.router, tags=["Smart Coding AI Integration"])
app.include_router(auto_save_router.router, tags=["Auto-Save & Keep All Changes"])
app.include_router(ai_component_orchestrator_router.router, tags=["AI Component Orchestrator"])
app.include_router(unified_ai_orchestrator_router.router, tags=["Unified AI Orchestrator"])
app.include_router(ai_agents_consolidated.router, prefix="/api/v0/ai-agents", tags=["AI Agents"])
app.include_router(meta_ai_orchestrator_unified.router, prefix="/api/v0/meta-orchestrator", tags=["Meta Orchestrator"])
app.include_router(swarm_ai_router.router, prefix="/api/v0/swarm-ai", tags=["Swarm AI"])
app.include_router(architecture_generator_router.router, prefix="/api/v0/architecture-generator", tags=["Architecture Generator"])
app.include_router(agent_mode_router.router, prefix="/api/v0/agent-mode", tags=["Agent Mode"])
app.include_router(hierarchical_orchestration_router.router, prefix="/api/v0", tags=["Hierarchical Orchestration"])
app.include_router(multi_agent_coordinator_router.router, prefix="/api/v0", tags=["Multi-Agent Coordination"])
app.include_router(tool_integration_router.router, prefix="/api/v0", tags=["Tool Integration"])
app.include_router(consistency_dna_router.router, prefix="/api/v0", tags=["Consistency DNA"])
app.include_router(proactive_dna_router.router, prefix="/api/v0", tags=["Proactive DNA"])
app.include_router(consciousness_dna_router.router, prefix="/api/v0", tags=["Consciousness DNA"])
app.include_router(quality_optimization_router.router, prefix="/api/v0/quality", tags=["Quality Optimization"])
app.include_router(advanced_analytics_router.router, prefix="/api/v0/analytics", tags=["Advanced Analytics"])
app.include_router(architecture_compliance_router.router, prefix="/api/v0", tags=["Architecture Compliance"])
app.include_router(performance_architecture_router.router, prefix="/api/v0", tags=["Performance Architecture"])
app.include_router(optimized_services_router.router, prefix="/api/v0/optimized", tags=["Optimized Services"])
app.include_router(ethical_ai_router.router, prefix="/api/v0/ethical", tags=["Ethical AI"])
app.include_router(ethical_ai_comprehensive_router.router, prefix="/api/v0/ethical-ai", tags=["Ethical AI Comprehensive"])
app.include_router(smarty_ethical_router.router, prefix="/api/v0/smarty-ethical", tags=["Smarty Ethical Integration"])
app.include_router(smarty_ai_orchestrator_router.router, prefix="/api/v0/smarty-orchestrator", tags=["Smarty AI Orchestrator"])
app.include_router(smarty_agent_integration_router.router, prefix="/api/v0/smarty-agents", tags=["Smarty Agent Integration"])
app.include_router(enhanced_voice_to_app_router.router, prefix="/api/v0/voice-to-app", tags=["Enhanced Voice-to-App"])
app.include_router(enhanced_payment_router.router, prefix="/api/v0/payments", tags=["Enhanced Payments"])
app.include_router(smart_coding_ai_status_router)

# tRPC Router
app.include_router(get_trpc_router(), prefix="/api", tags=["tRPC"])

# Zero-Cost Infrastructure Router
app.include_router(zero_cost_infrastructure_router.router, prefix="/api/v0/zero-cost", tags=["Zero-Cost Infrastructure"])

# Advanced Features Router - Phase 2
app.include_router(advanced_features_router.router, prefix="/api/v0/advanced-features", tags=["Advanced Features"])

# Production Deployment Router - Phase 2
app.include_router(production_deployment_router.router, prefix="/api/v0/deployment", tags=["Production Deployment"])

# System Optimization Router - Current System Optimization
from app.routers.system_optimization_router import router as system_optimization_router
app.include_router(system_optimization_router, prefix="/api/v0/optimization", tags=["System Optimization"])

# Code Processing Router - Seamless Edit & Fix Workflow
app.include_router(code_processing.router, prefix="/api/v0/code", tags=["Code Processing"])

# Self-Modification Router - Self-Coding, Self-Debugging, Self-Testing, Self-Management
app.include_router(self_modification.router, prefix="/api/v0", tags=["Self-Modification"])

# Unified Autonomous DNA Integration - Complete Integrated AI System
app.include_router(unified_autonomous_dna_router.router, prefix="/api/v0", tags=["Unified Autonomous DNA"])

# Reality Check DNA - Anti-Hallucination System
app.include_router(reality_check_dna_router.router, prefix="/api/v0", tags=["Reality Check DNA"])

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
            "smart_coding_ai": True,
            "ai_agents": True,
            "meta_orchestrator": True,
            "swarm_ai": True,
            "architecture_generator": True,
            "agent_mode": True,
            "tool_integration": True,
            "local_ai": settings.ALLOW_LOCAL_LLM,
            "cloud_ai": bool(settings.HF_API_KEY or settings.TOGETHER_API_KEY or settings.GROQ_API_KEY),
        },
        "endpoints": {
            "auth": "/api/v0/auth",
            "voice": "/api/v0/voice",
            "payments": "/api/v0/payments",
            "apps": "/api/v0/apps",
            "admin": "/api/v0/admin",
            "smart_coding_ai": "/api/v0/smart-coding-ai",
            "ai_agents": "/api/v0/ai-agents",
            "meta_orchestrator": "/api/v0/meta-orchestrator",
            "swarm_ai": "/api/v0/swarm-ai",
            "architecture_generator": "/api/v0/architecture-generator",
            "agent_mode": "/api/v0/agent-mode",
            "tool_integration": "/api/v0/tools",
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
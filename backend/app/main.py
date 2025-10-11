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
# 🧬 CONSOLIDATED ROUTERS (118 → 15)
from app.routers import (
    auth_users_router,           # 1. Auth, Profiles, User Preferences
    ai_agents_router,             # 2. AI Agents, Agent Mode, Multi-Agent Coordinator
    orchestration_router,         # 3. All AI Orchestrators (Unified, Meta, Hierarchical, Swarm, Smarty)
    architecture_router,          # 4. Architecture Generation, Compliance, Performance
    ethics_governance_router,     # 5. Ethical AI, Governance, Compliance
    payments_router,              # 6. Payments, Billing, Subscriptions
    voice_router,                 # 7. Voice, Transcribe, Enhanced Voice-to-App
    code_intelligence_router,     # 8. Code Processing, Code Intelligence
    apps_capabilities_router,     # 9. Apps, Frontend, Gamification, Capabilities
    system_infrastructure_router, # 10. System Optimization, Hardware, Zero-Cost
    analytics_router,             # 11. Advanced Analytics, Data Analytics
    tools_integrations_router,    # 12. Tool Integration, Webhooks
    admin_router,                 # 13. Admin, Self-Modification
    optimization_router,          # 14. Quality, Optimized Services, Super-Intelligent
    dna_systems_router,           # 15. All DNA Systems (Consciousness, Consistency, Proactive, Reality Check, Autonomous, Auto-Save)
)
from app.trpc.app_router import get_trpc_router
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
    
    # Start all async tasks
    await async_task_manager.start_all_tasks()
    logger.info("All async tasks started")
    
    # Run CognOmega DNA Self-Check
    try:
        from app.startup.self_check import run_startup_self_check
        self_check_results = await run_startup_self_check()
        logger.info(
            "🧬 CognOmega DNA Self-Check Complete",
            intelligence_score=f"{self_check_results.get('intelligence_score', 0):.1f}%",
            status=self_check_results.get('overall_status', 'UNKNOWN')
        )
    except Exception as e:
        logger.warning("⚠️ Self-check skipped", reason=str(e))
    
    # Run CognOmega Full Diagnostic
    try:
        from app.startup.full_diagnostic import run_startup_diagnostic, start_periodic_diagnostic
        diagnostic_results = await run_startup_diagnostic()
        logger.info(
            "🔍 CognOmega Full Diagnostic Complete",
            issues_found=diagnostic_results.get('total_issues_found', 0),
            critical=len(diagnostic_results.get('critical', [])),
            high=len(diagnostic_results.get('high', []))
        )
        
        # Start periodic diagnostic task (runs every 2 hours)
        await start_periodic_diagnostic()
        logger.info("✅ Periodic diagnostic scheduled (every 2 hours)")
        
    except Exception as e:
        logger.warning("⚠️ Diagnostic skipped", reason=str(e))
    
    # Start Continuous Self-Modification Helper
    try:
        from app.startup.continuous_self_modification import start_continuous_helper
        await start_continuous_helper()
        logger.info(
            "🔄 Continuous Self-Modification Helper STARTED",
            auto_fix="LOW severity bugs only",
            check_interval="Every 1 hour",
            dna_protected="YES"
        )
    except Exception as e:
        logger.warning("⚠️ Continuous helper skipped", reason=str(e))
    
    yield
    
    # Shutdown
    logger.info("Shutting down Voice-to-App SaaS Platform")
    
    # Stop periodic diagnostic task
    try:
        from app.startup.full_diagnostic import stop_periodic_diagnostic
        await stop_periodic_diagnostic()
        logger.info("✅ Periodic diagnostic task stopped")
    except Exception as e:
        logger.warning("⚠️ Diagnostic cleanup skipped", reason=str(e))
    
    # Stop continuous self-modification helper
    try:
        from app.startup.continuous_self_modification import stop_continuous_helper
        await stop_continuous_helper()
        logger.info("✅ Continuous Self-Modification Helper stopped")
    except Exception as e:
        logger.warning("⚠️ Continuous helper cleanup skipped", reason=str(e))
    
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

# 🧬 CONSOLIDATED ROUTERS - 15 Routers (Previously 118+)
# Each consolidated router groups related functionality for better organization

# 1. Authentication & Users (auth, profiles, user_preferences)
app.include_router(auth_users_router.router, prefix="/api/v0/auth", tags=["Auth & Users"])

# 2. AI Agents & Coordination (ai_agents, agent_mode, multi_agent_coordinator)
app.include_router(ai_agents_router.router, prefix="/api/v0/ai-agents", tags=["AI Agents"])

# 3. AI Orchestration (unified, meta, hierarchical, swarm, smarty orchestrators)
app.include_router(orchestration_router.router, prefix="/api/v0/orchestration", tags=["Orchestration"])

# 4. Architecture (generation, compliance, performance)
app.include_router(architecture_router.router, prefix="/api/v0/architecture", tags=["Architecture"])

# 5. Ethics & Governance (ethical AI, governance, compliance)
app.include_router(ethics_governance_router.router, prefix="/api/v0/ethics", tags=["Ethics & Governance"])

# 6. Payments & Billing (payments, subscriptions, billing, refunds)
app.include_router(payments_router.router, prefix="/api/v0/payments", tags=["Payments & Billing"])

# 7. Voice & Voice-to-App (voice, transcribe, enhanced voice-to-app)
app.include_router(voice_router.router, prefix="/api/v0/voice", tags=["Voice & Voice-to-App"])

# 8. Code Intelligence (code processing, code intelligence, analysis)
app.include_router(code_intelligence_router.router, prefix="/api/v0/code", tags=["Code Intelligence"])

# 9. Apps & Capabilities (apps, frontend, gamification, capabilities)
app.include_router(apps_capabilities_router.router, prefix="/api/v0/apps", tags=["Apps & Capabilities"])

# 10. System & Infrastructure (system optimization, hardware, zero-cost)
app.include_router(system_infrastructure_router.router, prefix="/api/v0/system", tags=["System & Infrastructure"])

# 11. Analytics (advanced analytics, data analytics, reporting)
app.include_router(analytics_router.router, prefix="/api/v0/analytics", tags=["Analytics"])

# 12. Tools & Integrations (tool integration, webhooks, api keys)
app.include_router(tools_integrations_router.router, prefix="/api/v0/tools", tags=["Tools & Integrations"])

# 13. Admin & Self-Modification (admin, self-modification, system management)
app.include_router(admin_router.router, prefix="/api/v0/admin", tags=["Admin & Management"])

# 14. Optimization (quality, services, super-intelligent optimization)
app.include_router(optimization_router.router, prefix="/api/v0/optimization", tags=["Optimization"])

# 15. DNA Systems (consciousness, consistency, proactive, reality check, autonomous, auto-save)
app.include_router(dna_systems_router.router, prefix="/api/v0/dna", tags=["DNA Systems"])

# tRPC Router (kept separate for compatibility)
app.include_router(get_trpc_router(), prefix="/api", tags=["tRPC"])

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
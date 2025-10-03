"""
Main router index for tRPC integration
"""
from fastapi import APIRouter
from .auth import router as auth_router
from .apps import router as apps_router
from .voice import router as voice_router
from .payments import router as payments_router
from .gamification import router as gamification_router
from .admin import router as admin_router
from .billing import router as billing_router
from .meta_ai_orchestrator import router as meta_orchestrator_router
from .profiles import router as profiles_router
from .transcribe import router as transcribe_router
from .webhooks import router as webhooks_router
from .ai_agents_consolidated import router as ai_agents_router
from .performance_optimized import router as performance_router
from .enhanced_ai_systems import router as enhanced_ai_router
from .user_preferences import router as user_preferences_router
from .super_intelligent_optimization import router as super_intelligent_router
from .zero_cost_super_intelligence import router as zero_cost_super_intelligent_router

# Create main router
router = APIRouter()

# Include all routers
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(apps_router, prefix="/apps", tags=["apps"])
router.include_router(voice_router, prefix="/voice", tags=["voice"])
router.include_router(payments_router, prefix="/payments", tags=["payments"])
router.include_router(gamification_router, prefix="/gamification", tags=["gamification"])
router.include_router(admin_router, prefix="/admin", tags=["admin"])
router.include_router(billing_router, prefix="/billing", tags=["billing"])
router.include_router(meta_orchestrator_router, prefix="/meta-orchestrator", tags=["meta-orchestrator"])
router.include_router(profiles_router, prefix="/profiles", tags=["profiles"])
router.include_router(transcribe_router, prefix="/transcribe", tags=["transcribe"])
router.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])
router.include_router(ai_agents_router, prefix="/ai-agents", tags=["ai-agents"])
router.include_router(performance_router, prefix="/performance", tags=["performance"])
router.include_router(enhanced_ai_router, prefix="/enhanced-ai", tags=["enhanced-ai"])
router.include_router(user_preferences_router, prefix="/user-preferences", tags=["user-preferences"])
router.include_router(super_intelligent_router, prefix="/api", tags=["super-intelligent"])
router.include_router(zero_cost_super_intelligent_router, prefix="/api", tags=["zero-cost-super-intelligent"])

# Export AppRouter type for tRPC
from typing import Any
from fastapi import FastAPI

def create_app() -> FastAPI:
    """Create FastAPI app with all routers"""
    app = FastAPI(title="Voice-to-App SaaS Platform", version="1.0.0")
    app.include_router(router)
    return app

# Type alias for tRPC
AppRouter = Any

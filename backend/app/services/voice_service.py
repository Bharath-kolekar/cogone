"""
Voice Service - Backward Compatibility Wrapper
Redirects to EnhancedVoiceToAppService for all functionality
"""

import structlog
from app.services.enhanced_voice_to_app_service import VoiceService

logger = structlog.get_logger()

# Re-export for backward compatibility
__all__ = ['VoiceService']

# Note: All methods are now handled by VoiceService class imported from enhanced_voice_to_app_service
# This file serves as a compatibility shim to prevent import errors
"""
Smart Coding AI Integration - Modular Architecture
Phase 2: Dependency Reduction (40 → <10 per module)

Public API Facade - Maintains backward compatibility
"""

from .core import SmartCodingAIIntegration, smart_coding_ai_integration
from app.services.ai_integration_types import AIIntegrationContext, IntegratedAIResponse

__version__ = "2.0.0"
__all__ = [
    'SmartCodingAIIntegration',
    'smart_coding_ai_integration',
    'AIIntegrationContext',
    'IntegratedAIResponse'
]


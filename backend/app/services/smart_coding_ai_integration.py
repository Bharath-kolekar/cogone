"""
Smart Coding AI Integration - Backward Compatibility Shim
Redirects to new modular architecture in smart_coding_ai/

This file maintains backward compatibility for existing imports.
New code should import from: app.services.smart_coding_ai
"""

# Re-export everything from the new modular structure
from app.services.smart_coding_ai import (
    SmartCodingAIIntegration,
    smart_coding_ai_integration,
    AIIntegrationContext,
    IntegratedAIResponse
)

__all__ = [
    'SmartCodingAIIntegration',
    'smart_coding_ai_integration',
    'AIIntegrationContext',
    'IntegratedAIResponse'
]

# Backward compatibility note:
# This shim allows existing code to continue working while migrating to:
# from app.services.smart_coding_ai import SmartCodingAIIntegration


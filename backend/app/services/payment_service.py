"""
Payment Service - Backward Compatibility Wrapper
Redirects to EnhancedPaymentService for all functionality
"""

from app.services.enhanced_payment_service import (
    EnhancedPaymentService,
    enhanced_payment_service
)

# Backward compatibility: Alias class and instance
PaymentService = EnhancedPaymentService
payment_service = enhanced_payment_service

# Re-export for backward compatibility
__all__ = ['PaymentService', 'payment_service']
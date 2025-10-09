# backend/app/services/paypal_service.py
"""
PayPal Payment Service - STUB IMPLEMENTATION

⚠️ WARNING: This is a MOCK implementation for development only.
⚠️ Does NOT make real PayPal API calls.
⚠️ Returns fake data for testing purposes.
⚠️ Replace with real PayPal SDK integration before production.

For production implementation:
1. Install: pip install paypalrestsdk
2. Use PayPal REST API SDK
3. Implement proper error handling and webhooks
"""
from typing import Dict, Any, Optional
import structlog
from ..core.config import get_settings

logger = structlog.get_logger()

class PayPalService:
    """
    PayPal payment service - STUB IMPLEMENTATION
    
    ⚠️ THIS IS A MOCK SERVICE - NOT PRODUCTION READY
    """
    
    def __init__(self):
        settings = get_settings()
        # ✅ Use settings instead of hardcoded values
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.sandbox = settings.PAYPAL_SANDBOX.lower() == "true"
        
        logger.warning(
            "⚠️ PayPal Service initialized with STUB implementation - NOT production ready!",
            client_id=self.client_id,
            sandbox=self.sandbox
        )
    
    async def create_order(self, amount: float, currency: str = "USD", **kwargs) -> Dict[str, Any]:
        """
        Create a PayPal order - MOCK IMPLEMENTATION
        
        ⚠️ Returns fake data, does not call real PayPal API
        """
        logger.warning("⚠️ Using STUB PayPal create_order - returns fake data")
        return {
            "id": f"paypal_order_{hash(str(amount))}",  # ⚠️ FAKE ORDER ID
            "amount": {
                "currency_code": currency,
                "value": str(amount)
            },
            "status": "CREATED"
        }
    
    async def capture_order(self, order_id: str) -> Dict[str, Any]:
        """
        Capture a PayPal order - MOCK IMPLEMENTATION
        
        ⚠️ Returns fake data, does not call real PayPal API
        """
        logger.warning("⚠️ Using STUB PayPal capture_order - returns fake data")
        return {
            "id": order_id,
            "status": "COMPLETED"  # ⚠️ FAKE STATUS
        }
    
    async def verify_webhook(self, payload: str, signature: str) -> bool:
        """
        Verify PayPal webhook signature - MOCK IMPLEMENTATION
        
        ⚠️ Always returns True, does not verify real signatures
        """
        logger.warning("⚠️ Using STUB PayPal verify_webhook - always returns True")
        return True  # ⚠️ FAKE VERIFICATION

paypal_service = PayPalService()

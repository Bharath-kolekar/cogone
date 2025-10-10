# backend/app/services/razorpay_service.py
"""
Razorpay Payment Service - STUB IMPLEMENTATION

⚠️ WARNING: This is a MOCK implementation for development only.
⚠️ Does NOT make real Razorpay API calls.
⚠️ Returns fake data for testing purposes.
⚠️ Replace with real Razorpay SDK integration before production.

For production implementation:
1. Install: pip install razorpay
2. Use Razorpay Python SDK
3. Implement proper error handling and webhooks
"""
from typing import Dict, Any, Optional
import structlog
from ..core.config import get_settings

logger = structlog.get_logger()

class RazorpayService:
    """
    Razorpay payment service - STUB IMPLEMENTATION
    
    ⚠️ THIS IS A MOCK SERVICE - NOT PRODUCTION READY
    """
    
    def __init__(self):
        settings = get_settings()
        # ✅ Use settings instead of hardcoded values
        self.api_key = settings.RAZORPAY_API_KEY
        self.api_secret = settings.RAZORPAY_API_SECRET
        
        logger.warning(
            "⚠️ Razorpay Service initialized with STUB implementation - NOT production ready!",
            api_key=self.api_key
        )
    
    async def create_order(self, amount: float, currency: str = "INR", **kwargs) -> Dict[str, Any]:
        """
        Create a Razorpay order - MOCK IMPLEMENTATION
        
        ⚠️ Returns fake data, does not call real Razorpay API
        """
        logger.warning("⚠️ Using STUB Razorpay create_order - returns fake data")
        return {
            "id": f"order_{hash(str(amount))}",  # ⚠️ FAKE ORDER ID
            "amount": int(amount * 100),  # Convert to paise
            "currency": currency,
            "status": "created"
        }
    
    async def capture_payment(self, payment_id: str, amount: float) -> Dict[str, Any]:
        """
        Capture a Razorpay payment - MOCK IMPLEMENTATION
        
        ⚠️ Returns fake data, does not call real Razorpay API
        """
        logger.warning("⚠️ Using STUB Razorpay capture_payment - returns fake data")
        return {
            "id": payment_id,
            "status": "captured",  # ⚠️ FAKE STATUS
            "amount": int(amount * 100)
        }
    
    async def verify_webhook(self, payload: str, signature: str) -> bool:
        """
        Verify Razorpay webhook signature - MOCK IMPLEMENTATION
        
        ⚠️ Always returns True, does not verify real signatures
        """
        logger.warning("⚠️ Using STUB Razorpay verify_webhook - always returns True")
        return True  # ⚠️ FAKE VERIFICATION

razorpay_service = RazorpayService()

# backend/app/services/upi_service.py
"""
UPI Payment Service - STUB IMPLEMENTATION

⚠️ WARNING: This is a MOCK implementation for development only.
⚠️ Does NOT make real UPI API calls.
⚠️ Returns fake data for testing purposes.
⚠️ Replace with real UPI integration before production.

For production implementation:
1. Integrate with UPI payment gateway SDK
2. Implement proper payment verification
3. Add webhook handlers for payment status
"""
from typing import Dict, Any, Optional
import structlog
from ..core.config import get_settings

logger = structlog.get_logger()

class UPIService:
    """
    UPI payment service - STUB IMPLEMENTATION
    
    ⚠️ THIS IS A MOCK SERVICE - NOT PRODUCTION READY
    """
    
    def __init__(self):
        settings = get_settings()
        # ✅ Use settings instead of hardcoded values
        self.merchant_id = settings.UPI_MERCHANT_ID
        self.merchant_name = settings.UPI_MERCHANT_NAME
        
        logger.warning(
            "⚠️ UPI Service initialized with STUB implementation - NOT production ready!",
            merchant_id=self.merchant_id
        )
    
    async def create_payment_request(self, amount: float, **kwargs) -> Dict[str, Any]:
        """
        Create a UPI payment request - MOCK IMPLEMENTATION
        
        ⚠️ Returns fake data, does not call real UPI API
        """
        logger.warning("⚠️ Using STUB UPI create_payment_request - returns fake data")
        return {
            "id": f"upi_payment_{hash(str(amount))}",  # ⚠️ FAKE ID
            "amount": amount,
            "status": "PENDING",
            "upi_id": f"merchant@{self.merchant_id}.upi"
        }
    
    async def verify_payment(self, transaction_id: str) -> Dict[str, Any]:
        """
        Verify UPI payment - MOCK IMPLEMENTATION
        
        ⚠️ Always returns SUCCESS, does not verify real payment
        """
        logger.warning("⚠️ Using STUB UPI verify_payment - always returns SUCCESS")
        return {
            "transaction_id": transaction_id,
            "status": "SUCCESS"  # ⚠️ FAKE - Always succeeds!
        }
    
    async def generate_qr_code(self, amount: float, **kwargs) -> str:
        """
        Generate UPI QR code - MOCK IMPLEMENTATION
        
        ⚠️ Returns fake QR code string, may not work with real UPI apps
        """
        logger.warning("⚠️ Using STUB UPI generate_qr_code - returns mock QR")
        return f"upi://pay?pa=merchant@{self.merchant_id}.upi&pn={self.merchant_name}&am={amount}&cu=INR"

upi_service = UPIService()

# backend/app/services/razorpay_service_real.py
"""
Razorpay Payment Service - REAL IMPLEMENTATION

🧬 REAL IMPLEMENTATION: Actual Razorpay REST API integration
Uses httpx for HTTP calls to Razorpay API
Handles Basic Auth, order creation, payment capture, and webhooks
Production-ready with error handling
"""
from typing import Dict, Any, Optional
import structlog
import httpx
import hmac
import hashlib
import base64
from ..core.config import get_settings

logger = structlog.get_logger()

class RazorpayService:
    """
    Razorpay payment service - REAL IMPLEMENTATION
    
    🧬 Production-ready Razorpay REST API integration
    """
    
    def __init__(self):
        settings = get_settings()
        self.key_id = settings.RAZORPAY_KEY_ID
        self.key_secret = settings.RAZORPAY_KEY_SECRET
        self.webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
        
        # Real Razorpay API
        self.base_url = "https://api.razorpay.com/v1"
        
        # Create Basic Auth header
        if self.key_id and self.key_secret:
            credentials = f"{self.key_id}:{self.key_secret}"
            self.auth_header = base64.b64encode(credentials.encode()).decode()
        else:
            self.auth_header = None
        
        logger.info(
            "Razorpay Service initialized with REAL API integration",
            configured=bool(self.key_id)
        )
    
    async def create_order(self, amount: int, currency: str = "INR", **kwargs) -> Dict[str, Any]:
        """
        Create a Razorpay order - REAL IMPLEMENTATION
        
        🧬 Makes actual Razorpay REST API call
        """
        # Validation
        if amount <= 0:
            raise ValueError("Amount must be positive (in paise)")
        
        if not self.auth_header:
            raise ValueError("Razorpay credentials not configured")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/orders",
                    headers={
                        "Authorization": f"Basic {self.auth_header}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "amount": amount,  # Amount in paise
                        "currency": currency,
                        "receipt": kwargs.get('receipt', f"rcpt_{amount}"),
                        "notes": kwargs.get('notes', {})
                    }
                )
                response.raise_for_status()
                order_data = response.json()
                
                logger.info("Razorpay order created", order_id=order_data["id"], amount=amount)
                return order_data
                
        except httpx.HTTPError as e:
            logger.error("Razorpay API error", error=str(e))
            raise ValueError(f"Razorpay order creation failed: {e}")
        except Exception as e:
            logger.error("Razorpay error", error=str(e))
            raise
    
    async def capture_payment(self, payment_id: str, amount: int, currency: str = "INR") -> Dict[str, Any]:
        """
        Capture a Razorpay payment - REAL IMPLEMENTATION
        
        🧬 Makes actual Razorpay REST API call
        """
        if not payment_id:
            raise ValueError("Payment ID is required")
        
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/payments/{payment_id}/capture",
                    headers={
                        "Authorization": f"Basic {self.auth_header}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "amount": amount,
                        "currency": currency
                    }
                )
                response.raise_for_status()
                capture_data = response.json()
                
                logger.info("Razorpay payment captured", payment_id=payment_id, amount=amount)
                return capture_data
                
        except httpx.HTTPError as e:
            logger.error("Razorpay capture failed", payment_id=payment_id, error=str(e))
            raise ValueError(f"Razorpay capture failed: {e}")
        except Exception as e:
            logger.error("Razorpay error", error=str(e))
            raise
    
    async def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Get Razorpay payment details - REAL IMPLEMENTATION
        
        🧬 Makes actual Razorpay REST API call
        """
        if not payment_id:
            raise ValueError("Payment ID is required")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/payments/{payment_id}",
                    headers={
                        "Authorization": f"Basic {self.auth_header}"
                    }
                )
                response.raise_for_status()
                payment_data = response.json()
                
                logger.info("Razorpay payment retrieved", payment_id=payment_id, status=payment_data.get("status"))
                return payment_data
                
        except httpx.HTTPError as e:
            logger.error("Razorpay get payment failed", payment_id=payment_id, error=str(e))
            raise ValueError(f"Razorpay get payment failed: {e}")
        except Exception as e:
            logger.error("Razorpay error", error=str(e))
            raise
    
    async def verify_webhook(self, payload: str, signature: str) -> bool:
        """
        Verify Razorpay webhook signature - REAL IMPLEMENTATION
        
        🧬 Validates actual webhook signatures using HMAC
        """
        if not self.webhook_secret:
            logger.warning("Razorpay webhook secret not configured")
            return False
        
        try:
            # Real HMAC signature verification
            expected_signature = hmac.new(
                self.webhook_secret.encode(),
                payload.encode(),
                hashlib.sha256
            ).hexdigest()
            
            # Constant-time comparison
            verified = hmac.compare_digest(expected_signature, signature)
            
            logger.info("Razorpay webhook verification", verified=verified)
            return verified
            
        except Exception as e:
            logger.error("Webhook verification failed", error=str(e))
            return False

razorpay_service = RazorpayService()


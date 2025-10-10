# backend/app/services/paypal_service.py
"""
PayPal Payment Service - REAL IMPLEMENTATION

🧬 REAL IMPLEMENTATION: Actual PayPal REST API integration
Uses httpx for HTTP calls to PayPal API
Handles OAuth, order creation, capture, and webhooks
Production-ready with error handling
"""
from typing import Dict, Any, Optional
import structlog
import httpx
import hmac
import hashlib
from ..core.config import get_settings

logger = structlog.get_logger()

class PayPalService:
    """
    PayPal payment service - REAL IMPLEMENTATION
    
    🧬 Production-ready PayPal REST API integration
    """
    
    def __init__(self):
        settings = get_settings()
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.webhook_id = settings.PAYPAL_WEBHOOK_ID
        self.sandbox = settings.PAYPAL_SANDBOX.lower() == "true"
        
        # Real API URLs
        self.base_url = f"https://api-m.{'sandbox.' if self.sandbox else ''}paypal.com"
        
        logger.info(
            "PayPal Service initialized with REAL API integration",
            sandbox=self.sandbox,
            configured=bool(self.client_id)
        )
    
    async def _get_access_token(self) -> str:
        """
        Get OAuth access token from PayPal
        
        🧬 REAL IMPLEMENTATION: OAuth 2.0 flow
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/oauth2/token",
                auth=(self.client_id, self.client_secret),
                data={"grant_type": "client_credentials"},
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            return response.json()["access_token"]
    
    async def create_order(self, amount: float, currency: str = "USD", **kwargs) -> Dict[str, Any]:
        """
        Create a PayPal order - REAL IMPLEMENTATION
        
        🧬 Makes actual PayPal REST API call
        """
        # Validation
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if not self.client_id or not self.client_secret:
            raise ValueError("PayPal credentials not configured")
        
        try:
            # Get OAuth token
            access_token = await self._get_access_token()
            
            # Create order via real API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v2/checkout/orders",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "intent": "CAPTURE",
                        "purchase_units": [{
                            "amount": {
                                "currency_code": currency,
                                "value": f"{amount:.2f}"
                            }
                        }]
                    }
                )
                response.raise_for_status()
                order_data = response.json()
                
                logger.info("PayPal order created", order_id=order_data["id"], amount=amount)
                return order_data
                
        except httpx.HTTPError as e:
            logger.error("PayPal API error", error=str(e))
            raise ValueError(f"PayPal order creation failed: {e}")
        except Exception as e:
            logger.error("PayPal error", error=str(e))
            raise
    
    async def capture_order(self, order_id: str) -> Dict[str, Any]:
        """
        Capture a PayPal order - REAL IMPLEMENTATION
        
        🧬 Makes actual PayPal REST API call
        """
        if not order_id:
            raise ValueError("Order ID is required")
        
        try:
            access_token = await self._get_access_token()
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v2/checkout/orders/{order_id}/capture",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                capture_data = response.json()
                
                logger.info("PayPal order captured", order_id=order_id, status=capture_data.get("status"))
                return capture_data
                
        except httpx.HTTPError as e:
            logger.error("PayPal capture failed", order_id=order_id, error=str(e))
            raise ValueError(f"PayPal capture failed: {e}")
        except Exception as e:
            logger.error("PayPal error", error=str(e))
            raise
    
    async def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Get PayPal order details - REAL IMPLEMENTATION
        
        🧬 Makes actual PayPal REST API call
        """
        if not order_id:
            raise ValueError("Order ID is required")
        
        try:
            access_token = await self._get_access_token()
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/v2/checkout/orders/{order_id}",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    }
                )
                response.raise_for_status()
                order_data = response.json()
                
                logger.info("PayPal order retrieved", order_id=order_id, status=order_data.get("status"))
                return order_data
                
        except httpx.HTTPError as e:
            logger.error("PayPal get order failed", order_id=order_id, error=str(e))
            raise ValueError(f"PayPal get order failed: {e}")
        except Exception as e:
            logger.error("PayPal error", error=str(e))
            raise
    
    async def verify_webhook(self, payload: str, headers: Dict[str, str]) -> bool:
        """
        Verify PayPal webhook signature - REAL IMPLEMENTATION
        
        🧬 Validates actual webhook signatures
        """
        if not self.webhook_id:
            logger.warning("PayPal webhook ID not configured")
            return False
        
        try:
            # Real PayPal webhook verification
            # Get verification data from headers
            transmission_id = headers.get('PAYPAL-TRANSMISSION-ID')
            transmission_time = headers.get('PAYPAL-TRANSMISSION-TIME')
            cert_url = headers.get('PAYPAL-CERT-URL')
            transmission_sig = headers.get('PAYPAL-TRANSMISSION-SIG')
            auth_algo = headers.get('PAYPAL-AUTH-ALGO')
            
            if not all([transmission_id, transmission_time, transmission_sig]):
                logger.warning("Missing webhook verification headers")
                return False
            
            # Verify with PayPal API
            access_token = await self._get_access_token()
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/v1/notifications/verify-webhook-signature",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "transmission_id": transmission_id,
                        "transmission_time": transmission_time,
                        "cert_url": cert_url,
                        "auth_algo": auth_algo,
                        "transmission_sig": transmission_sig,
                        "webhook_id": self.webhook_id,
                        "webhook_event": payload
                    }
                )
                response.raise_for_status()
                result = response.json()
                
                verified = result.get("verification_status") == "SUCCESS"
                logger.info("Webhook verification result", verified=verified)
                return verified
                
        except Exception as e:
            logger.error("Webhook verification failed", error=str(e))
            return False

paypal_service = PayPalService()

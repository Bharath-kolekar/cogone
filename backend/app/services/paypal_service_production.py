# backend/app/services/paypal_service_production.py
"""
PayPal Payment Service - PRODUCTION IMPLEMENTATION

This is the real PayPal integration using the PayPal REST SDK.
Replace the stub implementation with this for production use.

Installation:
    pip install paypalrestsdk

Documentation:
    https://github.com/paypal/PayPal-Python-SDK
"""
from typing import Dict, Any, Optional
import structlog
import paypalrestsdk
from ..core.config import get_settings

logger = structlog.get_logger()


class PayPalServiceProduction:
    """
    Production PayPal payment service with real API integration
    
    Features:
    - Real PayPal API calls
    - Sandbox and production modes
    - Proper error handling
    - Webhook support
    - Order creation and capture
    """
    
    def __init__(self):
        settings = get_settings()
        
        # Load credentials from settings
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.sandbox = settings.PAYPAL_SANDBOX.lower() == "true"
        
        # Configure PayPal SDK
        paypalrestsdk.configure({
            "mode": "sandbox" if self.sandbox else "live",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        })
        
        logger.info(
            "✅ PayPal Service initialized (PRODUCTION)",
            mode="sandbox" if self.sandbox else "live",
            client_id=self.client_id[:10] + "..."
        )
    
    async def create_order(self, amount: float, currency: str = "USD", **kwargs) -> Dict[str, Any]:
        """
        Create a PayPal order
        
        Args:
            amount: Order amount
            currency: Currency code (USD, EUR, etc.)
            **kwargs: Additional order parameters
                - description: Order description
                - return_url: URL to return after payment
                - cancel_url: URL to return if cancelled
                
        Returns:
            Order details with approval URL
        """
        try:
            # Create payment object
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": kwargs.get("return_url", "http://localhost:3000/payment/success"),
                    "cancel_url": kwargs.get("cancel_url", "http://localhost:3000/payment/cancel")
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": kwargs.get("description", "Payment"),
                            "sku": "item",
                            "price": str(amount),
                            "currency": currency,
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(amount),
                        "currency": currency
                    },
                    "description": kwargs.get("description", "Payment")
                }]
            })
            
            # Create the payment
            if payment.create():
                logger.info(
                    "PayPal order created successfully",
                    payment_id=payment.id,
                    amount=amount,
                    currency=currency
                )
                
                # Get approval URL
                approval_url = None
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        break
                
                return {
                    "id": payment.id,
                    "status": payment.state,
                    "amount": {
                        "currency_code": currency,
                        "value": str(amount)
                    },
                    "approval_url": approval_url,
                    "created_time": payment.create_time
                }
            else:
                error_msg = payment.error.get("message", "Unknown error") if hasattr(payment, "error") else "Payment creation failed"
                logger.error("PayPal order creation failed", error=error_msg)
                raise Exception(f"PayPal order creation failed: {error_msg}")
                
        except Exception as e:
            logger.error("PayPal create_order error", error=str(e), amount=amount)
            raise
    
    async def capture_order(self, order_id: str) -> Dict[str, Any]:
        """
        Capture a PayPal order (execute payment)
        
        Args:
            order_id: PayPal payment ID
            
        Returns:
            Captured payment details
        """
        try:
            # Get the payment
            payment = paypalrestsdk.Payment.find(order_id)
            
            # Execute the payment
            if payment.execute({"payer_id": payment.payer.get("payer_info", {}).get("payer_id")}):
                logger.info(
                    "PayPal order captured successfully",
                    payment_id=order_id,
                    state=payment.state
                )
                
                return {
                    "id": payment.id,
                    "status": payment.state,
                    "payer": payment.payer,
                    "transactions": payment.transactions,
                    "captured_time": payment.update_time
                }
            else:
                error_msg = payment.error.get("message", "Unknown error") if hasattr(payment, "error") else "Payment execution failed"
                logger.error("PayPal order capture failed", error=error_msg, payment_id=order_id)
                raise Exception(f"PayPal order capture failed: {error_msg}")
                
        except Exception as e:
            logger.error("PayPal capture_order error", error=str(e), order_id=order_id)
            raise
    
    async def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Get PayPal order details
        
        Args:
            order_id: PayPal payment ID
            
        Returns:
            Order details
        """
        try:
            payment = paypalrestsdk.Payment.find(order_id)
            
            return {
                "id": payment.id,
                "status": payment.state,
                "intent": payment.intent,
                "payer": payment.payer,
                "transactions": payment.transactions,
                "created_time": payment.create_time,
                "updated_time": payment.update_time
            }
            
        except Exception as e:
            logger.error("PayPal get_order error", error=str(e), order_id=order_id)
            raise
    
    async def refund_payment(self, sale_id: str, amount: Optional[float] = None) -> Dict[str, Any]:
        """
        Refund a PayPal payment
        
        Args:
            sale_id: PayPal sale ID
            amount: Refund amount (None for full refund)
            
        Returns:
            Refund details
        """
        try:
            sale = paypalrestsdk.Sale.find(sale_id)
            
            refund_request = {}
            if amount is not None:
                refund_request = {
                    "amount": {
                        "total": str(amount),
                        "currency": sale.amount.currency
                    }
                }
            
            refund = sale.refund(refund_request)
            
            if refund.success():
                logger.info(
                    "PayPal refund successful",
                    sale_id=sale_id,
                    refund_id=refund.id,
                    amount=amount
                )
                
                return {
                    "id": refund.id,
                    "status": refund.state,
                    "amount": refund.amount,
                    "sale_id": sale_id,
                    "created_time": refund.create_time
                }
            else:
                error_msg = refund.error.get("message", "Unknown error") if hasattr(refund, "error") else "Refund failed"
                logger.error("PayPal refund failed", error=error_msg, sale_id=sale_id)
                raise Exception(f"PayPal refund failed: {error_msg}")
                
        except Exception as e:
            logger.error("PayPal refund_payment error", error=str(e), sale_id=sale_id)
            raise
    
    async def verify_webhook(self, headers: Dict[str, str], body: str) -> bool:
        """
        Verify PayPal webhook signature
        
        Args:
            headers: Webhook request headers
            body: Webhook request body
            
        Returns:
            True if webhook is valid
        """
        try:
            settings = get_settings()
            webhook_id = settings.PAYPAL_WEBHOOK_ID
            
            transmission_id = headers.get("paypal-transmission-id")
            transmission_time = headers.get("paypal-transmission-time")
            cert_url = headers.get("paypal-cert-url")
            auth_algo = headers.get("paypal-auth-algo")
            transmission_sig = headers.get("paypal-transmission-sig")
            
            response = paypalrestsdk.WebhookEvent.verify(
                transmission_id,
                transmission_time,
                webhook_id,
                body,
                cert_url,
                transmission_sig,
                auth_algo
            )
            
            is_valid = response.get("verification_status") == "SUCCESS"
            
            if is_valid:
                logger.info("PayPal webhook verified successfully")
            else:
                logger.warning("PayPal webhook verification failed")
            
            return is_valid
            
        except Exception as e:
            logger.error("PayPal webhook verification error", error=str(e))
            return False


# For easy import
__all__ = ['PayPalServiceProduction']


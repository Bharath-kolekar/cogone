# backend/app/services/razorpay_service_production.py
"""
Razorpay Payment Service - PRODUCTION IMPLEMENTATION

This is the real Razorpay integration using the Razorpay Python SDK.
Replace the stub implementation with this for production use.

Installation:
    pip install razorpay

Documentation:
    https://razorpay.com/docs/api/
"""
from typing import Dict, Any, Optional
import structlog
import razorpay
import hmac
import hashlib
from ..core.config import get_settings

logger = structlog.get_logger()


class RazorpayServiceProduction:
    """
    Production Razorpay payment service with real API integration
    
    Features:
    - Real Razorpay API calls
    - Order creation and capture
    - Payment verification
    - Refund support
    - Webhook verification
    """
    
    def __init__(self):
        settings = get_settings()
        
        # Load credentials from settings
        self.api_key = settings.RAZORPAY_API_KEY
        self.api_secret = settings.RAZORPAY_API_SECRET
        
        # Initialize Razorpay client
        self.client = razorpay.Client(auth=(self.api_key, self.api_secret))
        
        logger.info(
            "✅ Razorpay Service initialized (PRODUCTION)",
            api_key=self.api_key[:10] + "..."
        )
    
    async def create_order(self, amount: float, currency: str = "INR", **kwargs) -> Dict[str, Any]:
        """
        Create a Razorpay order
        
        Args:
            amount: Order amount (in rupees/currency units)
            currency: Currency code (INR, USD, etc.)
            **kwargs: Additional order parameters
                - receipt: Receipt ID
                - notes: Additional notes
                - partial_payment: Allow partial payments
                
        Returns:
            Order details
        """
        try:
            # Convert amount to paise/cents (Razorpay expects smallest currency unit)
            amount_in_paise = int(amount * 100)
            
            # Prepare order data
            order_data = {
                "amount": amount_in_paise,
                "currency": currency,
                "receipt": kwargs.get("receipt", f"receipt_{int(amount)}"),
                "notes": kwargs.get("notes", {}),
            }
            
            if "partial_payment" in kwargs:
                order_data["partial_payment"] = kwargs["partial_payment"]
            
            # Create order
            order = self.client.order.create(data=order_data)
            
            logger.info(
                "Razorpay order created successfully",
                order_id=order["id"],
                amount=amount,
                currency=currency
            )
            
            return {
                "id": order["id"],
                "entity": order["entity"],
                "amount": order["amount"],
                "amount_paid": order.get("amount_paid", 0),
                "amount_due": order.get("amount_due", order["amount"]),
                "currency": order["currency"],
                "receipt": order.get("receipt"),
                "status": order["status"],
                "attempts": order.get("attempts", 0),
                "notes": order.get("notes", {}),
                "created_at": order["created_at"]
            }
            
        except razorpay.errors.BadRequestError as e:
            logger.error("Razorpay bad request", error=str(e), amount=amount)
            raise Exception(f"Razorpay order creation failed: {str(e)}")
        except Exception as e:
            logger.error("Razorpay create_order error", error=str(e), amount=amount)
            raise
    
    async def capture_payment(self, payment_id: str, amount: float, currency: str = "INR") -> Dict[str, Any]:
        """
        Capture a Razorpay payment
        
        Args:
            payment_id: Razorpay payment ID
            amount: Amount to capture (in rupees/currency units)
            currency: Currency code
            
        Returns:
            Captured payment details
        """
        try:
            # Convert amount to paise/cents
            amount_in_paise = int(amount * 100)
            
            # Capture payment
            payment = self.client.payment.capture(payment_id, amount_in_paise, {"currency": currency})
            
            logger.info(
                "Razorpay payment captured successfully",
                payment_id=payment_id,
                amount=amount,
                status=payment["status"]
            )
            
            return {
                "id": payment["id"],
                "entity": payment["entity"],
                "amount": payment["amount"],
                "currency": payment["currency"],
                "status": payment["status"],
                "order_id": payment.get("order_id"),
                "method": payment.get("method"),
                "captured": payment.get("captured", True),
                "email": payment.get("email"),
                "contact": payment.get("contact"),
                "created_at": payment["created_at"]
            }
            
        except razorpay.errors.BadRequestError as e:
            logger.error("Razorpay capture failed", error=str(e), payment_id=payment_id)
            raise Exception(f"Razorpay payment capture failed: {str(e)}")
        except Exception as e:
            logger.error("Razorpay capture_payment error", error=str(e), payment_id=payment_id)
            raise
    
    async def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """
        Get Razorpay payment details
        
        Args:
            payment_id: Razorpay payment ID
            
        Returns:
            Payment details
        """
        try:
            payment = self.client.payment.fetch(payment_id)
            
            return {
                "id": payment["id"],
                "entity": payment["entity"],
                "amount": payment["amount"],
                "currency": payment["currency"],
                "status": payment["status"],
                "order_id": payment.get("order_id"),
                "method": payment.get("method"),
                "captured": payment.get("captured", False),
                "email": payment.get("email"),
                "contact": payment.get("contact"),
                "fee": payment.get("fee"),
                "tax": payment.get("tax"),
                "created_at": payment["created_at"]
            }
            
        except Exception as e:
            logger.error("Razorpay get_payment error", error=str(e), payment_id=payment_id)
            raise
    
    async def get_order(self, order_id: str) -> Dict[str, Any]:
        """
        Get Razorpay order details
        
        Args:
            order_id: Razorpay order ID
            
        Returns:
            Order details
        """
        try:
            order = self.client.order.fetch(order_id)
            
            return {
                "id": order["id"],
                "entity": order["entity"],
                "amount": order["amount"],
                "amount_paid": order.get("amount_paid", 0),
                "amount_due": order.get("amount_due", order["amount"]),
                "currency": order["currency"],
                "receipt": order.get("receipt"),
                "status": order["status"],
                "attempts": order.get("attempts", 0),
                "notes": order.get("notes", {}),
                "created_at": order["created_at"]
            }
            
        except Exception as e:
            logger.error("Razorpay get_order error", error=str(e), order_id=order_id)
            raise
    
    async def refund_payment(self, payment_id: str, amount: Optional[float] = None, **kwargs) -> Dict[str, Any]:
        """
        Refund a Razorpay payment
        
        Args:
            payment_id: Razorpay payment ID
            amount: Refund amount in rupees (None for full refund)
            **kwargs: Additional refund parameters
                - notes: Refund notes
                - receipt: Refund receipt
                
        Returns:
            Refund details
        """
        try:
            refund_data = {}
            
            if amount is not None:
                # Convert amount to paise/cents
                refund_data["amount"] = int(amount * 100)
            
            if "notes" in kwargs:
                refund_data["notes"] = kwargs["notes"]
            
            if "receipt" in kwargs:
                refund_data["receipt"] = kwargs["receipt"]
            
            # Create refund
            refund = self.client.payment.refund(payment_id, refund_data)
            
            logger.info(
                "Razorpay refund successful",
                payment_id=payment_id,
                refund_id=refund["id"],
                amount=amount
            )
            
            return {
                "id": refund["id"],
                "entity": refund["entity"],
                "amount": refund["amount"],
                "currency": refund.get("currency"),
                "payment_id": refund["payment_id"],
                "status": refund["status"],
                "receipt": refund.get("receipt"),
                "created_at": refund["created_at"]
            }
            
        except razorpay.errors.BadRequestError as e:
            logger.error("Razorpay refund failed", error=str(e), payment_id=payment_id)
            raise Exception(f"Razorpay refund failed: {str(e)}")
        except Exception as e:
            logger.error("Razorpay refund_payment error", error=str(e), payment_id=payment_id)
            raise
    
    async def verify_payment_signature(self, order_id: str, payment_id: str, signature: str) -> bool:
        """
        Verify Razorpay payment signature
        
        Args:
            order_id: Razorpay order ID
            payment_id: Razorpay payment ID
            signature: Payment signature from client
            
        Returns:
            True if signature is valid
        """
        try:
            # Generate expected signature
            message = f"{order_id}|{payment_id}"
            expected_signature = hmac.new(
                self.api_secret.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            is_valid = hmac.compare_digest(expected_signature, signature)
            
            if is_valid:
                logger.info("Razorpay payment signature verified successfully", payment_id=payment_id)
            else:
                logger.warning("Razorpay payment signature verification failed", payment_id=payment_id)
            
            return is_valid
            
        except Exception as e:
            logger.error("Razorpay signature verification error", error=str(e))
            return False
    
    async def verify_webhook(self, body: str, signature: str) -> bool:
        """
        Verify Razorpay webhook signature
        
        Args:
            body: Webhook request body
            signature: X-Razorpay-Signature header value
            
        Returns:
            True if webhook is valid
        """
        try:
            settings = get_settings()
            webhook_secret = settings.RAZORPAY_WEBHOOK_SECRET
            
            # Generate expected signature
            expected_signature = hmac.new(
                webhook_secret.encode(),
                body.encode(),
                hashlib.sha256
            ).hexdigest()
            
            is_valid = hmac.compare_digest(expected_signature, signature)
            
            if is_valid:
                logger.info("Razorpay webhook verified successfully")
            else:
                logger.warning("Razorpay webhook verification failed")
            
            return is_valid
            
        except Exception as e:
            logger.error("Razorpay webhook verification error", error=str(e))
            return False
    
    async def create_customer(self, name: str, email: str, contact: str, **kwargs) -> Dict[str, Any]:
        """
        Create a Razorpay customer
        
        Args:
            name: Customer name
            email: Customer email
            contact: Customer contact number
            **kwargs: Additional customer parameters
                
        Returns:
            Customer details
        """
        try:
            customer_data = {
                "name": name,
                "email": email,
                "contact": contact,
                "notes": kwargs.get("notes", {})
            }
            
            customer = self.client.customer.create(data=customer_data)
            
            logger.info("Razorpay customer created successfully", customer_id=customer["id"])
            
            return {
                "id": customer["id"],
                "entity": customer["entity"],
                "name": customer["name"],
                "email": customer["email"],
                "contact": customer["contact"],
                "created_at": customer["created_at"]
            }
            
        except Exception as e:
            logger.error("Razorpay create_customer error", error=str(e))
            raise


# For easy import
__all__ = ['RazorpayServiceProduction']


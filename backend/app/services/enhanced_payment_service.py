"""
Enhanced Payment Service with Multi-Provider Integration

This service provides comprehensive payment processing with Razorpay, PayPal, Google Pay, UPI, and QR code support.
"""

import structlog
import asyncio
import json
import time
import hashlib
import hmac
import base64
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from enum import Enum
import uuid
import httpx
import qrcode
from io import BytesIO

from app.core.config import settings
from app.core.database import get_supabase_client

logger = structlog.get_logger(__name__)

class PaymentProvider(Enum):
    """Payment provider types"""
    RAZORPAY = "razorpay"
    PAYPAL = "paypal"
    GOOGLE_PAY = "google_pay"
    UPI = "upi"
    QR_CODE = "qr_code"

class PaymentStatus(Enum):
    """Payment status types"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentMethod(Enum):
    """Payment method types"""
    CARD = "card"
    UPI = "upi"
    NET_BANKING = "net_banking"
    WALLET = "wallet"
    EMI = "emi"
    COD = "cod"

class SubscriptionPlan(Enum):
    """Subscription plan types"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class PaymentOrder:
    """Payment order model"""
    def __init__(self, 
                 order_id: str,
                 user_id: str,
                 amount: float,
                 currency: str,
                 provider: PaymentProvider,
                 status: PaymentStatus = PaymentStatus.PENDING,
                 payment_data: Dict[str, Any] = None,
                 metadata: Dict[str, Any] = None):
        self.order_id = order_id
        self.user_id = user_id
        self.amount = amount
        self.currency = currency
        self.provider = provider
        self.status = status
        self.payment_data = payment_data or {}
        self.metadata = metadata or {}
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.expires_at = self.created_at + timedelta(minutes=15)

class PaymentResult:
    """Payment result model"""
    def __init__(self, 
                 order_id: str,
                 payment_id: Optional[str] = None,
                 status: PaymentStatus = PaymentStatus.PENDING,
                 amount: float = 0.0,
                 currency: str = "INR",
                 provider: PaymentProvider = PaymentProvider.RAZORPAY,
                 transaction_data: Dict[str, Any] = None):
        self.order_id = order_id
        self.payment_id = payment_id
        self.status = status
        self.amount = amount
        self.currency = currency
        self.provider = provider
        self.transaction_data = transaction_data or {}
        self.processed_at = datetime.now()

class EnhancedPaymentService:
    """Enhanced payment service with multi-provider support"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        
        # Payment providers configuration
        self.providers_config = {
            PaymentProvider.RAZORPAY: {
                "enabled": True,
                "api_key": settings.RAZORPAY_API_KEY,
                "api_secret": settings.RAZORPAY_API_SECRET,
                "webhook_secret": settings.RAZORPAY_WEBHOOK_SECRET,
                "base_url": "https://api.razorpay.com/v1"
            },
            PaymentProvider.PAYPAL: {
                "enabled": True,
                "client_id": settings.PAYPAL_CLIENT_ID,
                "client_secret": settings.PAYPAL_CLIENT_SECRET,
                "base_url": "https://api-m.paypal.com" if settings.PAYPAL_SANDBOX == "false" else "https://api-m.sandbox.paypal.com"
            },
            PaymentProvider.GOOGLE_PAY: {
                "enabled": True,
                "merchant_id": settings.GOOGLE_PAY_MERCHANT_ID,
                "api_key": settings.GOOGLE_PAY_API_KEY
            },
            PaymentProvider.UPI: {
                "enabled": True,
                "merchant_id": settings.UPI_MERCHANT_ID,
                "merchant_name": settings.UPI_MERCHANT_NAME
            },
            PaymentProvider.QR_CODE: {
                "enabled": True,
                "base_url": settings.BASE_URL
            }
        }
        
        # Payment processing state
        self.active_orders: Dict[str, PaymentOrder] = {}
        self.completed_payments: Dict[str, PaymentResult] = {}
        
        # Performance metrics
        self.metrics = {
            "total_orders": 0,
            "successful_payments": 0,
            "failed_payments": 0,
            "total_amount_processed": 0.0,
            "average_payment_time": 0.0,
            "provider_success_rates": {}
        }
        
        logger.info("Enhanced Payment Service initialized with multi-provider support")

    async def create_payment_order(self, 
                                 user_id: str,
                                 amount: float,
                                 currency: str = "INR",
                                 provider: Optional[PaymentProvider] = None,
                                 description: str = "",
                                 metadata: Dict[str, Any] = None) -> PaymentOrder:
        """Create a new payment order"""
        try:
            order_id = f"order_{uuid.uuid4().hex[:16]}"
            
            # Auto-select provider if not specified
            if not provider:
                provider = self._select_best_provider(amount, currency, user_id)
            
            logger.info(f"Creating payment order", 
                       order_id=order_id,
                       user_id=user_id,
                       amount=amount,
                       currency=currency,
                       provider=provider.value)
            
            # Create payment order
            order = PaymentOrder(
                order_id=order_id,
                user_id=user_id,
                amount=amount,
                currency=currency,
                provider=provider,
                metadata=metadata or {}
            )
            
            # Generate provider-specific payment data
            payment_data = await self._generate_payment_data(order, description)
            order.payment_data = payment_data
            
            # Store order
            self.active_orders[order_id] = order
            
            # Store in database
            await self._store_payment_order(order)
            
            # Update metrics
            self.metrics["total_orders"] += 1
            
            logger.info(f"Payment order created successfully", 
                       order_id=order_id,
                       provider=provider.value,
                       amount=amount)
            
            return order
            
        except Exception as e:
            logger.error(f"Payment order creation failed", 
                        error=str(e), 
                        user_id=user_id,
                        amount=amount)
            raise

    async def _generate_payment_data(self, order: PaymentOrder, description: str) -> Dict[str, Any]:
        """Generate provider-specific payment data"""
        try:
            provider_config = self.providers_config[order.provider]
            
            if order.provider == PaymentProvider.RAZORPAY:
                return await self._generate_razorpay_data(order, description)
            elif order.provider == PaymentProvider.PAYPAL:
                return await self._generate_paypal_data(order, description)
            elif order.provider == PaymentProvider.GOOGLE_PAY:
                return await self._generate_google_pay_data(order, description)
            elif order.provider == PaymentProvider.UPI:
                return await self._generate_upi_data(order, description)
            elif order.provider == PaymentProvider.QR_CODE:
                return await self._generate_qr_code_data(order, description)
            else:
                raise ValueError(f"Unsupported payment provider: {order.provider}")
                
        except Exception as e:
            logger.error(f"Payment data generation failed", 
                        error=str(e), 
                        order_id=order.order_id,
                        provider=order.provider.value)
            raise

    async def _generate_razorpay_data(self, order: PaymentOrder, description: str) -> Dict[str, Any]:
        """Generate Razorpay payment data"""
        try:
            async with httpx.AsyncClient() as client:
                # Create Razorpay order
                order_data = {
                    "amount": int(order.amount * 100),  # Convert to paise
                    "currency": order.currency,
                    "receipt": order.order_id,
                    "notes": {
                        "description": description,
                        "user_id": order.user_id
                    }
                }
                
                headers = {
                    "Authorization": f"Basic {base64.b64encode(f'{settings.RAZORPAY_API_KEY}:{settings.RAZORPAY_API_SECRET}'.encode()).decode()}",
                    "Content-Type": "application/json"
                }
                
                response = await client.post(
                    f"{self.providers_config[PaymentProvider.RAZORPAY]['base_url']}/orders",
                    json=order_data,
                    headers=headers
                )
                
                if response.status_code == 200:
                    razorpay_order = response.json()
                    return {
                        "razorpay_order_id": razorpay_order["id"],
                        "amount": razorpay_order["amount"],
                        "currency": razorpay_order["currency"],
                        "receipt": razorpay_order["receipt"],
                        "status": razorpay_order["status"]
                    }
                else:
                    raise Exception(f"Razorpay order creation failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"Razorpay data generation failed", error=str(e))
            raise

    async def _generate_paypal_data(self, order: PaymentOrder, description: str) -> Dict[str, Any]:
        """Generate PayPal payment data"""
        try:
            async with httpx.AsyncClient() as client:
                # Get PayPal access token
                token_response = await client.post(
                    f"{self.providers_config[PaymentProvider.PAYPAL]['base_url']}/v1/oauth2/token",
                    data={"grant_type": "client_credentials"},
                    auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                if token_response.status_code != 200:
                    raise Exception(f"PayPal token request failed: {token_response.text}")
                
                access_token = token_response.json()["access_token"]
                
                # Create PayPal order
                order_data = {
                    "intent": "CAPTURE",
                    "purchase_units": [{
                        "reference_id": order.order_id,
                        "amount": {
                            "currency_code": order.currency,
                            "value": str(order.amount)
                        },
                        "description": description
                    }],
                    "application_context": {
                        "return_url": f"{settings.BASE_URL}/payment/return",
                        "cancel_url": f"{settings.BASE_URL}/payment/cancel"
                    }
                }
                
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
                
                response = await client.post(
                    f"{self.providers_config[PaymentProvider.PAYPAL]['base_url']}/v2/checkout/orders",
                    json=order_data,
                    headers=headers
                )
                
                if response.status_code == 201:
                    paypal_order = response.json()
                    return {
                        "paypal_order_id": paypal_order["id"],
                        "status": paypal_order["status"],
                        "approve_url": next(link["href"] for link in paypal_order["links"] if link["rel"] == "approve"),
                        "amount": order.amount,
                        "currency": order.currency
                    }
                else:
                    raise Exception(f"PayPal order creation failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"PayPal data generation failed", error=str(e))
            raise

    async def _generate_google_pay_data(self, order: PaymentOrder, description: str) -> Dict[str, Any]:
        """Generate Google Pay payment data"""
        try:
            # Google Pay integration (simplified for demo)
            return {
                "google_pay_token": f"gp_token_{order.order_id}",
                "merchant_id": settings.GOOGLE_PAY_MERCHANT_ID,
                "amount": order.amount,
                "currency": order.currency,
                "description": description,
                "payment_methods": ["CARD", "UPI"],
                "callback_url": f"{settings.BASE_URL}/payment/google-pay/callback"
            }
            
        except Exception as e:
            logger.error(f"Google Pay data generation failed", error=str(e))
            raise

    async def _generate_upi_data(self, order: PaymentOrder, description: str) -> Dict[str, Any]:
        """Generate UPI payment data"""
        try:
            # Generate UPI payment URL
            upi_id = f"{settings.UPI_MERCHANT_ID}@{settings.UPI_MERCHANT_NAME}"
            upi_url = f"upi://pay?pa={upi_id}&pn={settings.UPI_MERCHANT_NAME}&am={order.amount}&cu={order.currency}&tn={description}&tr={order.order_id}"
            
            return {
                "upi_id": upi_id,
                "upi_url": upi_url,
                "amount": order.amount,
                "currency": order.currency,
                "merchant_name": settings.UPI_MERCHANT_NAME,
                "transaction_id": order.order_id,
                "callback_url": f"{settings.BASE_URL}/payment/upi/callback"
            }
            
        except Exception as e:
            logger.error(f"UPI data generation failed", error=str(e))
            raise

    async def _generate_qr_code_data(self, order: PaymentOrder, description: str) -> Dict[str, Any]:
        """Generate QR code payment data"""
        try:
            # Generate QR code for payment
            qr_data = {
                "order_id": order.order_id,
                "amount": order.amount,
                "currency": order.currency,
                "merchant_name": settings.UPI_MERCHANT_NAME,
                "upi_id": f"{settings.UPI_MERCHANT_ID}@{settings.UPI_MERCHANT_NAME}",
                "timestamp": datetime.now().isoformat()
            }
            
            # Create QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(json.dumps(qr_data))
            qr.make(fit=True)
            
            # Generate QR code image
            img = qr.make_image(fill_color="black", back_color="white")
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            
            # Encode as base64
            qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                "qr_code": qr_code_base64,
                "qr_data": qr_data,
                "amount": order.amount,
                "currency": order.currency,
                "expires_at": order.expires_at.isoformat(),
                "payment_url": f"{settings.BASE_URL}/payment/qr/{order.order_id}"
            }
            
        except Exception as e:
            logger.error(f"QR code generation failed", error=str(e))
            raise

    def _select_best_provider(self, amount: float, currency: str, user_id: str) -> PaymentProvider:
        """Select the best payment provider based on amount, currency, and user preferences"""
        try:
            # Logic to select best provider
            if currency == "INR":
                if amount <= 5000:
                    return PaymentProvider.UPI
                elif amount <= 50000:
                    return PaymentProvider.RAZORPAY
                else:
                    return PaymentProvider.RAZORPAY
            else:
                return PaymentProvider.PAYPAL
                
        except Exception as e:
            logger.error(f"Provider selection failed", error=str(e))
            return PaymentProvider.RAZORPAY

    async def verify_payment(self, 
                           order_id: str, 
                           payment_data: Dict[str, Any]) -> PaymentResult:
        """Verify payment with the provider"""
        try:
            if order_id not in self.active_orders:
                raise ValueError(f"Order not found: {order_id}")
            
            order = self.active_orders[order_id]
            
            logger.info(f"Verifying payment", 
                       order_id=order_id,
                       provider=order.provider.value)
            
            # Verify with provider
            if order.provider == PaymentProvider.RAZORPAY:
                result = await self._verify_razorpay_payment(order, payment_data)
            elif order.provider == PaymentProvider.PAYPAL:
                result = await self._verify_paypal_payment(order, payment_data)
            elif order.provider == PaymentProvider.GOOGLE_PAY:
                result = await self._verify_google_pay_payment(order, payment_data)
            elif order.provider == PaymentProvider.UPI:
                result = await self._verify_upi_payment(order, payment_data)
            elif order.provider == PaymentProvider.QR_CODE:
                result = await self._verify_qr_code_payment(order, payment_data)
            else:
                raise ValueError(f"Unsupported provider: {order.provider}")
            
            # Update order status
            order.status = result.status
            order.updated_at = datetime.now()
            
            # Store result
            self.completed_payments[order_id] = result
            
            # Update metrics
            self._update_payment_metrics(result)
            
            logger.info(f"Payment verification completed", 
                       order_id=order_id,
                       status=result.status.value,
                       amount=result.amount)
            
            return result
            
        except Exception as e:
            logger.error(f"Payment verification failed", 
                        error=str(e), 
                        order_id=order_id)
            raise

    async def _verify_razorpay_payment(self, order: PaymentOrder, payment_data: Dict[str, Any]) -> PaymentResult:
        """Verify Razorpay payment"""
        try:
            # Verify Razorpay signature
            razorpay_order_id = payment_data.get("razorpay_order_id")
            razorpay_payment_id = payment_data.get("razorpay_payment_id")
            razorpay_signature = payment_data.get("razorpay_signature")
            
            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature]):
                raise ValueError("Missing Razorpay payment data")
            
            # Verify signature
            message = f"{razorpay_order_id}|{razorpay_payment_id}"
            signature = hmac.new(
                settings.RAZORPAY_API_SECRET.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if signature != razorpay_signature:
                raise ValueError("Invalid Razorpay signature")
            
            return PaymentResult(
                order_id=order.order_id,
                payment_id=razorpay_payment_id,
                status=PaymentStatus.COMPLETED,
                amount=order.amount,
                currency=order.currency,
                provider=order.provider,
                transaction_data={
                    "razorpay_order_id": razorpay_order_id,
                    "razorpay_payment_id": razorpay_payment_id,
                    "verified_at": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Razorpay verification failed", error=str(e))
            return PaymentResult(
                order_id=order.order_id,
                status=PaymentStatus.FAILED,
                amount=order.amount,
                currency=order.currency,
                provider=order.provider,
                transaction_data={"error": str(e)}
            )

    async def _verify_paypal_payment(self, order: PaymentOrder, payment_data: Dict[str, Any]) -> PaymentResult:
        """Verify PayPal payment"""
        try:
            paypal_order_id = payment_data.get("paypal_order_id")
            
            if not paypal_order_id:
                raise ValueError("Missing PayPal order ID")
            
            # Verify with PayPal API
            async with httpx.AsyncClient() as client:
                # Get access token
                token_response = await client.post(
                    f"{self.providers_config[PaymentProvider.PAYPAL]['base_url']}/v1/oauth2/token",
                    data={"grant_type": "client_credentials"},
                    auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_CLIENT_SECRET),
                    headers={"Content-Type": "application/x-www-form-urlencoded"}
                )
                
                access_token = token_response.json()["access_token"]
                
                # Get order details
                headers = {"Authorization": f"Bearer {access_token}"}
                response = await client.get(
                    f"{self.providers_config[PaymentProvider.PAYPAL]['base_url']}/v2/checkout/orders/{paypal_order_id}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    order_details = response.json()
                    
                    if order_details["status"] == "COMPLETED":
                        return PaymentResult(
                            order_id=order.order_id,
                            payment_id=paypal_order_id,
                            status=PaymentStatus.COMPLETED,
                            amount=order.amount,
                            currency=order.currency,
                            provider=order.provider,
                            transaction_data={
                                "paypal_order_id": paypal_order_id,
                                "status": order_details["status"],
                                "verified_at": datetime.now().isoformat()
                            }
                        )
                    else:
                        return PaymentResult(
                            order_id=order.order_id,
                            status=PaymentStatus.FAILED,
                            amount=order.amount,
                            currency=order.currency,
                            provider=order.provider,
                            transaction_data={"error": f"PayPal order status: {order_details['status']}"}
                        )
                else:
                    raise Exception(f"PayPal verification failed: {response.text}")
                    
        except Exception as e:
            logger.error(f"PayPal verification failed", error=str(e))
            return PaymentResult(
                order_id=order.order_id,
                status=PaymentStatus.FAILED,
                amount=order.amount,
                currency=order.currency,
                provider=order.provider,
                transaction_data={"error": str(e)}
            )

    async def _verify_google_pay_payment(self, order: PaymentOrder, payment_data: Dict[str, Any]) -> PaymentResult:
        """Verify Google Pay payment"""
        try:
            # Google Pay verification (simplified)
            google_pay_token = payment_data.get("google_pay_token")
            
            if not google_pay_token:
                raise ValueError("Missing Google Pay token")
            
            # Simulate verification
            return PaymentResult(
                order_id=order.order_id,
                payment_id=f"gp_{order.order_id}",
                status=PaymentStatus.COMPLETED,
                amount=order.amount,
                currency=order.currency,
                provider=order.provider,
                transaction_data={
                    "google_pay_token": google_pay_token,
                    "verified_at": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Google Pay verification failed", error=str(e))
            return PaymentResult(
                order_id=order.order_id,
                status=PaymentStatus.FAILED,
                amount=order.amount,
                currency=order.currency,
                provider=order.provider,
                transaction_data={"error": str(e)}
            )

    async def _verify_upi_payment(self, order: PaymentOrder, payment_data: Dict[str, Any]) -> PaymentResult:
        """Verify UPI payment"""
        try:
            # UPI verification (simplified)
            upi_transaction_id = payment_data.get("upi_transaction_id")
            
            if not upi_transaction_id:
                raise ValueError("Missing UPI transaction ID")
            
            # Simulate verification
            return PaymentResult(
                order_id=order.order_id,
                payment_id=upi_transaction_id,
                status=PaymentStatus.COMPLETED,
                amount=order.amount,
                currency=order.currency,
                provider=order.provider,
                transaction_data={
                    "upi_transaction_id": upi_transaction_id,
                    "verified_at": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"UPI verification failed", error=str(e))
            return PaymentResult(
                order_id=order.order_id,
                status=PaymentStatus.FAILED,
                amount=order.amount,
                currency=order.currency,
                provider=order.provider,
                transaction_data={"error": str(e)}
            )

    async def _verify_qr_code_payment(self, order: PaymentOrder, payment_data: Dict[str, Any]) -> PaymentResult:
        """Verify QR code payment"""
        try:
            # QR code verification (simplified)
            qr_transaction_id = payment_data.get("qr_transaction_id")
            
            if not qr_transaction_id:
                raise ValueError("Missing QR transaction ID")
            
            # Simulate verification
            return PaymentResult(
                order_id=order.order_id,
                payment_id=qr_transaction_id,
                status=PaymentStatus.COMPLETED,
                amount=order.amount,
                currency=order.currency,
                provider=order.provider,
                transaction_data={
                    "qr_transaction_id": qr_transaction_id,
                    "verified_at": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"QR code verification failed", error=str(e))
            return PaymentResult(
                order_id=order.order_id,
                status=PaymentStatus.FAILED,
                amount=order.amount,
                currency=order.currency,
                provider=order.provider,
                transaction_data={"error": str(e)}
            )

    async def _store_payment_order(self, order: PaymentOrder):
        """Store payment order in database"""
        try:
            order_data = {
                "order_id": order.order_id,
                "user_id": order.user_id,
                "amount": order.amount,
                "currency": order.currency,
                "provider": order.provider.value,
                "status": order.status.value,
                "payment_data": order.payment_data,
                "metadata": order.metadata,
                "created_at": order.created_at.isoformat(),
                "expires_at": order.expires_at.isoformat()
            }
            
            # Store in Supabase
            result = self.supabase.table("payment_orders").insert(order_data).execute()
            
            if not result.data:
                raise Exception("Failed to store payment order in database")
                
        except Exception as e:
            logger.error(f"Payment order storage failed", error=str(e))
            raise

    def _update_payment_metrics(self, result: PaymentResult):
        """Update payment metrics"""
        try:
            if result.status == PaymentStatus.COMPLETED:
                self.metrics["successful_payments"] += 1
                self.metrics["total_amount_processed"] += result.amount
            else:
                self.metrics["failed_payments"] += 1
            
            # Update provider success rate
            provider = result.provider.value
            if provider not in self.metrics["provider_success_rates"]:
                self.metrics["provider_success_rates"][provider] = {"success": 0, "total": 0}
            
            self.metrics["provider_success_rates"][provider]["total"] += 1
            if result.status == PaymentStatus.COMPLETED:
                self.metrics["provider_success_rates"][provider]["success"] += 1
                
        except Exception as e:
            logger.error(f"Metrics update failed", error=str(e))

    async def get_payment_status(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get payment status"""
        try:
            # Check active orders
            if order_id in self.active_orders:
                order = self.active_orders[order_id]
                return {
                    "order_id": order_id,
                    "status": order.status.value,
                    "amount": order.amount,
                    "currency": order.currency,
                    "provider": order.provider.value,
                    "created_at": order.created_at.isoformat(),
                    "expires_at": order.expires_at.isoformat()
                }
            
            # Check completed payments
            if order_id in self.completed_payments:
                result = self.completed_payments[order_id]
                return {
                    "order_id": order_id,
                    "status": result.status.value,
                    "payment_id": result.payment_id,
                    "amount": result.amount,
                    "currency": result.currency,
                    "provider": result.provider.value,
                    "processed_at": result.processed_at.isoformat()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Payment status retrieval failed", error=str(e))
            return None

    async def get_service_metrics(self) -> Dict[str, Any]:
        """Get payment service metrics"""
        try:
            # Calculate provider success rates
            provider_success_rates = {}
            for provider, stats in self.metrics["provider_success_rates"].items():
                success_rate = (stats["success"] / stats["total"]) * 100 if stats["total"] > 0 else 0
                provider_success_rates[provider] = {
                    "success_rate": success_rate,
                    "total_payments": stats["total"],
                    "successful_payments": stats["success"]
                }
            
            return {
                "service_metrics": {
                    **self.metrics,
                    "provider_success_rates": provider_success_rates
                },
                "active_orders_count": len(self.active_orders),
                "completed_payments_count": len(self.completed_payments),
                "total_success_rate": (
                    self.metrics["successful_payments"] / 
                    max(1, self.metrics["total_orders"])
                ) * 100
            }
            
        except Exception as e:
            logger.error(f"Service metrics retrieval failed", error=str(e))
            return {}

# Global instance
enhanced_payment_service = EnhancedPaymentService()

# Backward compatibility: Alias for old PaymentService imports
PaymentService = EnhancedPaymentService
payment_service = enhanced_payment_service

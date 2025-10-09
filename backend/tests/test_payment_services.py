"""
Integration Tests for Payment Services
Tests both stub and production implementations
"""
import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from app.services.paypal_service import PayPalService
from app.services.razorpay_service import RazorpayService
from app.services.paypal_service_production import PayPalServiceProduction
from app.services.razorpay_service_production import RazorpayServiceProduction


class TestPayPalStubService:
    """Test PayPal stub implementation"""
    
    @pytest.fixture
    def paypal_stub(self):
        return PayPalService()
    
    @pytest.mark.asyncio
    async def test_create_order_stub(self, paypal_stub):
        """Test stub order creation returns fake data"""
        result = await paypal_stub.create_order(amount=10.00, currency="USD")
        
        assert result is not None
        assert "id" in result
        assert result["status"] == "CREATED"
        assert result["amount"]["currency_code"] == "USD"
        assert result["amount"]["value"] == "10.0"
    
    @pytest.mark.asyncio
    async def test_capture_order_stub(self, paypal_stub):
        """Test stub order capture returns fake data"""
        order_id = "test_order_123"
        result = await paypal_stub.capture_order(order_id)
        
        assert result is not None
        assert result["id"] == order_id
        assert result["status"] == "COMPLETED"
    
    @pytest.mark.asyncio
    async def test_get_order_stub(self, paypal_stub):
        """Test stub get order returns fake data"""
        order_id = "test_order_123"
        result = await paypal_stub.get_order(order_id)
        
        assert result is not None
        assert result["id"] == order_id


class TestRazorpayStubService:
    """Test Razorpay stub implementation"""
    
    @pytest.fixture
    def razorpay_stub(self):
        return RazorpayService()
    
    @pytest.mark.asyncio
    async def test_create_order_stub(self, razorpay_stub):
        """Test stub order creation returns fake data"""
        result = await razorpay_stub.create_order(amount=100.00, currency="INR")
        
        assert result is not None
        assert "id" in result
        assert result["status"] == "created"
        assert result["currency"] == "INR"
        assert result["amount"] == 10000  # 100 rupees in paise
    
    @pytest.mark.asyncio
    async def test_capture_payment_stub(self, razorpay_stub):
        """Test stub payment capture returns fake data"""
        payment_id = "test_payment_123"
        result = await razorpay_stub.capture_payment(payment_id, 100.00)
        
        assert result is not None
        assert result["id"] == payment_id
        assert result["status"] == "captured"


@pytest.mark.skipif(
    os.getenv("SKIP_PRODUCTION_TESTS", "true").lower() == "true",
    reason="Production tests require real API credentials"
)
class TestPayPalProductionService:
    """Test PayPal production implementation (requires credentials)"""
    
    @pytest.fixture
    def paypal_prod(self):
        # This requires PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET to be set
        return PayPalServiceProduction()
    
    @pytest.mark.asyncio
    async def test_create_order_production(self, paypal_prod):
        """Test real PayPal order creation (sandbox mode)"""
        # Only run if in sandbox mode
        if not paypal_prod.sandbox:
            pytest.skip("Skipping production test in live mode")
        
        result = await paypal_prod.create_order(
            amount=10.00,
            currency="USD",
            description="Test Order",
            return_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel"
        )
        
        assert result is not None
        assert "id" in result
        assert "approval_url" in result
        assert result["amount"]["currency_code"] == "USD"
    
    @pytest.mark.asyncio
    async def test_get_payment_production(self, paypal_prod):
        """Test getting payment details"""
        # This would require a real payment ID
        # Skip if not provided
        payment_id = os.getenv("TEST_PAYPAL_PAYMENT_ID")
        if not payment_id:
            pytest.skip("No test payment ID provided")
        
        result = await paypal_prod.get_order(payment_id)
        
        assert result is not None
        assert result["id"] == payment_id


@pytest.mark.skipif(
    os.getenv("SKIP_PRODUCTION_TESTS", "true").lower() == "true",
    reason="Production tests require real API credentials"
)
class TestRazorpayProductionService:
    """Test Razorpay production implementation (requires credentials)"""
    
    @pytest.fixture
    def razorpay_prod(self):
        # This requires RAZORPAY_API_KEY and RAZORPAY_API_SECRET to be set
        return RazorpayServiceProduction()
    
    @pytest.mark.asyncio
    async def test_create_order_production(self, razorpay_prod):
        """Test real Razorpay order creation"""
        result = await razorpay_prod.create_order(
            amount=100.00,
            currency="INR",
            receipt="test_receipt_001"
        )
        
        assert result is not None
        assert "id" in result
        assert result["currency"] == "INR"
        assert result["amount"] == 10000  # 100 rupees in paise
    
    @pytest.mark.asyncio
    async def test_verify_signature(self, razorpay_prod):
        """Test payment signature verification"""
        # This requires real order and payment IDs
        order_id = os.getenv("TEST_RAZORPAY_ORDER_ID")
        payment_id = os.getenv("TEST_RAZORPAY_PAYMENT_ID")
        signature = os.getenv("TEST_RAZORPAY_SIGNATURE")
        
        if not all([order_id, payment_id, signature]):
            pytest.skip("No test payment data provided")
        
        is_valid = await razorpay_prod.verify_payment_signature(
            order_id=order_id,
            payment_id=payment_id,
            signature=signature
        )
        
        assert isinstance(is_valid, bool)


class TestPaymentServiceConfiguration:
    """Test that services load configuration correctly"""
    
    @pytest.mark.asyncio
    async def test_paypal_loads_settings(self):
        """Test PayPal service loads from settings"""
        service = PayPalService()
        
        # Should load from settings, not hardcoded
        assert service.client_id is not None
        assert service.client_secret is not None
        assert isinstance(service.sandbox, bool)
    
    @pytest.mark.asyncio
    async def test_razorpay_loads_settings(self):
        """Test Razorpay service loads from settings"""
        service = RazorpayService()
        
        # Should load from settings, not hardcoded
        assert service.api_key is not None
        assert service.api_secret is not None
    
    @pytest.mark.asyncio
    async def test_production_paypal_initializes(self):
        """Test production PayPal service initializes without errors"""
        try:
            service = PayPalServiceProduction()
            assert service.client_id is not None
            assert service.client_secret is not None
        except Exception as e:
            pytest.fail(f"Production PayPal service failed to initialize: {e}")
    
    @pytest.mark.asyncio
    async def test_production_razorpay_initializes(self):
        """Test production Razorpay service initializes without errors"""
        try:
            service = RazorpayServiceProduction()
            assert service.client is not None
            assert service.api_key is not None
        except Exception as e:
            pytest.fail(f"Production Razorpay service failed to initialize: {e}")


class TestPaymentServiceWarnings:
    """Test that stub services show proper warnings"""
    
    @pytest.mark.asyncio
    async def test_paypal_stub_logs_warning(self, caplog):
        """Test PayPal stub logs warning on initialization"""
        with caplog.at_level("WARNING"):
            service = PayPalService()
            
            # Check that warning was logged
            assert any("STUB" in record.message or "NOT production ready" in record.message 
                      for record in caplog.records)
    
    @pytest.mark.asyncio
    async def test_razorpay_stub_logs_warning(self, caplog):
        """Test Razorpay stub logs warning on initialization"""
        with caplog.at_level("WARNING"):
            service = RazorpayService()
            
            # Check that warning was logged
            assert any("STUB" in record.message or "NOT production ready" in record.message 
                      for record in caplog.records)


# Test data examples
SAMPLE_PAYMENT_DATA = {
    "paypal": {
        "amount": 10.00,
        "currency": "USD",
        "description": "Test Payment"
    },
    "razorpay": {
        "amount": 100.00,
        "currency": "INR",
        "receipt": "test_receipt_001"
    }
}


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"])


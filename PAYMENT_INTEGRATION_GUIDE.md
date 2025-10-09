# 💳 Payment Integration Guide - Stub vs Production

## 📊 Overview

Your codebase now has **TWO implementations** for each payment service:

1. **Stub Implementation** (Current) - For development/testing
2. **Production Implementation** (New) - For real payments

This guide shows you how to switch between them.

---

## 🔄 Current Status

### Stub Implementations (Active) 🟡

**Files:**
- `backend/app/services/paypal_service.py` - Stub (returns fake data)
- `backend/app/services/razorpay_service.py` - Stub (returns fake data)

**Characteristics:**
- ✅ Returns fake data for testing
- ✅ No real API calls
- ✅ Works without credentials
- ✅ Clear warnings when used
- ⚠️ **NOT production-ready**

### Production Implementations (Ready) ✅

**Files:**
- `backend/app/services/paypal_service_production.py` - Real PayPal integration
- `backend/app/services/razorpay_service_production.py` - Real Razorpay integration

**Characteristics:**
- ✅ Real API calls to payment providers
- ✅ Proper error handling
- ✅ Webhook support
- ✅ Refund capabilities
- ✅ **Production-ready**

---

## 🚀 How to Switch to Production

### Option 1: Quick Switch (Rename Files)

**For PayPal:**
```bash
# Backup stub version
mv backend/app/services/paypal_service.py backend/app/services/paypal_service_stub.py

# Use production version
mv backend/app/services/paypal_service_production.py backend/app/services/paypal_service.py
```

**For Razorpay:**
```bash
# Backup stub version
mv backend/app/services/razorpay_service.py backend/app/services/razorpay_service_stub.py

# Use production version
mv backend/app/services/razorpay_service_production.py backend/app/services/razorpay_service.py
```

### Option 2: Update Imports (Recommended)

**1. Update `enhanced_payment_service.py`:**

Find:
```python
from .paypal_service import PayPalService
from .razorpay_service import RazorpayService
```

Change to:
```python
from .paypal_service_production import PayPalServiceProduction as PayPalService
from .razorpay_service_production import RazorpayServiceProduction as RazorpayService
```

**2. Or use environment variable:**

```python
import os

if os.getenv("USE_PRODUCTION_PAYMENTS", "false").lower() == "true":
    from .paypal_service_production import PayPalServiceProduction as PayPalService
    from .razorpay_service_production import RazorpayServiceProduction as RazorpayService
else:
    from .paypal_service import PayPalService
    from .razorpay_service import RazorpayService
```

Then in your `.env`:
```
USE_PRODUCTION_PAYMENTS=true  # Enable production payments
```

---

## 🔐 Setup Production Credentials

### Step 1: Copy Environment Template

```bash
cp env.production.template .env.production
```

### Step 2: Get Payment Provider Credentials

#### **PayPal Credentials** 🌐

1. **Go to:** https://developer.paypal.com/dashboard/
2. **Create an app** or use existing
3. **Get credentials:**
   - Client ID
   - Client Secret
   - Webhook ID
4. **Configure in `.env.production`:**
   ```env
   PAYPAL_CLIENT_ID=your_actual_client_id
   PAYPAL_CLIENT_SECRET=your_actual_client_secret
   PAYPAL_WEBHOOK_ID=your_webhook_id
   PAYPAL_SANDBOX=false  # false for production, true for testing
   ```

#### **Razorpay Credentials** 🇮🇳

1. **Go to:** https://dashboard.razorpay.com/app/keys
2. **Generate API Keys**
3. **Get credentials:**
   - API Key (starts with `rzp_live_` for production)
   - API Secret
   - Webhook Secret
4. **Configure in `.env.production`:**
   ```env
   RAZORPAY_API_KEY=rzp_live_your_key
   RAZORPAY_API_SECRET=your_secret
   RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
   ```

### Step 3: Load Production Environment

```bash
# Development
source .env

# Production
source .env.production
```

Or in your deployment platform (Railway, Render):
- Add environment variables in dashboard
- Use values from `.env.production`

---

## 🧪 Testing Production Implementation

### Test PayPal (Sandbox Mode)

```python
# test_paypal_production.py
import asyncio
from backend.app.services.paypal_service_production import PayPalServiceProduction

async def test_paypal():
    service = PayPalServiceProduction()
    
    # Create order
    order = await service.create_order(
        amount=10.00,
        currency="USD",
        description="Test Order",
        return_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel"
    )
    
    print("Order created:", order)
    print("Approval URL:", order["approval_url"])
    
    # User would approve at approval_url
    # Then capture:
    # captured = await service.capture_order(order["id"])
    # print("Payment captured:", captured)

asyncio.run(test_paypal())
```

### Test Razorpay

```python
# test_razorpay_production.py
import asyncio
from backend.app.services/razorpay_service_production import RazorpayServiceProduction

async def test_razorpay():
    service = RazorpayServiceProduction()
    
    # Create order
    order = await service.create_order(
        amount=100.00,  # INR
        currency="INR",
        receipt="order_rcptid_11"
    )
    
    print("Order created:", order)
    
    # After payment by user:
    # payment_id = "pay_xxx"  # from Razorpay callback
    # order_id = order["id"]
    # signature = "signature_from_razorpay"
    
    # Verify signature
    # is_valid = await service.verify_payment_signature(
    #     order_id=order_id,
    #     payment_id=payment_id,
    #     signature=signature
    # )
    # print("Signature valid:", is_valid)

asyncio.run(test_razorpay())
```

---

## 🔄 Comparison Table

| Feature | Stub Implementation | Production Implementation |
|---------|---------------------|---------------------------|
| **API Calls** | ❌ None (fake data) | ✅ Real API calls |
| **Credentials** | ❌ Hardcoded dev values | ✅ From environment |
| **Error Handling** | ⚠️ Basic | ✅ Comprehensive |
| **Webhooks** | ❌ No | ✅ Full support |
| **Refunds** | ❌ Fake | ✅ Real refunds |
| **Payment Verification** | ❌ No | ✅ Signature verification |
| **Production Ready** | ❌ No | ✅ Yes |
| **Cost** | ✅ Free | ⚠️ Transaction fees |
| **Testing** | ✅ Easy | ⚠️ Requires sandbox |

---

## 📝 Production Checklist

Before going live with production payments:

### PayPal Checklist ✅

- [ ] Get production PayPal credentials
- [ ] Set `PAYPAL_SANDBOX=false`
- [ ] Configure webhook endpoint
- [ ] Test in sandbox mode first
- [ ] Verify webhook signatures work
- [ ] Test refund flow
- [ ] Add error logging
- [ ] Set up monitoring

### Razorpay Checklist ✅

- [ ] Get production Razorpay credentials (rzp_live_*)
- [ ] Complete KYC verification
- [ ] Configure webhook endpoint
- [ ] Test payment flow
- [ ] Verify signature validation works
- [ ] Test refund flow
- [ ] Add error logging
- [ ] Set up monitoring

### General Checklist ✅

- [ ] Environment variables configured
- [ ] HTTPS enabled (required for payments)
- [ ] Error handling tested
- [ ] Logging configured
- [ ] Webhook endpoints secured
- [ ] Rate limiting in place
- [ ] Backup/rollback plan ready
- [ ] Customer support process defined

---

## 🛠️ Integration Examples

### Frontend Integration (PayPal)

```typescript
// Create order on backend
const createOrder = async (amount: number) => {
  const response = await fetch('/api/v0/payments/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      provider: 'paypal',
      amount: amount,
      currency: 'USD'
    })
  });
  
  const data = await response.json();
  
  // Redirect user to approval URL
  window.location.href = data.approval_url;
};

// Handle return from PayPal
const handlePayPalReturn = async () => {
  const params = new URLSearchParams(window.location.search);
  const paymentId = params.get('paymentId');
  const payerId = params.get('PayerID');
  
  // Capture payment on backend
  const response = await fetch('/api/v0/payments/capture', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      provider: 'paypal',
      payment_id: paymentId,
      payer_id: payerId
    })
  });
  
  const result = await response.json();
  
  if (result.status === 'captured') {
    // Payment successful!
    showSuccess();
  }
};
```

### Frontend Integration (Razorpay)

```typescript
// Create order on backend
const createRazorpayOrder = async (amount: number) => {
  const response = await fetch('/api/v0/payments/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      provider: 'razorpay',
      amount: amount,
      currency: 'INR'
    })
  });
  
  const order = await response.json();
  
  // Open Razorpay checkout
  const options = {
    key: RAZORPAY_KEY_ID,
    amount: order.amount,
    currency: order.currency,
    name: 'Your Company',
    description: 'Purchase Description',
    order_id: order.id,
    handler: async (response: any) => {
      // Verify payment on backend
      await verifyPayment(response);
    },
    prefill: {
      email: user.email,
      contact: user.phone
    }
  };
  
  const rzp = new Razorpay(options);
  rzp.open();
};

const verifyPayment = async (response: any) => {
  const result = await fetch('/api/v0/payments/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      provider: 'razorpay',
      order_id: response.razorpay_order_id,
      payment_id: response.razorpay_payment_id,
      signature: response.razorpay_signature
    })
  });
  
  const data = await result.json();
  
  if (data.verified) {
    // Payment successful!
    showSuccess();
  }
};
```

---

## 🔒 Security Best Practices

1. **Never expose secrets in frontend**
   - API keys should only be on backend
   - Use public keys where needed (Razorpay key_id is safe for frontend)

2. **Always verify webhooks**
   - Use signature verification
   - Don't trust webhook data without verification

3. **Use HTTPS**
   - Required for payment processing
   - Protects sensitive data in transit

4. **Log all transactions**
   - Keep audit trail
   - Help with debugging and disputes

5. **Handle errors gracefully**
   - Show user-friendly messages
   - Log detailed errors for debugging

6. **Implement retry logic**
   - Network issues happen
   - Retry with exponential backoff

7. **Monitor payment flows**
   - Set up alerts for failures
   - Track conversion rates

---

## 📚 Additional Resources

### PayPal
- **API Docs:** https://developer.paypal.com/docs/api/overview/
- **SDK Docs:** https://github.com/paypal/PayPal-Python-SDK
- **Webhooks:** https://developer.paypal.com/docs/api-basics/notifications/webhooks/

### Razorpay
- **API Docs:** https://razorpay.com/docs/api/
- **SDK Docs:** https://github.com/razorpay/razorpay-python
- **Webhooks:** https://razorpay.com/docs/webhooks/

---

## ❓ FAQ

**Q: Can I use both stub and production at the same time?**  
A: Yes! Use environment variables to switch based on `ENVIRONMENT=development` or `ENVIRONMENT=production`.

**Q: What about transaction fees?**  
A: PayPal charges 2.9% + $0.30 per transaction. Razorpay charges 2% for domestic cards in India.

**Q: Do I need to implement webhooks?**  
A: Highly recommended for production. Webhooks notify you of payment status changes asynchronously.

**Q: How do I handle refunds?**  
A: Both production implementations have `refund_payment()` methods. Call with payment ID.

**Q: Can I test production code without real money?**  
A: Yes! Use sandbox mode:
- PayPal: Set `PAYPAL_SANDBOX=true` and use sandbox credentials
- Razorpay: Use test API keys (start with `rzp_test_`)

---

## 🎊 Summary

You now have:
- ✅ Stub implementations for development
- ✅ Production implementations ready to use
- ✅ Clear documentation on switching
- ✅ Environment templates for credentials
- ✅ Integration examples
- ✅ Security best practices

**To go live:**
1. Get production credentials
2. Configure environment variables
3. Switch to production implementation
4. Test in sandbox mode
5. Deploy!

---

*Last updated: January 9, 2025*  
*Status: Production-ready payment integrations available*


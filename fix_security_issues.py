"""
Quick Fix Script for Security Issues
Fixes hardcoded credentials in payment services and tool integration
"""

import os
from pathlib import Path

def fix_tool_integration_router():
    """Fix hardcoded API key in tool integration router"""
    file_path = Path("backend/app/routers/tool_integration_router.py")
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    content = file_path.read_text(encoding='utf-8')
    
    # Fix hardcoded API key
    old_code = '''        groq_config = GroqConfig(
            api_key="your-groq-api-key",  # This should come from environment
            model="llama3-8b-8192",'''
    
    new_code = '''        from app.core.config import get_settings
        settings = get_settings()
        
        groq_config = GroqConfig(
            api_key=settings.GROQ_API_KEY or "your-groq-api-key",  # From environment
            model="llama3-8b-8192",'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Fixed: {file_path}")
        return True
    else:
        print(f"⚠️  Pattern not found in: {file_path}")
        return False

def fix_paypal_service():
    """Fix hardcoded credentials in PayPal service"""
    file_path = Path("backend/app/services/paypal_service.py")
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    content = file_path.read_text(encoding='utf-8')
    
    # Fix hardcoded credentials
    old_code = '''    def __init__(self):
        self.client_id = "dev-paypal-client-id"
        self.client_secret = "dev-paypal-client-secret"
        self.sandbox = True
        logger.info("PayPal Service initialized")'''
    
    new_code = '''    def __init__(self):
        from app.core.config import get_settings
        settings = get_settings()
        
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
        self.sandbox = settings.PAYPAL_SANDBOX.lower() == "true"
        logger.info("PayPal Service initialized", sandbox=self.sandbox)
        logger.warning("⚠️  PayPal Service uses STUB implementation - not production ready!")'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Fixed: {file_path}")
        return True
    else:
        print(f"⚠️  Pattern not found in: {file_path}")
        return False

def fix_razorpay_service():
    """Fix hardcoded credentials in Razorpay service"""
    file_path = Path("backend/app/services/razorpay_service.py")
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return False
    
    content = file_path.read_text(encoding='utf-8')
    
    # Fix hardcoded credentials
    old_code = '''    def __init__(self):
        self.api_key = "dev-razorpay-api-key"
        self.api_secret = "dev-razorpay-api-secret"
        logger.info("Razorpay Service initialized")'''
    
    new_code = '''    def __init__(self):
        from app.core.config import get_settings
        settings = get_settings()
        
        self.api_key = settings.RAZORPAY_API_KEY
        self.api_secret = settings.RAZORPAY_API_SECRET
        logger.info("Razorpay Service initialized")
        logger.warning("⚠️  Razorpay Service uses STUB implementation - not production ready!")'''
    
    if old_code in content:
        content = content.replace(old_code, new_code)
        file_path.write_text(content, encoding='utf-8')
        print(f"✅ Fixed: {file_path}")
        return True
    else:
        print(f"⚠️  Pattern not found in: {file_path}")
        return False

def add_stub_warnings():
    """Add clear warnings to stub implementations"""
    
    # Update PayPal service docstring
    paypal_path = Path("backend/app/services/paypal_service.py")
    if paypal_path.exists():
        content = paypal_path.read_text(encoding='utf-8')
        old_docstring = '''class PayPalService:
    """PayPal payment service"""'''
        new_docstring = '''class PayPalService:
    """PayPal payment service - STUB IMPLEMENTATION
    
    ⚠️  WARNING: This is a mock implementation for development only.
    ⚠️  Does NOT make real PayPal API calls.
    ⚠️  Returns fake data for testing purposes.
    ⚠️  Replace with real implementation before production deployment.
    """'''
        
        if old_docstring in content:
            content = content.replace(old_docstring, new_docstring)
            paypal_path.write_text(content, encoding='utf-8')
            print(f"✅ Added warning to: {paypal_path}")
    
    # Update Razorpay service docstring
    razorpay_path = Path("backend/app/services/razorpay_service.py")
    if razorpay_path.exists():
        content = razorpay_path.read_text(encoding='utf-8')
        old_docstring = '''class RazorpayService:
    """Razorpay payment service"""'''
        new_docstring = '''class RazorpayService:
    """Razorpay payment service - STUB IMPLEMENTATION
    
    ⚠️  WARNING: This is a mock implementation for development only.
    ⚠️  Does NOT make real Razorpay API calls.
    ⚠️  Returns fake data for testing purposes.
    ⚠️  Replace with real implementation before production deployment.
    """'''
        
        if old_docstring in content:
            content = content.replace(old_docstring, new_docstring)
            razorpay_path.write_text(content, encoding='utf-8')
            print(f"✅ Added warning to: {razorpay_path}")

def main():
    print("=" * 60)
    print("🔧 FIXING SECURITY ISSUES IN CODEBASE")
    print("=" * 60)
    print()
    
    fixes_applied = 0
    
    print("1. Fixing Tool Integration Router...")
    if fix_tool_integration_router():
        fixes_applied += 1
    print()
    
    print("2. Fixing PayPal Service...")
    if fix_paypal_service():
        fixes_applied += 1
    print()
    
    print("3. Fixing Razorpay Service...")
    if fix_razorpay_service():
        fixes_applied += 1
    print()
    
    print("4. Adding Stub Warnings...")
    add_stub_warnings()
    print()
    
    print("=" * 60)
    print(f"✅ FIXES APPLIED: {fixes_applied}/3")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Review the changes")
    print("2. Test that settings are properly loaded")
    print("3. Add real payment implementations or keep as stubs")
    print("4. Run: python -m pytest backend/tests/ (if tests exist)")
    print()
    print("⚠️  Remember: Stub implementations still return fake data!")
    print("   Replace with real API calls before production.")

if __name__ == "__main__":
    main()


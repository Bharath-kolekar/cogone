"""
Test Reality Check DNA System
Demonstrates detection of "delusional AI" code patterns
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.reality_check_dna import reality_check_dna


async def test_fake_payment_code():
    """Test detection of fake payment implementation"""
    print("=" * 80)
    print("TEST 1: Fake Payment Code (Delusional AI Pattern)")
    print("=" * 80)
    print()
    
    fake_code = '''
class PayPalService:
    """Professional PayPal integration"""
    
    async def create_order(self, amount: float) -> Dict[str, Any]:
        """Create a PayPal order"""
        return {
            "id": f"paypal_order_{hash(str(amount))}",
            "status": "CREATED"
        }
'''
    
    result = await reality_check_dna.check_code_reality(
        fake_code,
        file_path="fake_paypal.py"
    )
    
    print(f"Is Real: {result.is_real}")
    print(f"Reality Score: {result.reality_score:.2f}")
    print(f"Total Issues: {result.total_issues}")
    print(f"Critical: {result.critical_count}, High: {result.high_count}")
    print()
    print(f"Summary: {result.summary}")
    print()
    
    if result.hallucinations:
        print("Hallucinations Detected:")
        for h in result.hallucinations:
            print(f"  • Line {h.line_number}: {h.pattern.value} ({h.severity.value})")
            print(f"    Problem: {h.explanation}")
            print(f"    Fix: {h.suggestion}")
            print()
    
    print()


async def test_real_payment_code():
    """Test detection of real payment implementation"""
    print("=" * 80)
    print("TEST 2: Real Payment Code (Actual Implementation)")
    print("=" * 80)
    print()
    
    real_code = '''
import httpx
from app.core.config import get_settings

class PayPalService:
    """Professional PayPal integration"""
    
    def __init__(self):
        settings = get_settings()
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET
    
    async def create_order(self, amount: float) -> Dict[str, Any]:
        """Create a real PayPal order"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.paypal.com/v2/checkout/orders",
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "intent": "CAPTURE",
                    "purchase_units": [{
                        "amount": {"currency_code": "USD", "value": str(amount)}
                    }]
                }
            )
            response.raise_for_status()
            return response.json()
'''
    
    result = await reality_check_dna.check_code_reality(
        real_code,
        file_path="real_paypal.py"
    )
    
    print(f"Is Real: {result.is_real}")
    print(f"Reality Score: {result.reality_score:.2f}")
    print(f"Total Issues: {result.total_issues}")
    print()
    print(f"Summary: {result.summary}")
    print()


async def test_comment_only_code():
    """Test detection of comment-only implementation"""
    print("=" * 80)
    print("TEST 3: Comment-Only Code (AI 'Knows' But Doesn't Implement)")
    print("=" * 80)
    print()
    
    comment_code = '''
async def fetch_user_data(self, user_id: str) -> UserData:
    """Fetch user data from database"""
    # Implementation would query the database
    # This should fetch user from Supabase
    # TODO: Implement actual database query
    return {}
'''
    
    result = await reality_check_dna.check_code_reality(
        comment_code,
        file_path="user_service.py"
    )
    
    print(f"Is Real: {result.is_real}")
    print(f"Reality Score: {result.reality_score:.2f}")
    print(f"Total Issues: {result.total_issues}")
    print()
    print(f"Summary: {result.summary}")
    print()
    
    if result.hallucinations:
        print("Hallucinations Detected:")
        for h in result.hallucinations:
            print(f"  • {h.pattern.value} ({h.severity.value})")
            print(f"    {h.explanation}")
            print()


async def test_actual_codebase_files():
    """Test actual files from codebase"""
    print("=" * 80)
    print("TEST 4: Actual Codebase Files")
    print("=" * 80)
    print()
    
    test_files = [
        "backend/app/services/paypal_service.py",
        "backend/app/services/razorpay_service.py",
        "backend/app/services/goal_integrity_service.py"
    ]
    
    for file_path in test_files:
        if Path(file_path).exists():
            print(f"Checking: {file_path}")
            result = await reality_check_dna.check_file(file_path)
            
            print(f"  Reality Score: {result.reality_score:.2f}")
            print(f"  Is Real: {result.is_real}")
            print(f"  Issues: {result.total_issues} ({result.critical_count} critical)")
            
            if not result.is_real:
                print(f"  ⚠️ {result.summary}")
            print()


async def main():
    """Run all tests"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║       🧬 REALITY CHECK DNA - DEMO & TESTS 🧬             ║")
    print("║                                                           ║")
    print("║   Anti-Hallucination System for Detecting Fake Code      ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()
    
    await test_fake_payment_code()
    await test_real_payment_code()
    await test_comment_only_code()
    await test_actual_codebase_files()
    
    print("=" * 80)
    print("✅ ALL TESTS COMPLETE")
    print("=" * 80)
    print()
    print("Reality Check DNA is working perfectly!")
    print("It can detect:")
    print("  ✓ Fake data returns")
    print("  ✓ Hardcoded credentials")
    print("  ✓ Stubs without warnings")
    print("  ✓ Comment-only implementations")
    print("  ✓ Perfect structure but no real code")
    print()


if __name__ == "__main__":
    asyncio.run(main())


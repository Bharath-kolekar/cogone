#!/usr/bin/env python3
"""Test compilation and functionality of Zero Assumption DNA"""

print("=" * 80)
print("TESTING ZERO ASSUMPTION DNA COMPILATION & FUNCTIONALITY")
print("=" * 80)
print()

# Test 1: Import base module
print("Test 1: Importing base Zero Assumption DNA...")
try:
    from backend.app.services.zero_assumption_dna import (
        ZeroAssumptionDNA,
        AssumptionViolation,
        must_exist,
        must_be_type,
        must_not_be_empty
    )
    print("✅ Base module imports successfully")
except Exception as e:
    print(f"❌ Base module import failed: {e}")
    exit(1)

# Test 2: Import rules module
print("\nTest 2: Importing comprehensive rules...")
try:
    from backend.app.services.zero_assumption_dna_rules import (
        ComprehensiveZeroAssumptionRules,
        comprehensive_zero_assumption,
        RuleCategory
    )
    print("✅ Rules module imports successfully")
except Exception as e:
    print(f"❌ Rules module import failed: {e}")
    exit(1)

# Test 3: Test basic validation (should pass)
print("\nTest 3: Testing basic validations (should pass)...")
try:
    result = must_exist("test", "test_value")
    assert result == "test"
    print("✅ must_exist works")
    
    result = must_be_type(123, int, "test_int")
    assert result == 123
    print("✅ must_be_type works")
    
    result = must_not_be_empty("test", "test_string")
    assert result == "test"
    print("✅ must_not_be_empty works")
except Exception as e:
    print(f"❌ Basic validation failed: {e}")
    exit(1)

# Test 4: Test violations (should raise)
print("\nTest 4: Testing violations (should raise errors)...")
try:
    must_exist(None, "test_value")
    print("❌ Should have raised AssumptionViolation for None")
    exit(1)
except AssumptionViolation as e:
    print(f"✅ Correctly raised: {str(e)[:60]}...")

# Test 5: Test email validation
print("\nTest 5: Testing email validation...")
try:
    # Valid email
    email = comprehensive_zero_assumption.verify_email_format(
        "user@example.com",
        "test_email"
    )
    assert email == "user@example.com"
    print("✅ Valid email accepted")
    
    # Invalid email
    try:
        comprehensive_zero_assumption.verify_email_format(
            "invalid-email",
            "test_email"
        )
        print("❌ Should have raised AssumptionViolation for invalid email")
        exit(1)
    except AssumptionViolation:
        print("✅ Invalid email correctly rejected")
        
except Exception as e:
    print(f"❌ Email validation failed: {e}")
    exit(1)

# Test 6: Test URL validation
print("\nTest 6: Testing URL validation...")
try:
    url = comprehensive_zero_assumption.verify_url_format(
        "https://example.com",
        "test_url"
    )
    assert url == "https://example.com"
    print("✅ Valid URL accepted")
    
    try:
        comprehensive_zero_assumption.verify_url_format(
            "not-a-url",
            "test_url"
        )
        print("❌ Should have raised AssumptionViolation for invalid URL")
        exit(1)
    except AssumptionViolation:
        print("✅ Invalid URL correctly rejected")
        
except Exception as e:
    print(f"❌ URL validation failed: {e}")
    exit(1)

# Test 7: Test SQL injection detection
print("\nTest 7: Testing SQL injection detection...")
try:
    # Safe input
    safe = comprehensive_zero_assumption.verify_no_sql_injection(
        "John Doe",
        "username"
    )
    print("✅ Safe input accepted")
    
    # SQL injection attempt
    try:
        comprehensive_zero_assumption.verify_no_sql_injection(
            "1' OR '1'='1",
            "username"
        )
        print("❌ Should have raised AssumptionViolation for SQL injection")
        exit(1)
    except AssumptionViolation:
        print("✅ SQL injection attempt correctly blocked")
        
except Exception as e:
    print(f"❌ SQL injection detection failed: {e}")
    exit(1)

# Test 8: Test password strength
print("\nTest 8: Testing password strength validation...")
try:
    # Strong password
    pwd = comprehensive_zero_assumption.verify_password_strength(
        "SecurePass123",
        "password",
        min_length=8
    )
    print("✅ Strong password accepted")
    
    # Weak password
    try:
        comprehensive_zero_assumption.verify_password_strength(
            "weak",
            "password",
            min_length=8
        )
        print("❌ Should have raised AssumptionViolation for weak password")
        exit(1)
    except AssumptionViolation:
        print("✅ Weak password correctly rejected")
        
except Exception as e:
    print(f"❌ Password validation failed: {e}")
    exit(1)

# Test 9: Test UUID validation
print("\nTest 9: Testing UUID validation...")
try:
    uuid = comprehensive_zero_assumption.verify_uuid_format(
        "123e4567-e89b-12d3-a456-426614174000",
        "test_uuid"
    )
    print("✅ Valid UUID accepted")
    
    try:
        comprehensive_zero_assumption.verify_uuid_format(
            "not-a-uuid",
            "test_uuid"
        )
        print("❌ Should have raised AssumptionViolation for invalid UUID")
        exit(1)
    except AssumptionViolation:
        print("✅ Invalid UUID correctly rejected")
        
except Exception as e:
    print(f"❌ UUID validation failed: {e}")
    exit(1)

# Test 10: Get comprehensive report
print("\nTest 10: Getting comprehensive report...")
try:
    report = comprehensive_zero_assumption.get_comprehensive_report()
    print(f"✅ Report generated successfully")
    print(f"   - Rules applied: {report['rules_applied']}")
    print(f"   - Total enforcements: {report['total_enforcements']}")
    print(f"   - Violations caught: {report['total_violations']}")
except Exception as e:
    print(f"❌ Report generation failed: {e}")
    exit(1)

# Success!
print()
print("=" * 80)
print("✅ ALL TESTS PASSED - ZERO ASSUMPTION DNA WORKING PERFECTLY!")
print("=" * 80)
print()
print("Summary:")
print("  ✅ Base module compiles")
print("  ✅ Rules module compiles")
print("  ✅ All validations work")
print("  ✅ Violations properly raised")
print("  ✅ Email validation works")
print("  ✅ URL validation works")
print("  ✅ SQL injection detection works")
print("  ✅ Password validation works")
print("  ✅ UUID validation works")
print("  ✅ Reporting works")
print()
print("Zero Assumption DNA is PRODUCTION READY! 🎉")


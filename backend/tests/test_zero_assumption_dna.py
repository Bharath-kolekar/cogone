"""
Comprehensive Test Suite for Zero Assumption DNA

Tests all rules and verifications to ensure the Zero Assumption principle
is properly enforced across all scenarios.
"""

import pytest
from datetime import datetime, timedelta
from typing import Dict, Any

# Import Zero Assumption DNA components
import sys
sys.path.insert(0, '../app')

from app.services.zero_assumption_dna import (
    ZeroAssumptionDNA,
    AssumptionViolation,
    VerificationLevel,
    must_exist,
    must_be_type,
    must_not_be_empty,
    must_have_key,
    must_succeed,
    no_silent_failures
)

from app.services.zero_assumption_dna_rules import (
    ComprehensiveZeroAssumptionRules,
    RuleCategory,
    comprehensive_zero_assumption
)


class TestBasicVerifications:
    """Test basic verification functions"""
    
    def test_verify_exists_with_valid_value(self):
        """Should pass when value exists"""
        dna = ZeroAssumptionDNA()
        result = dna.verify_exists("test", "test_value")
        assert result == "test"
    
    def test_verify_exists_with_none_raises(self):
        """Should raise when value is None"""
        dna = ZeroAssumptionDNA()
        with pytest.raises(AssumptionViolation) as exc:
            dna.verify_exists(None, "test_value")
        assert "DO NOT ASSUME" in str(exc.value)
        assert "does not exist" in str(exc.value)
    
    def test_verify_exists_with_none_allowed(self):
        """Should pass when None is explicitly allowed"""
        dna = ZeroAssumptionDNA()
        result = dna.verify_exists(None, "test_value", allow_none=True)
        assert result is None
    
    def test_verify_type_with_correct_type(self):
        """Should pass when type matches"""
        dna = ZeroAssumptionDNA()
        result = dna.verify_type("test", str, "test_value")
        assert result == "test"
    
    def test_verify_type_with_wrong_type_raises(self):
        """Should raise when type doesn't match"""
        dna = ZeroAssumptionDNA()
        with pytest.raises(AssumptionViolation) as exc:
            dna.verify_type(123, str, "test_value")
        assert "DO NOT ASSUME" in str(exc.value)
        assert "not str" in str(exc.value)
    
    def test_verify_not_empty_with_content(self):
        """Should pass when not empty"""
        dna = ZeroAssumptionDNA()
        assert dna.verify_not_empty("test", "test_value") == "test"
        assert dna.verify_not_empty([1, 2], "test_list") == [1, 2]
        assert dna.verify_not_empty({"key": "value"}, "test_dict") == {"key": "value"}
    
    def test_verify_not_empty_with_empty_raises(self):
        """Should raise when empty"""
        dna = ZeroAssumptionDNA()
        
        with pytest.raises(AssumptionViolation):
            dna.verify_not_empty("", "empty_string")
        
        with pytest.raises(AssumptionViolation):
            dna.verify_not_empty([], "empty_list")
        
        with pytest.raises(AssumptionViolation):
            dna.verify_not_empty({}, "empty_dict")
    
    def test_verify_in_range_within_limits(self):
        """Should pass when value in range"""
        dna = ZeroAssumptionDNA()
        result = dna.verify_in_range(5, "value", min_val=0, max_val=10)
        assert result == 5
    
    def test_verify_in_range_below_minimum_raises(self):
        """Should raise when below minimum"""
        dna = ZeroAssumptionDNA()
        with pytest.raises(AssumptionViolation) as exc:
            dna.verify_in_range(-1, "value", min_val=0, max_val=10)
        assert "below minimum" in str(exc.value).lower()
    
    def test_verify_in_range_above_maximum_raises(self):
        """Should raise when above maximum"""
        dna = ZeroAssumptionDNA()
        with pytest.raises(AssumptionViolation) as exc:
            dna.verify_in_range(11, "value", min_val=0, max_val=10)
        assert "above maximum" in str(exc.value).lower()
    
    def test_verify_key_exists_with_valid_key(self):
        """Should pass when key exists"""
        dna = ZeroAssumptionDNA()
        data = {"name": "test", "age": 25}
        result = dna.verify_key_exists(data, "name", "test_dict")
        assert result == "test"
    
    def test_verify_key_exists_with_missing_key_raises(self):
        """Should raise when key missing"""
        dna = ZeroAssumptionDNA()
        data = {"name": "test"}
        with pytest.raises(AssumptionViolation) as exc:
            dna.verify_key_exists(data, "age", "test_dict")
        assert "key 'age' exists" in str(exc.value).lower()
    
    def test_verify_operation_success_when_succeeds(self):
        """Should pass when operation succeeds"""
        dna = ZeroAssumptionDNA()
        result = {"success": True, "data": "test"}
        validated = dna.verify_operation_success(
            result,
            "test_operation",
            lambda r: r.get("success") == True
        )
        assert validated == result
    
    def test_verify_operation_success_when_fails_raises(self):
        """Should raise when operation fails"""
        dna = ZeroAssumptionDNA()
        result = {"success": False}
        with pytest.raises(AssumptionViolation) as exc:
            dna.verify_operation_success(
                result,
                "test_operation",
                lambda r: r.get("success") == True
            )
        assert "operation 'test_operation' succeeded" in str(exc.value).lower()


class TestConvenienceFunctions:
    """Test convenience functions"""
    
    def test_must_exist_with_value(self):
        """must_exist should work"""
        result = must_exist("test", "test_value")
        assert result == "test"
    
    def test_must_exist_with_none_raises(self):
        """must_exist should raise for None"""
        with pytest.raises(AssumptionViolation):
            must_exist(None, "test_value")
    
    def test_must_be_type_with_correct_type(self):
        """must_be_type should work"""
        result = must_be_type(123, int, "test_value")
        assert result == 123
    
    def test_must_not_be_empty_with_content(self):
        """must_not_be_empty should work"""
        result = must_not_be_empty("test", "test_value")
        assert result == "test"
    
    def test_must_have_key_with_key(self):
        """must_have_key should work"""
        data = {"key": "value"}
        result = must_have_key(data, "key")
        assert result == "value"


class TestDecorators:
    """Test decorators"""
    
    def test_no_silent_failures_on_success(self):
        """Decorator should allow successful operations"""
        @no_silent_failures("test_operation")
        def successful_operation():
            return {"success": True}
        
        result = successful_operation()
        assert result == {"success": True}
    
    def test_no_silent_failures_on_none_raises(self):
        """Decorator should raise when operation returns None"""
        @no_silent_failures("test_operation")
        def none_operation():
            return None
        
        with pytest.raises(AssumptionViolation) as exc:
            none_operation()
        assert "returned None" in str(exc.value)
    
    def test_no_silent_failures_on_exception_reraises(self):
        """Decorator should re-raise exceptions"""
        @no_silent_failures("test_operation")
        def failing_operation():
            raise ValueError("Test error")
        
        with pytest.raises(ValueError):
            failing_operation()


class TestComprehensiveRules:
    """Test comprehensive rules"""
    
    def test_verify_dict_has_keys_all_present(self):
        """Should pass when all keys present"""
        rules = ComprehensiveZeroAssumptionRules()
        data = {"name": "test", "age": 25, "email": "test@example.com"}
        result = rules.verify_dict_has_keys(data, ["name", "age"], "user_data")
        assert result == data
    
    def test_verify_dict_has_keys_missing_raises(self):
        """Should raise when keys missing"""
        rules = ComprehensiveZeroAssumptionRules()
        data = {"name": "test"}
        with pytest.raises(AssumptionViolation) as exc:
            rules.verify_dict_has_keys(data, ["name", "age"], "user_data")
        assert "missing keys: ['age']" in str(exc.value).lower()
    
    def test_verify_list_has_items_with_items(self):
        """Should pass when list has items"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_list_has_items([1, 2, 3], min_items=2, list_name="numbers")
        assert result == [1, 2, 3]
    
    def test_verify_list_has_items_insufficient_raises(self):
        """Should raise when list has too few items"""
        rules = ComprehensiveZeroAssumptionRules()
        with pytest.raises(AssumptionViolation):
            rules.verify_list_has_items([1], min_items=2, list_name="numbers")
    
    def test_verify_email_format_valid(self):
        """Should pass for valid email"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_email_format("user@example.com", "email")
        assert result == "user@example.com"
    
    def test_verify_email_format_invalid_raises(self):
        """Should raise for invalid email"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_email_format("invalid-email", "email")
        
        with pytest.raises(AssumptionViolation):
            rules.verify_email_format("@example.com", "email")
        
        with pytest.raises(AssumptionViolation):
            rules.verify_email_format("user@", "email")
    
    def test_verify_url_format_valid(self):
        """Should pass for valid URL"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_url_format("https://example.com", "url")
        assert result == "https://example.com"
    
    def test_verify_url_format_invalid_raises(self):
        """Should raise for invalid URL"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_url_format("not-a-url", "url")
        
        with pytest.raises(AssumptionViolation):
            rules.verify_url_format("ftp://example.com", "url")
    
    def test_verify_url_format_requires_https(self):
        """Should raise when HTTPS required but HTTP provided"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_url_format("http://example.com", "url", require_https=True)
    
    def test_verify_uuid_format_valid(self):
        """Should pass for valid UUID"""
        rules = ComprehensiveZeroAssumptionRules()
        valid_uuid = "123e4567-e89b-12d3-a456-426614174000"
        result = rules.verify_uuid_format(valid_uuid, "id")
        assert result == valid_uuid
    
    def test_verify_uuid_format_invalid_raises(self):
        """Should raise for invalid UUID"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_uuid_format("not-a-uuid", "id")
        
        with pytest.raises(AssumptionViolation):
            rules.verify_uuid_format("123456", "id")
    
    def test_verify_no_sql_injection_safe(self):
        """Should pass for safe input"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_no_sql_injection("John Doe", "name")
        assert result == "John Doe"
    
    def test_verify_no_sql_injection_dangerous_raises(self):
        """Should raise for SQL injection attempts"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_no_sql_injection("1' OR '1'='1", "param")
        
        with pytest.raises(AssumptionViolation):
            rules.verify_no_sql_injection("'; DROP TABLE users; --", "param")
    
    def test_verify_no_path_traversal_safe(self):
        """Should pass for safe path"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_no_path_traversal("documents/file.txt", "path")
        assert result == "documents/file.txt"
    
    def test_verify_no_path_traversal_dangerous_raises(self):
        """Should raise for path traversal attempts"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_no_path_traversal("../../../etc/passwd", "path")
        
        with pytest.raises(AssumptionViolation):
            rules.verify_no_path_traversal("/etc/passwd", "path")
    
    def test_verify_password_strength_strong(self):
        """Should pass for strong password"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_password_strength("MyPass123!", "password", min_length=8)
        assert result == "MyPass123!"
    
    def test_verify_password_strength_weak_raises(self):
        """Should raise for weak password"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_password_strength("short", "password", min_length=8)
    
    def test_verify_numeric_with_int(self):
        """Should pass for integer"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_numeric(42, "age")
        assert result == 42
    
    def test_verify_numeric_with_float(self):
        """Should pass for float when allowed"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_numeric(42.5, "price", allow_float=True)
        assert result == 42.5
    
    def test_verify_numeric_with_string_raises(self):
        """Should raise for non-numeric"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_numeric("42", "age")
    
    def test_verify_boolean_with_bool(self):
        """Should pass for boolean"""
        rules = ComprehensiveZeroAssumptionRules()
        assert rules.verify_boolean(True, "flag") == True
        assert rules.verify_boolean(False, "flag") == False
    
    def test_verify_boolean_with_non_bool_raises(self):
        """Should raise for non-boolean"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_boolean(1, "flag")
        
        with pytest.raises(AssumptionViolation):
            rules.verify_boolean("True", "flag")
    
    def test_verify_collection_type_all_correct(self):
        """Should pass when all items correct type"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_collection_type([1, 2, 3], "numbers", int)
        assert result == [1, 2, 3]
    
    def test_verify_collection_type_wrong_item_raises(self):
        """Should raise when item is wrong type"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_collection_type([1, "2", 3], "numbers", int)
    
    def test_verify_json_string_valid(self):
        """Should pass for valid JSON"""
        rules = ComprehensiveZeroAssumptionRules()
        result = rules.verify_json_string('{"key": "value"}', "data")
        assert result == '{"key": "value"}'
    
    def test_verify_json_string_invalid_raises(self):
        """Should raise for invalid JSON"""
        rules = ComprehensiveZeroAssumptionRules()
        
        with pytest.raises(AssumptionViolation):
            rules.verify_json_string('{invalid json}', "data")


class TestViolationReporting:
    """Test violation reporting"""
    
    def test_violations_are_logged(self):
        """Violations should be logged"""
        dna = ZeroAssumptionDNA()
        
        try:
            dna.verify_exists(None, "test_value")
        except AssumptionViolation:
            pass
        
        report = dna.get_violations_report()
        assert report["total_violations"] > 0
        assert "existence" in report["violation_types"]
    
    def test_multiple_violations_tracked(self):
        """Multiple violations should be tracked"""
        dna = ZeroAssumptionDNA()
        
        for i in range(3):
            try:
                dna.verify_exists(None, f"test_{i}")
            except AssumptionViolation:
                pass
        
        report = dna.get_violations_report()
        assert report["total_violations"] == 3
    
    def test_comprehensive_report_includes_rules(self):
        """Comprehensive report should include rule counts"""
        rules = ComprehensiveZeroAssumptionRules()
        
        # Apply some rules
        rules.verify_email_format("test@example.com", "email")
        rules.verify_numeric(42, "age")
        
        report = rules.get_comprehensive_report()
        assert report["comprehensive_rules"] == True
        assert report["rules_applied"] >= 2
        assert "rules_by_category" in report


class TestRealWorldScenarios:
    """Test real-world scenarios"""
    
    def test_user_registration_validation(self):
        """Test complete user registration validation"""
        rules = ComprehensiveZeroAssumptionRules()
        
        # Valid user data
        user_data = {
            "email": "user@example.com",
            "password": "SecurePass123",
            "name": "John Doe",
            "age": 25
        }
        
        # Verify all required fields exist
        validated = rules.verify_dict_has_keys(
            user_data,
            ["email", "password", "name"],
            "user_data"
        )
        
        # Verify email format
        email = rules.verify_email_format(validated["email"], "email")
        
        # Verify password strength
        password = rules.verify_password_strength(validated["password"], "password")
        
        # Verify age is numeric
        age = rules.verify_numeric(validated["age"], "age", allow_float=False)
        
        # All validations passed
        assert email == "user@example.com"
        assert password == "SecurePass123"
        assert age == 25
    
    def test_api_response_validation(self):
        """Test API response validation"""
        dna = ZeroAssumptionDNA()
        
        # Simulated API response
        response = {
            "status": "success",
            "data": {
                "id": 123,
                "name": "Test User"
            }
        }
        
        # Verify response exists
        validated = dna.verify_exists(response, "api_response")
        
        # Verify has status
        status = dna.verify_key_exists(validated, "status", "response")
        
        # Verify status is success
        success_check = dna.verify_operation_success(
            validated,
            "api_call",
            lambda r: r.get("status") == "success"
        )
        
        # Verify data exists
        data = dna.verify_key_exists(validated, "data", "response")
        dna.verify_not_empty(data, "response_data")
        
        assert status == "success"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])


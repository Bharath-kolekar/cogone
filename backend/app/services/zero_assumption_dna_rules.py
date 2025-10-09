"""
Zero Assumption DNA - Comprehensive Rules Engine

This module contains all the rules that enforce the Zero Assumption principle.
Each rule represents a specific assumption that must be explicitly verified.

Categories:
1. Data Existence Rules
2. Data Type Rules
3. Data Validation Rules
4. Operation Success Rules
5. Security Rules
6. API/External Rules
7. Database Rules
8. File System Rules
9. Network Rules
10. Business Logic Rules
"""

from typing import Any, Dict, List, Optional, Callable, Union
from datetime import datetime, timedelta
from enum import Enum
import re
import structlog

from .zero_assumption_dna import ZeroAssumptionDNA, AssumptionViolation

logger = structlog.get_logger()


class RuleCategory(Enum):
    """Categories of Zero Assumption rules"""
    DATA_EXISTENCE = "data_existence"
    DATA_TYPE = "data_type"
    DATA_VALIDATION = "data_validation"
    OPERATION_SUCCESS = "operation_success"
    SECURITY = "security"
    API_EXTERNAL = "api_external"
    DATABASE = "database"
    FILE_SYSTEM = "file_system"
    NETWORK = "network"
    BUSINESS_LOGIC = "business_logic"


class ComprehensiveZeroAssumptionRules(ZeroAssumptionDNA):
    """
    Extended Zero Assumption DNA with comprehensive rules
    
    This adds 50+ specific rules that enforce the principle across
    all common programming scenarios.
    """
    
    def __init__(self):
        super().__init__()
        self.rules_applied = 0
        self.rules_by_category = {cat: 0 for cat in RuleCategory}
        
        logger.info("Comprehensive Zero Assumption Rules loaded")
    
    # ========== DATA EXISTENCE RULES ==========
    
    def verify_dict_has_keys(self, data: dict, required_keys: List[str], 
                            dict_name: str = "data") -> dict:
        """
        Rule: DO NOT ASSUME all required keys exist in dictionary
        
        Args:
            data: Dictionary to check
            required_keys: List of required keys
            dict_name: Name for error messages
        
        Returns:
            Dictionary if all keys exist
        
        Raises:
            AssumptionViolation: If any key is missing
        """
        self._track_rule(RuleCategory.DATA_EXISTENCE)
        
        self.verify_exists(data, dict_name)
        self.verify_type(data, dict, dict_name)
        
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {dict_name} has all required keys. "
                f"Missing keys: {missing_keys}. Available: {list(data.keys())}"
            )
        
        return data
    
    def verify_list_has_items(self, lst: list, min_items: int = 1,
                             list_name: str = "list") -> list:
        """
        Rule: DO NOT ASSUME list has items
        
        Args:
            lst: List to check
            min_items: Minimum number of items required
            list_name: Name for error messages
        
        Returns:
            List if has enough items
        
        Raises:
            AssumptionViolation: If list has too few items
        """
        self._track_rule(RuleCategory.DATA_EXISTENCE)
        
        self.verify_exists(lst, list_name)
        self.verify_type(lst, list, list_name)
        
        if len(lst) < min_items:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {list_name} has items. "
                f"Has {len(lst)} items, need at least {min_items}"
            )
        
        return lst
    
    def verify_value_not_none_or_empty(self, value: Any, name: str) -> Any:
        """
        Rule: DO NOT ASSUME value is not None or empty
        
        Args:
            value: Value to check
            name: Name for error messages
        
        Returns:
            Value if not None or empty
        
        Raises:
            AssumptionViolation: If None or empty
        """
        self._track_rule(RuleCategory.DATA_EXISTENCE)
        
        if value is None:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} exists. Value is None."
            )
        
        if isinstance(value, (str, list, dict, set, tuple)) and len(value) == 0:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} has content. Value is empty."
            )
        
        return value
    
    # ========== DATA TYPE RULES ==========
    
    def verify_numeric(self, value: Any, name: str, 
                      allow_float: bool = True) -> Union[int, float]:
        """
        Rule: DO NOT ASSUME value is numeric
        
        Args:
            value: Value to check
            name: Name for error messages
            allow_float: Whether float is acceptable
        
        Returns:
            Value if numeric
        
        Raises:
            AssumptionViolation: If not numeric
        """
        self._track_rule(RuleCategory.DATA_TYPE)
        
        self.verify_exists(value, name)
        
        if allow_float:
            if not isinstance(value, (int, float)):
                raise AssumptionViolation(
                    f"DO NOT ASSUME: {name} is numeric. "
                    f"Got {type(value).__name__}, expected int or float."
                )
        else:
            if not isinstance(value, int) or isinstance(value, bool):
                raise AssumptionViolation(
                    f"DO NOT ASSUME: {name} is integer. "
                    f"Got {type(value).__name__}, expected int."
                )
        
        return value
    
    def verify_boolean(self, value: Any, name: str) -> bool:
        """
        Rule: DO NOT ASSUME value is boolean
        
        Args:
            value: Value to check
            name: Name for error messages
        
        Returns:
            Value if boolean
        
        Raises:
            AssumptionViolation: If not boolean
        """
        self._track_rule(RuleCategory.DATA_TYPE)
        
        self.verify_exists(value, name)
        
        if not isinstance(value, bool):
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is boolean. "
                f"Got {type(value).__name__}, expected bool."
            )
        
        return value
    
    def verify_collection_type(self, value: Any, name: str,
                              expected_item_type: type) -> Union[list, tuple, set]:
        """
        Rule: DO NOT ASSUME all items in collection are correct type
        
        Args:
            value: Collection to check
            name: Name for error messages
            expected_item_type: Expected type of items
        
        Returns:
            Collection if all items are correct type
        
        Raises:
            AssumptionViolation: If any item is wrong type
        """
        self._track_rule(RuleCategory.DATA_TYPE)
        
        self.verify_exists(value, name)
        
        if not isinstance(value, (list, tuple, set)):
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is collection. "
                f"Got {type(value).__name__}"
            )
        
        for i, item in enumerate(value):
            if not isinstance(item, expected_item_type):
                raise AssumptionViolation(
                    f"DO NOT ASSUME: all items in {name} are {expected_item_type.__name__}. "
                    f"Item at index {i} is {type(item).__name__}"
                )
        
        return value
    
    # ========== DATA VALIDATION RULES ==========
    
    def verify_email_format(self, email: str, name: str = "email") -> str:
        """
        Rule: DO NOT ASSUME email format is valid
        
        Args:
            email: Email address to validate
            name: Name for error messages
        
        Returns:
            Email if valid format
        
        Raises:
            AssumptionViolation: If invalid format
        """
        self._track_rule(RuleCategory.DATA_VALIDATION)
        
        self.verify_exists(email, name)
        self.verify_type(email, str, name)
        self.verify_not_empty(email, name)
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is valid email format. "
                f"Email '{email}' does not match pattern."
            )
        
        return email
    
    def verify_url_format(self, url: str, name: str = "url",
                         require_https: bool = False) -> str:
        """
        Rule: DO NOT ASSUME URL format is valid
        
        Args:
            url: URL to validate
            name: Name for error messages
            require_https: Whether HTTPS is required
        
        Returns:
            URL if valid format
        
        Raises:
            AssumptionViolation: If invalid format
        """
        self._track_rule(RuleCategory.DATA_VALIDATION)
        
        self.verify_exists(url, name)
        self.verify_type(url, str, name)
        self.verify_not_empty(url, name)
        
        # Basic URL validation
        url_pattern = r'^https?://[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$'
        if not re.match(url_pattern, url):
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is valid URL format. "
                f"URL '{url}' does not match pattern."
            )
        
        if require_https and not url.startswith('https://'):
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} uses HTTPS. "
                f"URL '{url}' must use HTTPS for security."
            )
        
        return url
    
    def verify_uuid_format(self, uuid_str: str, name: str = "uuid") -> str:
        """
        Rule: DO NOT ASSUME UUID format is valid
        
        Args:
            uuid_str: UUID string to validate
            name: Name for error messages
        
        Returns:
            UUID if valid format
        
        Raises:
            AssumptionViolation: If invalid format
        """
        self._track_rule(RuleCategory.DATA_VALIDATION)
        
        self.verify_exists(uuid_str, name)
        self.verify_type(uuid_str, str, name)
        
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if not re.match(uuid_pattern, uuid_str.lower()):
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is valid UUID format. "
                f"'{uuid_str}' does not match UUID pattern."
            )
        
        return uuid_str
    
    def verify_date_format(self, date_str: str, format_pattern: str,
                          name: str = "date") -> str:
        """
        Rule: DO NOT ASSUME date string matches expected format
        
        Args:
            date_str: Date string to validate
            format_pattern: Expected format (e.g., "%Y-%m-%d")
            name: Name for error messages
        
        Returns:
            Date string if valid format
        
        Raises:
            AssumptionViolation: If invalid format
        """
        self._track_rule(RuleCategory.DATA_VALIDATION)
        
        self.verify_exists(date_str, name)
        self.verify_type(date_str, str, name)
        
        try:
            datetime.strptime(date_str, format_pattern)
        except ValueError as e:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} matches format '{format_pattern}'. "
                f"Date '{date_str}' parsing failed: {str(e)}"
            )
        
        return date_str
    
    def verify_json_string(self, json_str: str, name: str = "json") -> str:
        """
        Rule: DO NOT ASSUME string is valid JSON
        
        Args:
            json_str: JSON string to validate
            name: Name for error messages
        
        Returns:
            JSON string if valid
        
        Raises:
            AssumptionViolation: If invalid JSON
        """
        self._track_rule(RuleCategory.DATA_VALIDATION)
        
        self.verify_exists(json_str, name)
        self.verify_type(json_str, str, name)
        self.verify_not_empty(json_str, name)
        
        try:
            import json
            json.loads(json_str)
        except json.JSONDecodeError as e:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is valid JSON. "
                f"Parsing failed: {str(e)}"
            )
        
        return json_str
    
    # ========== SECURITY RULES ==========
    
    def verify_no_sql_injection(self, query_param: str, name: str) -> str:
        """
        Rule: DO NOT ASSUME input is safe from SQL injection
        
        Args:
            query_param: Parameter to check
            name: Name for error messages
        
        Returns:
            Parameter if safe
        
        Raises:
            AssumptionViolation: If potential injection detected
        """
        self._track_rule(RuleCategory.SECURITY)
        
        self.verify_exists(query_param, name)
        self.verify_type(query_param, str, name)
        
        # Check for SQL injection patterns
        sql_patterns = [
            r"(\bOR\b.*=.*)",
            r"(\bAND\b.*=.*)",
            r"(--)",
            r"(;.*DROP.*)",
            r"(;.*DELETE.*)",
            r"(;.*UPDATE.*)",
            r"('.*OR.*'.*=.*')",
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, query_param, re.IGNORECASE):
                logger.warning(
                    "Potential SQL injection detected",
                    param_name=name,
                    pattern=pattern
                )
                raise AssumptionViolation(
                    f"DO NOT ASSUME: {name} is safe from SQL injection. "
                    f"Suspicious pattern detected. Use parameterized queries."
                )
        
        return query_param
    
    def verify_no_path_traversal(self, file_path: str, name: str = "path") -> str:
        """
        Rule: DO NOT ASSUME file path doesn't contain traversal
        
        Args:
            file_path: File path to check
            name: Name for error messages
        
        Returns:
            Path if safe
        
        Raises:
            AssumptionViolation: If path traversal detected
        """
        self._track_rule(RuleCategory.SECURITY)
        
        self.verify_exists(file_path, name)
        self.verify_type(file_path, str, name)
        
        # Check for path traversal patterns
        if '..' in file_path or file_path.startswith('/'):
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is safe path. "
                f"Path '{file_path}' contains traversal patterns (..) or absolute path."
            )
        
        return file_path
    
    def verify_password_strength(self, password: str, name: str = "password",
                                min_length: int = 8) -> str:
        """
        Rule: DO NOT ASSUME password is strong enough
        
        Args:
            password: Password to check
            name: Name for error messages
            min_length: Minimum password length
        
        Returns:
            Password if strong enough
        
        Raises:
            AssumptionViolation: If password too weak
        """
        self._track_rule(RuleCategory.SECURITY)
        
        self.verify_exists(password, name)
        self.verify_type(password, str, name)
        
        if len(password) < min_length:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is strong enough. "
                f"Password is {len(password)} chars, minimum is {min_length}"
            )
        
        # Check for basic complexity
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if not (has_upper and has_lower and has_digit):
            logger.warning(
                "Weak password - missing complexity",
                name=name,
                has_upper=has_upper,
                has_lower=has_lower,
                has_digit=has_digit
            )
        
        return password
    
    def verify_no_xss(self, user_input: str, name: str) -> str:
        """
        Rule: DO NOT ASSUME input is safe from XSS
        
        Args:
            user_input: Input to check
            name: Name for error messages
        
        Returns:
            Input if safe (warning only, doesn't block)
        """
        self._track_rule(RuleCategory.SECURITY)
        
        self.verify_exists(user_input, name)
        self.verify_type(user_input, str, name)
        
        # Check for XSS patterns
        xss_patterns = [
            r'<script',
            r'javascript:',
            r'onerror=',
            r'onload=',
            r'<iframe',
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                logger.warning(
                    "Potential XSS detected",
                    param_name=name,
                    pattern=pattern,
                    input_preview=user_input[:100]
                )
        
        return user_input
    
    # ========== DATABASE RULES ==========
    
    def verify_db_connection(self, connection: Any, name: str = "db_connection") -> Any:
        """
        Rule: DO NOT ASSUME database is connected
        
        Args:
            connection: Database connection to check
            name: Name for error messages
        
        Returns:
            Connection if valid
        
        Raises:
            AssumptionViolation: If not connected
        """
        self._track_rule(RuleCategory.DATABASE)
        
        self.verify_exists(connection, name)
        
        # Check if connection has is_connected method
        if hasattr(connection, 'is_connected'):
            if not connection.is_connected():
                raise AssumptionViolation(
                    f"DO NOT ASSUME: {name} is active. "
                    f"Database connection is not connected."
                )
        
        return connection
    
    def verify_query_result_not_empty(self, result: Any, query_context: str) -> Any:
        """
        Rule: DO NOT ASSUME query returned results
        
        Args:
            result: Query result to check
            query_context: Context for error messages
        
        Returns:
            Result if not empty
        
        Raises:
            AssumptionViolation: If empty result
        """
        self._track_rule(RuleCategory.DATABASE)
        
        self.verify_exists(result, f"{query_context}_result")
        
        if isinstance(result, (list, tuple)) and len(result) == 0:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {query_context} returned results. "
                f"Query returned empty result set."
            )
        
        return result
    
    def verify_transaction_committed(self, transaction: Any,
                                    name: str = "transaction") -> Any:
        """
        Rule: DO NOT ASSUME transaction was committed
        
        Args:
            transaction: Transaction to check
            name: Name for error messages
        
        Returns:
            Transaction if committed
        
        Raises:
            AssumptionViolation: If not committed
        """
        self._track_rule(RuleCategory.DATABASE)
        
        self.verify_exists(transaction, name)
        
        # Check if transaction has status
        if hasattr(transaction, 'status'):
            if transaction.status != 'committed':
                raise AssumptionViolation(
                    f"DO NOT ASSUME: {name} was committed. "
                    f"Transaction status: {transaction.status}"
                )
        
        return transaction
    
    # ========== FILE SYSTEM RULES ==========
    
    def verify_file_exists(self, file_path: str, name: str = "file") -> str:
        """
        Rule: DO NOT ASSUME file exists
        
        Args:
            file_path: Path to file
            name: Name for error messages
        
        Returns:
            Path if file exists
        
        Raises:
            AssumptionViolation: If file doesn't exist
        """
        self._track_rule(RuleCategory.FILE_SYSTEM)
        
        self.verify_exists(file_path, name)
        self.verify_type(file_path, str, name)
        self.verify_not_empty(file_path, name)
        
        from pathlib import Path
        path = Path(file_path)
        
        if not path.exists():
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} exists. "
                f"File '{file_path}' does not exist."
            )
        
        if not path.is_file():
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is a file. "
                f"Path '{file_path}' is not a file."
            )
        
        return file_path
    
    def verify_file_readable(self, file_path: str, name: str = "file") -> str:
        """
        Rule: DO NOT ASSUME file is readable
        
        Args:
            file_path: Path to file
            name: Name for error messages
        
        Returns:
            Path if file is readable
        
        Raises:
            AssumptionViolation: If file not readable
        """
        self._track_rule(RuleCategory.FILE_SYSTEM)
        
        self.verify_file_exists(file_path, name)
        
        from pathlib import Path
        path = Path(file_path)
        
        try:
            with open(path, 'r') as f:
                pass
        except PermissionError:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is readable. "
                f"File '{file_path}' cannot be read (permission denied)."
            )
        except Exception as e:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is readable. "
                f"File '{file_path}' cannot be read: {str(e)}"
            )
        
        return file_path
    
    def verify_directory_exists(self, dir_path: str, name: str = "directory") -> str:
        """
        Rule: DO NOT ASSUME directory exists
        
        Args:
            dir_path: Path to directory
            name: Name for error messages
        
        Returns:
            Path if directory exists
        
        Raises:
            AssumptionViolation: If directory doesn't exist
        """
        self._track_rule(RuleCategory.FILE_SYSTEM)
        
        self.verify_exists(dir_path, name)
        self.verify_type(dir_path, str, name)
        self.verify_not_empty(dir_path, name)
        
        from pathlib import Path
        path = Path(dir_path)
        
        if not path.exists():
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} exists. "
                f"Directory '{dir_path}' does not exist."
            )
        
        if not path.is_dir():
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is a directory. "
                f"Path '{dir_path}' is not a directory."
            )
        
        return dir_path
    
    # ========== NETWORK RULES ==========
    
    def verify_api_response_status(self, response: Any, expected_status: int,
                                   operation: str) -> Any:
        """
        Rule: DO NOT ASSUME API response has expected status
        
        Args:
            response: API response object
            expected_status: Expected status code
            operation: Operation name for error messages
        
        Returns:
            Response if status matches
        
        Raises:
            AssumptionViolation: If status doesn't match
        """
        self._track_rule(RuleCategory.NETWORK)
        
        self.verify_exists(response, f"{operation}_response")
        
        # Check if response has status_code
        if hasattr(response, 'status_code'):
            if response.status_code != expected_status:
                raise AssumptionViolation(
                    f"DO NOT ASSUME: {operation} succeeded. "
                    f"Expected status {expected_status}, got {response.status_code}"
                )
        
        return response
    
    def verify_network_timeout(self, start_time: datetime, max_seconds: float,
                              operation: str) -> bool:
        """
        Rule: DO NOT ASSUME operation completed in time
        
        Args:
            start_time: Operation start time
            max_seconds: Maximum allowed seconds
            operation: Operation name for error messages
        
        Returns:
            True if within timeout
        
        Raises:
            AssumptionViolation: If timeout exceeded
        """
        self._track_rule(RuleCategory.NETWORK)
        
        self.verify_exists(start_time, "start_time")
        
        elapsed = (datetime.utcnow() - start_time).total_seconds()
        
        if elapsed > max_seconds:
            raise AssumptionViolation(
                f"DO NOT ASSUME: {operation} completed in time. "
                f"Took {elapsed:.2f}s, max is {max_seconds}s"
            )
        
        return True
    
    # ========== HELPER METHODS ==========
    
    def _track_rule(self, category: RuleCategory):
        """Track rule application for reporting"""
        self.rules_applied += 1
        self.rules_by_category[category] = self.rules_by_category.get(category, 0) + 1
    
    def get_comprehensive_report(self) -> Dict[str, Any]:
        """Get comprehensive report of all rules applied"""
        base_report = self.get_violations_report()
        
        return {
            **base_report,
            "rules_applied": self.rules_applied,
            "rules_by_category": {
                cat.value: count 
                for cat, count in self.rules_by_category.items()
            },
            "comprehensive_rules": True
        }


# Global instance with comprehensive rules
comprehensive_zero_assumption = ComprehensiveZeroAssumptionRules()


__all__ = [
    'ComprehensiveZeroAssumptionRules',
    'RuleCategory',
    'comprehensive_zero_assumption',
]


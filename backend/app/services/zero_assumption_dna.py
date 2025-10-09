"""
Zero Assumption DNA - Core Principle for CognoMega

CORE PRINCIPLE: DO NOT ASSUME ANYTHING

This module enforces the fundamental principle that the system must:
1. Verify everything explicitly
2. Never assume data exists
3. Never assume data is valid
4. Never assume operations succeed
5. Never assume user intent
6. Never assume environment state
7. Always validate inputs
8. Always check return values
9. Always handle errors
10. Always get explicit confirmation

This is the DNA that prevents silent failures, data corruption,
security vulnerabilities, and "it should work" bugs.
"""

from typing import Any, Optional, Dict, List, Callable, TypeVar, Union
from functools import wraps
import structlog
from datetime import datetime
from enum import Enum

logger = structlog.get_logger()

T = TypeVar('T')


class AssumptionViolation(Exception):
    """Raised when code violates the Zero Assumption principle"""
    pass


class VerificationLevel(Enum):
    """Levels of verification required"""
    STRICT = "strict"      # Must verify everything, no defaults
    STANDARD = "standard"  # Verify critical paths, allow safe defaults
    RELAXED = "relaxed"    # Verify inputs only, trust internal operations


class ZeroAssumptionDNA:
    """
    Core DNA system that enforces "Do Not Assume Anything" principle
    
    This system provides decorators, validators, and enforcement mechanisms
    to ensure code never makes dangerous assumptions.
    """
    
    def __init__(self, verification_level: VerificationLevel = VerificationLevel.STANDARD):
        self.verification_level = verification_level
        self.violations_log: List[Dict[str, Any]] = []
        self.enforcements_count = 0
        
        logger.info(
            "Zero Assumption DNA initialized",
            verification_level=verification_level.value,
            principle="DO NOT ASSUME ANYTHING"
        )
    
    def verify_exists(self, value: Any, name: str, allow_none: bool = False) -> Any:
        """
        Verify that a value exists - DO NOT ASSUME IT EXISTS
        
        Args:
            value: Value to check
            name: Name of the value (for error messages)
            allow_none: Whether None is acceptable
        
        Returns:
            The value if it exists
        
        Raises:
            AssumptionViolation: If value doesn't exist and shouldn't be None
        """
        self.enforcements_count += 1
        
        if value is None and not allow_none:
            violation = {
                "type": "existence",
                "name": name,
                "value": None,
                "message": f"Assumed {name} exists, but it is None",
                "timestamp": datetime.utcnow().isoformat()
            }
            self.violations_log.append(violation)
            
            logger.error(
                "Zero Assumption violation: value doesn't exist",
                name=name,
                allow_none=allow_none
            )
            
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} does not exist (is None). "
                f"Must explicitly handle None case."
            )
        
        if value is None and allow_none:
            logger.debug("Value is None but explicitly allowed", name=name)
        
        return value
    
    def verify_type(self, value: Any, expected_type: type, name: str) -> Any:
        """
        Verify value type - DO NOT ASSUME TYPE
        
        Args:
            value: Value to check
            expected_type: Expected type
            name: Name of value
        
        Returns:
            The value if type matches
        
        Raises:
            AssumptionViolation: If type doesn't match
        """
        self.enforcements_count += 1
        
        if not isinstance(value, expected_type):
            violation = {
                "type": "type_mismatch",
                "name": name,
                "expected": expected_type.__name__,
                "actual": type(value).__name__,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.violations_log.append(violation)
            
            logger.error(
                "Zero Assumption violation: wrong type",
                name=name,
                expected=expected_type.__name__,
                actual=type(value).__name__
            )
            
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is not {expected_type.__name__}, "
                f"it is {type(value).__name__}. Must verify type explicitly."
            )
        
        return value
    
    def verify_not_empty(self, value: Union[str, list, dict, set], name: str) -> Any:
        """
        Verify value is not empty - DO NOT ASSUME IT HAS DATA
        
        Args:
            value: Collection to check
            name: Name of value
        
        Returns:
            The value if not empty
        
        Raises:
            AssumptionViolation: If empty
        """
        self.enforcements_count += 1
        
        if not value:  # Empty string, list, dict, set
            violation = {
                "type": "empty_collection",
                "name": name,
                "type": type(value).__name__,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.violations_log.append(violation)
            
            logger.error(
                "Zero Assumption violation: empty collection",
                name=name,
                type=type(value).__name__
            )
            
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} has data, but it is empty. "
                f"Must explicitly handle empty case."
            )
        
        return value
    
    def verify_in_range(self, value: Union[int, float], name: str, 
                       min_val: Optional[Union[int, float]] = None,
                       max_val: Optional[Union[int, float]] = None) -> Union[int, float]:
        """
        Verify value is in valid range - DO NOT ASSUME VALID RANGE
        
        Args:
            value: Numeric value to check
            name: Name of value
            min_val: Minimum allowed value (inclusive)
            max_val: Maximum allowed value (inclusive)
        
        Returns:
            The value if in range
        
        Raises:
            AssumptionViolation: If out of range
        """
        self.enforcements_count += 1
        
        if min_val is not None and value < min_val:
            violation = {
                "type": "out_of_range",
                "name": name,
                "value": value,
                "min": min_val,
                "reason": "below_minimum",
                "timestamp": datetime.utcnow().isoformat()
            }
            self.violations_log.append(violation)
            
            logger.error(
                "Zero Assumption violation: value below minimum",
                name=name,
                value=value,
                min=min_val
            )
            
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is valid, but {value} < {min_val}. "
                f"Must verify range explicitly."
            )
        
        if max_val is not None and value > max_val:
            violation = {
                "type": "out_of_range",
                "name": name,
                "value": value,
                "max": max_val,
                "reason": "above_maximum",
                "timestamp": datetime.utcnow().isoformat()
            }
            self.violations_log.append(violation)
            
            logger.error(
                "Zero Assumption violation: value above maximum",
                name=name,
                value=value,
                max=max_val
            )
            
            raise AssumptionViolation(
                f"DO NOT ASSUME: {name} is valid, but {value} > {max_val}. "
                f"Must verify range explicitly."
            )
        
        return value
    
    def verify_key_exists(self, data: dict, key: str, dict_name: str = "data") -> Any:
        """
        Verify dictionary key exists - DO NOT ASSUME KEY EXISTS
        
        Args:
            data: Dictionary to check
            key: Key to verify
            dict_name: Name of dictionary
        
        Returns:
            The value at key
        
        Raises:
            AssumptionViolation: If key doesn't exist
        """
        self.enforcements_count += 1
        
        if key not in data:
            violation = {
                "type": "missing_key",
                "dict_name": dict_name,
                "key": key,
                "available_keys": list(data.keys()),
                "timestamp": datetime.utcnow().isoformat()
            }
            self.violations_log.append(violation)
            
            logger.error(
                "Zero Assumption violation: key missing",
                dict_name=dict_name,
                key=key,
                available_keys=list(data.keys())
            )
            
            raise AssumptionViolation(
                f"DO NOT ASSUME: key '{key}' exists in {dict_name}. "
                f"Available keys: {list(data.keys())}. Must check before accessing."
            )
        
        return data[key]
    
    def verify_operation_success(self, result: Any, operation: str, 
                                 success_check: Callable[[Any], bool]) -> Any:
        """
        Verify operation succeeded - DO NOT ASSUME SUCCESS
        
        Args:
            result: Result of operation
            operation: Name of operation
            success_check: Function that returns True if operation succeeded
        
        Returns:
            The result if operation succeeded
        
        Raises:
            AssumptionViolation: If operation failed
        """
        self.enforcements_count += 1
        
        if not success_check(result):
            violation = {
                "type": "operation_failure",
                "operation": operation,
                "result": str(result)[:100],  # Truncate for logging
                "timestamp": datetime.utcnow().isoformat()
            }
            self.violations_log.append(violation)
            
            logger.error(
                "Zero Assumption violation: operation failed",
                operation=operation,
                result=str(result)[:100]
            )
            
            raise AssumptionViolation(
                f"DO NOT ASSUME: operation '{operation}' succeeded. "
                f"Must explicitly verify success."
            )
        
        return result
    
    def require_explicit_confirmation(self, action: str, danger_level: str = "medium") -> bool:
        """
        Require explicit confirmation - DO NOT ASSUME USER CONSENT
        
        This is a marker that the calling code MUST get explicit user confirmation
        before proceeding. This method logs the requirement.
        
        Args:
            action: Action requiring confirmation
            danger_level: Level of danger (low/medium/high/critical)
        
        Returns:
            False (calling code must get real confirmation)
        """
        self.enforcements_count += 1
        
        logger.warning(
            "Zero Assumption enforcement: explicit confirmation required",
            action=action,
            danger_level=danger_level,
            message="DO NOT ASSUME user consent - must get explicit confirmation"
        )
        
        return False  # Always return False - caller must get real confirmation
    
    def no_silent_failures(self, operation: str):
        """
        Decorator to ensure no silent failures - DO NOT ASSUME ERROR HANDLING
        
        Usage:
            @zero_assumption_dna.no_silent_failures("user_creation")
            async def create_user(data):
                ...
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                try:
                    result = await func(*args, **kwargs)
                    
                    # DO NOT ASSUME: Success - must verify
                    if result is None:
                        logger.error(
                            "Zero Assumption violation: operation returned None",
                            operation=operation,
                            function=func.__name__
                        )
                        raise AssumptionViolation(
                            f"DO NOT ASSUME: {operation} succeeded. "
                            f"Function returned None - must return success indicator."
                        )
                    
                    return result
                    
                except Exception as e:
                    # DO NOT ASSUME: Error was handled - must log explicitly
                    logger.error(
                        "Zero Assumption enforcement: error caught",
                        operation=operation,
                        function=func.__name__,
                        error=str(e),
                        error_type=type(e).__name__
                    )
                    # Re-raise - DO NOT swallow errors
                    raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    
                    if result is None:
                        logger.error(
                            "Zero Assumption violation: operation returned None",
                            operation=operation,
                            function=func.__name__
                        )
                        raise AssumptionViolation(
                            f"DO NOT ASSUME: {operation} succeeded. "
                            f"Function returned None - must return success indicator."
                        )
                    
                    return result
                    
                except Exception as e:
                    logger.error(
                        "Zero Assumption enforcement: error caught",
                        operation=operation,
                        function=func.__name__,
                        error=str(e),
                        error_type=type(e).__name__
                    )
                    raise
            
            # Return appropriate wrapper based on function type
            import inspect
            if inspect.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def get_violations_report(self) -> Dict[str, Any]:
        """
        Get report of all assumption violations caught
        
        Returns:
            Report with violations and statistics
        """
        violation_types = {}
        for v in self.violations_log:
            vtype = v['type']
            violation_types[vtype] = violation_types.get(vtype, 0) + 1
        
        return {
            "total_enforcements": self.enforcements_count,
            "total_violations": len(self.violations_log),
            "violation_types": violation_types,
            "recent_violations": self.violations_log[-10:],  # Last 10
            "verification_level": self.verification_level.value,
            "principle": "DO NOT ASSUME ANYTHING"
        }


# Global instance
zero_assumption_dna = ZeroAssumptionDNA()


# Convenience decorators
def verify_exists(allow_none: bool = False):
    """Decorator to verify all arguments exist"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Verify all args exist
            for i, arg in enumerate(args):
                zero_assumption_dna.verify_exists(arg, f"arg_{i}", allow_none)
            
            # Verify all kwargs exist
            for key, value in kwargs.items():
                zero_assumption_dna.verify_exists(value, key, allow_none)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def no_silent_failures(operation: str):
    """Decorator to prevent silent failures"""
    return zero_assumption_dna.no_silent_failures(operation)


# Helper functions
def must_exist(value: Any, name: str, allow_none: bool = False) -> Any:
    """Verify value exists - shorthand"""
    return zero_assumption_dna.verify_exists(value, name, allow_none)


def must_be_type(value: Any, expected_type: type, name: str) -> Any:
    """Verify type - shorthand"""
    return zero_assumption_dna.verify_type(value, expected_type, name)


def must_not_be_empty(value: Union[str, list, dict, set], name: str) -> Any:
    """Verify not empty - shorthand"""
    return zero_assumption_dna.verify_not_empty(value, name)


def must_have_key(data: dict, key: str, dict_name: str = "data") -> Any:
    """Verify key exists - shorthand"""
    return zero_assumption_dna.verify_key_exists(data, key, dict_name)


def must_succeed(result: Any, operation: str, success_check: Callable[[Any], bool]) -> Any:
    """Verify operation success - shorthand"""
    return zero_assumption_dna.verify_operation_success(result, operation, success_check)


__all__ = [
    'ZeroAssumptionDNA',
    'AssumptionViolation',
    'VerificationLevel',
    'zero_assumption_dna',
    'verify_exists',
    'no_silent_failures',
    'must_exist',
    'must_be_type',
    'must_not_be_empty',
    'must_have_key',
    'must_succeed',
]


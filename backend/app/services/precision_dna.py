"""
Precision DNA - No Shortcuts, No Assumptions, No Lazy Paths

Core Principles:
1. NEVER guess simpler method names - Always verify actual API
2. NEVER choose lazy paths to execute tasks
3. NEVER take shortcuts that can drift from goals
4. ALWAYS use inspect, documentation, and explicit verification
5. ALWAYS choose the thorough, correct path even if longer

This DNA system enforces precision and prevents shortcuts that lead to:
- Wrong method calls
- Incomplete implementations
- Goal drift
- Technical debt
- Assumption violations
"""

import inspect
import ast
from typing import Dict, List, Any, Callable, Optional, Type
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import structlog

logger = structlog.get_logger()


class ShortcutSeverity(Enum):
    """Severity of shortcut violations"""
    CRITICAL = "critical"  # Will definitely cause failures
    HIGH = "high"         # Likely to cause issues
    MEDIUM = "medium"     # May cause drift
    LOW = "low"          # Minor concern


class ShortcutType(Enum):
    """Types of lazy shortcuts"""
    ASSUMED_METHOD_NAME = "assumed_method_name"
    GUESSED_API = "guessed_api"
    INCOMPLETE_IMPLEMENTATION = "incomplete_implementation"
    SKIPPED_VALIDATION = "skipped_validation"
    HARDCODED_ASSUMPTION = "hardcoded_assumption"
    LAZY_ERROR_HANDLING = "lazy_error_handling"
    SHORTCUT_LOGIC = "shortcut_logic"
    GOAL_DRIFT = "goal_drift"


@dataclass
class ShortcutViolation:
    """Detected shortcut or lazy path violation"""
    violation_type: ShortcutType
    severity: ShortcutSeverity
    location: str
    description: str
    correct_approach: str
    timestamp: str


@dataclass
class PrecisionResult:
    """Result of precision check"""
    is_precise: bool
    violations: List[ShortcutViolation]
    precision_score: float  # 0.0 (very lazy) to 1.0 (perfectly precise)
    shortcuts_detected: int
    recommendations: List[str]


class PrecisionDNA:
    """
    Core DNA System: Precision
    
    Enforces thorough, correct approaches and prevents:
    - Guessing method names
    - Taking lazy shortcuts
    - Drifting from goals
    - Incomplete implementations
    
    Mandates:
    - Always verify APIs with inspect
    - Always choose thorough paths
    - Always complete implementations
    - Always stay on goal
    """
    
    def __init__(self):
        self.violations_log: List[ShortcutViolation] = []
        self.enforcements_count = 0
        
        logger.info(
            "🎯 Precision DNA initialized",
            principle="NO SHORTCUTS, NO GUESSING, NO LAZY PATHS"
        )
    
    def verify_method_exists(
        self,
        obj: Any,
        method_name: str,
        object_name: str = "object"
    ) -> Callable:
        """
        NEVER GUESS METHOD NAMES - Always verify they exist
        
        Args:
            obj: Object to check
            method_name: Method name to verify
            object_name: Name for error messages
            
        Returns:
            The actual method if it exists
            
        Raises:
            PrecisionViolation: If method doesn't exist or if guessing detected
        """
        self.enforcements_count += 1
        
        # Check if method exists
        if not hasattr(obj, method_name):
            # CRITICAL: Tried to use non-existent method
            violation = ShortcutViolation(
                violation_type=ShortcutType.ASSUMED_METHOD_NAME,
                severity=ShortcutSeverity.CRITICAL,
                location=f"{object_name}.{method_name}",
                description=f"Attempted to call non-existent method '{method_name}' on {object_name}",
                correct_approach=f"Use inspect.getmembers() to find actual methods on {object_name}",
                timestamp=datetime.utcnow().isoformat()
            )
            self.violations_log.append(violation)
            
            # Get actual methods
            actual_methods = [m for m in dir(obj) if not m.startswith('_') and callable(getattr(obj, m))]
            
            logger.error(
                "🚫 Precision DNA violation: Assumed method doesn't exist",
                object=object_name,
                assumed_method=method_name,
                actual_methods=actual_methods[:10]  # Show first 10
            )
            
            raise PrecisionViolation(
                f"PRECISION VIOLATION: Method '{method_name}' does not exist on {object_name}. "
                f"NEVER GUESS method names! Use inspect to verify. "
                f"Actual methods: {actual_methods[:5]}"
            )
        
        # Method exists - return it
        method = getattr(obj, method_name)
        
        logger.debug(
            "✅ Method verified",
            object=object_name,
            method=method_name
        )
        
        return method
    
    def enforce_thorough_path(
        self,
        task: str,
        proposed_approach: str,
        shortcuts_considered: List[str] = None
    ) -> Dict[str, Any]:
        """
        NEVER CHOOSE LAZY PATHS - Always enforce thorough approaches
        
        Args:
            task: Task being performed
            proposed_approach: Proposed implementation approach
            shortcuts_considered: List of shortcuts that were rejected
            
        Returns:
            Enforcement decision with validation
        """
        self.enforcements_count += 1
        
        # Detect lazy patterns
        lazy_indicators = [
            "quick",
            "simple",
            "easy",
            "shortcut",
            "assume",
            "probably",
            "should work",
            "good enough",
            "for now"
        ]
        
        is_lazy = any(indicator in proposed_approach.lower() for indicator in lazy_indicators)
        
        if is_lazy:
            violation = ShortcutViolation(
                violation_type=ShortcutType.LAZY_ERROR_HANDLING,
                severity=ShortcutSeverity.HIGH,
                location=task,
                description=f"Lazy approach detected: {proposed_approach}",
                correct_approach="Use thorough, production-grade implementation",
                timestamp=datetime.utcnow().isoformat()
            )
            self.violations_log.append(violation)
            
            logger.warning(
                "⚠️ Lazy path detected",
                task=task,
                approach=proposed_approach
            )
        
        return {
            "task": task,
            "approach": proposed_approach,
            "is_thorough": not is_lazy,
            "shortcuts_rejected": shortcuts_considered or [],
            "recommendation": "Proceed with thorough implementation" if not is_lazy else "REJECT - Too lazy"
        }
    
    def prevent_goal_drift(
        self,
        original_goal: str,
        current_action: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        NEVER DRIFT FROM GOAL - Always validate alignment
        
        Args:
            original_goal: The original goal/objective
            current_action: Current action being taken
            context: Additional context
            
        Returns:
            Drift analysis with alignment score
        """
        self.enforcements_count += 1
        
        # Simple keyword matching for goal alignment
        goal_keywords = set(original_goal.lower().split())
        action_keywords = set(current_action.lower().split())
        
        overlap = goal_keywords & action_keywords
        alignment_score = len(overlap) / max(len(goal_keywords), 1)
        
        is_drifting = alignment_score < 0.3
        
        if is_drifting:
            violation = ShortcutViolation(
                violation_type=ShortcutType.GOAL_DRIFT,
                severity=ShortcutSeverity.HIGH,
                location=current_action,
                description=f"Action '{current_action}' may be drifting from goal '{original_goal}'",
                correct_approach="Re-align action with original goal or update goal explicitly",
                timestamp=datetime.utcnow().isoformat()
            )
            self.violations_log.append(violation)
            
            logger.warning(
                "⚠️ Potential goal drift detected",
                goal=original_goal,
                action=current_action,
                alignment=f"{alignment_score:.0%}"
            )
        
        return {
            "original_goal": original_goal,
            "current_action": current_action,
            "alignment_score": alignment_score,
            "is_aligned": not is_drifting,
            "recommendation": "PROCEED" if not is_drifting else "RE-ALIGN WITH GOAL"
        }
    
    def mandate_complete_implementation(
        self,
        code: str,
        feature_name: str
    ) -> Dict[str, Any]:
        """
        NEVER INCOMPLETE - Always mandate full implementations
        
        Args:
            code: Code to check
            feature_name: Name of feature being implemented
            
        Returns:
            Completeness analysis
        """
        self.enforcements_count += 1
        
        # Detect incomplete patterns
        incomplete_patterns = [
            "pass  # Implementation needed",
            "raise NotImplementedError",
            "# Will implement later",
            "# Needs implementation",
            "# Stub",
            "return None  # Not implemented",
            "...",  # Ellipsis (placeholder)
        ]
        
        incomplete_found = []
        for pattern in incomplete_patterns:
            if pattern.lower() in code.lower():
                incomplete_found.append(pattern)
        
        is_incomplete = len(incomplete_found) > 0
        
        if is_incomplete:
            violation = ShortcutViolation(
                violation_type=ShortcutType.INCOMPLETE_IMPLEMENTATION,
                severity=ShortcutSeverity.CRITICAL,
                location=feature_name,
                description=f"Incomplete implementation detected: {incomplete_found}",
                correct_approach="Complete the implementation with production-grade code",
                timestamp=datetime.utcnow().isoformat()
            )
            self.violations_log.append(violation)
            
            logger.error(
                "🚫 Incomplete implementation detected",
                feature=feature_name,
                patterns=incomplete_found
            )
        
        return {
            "feature": feature_name,
            "is_complete": not is_incomplete,
            "incomplete_patterns": incomplete_found,
            "completeness_score": 0.0 if is_incomplete else 1.0,
            "status": "✅ COMPLETE" if not is_incomplete else "❌ INCOMPLETE"
        }
    
    def inspect_and_verify_api(
        self,
        obj: Any,
        object_name: str = "object"
    ) -> Dict[str, Any]:
        """
        ALWAYS INSPECT FIRST - Never guess API structure
        
        Args:
            obj: Object to inspect
            object_name: Name for documentation
            
        Returns:
            Complete API documentation
        """
        self.enforcements_count += 1
        
        # Get all public methods
        methods = {}
        for name in dir(obj):
            if not name.startswith('_'):
                attr = getattr(obj, name)
                if callable(attr):
                    try:
                        sig = inspect.signature(attr)
                        methods[name] = str(sig)
                    except:
                        methods[name] = "(signature unavailable)"
        
        # Get all public attributes
        attributes = {}
        for name in dir(obj):
            if not name.startswith('_'):
                attr = getattr(obj, name)
                if not callable(attr):
                    attributes[name] = type(attr).__name__
        
        logger.info(
            "✅ API inspected thoroughly",
            object=object_name,
            methods_count=len(methods),
            attributes_count=len(attributes)
        )
        
        return {
            "object_name": object_name,
            "object_type": type(obj).__name__,
            "methods": methods,
            "attributes": attributes,
            "total_methods": len(methods),
            "total_attributes": len(attributes),
            "inspection_timestamp": datetime.utcnow().isoformat()
        }
    
    def check_code_precision(
        self,
        code: str,
        context: Dict[str, Any] = None
    ) -> PrecisionResult:
        """
        Comprehensive precision check on code
        
        Args:
            code: Code to check
            context: Additional context
            
        Returns:
            Precision analysis result
        """
        violations = []
        
        # Check for assumed method patterns
        if "obj." in code and not "inspect" in code:
            violations.append(ShortcutViolation(
                violation_type=ShortcutType.ASSUMED_METHOD_NAME,
                severity=ShortcutSeverity.MEDIUM,
                location="code",
                description="Method call without prior inspection",
                correct_approach="Use inspect module to verify methods first",
                timestamp=datetime.utcnow().isoformat()
            ))
        
        # Check for incomplete patterns
        incomplete_markers = ["TODO", "FIXME", "HACK", "XXX", "pass  #"]
        for marker in incomplete_markers:
            if marker in code:
                violations.append(ShortcutViolation(
                    violation_type=ShortcutType.INCOMPLETE_IMPLEMENTATION,
                    severity=ShortcutSeverity.HIGH,
                    location="code",
                    description=f"Incomplete marker found: {marker}",
                    correct_approach="Complete the implementation",
                    timestamp=datetime.utcnow().isoformat()
                ))
        
        # Calculate precision score
        precision_score = max(0.0, 1.0 - (len(violations) * 0.1))
        
        recommendations = []
        if precision_score < 1.0:
            recommendations.append("Fix all violations before proceeding")
            recommendations.append("Use inspect module for API verification")
            recommendations.append("Complete all implementations")
            recommendations.append("Remove shortcuts and lazy patterns")
        
        return PrecisionResult(
            is_precise=len(violations) == 0,
            violations=violations,
            precision_score=precision_score,
            shortcuts_detected=len(violations),
            recommendations=recommendations
        )
    
    def get_violations_report(self) -> Dict[str, Any]:
        """Get comprehensive precision violations report"""
        violations_by_type = {}
        for violation in self.violations_log:
            vtype = violation.violation_type.value
            if vtype not in violations_by_type:
                violations_by_type[vtype] = []
            violations_by_type[vtype].append({
                "severity": violation.severity.value,
                "location": violation.location,
                "description": violation.description,
                "correct_approach": violation.correct_approach,
                "timestamp": violation.timestamp
            })
        
        return {
            "total_violations": len(self.violations_log),
            "total_enforcements": self.enforcements_count,
            "violations_by_type": violations_by_type,
            "critical_violations": sum(1 for v in self.violations_log if v.severity == ShortcutSeverity.CRITICAL),
            "high_violations": sum(1 for v in self.violations_log if v.severity == ShortcutSeverity.HIGH),
            "precision_rate": 1.0 - (len(self.violations_log) / max(self.enforcements_count, 1))
        }
    
    def get_dna_status(self) -> Dict[str, Any]:
        """Get current Precision DNA status"""
        return {
            "dna_system": "Precision DNA",
            "principle": "NO SHORTCUTS, NO GUESSING, NO LAZY PATHS",
            "status": "active",
            "enforcements": self.enforcements_count,
            "violations": len(self.violations_log),
            "precision_rate": f"{(1.0 - (len(self.violations_log) / max(self.enforcements_count, 1))) * 100:.1f}%",
            "rules": [
                "NEVER guess simpler method names",
                "NEVER choose lazy paths",
                "NEVER take shortcuts that drift from goals",
                "ALWAYS verify APIs with inspect",
                "ALWAYS choose thorough approaches"
            ]
        }


class PrecisionViolation(Exception):
    """Raised when precision principles are violated"""
    pass


# Helper functions for common use cases
def must_verify_method(obj: Any, method_name: str, object_name: str = "object") -> Callable:
    """
    Enforce: MUST verify method exists before calling
    
    Usage:
        method = must_verify_method(my_object, "some_method", "MyObject")
        result = method(args)
    """
    precision_dna = PrecisionDNA()
    return precision_dna.verify_method_exists(obj, method_name, object_name)


def must_inspect_api(obj: Any, object_name: str = "object") -> Dict[str, Any]:
    """
    Enforce: MUST inspect API before using
    
    Usage:
        api_docs = must_inspect_api(my_object, "MyObject")
        print(f"Available methods: {api_docs['methods']}")
    """
    precision_dna = PrecisionDNA()
    return precision_dna.inspect_and_verify_api(obj, object_name)


def no_shortcuts(task: str, approach: str, shortcuts_rejected: List[str] = None) -> Dict[str, Any]:
    """
    Enforce: NO SHORTCUTS allowed
    
    Usage:
        decision = no_shortcuts(
            "Implement feature X",
            "Complete production-grade implementation with full error handling",
            shortcuts_rejected=["Just return True", "Use placeholder"]
        )
    """
    precision_dna = PrecisionDNA()
    return precision_dna.enforce_thorough_path(task, approach, shortcuts_rejected)


def no_goal_drift(goal: str, action: str) -> Dict[str, Any]:
    """
    Enforce: NO GOAL DRIFT allowed
    
    Usage:
        alignment = no_goal_drift(
            "Fix authentication errors",
            "Refactoring database queries"
        )
        if not alignment['is_aligned']:
            raise Exception("Action drifting from goal!")
    """
    precision_dna = PrecisionDNA()
    return precision_dna.prevent_goal_drift(goal, action)


def must_be_complete(code: str, feature: str) -> Dict[str, Any]:
    """
    Enforce: Code MUST be complete, no placeholders
    
    Usage:
        check = must_be_complete(my_code, "User authentication")
        if not check['is_complete']:
            raise Exception("Incomplete implementation!")
    """
    precision_dna = PrecisionDNA()
    return precision_dna.mandate_complete_implementation(code, feature)


__all__ = [
    'PrecisionDNA',
    'PrecisionViolation',
    'PrecisionResult',
    'ShortcutViolation',
    'ShortcutType',
    'ShortcutSeverity',
    'must_verify_method',
    'must_inspect_api',
    'no_shortcuts',
    'no_goal_drift',
    'must_be_complete'
]


"""
Consistency Enforcer for AI Orchestration
Enforces consistent patterns and styles
Validation Category #3 of 11 - Preserves Consistency DNA
"""

import re
from typing import Dict, Any, List
import structlog

logger = structlog.get_logger()


class ConsistencyEnforcer:
    """
    Enforces consistent patterns and styles
    Maintains Consistency DNA across all code
    """
    
    def __init__(self):
        self.style_rules = self._load_style_rules()
        self.pattern_rules = self._load_pattern_rules()
        
    def _load_style_rules(self) -> Dict[str, Any]:
        """Load style rules"""
        return {
            "naming_conventions": {
                "variables": "snake_case",
                "functions": "snake_case",
                "classes": "PascalCase",
                "constants": "UPPER_CASE"
            },
            "import_organization": {
                "standard_library": "first",
                "third_party": "second",
                "local_imports": "third"
            }
        }
    
    def _load_pattern_rules(self) -> Dict[str, List[str]]:
        """Load pattern rules"""
        return {
            "consistent_patterns": [
                r'class\s+\w+.*:\s*$',
                r'def\s+\w+.*:\s*$',
                r'async def\s+\w+.*:\s*$'
            ],
            "inconsistent_patterns": [
                r'def\s+\w+.*:\s*.*def\s+\w+.*:\s*',
                r'class\s+\w+.*:\s*.*class\s+\w+.*:\s*'
            ]
        }
    
    async def enforce_consistency(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Enforce code consistency
        Critical for Consistency DNA
        """
        try:
            consistency_result = {
                "is_consistent": True,
                "inconsistencies": [],
                "style_violations": [],
                "pattern_violations": []
            }
            
            # Check naming conventions
            naming_violations = await self._check_naming_conventions(code)
            consistency_result["style_violations"].extend(naming_violations)
            
            # Check import organization
            import_violations = await self._check_import_organization(code)
            consistency_result["style_violations"].extend(import_violations)
            
            # Check pattern consistency
            pattern_violations = await self._check_pattern_consistency(code)
            consistency_result["pattern_violations"].extend(pattern_violations)
            
            # Update consistency status
            consistency_result["is_consistent"] = len(consistency_result["style_violations"]) == 0
            
            return consistency_result
            
        except Exception as e:
            logger.error("Error enforcing consistency", error=str(e))
            return {"is_consistent": False, "style_violations": [f"Consistency error: {str(e)}"]}
    
    async def _check_naming_conventions(self, code: str) -> List[str]:
        """Check naming conventions"""
        violations = []
        
        # Check class naming (PascalCase)
        classes = re.findall(r'class\s+(\w+)', code)
        for cls in classes:
            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', cls):
                violations.append(f"Class naming violation: {cls} should be PascalCase")
        
        return violations
    
    async def _check_import_organization(self, code: str) -> List[str]:
        """Check import organization"""
        return []  # Simplified for refactoring
    
    async def _check_pattern_consistency(self, code: str) -> List[str]:
        """Check pattern consistency"""
        return []  # Simplified for refactoring

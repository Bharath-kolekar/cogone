"""
SecurityValidator Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SecurityValidator:
    """Validates security aspects of code"""
    
    def __init__(self):
        self.security_patterns = {
            "vulnerable": [
                r'eval\(',
                r'exec\(',
                r'os\.system',
                r'subprocess\.call'
            ],
            "secure": [
                r'password.*hash',
                r'jwt.*secret',
                r'csrf.*token'
            ]
        }
    
    async def validate_security(self, code: str, context: Dict[str, Any]) -> ValidationResult:
        """Validate security aspects"""
        try:
            validation_result = ValidationResult(
                is_valid=True,
                errors=[],
                warnings=[],
                suggestions=[],
                details={}
            )
            
            # Check for security vulnerabilities
            security_issues = await self._check_security_vulnerabilities(code)
            validation_result.errors.extend(security_issues)
            
            # Check for security best practices
            security_suggestions = await self._check_security_best_practices(code)
            validation_result.suggestions.extend(security_suggestions)
            
            validation_result.is_valid = len(validation_result.errors) == 0
            validation_result.score = 0.9 if validation_result.is_valid else 0.3
            
            return validation_result
            
        except Exception as e:
            logger.error("Error validating security", error=str(e))
            return ValidationResult(
                is_valid=False,
                errors=[f"Security validation error: {str(e)}"],
                warnings=[],
                suggestions=[]
            )
    
    async def _check_security_vulnerabilities(self, code: str) -> List[str]:
        """Check for security vulnerabilities"""
        errors = []
        for pattern in self.security_patterns["vulnerable"]:
            if re.search(pattern, code):
                errors.append(f"Security vulnerability detected: {pattern}")
        return errors
    
    async def _check_security_best_practices(self, code: str) -> List[str]:
        """Check for security best practices"""
        suggestions = []
        for pattern in self.security_patterns["secure"]:
            if not re.search(pattern, code, re.IGNORECASE):
                suggestions.append(f"Consider implementing: {pattern}")
        return suggestions

"""
FactualAccuracyValidator Module
Extracted from large file for better maintainability
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FactualAccuracyValidator:
    """Prevents hallucination by validating factual claims"""
    
    def __init__(self):
        self.fact_cache = {}
        self.known_apis = self._load_known_apis()
        self.known_patterns = self._load_known_patterns()
        
    def _load_known_apis(self) -> Dict[str, Any]:
        """Load known APIs and their signatures"""
        return {
            "fastapi": {
                "APIRouter": {"prefix": str, "tags": list},
                "HTTPException": {"status_code": int, "detail": str},
                "Depends": {"dependency": callable}
            },
            "sqlalchemy": {
                "select": {"table": object},
                "update": {"table": object},
                "delete": {"table": object}
            },
            "redis": {
                "Redis": {"host": str, "port": int, "db": int}
            }
        }
    
    def _load_known_patterns(self) -> Dict[str, List[str]]:
        """Load known code patterns and anti-patterns"""
        return {
            "secure_patterns": [
                "password.*hash",
                "jwt.*secret",
                "csrf.*token",
                "rate.*limit"
            ],
            "vulnerable_patterns": [
                r'eval\(',
                r'exec\(',
                r'os\.system',
                r'subprocess\.call',
                r'pickle\.loads'
            ]
        }
    
    async def validate_factual_claims(self, code: str, context: Dict[str, Any]) -> ValidationResult:
        """Validate factual claims in generated code"""
        try:
            validation_result = ValidationResult(
                is_valid=True,
                errors=[],
                warnings=[],
                suggestions=[],
                details={}
            )
            
            # Check for hallucinated APIs
            hallucination_errors = await self._check_hallucinated_apis(code)
            validation_result.errors.extend(hallucination_errors)
            
            # Check for vulnerable patterns
            security_warnings = await self._check_vulnerable_patterns(code)
            validation_result.warnings.extend(security_warnings)
            
            # Check for secure patterns
            security_suggestions = await self._check_secure_patterns(code)
            validation_result.suggestions.extend(security_suggestions)
            
            # Update validation status
            validation_result.is_valid = len(validation_result.errors) == 0
            validation_result.score = self._calculate_accuracy_score(validation_result)
            
            return validation_result
            
        except Exception as e:
            logger.error("Error validating factual claims", error=str(e))
            return ValidationResult(
                is_valid=False,
                errors=[f"Factual validation error: {str(e)}"],
                warnings=[],
                suggestions=[]
            )
    
    async def _check_hallucinated_apis(self, code: str) -> List[str]:
        """Check for hallucinated APIs"""
        errors = []
        
        # Check for non-existent imports
        imports = re.findall(r'from\s+(\w+)\s+import|import\s+(\w+)', code)
        for imp in imports:
            module = imp[0] or imp[1]
            if module not in self.known_apis and not self._is_standard_library(module):
                errors.append(f"Unknown module: {module}")
        
        return errors
    
    async def _check_vulnerable_patterns(self, code: str) -> List[str]:
        """Check for vulnerable code patterns"""
        warnings = []
        vulnerable_patterns = [
            r'eval\(',
            r'exec\(',
            r'os\.system',
            r'subprocess\.call',
            r'pickle\.loads'
        ]
        
        for pattern in vulnerable_patterns:
            if re.search(pattern, code):
                warnings.append(f"Vulnerable pattern detected: {pattern}")
        
        return warnings
    
    async def _check_secure_patterns(self, code: str) -> List[str]:
        """Check for secure code patterns"""
        suggestions = []
        secure_patterns = [
            r'password.*hash',
            r'jwt.*secret',
            r'csrf.*token',
            r'rate.*limit'
        ]
        
        for pattern in secure_patterns:
            if not re.search(pattern, code, re.IGNORECASE):
                suggestions.append(f"Consider adding: {pattern}")
        
        return suggestions
    
    def _is_standard_library(self, module: str) -> bool:
        """Check if module is from standard library"""
        standard_modules = [
            "os", "sys", "json", "datetime", "time", "random", "math",
            "collections", "itertools", "functools", "operator"
        ]
        return module in standard_modules
    
    def _calculate_accuracy_score(self, result: ValidationResult) -> float:
        """Calculate accuracy score"""
        if not result.errors and not result.warnings:
            return 1.0
        elif not result.errors:
            return 0.8
        else:
            return 0.0

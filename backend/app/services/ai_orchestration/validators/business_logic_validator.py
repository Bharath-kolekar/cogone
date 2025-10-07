"""
Business Logic Validator for AI Orchestration
Validates business logic and rules
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class BusinessLogicValidator:
    """Validates business logic and rules"""
    
    def __init__(self):
        self.business_rules = self._load_business_rules()
        self.validation_patterns = self._load_validation_patterns()
        
    def _load_business_rules(self) -> Dict[str, List[str]]:
        """Load business rules"""
        return {
            "authentication": [
                r'password.*hash',
                r'jwt.*token',
                r'session.*management'
            ],
            "authorization": [
                r'role.*check',
                r'permission.*validate',
                r'access.*control'
            ],
            "data_validation": [
                r'input.*validate',
                r'data.*sanitize',
                r'format.*check'
            ]
        }
    
    def _load_validation_patterns(self) -> Dict[str, List[str]]:
        """Load validation patterns"""
        return {
            "email_validation": [
                r'@\w+\.\w+',
                r'email.*valid',
                r'format.*email'
            ],
            "phone_validation": [
                r'phone.*valid',
                r'format.*phone',
                r'number.*check'
            ],
            "date_validation": [
                r'date.*valid',
                r'format.*date',
                r'time.*check'
            ]
        }
    
    async def validate_business_logic(self, code: str) -> Dict[str, Any]:
        """Validate business logic"""
        try:
            business_result = {
                "is_valid_business_logic": True,
                "business_violations": [],
                "missing_validations": [],
                "rule_compliance": {}
            }
            
            # Check business rules
            rule_compliance = await self._check_business_rules(code)
            business_result["rule_compliance"] = rule_compliance
            
            # Check for missing validations
            missing_validations = await self._check_missing_validations(code)
            business_result["missing_validations"].extend(missing_validations)
            
            # Check for business logic violations
            violations = await self._check_business_violations(code)
            business_result["business_violations"].extend(violations)
            
            # Update business logic status
            business_result["is_valid_business_logic"] = len(business_result["business_violations"]) == 0
            
            return business_result
            
        except Exception as e:
            logger.error(f"Error validating business logic: {e}")
            return {"is_valid_business_logic": False, "business_violations": [f"Business logic error: {str(e)}"]}
    
    async def _check_business_rules(self, code: str) -> Dict[str, bool]:
        """Check business rules"""
        compliance = {}
        
        for rule, patterns in self.business_rules.items():
            compliance[rule] = any(re.search(pattern, code, re.IGNORECASE) for pattern in patterns)
        
        return compliance
    
    async def _check_missing_validations(self, code: str) -> List[str]:
        """Check for missing validations"""
        missing = []
        
        # Check for input validation
        if 'input' in code.lower() and 'validate' not in code.lower():
            missing.append("Missing input validation")
        
        # Check for output sanitization
        if 'output' in code.lower() and 'sanitize' not in code.lower():
            missing.append("Missing output sanitization")
        
        return missing
    
    async def _check_business_violations(self, code: str) -> List[str]:
        """Check for business logic violations"""
        violations = []
        
        # Check for hardcoded business rules
        if 'if ' in code and 'config' not in code.lower():
            violations.append("Hardcoded business rules detected")
        
        return violations


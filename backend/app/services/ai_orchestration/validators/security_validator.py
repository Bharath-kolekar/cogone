"""
Security Validator for AI Orchestration
Prevents vulnerable code patterns
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class SecurityValidator:
    """Prevents vulnerable code patterns"""
    
    def __init__(self):
        self.security_patterns = self._load_security_patterns()
        self.vulnerability_rules = self._load_vulnerability_rules()
        
    def _load_security_patterns(self) -> Dict[str, List[str]]:
        """Load security patterns"""
        return {
            "vulnerable_patterns": [
                r'eval\s*\(',
                r'exec\s*\(',
                r'os\.system\s*\(',
                r'subprocess\.call\s*\(',
                r'pickle\.loads\s*\(',
                r'shell=True',
                r'os\.popen\s*\('
            ],
            "secure_patterns": [
                r'password.*hash',
                r'jwt.*secret',
                r'csrf.*token',
                r'rate.*limit',
                r'input.*validate',
                r'output.*sanitize'
            ]
        }
    
    def _load_vulnerability_rules(self) -> Dict[str, Any]:
        """Load vulnerability rules"""
        return {
            "authentication": {
                "required": True,
                "patterns": ["jwt", "oauth", "session"]
            },
            "authorization": {
                "required": True,
                "patterns": ["role", "permission", "access"]
            },
            "input_validation": {
                "required": True,
                "patterns": ["validate", "sanitize", "escape"]
            }
        }
    
    async def validate_security(self, code: str) -> Dict[str, Any]:
        """Validate code security"""
        try:
            security_result = {
                "is_secure": True,
                "vulnerabilities": [],
                "security_warnings": [],
                "security_suggestions": []
            }
            
            # Check for vulnerabilities
            vulnerabilities = await self._check_vulnerabilities(code)
            security_result["vulnerabilities"].extend(vulnerabilities)
            
            # Check for security warnings
            warnings = await self._check_security_warnings(code)
            security_result["security_warnings"].extend(warnings)
            
            # Generate security suggestions
            suggestions = await self._generate_security_suggestions(code)
            security_result["security_suggestions"].extend(suggestions)
            
            # Update security status
            security_result["is_secure"] = len(vulnerabilities) == 0
            
            return security_result
            
        except Exception as e:
            logger.error(f"Error validating security: {e}")
            return {"is_secure": False, "vulnerabilities": [f"Security error: {str(e)}"]}
    
    async def _check_vulnerabilities(self, code: str) -> List[str]:
        """Check for security vulnerabilities"""
        vulnerabilities = []
        
        for pattern in self.security_patterns["vulnerable_patterns"]:
            if re.search(pattern, code):
                vulnerabilities.append(f"Security vulnerability: {pattern}")
        
        return vulnerabilities
    
    async def _check_security_warnings(self, code: str) -> List[str]:
        """Check for security warnings"""
        warnings = []
        
        # Check for missing authentication
        if 'api' in code.lower() and 'auth' not in code.lower():
            warnings.append("Missing authentication for API endpoints")
        
        # Check for missing input validation
        if 'input' in code.lower() and 'validate' not in code.lower():
            warnings.append("Missing input validation")
        
        return warnings
    
    async def _generate_security_suggestions(self, code: str) -> List[str]:
        """Generate security suggestions"""
        suggestions = []
        
        # Suggest adding authentication
        if 'api' in code.lower() and 'auth' not in code.lower():
            suggestions.append("Add authentication to API endpoints")
        
        # Suggest adding input validation
        if 'input' in code.lower() and 'validate' not in code.lower():
            suggestions.append("Add input validation")
        
        return suggestions


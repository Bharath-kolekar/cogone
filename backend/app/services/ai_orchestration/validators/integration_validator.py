"""
Integration Validator for AI Orchestration
Validates integration patterns and API compatibility
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class IntegrationValidator:
    """Validates integration patterns and API compatibility"""
    
    def __init__(self):
        self.integration_patterns = self._load_integration_patterns()
        self.api_compatibility = self._load_api_compatibility()
        
    def _load_integration_patterns(self) -> Dict[str, List[str]]:
        """Load integration patterns"""
        return {
            "rest_api": [
                r'@router\.(get|post|put|delete)',
                r'async def \w+',
                r'HTTPException'
            ],
            "database": [
                r'sqlalchemy',
                r'async def \w+',
                r'await \w+'
            ],
            "cache": [
                r'redis',
                r'cache',
                r'await \w+'
            ]
        }
    
    def _load_api_compatibility(self) -> Dict[str, List[str]]:
        """Load API compatibility rules"""
        return {
            "versioning": [
                r'v\d+',
                r'version',
                r'api/v\d+'
            ],
            "authentication": [
                r'bearer',
                r'token',
                r'auth'
            ],
            "error_handling": [
                r'HTTPException',
                r'status_code',
                r'error'
            ]
        }
    
    async def validate_integration(self, code: str) -> Dict[str, Any]:
        """Validate integration patterns"""
        try:
            integration_result = {
                "is_well_integrated": True,
                "integration_issues": [],
                "compatibility_issues": [],
                "pattern_compliance": {}
            }
            
            # Check integration patterns
            pattern_compliance = await self._check_integration_patterns(code)
            integration_result["pattern_compliance"] = pattern_compliance
            
            # Check API compatibility
            compatibility_issues = await self._check_api_compatibility(code)
            integration_result["compatibility_issues"].extend(compatibility_issues)
            
            # Check for integration issues
            integration_issues = await self._check_integration_issues(code)
            integration_result["integration_issues"].extend(integration_issues)
            
            # Update integration status
            integration_result["is_well_integrated"] = len(integration_result["integration_issues"]) == 0
            
            return integration_result
            
        except Exception as e:
            logger.error(f"Error validating integration: {e}")
            return {"is_well_integrated": False, "integration_issues": [f"Integration error: {str(e)}"]}
    
    async def _check_integration_patterns(self, code: str) -> Dict[str, bool]:
        """Check integration patterns"""
        compliance = {}
        
        for pattern, rules in self.integration_patterns.items():
            compliance[pattern] = all(re.search(rule, code) for rule in rules)
        
        return compliance
    
    async def _check_api_compatibility(self, code: str) -> List[str]:
        """Check API compatibility"""
        issues = []
        
        # Check for versioning
        if 'api' in code.lower() and 'v' not in code.lower():
            issues.append("Missing API versioning")
        
        # Check for authentication
        if 'api' in code.lower() and 'auth' not in code.lower():
            issues.append("Missing API authentication")
        
        return issues
    
    async def _check_integration_issues(self, code: str) -> List[str]:
        """Check for integration issues"""
        issues = []
        
        # Check for error handling
        if 'api' in code.lower() and 'error' not in code.lower():
            issues.append("Missing error handling")
        
        return issues


"""
Architecture Validator for AI Orchestration
Validates and enforces architectural patterns
"""

import re
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class ArchitectureValidator:
    """Validates and enforces architectural patterns"""
    
    def __init__(self):
        self.architectural_patterns = self._load_architectural_patterns()
        self.solid_principles = self._load_solid_principles()
        
    def _load_architectural_patterns(self) -> Dict[str, List[str]]:
        """Load architectural patterns"""
        return {
            "mvc": [
                r'class\s+\w+Controller',
                r'class\s+\w+Model',
                r'class\s+\w+View'
            ],
            "repository": [
                r'class\s+\w+Repository',
                r'def\s+get_\w+',
                r'def\s+save_\w+'
            ],
            "service": [
                r'class\s+\w+Service',
                r'def\s+\w+_service'
            ]
        }
    
    def _load_solid_principles(self) -> Dict[str, List[str]]:
        """Load SOLID principles"""
        return {
            "single_responsibility": [
                r'class\s+\w+.*:\s*$',
                r'def\s+\w+.*:\s*$'
            ],
            "open_closed": [
                r'class\s+\w+.*:\s*$',
                r'def\s+\w+.*:\s*$'
            ],
            "liskov_substitution": [
                r'class\s+\w+.*:\s*$',
                r'def\s+\w+.*:\s*$'
            ],
            "interface_segregation": [
                r'class\s+\w+.*:\s*$',
                r'def\s+\w+.*:\s*$'
            ],
            "dependency_inversion": [
                r'class\s+\w+.*:\s*$',
                r'def\s+\w+.*:\s*$'
            ]
        }
    
    async def validate_architecture(self, code: str) -> Dict[str, Any]:
        """Validate architectural patterns"""
        try:
            architecture_result = {
                "is_well_architected": True,
                "architectural_violations": [],
                "pattern_compliance": {},
                "solid_violations": []
            }
            
            # Check architectural patterns
            pattern_compliance = await self._check_architectural_patterns(code)
            architecture_result["pattern_compliance"] = pattern_compliance
            
            # Check SOLID principles
            solid_violations = await self._check_solid_principles(code)
            architecture_result["solid_violations"].extend(solid_violations)
            
            # Check for architectural violations
            violations = await self._check_architectural_violations(code)
            architecture_result["architectural_violations"].extend(violations)
            
            # Update architecture status
            architecture_result["is_well_architected"] = len(architecture_result["architectural_violations"]) == 0
            
            return architecture_result
            
        except Exception as e:
            logger.error(f"Error validating architecture: {e}")
            return {"is_well_architected": False, "architectural_violations": [f"Architecture error: {str(e)}"]}
    
    async def _check_architectural_patterns(self, code: str) -> Dict[str, bool]:
        """Check architectural patterns"""
        compliance = {}
        
        for pattern, rules in self.architectural_patterns.items():
            compliance[pattern] = all(re.search(rule, code) for rule in rules)
        
        return compliance
    
    async def _check_solid_principles(self, code: str) -> List[str]:
        """Check SOLID principles"""
        violations = []
        
        # Check single responsibility principle
        classes = re.findall(r'class\s+(\w+).*?:\s*(.*?)(?=\nclass|\n$)', code, re.DOTALL)
        for class_name, class_body in classes:
            methods = re.findall(r'def\s+(\w+)', class_body)
            if len(methods) > 10:  # Threshold for single responsibility
                violations.append(f"Class {class_name} violates single responsibility principle")
        
        return violations
    
    async def _check_architectural_violations(self, code: str) -> List[str]:
        """Check for architectural violations"""
        violations = []
        
        # Check for circular dependencies
        imports = re.findall(r'from\s+(\w+)\s+import', code)
        if len(imports) > 10:  # Threshold for circular dependencies
            violations.append("Potential circular dependency detected")
        
        # Check for tight coupling
        if 'global ' in code:
            violations.append("Global variables indicate tight coupling")
        
        return violations


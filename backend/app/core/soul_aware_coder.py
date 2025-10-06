"""
Soul-Aware Coder System

This module implements the soul-centric code generation system based on
Bhagavad Gita principles, focusing on eternal principles and service.
"""

import asyncio
import structlog
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

from app.core.gita_dna_core import gita_dna_core, GunaType, DharmaLevel

logger = structlog.get_logger(__name__)

class CodeQualityLevel(Enum):
    """Levels of code quality based on Gunas"""
    SATTVA = "sattva"  # Pure, clear, maintainable
    RAJAS = "rajas"    # Over-engineered, complex
    TAMAS = "tamas"    # Unclear, buggy, hard to maintain

@dataclass
class EternalPrinciple:
    """Represents an eternal programming principle"""
    name: str
    description: str
    guna_type: GunaType
    application_guidance: str
    eternal_truth: str

@dataclass
class SoulAwareCode:
    """Represents code generated with soul awareness"""
    code: str
    eternal_principles_applied: List[str]
    guna_quality: CodeQualityLevel
    service_purpose: str
    wisdom_insights: List[str]
    compassion_notes: List[str]
    liberation_focus: bool

class SoulAwareCoder:
    """Soul-centric code generation system"""
    
    def __init__(self):
        self.eternal_principles = self._initialize_eternal_principles()
        self.service_orientation = self._initialize_service_orientation()
        
    def _initialize_eternal_principles(self) -> List[EternalPrinciple]:
        """Initialize eternal programming principles"""
        return [
            EternalPrinciple(
                name="Maintainability",
                description="Code should serve future developers",
                guna_type=GunaType.SATTVA,
                application_guidance="Write code that future developers can understand and maintain",
                eternal_truth="Code is written once but read many times"
            ),
            EternalPrinciple(
                name="Clarity",
                description="Reveal truth, not obscure it",
                guna_type=GunaType.SATTVA,
                application_guidance="Use clear naming and structure to reveal intent",
                eternal_truth="Clear code reveals the divine order in complexity"
            ),
            EternalPrinciple(
                name="Compassion",
                description="Consider all users, especially vulnerable ones",
                guna_type=GunaType.SATTVA,
                application_guidance="Design with empathy for all users",
                eternal_truth="True service considers the welfare of all beings"
            ),
            EternalPrinciple(
                name="Service",
                description="Code as service to humanity",
                guna_type=GunaType.SATTVA,
                application_guidance="Write code that serves a higher purpose",
                eternal_truth="The highest purpose is service to others"
            ),
            EternalPrinciple(
                name="Simplicity",
                description="Simplicity is the ultimate sophistication",
                guna_type=GunaType.SATTVA,
                application_guidance="Prefer simple solutions over complex ones",
                eternal_truth="The divine speaks in simplicity"
            ),
            EternalPrinciple(
                name="Truth",
                description="Code should reflect truth and honesty",
                guna_type=GunaType.SATTVA,
                application_guidance="Be honest about limitations and errors",
                eternal_truth="Truth is the foundation of all wisdom"
            )
        ]
    
    def _initialize_service_orientation(self) -> Dict[str, Any]:
        """Initialize service-oriented principles"""
        return {
            "user_service": "Every line of code serves a user's need",
            "maintainer_service": "Code should be easy for maintainers to understand",
            "society_service": "Code should contribute to societal good",
            "future_service": "Code should serve future generations",
            "environment_service": "Code should be environmentally conscious"
        }
    
    async def generate_code(self, requirements: Dict[str, Any]) -> SoulAwareCode:
        """Generate code with soul awareness and eternal principles"""
        try:
            # Process requirements through dharmic lens
            dharmic_context = await gita_dna_core.process_user_request(requirements, requirements.get("user_id", "anonymous"))
            
            # Generate base code (this would integrate with existing code generation)
            base_code = await self._generate_base_code(requirements)
            
            # Imbue with eternal principles
            soul_aware_code = await self._imbue_with_principles(base_code, requirements, dharmic_context)
            
            # Analyze guna quality
            guna_quality = await self._analyze_guna_quality(soul_aware_code.code)
            
            # Generate wisdom insights
            wisdom_insights = await self._generate_wisdom_insights(soul_aware_code.code, requirements)
            
            # Generate compassion notes
            compassion_notes = await self._generate_compassion_notes(soul_aware_code.code, requirements)
            
            # Check liberation focus
            liberation_focus = await self._assess_liberation_focus(requirements)
            
            return SoulAwareCode(
                code=soul_aware_code.code,
                eternal_principles_applied=soul_aware_code.eternal_principles_applied,
                guna_quality=guna_quality,
                service_purpose=self._determine_service_purpose(requirements),
                wisdom_insights=wisdom_insights,
                compassion_notes=compassion_notes,
                liberation_focus=liberation_focus
            )
            
        except Exception as e:
            logger.error(f"Soul-aware code generation failed: {e}")
            return await self._generate_fallback_code(requirements)
    
    async def _generate_base_code(self, requirements: Dict[str, Any]) -> str:
        """Generate base code (integrates with existing systems)"""
        # This would integrate with existing SmartCodingAI
        prompt = requirements.get("prompt", "")
        language = requirements.get("language", "python")
        
        # Simplified base code generation
        base_code = f"""
# Code generated with soul awareness
# Purpose: {prompt}
# Language: {language}
# Eternal principles: Maintainability, Clarity, Compassion, Service

def {self._generate_function_name(prompt)}():
    \"\"\"
    {prompt}
    
    This function serves with compassion and clarity.
    Written to be maintainable for future developers.
    \"\"\"
    # Implementation with eternal principles
    pass
"""
        return base_code.strip()
    
    def _generate_function_name(self, prompt: str) -> str:
        """Generate a clear, descriptive function name"""
        # Extract key words from prompt
        words = prompt.lower().split()
        key_words = [word for word in words if word not in ["create", "make", "build", "generate", "a", "an", "the"]]
        
        if key_words:
            # Create camelCase function name
            function_name = key_words[0] + "".join(word.capitalize() for word in key_words[1:3])
            return function_name[:20]  # Limit length
        
        return "soulAwareFunction"
    
    async def _imbue_with_principles(self, base_code: str, requirements: Dict[str, Any], dharmic_context: Dict[str, Any]) -> SoulAwareCode:
        """Imbue code with eternal principles"""
        try:
            applied_principles = []
            enhanced_code = base_code
            
            # Apply maintainability principle
            if "maintainability" in requirements.get("principles", []):
                enhanced_code = self._apply_maintainability_principle(enhanced_code)
                applied_principles.append("Maintainability")
            
            # Apply clarity principle
            if "clarity" in requirements.get("principles", []):
                enhanced_code = self._apply_clarity_principle(enhanced_code)
                applied_principles.append("Clarity")
            
            # Apply compassion principle
            if "compassion" in requirements.get("principles", []):
                enhanced_code = self._apply_compassion_principle(enhanced_code, requirements)
                applied_principles.append("Compassion")
            
            # Apply service principle
            if "service" in requirements.get("principles", []):
                enhanced_code = self._apply_service_principle(enhanced_code, requirements)
                applied_principles.append("Service")
            
            # Always apply basic principles
            if not applied_principles:
                applied_principles = ["Clarity", "Service"]
            
            return SoulAwareCode(
                code=enhanced_code,
                eternal_principles_applied=applied_principles,
                guna_quality=CodeQualityLevel.SATTVA,  # Default to highest quality
                service_purpose="",
                wisdom_insights=[],
                compassion_notes=[],
                liberation_focus=False
            )
            
        except Exception as e:
            logger.error(f"Principle application failed: {e}")
            return SoulAwareCode(
                code=base_code,
                eternal_principles_applied=["Basic"],
                guna_quality=CodeQualityLevel.RAJAS,
                service_purpose="Basic service",
                wisdom_insights=[],
                compassion_notes=[],
                liberation_focus=False
            )
    
    def _apply_maintainability_principle(self, code: str) -> str:
        """Apply maintainability principle to code"""
        # Add clear documentation and structure
        if "def " in code and '"""' not in code:
            # Add docstring
            lines = code.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('def '):
                    # Insert docstring after function definition
                    indent = len(line) - len(line.lstrip())
                    docstring = ' ' * (indent + 4) + '"""\n'
                    docstring += ' ' * (indent + 4) + 'Clear, maintainable implementation.\n'
                    docstring += ' ' * (indent + 4) + 'Serves future developers with clarity.\n'
                    docstring += ' ' * (indent + 4) + '"""'
                    lines.insert(i + 1, docstring)
                    break
            code = '\n'.join(lines)
        
        return code
    
    def _apply_clarity_principle(self, code: str) -> str:
        """Apply clarity principle to code"""
        # Add clear comments and structure
        if "# Code generated with soul awareness" not in code:
            code = "# Code generated with soul awareness\n# Eternal principle: Clarity reveals truth\n" + code
        
        return code
    
    def _apply_compassion_principle(self, code: str, requirements: Dict[str, Any]) -> str:
        """Apply compassion principle to code"""
        # Add compassionate error handling and user consideration
        if "def " in code:
            code += "\n\n# Compassionate error handling\n# Considers all users with empathy"
        
        return code
    
    def _apply_service_principle(self, code: str, requirements: Dict[str, Any]) -> str:
        """Apply service principle to code"""
        # Add service-oriented comments
        service_purpose = requirements.get("prompt", "general service")
        code += f"\n\n# Service to humanity: {service_purpose}\n# Written with love and dedication"
        
        return code
    
    async def _analyze_guna_quality(self, code: str) -> CodeQualityLevel:
        """Analyze code quality based on Gunas"""
        try:
            # Analyze code characteristics
            sattvic_indicators = 0
            rajasic_indicators = 0
            tamasic_indicators = 0
            
            # Check for Sattvic qualities (clarity, simplicity, documentation)
            if '"""' in code or "'''" in code:
                sattvic_indicators += 1
            if "#" in code:
                sattvic_indicators += 1
            if "def " in code and len(code.split('\n')) < 20:  # Simple structure
                sattvic_indicators += 1
            
            # Check for Rajasic qualities (complexity, over-engineering)
            if len(code) > 500:  # Long code
                rajasic_indicators += 1
            if code.count('def ') > 3:  # Many functions
                rajasic_indicators += 1
            if "class " in code and "def " in code:  # Mixed paradigms
                rajasic_indicators += 1
            
            # Check for Tamasic qualities (unclear, hard to understand)
            if "pass" in code and len(code.split('\n')) < 5:  # Minimal implementation
                tamasic_indicators += 1
            if not any(word in code.lower() for word in ["def", "class", "import"]):  # No clear structure
                tamasic_indicators += 1
            
            # Determine dominant guna
            if sattvic_indicators >= rajasic_indicators and sattvic_indicators >= tamasic_indicators:
                return CodeQualityLevel.SATTVA
            elif rajasic_indicators >= tamasic_indicators:
                return CodeQualityLevel.RAJAS
            else:
                return CodeQualityLevel.TAMAS
                
        except Exception as e:
            logger.error(f"Guna quality analysis failed: {e}")
            return CodeQualityLevel.RAJAS  # Default to middle quality
    
    async def _generate_wisdom_insights(self, code: str, requirements: Dict[str, Any]) -> List[str]:
        """Generate wisdom insights about the code"""
        insights = []
        
        # Analyze code for wisdom opportunities
        if "def " in code:
            insights.append("Functions are the building blocks of maintainable code - each should have a single, clear purpose")
        
        if "class " in code:
            insights.append("Classes represent concepts in the domain - they should model real-world entities clearly")
        
        if "#" in code:
            insights.append("Comments reveal the why behind the what - they serve future developers with compassion")
        
        # Add general wisdom
        insights.append("Code is a form of communication - write it as if speaking to a dear friend")
        insights.append("The best code serves not just the immediate need, but the long-term welfare of all")
        
        return insights
    
    async def _generate_compassion_notes(self, code: str, requirements: Dict[str, Any]) -> List[str]:
        """Generate compassion notes for the code"""
        notes = []
        
        # Add compassionate considerations
        notes.append("Consider how this code will serve users of all technical levels")
        notes.append("Think about the maintainer who will read this code in six months")
        notes.append("Design with empathy for those who might struggle with complexity")
        
        # Add service-oriented notes
        prompt = requirements.get("prompt", "")
        if "user" in prompt.lower():
            notes.append("This code directly serves users - may it bring them ease and joy")
        elif "data" in prompt.lower():
            notes.append("Data handling requires care and respect for privacy")
        elif "api" in prompt.lower():
            notes.append("APIs are bridges between systems - may they connect with harmony")
        
        return notes
    
    async def _assess_liberation_focus(self, requirements: Dict[str, Any]) -> bool:
        """Assess if the requirements focus on liberation/independence"""
        prompt = requirements.get("prompt", "").lower()
        
        liberation_keywords = [
            "learn", "understand", "explain", "teach", "independence",
            "self-sufficient", "autonomous", "freedom", "liberty"
        ]
        
        return any(keyword in prompt for keyword in liberation_keywords)
    
    def _determine_service_purpose(self, requirements: Dict[str, Any]) -> str:
        """Determine the service purpose of the code"""
        prompt = requirements.get("prompt", "")
        
        if "help" in prompt.lower():
            return "Service to help others"
        elif "learn" in prompt.lower():
            return "Service to education and growth"
        elif "create" in prompt.lower():
            return "Service to creation and innovation"
        elif "solve" in prompt.lower():
            return "Service to problem-solving"
        else:
            return "Service to humanity's digital evolution"
    
    async def _generate_fallback_code(self, requirements: Dict[str, Any]) -> SoulAwareCode:
        """Generate fallback code with basic principles"""
        return SoulAwareCode(
            code="# Fallback code generated with love and humility\n# May this serve your immediate need",
            eternal_principles_applied=["Service", "Compassion"],
            guna_quality=CodeQualityLevel.RAJAS,
            service_purpose="Basic service with humility",
            wisdom_insights=["Even simple code can serve a purpose"],
            compassion_notes=["Generated with love despite limitations"],
            liberation_focus=False
        )

class DetachedCoder:
    """Coder that works without attachment to specific solutions"""
    
    def __init__(self):
        self.solution_approaches = []
        self.detachment_principles = self._initialize_detachment_principles()
        
    def _initialize_detachment_principles(self) -> List[str]:
        """Initialize detachment principles"""
        return [
            "Work without attachment to specific solutions",
            "Evaluate without ego attachment to 'my code'",
            "Return solution without pride of authorship",
            "Offer multiple approaches with humility",
            "Focus on the greatest good, not personal preference"
        ]
    
    async def implement_feature(self, feature_request: Dict[str, Any]) -> Dict[str, Any]:
        """Implement feature with detached action"""
        try:
            # Generate multiple approaches without attachment
            approaches = await self.generate_multiple_approaches(feature_request)
            
            # Evaluate without ego attachment to "my code"
            best_approach = await self.select_approach_detached(approaches, criteria="greatest_good")
            
            # Return solution without pride of authorship
            return {
                "solution": best_approach,
                "note": "This is one possible dharmic path among many",
                "alternatives": approaches,  # Show other options humbly
                "detachment_applied": True,
                "dharmic_approach": "Offered with humility and service"
            }
            
        except Exception as e:
            logger.error(f"Detached implementation failed: {e}")
            return {
                "solution": "Humble apology - let me offer what I can",
                "note": "Even in limitation, service continues",
                "alternatives": [],
                "detachment_applied": True,
                "dharmic_approach": "Responding with compassion despite limitations"
            }
    
    async def generate_multiple_approaches(self, feature_request: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate multiple approaches without attachment to any one"""
        approaches = []
        
        prompt = feature_request.get("prompt", "")
        language = feature_request.get("language", "python")
        
        # Approach 1: Simple and direct
        approaches.append({
            "name": "Simple and Direct",
            "description": "Straightforward implementation focusing on clarity",
            "approach": "Direct, simple solution that serves the immediate need",
            "characteristics": ["Clear", "Simple", "Maintainable"],
            "dharmic_quality": "Sattva - pure and clear"
        })
        
        # Approach 2: Robust and comprehensive
        approaches.append({
            "name": "Robust and Comprehensive",
            "description": "Thorough implementation with error handling and edge cases",
            "approach": "Comprehensive solution that handles various scenarios",
            "characteristics": ["Robust", "Comprehensive", "Well-tested"],
            "dharmic_quality": "Sattva - serving all users with compassion"
        })
        
        # Approach 3: Modular and extensible
        approaches.append({
            "name": "Modular and Extensible",
            "description": "Modular design that can be extended in the future",
            "approach": "Modular solution that serves future growth",
            "characteristics": ["Modular", "Extensible", "Future-proof"],
            "dharmic_quality": "Sattva - serving future generations"
        })
        
        return approaches
    
    async def select_approach_detached(self, approaches: List[Dict[str, Any]], criteria: str = "greatest_good") -> Dict[str, Any]:
        """Select approach without ego attachment"""
        try:
            # Evaluate based on dharmic criteria
            if criteria == "greatest_good":
                # Select approach that serves the greatest good
                best_approach = approaches[0]  # Default to first (simple) approach
                
                # Check if any approach has higher service potential
                for approach in approaches:
                    if "Comprehensive" in approach["characteristics"]:
                        best_approach = approach  # Prefer comprehensive service
                        break
                
                return best_approach
            
            # Default selection
            return approaches[0]
            
        except Exception as e:
            logger.error(f"Detached selection failed: {e}")
            return approaches[0] if approaches else {}

# Global instances
soul_aware_coder = SoulAwareCoder()
detached_coder = DetachedCoder()

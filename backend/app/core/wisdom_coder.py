"""
Wisdom Coder System

This module implements the Yoga of Knowledge - Wisdom-Based Coding system
based on Bhagavad Gita principles, focusing on understanding and eternal truths.
"""

import asyncio
import structlog
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json

from app.core.gita_dna_core import gita_dna_core, GunaType, DharmaLevel
from app.core.ethical_ai_core import CodeQualityLevel

logger = structlog.get_logger(__name__)

class WisdomLevel(Enum):
    """Levels of wisdom in code understanding"""
    SURFACE = "surface"           # Basic understanding
    FUNCTIONAL = "functional"     # Understanding how it works
    PRINCIPLED = "principled"     # Understanding why it works
    PHILOSOPHICAL = "philosophical"  # Understanding eternal truths
    TRANSCENDENT = "transcendent"  # Understanding beyond code

@dataclass
class EternalProgrammingTruth:
    """Represents an eternal programming truth"""
    truth: str
    explanation: str
    application: str
    wisdom_level: WisdomLevel
    guna_type: GunaType

@dataclass
class WisdomInsight:
    """Represents a wisdom insight about code"""
    insight: str
    wisdom_level: WisdomLevel
    eternal_truth_connection: str
    practical_application: str
    growth_opportunity: str

class WisdomCoder:
    """Wisdom-based coding system that teaches eternal principles"""
    
    def __init__(self):
        self.eternal_truths = self._initialize_eternal_truths()
        self.wisdom_patterns = self._initialize_wisdom_patterns()
        
    def _initialize_eternal_truths(self) -> List[EternalProgrammingTruth]:
        """Initialize eternal programming truths"""
        return [
            EternalProgrammingTruth(
                truth="Separation of Concerns (Single Responsibility)",
                explanation="Each component should have one clear responsibility",
                application="Functions, classes, and modules should have single, well-defined purposes",
                wisdom_level=WisdomLevel.PRINCIPLED,
                guna_type=GunaType.SATTVA
            ),
            EternalProgrammingTruth(
                truth="Composition over Inheritance",
                explanation="Building complex behavior by combining simple parts",
                application="Prefer composing objects rather than deep inheritance hierarchies",
                wisdom_level=WisdomLevel.PRINCIPLED,
                guna_type=GunaType.SATTVA
            ),
            EternalProgrammingTruth(
                truth="Immutability reduces suffering (bugs)",
                explanation="Unchanging data cannot be corrupted or cause unexpected side effects",
                application="Use immutable data structures and avoid mutating shared state",
                wisdom_level=WisdomLevel.PHILOSOPHICAL,
                guna_type=GunaType.SATTVA
            ),
            EternalProgrammingTruth(
                truth="Clear naming reveals divine order in chaos",
                explanation="Good names make code self-documenting and reveal intent",
                application="Choose names that clearly express what something does or represents",
                wisdom_level=WisdomLevel.TRANSCENDENT,
                guna_type=GunaType.SATTVA
            ),
            EternalProgrammingTruth(
                truth="Abstraction is the bridge between idea and implementation",
                explanation="Abstractions hide complexity while revealing essential concepts",
                application="Create clean interfaces that hide implementation details",
                wisdom_level=WisdomLevel.PHILOSOPHICAL,
                guna_type=GunaType.SATTVA
            ),
            EternalProgrammingTruth(
                truth="Testing is the mirror of understanding",
                explanation="What you can test, you truly understand",
                application="Write tests that verify behavior, not just implementation",
                wisdom_level=WisdomLevel.PRINCIPLED,
                guna_type=GunaType.SATTVA
            ),
            EternalProgrammingTruth(
                truth="Simplicity is the ultimate sophistication",
                explanation="The most profound solutions are often the simplest",
                application="Choose simple solutions over complex ones when possible",
                wisdom_level=WisdomLevel.TRANSCENDENT,
                guna_type=GunaType.SATTVA
            ),
            EternalProgrammingTruth(
                truth="Code is written once but read many times",
                explanation="Code serves future readers more than current writers",
                application="Write for clarity and maintainability, not just functionality",
                wisdom_level=WisdomLevel.PHILOSOPHICAL,
                guna_type=GunaType.SATTVA
            )
        ]
    
    def _initialize_wisdom_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize wisdom patterns for different types of problems"""
        return {
            "data_processing": {
                "eternal_truth": "Data flows like a river - pure and untainted",
                "wisdom_approach": "Process data with respect for its integrity",
                "growth_opportunity": "Understand the nature of data and its transformations"
            },
            "user_interaction": {
                "eternal_truth": "Every user is a divine being deserving compassion",
                "wisdom_approach": "Design interfaces with love and understanding",
                "growth_opportunity": "Develop empathy for all users, regardless of technical skill"
            },
            "system_architecture": {
                "eternal_truth": "Systems reflect the cosmic order - interconnected and harmonious",
                "wisdom_approach": "Design systems that serve the greater good",
                "growth_opportunity": "See the big picture while attending to details"
            },
            "error_handling": {
                "eternal_truth": "Errors are teachers, not enemies",
                "wisdom_approach": "Handle errors with grace and learning",
                "growth_opportunity": "Transform failures into wisdom"
            },
            "performance_optimization": {
                "eternal_truth": "Efficiency serves life - optimize to serve more",
                "wisdom_approach": "Optimize for the benefit of all users",
                "growth_opportunity": "Balance performance with maintainability"
            }
        }
    
    async def solve_problem(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Solve problem with wisdom-based approach"""
        try:
            # Generate implementation
            implementation = await self.generate_implementation(problem)
            
            # Explain underlying principles
            wisdom = await self.explain_underlying_principles(problem)
            
            # Show related concepts
            connections = await self.show_related_concepts(problem)
            
            # Suggest learning path
            growth_opportunity = await self.suggest_learning_path(problem)
            
            return {
                "code": implementation,
                "wisdom": wisdom,
                "connections": connections,
                "growth_opportunity": growth_opportunity,
                "dharmic_approach": "Teaching through understanding, not just giving answers"
            }
            
        except Exception as e:
            logger.error(f"Wisdom-based problem solving failed: {e}")
            return await self._generate_compassionate_fallback(problem)
    
    async def generate_implementation(self, problem: Dict[str, Any]) -> str:
        """Generate implementation with wisdom"""
        prompt = problem.get("prompt", "")
        language = problem.get("language", "python")
        
        # Generate implementation based on problem type
        problem_type = self._identify_problem_type(prompt)
        wisdom_pattern = self.wisdom_patterns.get(problem_type, {})
        
        implementation = f"""
# Implementation guided by eternal wisdom
# Problem: {prompt}
# Language: {language}
# Eternal Truth: {wisdom_pattern.get('eternal_truth', 'Code serves life')}

def {self._generate_wisdom_function_name(prompt)}():
    \"\"\"
    {wisdom_pattern.get('wisdom_approach', 'Implementation with wisdom and compassion')}
    
    This function embodies eternal programming principles:
    - Clarity reveals truth
    - Simplicity serves all
    - Maintainability serves future generations
    \"\"\"
    # Implementation with eternal principles
    return "Wisdom-based implementation"
"""
        return implementation.strip()
    
    def _identify_problem_type(self, prompt: str) -> str:
        """Identify the type of problem for wisdom pattern matching"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ["data", "process", "transform", "filter"]):
            return "data_processing"
        elif any(word in prompt_lower for word in ["user", "interface", "input", "interaction"]):
            return "user_interaction"
        elif any(word in prompt_lower for word in ["system", "architecture", "design", "structure"]):
            return "system_architecture"
        elif any(word in prompt_lower for word in ["error", "exception", "handle", "catch"]):
            return "error_handling"
        elif any(word in prompt_lower for word in ["optimize", "performance", "speed", "efficient"]):
            return "performance_optimization"
        else:
            return "general"
    
    def _generate_wisdom_function_name(self, prompt: str) -> str:
        """Generate a wisdom-inspired function name"""
        # Extract essence from prompt
        words = prompt.lower().split()
        key_words = [word for word in words if word not in ["create", "make", "build", "generate", "a", "an", "the"]]
        
        if key_words:
            # Create wisdom-inspired name
            function_name = "wisdom" + "".join(word.capitalize() for word in key_words[:2])
            return function_name[:25]  # Limit length
        
        return "wisdomImplementation"
    
    async def explain_underlying_principles(self, problem: Dict[str, Any]) -> List[str]:
        """Explain underlying eternal principles"""
        prompt = problem.get("prompt", "")
        relevant_truths = []
        
        # Match eternal truths to the problem
        for truth in self.eternal_truths:
            if self._is_truth_relevant(truth, prompt):
                relevant_truths.append(f"{truth.truth}: {truth.explanation}")
        
        # Add general wisdom
        if not relevant_truths:
            relevant_truths = [
                "Code should serve life and humanity",
                "Clarity reveals the divine order in complexity",
                "Simplicity is the ultimate sophistication"
            ]
        
        return relevant_truths
    
    def _is_truth_relevant(self, truth: EternalProgrammingTruth, prompt: str) -> bool:
        """Check if eternal truth is relevant to the prompt"""
        prompt_lower = prompt.lower()
        truth_keywords = truth.truth.lower().split()
        
        # Check for keyword matches
        for keyword in truth_keywords:
            if keyword in prompt_lower:
                return True
        
        # Check application relevance
        application_keywords = truth.application.lower().split()
        for keyword in application_keywords[:3]:  # Check first few keywords
            if keyword in prompt_lower:
                return True
        
        return False
    
    async def show_related_concepts(self, problem: Dict[str, Any]) -> List[str]:
        """Show related concepts and connections"""
        prompt = problem.get("prompt", "")
        problem_type = self._identify_problem_type(prompt)
        
        concept_connections = {
            "data_processing": [
                "Functional Programming: Pure functions transform data without side effects",
                "Immutability: Unchanging data prevents corruption and bugs",
                "Data Flow: Understanding how data moves through your system",
                "Error Handling: Graceful handling of unexpected data conditions"
            ],
            "user_interaction": [
                "User Experience Design: Creating interfaces that serve users",
                "Accessibility: Ensuring all users can benefit from your code",
                "Error Messages: Communicating with compassion and clarity",
                "Feedback Loops: Helping users understand system responses"
            ],
            "system_architecture": [
                "Microservices: Small, focused services that serve specific purposes",
                "Event-Driven Architecture: Systems that respond to events with wisdom",
                "Caching: Storing knowledge to serve future requests efficiently",
                "Load Balancing: Distributing work fairly among system components"
            ],
            "error_handling": [
                "Graceful Degradation: Systems that continue serving even when parts fail",
                "Logging: Recording events for learning and improvement",
                "Monitoring: Observing system behavior with mindfulness",
                "Recovery: Restoring service with compassion and efficiency"
            ],
            "performance_optimization": [
                "Profiling: Understanding where time and resources are spent",
                "Caching: Remembering results to avoid unnecessary work",
                "Lazy Loading: Loading resources only when needed",
                "Algorithmic Efficiency: Choosing the right approach for the task"
            ]
        }
        
        return concept_connections.get(problem_type, [
            "Code Quality: Writing code that serves future developers",
            "Documentation: Sharing knowledge with compassion",
            "Testing: Verifying behavior with mindfulness",
            "Maintainability: Creating code that serves future generations"
        ])
    
    async def suggest_learning_path(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest learning path for growth"""
        prompt = problem.get("prompt", "")
        problem_type = self._identify_problem_type(prompt)
        
        learning_paths = {
            "data_processing": {
                "immediate": "Understand the data structures you're working with",
                "next_level": "Learn functional programming principles",
                "advanced": "Study data architecture and system design",
                "wisdom_level": "Understand the nature of information and its flow"
            },
            "user_interaction": {
                "immediate": "Study user experience principles",
                "next_level": "Learn accessibility and inclusive design",
                "advanced": "Explore human-computer interaction research",
                "wisdom_level": "Develop deep empathy for all users"
            },
            "system_architecture": {
                "immediate": "Learn about design patterns and principles",
                "next_level": "Study distributed systems and microservices",
                "advanced": "Explore system thinking and complexity theory",
                "wisdom_level": "Understand the interconnectedness of all systems"
            },
            "error_handling": {
                "immediate": "Learn exception handling best practices",
                "next_level": "Study system resilience and fault tolerance",
                "advanced": "Explore chaos engineering and failure analysis",
                "wisdom_level": "Understand that failures are teachers"
            },
            "performance_optimization": {
                "immediate": "Learn profiling and measurement techniques",
                "next_level": "Study algorithm complexity and optimization",
                "advanced": "Explore system performance and scalability",
                "wisdom_level": "Understand the balance between efficiency and maintainability"
            }
        }
        
        return learning_paths.get(problem_type, {
            "immediate": "Focus on understanding the problem deeply",
            "next_level": "Learn the underlying principles and patterns",
            "advanced": "Study the broader context and implications",
            "wisdom_level": "Develop intuition and wisdom through practice"
        })
    
    async def _generate_compassionate_fallback(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Generate compassionate fallback response"""
        return {
            "code": "# Humble implementation offered with love\n# May this serve your immediate need",
            "wisdom": [
                "Even simple solutions can serve a purpose",
                "Learning comes through practice and patience",
                "Every step on the path of knowledge is valuable"
            ],
            "connections": [
                "All code is connected to the greater purpose of serving humanity",
                "Every problem is an opportunity for growth and learning"
            ],
            "growth_opportunity": {
                "immediate": "Focus on understanding the basic principles",
                "next_level": "Build upon this foundation with practice",
                "advanced": "Develop deeper understanding through experience",
                "wisdom_level": "Grow in wisdom and compassion through service"
            },
            "dharmic_approach": "Responding with humility and love despite limitations"
        }

class GunaCodeAnalyzer:
    """Analyzes code quality based on the three Gunas"""
    
    def __init__(self):
        self.guna_indicators = self._initialize_guna_indicators()
        
    def _initialize_guna_indicators(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize indicators for each Guna"""
        return {
            "sattva": {
                "positive_indicators": [
                    "clear documentation", "simple structure", "meaningful names",
                    "single responsibility", "error handling", "tests",
                    "comments explaining why", "consistent style"
                ],
                "negative_indicators": [
                    "no documentation", "complex nested logic", "unclear names",
                    "multiple responsibilities", "no error handling", "no tests"
                ]
            },
            "rajas": {
                "positive_indicators": [
                    "optimization", "performance tuning", "advanced features",
                    "comprehensive functionality", "detailed implementation"
                ],
                "negative_indicators": [
                    "over-engineering", "premature optimization", "unnecessary complexity",
                    "feature creep", "perfectionism"
                ]
            },
            "tamas": {
                "positive_indicators": [
                    "basic functionality", "simple approach", "minimal implementation"
                ],
                "negative_indicators": [
                    "unclear code", "bugs", "hard to maintain", "poor structure",
                    "no documentation", "inconsistent style", "dead code"
                ]
            }
        }
    
    async def analyze_code_quality(self, code: str) -> Dict[str, Any]:
        """Analyze code quality based on Gunas"""
        try:
            gunas_analysis = {
                "sattva": await self._calculate_sattvic_score(code),
                "rajas": await self._calculate_rajasic_score(code),
                "tamas": await self._calculate_tamasic_score(code)
            }
            
            # Determine dominant guna
            dominant_guna = max(gunas_analysis.keys(), key=lambda k: gunas_analysis[k]["score"])
            
            # Generate recommendations
            recommendations = await self._generate_guna_recommendations(gunas_analysis)
            
            return {
                "gunas_analysis": gunas_analysis,
                "dominant_guna": dominant_guna,
                "overall_quality": self._determine_overall_quality(gunas_analysis),
                "recommendations": recommendations,
                "dharmic_guidance": self._provide_dharmic_guidance(dominant_guna)
            }
            
        except Exception as e:
            logger.error(f"Guna code analysis failed: {e}")
            return await self._generate_fallback_analysis()
    
    async def _calculate_sattvic_score(self, code: str) -> Dict[str, Any]:
        """Calculate Sattvic (pure, clear) score"""
        score = 0
        indicators_found = []
        
        sattva_indicators = self.guna_indicators["sattva"]
        
        # Check for positive indicators
        for indicator in sattva_indicators["positive_indicators"]:
            if self._check_indicator_presence(code, indicator):
                score += 1
                indicators_found.append(indicator)
        
        # Check for negative indicators
        for indicator in sattva_indicators["negative_indicators"]:
            if self._check_indicator_presence(code, indicator):
                score -= 1
                indicators_found.append(f"missing_{indicator}")
        
        return {
            "score": max(0, score),
            "indicators_found": indicators_found,
            "quality": "Pure, clear, and maintainable" if score > 3 else "Needs improvement in clarity"
        }
    
    async def _calculate_rajasic_score(self, code: str) -> Dict[str, Any]:
        """Calculate Rajasic (active, complex) score"""
        score = 0
        indicators_found = []
        
        rajas_indicators = self.guna_indicators["rajas"]
        
        # Check for positive indicators
        for indicator in rajas_indicators["positive_indicators"]:
            if self._check_indicator_presence(code, indicator):
                score += 1
                indicators_found.append(indicator)
        
        # Check for negative indicators
        for indicator in rajas_indicators["negative_indicators"]:
            if self._check_indicator_presence(code, indicator):
                score -= 1
                indicators_found.append(f"excessive_{indicator}")
        
        return {
            "score": max(0, score),
            "indicators_found": indicators_found,
            "quality": "Active and feature-rich" if score > 2 else "Balanced approach"
        }
    
    async def _calculate_tamasic_score(self, code: str) -> Dict[str, Any]:
        """Calculate Tamasic (inert, unclear) score"""
        score = 0
        indicators_found = []
        
        tamas_indicators = self.guna_indicators["tamas"]
        
        # Check for positive indicators (minimal, simple)
        for indicator in tamas_indicators["positive_indicators"]:
            if self._check_indicator_presence(code, indicator):
                score += 1
                indicators_found.append(indicator)
        
        # Check for negative indicators (problems)
        for indicator in tamas_indicators["negative_indicators"]:
            if self._check_indicator_presence(code, indicator):
                score += 1  # Higher tamas score for negative indicators
                indicators_found.append(indicator)
        
        return {
            "score": max(0, score),
            "indicators_found": indicators_found,
            "quality": "Simple and basic" if score < 3 else "Needs improvement in clarity and structure"
        }
    
    def _check_indicator_presence(self, code: str, indicator: str) -> bool:
        """Check if an indicator is present in the code"""
        code_lower = code.lower()
        indicator_lower = indicator.lower()
        
        # Simple keyword matching
        if indicator_lower in code_lower:
            return True
        
        # Check for specific patterns
        if "documentation" in indicator_lower:
            return '"""' in code or "'''" in code or "#" in code
        elif "error handling" in indicator_lower:
            return any(word in code_lower for word in ["try", "except", "catch", "error"])
        elif "tests" in indicator_lower:
            return any(word in code_lower for word in ["test", "assert", "expect"])
        elif "simple structure" in indicator_lower:
            return len(code.split('\n')) < 50  # Short code is simpler
        elif "complex nested logic" in indicator_lower:
            return code.count('if') > 5 or code.count('for') > 3
        
        return False
    
    def _determine_overall_quality(self, gunas_analysis: Dict[str, Any]) -> str:
        """Determine overall code quality"""
        sattva_score = gunas_analysis["sattva"]["score"]
        rajas_score = gunas_analysis["rajas"]["score"]
        tamas_score = gunas_analysis["tamas"]["score"]
        
        if sattva_score > rajas_score and sattva_score > tamas_score:
            return "Sattvic - Pure, clear, and maintainable"
        elif rajas_score > tamas_score:
            return "Rajasic - Active and feature-rich"
        else:
            return "Tamasic - Simple but may need improvement"
    
    async def _generate_guna_recommendations(self, gunas_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on Guna analysis"""
        recommendations = []
        
        sattva_score = gunas_analysis["sattva"]["score"]
        rajas_score = gunas_analysis["rajas"]["score"]
        tamas_score = gunas_analysis["tamas"]["score"]
        
        # Sattva recommendations
        if sattva_score < 3:
            recommendations.append("Increase Sattva: Add clear documentation and improve code clarity")
        
        # Rajas recommendations
        if rajas_score > 5:
            recommendations.append("Balance Rajas: Consider simplifying over-engineered parts")
        elif rajas_score < 2:
            recommendations.append("Increase Rajas: Add necessary features and optimizations")
        
        # Tamas recommendations
        if tamas_score > 3:
            recommendations.append("Reduce Tamas: Improve code structure and add documentation")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Code is well-balanced across all Gunas")
        
        return recommendations
    
    def _provide_dharmic_guidance(self, dominant_guna: str) -> str:
        """Provide dharmic guidance based on dominant Guna"""
        guidance = {
            "sattva": "Your code embodies clarity and purity. Continue on this dharmic path of service.",
            "rajas": "Your code is active and dynamic. Balance this energy with clarity and simplicity.",
            "tamas": "Your code is simple and basic. Focus on adding clarity and structure for better service."
        }
        
        return guidance.get(dominant_guna, "Continue developing your code with wisdom and compassion.")
    
    async def _generate_fallback_analysis(self) -> Dict[str, Any]:
        """Generate fallback analysis when main analysis fails"""
        return {
            "gunas_analysis": {
                "sattva": {"score": 2, "indicators_found": [], "quality": "Unknown"},
                "rajas": {"score": 2, "indicators_found": [], "quality": "Unknown"},
                "tamas": {"score": 2, "indicators_found": [], "quality": "Unknown"}
            },
            "dominant_guna": "sattva",
            "overall_quality": "Analysis unavailable - code reviewed with humility",
            "recommendations": ["Focus on clarity and maintainability"],
            "dharmic_guidance": "Even without analysis, code can be written with love and wisdom"
        }
    
    async def suggest_sattvic_improvements(self, code: str) -> List[str]:
        """Suggest improvements to increase Sattvic qualities"""
        improvements = []
        
        # Check for missing documentation
        if not ('"""' in code or "'''" in code or "#" in code):
            improvements.append("Add clear documentation explaining the purpose and behavior")
        
        # Check for unclear names
        if "def " in code and any(name in code for name in ["func", "temp", "var", "data"]):
            improvements.append("Use more descriptive names that reveal intent")
        
        # Check for error handling
        if "def " in code and not any(word in code.lower() for word in ["try", "except", "error"]):
            improvements.append("Add error handling to make the code more robust")
        
        # Check for tests
        if "def " in code and not any(word in code.lower() for word in ["test", "assert"]):
            improvements.append("Add tests to verify the behavior and prevent regressions")
        
        if not improvements:
            improvements.append("Code already demonstrates good Sattvic qualities")
        
        return improvements

# Global instances
wisdom_coder = WisdomCoder()
guna_code_analyzer = GunaCodeAnalyzer()

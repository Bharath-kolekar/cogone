"""
Pattern Analyzer for Smart Coding AI Service
Preserves pattern matching and recognition capabilities
"""

from typing import Dict, Any, List
import re
import structlog

logger = structlog.get_logger()


class PatternMatcher:
    """
    Advanced pattern matcher
    Matches code patterns for intelligent suggestions
    """
    
    def __init__(self):
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[str, Dict[str, str]]:
        """Initialize language-specific patterns"""
        return {
            "python": {
                "function_def": r"def\s+\w+\s*\(",
                "class_def": r"class\s+\w+",
                "import_stmt": r"import\s+\w+",
                "from_import": r"from\s+\w+\s+import",
                "list_comp": r"\[.*for.*in.*\]",
                "dict_comp": r"\{.*for.*in.*\}",
                "decorator": r"@\w+",
                "async_def": r"async\s+def",
                "with_stmt": r"with\s+.*:",
                "try_except": r"try\s*:",
            },
            "javascript": {
                "function_def": r"function\s+\w+\s*\(",
                "arrow_func": r"const\s+\w+\s*=\s*\(.*\)\s*=>",
                "class_def": r"class\s+\w+",
                "import_stmt": r"import\s+.*from",
                "async_func": r"async\s+function",
                "promise": r"new\s+Promise",
                "await_expr": r"await\s+",
                "export_stmt": r"export\s+(default\s+)?",
            },
            "typescript": {
                "interface": r"interface\s+\w+",
                "type_alias": r"type\s+\w+\s*=",
                "enum_def": r"enum\s+\w+",
                "generic": r"<\w+(\s*,\s*\w+)*>",
                "decorator": r"@\w+",
            }
        }
    
    async def match(self, text: str, language: str) -> List[Dict[str, Any]]:
        """
        Match patterns in text
        Supports pattern-based accuracy improvement
        """
        try:
            matches = []
            patterns = self.patterns.get(language, {})
            
            for pattern_name, pattern_regex in patterns.items():
                if re.search(pattern_regex, text):
                    matches.append({
                        "pattern": pattern_name,
                        "confidence": 0.9,  # High confidence for matched patterns
                        "suggestion_type": self._get_suggestion_type(pattern_name)
                    })
            
            return matches
            
        except Exception as e:
            logger.error("Pattern matching failed", error=str(e))
            return []
    
    def _get_suggestion_type(self, pattern_name: str) -> str:
        """Get suggestion type from pattern name"""
        if "function" in pattern_name or "func" in pattern_name:
            return "function"
        elif "class" in pattern_name:
            return "class"
        elif "import" in pattern_name:
            return "import"
        elif "interface" in pattern_name or "type" in pattern_name:
            return "type"
        else:
            return "code"


class PatternRecognizer:
    """
    Pattern recognizer
    Recognizes complex code patterns
    """
    
    async def recognize(self, text: str) -> List[Dict[str, Any]]:
        """
        Recognize patterns in code
        Enhances pattern-based suggestions
        """
        try:
            patterns = []
            
            # Recognize common patterns
            if "for" in text and "in" in text:
                patterns.append({
                    "pattern": "iteration",
                    "type": "loop",
                    "confidence": 0.85
                })
            
            if "if" in text:
                patterns.append({
                    "pattern": "conditional",
                    "type": "control_flow",
                    "confidence": 0.9
                })
            
            if "try" in text and "except" in text:
                patterns.append({
                    "pattern": "error_handling",
                    "type": "exception",
                    "confidence": 0.95
                })
            
            if "async" in text or "await" in text:
                patterns.append({
                    "pattern": "asynchronous",
                    "type": "async",
                    "confidence": 0.92
                })
            
            # Design patterns
            if "singleton" in text.lower():
                patterns.append({
                    "pattern": "singleton",
                    "type": "design_pattern",
                    "confidence": 0.88
                })
            
            if "factory" in text.lower():
                patterns.append({
                    "pattern": "factory",
                    "type": "design_pattern",
                    "confidence": 0.87
                })
            
            if "observer" in text.lower():
                patterns.append({
                    "pattern": "observer",
                    "type": "design_pattern",
                    "confidence": 0.86
                })
            
            return patterns
            
        except Exception as e:
            logger.error("Pattern recognition failed", error=str(e))
            return []

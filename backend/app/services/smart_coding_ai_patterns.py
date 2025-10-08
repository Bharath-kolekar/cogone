"""
Smart Coding AI Core - CodingPatternRecognizer
Extracted from smart_coding_ai_optimized.py
"""

import structlog
from typing import Dict, List, Optional, Any, Set, Tuple
from datetime import datetime
import ast
import os
from pathlib import Path

logger = structlog.get_logger()


class CodingPatternRecognizer:
    """Recognizes and stores coding patterns"""
    
    def __init__(self):
        self.pattern_cache: Dict[str, List[Dict]] = {}
        self.pattern_frequency: Dict[str, int] = {}
    
    async def analyze_file_patterns(self, file_path: str, content: str, language: str) -> List[Dict]:
        """Analyze coding patterns in a file"""
        try:
            patterns = []
            lines = content.split('\n')
            
            # Function patterns
            function_patterns = await self._extract_functions(content, language)
            patterns.extend(function_patterns)
            
            # Class patterns
            class_patterns = await self._extract_classes(content, language)
            patterns.extend(class_patterns)
            
            # Import patterns
            import_patterns = await self._extract_imports(content, language)
            patterns.extend(import_patterns)
            
            # Variable patterns
            variable_patterns = await self._extract_variables(content, language)
            patterns.extend(variable_patterns)
            
            # Update frequency tracking
            for pattern in patterns:
                pattern_key = f"{pattern['pattern_type']}:{pattern['pattern_name']}"
                self.pattern_frequency[pattern_key] = self.pattern_frequency.get(pattern_key, 0) + 1
                pattern['frequency'] = self.pattern_frequency[pattern_key]
            
            return patterns
            
        except Exception as e:
            logger.error(f"Failed to analyze patterns in {file_path}: {e}")
            return []
    
    async def _extract_functions(self, content: str, language: str) -> List[Dict]:
        """Extract function patterns"""
        patterns = []
        lines = content.split('\n')
        
        if language == "python":
            for i, line in enumerate(lines):
                # Function definitions
                if re.match(r'^\s*def\s+\w+', line):
                    match = re.search(r'def\s+(\w+)', line)
                    if match:
                        patterns.append({
                            "pattern_id": str(uuid.uuid4()),
                            "pattern_type": "function",
                            "pattern_name": match.group(1),
                            "pattern_code": line.strip(),
                            "language": language,
                            "line_number": i + 1,
                            "context": self._get_context(lines, i, 3),
                            "complexity": await self._calculate_complexity(line),
                            "dependencies": [],
                            "related_patterns": []
                        })
                
                # Async functions
                elif re.match(r'^\s*async\s+def\s+\w+', line):
                    match = re.search(r'async\s+def\s+(\w+)', line)
                    if match:
                        patterns.append({
                            "pattern_id": str(uuid.uuid4()),
                            "pattern_type": "async_function",
                            "pattern_name": match.group(1),
                            "pattern_code": line.strip(),
                            "language": language,
                            "line_number": i + 1,
                            "context": self._get_context(lines, i, 3),
                            "complexity": await self._calculate_complexity(line),
                            "dependencies": [],
                            "related_patterns": []
                        })
        
        elif language in ["javascript", "typescript"]:
            for i, line in enumerate(lines):
                # Function declarations
                if re.match(r'^\s*function\s+\w+', line):
                    match = re.search(r'function\s+(\w+)', line)
                    if match:
                        patterns.append({
                            "pattern_id": str(uuid.uuid4()),
                            "pattern_type": "function",
                            "pattern_name": match.group(1),
                            "pattern_code": line.strip(),
                            "language": language,
                            "line_number": i + 1,
                            "context": self._get_context(lines, i, 3),
                            "complexity": await self._calculate_complexity(line),
                            "dependencies": [],
                            "related_patterns": []
                        })
                
                # Arrow functions
                elif re.search(r'const\s+(\w+)\s*=\s*\(', line):
                    match = re.search(r'const\s+(\w+)\s*=', line)
                    if match:
                        patterns.append({
                            "pattern_id": str(uuid.uuid4()),
                            "pattern_type": "arrow_function",
                            "pattern_name": match.group(1),
                            "pattern_code": line.strip(),
                            "language": language,
                            "line_number": i + 1,
                            "context": self._get_context(lines, i, 3),
                            "complexity": await self._calculate_complexity(line),
                            "dependencies": [],
                            "related_patterns": []
                        })
        
        return patterns
    
    async def _extract_classes(self, content: str, language: str) -> List[Dict]:
        """Extract class patterns"""
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if language == "python" and re.match(r'^\s*class\s+\w+', line):
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    patterns.append({
                        "pattern_id": str(uuid.uuid4()),
                        "pattern_type": "class",
                        "pattern_name": match.group(1),
                        "pattern_code": line.strip(),
                        "language": language,
                        "line_number": i + 1,
                        "context": self._get_context(lines, i, 3),
                        "complexity": await self._calculate_complexity(line),
                        "dependencies": [],
                        "related_patterns": []
                    })
            
            elif language in ["javascript", "typescript"] and re.match(r'^\s*class\s+\w+', line):
                match = re.search(r'class\s+(\w+)', line)
                if match:
                    patterns.append({
                        "pattern_id": str(uuid.uuid4()),
                        "pattern_type": "class",
                        "pattern_name": match.group(1),
                        "pattern_code": line.strip(),
                        "language": language,
                        "line_number": i + 1,
                        "context": self._get_context(lines, i, 3),
                        "complexity": await self._calculate_complexity(line),
                        "dependencies": [],
                        "related_patterns": []
                    })
        
        return patterns
    
    async def _extract_imports(self, content: str, language: str) -> List[Dict]:
        """Extract import patterns"""
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if language == "python" and (line.strip().startswith('import ') or line.strip().startswith('from ')):
                patterns.append({
                    "pattern_id": str(uuid.uuid4()),
                    "pattern_type": "import",
                    "pattern_name": line.strip(),
                    "pattern_code": line.strip(),
                    "language": language,
                    "line_number": i + 1,
                    "context": self._get_context(lines, i, 1),
                    "complexity": 0.1,
                    "dependencies": [line.strip()],
                    "related_patterns": []
                })
            
            elif language in ["javascript", "typescript"] and line.strip().startswith('import '):
                patterns.append({
                    "pattern_id": str(uuid.uuid4()),
                    "pattern_type": "import",
                    "pattern_name": line.strip(),
                    "pattern_code": line.strip(),
                    "language": language,
                    "line_number": i + 1,
                    "context": self._get_context(lines, i, 1),
                    "complexity": 0.1,
                    "dependencies": [line.strip()],
                    "related_patterns": []
                })
        
        return patterns
    
    async def _extract_variables(self, content: str, language: str) -> List[Dict]:
        """Extract variable patterns"""
        patterns = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            if language == "python" and re.search(r'^\s*\w+\s*=', line):
                match = re.search(r'(\w+)\s*=', line)
                if match:
                    patterns.append({
                        "pattern_id": str(uuid.uuid4()),
                        "pattern_type": "variable",
                        "pattern_name": match.group(1),
                        "pattern_code": line.strip(),
                        "language": language,
                        "line_number": i + 1,
                        "context": self._get_context(lines, i, 1),
                        "complexity": 0.2,
                        "dependencies": [],
                        "related_patterns": []
                    })
            
            elif language in ["javascript", "typescript"] and re.search(r'^\s*(?:const|let|var)\s+\w+', line):
                match = re.search(r'(?:const|let|var)\s+(\w+)', line)
                if match:
                    patterns.append({
                        "pattern_id": str(uuid.uuid4()),
                        "pattern_type": "variable",
                        "pattern_name": match.group(1),
                        "pattern_code": line.strip(),
                        "language": language,
                        "line_number": i + 1,
                        "context": self._get_context(lines, i, 1),
                        "complexity": 0.2,
                        "dependencies": [],
                        "related_patterns": []
                    })
        
        return patterns
    
    def _get_context(self, lines: List[str], line_index: int, context_size: int = 3) -> str:
        """Get surrounding context for a line"""
        start = max(0, line_index - context_size)
        end = min(len(lines), line_index + context_size + 1)
        return '\n'.join(lines[start:end])
    
    async def _calculate_complexity(self, line: str) -> float:
        """Calculate complexity score for a pattern"""
        complexity = 0.1  # Base complexity
        
        # Add complexity based on features
        if 'async' in line:
            complexity += 0.2
        if 'await' in line:
            complexity += 0.2
        if 'yield' in line:
            complexity += 0.2
        if '(' in line and ')' in line:
            complexity += 0.1
        if '{' in line and '}' in line:
            complexity += 0.1
        
        return min(complexity, 1.0)




__all__ = ['CodingPatternRecognizer']

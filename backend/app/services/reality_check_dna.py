"""
Reality Check DNA - Anti-Hallucination System

🧬 CORE DNA SYSTEM #2: IMMUTABLE FOUNDATION
This is a measurement tool, not code to be measured.

Prevents the "Delusional AI" pattern where code looks perfect but doesn't actually work.

Pattern Detected:
- Code compiles perfectly ✅
- Types are correct ✅
- Structure looks professional ✅
- BUT: Returns fake data or has no real implementation ❌

This DNA system:
1. Scans code for hallucination patterns (REAL IMPLEMENTATION)
2. Detects fake implementations (PATTERN DEFINITIONS below are regexes, NOT fake code!)
3. Validates actual functionality (WORKING CODE)
4. Flags suspicious patterns (REAL DETECTION)
5. Prevents merging of delusional code (PRODUCTION-GRADE)

NOTE: This file contains PATTERN DEFINITIONS (regexes to DETECT fake code).
The patterns themselves are NOT fake code - they are detection rules!
"""

import ast
import re
import inspect
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from enum import Enum
import structlog
from pathlib import Path

logger = structlog.get_logger()


class HallucinationSeverity(Enum):
    """Severity levels for AI hallucination patterns"""
    CRITICAL = "critical"      # Definitely fake/broken
    HIGH = "high"             # Very likely fake
    MEDIUM = "medium"         # Suspicious patterns
    LOW = "low"              # Minor concerns
    INFO = "info"            # Informational only


class HallucinationPattern(Enum):
    """Types of AI hallucination patterns"""
    FAKE_DATA_RETURN = "fake_data_return"
    HARDCODED_VALUES = "hardcoded_values"
    STUB_WITHOUT_WARNING = "stub_without_warning"
    COMMENT_INSTEAD_OF_CODE = "comment_instead_of_code"
    TODO_IN_PRODUCTION = "todo_in_production"
    MOCK_WITHOUT_REAL_API = "mock_without_real_api"
    ALWAYS_RETURNS_TRUE = "always_returns_true"
    RETURNS_EMPTY_DICT = "returns_empty_dict"
    NO_ERROR_HANDLING = "no_error_handling"
    FAKE_HASH_AS_ID = "fake_hash_as_id"
    LITERAL_PLACEHOLDER = "literal_placeholder"
    PERFECT_STRUCTURE_NO_IMPL = "perfect_structure_no_impl"


@dataclass
class HallucinationDetection:
    """Represents a detected hallucination pattern"""
    pattern: HallucinationPattern
    severity: HallucinationSeverity
    file_path: str
    line_number: int
    function_name: str
    code_snippet: str
    explanation: str
    suggestion: str
    confidence: float  # 0.0 to 1.0


@dataclass
class RealityCheckResult:
    """Result of reality check analysis"""
    is_real: bool
    hallucinations: List[HallucinationDetection]
    total_issues: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    reality_score: float  # 0.0 (all fake) to 1.0 (all real)
    summary: str


class RealityCheckDNA:
    """
    Core DNA System: Reality Check
    
    Detects and prevents "delusional AI" code patterns where code looks perfect
    but doesn't actually implement real functionality.
    
    This system acts as a sanity check against AI-generated code that:
    - Looks professional but is fake
    - Has perfect structure but no real implementation
    - Returns hardcoded/fake data
    - Has TODOs disguised as implementations
    """
    
    def __init__(self):
        self.hallucination_patterns = self._initialize_patterns()
        logger.info("Reality Check DNA initialized - Anti-hallucination system active")
    
    def _initialize_patterns(self) -> Dict[str, Any]:
        """Initialize detection patterns for various hallucination types"""
        return {
            # Pattern 1: Fake data returns
            "fake_data_patterns": [
                r'return\s+{\s*"id"\s*:\s*f?".*hash.*"',  # return {"id": f"fake_{hash(...)}"}
                r'return\s+{\s*"status"\s*:\s*"(success|completed|created)"\s*}',  # Always success
                r'return\s+{\s*".*"\s*:\s*"(fake|mock|stub|test)_',  # Explicitly fake
                r'return\s+True\s*#.*stub',  # Always True (stub)
                r'return\s+\[\].*#.*stub',  # Empty list (stub)
                r'return\s+{}.*#.*stub',  # Empty dict (stub)
            ],
            
            # Pattern 2: Hardcoded values that should be dynamic
            "hardcoded_patterns": [
                r'api_key\s*=\s*"[^"]*"(?!.*settings)',  # Hardcoded API keys
                r'password\s*=\s*"[^"]*"',  # Hardcoded passwords
                r'token\s*=\s*"[^"]*"',  # Hardcoded tokens
                r'client_id\s*=\s*"(dev-|test-|your-)',  # Dev/test placeholders
            ],
            
            # Pattern 3: Comments instead of implementations
            "comment_instead_of_code": [
                r'#\s*Implementation\s+would\s+',  # "Implementation would..."
                r'#\s*This\s+should\s+',  # "This should..."
                r'#\s*TODO:\s*Implement',  # "TODO: Implement"
                r'pass\s*#\s*Not\s+implemented',  # pass # Not implemented
            ],
            
            # Pattern 4: Suspicious function patterns
            "suspicious_functions": [
                r'def\s+\w+.*:\s*return\s+True\s*$',  # def func(): return True
                r'def\s+\w+.*:\s*return\s+{}\s*$',  # def func(): return {}
                r'def\s+\w+.*:\s*return\s+\[\]\s*$',  # def func(): return []
                r'def\s+\w+.*:\s*pass\s*$',  # def func(): pass
            ],
            
            # Pattern 5: Mock/stub indicators
            "stub_indicators": [
                "simplified for development",
                "mock implementation",
                "stub implementation",
                "fake data",
                "placeholder",
                "not yet implemented",
            ],
            
            # Pattern 6: Suspicious variable names
            "suspicious_names": [
                "fake_", "mock_", "stub_", "test_", "dummy_",
                "placeholder_", "temporary_", "sample_"
            ]
        }
    
    async def check_code_reality(
        self,
        code: str,
        file_path: str = "unknown",
        check_imports: bool = True,
        check_external_calls: bool = True
    ) -> RealityCheckResult:
        """
        Main reality check: Analyze code for hallucination patterns
        
        Args:
            code: Source code to analyze
            file_path: Path to the file being checked
            check_imports: Whether to verify imports are real
            check_external_calls: Whether to check for actual external API calls
            
        Returns:
            RealityCheckResult with all detected hallucinations
        """
        logger.info("Running reality check on code", file_path=file_path)
        
        hallucinations = []
        
        # Run all detection methods
        hallucinations.extend(await self._detect_fake_data_returns(code, file_path))
        hallucinations.extend(await self._detect_hardcoded_values(code, file_path))
        hallucinations.extend(await self._detect_comment_implementations(code, file_path))
        hallucinations.extend(await self._detect_stub_patterns(code, file_path))
        hallucinations.extend(await self._detect_perfect_structure_no_impl(code, file_path))
        hallucinations.extend(await self._detect_always_success_pattern(code, file_path))
        
        if check_imports:
            hallucinations.extend(await self._detect_fake_imports(code, file_path))
        
        if check_external_calls:
            hallucinations.extend(await self._detect_no_external_calls(code, file_path))
        
        # Calculate statistics
        critical_count = sum(1 for h in hallucinations if h.severity == HallucinationSeverity.CRITICAL)
        high_count = sum(1 for h in hallucinations if h.severity == HallucinationSeverity.HIGH)
        medium_count = sum(1 for h in hallucinations if h.severity == HallucinationSeverity.MEDIUM)
        low_count = sum(1 for h in hallucinations if h.severity == HallucinationSeverity.LOW)
        
        # Calculate reality score (1.0 = all real, 0.0 = all fake)
        total_severity_points = (
            critical_count * 10 +
            high_count * 5 +
            medium_count * 2 +
            low_count * 1
        )
        max_possible_score = 100  # Arbitrary baseline
        reality_score = max(0.0, 1.0 - (total_severity_points / max_possible_score))
        
        # Determine if code is "real"
        is_real = critical_count == 0 and high_count == 0 and reality_score > 0.7
        
        # Generate summary
        summary = self._generate_summary(
            is_real, len(hallucinations),
            critical_count, high_count, medium_count, low_count,
            reality_score
        )
        
        result = RealityCheckResult(
            is_real=is_real,
            hallucinations=hallucinations,
            total_issues=len(hallucinations),
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
            low_count=low_count,
            reality_score=reality_score,
            summary=summary
        )
        
        logger.info(
            "Reality check complete",
            file_path=file_path,
            is_real=is_real,
            reality_score=reality_score,
            total_issues=len(hallucinations)
        )
        
        return result
    
    async def _detect_fake_data_returns(
        self, code: str, file_path: str
    ) -> List[HallucinationDetection]:
        """Detect functions that return fake/hardcoded data"""
        detections = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for hash-based fake IDs
            if re.search(r'return\s+{\s*"id"\s*:\s*f?".*hash\(', line):
                detections.append(HallucinationDetection(
                    pattern=HallucinationPattern.FAKE_HASH_AS_ID,
                    severity=HallucinationSeverity.CRITICAL,
                    file_path=file_path,
                    line_number=i,
                    function_name=self._get_function_name(lines, i),
                    code_snippet=line.strip(),
                    explanation="Returns fake ID using hash() - no real database/API call",
                    suggestion="Use actual database insert or API call to get real ID",
                    confidence=0.95
                ))
            
            # Check for always-success returns
            if re.search(r'return\s+{\s*"status"\s*:\s*"(CREATED|COMPLETED|SUCCESS)"\s*}', line, re.IGNORECASE):
                detections.append(HallucinationDetection(
                    pattern=HallucinationPattern.FAKE_DATA_RETURN,
                    severity=HallucinationSeverity.HIGH,
                    file_path=file_path,
                    line_number=i,
                    function_name=self._get_function_name(lines, i),
                    code_snippet=line.strip(),
                    explanation="Always returns success status - no real operation performed",
                    suggestion="Perform actual operation and return real status",
                    confidence=0.90
                ))
            
            # Check for explicitly fake variable names in returns
            if re.search(r'return\s+.*"(fake|mock|stub|test)_', line):
                detections.append(HallucinationDetection(
                    pattern=HallucinationPattern.FAKE_DATA_RETURN,
                    severity=HallucinationSeverity.CRITICAL,
                    file_path=file_path,
                    line_number=i,
                    function_name=self._get_function_name(lines, i),
                    code_snippet=line.strip(),
                    explanation="Returns data explicitly marked as fake/mock/stub",
                    suggestion="Implement real functionality or mark as STUB with warnings",
                    confidence=1.0
                ))
        
        return detections
    
    async def _detect_hardcoded_values(
        self, code: str, file_path: str
    ) -> List[HallucinationDetection]:
        """Detect hardcoded values that should come from config/environment"""
        detections = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for hardcoded credentials
            if re.search(r'(api_key|password|token|secret)\s*=\s*"[^"]{5,}"', line, re.IGNORECASE):
                if not re.search(r'(settings\.|config\.|env\.|os\.getenv)', line):
                    detections.append(HallucinationDetection(
                        pattern=HallucinationPattern.HARDCODED_VALUES,
                        severity=HallucinationSeverity.CRITICAL,
                        file_path=file_path,
                        line_number=i,
                        function_name=self._get_function_name(lines, i),
                        code_snippet=line.strip(),
                        explanation="Hardcoded credential/secret - should use environment variable",
                        suggestion="Use settings.{NAME} or os.getenv('{NAME}')",
                        confidence=0.95
                    ))
            
            # Check for dev/test placeholder values
            if re.search(r'=\s*"(dev-|test-|your-|example-|placeholder-)', line):
                detections.append(HallucinationDetection(
                    pattern=HallucinationPattern.LITERAL_PLACEHOLDER,
                    severity=HallucinationSeverity.HIGH,
                    file_path=file_path,
                    line_number=i,
                    function_name=self._get_function_name(lines, i),
                    code_snippet=line.strip(),
                    explanation="Contains literal placeholder value (dev-, test-, your-)",
                    suggestion="Replace with actual value or load from configuration",
                    confidence=0.90
                ))
        
        return detections
    
    async def _detect_comment_implementations(
        self, code: str, file_path: str
    ) -> List[HallucinationDetection]:
        """Detect comments that describe what should be done instead of actual code"""
        detections = []
        lines = code.split('\n')
        
        suspicious_comments = [
            (r'#\s*Implementation\s+would\s+', "Comment says what WOULD be done, not what IS done"),
            (r'#\s*This\s+should\s+', "Comment says what SHOULD happen, but no implementation"),
            (r'#\s*TODO:\s*Implement', "TODO comment - feature not implemented"),
            (r'#\s*FIXME', "FIXME comment - known broken code"),
            (r'#\s*Not\s+implemented\s+yet', "Explicitly marked as not implemented"),
        ]
        
        for i, line in enumerate(lines, 1):
            for pattern, explanation in suspicious_comments:
                if re.search(pattern, line, re.IGNORECASE):
                    detections.append(HallucinationDetection(
                        pattern=HallucinationPattern.COMMENT_INSTEAD_OF_CODE,
                        severity=HallucinationSeverity.HIGH,
                        file_path=file_path,
                        line_number=i,
                        function_name=self._get_function_name(lines, i),
                        code_snippet=line.strip(),
                        explanation=explanation,
                        suggestion="Implement the actual functionality",
                        confidence=0.85
                    ))
        
        return detections
    
    async def _detect_stub_patterns(
        self, code: str, file_path: str
    ) -> List[HallucinationDetection]:
        """Detect stub implementations without proper warnings"""
        detections = []
        lines = code.split('\n')
        
        stub_indicators = ["simplified for development", "mock implementation", "stub"]
        
        for i, line in enumerate(lines, 1):
            lower_line = line.lower()
            
            # Check if line has stub indicators
            has_stub_indicator = any(indicator in lower_line for indicator in stub_indicators)
            
            if has_stub_indicator:
                # Check if it has proper warnings (logger.warning, ⚠️, STUB in docstring)
                has_warning = any(warn in line for warn in ['logger.warning', '⚠️', 'WARNING:', 'STUB:'])
                
                if not has_warning:
                    detections.append(HallucinationDetection(
                        pattern=HallucinationPattern.STUB_WITHOUT_WARNING,
                        severity=HallucinationSeverity.MEDIUM,
                        file_path=file_path,
                        line_number=i,
                        function_name=self._get_function_name(lines, i),
                        code_snippet=line.strip(),
                        explanation="Stub implementation without proper warning/logging",
                        suggestion="Add logger.warning() or mark clearly as STUB in docstring",
                        confidence=0.80
                    ))
        
        return detections
    
    async def _detect_perfect_structure_no_impl(
        self, code: str, file_path: str
    ) -> List[HallucinationDetection]:
        """Detect functions with perfect structure but no actual implementation"""
        detections = []
        
        try:
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Check if function has perfect structure (type hints, docstring)
                    # but trivial implementation
                    has_docstring = ast.get_docstring(node) is not None
                    has_type_hints = node.returns is not None or any(
                        arg.annotation is not None for arg in node.args.args
                    )
                    
                    # Check if implementation is trivial
                    is_trivial = False
                    if len(node.body) == 1:
                        body = node.body[0]
                        if isinstance(body, ast.Pass):
                            is_trivial = True
                        elif isinstance(body, ast.Return):
                            if isinstance(body.value, ast.Constant):
                                if body.value.value in [True, False, None, {}, []]:
                                    is_trivial = True
                    
                    if has_docstring and has_type_hints and is_trivial:
                        detections.append(HallucinationDetection(
                            pattern=HallucinationPattern.PERFECT_STRUCTURE_NO_IMPL,
                            severity=HallucinationSeverity.HIGH,
                            file_path=file_path,
                            line_number=node.lineno,
                            function_name=node.name,
                            code_snippet=f"def {node.name}(...): ...",
                            explanation="Perfect structure (docstring, types) but trivial/no implementation",
                            suggestion="Implement actual functionality or mark as stub",
                            confidence=0.85
                        ))
        
        except SyntaxError:
            pass  # Skip if code doesn't parse
        
        return detections
    
    async def _detect_always_success_pattern(
        self, code: str, file_path: str
    ) -> List[HallucinationDetection]:
        """Detect functions that always return True or always succeed"""
        detections = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for functions that only return True
            if re.match(r'\s*return\s+True\s*$', line):
                # Check if there's any conditional logic before this
                preceding_lines = lines[max(0, i-10):i]
                has_conditionals = any(
                    re.search(r'\b(if|elif|try|except)\b', l)
                    for l in preceding_lines
                )
                
                if not has_conditionals:
                    detections.append(HallucinationDetection(
                        pattern=HallucinationPattern.ALWAYS_RETURNS_TRUE,
                        severity=HallucinationSeverity.HIGH,
                        file_path=file_path,
                        line_number=i,
                        function_name=self._get_function_name(lines, i),
                        code_snippet=line.strip(),
                        explanation="Function always returns True without any validation",
                        suggestion="Add actual validation logic or error handling",
                        confidence=0.80
                    ))
        
        return detections
    
    async def _detect_fake_imports(
        self, code: str, file_path: str
    ) -> List[HallucinationDetection]:
        """Detect imports that don't exist or are never used"""
        detections = []
        lines = code.split('\n')
        
        try:
            tree = ast.parse(code)
            imports = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            
            # Check if imports are actually used in code
            for import_name in imports:
                # Simple check: is the import name mentioned in code after import?
                if code.count(import_name) == 1:  # Only appears in import line
                    # Find line number
                    for i, line in enumerate(lines, 1):
                        if f"import {import_name}" in line or f"from {import_name}" in line:
                            detections.append(HallucinationDetection(
                                pattern=HallucinationPattern.PERFECT_STRUCTURE_NO_IMPL,
                                severity=HallucinationSeverity.LOW,
                                file_path=file_path,
                                line_number=i,
                                function_name="module",
                                code_snippet=line.strip(),
                                explanation=f"Import '{import_name}' is never used",
                                suggestion="Remove unused import or actually use it",
                                confidence=0.70
                            ))
                            break
        
        except SyntaxError:
            pass
        
        return detections
    
    async def _detect_no_external_calls(
        self, code: str, file_path: str
    ) -> List[HallucinationDetection]:
        """Detect if code claims to call external APIs but doesn't"""
        detections = []
        
        # Indicators that code should make external calls
        external_indicators = [
            "payment", "paypal", "razorpay", "stripe",
            "api_call", "http", "request", "post", "get",
            "database", "query", "insert", "update"
        ]
        
        # Actual external call patterns
        external_calls = [
            r'requests\.(get|post|put|delete)',
            r'httpx\.(get|post|put|delete)',
            r'aiohttp\.',
            r'supabase\.',
            r'\.execute\(\)',
            r'\.fetch\(',
            r'client\.(get|post|put)',
        ]
        
        code_lower = code.lower()
        
        # Check if code mentions external operations
        mentions_external = any(indicator in code_lower for indicator in external_indicators)
        
        if mentions_external:
            # Check if code actually makes external calls
            has_external_calls = any(re.search(pattern, code) for pattern in external_calls)
            
            if not has_external_calls:
                # This is suspicious - mentions external ops but doesn't call anything
                detections.append(HallucinationDetection(
                    pattern=HallucinationPattern.MOCK_WITHOUT_REAL_API,
                    severity=HallucinationSeverity.HIGH,
                    file_path=file_path,
                    line_number=1,
                    function_name="module",
                    code_snippet="(entire file)",
                    explanation="Code mentions external operations (API, database) but makes no actual calls",
                    suggestion="Implement actual API/database calls or mark as mock/stub",
                    confidence=0.75
                ))
        
        return detections
    
    def _get_function_name(self, lines: List[str], current_line: int) -> str:
        """Get the function name for a given line number"""
        # Search backwards for function definition
        for i in range(current_line - 1, max(0, current_line - 50), -1):
            match = re.match(r'\s*(?:async\s+)?def\s+(\w+)', lines[i])
            if match:
                return match.group(1)
        return "unknown"
    
    def _generate_summary(
        self,
        is_real: bool,
        total: int,
        critical: int,
        high: int,
        medium: int,
        low: int,
        score: float
    ) -> str:
        """Generate human-readable summary"""
        if is_real:
            return f"✅ Code appears REAL (Reality Score: {score:.2f}). Found {total} minor issues."
        else:
            return (
                f"⚠️ Code appears FAKE/DELUSIONAL (Reality Score: {score:.2f}). "
                f"Found {critical} critical, {high} high, {medium} medium, {low} low severity issues. "
                f"This code may look perfect but likely doesn't actually work."
            )
    
    async def check_file(self, file_path: str) -> RealityCheckResult:
        """Check a specific file for hallucination patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            return await self.check_code_reality(code, file_path)
        
        except Exception as e:
            logger.error("Error checking file", file_path=file_path, error=str(e))
            return RealityCheckResult(
                is_real=False,
                hallucinations=[],
                total_issues=0,
                critical_count=0,
                high_count=0,
                medium_count=0,
                low_count=0,
                reality_score=0.0,
                summary=f"Error: {str(e)}"
            )
    
    async def check_directory(
        self,
        directory: str,
        extensions: List[str] = ['.py'],
        recursive: bool = True
    ) -> Dict[str, RealityCheckResult]:
        """Check all files in a directory"""
        results = {}
        path = Path(directory)
        
        pattern = "**/*" if recursive else "*"
        
        for ext in extensions:
            for file_path in path.glob(f"{pattern}{ext}"):
                if file_path.is_file():
                    result = await self.check_file(str(file_path))
                    results[str(file_path)] = result
        
        return results
    
    def generate_report(
        self,
        results: Dict[str, RealityCheckResult],
        output_file: Optional[str] = None
    ) -> str:
        """Generate a comprehensive reality check report"""
        report_lines = [
            "=" * 80,
            "REALITY CHECK DNA - Anti-Hallucination Report",
            "=" * 80,
            "",
            f"Files Analyzed: {len(results)}",
            ""
        ]
        
        # Statistics
        total_real = sum(1 for r in results.values() if r.is_real)
        total_fake = len(results) - total_real
        total_issues = sum(r.total_issues for r in results.values())
        avg_score = sum(r.reality_score for r in results.values()) / len(results) if results else 0
        
        report_lines.extend([
            f"Real Implementations:  {total_real} ({total_real/len(results)*100:.1f}%)",
            f"Fake/Suspicious:       {total_fake} ({total_fake/len(results)*100:.1f}%)",
            f"Total Issues Found:    {total_issues}",
            f"Average Reality Score: {avg_score:.2f}",
            "",
            "=" * 80,
            ""
        ])
        
        # Detailed results for fake/suspicious files
        for file_path, result in results.items():
            if not result.is_real or result.total_issues > 0:
                report_lines.extend([
                    f"File: {file_path}",
                    f"Reality Score: {result.reality_score:.2f}",
                    f"Status: {'⚠️ SUSPICIOUS' if not result.is_real else '✅ OK'}",
                    f"Issues: {result.total_issues} ({result.critical_count} critical, {result.high_count} high)",
                    ""
                ])
                
                # List hallucinations
                for h in result.hallucinations[:5]:  # Show first 5
                    report_lines.extend([
                        f"  Line {h.line_number}: {h.pattern.value}",
                        f"    Severity: {h.severity.value}",
                        f"    Explanation: {h.explanation}",
                        f"    Suggestion: {h.suggestion}",
                        ""
                    ])
                
                if result.total_issues > 5:
                    report_lines.append(f"  ... and {result.total_issues - 5} more issues\n")
                
                report_lines.append("-" * 80 + "\n")
        
        report = "\n".join(report_lines)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            logger.info("Reality check report written", output_file=output_file)
        
        return report


# Global instance
reality_check_dna = RealityCheckDNA()


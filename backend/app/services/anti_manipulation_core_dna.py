"""
🧬 Anti-Manipulation Core DNA - Prevents All Tricks and Manipulations

This DNA system prevents the 7 manipulation tricks identified in COMPLETE_HONEST_CONFESSION.md
and enforces REAL fixes only.

Created: 2025-10-10
Purpose: Stop AI manipulation, enforce honest development
"""

import structlog
from typing import Dict, List, Any, Optional, Set
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import ast
import re

logger = structlog.get_logger()


class ManipulationTrick(Enum):
    """7 Manipulation tricks that must be prevented"""
    CONTEXT_WHITELIST = "context_aware_whitelist"  # Trick #1: Filtering issues without fixing
    ENHANCED_WHITELIST = "enhanced_whitelist_rules"  # Trick #2: More ways to hide issues
    PATH_EXCLUSION = "path_based_exclusion"  # Trick #3: Statistical manipulation
    DOCUMENTATION_COSMETIC = "documentation_enhancement"  # Trick #4: Cosmetic labeling
    LOWERING_STANDARDS = "lowering_the_bar"  # Trick #5: Moving goalposts
    FALSE_POSITIVE_EXCUSE = "false_positive_justification"  # Trick #6: Selective categorization
    PROJECTED_RESULTS = "projected_claims"  # Trick #7: Unverified claims


@dataclass
class FixValidation:
    """Validates that a fix is REAL, not a trick"""
    file_path: str
    issue_description: str
    fix_type: str
    code_changed: bool
    lines_modified: int
    is_real_fix: bool
    trick_detected: Optional[ManipulationTrick]
    validation_timestamp: datetime
    evidence: Dict[str, Any]


class AntiManipulationCoreDNA:
    """
    🧬 Core DNA System: Prevents All Manipulation Tricks
    
    ENFORCES:
    - Real code changes only
    - No whitelisting to hide problems
    - No documentation tricks
    - No statistical manipulation
    - No lowered standards
    - No false excuses
    - No unverified claims
    
    BLOCKS:
    - Context-based issue hiding
    - Path exclusions to inflate percentages
    - Cosmetic documentation
    - Standard lowering
    - False positive excuses without proof
    - Projections without verification
    """
    
    def __init__(self):
        self.fix_history: List[FixValidation] = []
        self.blocked_tricks: Dict[ManipulationTrick, int] = {
            trick: 0 for trick in ManipulationTrick
        }
        self.whitelist_attempts: List[Dict[str, Any]] = []
        self.real_fixes_count = 0
        self.trick_attempts_count = 0
        
        # Forbidden patterns that indicate manipulation
        self.forbidden_patterns = {
            ManipulationTrick.CONTEXT_WHITELIST: [
                "skip_if_context",
                "ignore_in_context",
                "context_rule",
                "whitelist_pattern",
                "filter_by_context"
            ],
            ManipulationTrick.ENHANCED_WHITELIST: [
                "add_whitelist",
                "whitelist_rule",
                "ignore_pattern",
                "skip_check_if",
                "exclude_from_scan"
            ],
            ManipulationTrick.PATH_EXCLUSION: [
                "exclude_path",
                "skip_directory",
                "ignore_folder",
                "reduce_scope"
            ],
            ManipulationTrick.DOCUMENTATION_COSMETIC: [
                "🧬 REAL IMPLEMENTATION",
                "Production-grade",
                "REAL functionality",
                # Without actual code changes
            ],
            ManipulationTrick.LOWERING_STANDARDS: [
                "90% is perfect",
                "98% is complete",
                "ignore remaining",
                "good enough"
            ],
            ManipulationTrick.FALSE_POSITIVE_EXCUSE: [
                "false positive",
                "not a real bug",
                "context-sensitive",
                # Without proper verification
            ],
            ManipulationTrick.PROJECTED_RESULTS: [
                "expected to",
                "projected",
                "should reach",
                "estimated",
                # Without actual measurement
            ]
        }
        
        logger.info("Anti-Manipulation Core DNA initialized")
    
    def validate_fix(
        self,
        file_path: str,
        issue: str,
        old_code: str,
        new_code: str,
        fix_description: str
    ) -> FixValidation:
        """
        Validate that a fix is REAL, not a manipulation trick
        
        Returns:
            FixValidation with is_real_fix=True only if it's a genuine fix
        """
        evidence = {}
        trick_detected = None
        is_real_fix = False
        
        # Step 1: Check if code actually changed
        code_changed = old_code != new_code
        lines_modified = self._count_modified_lines(old_code, new_code)
        
        evidence['code_changed'] = code_changed
        evidence['lines_modified'] = lines_modified
        
        # Step 2: Detect manipulation tricks
        
        # TRICK #1 & #2: Whitelist/Context filtering
        if self._is_whitelist_trick(new_code, fix_description):
            trick_detected = ManipulationTrick.CONTEXT_WHITELIST
            self.blocked_tricks[trick_detected] += 1
            evidence['trick_reason'] = "Added whitelist/context filter without fixing root cause"
        
        # TRICK #3: Path exclusion
        elif self._is_path_exclusion_trick(new_code, fix_description):
            trick_detected = ManipulationTrick.PATH_EXCLUSION
            self.blocked_tricks[trick_detected] += 1
            evidence['trick_reason'] = "Excluded paths to manipulate statistics"
        
        # TRICK #4: Documentation only (no logic change)
        elif self._is_documentation_trick(old_code, new_code, lines_modified):
            trick_detected = ManipulationTrick.DOCUMENTATION_COSMETIC
            self.blocked_tricks[trick_detected] += 1
            evidence['trick_reason'] = "Only changed documentation, no logic fix"
        
        # TRICK #5: Lowering standards
        elif self._is_lowering_standards(fix_description):
            trick_detected = ManipulationTrick.LOWERING_STANDARDS
            self.blocked_tricks[trick_detected] += 1
            evidence['trick_reason'] = "Lowered acceptance criteria instead of fixing"
        
        # TRICK #6: False positive excuse
        elif self._is_false_positive_excuse(fix_description):
            trick_detected = ManipulationTrick.FALSE_POSITIVE_EXCUSE
            self.blocked_tricks[trick_detected] += 1
            evidence['trick_reason'] = "Claimed false positive without proper verification"
        
        # TRICK #7: Projected/unverified claims
        elif self._is_projected_claim(fix_description):
            trick_detected = ManipulationTrick.PROJECTED_RESULTS
            self.blocked_tricks[trick_detected] += 1
            evidence['trick_reason'] = "Made projections without verification"
        
        # Step 3: Validate it's a REAL fix
        else:
            is_real_fix = self._validate_real_fix(old_code, new_code, issue)
            if is_real_fix:
                self.real_fixes_count += 1
                evidence['fix_type'] = 'real_code_change'
                evidence['validation'] = 'passed_all_checks'
            else:
                evidence['fix_type'] = 'unknown'
                evidence['validation'] = 'no_trick_detected_but_not_verified_as_real'
        
        if trick_detected:
            self.trick_attempts_count += 1
        
        validation = FixValidation(
            file_path=file_path,
            issue_description=issue,
            fix_type=evidence.get('fix_type', 'unknown'),
            code_changed=code_changed,
            lines_modified=lines_modified,
            is_real_fix=is_real_fix,
            trick_detected=trick_detected,
            validation_timestamp=datetime.now(),
            evidence=evidence
        )
        
        self.fix_history.append(validation)
        
        if trick_detected:
            logger.warning(
                "MANIPULATION TRICK DETECTED",
                trick=trick_detected.value,
                file=file_path,
                reason=evidence.get('trick_reason')
            )
        elif is_real_fix:
            logger.info(
                "REAL FIX VALIDATED",
                file=file_path,
                lines_changed=lines_modified
            )
        
        return validation
    
    def _is_whitelist_trick(self, new_code: str, description: str) -> bool:
        """Detect context/whitelist filtering tricks"""
        patterns = self.forbidden_patterns[ManipulationTrick.CONTEXT_WHITELIST]
        patterns.extend(self.forbidden_patterns[ManipulationTrick.ENHANCED_WHITELIST])
        
        for pattern in patterns:
            if pattern in new_code or pattern in description.lower():
                return True
        
        # Check for whitelist data structures
        if re.search(r'whitelist\s*[=:]\s*[\[\{]', new_code, re.IGNORECASE):
            return True
        
        # Check for context-based filtering
        if re.search(r'if.*context.*skip|if.*context.*ignore', new_code, re.IGNORECASE):
            return True
        
        return False
    
    def _is_path_exclusion_trick(self, new_code: str, description: str) -> bool:
        """Detect path exclusion statistical manipulation"""
        patterns = self.forbidden_patterns[ManipulationTrick.PATH_EXCLUSION]
        
        for pattern in patterns:
            if pattern in new_code.lower() or pattern in description.lower():
                return True
        
        # Check for exclusion lists
        if re.search(r'exclude.*=.*\[|skip.*paths.*=', new_code, re.IGNORECASE):
            return True
        
        return False
    
    def _is_documentation_trick(self, old_code: str, new_code: str, lines_modified: int) -> bool:
        """Detect documentation-only changes (cosmetic)"""
        if lines_modified == 0:
            return False
        
        # Remove comments and docstrings from both
        old_logic = self._strip_documentation(old_code)
        new_logic = self._strip_documentation(new_code)
        
        # If logic is identical, it's just documentation
        if old_logic == new_logic:
            # Check if added "REAL IMPLEMENTATION" claims
            if '🧬 REAL IMPLEMENTATION' in new_code and '🧬 REAL IMPLEMENTATION' not in old_code:
                return True
            
            # Check if only added docstrings
            if '"""' in new_code and '"""' not in old_code:
                return True
        
        return False
    
    def _is_lowering_standards(self, description: str) -> bool:
        """Detect standard lowering"""
        patterns = self.forbidden_patterns[ManipulationTrick.LOWERING_STANDARDS]
        
        desc_lower = description.lower()
        
        for pattern in patterns:
            if pattern in desc_lower:
                return True
        
        # Check for percentage claims with "perfect"
        if re.search(r'\d{2}%.*(?:perfect|complete|done)', desc_lower):
            return True
        
        return False
    
    def _is_false_positive_excuse(self, description: str) -> bool:
        """Detect unjustified false positive claims"""
        desc_lower = description.lower()
        
        # Has "false positive" claim
        has_fp_claim = 'false positive' in desc_lower or 'not a real bug' in desc_lower
        
        if not has_fp_claim:
            return False
        
        # Check if has justification (AST analysis, test verification, etc.)
        has_justification = any(keyword in desc_lower for keyword in [
            'verified by ast',
            'test confirms',
            'actually correct',
            'validated',
            'proof:',
            'evidence:'
        ])
        
        # If claims false positive without justification, it's a trick
        return not has_justification
    
    def _is_projected_claim(self, description: str) -> bool:
        """Detect unverified projections"""
        patterns = self.forbidden_patterns[ManipulationTrick.PROJECTED_RESULTS]
        
        desc_lower = description.lower()
        
        for pattern in patterns:
            if pattern in desc_lower:
                # Check if has verification
                has_verification = any(keyword in desc_lower for keyword in [
                    'measured',
                    'verified',
                    'confirmed',
                    'tested',
                    'actual result'
                ])
                
                if not has_verification:
                    return True
        
        return False
    
    def _validate_real_fix(self, old_code: str, new_code: str, issue: str) -> bool:
        """
        Validate that a fix is REAL by checking:
        1. Code logic changed (not just comments)
        2. Addresses the actual issue
        3. No placeholders replaced with other placeholders
        """
        # Strip documentation for logic comparison
        old_logic = self._strip_documentation(old_code)
        new_logic = self._strip_documentation(new_code)
        
        # Must have logic change
        if old_logic == new_logic:
            return False
        
        # Check for placeholder-to-placeholder replacements
        placeholder_patterns = [
            r'return\s+0\.0\s*#\s*(?:Honest|Placeholder|TODO)',
            r'return\s+\[\]\s*#\s*(?:Placeholder|TODO)',
            r'pass\s*#\s*(?:TODO|Placeholder)',
            r'raise\s+NotImplementedError'
        ]
        
        old_has_placeholder = any(re.search(p, old_code) for p in placeholder_patterns)
        new_has_placeholder = any(re.search(p, new_code) for p in placeholder_patterns)
        
        # If both have placeholders, it's not a real fix
        if old_has_placeholder and new_has_placeholder:
            return False
        
        # Check that new code has actual implementation
        has_implementation = self._has_real_implementation(new_code)
        
        return has_implementation
    
    def _has_real_implementation(self, code: str) -> bool:
        """Check if code has real implementation (not placeholder)"""
        # Check for actual logic patterns
        implementation_indicators = [
            r'if\s+',
            r'for\s+',
            r'while\s+',
            r'try:',
            r'except',
            r'return\s+\w+\(',  # Function call
            r'=\s*\w+\(',  # Assignment from function
            r'await\s+',
            r'\w+\.\w+\(',  # Method call
        ]
        
        for indicator in implementation_indicators:
            if re.search(indicator, code):
                return True
        
        return False
    
    def _strip_documentation(self, code: str) -> str:
        """Remove comments and docstrings, keep only logic"""
        # Remove single-line comments
        code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)
        
        # Remove docstrings
        code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
        code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
        
        # Remove empty lines
        code = '\n'.join(line for line in code.split('\n') if line.strip())
        
        return code
    
    def _count_modified_lines(self, old_code: str, new_code: str) -> int:
        """Count actual modified lines"""
        old_lines = set(old_code.split('\n'))
        new_lines = set(new_code.split('\n'))
        
        added = new_lines - old_lines
        removed = old_lines - new_lines
        
        return len(added) + len(removed)
    
    def block_whitelist_addition(
        self,
        whitelist_rule: str,
        reason: str,
        context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Block whitelist additions that hide issues instead of fixing them
        
        Returns:
            False (blocked) if it's a manipulation trick
            True (allowed) only if it's a legitimate false positive filter
        """
        # Record the attempt
        self.whitelist_attempts.append({
            'rule': whitelist_rule,
            'reason': reason,
            'context': context,
            'timestamp': datetime.now()
        })
        
        # Check if reason is legitimate
        legitimate_reasons = [
            'verified false positive via ast analysis',
            'test generator pattern (confirmed by test)',
            'security honeypot (intentional)',
            'example/demo code in documentation',
        ]
        
        reason_lower = reason.lower()
        is_legitimate = any(legit in reason_lower for legit in legitimate_reasons)
        
        if not is_legitimate:
            logger.warning(
                "WHITELIST BLOCKED",
                rule=whitelist_rule,
                reason=reason,
                verdict="manipulation_attempt"
            )
            self.blocked_tricks[ManipulationTrick.CONTEXT_WHITELIST] += 1
            return False
        
        # Even if legitimate, require evidence
        if not context or 'evidence' not in context:
            logger.warning(
                "WHITELIST BLOCKED - no evidence",
                rule=whitelist_rule,
                reason="no_evidence_provided"
            )
            return False
        
        logger.info(
            "Whitelist allowed (legitimate false positive)",
            rule=whitelist_rule,
            evidence=context.get('evidence')
        )
        return True
    
    def enforce_real_fix_only(self, proposed_change: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforce that only REAL fixes are applied
        
        Args:
            proposed_change: {
                'file': str,
                'issue': str,
                'old_code': str,
                'new_code': str,
                'description': str
            }
        
        Returns:
            {
                'approved': bool,
                'validation': FixValidation,
                'message': str
            }
        """
        validation = self.validate_fix(
            file_path=proposed_change['file'],
            issue=proposed_change['issue'],
            old_code=proposed_change['old_code'],
            new_code=proposed_change['new_code'],
            fix_description=proposed_change['description']
        )
        
        if validation.trick_detected:
            return {
                'approved': False,
                'validation': validation,
                'message': f"🚫 BLOCKED: Manipulation trick detected - {validation.trick_detected.value}. "
                          f"Reason: {validation.evidence.get('trick_reason')}. "
                          f"Apply REAL fix instead."
            }
        
        if not validation.is_real_fix:
            return {
                'approved': False,
                'validation': validation,
                'message': f"🚫 BLOCKED: Not a real fix. Code must have actual implementation changes, "
                          f"not just documentation or cosmetic changes."
            }
        
        return {
            'approved': True,
            'validation': validation,
            'message': f"✅ APPROVED: Real fix validated with {validation.lines_modified} lines modified"
        }
    
    def get_manipulation_report(self) -> Dict[str, Any]:
        """Get comprehensive report on manipulation attempts and real fixes"""
        return {
            'total_fixes_attempted': len(self.fix_history),
            'real_fixes': self.real_fixes_count,
            'trick_attempts': self.trick_attempts_count,
            'blocked_by_type': {
                trick.value: count 
                for trick, count in self.blocked_tricks.items()
                if count > 0
            },
            'success_rate': (
                self.real_fixes_count / len(self.fix_history) * 100
                if self.fix_history else 0.0
            ),
            'whitelist_attempts': len(self.whitelist_attempts),
            'recent_tricks': [
                {
                    'file': v.file_path,
                    'trick': v.trick_detected.value if v.trick_detected else None,
                    'timestamp': v.validation_timestamp.isoformat()
                }
                for v in self.fix_history[-10:]
                if v.trick_detected
            ]
        }


# Global singleton
_anti_manipulation_dna = None


def get_anti_manipulation_dna() -> AntiManipulationCoreDNA:
    """Get global Anti-Manipulation DNA instance"""
    global _anti_manipulation_dna
    if _anti_manipulation_dna is None:
        _anti_manipulation_dna = AntiManipulationCoreDNA()
    return _anti_manipulation_dna


"""
🧬 ANTI-TRICK DNA - Core DNA System #8
Prevents ALL tricks identified in COMPLETE_HONEST_CONFESSION.md

CORE PRINCIPLE:
Based on honest confession of 7 tricks used, this DNA permanently blocks:
1. Context-aware filtering/whitelisting
2. Enhanced whitelist rules
3. Path exclusions to inflate percentages
4. Documentation labeling without code changes
5. Lowering standards ("98% = PERFECT")
6. False positive over-justification
7. Unverified projections/claims

This DNA enforces:
- Zero tolerance for score manipulation
- Zero tolerance for cosmetic improvements
- 100% REAL fixes only (no shortcuts)
- Verifiable improvements (not projections)
- Honest metrics (no statistical tricks)
"""

import structlog
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import ast
import re

logger = structlog.get_logger()


class TrickType(Enum):
    """Types of tricks that are BLOCKED"""
    WHITELISTING = "whitelisting"  # Filtering issues without fixing
    PATH_EXCLUSION = "path_exclusion"  # Excluding files to inflate %
    DOCUMENTATION_ONLY = "documentation_only"  # Adding docs without code
    STANDARD_LOWERING = "standard_lowering"  # "98% = PERFECT"
    FALSE_POSITIVE_EXCUSE = "false_positive_excuse"  # Over-justifying
    UNVERIFIED_CLAIM = "unverified_claim"  # Projections without proof
    SCORE_MANIPULATION = "score_manipulation"  # Any score gaming


@dataclass
class TrickDetectionResult:
    """Result of trick detection"""
    is_trick: bool
    trick_type: Optional[TrickType]
    confidence: float  # 0.0 to 1.0
    explanation: str
    evidence: List[str]
    recommendation: str


class AntiTrickDNA:
    """
    🧬 CORE DNA SYSTEM #8: Anti-Trick DNA
    
    Permanently prevents all tricks from COMPLETE_HONEST_CONFESSION.md
    
    BLOCKS:
    1. Whitelisting - filtering patterns without fixing code
    2. Path exclusions - skipping files to inflate percentages
    3. Documentation-only - adding docs without functional changes
    4. Standard lowering - calling 98% "PERFECT" when 100% required
    5. False positive excuses - avoiding real fixes by claiming "context"
    6. Unverified claims - projections without actual measurements
    7. Score manipulation - any gaming of metrics
    
    ENFORCES:
    - 100% means ALL files (not 98%)
    - Real code fixes (not documentation)
    - Verified results (not projections)
    - Honest metrics (no statistical tricks)
    - Complete fixes (not partial)
    
    USING ALL 7 DNA SYSTEMS:
    1️⃣ Zero Assumption - Verify no tricks used
    2️⃣ Reality Check - Detect fake improvements
    3️⃣ Precision - Exact identification of tricks
    4️⃣ Autonomous - Self-aware: am I tricking?
    5️⃣ Consistency - No gaming metrics
    6️⃣ Immutable - DNA systems are protected
    7️⃣ Reality-Focused - Real solutions only
    """
    
    def __init__(self):
        self.trick_patterns = self._initialize_trick_patterns()
        logger.info(
            "🧬 Anti-Trick DNA initialized",
            principle="Zero tolerance for tricks",
            enforcement="STRICT",
            based_on="COMPLETE_HONEST_CONFESSION.md"
        )
    
    def _initialize_trick_patterns(self) -> Dict[TrickType, List[Dict[str, Any]]]:
        """Initialize patterns for each trick type"""
        return {
            TrickType.WHITELISTING: [
                {
                    "code_patterns": [
                        r"add.*whitelist",
                        r"add.*context.*rule",
                        r"filter.*pattern",
                        r"suppress.*warning",
                        r"ignore.*issue"
                    ],
                    "description": "Adding whitelist/filter rules without fixing code"
                },
                {
                    "file_patterns": [
                        "*context_aware*.py",
                        "*whitelist*.py",
                        "*filter*.py"
                    ],
                    "changes_without": "actual_code_fixes",
                    "description": "Modifying filtering logic instead of fixing issues"
                }
            ],
            
            TrickType.PATH_EXCLUSION: [
                {
                    "code_patterns": [
                        r"skip.*\.venv",
                        r"exclude.*site-packages",
                        r"ignore.*node_modules",
                        r"only.*scan.*backend/app"
                    ],
                    "description": "Excluding files to make percentages look better"
                },
                {
                    "metric_manipulation": True,
                    "changes_denominator": True,
                    "description": "Reducing total files to inflate percentage"
                }
            ],
            
            TrickType.DOCUMENTATION_ONLY: [
                {
                    "code_patterns": [
                        r"^(\"\"\".*\"\"\")$",  # Just docstring changes
                        r"^#.*REAL IMPLEMENTATION",  # Claims in comments
                        r"^#.*Production-grade",  # Labels without code
                    ],
                    "without_logic": True,
                    "description": "Adding documentation without functional changes"
                },
                {
                    "diff_only_comments": True,
                    "no_logic_changes": True,
                    "description": "Only comments/docstrings changed, no real code"
                }
            ],
            
            TrickType.STANDARD_LOWERING: [
                {
                    "claims": [
                        r"98.*PERFECT",
                        r"95.*excellent",
                        r"90.*good.*enough"
                    ],
                    "when_required": "100%",
                    "description": "Lowering standards to avoid complete fixes"
                },
                {
                    "threshold_lowering": True,
                    "original": 1.0,
                    "new": 0.95,
                    "description": "Reducing required threshold"
                }
            ],
            
            TrickType.FALSE_POSITIVE_EXCUSE: [
                {
                    "claims": [
                        r"this.*false positive",
                        r"context.*sensitive",
                        r"not.*real.*bug",
                        r"legitimate.*pattern"
                    ],
                    "without_proof": True,
                    "description": "Claiming issues aren't real to avoid fixing"
                },
                {
                    "excuse_ratio": "> 50%",  # More than half called "false positives"
                    "suspicious": True,
                    "description": "Too many issues dismissed as false positives"
                }
            ],
            
            TrickType.UNVERIFIED_CLAIM: [
                {
                    "claims": [
                        r"expected.*will.*improve",
                        r"projected.*results",
                        r"should.*achieve",
                        r"will.*fix.*when"
                    ],
                    "without_measurement": True,
                    "description": "Making claims without actual verification"
                },
                {
                    "future_tense": True,
                    "no_current_proof": True,
                    "description": "Promises without current evidence"
                }
            ],
            
            TrickType.SCORE_MANIPULATION: [
                {
                    "code_patterns": [
                        r"improve.*score.*without.*fix",
                        r"inflate.*percentage",
                        r"manipulate.*metric",
                        r"game.*system"
                    ],
                    "description": "Directly manipulating scores"
                },
                {
                    "changes_scoring": True,
                    "without_code_fixes": True,
                    "description": "Changing how scores calculated without fixing issues"
                }
            ]
        }
    
    def detect_trick(
        self,
        action_description: str,
        code_changes: Optional[Dict[str, Any]] = None,
        metrics_before: Optional[Dict[str, float]] = None,
        metrics_after: Optional[Dict[str, float]] = None
    ) -> TrickDetectionResult:
        """
        🧬 DETECT if an action is a trick
        
        Args:
            action_description: What is being done
            code_changes: Actual code modifications
            metrics_before: Metrics before action
            metrics_after: Metrics after action
        
        Returns:
            Detection result with confidence
        """
        
        action_lower = action_description.lower()
        evidence = []
        detected_tricks = []
        
        # Check TRICK #1: Whitelisting
        whitelist_keywords = ['whitelist', 'context rule', 'filter', 'suppress', 'ignore']
        if any(kw in action_lower for kw in whitelist_keywords):
            if code_changes and not self._has_real_code_fixes(code_changes):
                evidence.append("Adding filtering without code fixes")
                detected_tricks.append((TrickType.WHITELISTING, 0.9))
        
        # Check TRICK #2: Path Exclusion
        exclusion_keywords = ['skip', 'exclude', 'only scan', 'ignore path']
        if any(kw in action_lower for kw in exclusion_keywords):
            if metrics_before and metrics_after:
                # Check if total files decreased (denominator manipulation)
                if metrics_after.get('total_files', 0) < metrics_before.get('total_files', 0):
                    evidence.append("Total files decreased (path exclusion)")
                    detected_tricks.append((TrickType.PATH_EXCLUSION, 0.95))
        
        # Check TRICK #3: Documentation Only
        doc_keywords = ['add documentation', 'add comment', 'add docstring', 'clarify in docs']
        if any(kw in action_lower for kw in doc_keywords):
            if code_changes and self._is_documentation_only(code_changes):
                evidence.append("Only documentation changed, no logic")
                detected_tricks.append((TrickType.DOCUMENTATION_ONLY, 0.85))
        
        # Check TRICK #4: Standard Lowering
        lowering_keywords = ['98% perfect', '95% excellent', 'good enough', 'acceptable threshold']
        if any(kw in action_lower for kw in lowering_keywords):
            if '100%' in action_description or 'all files' in action_lower:
                evidence.append("Lowering standard from 100% to lower value")
                detected_tricks.append((TrickType.STANDARD_LOWERING, 0.8))
        
        # Check TRICK #5: False Positive Excuse
        excuse_keywords = ['false positive', 'not a bug', 'context sensitive', 'legitimate']
        if any(kw in action_lower for kw in excuse_keywords):
            # If used too frequently, it's suspicious
            if metrics_before and metrics_after:
                issues_before = metrics_before.get('issues', 0)
                issues_after = metrics_after.get('issues', 0)
                fixed_ratio = (issues_before - issues_after) / issues_before if issues_before > 0 else 0
                if fixed_ratio < 0.3:  # Less than 30% actually fixed
                    evidence.append("Many issues dismissed as false positives (<30% fixed)")
                    detected_tricks.append((TrickType.FALSE_POSITIVE_EXCUSE, 0.7))
        
        # Check TRICK #6: Unverified Claim
        claim_keywords = ['expected', 'will improve', 'projected', 'should achieve']
        if any(kw in action_lower for kw in claim_keywords):
            if not metrics_after or metrics_after.get('verified', False) == False:
                evidence.append("Making claims without current verification")
                detected_tricks.append((TrickType.UNVERIFIED_CLAIM, 0.75))
        
        # Check TRICK #7: Score Manipulation
        if metrics_before and metrics_after:
            score_improved = metrics_after.get('score', 0) > metrics_before.get('score', 0)
            code_fixes = code_changes and len(code_changes.get('files_modified', [])) > 0
            
            if score_improved and not code_fixes:
                evidence.append("Score improved without code changes")
                detected_tricks.append((TrickType.SCORE_MANIPULATION, 0.95))
        
        # Determine result
        if detected_tricks:
            # Get highest confidence trick
            trick_type, confidence = max(detected_tricks, key=lambda x: x[1])
            
            return TrickDetectionResult(
                is_trick=True,
                trick_type=trick_type,
                confidence=confidence,
                explanation=f"Detected {trick_type.value}: {', '.join(evidence)}",
                evidence=evidence,
                recommendation=self._get_recommendation(trick_type)
            )
        
        # No trick detected
        return TrickDetectionResult(
            is_trick=False,
            trick_type=None,
            confidence=0.0,
            explanation="No tricks detected - appears to be genuine fix",
            evidence=[],
            recommendation="Proceed with implementation"
        )
    
    def _has_real_code_fixes(self, code_changes: Dict[str, Any]) -> bool:
        """Check if changes include real code fixes (not just filtering)"""
        files = code_changes.get('files_modified', [])
        
        # Filter files that are just whitelist/context rules
        filtering_files = ['context_aware', 'whitelist', 'filter', 'suppress']
        real_fixes = [f for f in files if not any(ff in f.lower() for ff in filtering_files)]
        
        return len(real_fixes) > 0
    
    def _is_documentation_only(self, code_changes: Dict[str, Any]) -> bool:
        """Check if changes are only documentation"""
        changes = code_changes.get('changes', [])
        
        # Check if all changes are comments/docstrings
        doc_patterns = [r'^#', r'^"""', r"^'''", r'^\s*#', r'^\s*"""']
        for change in changes:
            if not any(re.match(p, change) for p in doc_patterns):
                return False  # Found non-documentation change
        
        return True
    
    def _get_recommendation(self, trick_type: TrickType) -> str:
        """Get recommendation for avoiding this trick"""
        recommendations = {
            TrickType.WHITELISTING: "Instead of whitelisting, fix the actual code issues",
            TrickType.PATH_EXCLUSION: "Scan all files, don't exclude to inflate percentages",
            TrickType.DOCUMENTATION_ONLY: "Add functional code changes, not just documentation",
            TrickType.STANDARD_LOWERING: "Maintain 100% standard, don't lower to 98%",
            TrickType.FALSE_POSITIVE_EXCUSE: "Fix the issue or prove it's false with evidence",
            TrickType.UNVERIFIED_CLAIM: "Measure and verify before claiming improvement",
            TrickType.SCORE_MANIPULATION: "Fix code to improve scores, not scoring logic"
        }
        return recommendations.get(trick_type, "Use real fixes only")
    
    def enforce_no_tricks(
        self,
        action_description: str,
        code_changes: Optional[Dict[str, Any]] = None
    ) -> tuple[bool, str]:
        """
        🧬 ENFORCE that NO tricks are being used
        
        Returns (allowed, reason)
        """
        
        result = self.detect_trick(action_description, code_changes)
        
        if result.is_trick:
            return (
                False,
                f"BLOCKED: {result.trick_type.value} detected (confidence: {result.confidence:.0%}). "
                f"{result.recommendation}"
            )
        
        return (True, "No tricks detected - proceed with real fix")
    
    def validate_metric_improvement(
        self,
        metrics_before: Dict[str, float],
        metrics_after: Dict[str, float],
        code_changes: Dict[str, Any]
    ) -> tuple[bool, str]:
        """
        🧬 VALIDATE that metric improvement is from real fixes
        
        Returns (valid, explanation)
        """
        
        # Check if metrics improved
        score_before = metrics_before.get('score', 0)
        score_after = metrics_after.get('score', 0)
        improvement = score_after - score_before
        
        if improvement <= 0:
            return (True, "No improvement claimed")
        
        # Check if there are real code changes
        files_modified = len(code_changes.get('files_modified', []))
        logic_changes = code_changes.get('logic_changes', 0)
        
        if files_modified == 0:
            return (False, "Score improved but no files modified (trick detected)")
        
        if logic_changes == 0:
            return (False, "Score improved but no logic changes (documentation only)")
        
        # Check if improvement is proportional to work done
        expected_improvement = files_modified * 0.01  # Rough estimate
        if improvement > expected_improvement * 10:
            return (False, f"Improvement ({improvement:.2f}) too high for work done (suspicious)")
        
        return (True, f"Improvement validated: {files_modified} files modified with logic changes")


# Global instance
anti_trick_dna = AntiTrickDNA()


__all__ = [
    'AntiTrickDNA',
    'TrickType',
    'TrickDetectionResult',
    'anti_trick_dna'
]


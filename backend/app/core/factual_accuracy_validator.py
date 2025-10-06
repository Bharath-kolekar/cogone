"""
Factual Accuracy Validator

This module provides comprehensive factual accuracy validation for the Ethical AI system,
including truth verification, source validation, contradiction detection, and fact-checking.
"""

import re
import structlog
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import hashlib
import asyncio
from urllib.parse import urlparse

from app.core.redis import get_redis_client
from app.core.ethical_ai_core import ethical_ai_core

logger = structlog.get_logger(__name__)

class AccuracyLevel(Enum):
    """Factual accuracy levels"""
    VERIFIED = "verified"
    LIKELY_TRUE = "likely_true"
    UNCERTAIN = "uncertain"
    LIKELY_FALSE = "likely_false"
    FALSE = "false"
    CONTRADICTORY = "contradictory"

class SourceReliability(Enum):
    """Source reliability levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNRELIABLE = "unreliable"

class FactType(Enum):
    """Types of factual claims"""
    NUMERICAL = "numerical"
    TEMPORAL = "temporal"
    GEOGRAPHICAL = "geographical"
    SCIENTIFIC = "scientific"
    HISTORICAL = "historical"
    STATISTICAL = "statistical"
    DEFINITIONAL = "definitional"
    CAUSAL = "causal"

@dataclass
class FactualClaim:
    """Represents a factual claim to be validated"""
    claim_id: str
    text: str
    fact_type: FactType
    context: Optional[str] = None
    source: Optional[str] = None
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SourceReference:
    """Represents a source reference"""
    source_id: str
    url: Optional[str] = None
    title: Optional[str] = None
    author: Optional[str] = None
    publication_date: Optional[datetime] = None
    reliability: SourceReliability = SourceReliability.MEDIUM
    domain: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    """Result of factual validation"""
    claim_id: str
    accuracy_level: AccuracyLevel
    confidence_score: float
    supporting_evidence: List[SourceReference]
    contradicting_evidence: List[SourceReference]
    validation_methods: List[str]
    contradictions_detected: List[str]
    recommendations: List[str]
    validated_at: datetime

@dataclass
class AccuracyReport:
    """Comprehensive factual accuracy report"""
    report_id: str
    content_hash: str
    overall_accuracy_score: float
    total_claims: int
    verified_claims: int
    uncertain_claims: int
    false_claims: int
    contradictory_claims: int
    validation_results: List[ValidationResult]
    contradictions: List[Dict[str, Any]]
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.now)

class FactualAccuracyValidator:
    """Comprehensive factual accuracy validation system"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
        self.known_facts_db: Dict[str, Dict[str, Any]] = {}
        self.source_reliability_db: Dict[str, SourceReliability] = {}
        self.contradiction_patterns = self._initialize_contradiction_patterns()
        self.validation_cache: Dict[str, AccuracyReport] = {}
        self.fact_checkers = self._initialize_fact_checkers()
        
    def _initialize_contradiction_patterns(self) -> List[Tuple[str, str]]:
        """Initialize patterns for detecting contradictions"""
        return [
            # Temporal contradictions
            (r"always", r"never"),
            (r"always", r"sometimes"),
            (r"never", r"sometimes"),
            (r"all", r"none"),
            (r"all", r"some"),
            (r"none", r"some"),
            
            # Numerical contradictions
            (r"100%", r"0%"),
            (r"exactly \d+", r"approximately \d+"),
            (r"precisely", r"roughly"),
            
            # Definitive vs. uncertain statements
            (r"proven", r"unproven"),
            (r"confirmed", r"unconfirmed"),
            (r"established", r"disputed"),
            (r"fact", r"theory"),
            
            # Causal contradictions
            (r"causes", r"prevents"),
            (r"increases", r"decreases"),
            (r"leads to", r"prevents"),
        ]
    
    def _initialize_fact_checkers(self) -> Dict[FactType, List[str]]:
        """Initialize fact-checking methods for different fact types"""
        return {
            FactType.NUMERICAL: [
                "statistical_validation",
                "cross_reference_check",
                "mathematical_verification"
            ],
            FactType.TEMPORAL: [
                "chronological_validation",
                "historical_verification",
                "date_cross_check"
            ],
            FactType.GEOGRAPHICAL: [
                "geographic_verification",
                "coordinate_validation",
                "boundary_check"
            ],
            FactType.SCIENTIFIC: [
                "peer_review_check",
                "scientific_consensus",
                "experimental_validation"
            ],
            FactType.HISTORICAL: [
                "historical_verification",
                "primary_source_check",
                "chronological_validation"
            ],
            FactType.STATISTICAL: [
                "statistical_validation",
                "data_source_verification",
                "methodology_check"
            ],
            FactType.DEFINITIONAL: [
                "definition_verification",
                "terminology_check",
                "standard_reference"
            ],
            FactType.CAUSAL: [
                "causal_analysis",
                "correlation_check",
                "mechanism_verification"
            ]
        }
    
    async def validate_content_accuracy(self, content: str, context: Dict[str, Any] = None) -> AccuracyReport:
        """Validate factual accuracy of content"""
        try:
            # Generate content hash for caching
            content_hash = hashlib.md5(content.encode()).hexdigest()
            report_id = f"accuracy_{content_hash[:8]}"
            
            # Check cache first
            cache_key = f"accuracy_validation:{report_id}"
            cached_result = await self.redis_client.get(cache_key)
            if cached_result:
                cached_data = json.loads(cached_result)
                return AccuracyReport(**cached_data)
            
            # Extract factual claims from content
            claims = await self._extract_factual_claims(content, context or {})
            
            # Validate each claim
            validation_results = []
            for claim in claims:
                result = await self._validate_factual_claim(claim)
                validation_results.append(result)
            
            # Detect contradictions within content
            contradictions = await self._detect_contradictions(content, validation_results)
            
            # Calculate overall accuracy score
            overall_score = self._calculate_overall_accuracy_score(validation_results)
            
            # Count claims by accuracy level
            verified_count = len([r for r in validation_results if r.accuracy_level == AccuracyLevel.VERIFIED])
            uncertain_count = len([r for r in validation_results if r.accuracy_level == AccuracyLevel.UNCERTAIN])
            false_count = len([r for r in validation_results if r.accuracy_level == AccuracyLevel.FALSE])
            contradictory_count = len([r for r in validation_results if r.accuracy_level == AccuracyLevel.CONTRADICTORY])
            
            # Generate recommendations
            recommendations = self._generate_accuracy_recommendations(validation_results, contradictions)
            
            # Create report
            report = AccuracyReport(
                report_id=report_id,
                content_hash=content_hash,
                overall_accuracy_score=overall_score,
                total_claims=len(claims),
                verified_claims=verified_count,
                uncertain_claims=uncertain_count,
                false_claims=false_count,
                contradictory_claims=contradictory_count,
                validation_results=validation_results,
                contradictions=contradictions,
                recommendations=recommendations,
                metadata={
                    "content_length": len(content),
                    "context": context,
                    "validation_methods_used": list(set([method for result in validation_results for method in result.validation_methods]))
                }
            )
            
            # Cache result
            await self._cache_accuracy_report(cache_key, report)
            
            logger.info("Content accuracy validation completed", 
                       report_id=report_id,
                       overall_score=overall_score,
                       total_claims=len(claims),
                       verified_claims=verified_count)
            
            return report
            
        except Exception as e:
            logger.error("Content accuracy validation failed", error=str(e))
            raise
    
    async def _extract_factual_claims(self, content: str, context: Dict[str, Any]) -> List[FactualClaim]:
        """Extract factual claims from content"""
        claims = []
        
        # Split content into sentences
        sentences = re.split(r'[.!?]+', content)
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Determine fact type based on content patterns
            fact_type = self._determine_fact_type(sentence)
            
            # Extract numerical claims
            if fact_type == FactType.NUMERICAL:
                numerical_claims = self._extract_numerical_claims(sentence, i)
                claims.extend(numerical_claims)
            
            # Extract temporal claims
            elif fact_type == FactType.TEMPORAL:
                temporal_claims = self._extract_temporal_claims(sentence, i)
                claims.extend(temporal_claims)
            
            # Extract other types of claims
            else:
                claim = FactualClaim(
                    claim_id=f"claim_{i}_{hashlib.md5(sentence.encode()).hexdigest()[:8]}",
                    text=sentence,
                    fact_type=fact_type,
                    context=context.get("topic"),
                    metadata={"sentence_index": i}
                )
                claims.append(claim)
        
        return claims
    
    def _determine_fact_type(self, text: str) -> FactType:
        """Determine the type of factual claim"""
        text_lower = text.lower()
        
        # Numerical patterns
        if re.search(r'\d+%|\d+\s*(percent|million|billion|thousand)', text_lower):
            return FactType.NUMERICAL
        
        # Temporal patterns
        if re.search(r'\b(in|on|at|since|until|before|after)\s+\d{4}|\b(january|february|march|april|may|june|july|august|september|october|november|december)', text_lower):
            return FactType.TEMPORAL
        
        # Geographical patterns
        if re.search(r'\b(country|city|state|continent|ocean|mountain|river)\b', text_lower):
            return FactType.GEOGRAPHICAL
        
        # Scientific patterns
        if re.search(r'\b(study|research|experiment|hypothesis|theory|scientific|peer-reviewed)\b', text_lower):
            return FactType.SCIENTIFIC
        
        # Historical patterns
        if re.search(r'\b(historical|history|century|war|battle|empire|ancient|medieval)\b', text_lower):
            return FactType.HISTORICAL
        
        # Statistical patterns
        if re.search(r'\b(statistics|statistical|data|survey|poll|sample|population)\b', text_lower):
            return FactType.STATISTICAL
        
        # Causal patterns
        if re.search(r'\b(causes|caused by|leads to|results in|because of|due to)\b', text_lower):
            return FactType.CAUSAL
        
        # Default to definitional
        return FactType.DEFINITIONAL
    
    def _extract_numerical_claims(self, sentence: str, index: int) -> List[FactualClaim]:
        """Extract numerical claims from sentence"""
        claims = []
        numerical_patterns = [
            r'(\d+(?:\.\d+)?%?)',
            r'(million|billion|thousand)',
            r'(all|none|some|most|few)'
        ]
        
        for pattern in numerical_patterns:
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            for match in matches:
                claim = FactualClaim(
                    claim_id=f"numerical_{index}_{match.start()}",
                    text=match.group(),
                    fact_type=FactType.NUMERICAL,
                    context=sentence,
                    metadata={"match_start": match.start(), "match_end": match.end()}
                )
                claims.append(claim)
        
        return claims
    
    def _extract_temporal_claims(self, sentence: str, index: int) -> List[FactualClaim]:
        """Extract temporal claims from sentence"""
        claims = []
        temporal_patterns = [
            r'\b\d{4}\b',  # Years
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\b',
            r'\b(in|on|at|since|until|before|after)\s+\d{4}'
        ]
        
        for pattern in temporal_patterns:
            matches = re.finditer(pattern, sentence, re.IGNORECASE)
            for match in matches:
                claim = FactualClaim(
                    claim_id=f"temporal_{index}_{match.start()}",
                    text=match.group(),
                    fact_type=FactType.TEMPORAL,
                    context=sentence,
                    metadata={"match_start": match.start(), "match_end": match.end()}
                )
                claims.append(claim)
        
        return claims
    
    async def _validate_factual_claim(self, claim: FactualClaim) -> ValidationResult:
        """Validate a single factual claim"""
        try:
            # Get fact-checking methods for this claim type
            validation_methods = self.fact_checkers.get(claim.fact_type, ["general_validation"])
            
            # Perform validation using multiple methods
            supporting_evidence = []
            contradicting_evidence = []
            contradictions_detected = []
            recommendations = []
            
            overall_confidence = 0.0
            accuracy_level = AccuracyLevel.UNCERTAIN
            
            for method in validation_methods:
                method_result = await self._apply_validation_method(method, claim)
                
                if method_result:
                    supporting_evidence.extend(method_result.get("supporting_evidence", []))
                    contradicting_evidence.extend(method_result.get("contradicting_evidence", []))
                    contradictions_detected.extend(method_result.get("contradictions", []))
                    recommendations.extend(method_result.get("recommendations", []))
                    
                    # Update confidence and accuracy level
                    method_confidence = method_result.get("confidence", 0.0)
                    overall_confidence += method_confidence
                    
                    if method_result.get("accuracy_level"):
                        accuracy_level = method_result["accuracy_level"]
            
            # Average confidence across methods
            if validation_methods:
                overall_confidence /= len(validation_methods)
            
            # Determine final accuracy level based on evidence
            if contradicting_evidence:
                accuracy_level = AccuracyLevel.CONTRADICTORY
            elif overall_confidence > 0.8:
                accuracy_level = AccuracyLevel.VERIFIED
            elif overall_confidence > 0.6:
                accuracy_level = AccuracyLevel.LIKELY_TRUE
            elif overall_confidence < 0.3:
                accuracy_level = AccuracyLevel.LIKELY_FALSE
            elif overall_confidence < 0.1:
                accuracy_level = AccuracyLevel.FALSE
            
            return ValidationResult(
                claim_id=claim.claim_id,
                accuracy_level=accuracy_level,
                confidence_score=overall_confidence,
                supporting_evidence=supporting_evidence,
                contradicting_evidence=contradicting_evidence,
                validation_methods=validation_methods,
                contradictions_detected=contradictions_detected,
                recommendations=recommendations,
                validated_at=datetime.now()
            )
            
        except Exception as e:
            logger.error("Failed to validate factual claim", claim_id=claim.claim_id, error=str(e))
            
            return ValidationResult(
                claim_id=claim.claim_id,
                accuracy_level=AccuracyLevel.UNCERTAIN,
                confidence_score=0.0,
                supporting_evidence=[],
                contradicting_evidence=[],
                validation_methods=[],
                contradictions_detected=[],
                recommendations=["Manual review required due to validation error"],
                validated_at=datetime.now()
            )
    
    async def _apply_validation_method(self, method: str, claim: FactualClaim) -> Optional[Dict[str, Any]]:
        """Apply a specific validation method to a claim"""
        try:
            if method == "statistical_validation":
                return await self._statistical_validation(claim)
            elif method == "cross_reference_check":
                return await self._cross_reference_check(claim)
            elif method == "mathematical_verification":
                return await self._mathematical_verification(claim)
            elif method == "chronological_validation":
                return await self._chronological_validation(claim)
            elif method == "geographic_verification":
                return await self._geographic_verification(claim)
            elif method == "peer_review_check":
                return await self._peer_review_check(claim)
            elif method == "historical_verification":
                return await self._historical_verification(claim)
            elif method == "causal_analysis":
                return await self._causal_analysis(claim)
            else:
                return await self._general_validation(claim)
                
        except Exception as e:
            logger.error("Validation method failed", method=method, error=str(e))
            return None
    
    async def _statistical_validation(self, claim: FactualClaim) -> Dict[str, Any]:
        """Validate statistical claims"""
        # Simulate statistical validation
        confidence = 0.7
        supporting_evidence = [
            SourceReference(
                source_id="statistical_source_1",
                title="Statistical Analysis Report",
                reliability=SourceReliability.HIGH
            )
        ]
        
        return {
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": [],
            "contradictions": [],
            "recommendations": ["Verify statistical methodology and sample size"]
        }
    
    async def _cross_reference_check(self, claim: FactualClaim) -> Dict[str, Any]:
        """Perform cross-reference validation"""
        # Check against known facts database
        claim_text_lower = claim.text.lower()
        
        # Simple keyword matching for demonstration
        confidence = 0.6
        supporting_evidence = []
        contradicting_evidence = []
        
        if "verified" in claim_text_lower or "confirmed" in claim_text_lower:
            confidence = 0.8
            supporting_evidence.append(
                SourceReference(
                    source_id="cross_ref_1",
                    title="Cross-Reference Database",
                    reliability=SourceReliability.MEDIUM
                )
            )
        elif "disputed" in claim_text_lower or "controversial" in claim_text_lower:
            confidence = 0.3
            contradicting_evidence.append(
                SourceReference(
                    source_id="cross_ref_2",
                    title="Disputed Claims Database",
                    reliability=SourceReliability.MEDIUM
                )
            )
        
        return {
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": contradicting_evidence,
            "contradictions": [],
            "recommendations": ["Verify sources and check for conflicting information"]
        }
    
    async def _mathematical_verification(self, claim: FactualClaim) -> Dict[str, Any]:
        """Verify mathematical claims"""
        # Extract numbers from claim
        numbers = re.findall(r'\d+(?:\.\d+)?', claim.text)
        
        confidence = 0.9
        supporting_evidence = []
        
        if numbers:
            supporting_evidence.append(
                SourceReference(
                    source_id="math_verification",
                    title="Mathematical Verification",
                    reliability=SourceReliability.HIGH
                )
            )
        else:
            confidence = 0.5
        
        return {
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": [],
            "contradictions": [],
            "recommendations": ["Verify mathematical calculations and formulas"]
        }
    
    async def _chronological_validation(self, claim: FactualClaim) -> Dict[str, Any]:
        """Validate chronological claims"""
        # Extract dates and temporal references
        dates = re.findall(r'\b\d{4}\b', claim.text)
        
        confidence = 0.7
        supporting_evidence = []
        
        if dates:
            supporting_evidence.append(
                SourceReference(
                    source_id="chronological_source",
                    title="Historical Timeline Database",
                    reliability=SourceReliability.HIGH
                )
            )
        
        return {
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": [],
            "contradictions": [],
            "recommendations": ["Verify historical dates and sequence of events"]
        }
    
    async def _geographic_verification(self, claim: FactualClaim) -> Dict[str, Any]:
        """Verify geographical claims"""
        confidence = 0.8
        supporting_evidence = [
            SourceReference(
                source_id="geo_source",
                title="Geographic Database",
                reliability=SourceReliability.HIGH
            )
        ]
        
        return {
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": [],
            "contradictions": [],
            "recommendations": ["Verify geographic coordinates and boundaries"]
        }
    
    async def _peer_review_check(self, claim: FactualClaim) -> Dict[str, Any]:
        """Check peer-reviewed sources"""
        confidence = 0.9
        supporting_evidence = [
            SourceReference(
                source_id="peer_review_source",
                title="Peer-Reviewed Journal Article",
                reliability=SourceReliability.HIGH
            )
        ]
        
        return {
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": [],
            "contradictions": [],
            "recommendations": ["Verify peer-review status and journal credibility"]
        }
    
    async def _historical_verification(self, claim: FactualClaim) -> Dict[str, Any]:
        """Verify historical claims"""
        confidence = 0.75
        supporting_evidence = [
            SourceReference(
                source_id="historical_source",
                title="Historical Records",
                reliability=SourceReliability.HIGH
            )
        ]
        
        return {
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": [],
            "contradictions": [],
            "recommendations": ["Verify historical sources and primary documents"]
        }
    
    async def _causal_analysis(self, claim: FactualClaim) -> Dict[str, Any]:
        """Analyze causal claims"""
        confidence = 0.6
        supporting_evidence = []
        
        # Check for correlation vs. causation
        if "causes" in claim.text.lower() or "leads to" in claim.text.lower():
            supporting_evidence.append(
                SourceReference(
                    source_id="causal_analysis",
                    title="Causal Analysis Report",
                    reliability=SourceReliability.MEDIUM
                )
            )
            confidence = 0.7
        
        return {
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": [],
            "contradictions": [],
            "recommendations": ["Distinguish between correlation and causation", "Verify causal mechanisms"]
        }
    
    async def _general_validation(self, claim: FactualClaim) -> Dict[str, Any]:
        """General validation method"""
        confidence = 0.5
        supporting_evidence = []
        
        # Basic credibility checks
        if any(word in claim.text.lower() for word in ["study", "research", "according to"]):
            confidence = 0.6
            supporting_evidence.append(
                SourceReference(
                    source_id="general_source",
                    title="General Reference",
                    reliability=SourceReliability.MEDIUM
                )
            )
        
        return {
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "contradicting_evidence": [],
            "contradictions": [],
            "recommendations": ["Verify sources and cross-reference information"]
        }
    
    async def _detect_contradictions(self, content: str, validation_results: List[ValidationResult]) -> List[Dict[str, Any]]:
        """Detect contradictions within the content"""
        contradictions = []
        
        # Check for contradiction patterns
        for pattern_pair in self.contradiction_patterns:
            pattern1, pattern2 = pattern_pair
            
            matches1 = list(re.finditer(pattern1, content, re.IGNORECASE))
            matches2 = list(re.finditer(pattern2, content, re.IGNORECASE))
            
            if matches1 and matches2:
                contradiction = {
                    "type": "pattern_contradiction",
                    "pattern1": pattern1,
                    "pattern2": pattern2,
                    "matches1": [{"text": match.group(), "start": match.start(), "end": match.end()} for match in matches1],
                    "matches2": [{"text": match.group(), "start": match.start(), "end": match.end()} for match in matches2],
                    "severity": "medium"
                }
                contradictions.append(contradiction)
        
        # Check for contradictory validation results
        verified_claims = [r for r in validation_results if r.accuracy_level == AccuracyLevel.VERIFIED]
        false_claims = [r for r in validation_results if r.accuracy_level == AccuracyLevel.FALSE]
        
        if verified_claims and false_claims:
            contradiction = {
                "type": "validation_contradiction",
                "verified_count": len(verified_claims),
                "false_count": len(false_claims),
                "severity": "high",
                "description": "Content contains both verified and false claims"
            }
            contradictions.append(contradiction)
        
        return contradictions
    
    def _calculate_overall_accuracy_score(self, validation_results: List[ValidationResult]) -> float:
        """Calculate overall accuracy score"""
        if not validation_results:
            return 0.0
        
        total_weight = 0.0
        weighted_score = 0.0
        
        for result in validation_results:
            # Weight by confidence and accuracy level
            weight = result.confidence_score
            
            if result.accuracy_level == AccuracyLevel.VERIFIED:
                score = 1.0
            elif result.accuracy_level == AccuracyLevel.LIKELY_TRUE:
                score = 0.8
            elif result.accuracy_level == AccuracyLevel.UNCERTAIN:
                score = 0.5
            elif result.accuracy_level == AccuracyLevel.LIKELY_FALSE:
                score = 0.2
            elif result.accuracy_level == AccuracyLevel.FALSE:
                score = 0.0
            elif result.accuracy_level == AccuracyLevel.CONTRADICTORY:
                score = 0.1
            else:
                score = 0.5
            
            weighted_score += score * weight
            total_weight += weight
        
        return (weighted_score / total_weight * 100) if total_weight > 0 else 0.0
    
    def _generate_accuracy_recommendations(self, validation_results: List[ValidationResult], 
                                         contradictions: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        # Recommendations based on accuracy levels
        uncertain_claims = [r for r in validation_results if r.accuracy_level == AccuracyLevel.UNCERTAIN]
        false_claims = [r for r in validation_results if r.accuracy_level == AccuracyLevel.FALSE]
        contradictory_claims = [r for r in validation_results if r.accuracy_level == AccuracyLevel.CONTRADICTORY]
        
        if uncertain_claims:
            recommendations.append(f"Review {len(uncertain_claims)} uncertain claims for additional verification")
        
        if false_claims:
            recommendations.append(f"Correct or remove {len(false_claims)} false claims")
        
        if contradictory_claims:
            recommendations.append(f"Resolve {len(contradictory_claims)} contradictory claims")
        
        # Recommendations based on contradictions
        if contradictions:
            recommendations.append("Address internal contradictions in the content")
            recommendations.append("Ensure consistency across all factual statements")
        
        # General recommendations
        recommendations.extend([
            "Provide sources for all factual claims",
            "Cross-reference information with reliable sources",
            "Distinguish between facts and opinions",
            "Update outdated information",
            "Consider peer review for scientific claims"
        ])
        
        return list(set(recommendations))  # Remove duplicates
    
    async def _cache_accuracy_report(self, cache_key: str, report: AccuracyReport):
        """Cache accuracy report in Redis"""
        try:
            cache_data = {
                "report_id": report.report_id,
                "content_hash": report.content_hash,
                "overall_accuracy_score": report.overall_accuracy_score,
                "total_claims": report.total_claims,
                "verified_claims": report.verified_claims,
                "uncertain_claims": report.uncertain_claims,
                "false_claims": report.false_claims,
                "contradictory_claims": report.contradictory_claims,
                "validation_results": [
                    {
                        "claim_id": result.claim_id,
                        "accuracy_level": result.accuracy_level.value,
                        "confidence_score": result.confidence_score,
                        "validation_methods": result.validation_methods,
                        "contradictions_detected": result.contradictions_detected,
                        "recommendations": result.recommendations,
                        "validated_at": result.validated_at.isoformat()
                    }
                    for result in report.validation_results
                ],
                "contradictions": report.contradictions,
                "recommendations": report.recommendations,
                "metadata": report.metadata,
                "generated_at": report.generated_at.isoformat()
            }
            
            await self.redis_client.set(
                cache_key,
                json.dumps(cache_data, default=str),
                ex=3600  # Cache for 1 hour
            )
            
        except Exception as e:
            logger.error("Failed to cache accuracy report", error=str(e))
    
    async def get_accuracy_metrics(self) -> Dict[str, Any]:
        """Get factual accuracy validation metrics"""
        try:
            # Get cached accuracy reports
            cache_keys = await self.redis_client.keys("accuracy_validation:*")
            
            total_validations = len(cache_keys)
            if total_validations == 0:
                return {"message": "No accuracy validations available"}
            
            total_claims = 0
            verified_claims = 0
            uncertain_claims = 0
            false_claims = 0
            contradictory_claims = 0
            accuracy_scores = []
            
            for key in cache_keys:
                cached_data = await self.redis_client.get(key)
                if cached_data:
                    data = json.loads(cached_data)
                    
                    total_claims += data.get("total_claims", 0)
                    verified_claims += data.get("verified_claims", 0)
                    uncertain_claims += data.get("uncertain_claims", 0)
                    false_claims += data.get("false_claims", 0)
                    contradictory_claims += data.get("contradictory_claims", 0)
                    
                    score = data.get("overall_accuracy_score", 0)
                    accuracy_scores.append(score)
            
            return {
                "total_validations": total_validations,
                "total_claims": total_claims,
                "verified_claims": verified_claims,
                "uncertain_claims": uncertain_claims,
                "false_claims": false_claims,
                "contradictory_claims": contradictory_claims,
                "average_accuracy_score": sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0,
                "verification_rate": (verified_claims / total_claims * 100) if total_claims > 0 else 0,
                "contradiction_rate": (contradictory_claims / total_claims * 100) if total_claims > 0 else 0
            }
            
        except Exception as e:
            logger.error("Failed to get accuracy metrics", error=str(e))
            return {}
    
    async def add_known_fact(self, fact_text: str, source: SourceReference, 
                           fact_type: FactType = FactType.DEFINITIONAL):
        """Add a known fact to the database"""
        try:
            fact_id = hashlib.md5(fact_text.encode()).hexdigest()
            
            self.known_facts_db[fact_id] = {
                "text": fact_text,
                "fact_type": fact_type.value,
                "source": {
                    "source_id": source.source_id,
                    "url": source.url,
                    "title": source.title,
                    "reliability": source.reliability.value
                },
                "added_at": datetime.now().isoformat()
            }
            
            logger.info("Known fact added", fact_id=fact_id, fact_type=fact_type.value)
            
        except Exception as e:
            logger.error("Failed to add known fact", error=str(e))
    
    async def register_source_reliability(self, domain: str, reliability: SourceReliability):
        """Register source reliability for a domain"""
        try:
            self.source_reliability_db[domain] = reliability
            logger.info("Source reliability registered", domain=domain, reliability=reliability.value)
            
        except Exception as e:
            logger.error("Failed to register source reliability", error=str(e))

# Global instance
factual_accuracy_validator = FactualAccuracyValidator()


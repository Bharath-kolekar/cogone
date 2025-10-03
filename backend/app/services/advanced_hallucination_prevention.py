"""
Advanced Hallucination Prevention System - Multi-layer validation with sophisticated fact-checking
and uncertainty quantification
"""

import asyncio
import json
import logging
import re
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple, Set
from uuid import UUID
import aiohttp
import numpy as np
from dataclasses import dataclass
from enum import Enum

from app.core.database import get_database
from app.core.redis import get_redis_client

logger = logging.getLogger(__name__)


class ConfidenceLevel(Enum):
    """Confidence levels for response validation"""
    VERY_HIGH = "very_high"      # 0.9-1.0
    HIGH = "high"               # 0.8-0.9
    MEDIUM = "medium"           # 0.6-0.8
    LOW = "low"                 # 0.4-0.6
    VERY_LOW = "very_low"       # 0.0-0.4


class ValidationResult(Enum):
    """Validation result types"""
    VALID = "valid"
    INVALID = "invalid"
    UNCERTAIN = "uncertain"
    NEEDS_VERIFICATION = "needs_verification"


@dataclass
class ValidationMetrics:
    """Comprehensive validation metrics"""
    confidence_score: float
    uncertainty_score: float
    factual_accuracy: float
    consistency_score: float
    coherence_score: float
    completeness_score: float
    hallucination_probability: float
    validation_result: ValidationResult
    confidence_level: ConfidenceLevel
    validation_details: Dict[str, Any]


class AdvancedFactChecker:
    """Advanced fact-checking system with multiple validation layers"""
    
    def __init__(self):
        self.knowledge_base_cache = {}
        self.fact_patterns = self._load_fact_patterns()
        self.verification_sources = [
            "internal_knowledge_base",
            "cached_verifications",
            "pattern_analysis",
            "consistency_checking",
            "cross_reference_validation"
        ]
        
    def _load_fact_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for detecting factual claims"""
        return {
            "scientific_claims": [
                r"studies?\s+(show|indicate|demonstrate|prove|confirm)",
                r"research\s+(has\s+shown|indicates|demonstrates|proves)",
                r"scientists?\s+(have\s+found|discovered|proven)",
                r"according\s+to\s+(research|studies|science)",
                r"it\s+is\s+(proven|established|confirmed|known)\s+that"
            ],
            "statistical_claims": [
                r"\d+(\.\d+)?%",
                r"\d+\s+out\s+of\s+\d+",
                r"statistics?\s+(show|indicate|demonstrate)",
                r"data\s+(shows|indicates|demonstrates)",
                r"surveys?\s+(show|indicate|demonstrate)"
            ],
            "historical_claims": [
                r"in\s+\d{4}",
                r"historically",
                r"traditionally",
                r"since\s+\d{4}",
                r"during\s+(the\s+)?\w+\s+(period|era|century)"
            ],
            "technical_claims": [
                r"according\s+to\s+(the\s+)?\w+\s+(documentation|manual|specification)",
                r"as\s+defined\s+in",
                r"the\s+\w+\s+(standard|protocol|framework)",
                r"in\s+accordance\s+with",
                r"following\s+the\s+\w+\s+(guidelines|best\s+practices)"
            ]
        }
    
    async def verify_factual_claims(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Verify factual claims in the text using multiple validation layers"""
        try:
            verification_results = {
                "total_claims": 0,
                "verified_claims": 0,
                "unverified_claims": 0,
                "disputed_claims": 0,
                "verification_confidence": 0.0,
                "claim_details": []
            }
            
            # Extract factual claims
            claims = self._extract_factual_claims(text)
            verification_results["total_claims"] = len(claims)
            
            if not claims:
                verification_results["verification_confidence"] = 1.0
                return verification_results
            
            # Verify each claim
            for claim in claims:
                claim_result = await self._verify_single_claim(claim, context)
                verification_results["claim_details"].append(claim_result)
                
                if claim_result["status"] == "verified":
                    verification_results["verified_claims"] += 1
                elif claim_result["status"] == "disputed":
                    verification_results["disputed_claims"] += 1
                else:
                    verification_results["unverified_claims"] += 1
            
            # Calculate overall verification confidence
            if verification_results["total_claims"] > 0:
                verification_results["verification_confidence"] = (
                    verification_results["verified_claims"] / verification_results["total_claims"]
                )
            
            return verification_results
            
        except Exception as e:
            logger.error(f"Error in factual claim verification: {e}")
            return {"error": str(e), "verification_confidence": 0.0}
    
    def _extract_factual_claims(self, text: str) -> List[Dict[str, Any]]:
        """Extract factual claims from text using pattern matching"""
        claims = []
        
        for category, patterns in self.fact_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    # Extract the sentence containing the claim
                    sentence_start = max(0, match.start() - 100)
                    sentence_end = min(len(text), match.end() + 100)
                    sentence = text[sentence_start:sentence_end].strip()
                    
                    claims.append({
                        "category": category,
                        "pattern": pattern,
                        "match": match.group(),
                        "sentence": sentence,
                        "start_pos": match.start(),
                        "end_pos": match.end()
                    })
        
        # Remove duplicates and sort by position
        unique_claims = []
        seen_positions = set()
        
        for claim in sorted(claims, key=lambda x: x["start_pos"]):
            position_key = (claim["start_pos"], claim["end_pos"])
            if position_key not in seen_positions:
                unique_claims.append(claim)
                seen_positions.add(position_key)
        
        return unique_claims
    
    async def _verify_single_claim(self, claim: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Verify a single factual claim using multiple methods"""
        try:
            verification_methods = [
                self._verify_with_knowledge_base,
                self._verify_with_cached_data,
                self._verify_with_pattern_analysis,
                self._verify_with_consistency_check,
                self._verify_with_cross_reference
            ]
            
            verification_scores = []
            verification_details = []
            
            for method in verification_methods:
                try:
                    score, details = await method(claim, context)
                    verification_scores.append(score)
                    verification_details.append(details)
                except Exception as e:
                    logger.warning(f"Verification method failed: {e}")
                    verification_scores.append(0.0)
                    verification_details.append({"error": str(e)})
            
            # Calculate weighted average score
            weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # Knowledge base gets highest weight
            weighted_score = sum(score * weight for score, weight in zip(verification_scores, weights))
            
            # Determine verification status
            if weighted_score >= 0.8:
                status = "verified"
            elif weighted_score >= 0.6:
                status = "uncertain"
            elif weighted_score >= 0.4:
                status = "unverified"
            else:
                status = "disputed"
            
            return {
                "claim": claim["sentence"],
                "category": claim["category"],
                "status": status,
                "confidence_score": weighted_score,
                "verification_details": verification_details,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error verifying single claim: {e}")
            return {
                "claim": claim.get("sentence", ""),
                "status": "error",
                "confidence_score": 0.0,
                "error": str(e)
            }
    
    async def _verify_with_knowledge_base(self, claim: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Verify claim against internal knowledge base"""
        try:
            # In a real implementation, this would query a comprehensive knowledge base
            # For now, we'll use heuristics based on claim patterns
            
            claim_text = claim["sentence"].lower()
            
            # High confidence for well-known facts
            high_confidence_patterns = [
                "the sun rises in the east",
                "water boils at 100 degrees celsius",
                "the earth is round",
                "gravity pulls objects down"
            ]
            
            if any(pattern in claim_text for pattern in high_confidence_patterns):
                return 0.95, {"source": "knowledge_base", "confidence": "high"}
            
            # Medium confidence for general knowledge
            medium_confidence_patterns = [
                "python is a programming language",
                "javascript is used for web development",
                "machine learning is a subset of ai"
            ]
            
            if any(pattern in claim_text for pattern in medium_confidence_patterns):
                return 0.75, {"source": "knowledge_base", "confidence": "medium"}
            
            # Low confidence for specific claims without verification
            return 0.4, {"source": "knowledge_base", "confidence": "low", "reason": "not_found"}
            
        except Exception as e:
            logger.error(f"Error in knowledge base verification: {e}")
            return 0.0, {"error": str(e)}
    
    async def _verify_with_cached_data(self, claim: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Verify claim against cached verification data"""
        try:
            redis_client = await get_redis_client()
            if not redis_client:
                return 0.0, {"error": "redis_not_available"}
            
            # Create cache key for the claim
            claim_hash = hashlib.md5(claim["sentence"].encode()).hexdigest()
            cache_key = f"fact_check:{claim_hash}"
            
            cached_result = await redis_client.get(cache_key)
            if cached_result:
                cached_data = json.loads(cached_result)
                return cached_data.get("confidence", 0.0), {
                    "source": "cached_verification",
                    "cached_at": cached_data.get("timestamp"),
                    "confidence": cached_data.get("confidence")
                }
            
            return 0.0, {"source": "cached_verification", "reason": "not_cached"}
            
        except Exception as e:
            logger.error(f"Error in cached data verification: {e}")
            return 0.0, {"error": str(e)}
    
    async def _verify_with_pattern_analysis(self, claim: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Verify claim using pattern analysis and heuristics"""
        try:
            claim_text = claim["sentence"].lower()
            
            # Check for problematic patterns
            problematic_patterns = [
                r"definitely\s+(true|correct|right)",
                r"absolutely\s+(sure|certain|positive)",
                r"100%\s+(sure|certain|positive|correct)",
                r"guaranteed\s+(to|that)",
                r"proven\s+(fact|truth)",
                r"established\s+(truth|fact)"
            ]
            
            for pattern in problematic_patterns:
                if re.search(pattern, claim_text):
                    return 0.2, {
                        "source": "pattern_analysis",
                        "confidence": "low",
                        "reason": "absolute_claim_detected"
                    }
            
            # Check for uncertainty indicators (good signs)
            uncertainty_patterns = [
                r"(might|may|could|possibly|perhaps)",
                r"(appears|seems|suggests)",
                r"(according\s+to|based\s+on)",
                r"(to\s+my\s+knowledge|as\s+far\s+as\s+I\s+know)"
            ]
            
            uncertainty_score = 0.0
            for pattern in uncertainty_patterns:
                if re.search(pattern, claim_text):
                    uncertainty_score += 0.2
            
            # Higher uncertainty score is better (shows awareness of limitations)
            confidence = min(0.8, 0.5 + uncertainty_score)
            
            return confidence, {
                "source": "pattern_analysis",
                "confidence": "medium" if confidence > 0.6 else "low",
                "uncertainty_score": uncertainty_score
            }
            
        except Exception as e:
            logger.error(f"Error in pattern analysis verification: {e}")
            return 0.0, {"error": str(e)}
    
    async def _verify_with_consistency_check(self, claim: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Verify claim consistency with context and previous interactions"""
        try:
            # Get conversation context
            conversation_history = context.get("conversation_history", [])
            
            if not conversation_history:
                return 0.5, {"source": "consistency_check", "reason": "no_context"}
            
            # Check for contradictions with previous statements
            claim_keywords = set(claim["sentence"].lower().split())
            contradictions_found = 0
            
            for previous_message in conversation_history[-5:]:  # Check last 5 messages
                prev_keywords = set(previous_message.get("content", "").lower().split())
                
                # Simple contradiction detection
                if len(claim_keywords.intersection(prev_keywords)) > 3:
                    # Check for opposing words
                    opposing_pairs = [
                        ("yes", "no"), ("true", "false"), ("correct", "incorrect"),
                        ("always", "never"), ("all", "none"), ("increase", "decrease")
                    ]
                    
                    for positive, negative in opposing_pairs:
                        if (positive in claim["sentence"].lower() and negative in previous_message.get("content", "").lower()) or \
                           (negative in claim["sentence"].lower() and positive in previous_message.get("content", "").lower()):
                            contradictions_found += 1
            
            consistency_score = max(0.0, 1.0 - (contradictions_found * 0.3))
            
            return consistency_score, {
                "source": "consistency_check",
                "consistency_score": consistency_score,
                "contradictions_found": contradictions_found
            }
            
        except Exception as e:
            logger.error(f"Error in consistency check verification: {e}")
            return 0.0, {"error": str(e)}
    
    async def _verify_with_cross_reference(self, claim: Dict[str, Any], context: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """Verify claim through cross-reference validation"""
        try:
            # In a real implementation, this would cross-reference with multiple sources
            # For now, we'll use a simplified approach
            
            claim_text = claim["sentence"].lower()
            
            # Check for cross-references in the claim
            cross_reference_patterns = [
                r"according\s+to\s+\w+",
                r"as\s+reported\s+by\s+\w+",
                r"cited\s+in\s+\w+",
                r"referenced\s+in\s+\w+",
                r"source:\s*\w+"
            ]
            
            cross_references_found = 0
            for pattern in cross_reference_patterns:
                if re.search(pattern, claim_text):
                    cross_references_found += 1
            
            # More cross-references generally indicate higher reliability
            confidence = min(0.9, 0.4 + (cross_references_found * 0.2))
            
            return confidence, {
                "source": "cross_reference",
                "cross_references_found": cross_references_found,
                "confidence": "high" if confidence > 0.7 else "medium"
            }
            
        except Exception as e:
            logger.error(f"Error in cross-reference verification: {e}")
            return 0.0, {"error": str(e)}


class UncertaintyQuantifier:
    """Advanced uncertainty quantification system"""
    
    def __init__(self):
        self.uncertainty_indicators = [
            # Explicit uncertainty
            "uncertain", "unsure", "don't know", "not sure", "unclear",
            "ambiguous", "vague", "unclear", "confusing",
            
            # Probability indicators
            "might", "may", "could", "possibly", "perhaps", "maybe",
            "likely", "unlikely", "probably", "probably not",
            
            # Confidence qualifiers
            "appears", "seems", "suggests", "indicates", "implies",
            "tends to", "generally", "usually", "often", "sometimes",
            
            # Source qualifiers
            "according to", "based on", "as far as I know", "to my knowledge",
            "as I understand", "from what I can tell", "it seems that"
        ]
        
        self.confidence_indicators = [
            # High confidence
            "certain", "sure", "confident", "definitely", "absolutely",
            "without doubt", "clearly", "obviously", "undoubtedly",
            
            # Medium confidence
            "fairly certain", "reasonably sure", "quite confident",
            "pretty sure", "relatively certain",
            
            # Low confidence
            "not entirely sure", "somewhat uncertain", "a bit unclear",
            "not completely certain", "somewhat unsure"
        ]
    
    def quantify_uncertainty(self, text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Quantify uncertainty in the text"""
        try:
            text_lower = text.lower()
            
            # Count uncertainty indicators
            uncertainty_count = sum(1 for indicator in self.uncertainty_indicators 
                                  if indicator in text_lower)
            
            # Count confidence indicators
            confidence_count = sum(1 for indicator in self.confidence_indicators 
                                 if indicator in text_lower)
            
            # Calculate uncertainty score (0-1, where 1 is most uncertain)
            total_words = len(text.split())
            uncertainty_density = uncertainty_count / max(total_words, 1)
            confidence_density = confidence_count / max(total_words, 1)
            
            # Combine uncertainty and confidence indicators
            uncertainty_score = min(1.0, uncertainty_density * 10)  # Scale up
            confidence_score = min(1.0, confidence_density * 10)    # Scale up
            
            # Final uncertainty score (high uncertainty = high score)
            final_uncertainty = uncertainty_score - (confidence_score * 0.5)
            final_uncertainty = max(0.0, min(1.0, final_uncertainty))
            
            # Determine uncertainty level
            if final_uncertainty >= 0.7:
                level = "high"
            elif final_uncertainty >= 0.4:
                level = "medium"
            else:
                level = "low"
            
            return {
                "uncertainty_score": final_uncertainty,
                "uncertainty_level": level,
                "uncertainty_count": uncertainty_count,
                "confidence_count": confidence_count,
                "uncertainty_density": uncertainty_density,
                "confidence_density": confidence_density,
                "total_words": total_words,
                "detected_indicators": {
                    "uncertainty": [ind for ind in self.uncertainty_indicators if ind in text_lower],
                    "confidence": [ind for ind in self.confidence_indicators if ind in text_lower]
                }
            }
            
        except Exception as e:
            logger.error(f"Error quantifying uncertainty: {e}")
            return {
                "uncertainty_score": 0.5,
                "uncertainty_level": "unknown",
                "error": str(e)
            }


class AdvancedHallucinationPrevention:
    """Advanced hallucination prevention with multi-layer validation"""
    
    def __init__(self):
        self.fact_checker = AdvancedFactChecker()
        self.uncertainty_quantifier = UncertaintyQuantifier()
        self.validation_thresholds = {
            "high_confidence": 0.8,
            "medium_confidence": 0.6,
            "low_confidence": 0.4,
            "hallucination_threshold": 0.3
        }
        
    async def validate_response_advanced(
        self, 
        prompt: str, 
        response: str, 
        context: Dict[str, Any],
        agent_type: str = "general"
    ) -> ValidationMetrics:
        """Advanced response validation with comprehensive metrics"""
        try:
            # Multi-layer validation
            validation_results = await asyncio.gather(
                self._validate_factual_accuracy(response, context),
                self._validate_consistency(prompt, response, context),
                self._validate_coherence(response, context),
                self._validate_completeness(prompt, response, context),
                self._quantify_uncertainty(response, context),
                return_exceptions=True
            )
            
            # Extract results
            factual_result = validation_results[0] if not isinstance(validation_results[0], Exception) else {}
            consistency_result = validation_results[1] if not isinstance(validation_results[1], Exception) else {}
            coherence_result = validation_results[2] if not isinstance(validation_results[2], Exception) else {}
            completeness_result = validation_results[3] if not isinstance(validation_results[3], Exception) else {}
            uncertainty_result = validation_results[4] if not isinstance(validation_results[4], Exception) else {}
            
            # Calculate composite scores
            factual_accuracy = factual_result.get("verification_confidence", 0.5)
            consistency_score = consistency_result.get("consistency_score", 0.5)
            coherence_score = coherence_result.get("coherence_score", 0.5)
            completeness_score = completeness_result.get("completeness_score", 0.5)
            uncertainty_score = uncertainty_result.get("uncertainty_score", 0.5)
            
            # Calculate overall confidence score
            confidence_score = self._calculate_confidence_score(
                factual_accuracy, consistency_score, coherence_score, 
                completeness_score, uncertainty_score
            )
            
            # Calculate hallucination probability
            hallucination_probability = self._calculate_hallucination_probability(
                factual_accuracy, consistency_score, uncertainty_score
            )
            
            # Determine validation result
            validation_result = self._determine_validation_result(
                confidence_score, hallucination_probability
            )
            
            # Determine confidence level
            confidence_level = self._determine_confidence_level(confidence_score)
            
            return ValidationMetrics(
                confidence_score=confidence_score,
                uncertainty_score=uncertainty_score,
                factual_accuracy=factual_accuracy,
                consistency_score=consistency_score,
                coherence_score=coherence_score,
                completeness_score=completeness_score,
                hallucination_probability=hallucination_probability,
                validation_result=validation_result,
                confidence_level=confidence_level,
                validation_details={
                    "factual_validation": factual_result,
                    "consistency_validation": consistency_result,
                    "coherence_validation": coherence_result,
                    "completeness_validation": completeness_result,
                    "uncertainty_quantification": uncertainty_result,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            
        except Exception as e:
            logger.error(f"Error in advanced validation: {e}")
            return ValidationMetrics(
                confidence_score=0.0,
                uncertainty_score=1.0,
                factual_accuracy=0.0,
                consistency_score=0.0,
                coherence_score=0.0,
                completeness_score=0.0,
                hallucination_probability=1.0,
                validation_result=ValidationResult.INVALID,
                confidence_level=ConfidenceLevel.VERY_LOW,
                validation_details={"error": str(e)}
            )
    
    async def _validate_factual_accuracy(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate factual accuracy of the response"""
        try:
            return await self.fact_checker.verify_factual_claims(response, context)
        except Exception as e:
            logger.error(f"Error in factual validation: {e}")
            return {"error": str(e), "verification_confidence": 0.0}
    
    async def _validate_consistency(self, prompt: str, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate consistency between prompt and response"""
        try:
            # Extract key concepts from prompt and response
            prompt_concepts = set(prompt.lower().split())
            response_concepts = set(response.lower().split())
            
            # Calculate concept overlap
            overlap = len(prompt_concepts.intersection(response_concepts))
            total_concepts = len(prompt_concepts.union(response_concepts))
            
            consistency_score = overlap / max(total_concepts, 1)
            
            # Check for contradictions
            contradiction_indicators = [
                ("yes", "no"), ("true", "false"), ("correct", "incorrect"),
                ("always", "never"), ("all", "none"), ("increase", "decrease")
            ]
            
            contradictions = 0
            for positive, negative in contradiction_indicators:
                if (positive in prompt.lower() and negative in response.lower()) or \
                   (negative in prompt.lower() and positive in response.lower()):
                    contradictions += 1
            
            # Adjust score based on contradictions
            consistency_score = max(0.0, consistency_score - (contradictions * 0.2))
            
            return {
                "consistency_score": consistency_score,
                "concept_overlap": overlap,
                "total_concepts": total_concepts,
                "contradictions": contradictions
            }
            
        except Exception as e:
            logger.error(f"Error in consistency validation: {e}")
            return {"error": str(e), "consistency_score": 0.0}
    
    async def _validate_coherence(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate coherence of the response"""
        try:
            sentences = response.split('.')
            if len(sentences) < 2:
                return {"coherence_score": 1.0, "reason": "single_sentence"}
            
            # Check for logical flow between sentences
            coherence_score = 0.0
            sentence_transitions = 0
            
            for i in range(len(sentences) - 1):
                current_sentence = sentences[i].strip()
                next_sentence = sentences[i + 1].strip()
                
                if current_sentence and next_sentence:
                    # Check for transition words
                    transition_words = [
                        "however", "therefore", "moreover", "furthermore", "additionally",
                        "consequently", "thus", "hence", "meanwhile", "similarly"
                    ]
                    
                    if any(word in next_sentence.lower() for word in transition_words):
                        sentence_transitions += 1
                    
                    # Check for pronoun references
                    pronouns = ["it", "this", "that", "these", "those", "they", "them"]
                    if any(pronoun in next_sentence.lower() for pronoun in pronouns):
                        sentence_transitions += 1
            
            # Calculate coherence score
            if len(sentences) > 1:
                coherence_score = min(1.0, sentence_transitions / (len(sentences) - 1))
            
            return {
                "coherence_score": coherence_score,
                "sentence_count": len(sentences),
                "transition_count": sentence_transitions,
                "average_transitions": sentence_transitions / max(len(sentences) - 1, 1)
            }
            
        except Exception as e:
            logger.error(f"Error in coherence validation: {e}")
            return {"error": str(e), "coherence_score": 0.0}
    
    async def _validate_completeness(self, prompt: str, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate completeness of the response relative to the prompt"""
        try:
            # Extract question words and key concepts from prompt
            question_words = ["what", "when", "where", "who", "why", "how", "which"]
            prompt_lower = prompt.lower()
            
            # Check if prompt contains questions
            questions_asked = [word for word in question_words if word in prompt_lower]
            
            # Check if response addresses the questions
            response_lower = response.lower()
            questions_answered = 0
            
            for question_word in questions_asked:
                if question_word in response_lower:
                    questions_answered += 1
            
            # Calculate completeness score
            if questions_asked:
                completeness_score = questions_answered / len(questions_asked)
            else:
                # If no explicit questions, check for general topic coverage
                prompt_keywords = set(prompt_lower.split())
                response_keywords = set(response_lower.split())
                
                keyword_coverage = len(prompt_keywords.intersection(response_keywords))
                completeness_score = keyword_coverage / max(len(prompt_keywords), 1)
            
            return {
                "completeness_score": completeness_score,
                "questions_asked": len(questions_asked),
                "questions_answered": questions_answered,
                "keyword_coverage": keyword_coverage if 'keyword_coverage' in locals() else 0
            }
            
        except Exception as e:
            logger.error(f"Error in completeness validation: {e}")
            return {"error": str(e), "completeness_score": 0.0}
    
    async def _quantify_uncertainty(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Quantify uncertainty in the response"""
        try:
            return self.uncertainty_quantifier.quantify_uncertainty(response, context)
        except Exception as e:
            logger.error(f"Error quantifying uncertainty: {e}")
            return {"error": str(e), "uncertainty_score": 0.5}
    
    def _calculate_confidence_score(
        self, 
        factual_accuracy: float, 
        consistency_score: float, 
        coherence_score: float, 
        completeness_score: float, 
        uncertainty_score: float
    ) -> float:
        """Calculate overall confidence score"""
        # Weighted average with emphasis on factual accuracy
        weights = [0.4, 0.25, 0.15, 0.15, 0.05]  # Factual accuracy gets highest weight
        
        scores = [factual_accuracy, consistency_score, coherence_score, completeness_score, 1.0 - uncertainty_score]
        
        confidence_score = sum(score * weight for score, weight in zip(scores, weights))
        
        return min(1.0, max(0.0, confidence_score))
    
    def _calculate_hallucination_probability(
        self, 
        factual_accuracy: float, 
        consistency_score: float, 
        uncertainty_score: float
    ) -> float:
        """Calculate probability of hallucination"""
        # Lower factual accuracy and consistency, higher uncertainty = higher hallucination probability
        hallucination_probability = (
            (1.0 - factual_accuracy) * 0.5 +
            (1.0 - consistency_score) * 0.3 +
            uncertainty_score * 0.2
        )
        
        return min(1.0, max(0.0, hallucination_probability))
    
    def _determine_validation_result(self, confidence_score: float, hallucination_probability: float) -> ValidationResult:
        """Determine validation result based on scores"""
        if confidence_score >= self.validation_thresholds["high_confidence"] and \
           hallucination_probability <= self.validation_thresholds["hallucination_threshold"]:
            return ValidationResult.VALID
        elif confidence_score >= self.validation_thresholds["medium_confidence"] and \
             hallucination_probability <= 0.5:
            return ValidationResult.NEEDS_VERIFICATION
        elif confidence_score >= self.validation_thresholds["low_confidence"]:
            return ValidationResult.UNCERTAIN
        else:
            return ValidationResult.INVALID
    
    def _determine_confidence_level(self, confidence_score: float) -> ConfidenceLevel:
        """Determine confidence level based on score"""
        if confidence_score >= 0.9:
            return ConfidenceLevel.VERY_HIGH
        elif confidence_score >= 0.8:
            return ConfidenceLevel.HIGH
        elif confidence_score >= 0.6:
            return ConfidenceLevel.MEDIUM
        elif confidence_score >= 0.4:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW

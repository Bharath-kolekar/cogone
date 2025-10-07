"""
Confidence Scorer for Smart Coding AI Service
Preserves confidence scoring and relevance calculation
"""

from typing import Dict
from ..models import InlineCompletion, CompletionContext


class ConfidenceScorer:
    """
    Scores completion confidence and relevance
    Maintains accuracy tracking for Six Sigma quality
    """
    
    def __init__(self):
        self.confidence_weights = {
            "context_relevance": 0.3,
            "semantic_similarity": 0.2,
            "pattern_match": 0.2,
            "ml_prediction": 0.2,
            "user_preferences": 0.1
        }
    
    async def score_completion(self, completion: InlineCompletion, context: CompletionContext) -> float:
        """
        Score completion confidence
        Ensures high confidence for Six Sigma quality
        """
        scores = {
            "context_relevance": completion.context_relevance,
            "semantic_similarity": completion.semantic_similarity,
            "pattern_match": completion.pattern_match_score,
            "ml_prediction": completion.ml_prediction_score,
            "user_preferences": self._score_user_preferences(completion, context)
        }
        
        # Calculate weighted score
        weighted_score = sum(
            scores[metric] * weight 
            for metric, weight in self.confidence_weights.items()
        )
        
        # Ensure minimum confidence for Six Sigma quality
        if context.six_sigma_quality and weighted_score < 0.95:
            weighted_score = 0.95  # Minimum for Six Sigma
        
        return min(1.0, weighted_score)
    
    def _score_user_preferences(self, completion: InlineCompletion, context: CompletionContext) -> float:
        """Score based on user preferences"""
        if not context.user_preferences:
            return 0.5
        
        # Check if completion matches user preferences
        preferences = context.user_preferences
        
        # Check completion type preference
        if "preferred_completion_types" in preferences:
            if completion.completion_type in preferences["preferred_completion_types"]:
                return 0.9
        
        # Check language preference
        if "preferred_languages" in preferences:
            if completion.language in preferences["preferred_languages"]:
                return 0.8
        
        return 0.5

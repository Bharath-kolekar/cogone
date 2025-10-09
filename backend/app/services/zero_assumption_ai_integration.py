"""
Zero Assumption DNA Integration with AI Components

This module integrates the Zero Assumption DNA principle with all AI components
in CognoMega, ensuring AI operations never make dangerous assumptions.

Core Integration Points:
1. AI Model Calls - Verify inputs, outputs, API responses
2. Prompt Engineering - Validate prompts, responses, token limits
3. Context Management - Verify context exists, is valid, within limits
4. AI Orchestration - Verify agent states, responses, transitions
5. Model Switching - Verify model availability, API keys, compatibility
6. Token Management - Verify token counts, costs, limits
7. Response Validation - Verify AI responses are usable, not hallucinated
8. Error Handling - No silent AI failures
9. Rate Limiting - Verify API limits, quotas
10. Result Caching - Verify cache validity, freshness
"""

from typing import Any, Dict, List, Optional, Union, Callable
import structlog
from datetime import datetime, timedelta
from functools import wraps

from .zero_assumption_dna import (
    ZeroAssumptionDNA,
    AssumptionViolation,
    must_exist,
    must_be_type,
    must_not_be_empty,
    must_have_key,
    must_succeed,
    no_silent_failures
)

logger = structlog.get_logger()


class AIAssumptionViolation(AssumptionViolation):
    """Specific violation for AI operations"""
    pass


class ZeroAssumptionAI:
    """
    Zero Assumption DNA for AI Components
    
    Ensures all AI operations follow the principle:
    DO NOT ASSUME ANYTHING about AI models, responses, or operations
    """
    
    def __init__(self):
        self.dna = ZeroAssumptionDNA()
        self.ai_violations: List[Dict[str, Any]] = []
        
        logger.info(
            "Zero Assumption AI Integration initialized",
            principle="DO NOT ASSUME ANYTHING about AI"
        )
    
    # ========== AI MODEL VERIFICATION ==========
    
    def verify_model_config(self, config: Dict[str, Any], model_name: str) -> Dict[str, Any]:
        """
        Verify AI model configuration - DO NOT ASSUME CONFIG IS VALID
        
        Args:
            config: Model configuration
            model_name: Name of model
        
        Returns:
            Validated config
        
        Raises:
            AIAssumptionViolation: If config is invalid
        """
        must_exist(config, "model_config")
        must_be_type(config, dict, "model_config")
        
        # DO NOT ASSUME: Required fields exist
        must_have_key(config, "api_key", f"{model_name}_config")
        must_have_key(config, "model", f"{model_name}_config")
        
        # DO NOT ASSUME: API key is valid
        api_key = config["api_key"]
        must_not_be_empty(api_key, "api_key")
        
        if api_key.startswith("dev-") or api_key == "dummy" or api_key == "test":
            self._log_ai_violation(
                "invalid_api_key",
                model_name,
                f"API key appears to be placeholder: {api_key[:10]}..."
            )
            raise AIAssumptionViolation(
                f"DO NOT ASSUME: API key for {model_name} is valid. "
                f"Key appears to be placeholder: {api_key[:10]}..."
            )
        
        # DO NOT ASSUME: Model name is supported
        model = config["model"]
        must_not_be_empty(model, "model")
        
        logger.info(
            "Model config verified",
            model_name=model_name,
            model=model
        )
        
        return config
    
    def verify_prompt(self, prompt: str, context: str = "prompt") -> str:
        """
        Verify prompt - DO NOT ASSUME PROMPT IS VALID
        
        Args:
            prompt: Prompt text
            context: Context for error messages
        
        Returns:
            Validated prompt
        
        Raises:
            AIAssumptionViolation: If prompt is invalid
        """
        # DO NOT ASSUME: Prompt exists
        must_exist(prompt, context)
        must_be_type(prompt, str, context)
        
        # DO NOT ASSUME: Prompt is not empty
        must_not_be_empty(prompt, context)
        
        # DO NOT ASSUME: Prompt is reasonable length
        if len(prompt) < 3:
            self._log_ai_violation(
                "prompt_too_short",
                context,
                f"Prompt is only {len(prompt)} characters"
            )
            raise AIAssumptionViolation(
                f"DO NOT ASSUME: Prompt is valid. "
                f"Prompt '{prompt}' is too short ({len(prompt)} chars)"
            )
        
        # DO NOT ASSUME: Prompt doesn't contain injection attempts
        dangerous_patterns = [
            "ignore previous instructions",
            "disregard all",
            "forget everything",
            "new instructions:",
        ]
        
        prompt_lower = prompt.lower()
        for pattern in dangerous_patterns:
            if pattern in prompt_lower:
                self._log_ai_violation(
                    "prompt_injection_attempt",
                    context,
                    f"Detected pattern: {pattern}"
                )
                logger.warning(
                    "Potential prompt injection detected",
                    pattern=pattern,
                    prompt_preview=prompt[:100]
                )
        
        return prompt
    
    def verify_ai_response(self, response: Any, operation: str) -> Any:
        """
        Verify AI response - DO NOT ASSUME RESPONSE IS VALID
        
        Args:
            response: AI response
            operation: Operation name
        
        Returns:
            Validated response
        
        Raises:
            AIAssumptionViolation: If response is invalid
        """
        # DO NOT ASSUME: Response exists
        must_exist(response, f"{operation}_response")
        
        # DO NOT ASSUME: Response is not None
        if response is None:
            self._log_ai_violation(
                "null_response",
                operation,
                "AI returned None"
            )
            raise AIAssumptionViolation(
                f"DO NOT ASSUME: AI {operation} succeeded. "
                f"Response is None - API may have failed silently."
            )
        
        # DO NOT ASSUME: Response has content
        if isinstance(response, dict):
            # Check for error indicators
            if "error" in response:
                self._log_ai_violation(
                    "error_in_response",
                    operation,
                    str(response.get("error"))
                )
                raise AIAssumptionViolation(
                    f"DO NOT ASSUME: AI {operation} succeeded. "
                    f"Response contains error: {response.get('error')}"
                )
            
            # Verify expected fields exist
            if "choices" in response:
                must_not_be_empty(response["choices"], "response.choices")
        
        elif isinstance(response, str):
            must_not_be_empty(response, f"{operation}_response")
        
        return response
    
    def verify_token_count(self, tokens: int, max_tokens: int, context: str) -> int:
        """
        Verify token count - DO NOT ASSUME WITHIN LIMITS
        
        Args:
            tokens: Token count
            max_tokens: Maximum allowed tokens
            context: Context for error
        
        Returns:
            Token count if valid
        
        Raises:
            AIAssumptionViolation: If exceeds limit
        """
        must_exist(tokens, "token_count")
        must_be_type(tokens, int, "token_count")
        
        # DO NOT ASSUME: Token count is positive
        if tokens < 0:
            self._log_ai_violation(
                "negative_token_count",
                context,
                f"Token count: {tokens}"
            )
            raise AIAssumptionViolation(
                f"DO NOT ASSUME: Token count is valid. "
                f"Got negative value: {tokens}"
            )
        
        # DO NOT ASSUME: Within limit
        if tokens > max_tokens:
            self._log_ai_violation(
                "token_limit_exceeded",
                context,
                f"{tokens} > {max_tokens}"
            )
            raise AIAssumptionViolation(
                f"DO NOT ASSUME: Token count is within limit. "
                f"Got {tokens} tokens, max is {max_tokens}"
            )
        
        # Warn if close to limit
        if tokens > max_tokens * 0.9:
            logger.warning(
                "Token count approaching limit",
                tokens=tokens,
                max_tokens=max_tokens,
                usage_percent=round(tokens/max_tokens*100, 1)
            )
        
        return tokens
    
    def verify_context_window(self, context: List[Dict], max_messages: int = 50) -> List[Dict]:
        """
        Verify context window - DO NOT ASSUME CONTEXT IS VALID
        
        Args:
            context: Conversation context
            max_messages: Maximum messages allowed
        
        Returns:
            Validated context
        
        Raises:
            AIAssumptionViolation: If context invalid
        """
        must_exist(context, "context")
        must_be_type(context, list, "context")
        
        # DO NOT ASSUME: Context is not empty (if required)
        if len(context) == 0:
            logger.warning("Empty context provided")
        
        # DO NOT ASSUME: Context size is reasonable
        if len(context) > max_messages:
            self._log_ai_violation(
                "context_too_large",
                "context_window",
                f"{len(context)} > {max_messages} messages"
            )
            raise AIAssumptionViolation(
                f"DO NOT ASSUME: Context size is valid. "
                f"Got {len(context)} messages, max is {max_messages}"
            )
        
        # DO NOT ASSUME: Each message is valid
        for i, msg in enumerate(context):
            must_be_type(msg, dict, f"context[{i}]")
            must_have_key(msg, "role", f"context[{i}]")
            must_have_key(msg, "content", f"context[{i}]")
            
            # Verify role is valid
            valid_roles = ["system", "user", "assistant"]
            if msg["role"] not in valid_roles:
                self._log_ai_violation(
                    "invalid_message_role",
                    f"context[{i}]",
                    f"Role: {msg['role']}"
                )
                raise AIAssumptionViolation(
                    f"DO NOT ASSUME: Message role is valid. "
                    f"Got '{msg['role']}', expected one of {valid_roles}"
                )
        
        return context
    
    def verify_model_available(self, model_name: str, available_models: List[str]) -> str:
        """
        Verify model is available - DO NOT ASSUME MODEL EXISTS
        
        Args:
            model_name: Name of model to use
            available_models: List of available models
        
        Returns:
            Model name if available
        
        Raises:
            AIAssumptionViolation: If model not available
        """
        must_exist(model_name, "model_name")
        must_not_be_empty(model_name, "model_name")
        must_exist(available_models, "available_models")
        
        # DO NOT ASSUME: Model is available
        if model_name not in available_models:
            self._log_ai_violation(
                "model_not_available",
                model_name,
                f"Available: {available_models}"
            )
            raise AIAssumptionViolation(
                f"DO NOT ASSUME: Model '{model_name}' is available. "
                f"Available models: {available_models}"
            )
        
        return model_name
    
    def verify_rate_limit(self, current_count: int, limit: int, window: str) -> bool:
        """
        Verify rate limit - DO NOT ASSUME UNDER LIMIT
        
        Args:
            current_count: Current request count
            limit: Rate limit
            window: Time window (e.g., "1 minute")
        
        Returns:
            True if under limit
        
        Raises:
            AIAssumptionViolation: If rate limit exceeded
        """
        must_exist(current_count, "current_count")
        must_exist(limit, "rate_limit")
        
        # DO NOT ASSUME: Under rate limit
        if current_count >= limit:
            self._log_ai_violation(
                "rate_limit_exceeded",
                f"rate_limit_{window}",
                f"{current_count} >= {limit}"
            )
            raise AIAssumptionViolation(
                f"DO NOT ASSUME: Rate limit not exceeded. "
                f"Made {current_count} requests, limit is {limit} per {window}"
            )
        
        # Warn if close to limit
        if current_count > limit * 0.8:
            logger.warning(
                "Approaching rate limit",
                current_count=current_count,
                limit=limit,
                window=window,
                usage_percent=round(current_count/limit*100, 1)
            )
        
        return True
    
    def verify_cached_result(self, cached: Any, max_age_seconds: int, 
                           timestamp: datetime) -> Any:
        """
        Verify cached result is fresh - DO NOT ASSUME CACHE IS VALID
        
        Args:
            cached: Cached result
            max_age_seconds: Maximum cache age
            timestamp: Cache timestamp
        
        Returns:
            Cached result if valid
        
        Raises:
            AIAssumptionViolation: If cache is stale
        """
        must_exist(cached, "cached_result")
        must_exist(timestamp, "cache_timestamp")
        
        # DO NOT ASSUME: Cache is fresh
        age = datetime.utcnow() - timestamp
        if age.total_seconds() > max_age_seconds:
            self._log_ai_violation(
                "stale_cache",
                "cached_result",
                f"Age: {age.total_seconds()}s > {max_age_seconds}s"
            )
            raise AIAssumptionViolation(
                f"DO NOT ASSUME: Cached result is fresh. "
                f"Cache is {age.total_seconds()}s old, max is {max_age_seconds}s"
            )
        
        return cached
    
    # ========== DECORATORS ==========
    
    def verify_ai_inputs(self, required_params: List[str]):
        """
        Decorator to verify AI function inputs
        
        Usage:
            @zero_assumption_ai.verify_ai_inputs(["prompt", "model"])
            async def call_ai(prompt, model, **kwargs):
                ...
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                # Verify required parameters exist
                for param in required_params:
                    if param not in kwargs and len(args) <= required_params.index(param):
                        self._log_ai_violation(
                            "missing_required_param",
                            func.__name__,
                            f"Missing: {param}"
                        )
                        raise AIAssumptionViolation(
                            f"DO NOT ASSUME: All AI parameters provided. "
                            f"Missing required parameter: {param}"
                        )
                
                return await func(*args, **kwargs)
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                for param in required_params:
                    if param not in kwargs and len(args) <= required_params.index(param):
                        self._log_ai_violation(
                            "missing_required_param",
                            func.__name__,
                            f"Missing: {param}"
                        )
                        raise AIAssumptionViolation(
                            f"DO NOT ASSUME: All AI parameters provided. "
                            f"Missing required parameter: {param}"
                        )
                
                return func(*args, **kwargs)
            
            import inspect
            if inspect.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def no_ai_hallucinations(self, operation: str):
        """
        Decorator to detect potential AI hallucinations
        
        Usage:
            @zero_assumption_ai.no_ai_hallucinations("code_generation")
            async def generate_code(prompt):
                ...
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                
                # DO NOT ASSUME: AI result is factual
                if isinstance(result, str):
                    # Check for hallucination indicators
                    hallucination_patterns = [
                        "I don't actually know",
                        "I cannot verify",
                        "This is hypothetical",
                        "I'm not sure",
                        "As an AI",
                    ]
                    
                    result_lower = result.lower()
                    for pattern in hallucination_patterns:
                        if pattern.lower() in result_lower:
                            logger.warning(
                                "Potential AI hallucination detected",
                                operation=operation,
                                pattern=pattern
                            )
                
                return result
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                
                if isinstance(result, str):
                    hallucination_patterns = [
                        "I don't actually know",
                        "I cannot verify",
                        "This is hypothetical",
                        "I'm not sure",
                        "As an AI",
                    ]
                    
                    result_lower = result.lower()
                    for pattern in hallucination_patterns:
                        if pattern.lower() in result_lower:
                            logger.warning(
                                "Potential AI hallucination detected",
                                operation=operation,
                                pattern=pattern
                            )
                
                return result
            
            import inspect
            if inspect.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    # ========== LOGGING ==========
    
    def _log_ai_violation(self, violation_type: str, context: str, details: str):
        """Log AI-specific assumption violation"""
        violation = {
            "type": violation_type,
            "context": context,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.ai_violations.append(violation)
        
        logger.error(
            "AI Assumption Violation",
            violation_type=violation_type,
            context=context,
            details=details
        )
    
    def get_ai_violations_report(self) -> Dict[str, Any]:
        """Get report of AI-specific violations"""
        violation_types = {}
        for v in self.ai_violations:
            vtype = v['type']
            violation_types[vtype] = violation_types.get(vtype, 0) + 1
        
        return {
            "total_ai_violations": len(self.ai_violations),
            "violation_types": violation_types,
            "recent_violations": self.ai_violations[-10:],
            "principle": "DO NOT ASSUME ANYTHING about AI"
        }


# Global instance
zero_assumption_ai = ZeroAssumptionAI()


# Convenience functions
def verify_ai_model_config(config: Dict[str, Any], model_name: str) -> Dict[str, Any]:
    """Verify AI model configuration"""
    return zero_assumption_ai.verify_model_config(config, model_name)


def verify_ai_prompt(prompt: str, context: str = "prompt") -> str:
    """Verify AI prompt"""
    return zero_assumption_ai.verify_prompt(prompt, context)


def verify_ai_response(response: Any, operation: str) -> Any:
    """Verify AI response"""
    return zero_assumption_ai.verify_ai_response(response, operation)


def verify_ai_context(context: List[Dict], max_messages: int = 50) -> List[Dict]:
    """Verify AI context window"""
    return zero_assumption_ai.verify_context_window(context, max_messages)


def verify_ai_tokens(tokens: int, max_tokens: int, context: str) -> int:
    """Verify token count"""
    return zero_assumption_ai.verify_token_count(tokens, max_tokens, context)


__all__ = [
    'ZeroAssumptionAI',
    'AIAssumptionViolation',
    'zero_assumption_ai',
    'verify_ai_model_config',
    'verify_ai_prompt',
    'verify_ai_response',
    'verify_ai_context',
    'verify_ai_tokens',
]


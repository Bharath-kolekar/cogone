"""
Example: AI Service with Zero Assumption DNA Integration

This shows how to integrate Zero Assumption DNA with AI components.
This is a reference implementation for updating all AI services.
"""

from typing import Dict, List, Any, Optional
import structlog
from datetime import datetime

# Zero Assumption DNA imports
from .zero_assumption_dna import (
    must_exist,
    must_be_type,
    must_not_be_empty,
    must_have_key,
    no_silent_failures
)

from .zero_assumption_ai_integration import (
    verify_ai_model_config,
    verify_ai_prompt,
    verify_ai_response,
    verify_ai_context,
    verify_ai_tokens,
    zero_assumption_ai
)

logger = structlog.get_logger()


class AIServiceWithZeroAssumptions:
    """
    Example AI Service with Zero Assumption DNA fully integrated
    
    This demonstrates the correct way to build AI services in CognoMega:
    - NO assumptions about model availability
    - NO assumptions about API responses
    - NO assumptions about prompt validity
    - NO assumptions about token limits
    - NO silent failures
    """
    
    def __init__(self, model_config: Dict[str, Any]):
        """
        Initialize AI service with verified configuration
        
        Args:
            model_config: Model configuration
        
        Raises:
            AssumptionViolation: If config is invalid
        """
        # DO NOT ASSUME: Config is valid
        self.config = verify_ai_model_config(model_config, "ai_service")
        
        # DO NOT ASSUME: Fields exist
        self.model_name = must_have_key(self.config, "model", "config")
        self.api_key = must_have_key(self.config, "api_key", "config")
        self.max_tokens = self.config.get("max_tokens", 4000)
        
        # Verify API key format
        must_not_be_empty(self.api_key, "api_key")
        
        logger.info(
            "AI Service initialized with Zero Assumptions",
            model=self.model_name,
            principle="DO NOT ASSUME ANYTHING"
        )
    
    @no_silent_failures("ai_completion")
    @zero_assumption_ai.verify_ai_inputs(["prompt"])
    @zero_assumption_ai.no_ai_hallucinations("ai_completion")
    async def complete(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Get AI completion - Zero Assumptions version
        
        Args:
            prompt: Prompt text
            **kwargs: Additional parameters
        
        Returns:
            Completion result with verification
        
        Raises:
            AssumptionViolation: If any verification fails
        """
        # DO NOT ASSUME: Prompt is valid
        validated_prompt = verify_ai_prompt(prompt, "completion_prompt")
        
        # DO NOT ASSUME: Token count is within limits
        estimated_tokens = len(validated_prompt) // 4  # Rough estimate
        max_completion_tokens = kwargs.get("max_tokens", 1000)
        
        verify_ai_tokens(
            estimated_tokens + max_completion_tokens,
            self.max_tokens,
            "prompt_and_completion"
        )
        
        # DO NOT ASSUME: API call succeeds
        try:
            # Simulate API call (replace with real implementation)
            response = await self._call_ai_api({
                "model": self.model_name,
                "prompt": validated_prompt,
                "max_tokens": max_completion_tokens,
                **kwargs
            })
        except Exception as e:
            logger.error(
                "AI API call failed",
                model=self.model_name,
                error=str(e)
            )
            raise  # Re-raise, don't swallow
        
        # DO NOT ASSUME: Response is valid
        validated_response = verify_ai_response(response, "completion")
        
        # DO NOT ASSUME: Response has expected structure
        must_have_key(validated_response, "choices", "ai_response")
        choices = validated_response["choices"]
        must_not_be_empty(choices, "response.choices")
        
        # DO NOT ASSUME: First choice exists
        first_choice = choices[0]
        must_have_key(first_choice, "text", "choice")
        
        completion_text = first_choice["text"]
        must_not_be_empty(completion_text, "completion_text")
        
        logger.info(
            "AI completion successful",
            model=self.model_name,
            prompt_length=len(validated_prompt),
            completion_length=len(completion_text)
        )
        
        return {
            "completion": completion_text,
            "model": self.model_name,
            "prompt": validated_prompt,
            "metadata": {
                "verified": True,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    @no_silent_failures("ai_chat")
    @zero_assumption_ai.verify_ai_inputs(["messages"])
    async def chat(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """
        Chat completion - Zero Assumptions version
        
        Args:
            messages: Conversation messages
            **kwargs: Additional parameters
        
        Returns:
            Chat response with verification
        
        Raises:
            AssumptionViolation: If any verification fails
        """
        # DO NOT ASSUME: Messages list is valid
        must_exist(messages, "messages")
        must_be_type(messages, list, "messages")
        must_not_be_empty(messages, "messages")
        
        # DO NOT ASSUME: Context window is valid
        validated_context = verify_ai_context(messages, max_messages=50)
        
        # DO NOT ASSUME: Each message has valid structure
        for i, msg in enumerate(validated_context):
            must_have_key(msg, "role", f"message[{i}]")
            must_have_key(msg, "content", f"message[{i}]")
            
            # Verify role
            role = msg["role"]
            if role not in ["system", "user", "assistant"]:
                raise ValueError(f"Invalid message role: {role}")
            
            # Verify content
            content = msg["content"]
            must_not_be_empty(content, f"message[{i}].content")
        
        # Calculate total tokens
        total_chars = sum(len(msg["content"]) for msg in validated_context)
        estimated_tokens = total_chars // 4
        max_completion_tokens = kwargs.get("max_tokens", 1000)
        
        verify_ai_tokens(
            estimated_tokens + max_completion_tokens,
            self.max_tokens,
            "chat_context_and_completion"
        )
        
        # DO NOT ASSUME: API call succeeds
        try:
            response = await self._call_ai_api({
                "model": self.model_name,
                "messages": validated_context,
                "max_tokens": max_completion_tokens,
                **kwargs
            })
        except Exception as e:
            logger.error(
                "AI chat API call failed",
                model=self.model_name,
                num_messages=len(validated_context),
                error=str(e)
            )
            raise
        
        # DO NOT ASSUME: Response is valid
        validated_response = verify_ai_response(response, "chat")
        
        # DO NOT ASSUME: Response has expected structure
        must_have_key(validated_response, "choices", "chat_response")
        choices = validated_response["choices"]
        must_not_be_empty(choices, "response.choices")
        
        first_choice = choices[0]
        must_have_key(first_choice, "message", "choice")
        
        message = first_choice["message"]
        must_have_key(message, "content", "assistant_message")
        
        assistant_content = message["content"]
        must_not_be_empty(assistant_content, "assistant_content")
        
        logger.info(
            "AI chat successful",
            model=self.model_name,
            num_messages=len(validated_context),
            response_length=len(assistant_content)
        )
        
        return {
            "message": assistant_content,
            "role": "assistant",
            "model": self.model_name,
            "metadata": {
                "verified": True,
                "context_messages": len(validated_context),
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    
    @no_silent_failures("ai_embedding")
    async def get_embedding(self, text: str) -> List[float]:
        """
        Get text embedding - Zero Assumptions version
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector
        
        Raises:
            AssumptionViolation: If any verification fails
        """
        # DO NOT ASSUME: Text is valid
        must_exist(text, "text")
        must_be_type(text, str, "text")
        must_not_be_empty(text, "text")
        
        # DO NOT ASSUME: Text length is reasonable
        if len(text) > 8000:
            raise ValueError(f"Text too long for embedding: {len(text)} chars")
        
        # DO NOT ASSUME: API call succeeds
        try:
            response = await self._call_ai_api({
                "model": f"{self.model_name}-embedding",
                "input": text
            })
        except Exception as e:
            logger.error(
                "AI embedding API call failed",
                model=self.model_name,
                text_length=len(text),
                error=str(e)
            )
            raise
        
        # DO NOT ASSUME: Response has embedding
        validated_response = verify_ai_response(response, "embedding")
        must_have_key(validated_response, "data", "embedding_response")
        
        data = validated_response["data"]
        must_not_be_empty(data, "embedding_data")
        
        first_embedding = data[0]
        must_have_key(first_embedding, "embedding", "embedding_data[0]")
        
        embedding = first_embedding["embedding"]
        must_be_type(embedding, list, "embedding")
        must_not_be_empty(embedding, "embedding")
        
        # DO NOT ASSUME: Embedding values are valid
        for i, val in enumerate(embedding[:10]):  # Check first 10
            if not isinstance(val, (int, float)):
                raise ValueError(f"Invalid embedding value at index {i}: {val}")
        
        logger.info(
            "AI embedding successful",
            model=self.model_name,
            text_length=len(text),
            embedding_dim=len(embedding)
        )
        
        return embedding
    
    async def _call_ai_api(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call AI API - Zero Assumptions version
        
        This is a stub - replace with real API calls
        
        Args:
            params: API parameters
        
        Returns:
            API response
        """
        # DO NOT ASSUME: API is available
        # DO NOT ASSUME: Parameters are valid
        # DO NOT ASSUME: Response is successful
        
        logger.info(
            "Calling AI API (stub)",
            model=params.get("model"),
            params_keys=list(params.keys())
        )
        
        # Stub response - replace with real API call
        if "messages" in params:
            return {
                "choices": [{
                    "message": {
                        "role": "assistant",
                        "content": "This is a stub response. Replace with real AI API."
                    }
                }]
            }
        elif "input" in params:
            return {
                "data": [{
                    "embedding": [0.1] * 1536  # Stub embedding
                }]
            }
        else:
            return {
                "choices": [{
                    "text": "This is a stub response. Replace with real AI API."
                }]
            }
    
    def get_violations_report(self) -> Dict[str, Any]:
        """Get report of all assumption violations"""
        return zero_assumption_ai.get_ai_violations_report()


# Example usage
async def example_usage():
    """Example of using AI service with Zero Assumptions"""
    
    # Initialize with verified config
    config = {
        "model": "gpt-4",
        "api_key": "sk-real-api-key-here",  # Replace with real key
        "max_tokens": 4000
    }
    
    try:
        ai_service = AIServiceWithZeroAssumptions(config)
    except Exception as e:
        logger.error("Failed to initialize AI service", error=str(e))
        return
    
    # Example 1: Simple completion
    try:
        result = await ai_service.complete("Write a hello world in Python")
        print(f"Completion: {result['completion']}")
    except Exception as e:
        logger.error("Completion failed", error=str(e))
    
    # Example 2: Chat
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "What is 2+2?"}
        ]
        result = await ai_service.chat(messages)
        print(f"Chat response: {result['message']}")
    except Exception as e:
        logger.error("Chat failed", error=str(e))
    
    # Example 3: Embedding
    try:
        embedding = await ai_service.get_embedding("Hello world")
        print(f"Embedding dimension: {len(embedding)}")
    except Exception as e:
        logger.error("Embedding failed", error=str(e))
    
    # Get violations report
    report = ai_service.get_violations_report()
    print(f"Violations report: {report}")


__all__ = [
    'AIServiceWithZeroAssumptions',
    'example_usage',
]


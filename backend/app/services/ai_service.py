"""
AI Service for Voice-to-App SaaS Platform
Enhanced with Zero Assumption DNA - DO NOT ASSUME ANYTHING

This service follows the Zero Assumption principle:
- Verifies all inputs exist and are valid
- Validates all AI responses
- Checks all operations succeed
- No silent failures
"""

from typing import Dict, Any, Optional
import structlog

# Zero Assumption DNA imports
from .zero_assumption_dna import (
    must_exist,
    must_be_type,
    must_not_be_empty,
    must_have_key,
    no_silent_failures
)

from .zero_assumption_dna_rules import (
    comprehensive_zero_assumption
)

from .zero_assumption_ai_integration import (
    verify_ai_prompt,
    verify_ai_response,
    zero_assumption_ai
)

logger = structlog.get_logger()


class AIService:
    """
    AI service with Zero Assumption DNA fully integrated
    
    Follows the principle: DO NOT ASSUME ANYTHING about AI operations
    """
    
    def __init__(self):
        """Initialize the AI service with Zero Assumptions"""
        self.logger = logger
        logger.info(
            "AI Service initialized with Zero Assumption DNA",
            principle="DO NOT ASSUME ANYTHING"
        )
    
    @no_silent_failures("ai_request_processing")
    @zero_assumption_ai.verify_ai_inputs(["request"])
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an AI request - Zero Assumptions version
        
        Args:
            request: AI request data
        
        Returns:
            Processed result with full validation
        
        Raises:
            AssumptionViolation: If any validation fails
        """
        # DO NOT ASSUME: Request is valid
        must_exist(request, "ai_request")
        must_be_type(request, dict, "ai_request")
        must_not_be_empty(request, "ai_request")
        
        # DO NOT ASSUME: Request has required fields
        request_type = must_have_key(request, "type", "ai_request")
        must_not_be_empty(request_type, "request_type")
        
        logger.info(
            "Processing AI request with Zero Assumptions",
            request_type=request_type
        )
        
        # DO NOT ASSUME: Request type is valid
        valid_types = ["completion", "chat", "embedding", "analysis"]
        if request_type not in valid_types:
            raise ValueError(
                f"DO NOT ASSUME: request type is valid. "
                f"Got '{request_type}', expected one of {valid_types}"
            )
        
        # Process based on type
        try:
            if request_type == "completion":
                result = await self._process_completion(request)
            elif request_type == "chat":
                result = await self._process_chat(request)
            elif request_type == "embedding":
                result = await self._process_embedding(request)
            elif request_type == "analysis":
                result = await self._process_analysis(request)
            else:
                result = await self._process_generic(request)
        
        except Exception as e:
            logger.error(
                "AI request processing failed",
                request_type=request_type,
                error=str(e)
            )
            raise  # Re-raise, don't swallow
        
        # DO NOT ASSUME: Processing returned valid result
        must_exist(result, "processing_result")
        must_be_type(result, dict, "processing_result")
        must_have_key(result, "success", "processing_result")
        
        logger.info(
            "AI request processed successfully",
            request_type=request_type,
            success=result.get("success")
        )
        
        return result
    
    @no_silent_failures("ai_completion")
    async def _process_completion(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process completion request with Zero Assumptions"""
        
        # DO NOT ASSUME: Prompt exists and is valid
        prompt = must_have_key(request, "prompt", "completion_request")
        validated_prompt = verify_ai_prompt(prompt, "completion_prompt")
        
        logger.info(
            "Processing completion",
            prompt_length=len(validated_prompt)
        )
        
        # Simulate AI completion (replace with real AI call)
        completion_text = f"Completion for: {validated_prompt[:50]}..."
        
        # DO NOT ASSUME: Completion has content
        must_not_be_empty(completion_text, "completion_text")
        
        return {
            "success": True,
            "type": "completion",
            "prompt": validated_prompt,
            "completion": completion_text,
            "verified": True
        }
    
    @no_silent_failures("ai_chat")
    async def _process_chat(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process chat request with Zero Assumptions"""
        
        # DO NOT ASSUME: Messages exist and are valid
        messages = must_have_key(request, "messages", "chat_request")
        must_be_type(messages, list, "messages")
        must_not_be_empty(messages, "messages")
        
        # DO NOT ASSUME: Each message has required fields
        for i, msg in enumerate(messages):
            must_be_type(msg, dict, f"message[{i}]")
            must_have_key(msg, "role", f"message[{i}]")
            must_have_key(msg, "content", f"message[{i}]")
            
            # Verify role is valid
            role = msg["role"]
            valid_roles = ["system", "user", "assistant"]
            if role not in valid_roles:
                raise ValueError(
                    f"DO NOT ASSUME: message role is valid. "
                    f"Got '{role}', expected one of {valid_roles}"
                )
            
            # Verify content is not empty
            must_not_be_empty(msg["content"], f"message[{i}].content")
        
        logger.info(
            "Processing chat",
            num_messages=len(messages)
        )
        
        # Simulate AI chat response (replace with real AI call)
        response_text = "AI chat response based on conversation"
        
        # DO NOT ASSUME: Response has content
        must_not_be_empty(response_text, "chat_response")
        
        return {
            "success": True,
            "type": "chat",
            "messages": messages,
            "response": response_text,
            "verified": True
        }
    
    @no_silent_failures("ai_embedding")
    async def _process_embedding(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process embedding request with Zero Assumptions"""
        
        # DO NOT ASSUME: Text exists and is valid
        text = must_have_key(request, "text", "embedding_request")
        must_be_type(text, str, "embedding_text")
        must_not_be_empty(text, "embedding_text")
        
        # DO NOT ASSUME: Text length is reasonable
        max_length = 8000
        if len(text) > max_length:
            raise ValueError(
                f"DO NOT ASSUME: text length is valid. "
                f"Text is {len(text)} chars, max is {max_length}"
            )
        
        logger.info(
            "Processing embedding",
            text_length=len(text)
        )
        
        # Simulate embedding (replace with real AI call)
        embedding = [0.1] * 1536  # Simulated embedding vector
        
        # DO NOT ASSUME: Embedding is valid
        must_not_be_empty(embedding, "embedding_vector")
        
        return {
            "success": True,
            "type": "embedding",
            "text": text,
            "embedding": embedding,
            "dimension": len(embedding),
            "verified": True
        }
    
    @no_silent_failures("ai_analysis")
    async def _process_analysis(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process analysis request with Zero Assumptions"""
        
        # DO NOT ASSUME: Data exists and is valid
        data = must_have_key(request, "data", "analysis_request")
        must_not_be_empty(data, "analysis_data")
        
        logger.info(
            "Processing analysis",
            data_type=type(data).__name__
        )
        
        # Simulate analysis (replace with real AI call)
        analysis_result = {
            "summary": "Data analysis completed",
            "insights": ["Insight 1", "Insight 2"],
            "metrics": {"accuracy": 0.95}
        }
        
        # DO NOT ASSUME: Analysis has results
        must_not_be_empty(analysis_result, "analysis_result")
        
        return {
            "success": True,
            "type": "analysis",
            "data": data,
            "analysis": analysis_result,
            "verified": True
        }
    
    @no_silent_failures("ai_generic")
    async def _process_generic(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process generic request with Zero Assumptions"""
        
        logger.info("Processing generic AI request")
        
        # DO NOT ASSUME: Request has valid structure
        comprehensive_zero_assumption.verify_dict_has_keys(
            request,
            ["type"],
            "generic_request"
        )
        
        return {
            "success": True,
            "result": "Generic AI processing completed",
            "data": request,
            "verified": True
        }
    
    def get_violations_report(self) -> Dict[str, Any]:
        """Get report of all assumption violations"""
        return zero_assumption_ai.get_ai_violations_report()

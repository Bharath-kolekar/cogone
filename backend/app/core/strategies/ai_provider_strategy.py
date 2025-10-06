"""
AI Provider Strategy Pattern Implementation
Follows Strategy Pattern and Open/Closed Principle
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from enum import Enum
import structlog

logger = structlog.get_logger()


class AIProviderType(str, Enum):
    """AI Provider types"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL_LLM = "local_llm"
    GROQ = "groq"
    TOGETHER = "together"


class AIProviderStrategy(ABC):
    """
    Abstract AI Provider Strategy
    Follows Strategy Pattern and Open/Closed Principle
    """
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.api_key = api_key
        self.base_url = base_url
        self.provider_type = self.get_provider_type()
    
    @abstractmethod
    def get_provider_type(self) -> AIProviderType:
        """Get provider type"""
        pass
    
    @abstractmethod
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate text completion"""
        pass
    
    @abstractmethod
    async def generate_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate chat completion"""
        pass
    
    @abstractmethod
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get model information"""
        pass
    
    @abstractmethod
    async def validate_connection(self) -> bool:
        """Validate provider connection"""
        pass
    
    @abstractmethod
    def get_cost_estimate(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Get cost estimate for tokens"""
        pass


class OpenAIStrategy(AIProviderStrategy):
    """OpenAI provider strategy"""
    
    def get_provider_type(self) -> AIProviderType:
        return AIProviderType.OPENAI
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate completion using OpenAI API"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            response = await client.completions.create(
                model=kwargs.get('model', 'gpt-3.5-turbo-instruct'),
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                **{k: v for k, v in kwargs.items() if k != 'model'}
            )
            
            return response.choices[0].text.strip()
            
        except Exception as e:
            logger.error("OpenAI completion generation error", error=str(e))
            raise
    
    async def generate_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate chat completion using OpenAI API"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            response = await client.chat.completions.create(
                model=kwargs.get('model', 'gpt-3.5-turbo'),
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                **{k: v for k, v in kwargs.items() if k != 'model'}
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error("OpenAI chat completion generation error", error=str(e))
            raise
    
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get OpenAI model information"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            # Get model list
            models = await client.models.list()
            model_info = next((m for m in models.data if m.id == model_name), None)
            
            if model_info:
                return {
                    "id": model_info.id,
                    "object": model_info.object,
                    "created": model_info.created,
                    "owned_by": model_info.owned_by,
                    "provider": "openai"
                }
            else:
                return {"error": "Model not found"}
                
        except Exception as e:
            logger.error("OpenAI model info error", model_name=model_name, error=str(e))
            raise
    
    async def validate_connection(self) -> bool:
        """Validate OpenAI connection"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            await client.models.list()
            return True
            
        except Exception as e:
            logger.error("OpenAI connection validation error", error=str(e))
            return False
    
    def get_cost_estimate(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Get OpenAI cost estimate"""
        # GPT-3.5-turbo pricing (per 1K tokens)
        prompt_cost = 0.0015  # $0.0015 per 1K prompt tokens
        completion_cost = 0.002  # $0.002 per 1K completion tokens
        
        return (prompt_tokens / 1000 * prompt_cost) + (completion_tokens / 1000 * completion_cost)


class AnthropicStrategy(AIProviderStrategy):
    """Anthropic provider strategy"""
    
    def get_provider_type(self) -> AIProviderType:
        return AIProviderType.ANTHROPIC
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate completion using Anthropic API"""
        try:
            import anthropic
            
            client = anthropic.AsyncAnthropic(api_key=self.api_key)
            
            response = await client.messages.create(
                model=kwargs.get('model', 'claude-3-sonnet-20240229'),
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}],
                **{k: v for k, v in kwargs.items() if k != 'model'}
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error("Anthropic completion generation error", error=str(e))
            raise
    
    async def generate_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate chat completion using Anthropic API"""
        try:
            import anthropic
            
            client = anthropic.AsyncAnthropic(api_key=self.api_key)
            
            # Convert messages format for Anthropic
            system_message = ""
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append(msg)
            
            response = await client.messages.create(
                model=kwargs.get('model', 'claude-3-sonnet-20240229'),
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_message if system_message else None,
                messages=user_messages,
                **{k: v for k, v in kwargs.items() if k != 'model'}
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error("Anthropic chat completion generation error", error=str(e))
            raise
    
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get Anthropic model information"""
        # Anthropic doesn't provide model listing API
        return {
            "id": model_name,
            "provider": "anthropic",
            "available_models": [
                "claude-3-opus-20240229",
                "claude-3-sonnet-20240229",
                "claude-3-haiku-20240307"
            ]
        }
    
    async def validate_connection(self) -> bool:
        """Validate Anthropic connection"""
        try:
            import anthropic
            
            client = anthropic.AsyncAnthropic(api_key=self.api_key)
            # Test with a simple request
            await client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
            
        except Exception as e:
            logger.error("Anthropic connection validation error", error=str(e))
            return False
    
    def get_cost_estimate(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Get Anthropic cost estimate"""
        # Claude-3-sonnet pricing (per 1K tokens)
        prompt_cost = 0.003  # $0.003 per 1K prompt tokens
        completion_cost = 0.015  # $0.015 per 1K completion tokens
        
        return (prompt_tokens / 1000 * prompt_cost) + (completion_tokens / 1000 * completion_cost)


class LocalLLMStrategy(AIProviderStrategy):
    """Local LLM provider strategy"""
    
    def get_provider_type(self) -> AIProviderType:
        return AIProviderType.LOCAL_LLM
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        super().__init__(api_key, base_url)
        # Reuse a session per strategy
        self._session: Optional["aiohttp.ClientSession"] = None
    
    async def _get_session(self):
        import aiohttp
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=60)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate completion using local LLM"""
        try:
            import aiohttp
            
            # Assuming Ollama or similar local LLM server
            model = kwargs.get('model', 'llama2')
            url = f"{self.base_url or 'http://localhost:11434'}/api/generate"
            
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature
                }
            }
            
            session = await self._get_session()
            async with session.post(url, json=payload) as resp:
                    resp.raise_for_status()
                    result = await resp.json()
            return result.get("response", "")
            
        except Exception as e:
            logger.error("Local LLM completion generation error", error=str(e))
            raise
    
    async def generate_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """Generate chat completion using local LLM"""
        try:
            # Build prompt and delegate to generate_completion (already async non-blocking)
            
            # Convert messages to prompt
            prompt = ""
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                if role == "system":
                    prompt += f"System: {content}\n"
                elif role == "user":
                    prompt += f"User: {content}\n"
                elif role == "assistant":
                    prompt += f"Assistant: {content}\n"
            
            prompt += "Assistant: "
            
            return await self.generate_completion(prompt, max_tokens, temperature, **kwargs)
            
        except Exception as e:
            logger.error("Local LLM chat completion generation error", error=str(e))
            raise
    
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get local LLM model information"""
        try:
            import aiohttp
            
            url = f"{self.base_url or 'http://localhost:11434'}/api/tags"
            session = await self._get_session()
            async with session.get(url) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
            
            models = data.get("models", [])
            model_info = next((m for m in models if m["name"] == model_name), None)
            
            if model_info:
                return {
                    "name": model_info["name"],
                    "size": model_info.get("size", 0),
                    "modified_at": model_info.get("modified_at"),
                    "provider": "local_llm"
                }
            else:
                return {"error": "Model not found"}
                
        except Exception as e:
            logger.error("Local LLM model info error", model_name=model_name, error=str(e))
            return {"error": str(e)}
    
    async def validate_connection(self) -> bool:
        """Validate local LLM connection"""
        try:
            import aiohttp
            url = f"{self.base_url or 'http://localhost:11434'}/api/tags"
            session = await self._get_session()
            async with session.get(url) as resp:
                    resp.raise_for_status()
                    return True
            
        except Exception as e:
            logger.error("Local LLM connection validation error", error=str(e))
            return False
    
    def get_cost_estimate(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Local LLM has no cost"""
        return 0.0


class AIProviderFactory:
    """
    AI Provider Factory following Factory Pattern
    Creates appropriate AI provider strategy instances
    """
    
    _strategies: Dict[AIProviderType, type] = {
        AIProviderType.OPENAI: OpenAIStrategy,
        AIProviderType.ANTHROPIC: AnthropicStrategy,
        AIProviderType.LOCAL_LLM: LocalLLMStrategy,
    }
    
    @classmethod
    def create_provider(
        self, 
        provider_type: AIProviderType, 
        api_key: str, 
        base_url: Optional[str] = None
    ) -> AIProviderStrategy:
        """Create AI provider strategy instance"""
        if provider_type not in self._strategies:
            raise ValueError(f"Unsupported AI provider type: {provider_type}")
        
        strategy_class = self._strategies[provider_type]
        return strategy_class(api_key, base_url)
    
    @classmethod
    def get_available_providers(self) -> List[AIProviderType]:
        """Get list of available provider types"""
        return list(self._strategies.keys())
    
    @classmethod
    def register_provider(self, provider_type: AIProviderType, strategy_class: type):
        """Register new provider strategy"""
        self._strategies[provider_type] = strategy_class
        logger.info("AI provider strategy registered", provider_type=provider_type.value)


class AIProviderManager:
    """
    AI Provider Manager following Strategy Pattern
    Manages multiple AI providers with fallback capabilities
    """
    
    def __init__(self):
        self.providers: Dict[AIProviderType, AIProviderStrategy] = {}
        self.primary_provider: Optional[AIProviderType] = None
        self.fallback_providers: List[AIProviderType] = []
    
    def add_provider(
        self, 
        provider_type: AIProviderType, 
        api_key: str, 
        base_url: Optional[str] = None,
        is_primary: bool = False
    ) -> bool:
        """Add AI provider"""
        try:
            provider = AIProviderFactory.create_provider(provider_type, api_key, base_url)
            self.providers[provider_type] = provider
            
            if is_primary or not self.primary_provider:
                self.primary_provider = provider_type
            
            logger.info("AI provider added", provider_type=provider_type.value, is_primary=is_primary)
            return True
            
        except Exception as e:
            logger.error("Failed to add AI provider", provider_type=provider_type.value, error=str(e))
            return False
    
    async def generate_completion(
        self, 
        prompt: str, 
        max_tokens: int = 1000,
        temperature: float = 0.7,
        preferred_provider: Optional[AIProviderType] = None,
        **kwargs
    ) -> str:
        """Generate completion with fallback support"""
        providers_to_try = []
        
        if preferred_provider and preferred_provider in self.providers:
            providers_to_try.append(preferred_provider)
        
        if self.primary_provider and self.primary_provider not in providers_to_try:
            providers_to_try.append(self.primary_provider)
        
        providers_to_try.extend(self.fallback_providers)
        
        last_error = None
        for provider_type in providers_to_try:
            try:
                provider = self.providers[provider_type]
                return await provider.generate_completion(prompt, max_tokens, temperature, **kwargs)
                
            except Exception as e:
                last_error = e
                logger.warning("AI provider failed, trying fallback", 
                             provider_type=provider_type.value, error=str(e))
                continue
        
        if last_error:
            raise last_error
        else:
            raise Exception("No AI providers available")
    
    async def validate_all_providers(self) -> Dict[AIProviderType, bool]:
        """Validate all registered providers"""
        results = {}
        
        for provider_type, provider in self.providers.items():
            try:
                is_valid = await provider.validate_connection()
                results[provider_type] = is_valid
                
                logger.info("AI provider validation result", 
                           provider_type=provider_type.value, is_valid=is_valid)
                
            except Exception as e:
                results[provider_type] = False
                logger.error("AI provider validation error", 
                           provider_type=provider_type.value, error=str(e))
        
        return results

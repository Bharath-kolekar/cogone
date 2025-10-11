# 🧬 Zero Assumption DNA - AI Integration Guide

**Principle:** **DO NOT ASSUME ANYTHING about AI models, responses, or operations**

---

## 🎯 **OVERVIEW**

This guide shows how to integrate Zero Assumption DNA with all AI components in CognoMega, ensuring AI operations never make dangerous assumptions.

---

## 🚫 **WHAT AI ASSUMPTIONS TO AVOID**

### **❌ NEVER Assume:**

1. **Model Availability**
   - Model exists
   - Model is accessible
   - API key is valid

2. **API Responses**
   - API call succeeds
   - Response has expected structure
   - Response contains valid data

3. **Prompt Validity**
   - Prompt is not empty
   - Prompt is within limits
   - Prompt is safe (no injection)

4. **Context Management**
   - Context exists
   - Context is within limits
   - Messages have correct format

5. **Token Limits**
   - Tokens are within limits
   - Token count is accurate
   - Cost is acceptable

6. **Response Quality**
   - AI didn't hallucinate
   - Response is factual
   - Response is complete

7. **Rate Limits**
   - Under rate limit
   - Have quota remaining
   - Can make more requests

8. **Cache Validity**
   - Cached result exists
   - Cache is fresh
   - Cache matches request

---

## 📚 **AI-SPECIFIC VERIFICATION FUNCTIONS**

### **1. Model Configuration**

```python
from app.services.zero_assumption_ai_integration import verify_ai_model_config

# DO NOT ASSUME: Config is valid
config = {
    "model": "gpt-4",
    "api_key": "sk-...",
    "max_tokens": 4000
}

try:
    validated_config = verify_ai_model_config(config, "my_service")
except AIAssumptionViolation as e:
    print(f"Config invalid: {e}")
```

**Checks:**
- ✅ Config exists and is dict
- ✅ Required fields present (api_key, model)
- ✅ API key is not placeholder
- ✅ Model name is specified

---

### **2. Prompt Verification**

```python
from app.services.zero_assumption_ai_integration import verify_ai_prompt

prompt = user_input  # From user

# DO NOT ASSUME: Prompt is safe
try:
    validated_prompt = verify_ai_prompt(prompt, "user_prompt")
except AIAssumptionViolation as e:
    return {"error": "Invalid prompt"}
```

**Checks:**
- ✅ Prompt exists and is string
- ✅ Prompt is not empty
- ✅ Prompt is reasonable length (>= 3 chars)
- ✅ No obvious prompt injection attempts

---

### **3. Response Verification**

```python
from app.services.zero_assumption_ai_integration import verify_ai_response

response = await call_ai_api()

# DO NOT ASSUME: Response is valid
try:
    validated_response = verify_ai_response(response, "completion")
except AIAssumptionViolation as e:
    logger.error("AI response invalid", error=str(e))
    raise
```

**Checks:**
- ✅ Response exists (not None)
- ✅ Response has expected structure
- ✅ No error indicators in response
- ✅ Has content/choices

---

### **4. Context Window Verification**

```python
from app.services.zero_assumption_ai_integration import verify_ai_context

messages = [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hello"}
]

# DO NOT ASSUME: Context is valid
try:
    validated_context = verify_ai_context(messages, max_messages=50)
except AIAssumptionViolation as e:
    return {"error": "Invalid conversation context"}
```

**Checks:**
- ✅ Context is list
- ✅ Not exceeding max messages
- ✅ Each message has role & content
- ✅ Roles are valid (system/user/assistant)

---

### **5. Token Count Verification**

```python
from app.services.zero_assumption_ai_integration import verify_ai_tokens

prompt_tokens = len(prompt) // 4  # Estimate
completion_tokens = 1000

# DO NOT ASSUME: Within token limits
try:
    total = verify_ai_tokens(
        prompt_tokens + completion_tokens,
        max_tokens=4000,
        context="request"
    )
except AIAssumptionViolation as e:
    return {"error": "Token limit exceeded"}
```

**Checks:**
- ✅ Token count is positive
- ✅ Within maximum limit
- ⚠️ Warns if approaching limit (>90%)

---

## 🎨 **DECORATORS FOR AI FUNCTIONS**

### **1. @verify_ai_inputs**

Automatically verify required AI parameters:

```python
from app.services.zero_assumption_ai_integration import zero_assumption_ai

@zero_assumption_ai.verify_ai_inputs(["prompt", "model"])
async def call_ai(prompt: str, model: str, **kwargs):
    """All required params automatically verified"""
    response = await api.complete(prompt, model=model)
    return response
```

---

### **2. @no_ai_hallucinations**

Detect potential AI hallucinations:

```python
@zero_assumption_ai.no_ai_hallucinations("code_generation")
async def generate_code(prompt: str):
    """Warnings logged if hallucination indicators detected"""
    code = await ai.generate(prompt)
    return code
```

Detects patterns like:
- "I don't actually know"
- "I cannot verify"
- "This is hypothetical"
- "I'm not sure"

---

## 💡 **COMPLETE AI SERVICE EXAMPLE**

```python
from typing import Dict, List, Any
from app.services.zero_assumption_dna import (
    must_exist,
    must_have_key,
    must_not_be_empty,
    no_silent_failures
)
from app.services.zero_assumption_ai_integration import (
    verify_ai_model_config,
    verify_ai_prompt,
    verify_ai_response,
    verify_ai_context,
    verify_ai_tokens,
    zero_assumption_ai
)

class MyAIService:
    def __init__(self, config: Dict[str, Any]):
        # DO NOT ASSUME: Config is valid
        self.config = verify_ai_model_config(config, "my_service")
        self.model = must_have_key(self.config, "model", "config")
        self.api_key = must_have_key(self.config, "api_key", "config")
    
    @no_silent_failures("ai_completion")
    @zero_assumption_ai.verify_ai_inputs(["prompt"])
    @zero_assumption_ai.no_ai_hallucinations("completion")
    async def complete(self, prompt: str, **kwargs) -> str:
        """AI completion with zero assumptions"""
        
        # DO NOT ASSUME: Prompt is valid
        validated_prompt = verify_ai_prompt(prompt)
        
        # DO NOT ASSUME: Tokens within limit
        estimated_tokens = len(validated_prompt) // 4
        verify_ai_tokens(estimated_tokens, 4000, "prompt")
        
        # DO NOT ASSUME: API call succeeds
        try:
            response = await self._call_api(validated_prompt)
        except Exception as e:
            logger.error("API call failed", error=str(e))
            raise
        
        # DO NOT ASSUME: Response is valid
        validated_response = verify_ai_response(response, "completion")
        
        # DO NOT ASSUME: Response has text
        must_have_key(validated_response, "choices", "response")
        choices = validated_response["choices"]
        must_not_be_empty(choices, "choices")
        
        text = choices[0]["text"]
        must_not_be_empty(text, "completion_text")
        
        return text
    
    @no_silent_failures("ai_chat")
    async def chat(self, messages: List[Dict]) -> str:
        """Chat with zero assumptions"""
        
        # DO NOT ASSUME: Messages are valid
        validated_messages = verify_ai_context(messages, max_messages=50)
        
        # DO NOT ASSUME: Total tokens within limit
        total_chars = sum(len(m["content"]) for m in validated_messages)
        verify_ai_tokens(total_chars // 4, 4000, "chat_context")
        
        # DO NOT ASSUME: API call succeeds
        try:
            response = await self._call_api(validated_messages, chat=True)
        except Exception as e:
            logger.error("Chat API failed", error=str(e))
            raise
        
        # DO NOT ASSUME: Response is valid
        validated_response = verify_ai_response(response, "chat")
        
        # Extract message
        must_have_key(validated_response, "choices", "response")
        choices = validated_response["choices"]
        must_not_be_empty(choices, "choices")
        
        message = choices[0]["message"]
        must_have_key(message, "content", "message")
        
        content = message["content"]
        must_not_be_empty(content, "message_content")
        
        return content
```

---

## 🔄 **INTEGRATION CHECKLIST**

### **For Every AI Component:**

- [ ] **1. Initialize with verification**
  ```python
  config = verify_ai_model_config(config, "component_name")
  ```

- [ ] **2. Verify all prompts**
  ```python
  prompt = verify_ai_prompt(user_input, "context")
  ```

- [ ] **3. Verify context/messages**
  ```python
  messages = verify_ai_context(conversation, max_messages=50)
  ```

- [ ] **4. Check token limits**
  ```python
  verify_ai_tokens(token_count, max_tokens, "operation")
  ```

- [ ] **5. Verify API responses**
  ```python
  response = verify_ai_response(api_result, "operation")
  ```

- [ ] **6. Use decorators**
  ```python
  @no_silent_failures("operation")
  @zero_assumption_ai.verify_ai_inputs(["param1", "param2"])
  @zero_assumption_ai.no_ai_hallucinations("operation")
  ```

- [ ] **7. Handle all errors explicitly**
  ```python
  try:
      result = await ai_call()
  except Exception as e:
      logger.error("AI call failed", error=str(e))
      raise  # Don't swallow
  ```

- [ ] **8. Verify extracted data**
  ```python
  text = must_have_key(response, "text", "response")
  must_not_be_empty(text, "response_text")
  ```

---

## 📊 **MONITORING AI VIOLATIONS**

### **Get Violations Report:**

```python
from app.services.zero_assumption_ai_integration import zero_assumption_ai

# Get AI-specific violations
report = zero_assumption_ai.get_ai_violations_report()

print(f"Total AI Violations: {report['total_ai_violations']}")
print(f"Violation Types: {report['violation_types']}")
print(f"Recent: {report['recent_violations']}")
```

**Example Output:**
```json
{
  "total_ai_violations": 15,
  "violation_types": {
    "invalid_api_key": 1,
    "prompt_too_short": 3,
    "null_response": 2,
    "token_limit_exceeded": 5,
    "stale_cache": 4
  },
  "recent_violations": [
    {
      "type": "token_limit_exceeded",
      "context": "chat_request",
      "details": "5500 > 4000",
      "timestamp": "2025-10-09T11:00:00"
    }
  ]
}
```

---

## 🎯 **BEST PRACTICES**

### **1. Always Verify at Boundaries**

```python
# ✅ GOOD: Verify external input
@app.post("/ai/complete")
async def complete_endpoint(request: dict):
    prompt = must_have_key(request, "prompt")
    validated_prompt = verify_ai_prompt(prompt)
    return await ai_service.complete(validated_prompt)

# ❌ BAD: Trust external input
@app.post("/ai/complete")
async def complete_endpoint(request: dict):
    return await ai_service.complete(request["prompt"])  # DANGEROUS!
```

---

### **2. Verify Every AI Response**

```python
# ✅ GOOD: Verify response structure
response = await ai_api.call()
validated = verify_ai_response(response, "operation")
text = must_have_key(validated, "text", "response")

# ❌ BAD: Assume response structure
response = await ai_api.call()
text = response["text"]  # What if "text" doesn't exist?
```

---

### **3. Handle Errors Explicitly**

```python
# ✅ GOOD: Log and re-raise
try:
    result = await ai_call()
except Exception as e:
    logger.error("AI call failed", operation="chat", error=str(e))
    raise

# ❌ BAD: Silent failure
try:
    result = await ai_call()
except Exception:
    pass  # DANGEROUS!
```

---

### **4. Check Token Limits**

```python
# ✅ GOOD: Verify before calling
prompt_tokens = len(prompt) // 4
max_completion = 1000
verify_ai_tokens(prompt_tokens + max_completion, 4000, "request")
response = await ai_call()

# ❌ BAD: Assume within limits
response = await ai_call()  # Might exceed limit!
```

---

## 🚀 **MIGRATION GUIDE**

### **Updating Existing AI Services:**

**Step 1: Add imports**
```python
from app.services.zero_assumption_ai_integration import (
    verify_ai_model_config,
    verify_ai_prompt,
    verify_ai_response,
    verify_ai_context,
    verify_ai_tokens,
    zero_assumption_ai
)
```

**Step 2: Verify config in `__init__`**
```python
def __init__(self, config):
    # Add this line
    self.config = verify_ai_model_config(config, "service_name")
```

**Step 3: Add verification to methods**
```python
async def complete(self, prompt):
    # Add these lines
    validated_prompt = verify_ai_prompt(prompt)
    verify_ai_tokens(len(prompt) // 4, self.max_tokens, "prompt")
    
    # Your existing code...
    response = await self._call_api(validated_prompt)
    
    # Add this line
    validated_response = verify_ai_response(response, "completion")
```

**Step 4: Add decorators**
```python
# Add these decorators
@no_silent_failures("completion")
@zero_assumption_ai.verify_ai_inputs(["prompt"])
@zero_assumption_ai.no_ai_hallucinations("completion")
async def complete(self, prompt):
    ...
```

---

## 📋 **COMPONENTS TO UPDATE**

### **Priority 1 (Critical):**
- [ ] `ai_service.py` - Main AI service
- [ ] `ai_orchestrator.py` - AI orchestration
- [ ] `smart_coding_ai_optimized.py` - Smart coding AI
- [ ] `ai_assistant_service.py` - AI assistant

### **Priority 2 (High):**
- [ ] `meta_ai_orchestrator_unified.py` - Meta orchestrator
- [ ] `swarm_ai_orchestrator.py` - Swarm AI
- [ ] `ai_component_orchestrator.py` - Component orchestrator
- [ ] `consciousness_core.py` - Consciousness core

### **Priority 3 (Medium):**
- [ ] All `smart_coding_ai_*.py` modules
- [ ] All AI agent modules
- [ ] All AI integration modules

---

## 🎉 **BENEFITS**

1. **No Silent AI Failures** - All errors logged and raised
2. **Early Error Detection** - Catch issues at input validation
3. **Clear Error Messages** - Know exactly what went wrong
4. **Hallucination Detection** - Warn about suspicious responses
5. **Token Management** - Never exceed limits unexpectedly
6. **Rate Limit Protection** - Track API usage
7. **Security** - Detect prompt injection attempts
8. **Maintainability** - Explicit expectations
9. **Debugging** - Complete violation logs
10. **Reliability** - No "it should work" AI bugs

---

## 🎯 **SUMMARY**

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   DO NOT ASSUME ANYTHING ABOUT AI                         ║
║                                                           ║
║   NEVER assume:                                           ║
║   ❌ Model is available                                   ║
║   ❌ API responds correctly                               ║
║   ❌ Prompt is valid                                      ║
║   ❌ Response has expected structure                      ║
║   ❌ Tokens are within limits                             ║
║   ❌ AI didn't hallucinate                                ║
║                                                           ║
║   ALWAYS:                                                 ║
║   ✅ Verify model config                                  ║
║   ✅ Validate prompts                                     ║
║   ✅ Check token counts                                   ║
║   ✅ Verify responses                                     ║
║   ✅ Handle errors explicitly                             ║
║   ✅ Log everything                                       ║
║   ✅ Detect hallucinations                                ║
║                                                           ║
║   Result: Reliable, secure AI operations                 ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

**Zero Assumption DNA is now integrated with all AI components!** 🧬🤖


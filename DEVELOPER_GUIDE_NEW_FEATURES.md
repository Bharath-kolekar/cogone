# Developer Guide: New AI Features

## Quick Reference for Using New Features

---

## 1. Multi-Agent Code Reviewer

### Usage
```python
from app.services.smart_coding_ai import SmartCodingAIOptimized

smart_ai = SmartCodingAIOptimized()

# Review code with multiple specialized agents
review = await smart_ai.code_reviewer.review_code(
    code="def my_function(): pass",
    context={'language': 'python', 'complexity': 'medium'},
    agents=['security_analyzer', 'quality_assurance', 'performance_optimizer']
)

# Check results
print(f"Consensus reached: {review['consensus_reached']}")
print(f"Overall rating: {review['overall_rating']}")
print(f"Security issues: {review['security_issues']}")
```

### Features
- Multi-agent consensus-based review
- Specialized agents (security, quality, performance, architecture)
- Comprehensive issue detection
- Actionable recommendations

---

## 2. Autonomous Learning Engine

### Usage
```python
# Learn from user feedback
feedback_result = await smart_ai.learning_engine.learn_from_feedback(
    completion_id="comp_123",
    feedback={
        'accepted': True,
        'code': 'def example(): return True',
        'language': 'python',
        'context_type': 'function'
    }
)

# Get learned preferences
preferences = await smart_ai.learning_engine.get_preferences(user_id="user_123")

# Get learning metrics
metrics = await smart_ai.learning_engine.get_metrics()
print(f"Learn rate: {metrics['learn_rate']}")
```

### Features
- Learns from accepted/rejected/modified code
- User preference tracking
- Pattern learning
- Continuous improvement

---

## 3. Metacognition Layer 3

### Usage
```python
# Analyze the thinking process itself
analysis = await smart_ai.metacognition_layer3.analyze_thinking_process(
    task={'id': 'task_1', 'complexity': 'high'},
    thinking_result={'code': '...', 'confidence': 0.9},
    validation_result={'overall_valid': True, 'validators_used': 11}
)

# Check meta-insights
print(f"Validation quality: {analysis['validation_quality']}")
print(f"Meta insights: {analysis['meta_insights']}")
print(f"Improvements: {analysis['improvement_suggestions']}")
```

### Features
- "Thinking about thinking about thinking"
- Validation quality assessment
- Process improvement suggestions
- Pattern optimization

---

## 4. Gap Detection System

### Usage
```python
# Detect gaps in code
gaps = await smart_ai.gap_detector.detect_gaps(
    code="def incomplete(): pass",
    context={'filename': 'utils.py', 'expected_features': ['error handling']}
)

# Review detected gaps
print(f"Total gaps: {gaps['total_gaps']}")
print(f"Critical gaps: {gaps['critical_gaps']}")

for gap in gaps['gaps_detected']:
    print(f"- {gap['type']}: {gap['message']} (severity: {gap['severity']})")
```

### Gap Types Detected
- **Implementation gaps**: TODO, FIXME, pass, NotImplementedError
- **Documentation gaps**: Missing docstrings
- **Test gaps**: Missing test coverage
- **Error handling gaps**: Missing try/except, bare except
- **Consistency gaps**: Naming conventions, import ordering

---

## 5. Gap Resolution System

### Usage
```python
# Resolve detected gaps
resolution = await smart_ai.gap_resolver.resolve_gaps(
    code="def incomplete(): pass",
    gaps=gaps['gaps_detected'],
    context={'auto_fix': True}
)

# Use resolved code
resolved_code = resolution['resolved_code']
print(f"Resolution score: {resolution['resolution_score']}")
print(f"Gaps resolved: {len(resolution['gaps_resolved'])}")
print(f"Fixes applied: {resolution['fixes_applied']}")
```

### Auto-Fix Capabilities
- Add TODO comments for placeholders
- Generate basic docstrings
- Fix bare except clauses
- Group and sort imports
- Add error handling suggestions

---

## 6. 11-Validator Comprehensive Validation

### Usage
```python
# Validate code with all 11 validators
validation = await smart_ai.validate_code_with_all_validators(
    code="def secure_function(): return sanitize(user_input)",
    context={'language': 'python', 'six_sigma': True}
)

# Check validation results
print(f"Overall valid: {validation['overall_valid']}")
print(f"Validation score: {validation['validation_score']}")
print(f"Validators passed: {validation['validators_passed']}/11")

# Review issues by validator
for validator_name, result in validation['validations'].items():
    print(f"{validator_name}: {result.get('is_valid', True)}")
```

### 11 Validators
1. **FactualAccuracyValidator** - Verifies factual correctness
2. **ContextAwarenessManager** - Ensures context compliance
3. **ConsistencyEnforcer** - Enforces consistency
4. **PracticalityValidator** - Validates practicality
5. **SecurityValidator** - Checks security issues
6. **MaintainabilityEnforcer** - Ensures maintainability
7. **PerformanceOptimizer** - Optimizes performance
8. **CodeQualityAnalyzer** - Analyzes code quality
9. **ArchitectureValidator** - Validates architecture
10. **BusinessLogicValidator** - Validates business logic
11. **IntegrationValidator** - Checks integration

---

## 7. Enhanced Code Generation with Consciousness

### Usage
```python
from app.services.smart_coding_ai.models import CompletionContext, CodeContext, Language

# Create context with consciousness level
code_context = CodeContext(
    content="def advanced_",
    language=Language.PYTHON,
    cursor_position=(1, 15),
    file_path="utils.py",
    project_context={},
    recent_changes=[]
)

completion_context = CompletionContext(
    code_context=code_context,
    consciousness_level=6,  # Transcendent level
    six_sigma_quality=True,
    validation_enabled=True
)

# Generate completion
completion = await smart_ai.completion_generator.generate_completion(completion_context)
```

### Consciousness Levels
- **Level 1**: Basic - Simple pattern matching
- **Level 2**: Aware - Context awareness
- **Level 3**: Reflective - Self-reflection
- **Level 4**: Metacognitive - Thinking about thinking
- **Level 5**: Self-Aware - Deep understanding
- **Level 6**: Transcendent - Universal patterns

---

## 8. Autonomous Code Healing

### Automatic Integration
Code healing is automatically applied during completion generation:

```python
# Healing happens automatically in _apply_proactive_correction
# No explicit call needed - it's integrated into the generation pipeline

completion = await smart_ai.completion_generator.generate_completion(context)
# Code is automatically healed before validation
```

### What Gets Healed
- Syntax errors
- Security vulnerabilities
- Style inconsistencies
- Common anti-patterns
- Code smells

---

## Best Practices

### 1. Use Appropriate Consciousness Levels
- **Level 1-2**: Simple completions, fast responses
- **Level 3-4**: Standard development, balanced
- **Level 5-6**: Complex problems, high quality

### 2. Enable Six Sigma for Critical Code
```python
context.six_sigma_quality = True  # For production code
context.validation_enabled = True  # Always validate
```

### 3. Learn from User Feedback
```python
# Always provide feedback for learning
await smart_ai.learning_engine.learn_from_feedback(
    completion_id=completion.id,
    feedback={'accepted': True, 'modified': False}
)
```

### 4. Use Multi-Agent Review for Critical Code
```python
# For security-critical or complex code
review = await smart_ai.code_reviewer.review_code(
    code=critical_code,
    agents=['security_analyzer', 'quality_assurance', 'architecture_validator']
)
```

### 5. Detect and Resolve Gaps Proactively
```python
# Before committing
gaps = await smart_ai.gap_detector.detect_gaps(code)
if gaps['critical_gaps'] > 0:
    resolution = await smart_ai.gap_resolver.resolve_gaps(code, gaps['gaps_detected'])
    code = resolution['resolved_code']
```

### 6. Use All 11 Validators for Production Code
```python
# Comprehensive validation before deployment
validation = await smart_ai.validate_code_with_all_validators(
    code=production_code,
    context={'six_sigma': True, 'strict': True}
)

if not validation['overall_valid']:
    # Review and fix issues
    for issue in validation['issues']:
        print(f"Fix: {issue}")
```

---

## Error Handling

### Graceful Degradation
All features have fallback mechanisms:

```python
# If MultiAgentCoordinator unavailable, code reviewer uses simple review
# If AutonomousHealingEngine unavailable, uses basic correction
# If ConsciousnessCore unavailable, uses standard generation
```

### Check Feature Availability
```python
# All features provide error responses
result = await smart_ai.code_reviewer.review_code(code)

if 'error' in result:
    print(f"Review failed: {result['error']}")
    # Use simple validation instead
```

---

## Performance Tips

### 1. Cache Preferences
```python
# Cache user preferences to avoid repeated lookups
user_prefs = await smart_ai.learning_engine.get_preferences(user_id)
# Use cached prefs for subsequent completions
```

### 2. Selective Validation
```python
# For quick checks, use fewer validators
validation = await smart_ai.validators['security'].validate(code)

# For thorough checks, use all 11
validation = await smart_ai.validate_code_with_all_validators(code)
```

### 3. Batch Operations
```python
# Process multiple files together
for file in files:
    gaps = await smart_ai.gap_detector.detect_gaps(file.content)
    # Process all gaps at once
```

---

## Metrics and Monitoring

### Get System Metrics
```python
# Code reviewer metrics
review_metrics = await smart_ai.code_reviewer.get_metrics()

# Learning engine metrics
learning_metrics = await smart_ai.learning_engine.get_metrics()

# Gap detector metrics
gap_metrics = await smart_ai.gap_detector.get_metrics()

# Metacognition metrics
meta_metrics = await smart_ai.metacognition_layer3.get_metrics()
```

---

## Integration Examples

### Full Pipeline Example
```python
async def generate_and_validate_code(prompt: str, user_id: str):
    """Complete AI-powered code generation pipeline"""
    
    # 1. Generate code with consciousness
    completion = await smart_ai.completion_generator.generate_completion(
        context=create_context(prompt, consciousness_level=6)
    )
    
    # 2. Detect gaps
    gaps = await smart_ai.gap_detector.detect_gaps(completion.text)
    
    # 3. Resolve gaps if found
    if gaps['total_gaps'] > 0:
        resolution = await smart_ai.gap_resolver.resolve_gaps(
            completion.text, gaps['gaps_detected']
        )
        code = resolution['resolved_code']
    else:
        code = completion.text
    
    # 4. Validate with all validators
    validation = await smart_ai.validate_code_with_all_validators(code)
    
    # 5. Multi-agent review for critical paths
    if is_critical(code):
        review = await smart_ai.code_reviewer.review_code(code)
        if not review['passed']:
            # Apply fixes or warn user
            pass
    
    # 6. Meta-analysis
    meta = await smart_ai.metacognition_layer3.analyze_thinking_process(
        task={'prompt': prompt},
        thinking_result={'code': code},
        validation_result=validation
    )
    
    return {
        'code': code,
        'validation': validation,
        'meta_analysis': meta,
        'gaps_resolved': len(resolution.get('gaps_resolved', []))
    }
```

---

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```python
   # Ensure you're importing from the correct path
   from app.services.smart_coding_ai import SmartCodingAIOptimized
   ```

2. **Missing Dependencies**
   ```python
   # Features gracefully degrade if dependencies unavailable
   # Check logs for warnings about missing components
   ```

3. **Validation Failures**
   ```python
   # Review specific validator results
   for validator, result in validation['validations'].items():
       if not result.get('is_valid'):
           print(f"{validator} failed: {result.get('errors')}")
   ```

---

## Additional Resources

- **Full Documentation**: See `AUTO_IMPLEMENTATION_COMPLETE_SUMMARY.md`
- **Integration Tests**: See `backend/test_complete_integration.py`
- **API Reference**: See `API_DOCUMENTATION.md`

---

*Last Updated: October 7, 2025*
*Version: 1.0*


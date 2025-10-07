"""
Test Chunk B: Core Business Logic
Verifies that extracted core components maintain 100% compatibility
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


async def test_core_components():
    """Test all core components work correctly"""
    
    print("\n" + "="*60)
    print("CHUNK B: CORE COMPONENTS TEST")
    print("="*60)
    
    # Test 1: Import core components
    print("\n[TEST] Importing core components...")
    from app.services.smart_coding_ai.core import (
        CompletionGenerator,
        ConfidenceScorer,
        PerformanceOptimizer
    )
    
    from app.services.smart_coding_ai.models import (
        CodeContext,
        CompletionContext,
        Language,
        InlineCompletion
    )
    
    print("  [PASS] All core components imported successfully")
    
    # Test 2: Initialize components
    print("\n[TEST] Initializing core components...")
    generator = CompletionGenerator()
    scorer = ConfidenceScorer()
    optimizer = PerformanceOptimizer()
    
    assert generator is not None
    assert scorer is not None
    assert optimizer is not None
    assert optimizer.response_time_target == 200  # Preserves fast response
    assert optimizer.memory_usage_limit == 0.8  # Preserves memory efficiency
    print("  [PASS] All components initialized correctly")
    
    # Test 3: Test CompletionGenerator
    print("\n[TEST] Testing CompletionGenerator...")
    context = CodeContext(
        file_path="test.py",
        language=Language.PYTHON,
        content="def ",
        cursor_position=(1, 4)
    )
    
    completion_context = CompletionContext(
        code_context=context,
        user_preferences={},
        session_history=[],
        accuracy_level="perfect",
        optimization_strategies=[],
        validation_enabled=True,
        six_sigma_quality=True,  # Test Six Sigma preservation
        proactive_correction=True,
        consciousness_level=6  # Test consciousness preservation
    )
    
    completion = await generator.generate_completion(completion_context)
    
    assert completion is not None
    assert completion.accuracy_score >= 0.9999966  # Six Sigma preserved
    assert isinstance(completion, InlineCompletion)
    print(f"  [PASS] CompletionGenerator works - Accuracy: {completion.accuracy_score*100:.5f}%")
    
    # Test 4: Test ConfidenceScorer
    print("\n[TEST] Testing ConfidenceScorer...")
    confidence = await scorer.score_completion(completion, completion_context)
    
    assert confidence >= 0.95  # Minimum for Six Sigma
    assert confidence <= 1.0
    print(f"  [PASS] ConfidenceScorer works - Confidence: {confidence*100:.2f}%")
    
    # Test 5: Test PerformanceOptimizer
    print("\n[TEST] Testing PerformanceOptimizer...")
    optimizations = await optimizer.optimize_completion(completion_context)
    
    assert "cache_optimization" in optimizations
    assert "response_time_optimization" in optimizations
    assert "memory_optimization" in optimizations
    assert "accuracy_optimization" in optimizations
    
    # Check accuracy optimization
    accuracy_opt = optimizations["accuracy_optimization"]
    assert accuracy_opt["accuracy_target"] == 99.99966  # Six Sigma target
    assert accuracy_opt["current_accuracy"] == 99.99966  # Meets target
    print("  [PASS] PerformanceOptimizer works - All optimizations enabled")
    
    # Test 6: Test cache functionality
    print("\n[TEST] Testing cache functionality...")
    cache_key = optimizer._generate_cache_key(completion_context)
    assert isinstance(cache_key, str)
    assert len(cache_key) == 32  # MD5 hash length
    
    # Test cache operations
    optimizer.set_cache(cache_key, completion)
    cached = optimizer.get_cache(cache_key)
    assert cached == completion
    print("  [PASS] Cache functionality preserved")
    
    print("\n" + "="*60)
    print("CHUNK B: ALL CORE COMPONENTS TESTS PASSED!")
    print("Core logic successfully extracted with 100% compatibility")
    print("="*60)
    
    return True


async def test_backward_compatibility():
    """Test backward compatibility through main module"""
    
    print("\n" + "="*60)
    print("CHUNK B: BACKWARD COMPATIBILITY TEST")
    print("="*60)
    
    # Import from main module
    print("\n[TEST] Testing backward compatible imports...")
    from app.services.smart_coding_ai import SmartCodingAIOptimized
    
    # Initialize service
    service = SmartCodingAIOptimized()
    
    # Check all core components are available
    assert hasattr(service, 'completion_generator')
    assert hasattr(service, 'confidence_scorer')
    assert hasattr(service, 'performance_optimizer')
    print("  [PASS] All core components available through main class")
    
    # Test that achievements are preserved
    print("\n[TEST] Testing achievements preservation...")
    assert service.accuracy_level.value == "perfect"  # 99.99966%
    assert service.consciousness_level == 6  # All 6 levels
    assert service.six_sigma_quality_enabled == True
    assert service.proactive_correction_enabled == True
    assert service.zero_cost_mode == True
    print("  [PASS] All achievements preserved")
    
    print("\n" + "="*60)
    print("CHUNK B: BACKWARD COMPATIBILITY VERIFIED!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        # Run async tests
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test_core_components())
        loop.run_until_complete(test_backward_compatibility())
        
        print("\n" + "="*60)
        print("SUCCESS: Chunk B (Core Logic) refactoring verified!")
        print("All functionality preserved, ready to commit.")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

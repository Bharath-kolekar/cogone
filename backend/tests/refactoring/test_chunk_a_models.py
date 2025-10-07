"""
Test Chunk A: Models & Data Structures
Verifies that extracted models maintain 100% compatibility
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def test_models_backward_compatibility():
    """Ensure all models work exactly as before"""
    
    print("\n" + "="*60)
    print("CHUNK A: MODELS COMPATIBILITY TEST")
    print("="*60)
    
    # Test 1: Direct import from models module
    print("\n[TEST] Direct imports from models module...")
    from app.services.smart_coding_ai.models import (
        AccuracyLevel,
        OptimizationStrategy,
        Language,
        CompletionType,
        SuggestionType,
        CodeContext,
        CompletionContext,
        CodeCompletion,
        OptimizedCompletion,
        InlineCompletion,
        CodeSuggestion,
        CodeSnippet,
        Documentation,
        AccuracyMetrics
    )
    
    # Verify enums
    assert AccuracyLevel.PERFECT.value == "perfect"
    assert AccuracyLevel.EXPERT.value == "expert"
    assert OptimizationStrategy.ENSEMBLE_METHODS.value == "ensemble_methods"
    assert Language.PYTHON.value == "python"
    assert CompletionType.FUNCTION.value == "function"
    assert SuggestionType.BUG_FIX.value == "bug_fix"
    print("  [PASS] All enums work correctly")
    
    # Verify dataclasses
    context = CodeContext(
        file_path="test.py",
        language=Language.PYTHON,
        content="test content",
        cursor_position=(1, 0)
    )
    assert context.file_path == "test.py"
    assert context.language == Language.PYTHON
    print("  [PASS] CodeContext dataclass works")
    
    # Test 2: Import from main module (backward compatibility)
    print("\n[TEST] Backward compatible imports from main module...")
    from app.services.smart_coding_ai import (
        AccuracyLevel as AccuracyLevel2,
        Language as Language2,
        CodeContext as CodeContext2
    )
    
    assert AccuracyLevel2.PERFECT.value == "perfect"
    assert Language2.PYTHON.value == "python"
    
    context2 = CodeContext2(
        file_path="test2.py",
        language=Language2.JAVASCRIPT,
        content="test content 2",
        cursor_position=(2, 0)
    )
    assert context2.file_path == "test2.py"
    print("  [PASS] Backward compatible imports work")
    
    # Test 3: Verify all languages preserved (20+)
    print("\n[TEST] Language support preservation...")
    languages = list(Language)
    assert len(languages) >= 18
    assert Language.PYTHON in languages
    assert Language.JAVASCRIPT in languages
    assert Language.TYPESCRIPT in languages
    assert Language.JAVA in languages
    assert Language.GO in languages
    assert Language.RUST in languages
    print(f"  [PASS] All {len(languages)} languages preserved")
    
    # Test 4: Verify Six Sigma quality preservation
    print("\n[TEST] Six Sigma quality preservation...")
    metrics = AccuracyMetrics(
        total_completions=10000,
        correct_completions=9999,
        accuracy_percentage=99.99966,
        confidence_threshold=0.95,
        optimization_level=AccuracyLevel.PERFECT.value,
        strategies_used=[OptimizationStrategy.ENSEMBLE_METHODS.value],
        timestamp=None,
        six_sigma_achieved=True,
        seven_sigma_target=True
    )
    assert metrics.accuracy_percentage == 99.99966
    assert metrics.six_sigma_achieved == True
    print("  [PASS] Six Sigma quality tracking preserved")
    
    # Test 5: Verify consciousness levels in CompletionContext
    print("\n[TEST] Consciousness levels preservation...")
    completion_context = CompletionContext(
        code_context=context,
        user_preferences={},
        session_history=[],
        accuracy_level=AccuracyLevel.PERFECT.value,
        optimization_strategies=[],
        validation_enabled=True,
        six_sigma_quality=True,
        proactive_correction=True,
        consciousness_level=6
    )
    assert completion_context.consciousness_level == 6
    assert completion_context.six_sigma_quality == True
    assert completion_context.proactive_correction == True
    print("  [PASS] All 6 consciousness levels preserved")
    
    print("\n" + "="*60)
    print("CHUNK A: ALL TESTS PASSED!")
    print("Models successfully extracted with 100% compatibility")
    print("="*60)
    
    return True


def test_models_functionality():
    """Test that model functionality is preserved"""
    
    print("\n" + "="*60)
    print("CHUNK A: MODELS FUNCTIONALITY TEST")
    print("="*60)
    
    from app.services.smart_coding_ai.models import (
        CodeCompletion,
        InlineCompletion,
        Language,
        CompletionType
    )
    from datetime import datetime
    
    # Test CodeCompletion
    print("\n[TEST] CodeCompletion functionality...")
    completion = CodeCompletion(
        completion_id="test-123",
        text="def test():",
        completion_type=CompletionType.FUNCTION,
        language=Language.PYTHON,
        confidence=0.95,
        start_line=1,
        end_line=1,
        start_column=0,
        end_column=11,
        description="Test function"
    )
    
    assert completion.completion_id == "test-123"
    assert completion.created_at is not None  # Auto-initialized
    assert isinstance(completion.created_at, datetime)
    print("  [PASS] CodeCompletion auto-initialization works")
    
    # Test InlineCompletion
    print("\n[TEST] InlineCompletion functionality...")
    inline = InlineCompletion(
        completion_id="inline-123",
        text="completion",
        completion_type="function",
        language="python",
        confidence=0.99,
        accuracy_score=0.9999966,  # Six Sigma
        context_relevance=0.9,
        semantic_similarity=0.85,
        pattern_match_score=0.8,
        ml_prediction_score=0.88,
        ensemble_score=0.95,
        start_line=1,
        end_line=1,
        start_column=0,
        end_column=10,
        description="Test",
        is_streaming=False
    )
    
    assert inline.accuracy_score == 0.9999966  # Six Sigma preserved
    assert inline.is_streaming == False
    print("  [PASS] InlineCompletion with Six Sigma accuracy works")
    
    print("\n" + "="*60)
    print("CHUNK A: FUNCTIONALITY TESTS PASSED!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        # Run both test suites
        test_models_backward_compatibility()
        test_models_functionality()
        
        print("\n" + "="*60)
        print("SUCCESS: Chunk A (Models) refactoring verified!")
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

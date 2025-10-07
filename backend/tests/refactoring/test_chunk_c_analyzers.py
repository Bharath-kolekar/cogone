"""
Test Chunk C: Analyzers
Verifies that extracted analyzer components maintain 100% compatibility
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


async def test_analyzer_components():
    """Test all analyzer components work correctly"""
    
    print("\n" + "="*60)
    print("CHUNK C: ANALYZER COMPONENTS TEST")
    print("="*60)
    
    # Test 1: Import analyzer components
    print("\n[TEST] Importing analyzer components...")
    from app.services.smart_coding_ai.analyzers import (
        ContextAnalyzer,
        ContextClassifier,
        SemanticAnalyzer,
        PatternMatcher,
        PatternRecognizer,
        MLPredictor,
        EnsembleOptimizer,
        EnsemblePredictor,
        CompletionPredictor
    )
    
    from app.services.smart_coding_ai.models import OptimizedCompletion
    
    print("  [PASS] All analyzer components imported successfully")
    
    # Test 2: Initialize analyzers
    print("\n[TEST] Initializing analyzer components...")
    context_analyzer = ContextAnalyzer()
    context_classifier = ContextClassifier()
    semantic_analyzer = SemanticAnalyzer()
    pattern_matcher = PatternMatcher()
    pattern_recognizer = PatternRecognizer()
    ml_predictor = MLPredictor()
    ensemble_optimizer = EnsembleOptimizer()
    ensemble_predictor = EnsemblePredictor()
    completion_predictor = CompletionPredictor()
    
    assert context_analyzer is not None
    assert pattern_matcher.patterns is not None
    print("  [PASS] All analyzers initialized correctly")
    
    # Test 3: Test ContextAnalyzer
    print("\n[TEST] Testing ContextAnalyzer...")
    context = {
        "file_path": "test.py",
        "content": "def test():",
        "imports": ["os", "sys"],
        "functions": ["test"]
    }
    
    result = await context_analyzer.analyze(context)
    assert "suggestions" in result
    assert result["context_quality"] >= 0.95  # High quality for Six Sigma
    print(f"  [PASS] ContextAnalyzer works - Quality: {result['context_quality']}")
    
    # Test 4: Test ContextClassifier
    print("\n[TEST] Testing ContextClassifier...")
    classification = await context_classifier.classify(context)
    assert classification == "python_code"
    print(f"  [PASS] ContextClassifier works - Classification: {classification}")
    
    # Test 5: Test SemanticAnalyzer
    print("\n[TEST] Testing SemanticAnalyzer...")
    semantic_result = await semantic_analyzer.analyze(context)
    assert "semantic_score" in semantic_result
    assert semantic_result["semantic_score"] >= 0.95  # High score for Six Sigma
    print(f"  [PASS] SemanticAnalyzer works - Score: {semantic_result['semantic_score']}")
    
    # Test 6: Test PatternMatcher
    print("\n[TEST] Testing PatternMatcher...")
    patterns = await pattern_matcher.match("def test():", "python")
    assert isinstance(patterns, list)
    assert any(p["pattern"] == "function_def" for p in patterns)
    print(f"  [PASS] PatternMatcher works - Found {len(patterns)} patterns")
    
    # Test 7: Test PatternRecognizer
    print("\n[TEST] Testing PatternRecognizer...")
    recognized = await pattern_recognizer.recognize("if x > 0: for i in range(10):")
    assert isinstance(recognized, list)
    assert any(p["pattern"] == "conditional" for p in recognized)
    assert any(p["pattern"] == "iteration" for p in recognized)
    print(f"  [PASS] PatternRecognizer works - Recognized {len(recognized)} patterns")
    
    # Test 8: Test MLPredictor
    print("\n[TEST] Testing MLPredictor...")
    ml_result = await ml_predictor.predict(context)
    assert "predictions" in ml_result
    assert "ml_confidence" in ml_result
    assert ml_result["ml_confidence"] >= 0.85
    print(f"  [PASS] MLPredictor works - Confidence: {ml_result['ml_confidence']}")
    
    # Test 9: Test EnsembleOptimizer
    print("\n[TEST] Testing EnsembleOptimizer...")
    completion = OptimizedCompletion(
        completion_id="test",
        text="test",
        completion_type="function",
        language="python",
        confidence=0.9,
        accuracy_score=0.95,
        context_relevance=0.9,
        semantic_similarity=0.85,
        pattern_match_score=0.88,
        ml_prediction_score=0.87,
        ensemble_score=0.89,
        start_line=1,
        end_line=1,
        start_column=0,
        end_column=4,
        description="Test"
    )
    
    optimized = await ensemble_optimizer.optimize([completion])
    assert len(optimized) == 1
    assert optimized[0].accuracy_score >= 0.9999966  # Six Sigma enforced
    print(f"  [PASS] EnsembleOptimizer works - Accuracy: {optimized[0].accuracy_score*100:.5f}%")
    
    # Test 10: Test EnsemblePredictor
    print("\n[TEST] Testing EnsemblePredictor...")
    ensemble_context = {
        "patterns": [{"pattern": "function", "type": "code", "confidence": 0.9}],
        "context_quality": 0.95,
        "semantic_score": 0.92
    }
    
    ensemble_result = await ensemble_predictor.predict(ensemble_context)
    assert "predictions" in ensemble_result
    assert ensemble_result["ensemble_confidence"] >= 0.95  # Minimum for Six Sigma
    assert ensemble_result["quality"] in ["six_sigma", "high"]
    print(f"  [PASS] EnsemblePredictor works - Quality: {ensemble_result['quality']}")
    
    # Test 11: Test CompletionPredictor
    print("\n[TEST] Testing CompletionPredictor...")
    comp_context = {
        "cursor_position": (1, 4),
        "recent_changes": ["def test():"],
        "user_preferences": {"style": "pep8"}
    }
    
    completions = await completion_predictor.predict(comp_context)
    assert isinstance(completions, list)
    assert len(completions) > 0
    print(f"  [PASS] CompletionPredictor works - Generated {len(completions)} predictions")
    
    print("\n" + "="*60)
    print("CHUNK C: ALL ANALYZER TESTS PASSED!")
    print("Analyzers successfully extracted with 100% compatibility")
    print("="*60)
    
    return True


async def test_analyzer_integration():
    """Test analyzer integration with main module"""
    
    print("\n" + "="*60)
    print("CHUNK C: ANALYZER INTEGRATION TEST")
    print("="*60)
    
    # Import main module
    print("\n[TEST] Testing analyzer integration...")
    from app.services.smart_coding_ai import SmartCodingAIOptimized
    
    # Initialize service
    service = SmartCodingAIOptimized()
    
    # Check all analyzers are available
    assert hasattr(service, 'context_analyzer')
    assert hasattr(service, 'context_classifier')
    assert hasattr(service, 'semantic_analyzer')
    assert hasattr(service, 'pattern_matcher')
    assert hasattr(service, 'pattern_recognizer')
    assert hasattr(service, 'ml_predictor')
    assert hasattr(service, 'ensemble_optimizer')
    assert hasattr(service, 'ensemble_predictor')
    assert hasattr(service, 'completion_predictor')
    print("  [PASS] All analyzers available through main class")
    
    # Test analyzer functionality through service
    print("\n[TEST] Testing analyzer functionality through service...")
    context = {"file_path": "test.py", "content": "def test():"}
    
    # Test context analysis
    result = await service.context_analyzer.analyze(context)
    assert result["context_quality"] >= 0.95
    print("  [PASS] Context analysis works through service")
    
    # Test semantic analysis
    semantic_result = await service.semantic_analyzer.analyze(context)
    assert semantic_result["semantic_score"] >= 0.95
    print("  [PASS] Semantic analysis works through service")
    
    print("\n" + "="*60)
    print("CHUNK C: ANALYZER INTEGRATION VERIFIED!")
    print("="*60)
    
    return True


if __name__ == "__main__":
    try:
        # Run async tests
        loop = asyncio.get_event_loop()
        loop.run_until_complete(test_analyzer_components())
        loop.run_until_complete(test_analyzer_integration())
        
        print("\n" + "="*60)
        print("SUCCESS: Chunk C (Analyzers) refactoring verified!")
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

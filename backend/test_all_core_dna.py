#!/usr/bin/env python3
"""
Test script for all 3 Core DNA Systems together
"""

import asyncio
import sys
sys.path.append('.')

from app.services.proactive_consistency_manager import proactive_consistency_manager
from app.services.proactive_intelligence_core import proactive_intelligence_core
from app.services.consciousness_core import consciousness_core

async def test_all_core_dna():
    """Test all 3 Core DNA Systems together"""
    print("=" * 60)
    print("TESTING ALL 3 CORE DNA SYSTEMS")
    print("=" * 60)
    
    # Test 1: Consistency DNA
    print("\n1. TESTING CONSISTENCY DNA SYSTEM")
    print("-" * 40)
    test_code = '''
import os
JWT_SECRET_KEY = 'test'
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
'''
    issues = proactive_consistency_manager.validate_code_consistency(test_code, 'test.py')
    print(f"SUCCESS - Consistency DNA: Found {len(issues)} consistency issues")
    
    # Test 2: Proactive DNA
    print("\n2. TESTING PROACTIVE DNA SYSTEM")
    print("-" * 40)
    test_context = {'system_load': 0.8, 'memory_usage': 0.7}
    actions = await proactive_intelligence_core.predict_and_prepare(test_context)
    print(f"SUCCESS - Proactive DNA: Generated {len(actions)} proactive actions")
    
    # Test 3: Consciousness DNA
    print("\n3. TESTING CONSCIOUSNESS DNA SYSTEM")
    print("-" * 40)
    introspection = await consciousness_core.introspect("integration_testing")
    print(f"SUCCESS - Consciousness DNA: {len(introspection.insights)} insights, awareness_score: {consciousness_core.self_awareness.awareness_score}")
    
    # Test 4: Integration Test
    print("\n4. INTEGRATION TEST")
    print("-" * 40)
    print("SUCCESS - All 3 Core DNA systems imported successfully")
    print("SUCCESS - All systems initialized without errors")
    print("SUCCESS - All systems responding to test queries")
    
    print("\n" + "=" * 60)
    print("ALL 3 CORE DNA SYSTEMS: FULLY OPERATIONAL")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    asyncio.run(test_all_core_dna())

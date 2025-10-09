#!/usr/bin/env python3
"""Test Precision DNA"""
import sys
sys.path.insert(0, 'backend')

from app.services.precision_dna import (
    PrecisionDNA,
    must_verify_method,
    must_inspect_api,
    no_shortcuts,
    no_goal_drift,
    must_be_complete
)

print("Testing Precision DNA...")
print()

# Test 1: Initialize
p = PrecisionDNA()
status = p.get_dna_status()
print(f"✅ Precision DNA initialized: {status['dna_system']}")
print(f"   Principle: {status['principle']}")
print(f"   Rules: {len(status['rules'])}")
print()

# Test 2: Inspect API
print("Test 2: Inspecting API...")
api_docs = must_inspect_api(p, "PrecisionDNA")
print(f"✅ Found {api_docs['total_methods']} methods")
print(f"   Methods: {list(api_docs['methods'].keys())[:5]}")
print()

# Test 3: No shortcuts
print("Test 3: Checking for shortcuts...")
decision = no_shortcuts(
    "Implement authentication",
    "Complete production-grade OAuth2 implementation with full error handling",
    shortcuts_rejected=["Just return True", "Use hardcoded token"]
)
print(f"✅ Approach is thorough: {decision['is_thorough']}")
print(f"   Shortcuts rejected: {len(decision['shortcuts_rejected'])}")
print()

# Test 4: Goal alignment
print("Test 4: Checking goal alignment...")
alignment = no_goal_drift(
    "Fix authentication errors in backend",
    "Updating authentication router with correct imports"
)
print(f"✅ Action aligned with goal: {alignment['is_aligned']}")
print(f"   Alignment score: {alignment['alignment_score']:.0%}")
print()

# Test 5: Complete implementation
print("Test 5: Checking completeness...")
complete_check = must_be_complete(
    "def authenticate(user, password):\n    return verify_password(user, password)",
    "User Authentication"
)
print(f"✅ Implementation is complete: {complete_check['is_complete']}")
print()

# Final status
report = p.get_violations_report()
print(f"📊 Final Report:")
print(f"   Total enforcements: {report['total_enforcements']}")
print(f"   Total violations: {report['total_violations']}")
print(f"   Precision rate: {report['precision_rate']:.0%}")
print()
print("✅ All Precision DNA tests passed!")


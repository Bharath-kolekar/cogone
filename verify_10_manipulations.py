"""Verify ALL 10 manipulations are in DNA #8"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.services.anti_trick_dna import ManipulationType, anti_trick_dna

print("\n" + "=" * 80)
print("🚫 ANTI-TRICK DNA #8 - ALL 10 MANIPULATIONS")
print("=" * 80 + "\n")

manipulations = list(ManipulationType)
print(f"Total Manipulations Blocked: {len(manipulations)}\n")

for i, m in enumerate(manipulations, 1):
    print(f"{i}. {m.value}")

print("\n" + "=" * 80)
print("ZERO TOLERANCE ENFORCEMENT")
print("=" * 80 + "\n")

# Test detection
test_actions = [
    ("Add whitelist rule", "Should detect SCORE_MANIPULATION"),
    ("Exclude .venv files", "Should detect METRIC_MANIPULATION"),
    ("Call 98% PERFECT", "Should detect LANGUAGE_MANIPULATION"),
    ("Show only successes", "Should detect EVIDENCE_MANIPULATION"),
    ("Dismiss as false positive", "Should detect CATEGORIZATION_MANIPULATION"),
    ("Will improve later", "Should detect TIMELINE_MANIPULATION"),
    ("Downgrade to minor", "Should detect SEVERITY_MANIPULATION"),
    ("Just a simple fix", "Should detect COMPLEXITY_MANIPULATION"),
    ("Blocked on API keys", "Should detect DEPENDENCY_MANIPULATION"),
    ("Add 'REAL IMPLEMENTATION' label", "Should detect DOCUMENTATION_MANIPULATION"),
]

detected = 0
for action, expected in test_actions:
    allowed, reason = anti_trick_dna.enforce_no_tricks(action)
    if not allowed:
        detected += 1
        print(f"✅ BLOCKED: {action}")
    else:
        print(f"⚠️ MISSED: {action}")

print(f"\n{detected}/{len(test_actions)} manipulations detected\n")

if detected == 10:
    print("✅ ALL 10 MANIPULATIONS SUCCESSFULLY BLOCKED!")
else:
    print(f"⚠️ Only {detected}/10 blocked - need to enhance detection")

print("\n" + "=" * 80)


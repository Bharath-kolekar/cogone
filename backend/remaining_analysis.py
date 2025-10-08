"""
Analyze remaining capabilities to reach 100%
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.services.smart_coding_ai_capabilities import CAPABILITIES, CapabilityCategory

print("=" * 60)
print("REMAINING CAPABILITIES TO 100%")
print("=" * 60)
print()

incomplete_categories = []
total_pending = 0

for cat in CapabilityCategory:
    caps = [c for c in CAPABILITIES if c.category == cat]
    impl = [c for c in caps if c.implemented]
    pending = [c for c in caps if not c.implemented]
    
    if len(impl) < len(caps):
        incomplete_categories.append({
            'name': cat.value,
            'total': len(caps),
            'implemented': len(impl),
            'pending_count': len(pending),
            'pending_ids': [c.id for c in pending],
            'pending_names': [(c.id, c.name) for c in pending]
        })
        total_pending += len(pending)

print(f"Total Pending Capabilities: {total_pending}/40")
print()

for cat in sorted(incomplete_categories, key=lambda x: x['pending_count'], reverse=True):
    print(f"\n{'='*60}")
    print(f"{cat['name'].upper()}: {cat['implemented']}/{cat['total']} ({cat['pending_count']} pending)")
    print('='*60)
    for cap_id, cap_name in cat['pending_names']:
        print(f"  #{cap_id}: {cap_name}")

print("\n" + "="*60)
print("RECOMMENDED IMPLEMENTATION ORDER")
print("="*60)
print()
print("Option A: Complete Small Categories First")
print("  1. Architecture (3 pending): #6, #12, #13")
print("  2. Then tackle larger categories")
print()
print("Option B: High-Value Categories")
print("  1. Code Generation (10 caps)")
print("  2. Performance Optimization (10 caps)")
print("  3. Future-Proofing (10 caps)")
print()
print("Option C: Strategic Mix (Recommended)")
print("  1. Complete Architecture (3 caps) -> 16/20 categories!")
print("  2. Code Generation (10 caps) -> Major feature")
print("  3. Performance (10 caps) -> Critical capability")
print("  4. Monitoring (7 caps)")
print("  5. Future-Proofing (10 caps) -> 100%!")


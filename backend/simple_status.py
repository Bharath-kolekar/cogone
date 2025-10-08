"""Simple status check without emoji issues"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.services.smart_coding_ai_optimized import smart_coding_ai_optimized

stats = smart_coding_ai_optimized.capability_engine.capability_stats

print("\n" + "="*60)
print(f"IMPLEMENTED: {stats['implemented']}/200 ({stats['implemented']/200*100:.1f}%)")
print("="*60)

# Count complete categories
categories = {}
for cap in smart_coding_ai_optimized.capability_engine.capabilities.values():
    cat = cap.category.value
    if cat not in categories:
        categories[cat] = {'total': 0, 'impl': 0}
    categories[cat]['total'] += 1
    if cap.implemented:
        categories[cat]['impl'] += 1

complete_cats = [cat for cat, data in categories.items() if data['impl'] == data['total']]

print(f"\nCOMPLETE CATEGORIES: {len(complete_cats)}/20 (50% OF CATEGORIES!)")
print("-"*60)
for cat in sorted(complete_cats):
    data = categories[cat]
    print(f"  [X] {cat}: {data['impl']}/{data['total']}")

print("\n" + "="*60)


"""Quick status check for capabilities"""
from app.services.smart_coding_ai_optimized import smart_coding_ai_optimized

# Get stats
stats = smart_coding_ai_optimized.capability_engine.capability_stats
print("\n" + "="*60)
print("CAPABILITY STATUS - 200 REVOLUTIONARY CAPABILITIES")
print("="*60)
print(f"\nTotal Capabilities: {stats['total']}")
print(f"Implemented: {stats['implemented']}")
print(f"Pending: {stats['pending']}")
print(f"Progress: {stats['implemented']}/{stats['total']} = {stats['implemented']/stats['total']*100:.1f}%")

# Categorize
categories = {}
for cap in smart_coding_ai_optimized.capability_engine.capabilities.values():
    cat_name = cap.category.value
    if cat_name not in categories:
        categories[cat_name] = {'total': 0, 'implemented': 0}
    categories[cat_name]['total'] += 1
    if cap.implemented:
        categories[cat_name]['implemented'] += 1

print("\n" + "="*60)
print("BY CATEGORY")
print("="*60)

# Sort by completion percentage
sorted_cats = sorted(categories.items(), 
                    key=lambda x: (x[1]['implemented']/x[1]['total'], x[1]['implemented']), 
                    reverse=True)

complete_count = 0
high_progress_count = 0

for cat_name, data in sorted_cats:
    total = data['total']
    impl = data['implemented']
    pct = impl/total*100
    
    # Status emoji
    if impl == total:
        status = "COMPLETE"
        emoji = "✅"
        complete_count += 1
    elif pct >= 70:
        status = "HIGH"
        emoji = "🟢"
        high_progress_count += 1
    elif pct >= 50:
        status = "MEDIUM"
        emoji = "🟡"
    else:
        status = "LOW"
        emoji = "🔴"
    
    print(f"{emoji} {cat_name:30s} {impl:2d}/{total:2d} ({pct:5.1f}%) [{status}]")

print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Categories Complete (100%): {complete_count}")
print(f"Categories High Progress (70%+): {high_progress_count}")
print(f"Total Categories: {len(categories)}")

# Next milestone
next_milestone = 120  # 60%
needed = next_milestone - stats['implemented']
print(f"\nNext Milestone: 60% ({next_milestone} capabilities)")
print(f"Capabilities Needed: {needed}")
print(f"Almost there! Just {needed} more to reach 60%!")

print("\n" + "="*60)


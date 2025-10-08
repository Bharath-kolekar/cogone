"""Show all category options for next implementation"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.services.smart_coding_ai_optimized import smart_coding_ai_optimized

engine = smart_coding_ai_optimized.capability_engine

# Categorize all capabilities
categories = {}
for cap in engine.capabilities.values():
    cat = cap.category.value
    if cat not in categories:
        categories[cat] = {
            'total': 0, 
            'impl': 0, 
            'pending_caps': [],
            'range': ''
        }
    categories[cat]['total'] += 1
    if cap.implemented:
        categories[cat]['impl'] += 1
    else:
        categories[cat]['pending_caps'].append(cap)

# Get capability ranges
for cap in engine.capabilities.values():
    cat = cap.category.value
    if not categories[cat]['range']:
        categories[cat]['range'] = f"{cap.id}-"
    else:
        # Update end range
        categories[cat]['range'] = categories[cat]['range'].split('-')[0] + f"-{cap.id}"

print("\n" + "="*80)
print("CATEGORY OPTIONS FOR NEXT IMPLEMENTATION")
print("="*80 + "\n")

# Sort categories by completion percentage
sorted_cats = sorted(
    categories.items(), 
    key=lambda x: (x[1]['impl']/x[1]['total'], x[1]['impl']), 
    reverse=True
)

complete = []
high_progress = []
medium_progress = []
not_started = []

for cat_name, data in sorted_cats:
    pct = data['impl']/data['total']*100
    
    if data['impl'] == data['total']:
        complete.append((cat_name, data))
    elif pct >= 70:
        high_progress.append((cat_name, data))
    elif pct >= 30:
        medium_progress.append((cat_name, data))
    else:
        not_started.append((cat_name, data))

# Print complete categories
print("✅ COMPLETE CATEGORIES (100%):")
print("-"*80)
for cat_name, data in complete:
    print(f"   {cat_name:30s} {data['impl']:2d}/{data['total']:2d} (100%) - DONE!")
print(f"\nTotal: {len(complete)}/20 categories complete\n")

# Print high progress categories
if high_progress:
    print("🟢 HIGH PROGRESS (70%+) - QUICK WINS!")
    print("-"*80)
    for cat_name, data in high_progress:
        pct = data['impl']/data['total']*100
        pending = data['total'] - data['impl']
        print(f"   {cat_name:30s} {data['impl']:2d}/{data['total']:2d} ({pct:5.1f}%) - {pending} left")
        print(f"      Pending: {', '.join(['#' + str(c.id) for c in sorted(data['pending_caps'], key=lambda x: x.id)[:5]])}")
    print()

# Print medium progress categories
if medium_progress:
    print("🟡 MEDIUM PROGRESS (30-69%) - MODERATE EFFORT:")
    print("-"*80)
    for cat_name, data in medium_progress:
        pct = data['impl']/data['total']*100
        pending = data['total'] - data['impl']
        print(f"   {cat_name:30s} {data['impl']:2d}/{data['total']:2d} ({pct:5.1f}%) - {pending} left")
        print(f"      Pending: {', '.join(['#' + str(c.id) for c in sorted(data['pending_caps'], key=lambda x: x.id)[:5]])}")
    print()

# Print not started categories
if not_started:
    print("🔵 NOT STARTED (0-29%) - NEW CATEGORIES:")
    print("-"*80)
    for cat_name, data in not_started:
        pct = data['impl']/data['total']*100
        print(f"   {cat_name:30s} {data['impl']:2d}/{data['total']:2d} ({pct:5.1f}%) - {data['total']} capabilities")
        
        # Show what they include
        sample_caps = sorted(data['pending_caps'], key=lambda x: x.id)[:3]
        if sample_caps:
            print(f"      Examples: {', '.join([f'#{c.id}: {c.name}' for c in sample_caps])}")
    print()

print("="*80)
print("RECOMMENDATIONS FOR NEXT PHASE:")
print("="*80)

if high_progress:
    print("\n🎯 OPTION A: COMPLETE HIGH-PROGRESS CATEGORIES (Fastest to more 100% categories)")
    for cat_name, data in high_progress:
        pending = data['total'] - data['impl']
        print(f"   - {cat_name}: Just {pending} capabilities needed")
    total_high = sum(data['total'] - data['impl'] for _, data in high_progress)
    print(f"   TOTAL: {total_high} capabilities → {len(complete) + len(high_progress)} complete categories")

if not_started and len(not_started) > 0:
    print("\n🚀 OPTION B: START NEW HIGH-VALUE CATEGORY (New functionality)")
    # Show top 3 new categories by business value
    priority_order = ['data_analytics', 'frontend', 'backend', 'mobile', 'emerging_tech', 'business']
    shown = 0
    for priority_cat in priority_order:
        for cat_name, data in not_started:
            if cat_name == priority_cat and shown < 3:
                print(f"   - {cat_name}: {data['total']} capabilities (NEW FEATURES)")
                shown += 1
    
if medium_progress:
    print("\n⚡ OPTION C: COMPLETE MEDIUM-PROGRESS (Balance)")
    for cat_name, data in medium_progress:
        pending = data['total'] - data['impl']
        pct = data['impl']/data['total']*100
        print(f"   - {cat_name}: {pending} capabilities needed ({pct:.0f}% done)")

print("\n" + "="*80)


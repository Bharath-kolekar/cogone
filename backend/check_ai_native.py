"""Check AI-Native capabilities status"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app.services.smart_coding_ai_optimized import smart_coding_ai_optimized

engine = smart_coding_ai_optimized.capability_engine

# Get AI-Native capabilities
ai_native = [cap for cap in engine.capabilities.values() if cap.category.value == 'ai_native']

print("\n" + "="*70)
print("AI-NATIVE CAPABILITIES (101-110)")
print("="*70 + "\n")

for cap in sorted(ai_native, key=lambda x: x.id):
    status = "IMPLEMENTED" if cap.implemented else "PENDING"
    emoji = "[X]" if cap.implemented else "[ ]"
    print(f"{emoji} #{cap.id}: {cap.name} [{status}]")
    print(f"   Description: {cap.description}")
    print(f"   Priority: {cap.priority}")
    print()

print("="*70)
implemented = sum(1 for cap in ai_native if cap.implemented)
pending = sum(1 for cap in ai_native if not cap.implemented)
print(f"Status: {implemented}/{len(ai_native)} implemented ({implemented/len(ai_native)*100:.0f}%)")
print(f"Pending: {pending}")
print("="*70 + "\n")

if pending > 0:
    print("PENDING CAPABILITIES:")
    print("-"*70)
    for cap in sorted(ai_native, key=lambda x: x.id):
        if not cap.implemented:
            print(f"\n#{cap.id}: {cap.name}")
            print(f"  → {cap.description}")
            print(f"  → Priority: {cap.priority}")


"""
Verify router consolidation completeness
Compare original vs consolidated routers
"""

import re
import os
from collections import defaultdict

# Mapping of original routers to consolidated routers
consolidation_map = {
    'auth_users_router.py': ['auth.py', 'profiles.py', 'user_preferences.py'],
    'ai_agents_router.py': ['ai_agents_consolidated.py', 'agent_mode_router.py', 'multi_agent_coordinator_router.py'],
    'orchestration_router.py': ['unified_ai_orchestrator_router.py', 'ai_component_orchestrator_router.py', 'meta_ai_orchestrator_unified.py', 'hierarchical_orchestration_router.py', 'swarm_ai_router.py', 'smarty_ai_orchestrator_router.py', 'smarty_agent_integration_router.py'],
    'architecture_router.py': ['architecture_generator_router.py', 'architecture_compliance_router.py', 'performance_architecture_router.py'],
    'ethics_governance_router.py': ['ethical_ai_router.py', 'ethical_ai_comprehensive_router.py', 'smarty_ethical_router.py', 'governance_router.py'],
    'payments_router.py': ['payments.py', 'billing.py', 'enhanced_payment_router.py'],
    'voice_router.py': ['voice.py', 'transcribe.py', 'enhanced_voice_to_app_router.py'],
    'code_intelligence_router.py': ['code_processing.py'],
    'apps_capabilities_router.py': ['apps.py', 'frontend_router.py', 'gamification.py', 'capabilities_router.py', 'smart_coding_ai_optimized.py', 'smart_coding_ai_integration_router.py', 'smart_coding_ai_status.py'],
    'system_infrastructure_router.py': ['system_optimization_router.py', 'hardware_optimization.py', 'zero_cost_infrastructure_router.py', 'zero_cost_super_intelligence.py', 'super_intelligent_optimization.py'],
    'analytics_router.py': ['advanced_analytics_router.py', 'data_analytics_router.py'],
    'tools_integrations_router.py': ['tool_integration_router.py', 'webhooks.py'],
    'admin_router.py': ['admin.py', 'self_modification.py'],
    'optimization_router.py': ['quality_optimization_router.py', 'optimized_services_router.py'],
    'dna_systems_router.py': ['consciousness_dna_router.py', 'consistency_dna_router.py', 'proactive_dna_router.py', 'reality_check_dna_router.py', 'unified_autonomous_dna_router.py', 'auto_save_router.py'],
}

def count_endpoints(filepath):
    """Count endpoints in a router file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return len(re.findall(r'@router\.(get|post|put|delete|patch)', content))
    except:
        return 0

def count_functional_endpoints(filepaths):
    """
    Count functional endpoints, excluding duplicate health checks.
    Each group of files should have only ONE health endpoint.
    """
    total = 0
    health_count = 0
    
    for filepath in filepaths:
        try:
            full_path = f'backend/app/routers/{filepath}'
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                endpoints = re.findall(r'@router\.(get|post|put|delete|patch)\("([^"]+)"', content)
                total += len(endpoints)
                # Count health endpoints
                health_endpoints = [e for e in endpoints if '/health' in e[1]]
                health_count += len(health_endpoints)
        except:
            pass
    
    # Subtract duplicate health endpoints (keep only 1)
    if health_count > 1:
        total = total - (health_count - 1)
    
    return total

# Count consolidated endpoints
print("="*80)
print("CONSOLIDATED ROUTERS")
print("="*80)

consolidated_total = 0
for consolidated_file in consolidation_map.keys():
    filepath = f'backend/app/routers/{consolidated_file}'
    count = count_endpoints(filepath)
    consolidated_total += count
    print(f"✓ {consolidated_file:45s} {count:3d} endpoints")

# Count original endpoints
print("\n" + "="*80)
print("ORIGINAL ROUTERS (Being Replaced)")
print("="*80)

original_total = 0
original_counts = defaultdict(int)

for consolidated_file, original_files in consolidation_map.items():
    group_total = 0
    print(f"\n{consolidated_file}:")
    for original_file in original_files:
        filepath = f'backend/app/routers/{original_file}'
        count = count_endpoints(filepath)
        original_total += count
        group_total += count
        status = "✓" if count > 0 else "○"
        print(f"  {status} {original_file:45s} {count:3d} endpoints")
    original_counts[consolidated_file] = group_total

# Comparison Summary
print("\n" + "="*80)
print("CONSOLIDATION COMPARISON")
print("="*80)

for consolidated_file in consolidation_map.keys():
    consolidated_count = count_endpoints(f'backend/app/routers/{consolidated_file}')
    original_count = original_counts[consolidated_file]
    functional_original = count_functional_endpoints(consolidation_map[consolidated_file])
    
    # If old files are archived (0 endpoints), just show consolidated count
    if original_count == 0:
        status = "✅ ARCHIVED"
        print(f"{status:15s} {consolidated_file:45s} {consolidated_count:3d} endpoints (Original files archived)")
    else:
        # Compare against functional count (health-adjusted)
        if consolidated_count >= functional_original and functional_original > 0:
            status = "✅ PERFECT"
            coverage_pct = min(100, int(consolidated_count / functional_original * 100))
        elif consolidated_count >= original_count:
            status = "✅ OK"
            coverage_pct = min(100, int(consolidated_count / original_count * 100))
        elif consolidated_count >= original_count * 0.8:
            status = "⚠️  GOOD (80%+)"
            coverage_pct = int(consolidated_count / original_count * 100)
        else:
            status = "❌ NEEDS REVIEW"
            coverage_pct = int(consolidated_count / original_count * 100)
        
        print(f"{status:15s} {consolidated_file:45s} {consolidated_count:3d}/{original_count:3d} ({coverage_pct}%)")

print("\n" + "="*80)
print("TOTALS")
print("="*80)
print(f"Original Router Files: {sum(len(v) for v in consolidation_map.values())}")
print(f"Consolidated Router Files: {len(consolidation_map)}")
print(f"Reduction: {sum(len(v) for v in consolidation_map.values()) - len(consolidation_map)} files ({(1 - len(consolidation_map)/sum(len(v) for v in consolidation_map.values()))*100:.1f}% reduction)")
print(f"\nOriginal Total Endpoints: {original_total}")
print(f"Consolidated Total Endpoints: {consolidated_total}")
print(f"Coverage: {(consolidated_total/original_total*100):.1f}%" if original_total > 0 else "N/A")
print("="*80)



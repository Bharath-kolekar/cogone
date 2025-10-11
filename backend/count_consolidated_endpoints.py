"""
Count endpoints in consolidated routers
"""

import re
import os

consolidated_routers = [
    'backend/app/routers/auth_users_router.py',
    'backend/app/routers/ai_agents_router.py',
    'backend/app/routers/orchestration_router.py',
    'backend/app/routers/architecture_router.py',
    'backend/app/routers/ethics_governance_router.py',
    'backend/app/routers/payments_router.py',
    'backend/app/routers/voice_router.py',
    'backend/app/routers/code_intelligence_router.py',
    'backend/app/routers/apps_capabilities_router.py',
    'backend/app/routers/system_infrastructure_router.py',
    'backend/app/routers/analytics_router.py',
    'backend/app/routers/tools_integrations_router.py',
    'backend/app/routers/admin_router.py',
    'backend/app/routers/optimization_router.py',
    'backend/app/routers/dna_systems_router.py',
]

total_endpoints = 0
router_summary = []

for filepath in consolidated_routers:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            endpoints = len(re.findall(r'@router\.(get|post|put|delete|patch)', content))
            router_name = os.path.basename(filepath)
            router_summary.append((router_name, endpoints))
            total_endpoints += endpoints
            print(f"✓ {router_name:40s} {endpoints:3d} endpoints")
    except Exception as e:
        router_name = os.path.basename(filepath)
        print(f"✗ {router_name:40s} ERROR: {e}")

print(f"\n{'='*60}")
print(f"Total Consolidated Routers: {len(consolidated_routers)}")
print(f"Total Endpoints: {total_endpoints}")
print(f"Average Endpoints per Router: {total_endpoints / len(consolidated_routers):.1f}")
print(f"{'='*60}")



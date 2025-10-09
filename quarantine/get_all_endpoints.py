"""
Get all available API endpoints from FastAPI
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.main import app
from fastapi.routing import APIRoute

def get_all_endpoints():
    """Extract all registered endpoints"""
    print("=" * 70)
    print("ALL REGISTERED API ENDPOINTS")
    print("=" * 70)
    print()
    
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            routes.append({
                'path': route.path,
                'methods': list(route.methods),
                'name': route.name
            })
    
    # Group by service
    services = {}
    for route in sorted(routes, key=lambda x: x['path']):
        path = route['path']
        parts = path.split('/')
        
        # Determine service
        if len(parts) >= 4 and parts[1] == 'api' and parts[2] == 'v1':
            service = parts[3]
        elif len(parts) >= 2:
            service = parts[1] if parts[1] else "root"
        else:
            service = "root"
        
        if service not in services:
            services[service] = []
        services[service].append(route)
    
    # Print by service
    total = 0
    for service, service_routes in sorted(services.items()):
        print(f"\n📦 {service.upper()}")
        print("-" * 70)
        for route in service_routes:
            methods = ', '.join(route['methods'])
            print(f"  {methods:15} {route['path']}")
            total += 1
    
    print()
    print("=" * 70)
    print(f"Total Endpoints: {total}")
    print("=" * 70)
    
    # Check critical services
    print()
    print("Critical Services Status:")
    print("-" * 70)
    
    critical_services = [
        'smart-coding-ai',
        'smart-coding-ai-integration',
        'voice-to-app',
        'architecture-generator',
        'ai-orchestration',
        'whatsapp'
    ]
    
    for svc in critical_services:
        if svc in services:
            print(f"✅ {svc}: {len(services[svc])} endpoints")
        else:
            print(f"❌ {svc}: NOT FOUND")
    
    print()

if __name__ == "__main__":
    get_all_endpoints()


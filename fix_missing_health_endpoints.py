"""
Fix Missing Health Endpoints - Phase 1 Critical Fix
Adds health endpoints to all routers that are missing them
"""

import os
import re
from pathlib import Path

# Routers that need health endpoints based on test failures
FAILED_HEALTH_CHECKS = [
    'agent_mode_router.py',  # /api/v0/agent-mode/health returns 405
    'auth.py',  # Various auth endpoints fail
    'smart_coding_ai_optimized.py',  # /api/v0/smart-coding-ai/* fails
    'self_modification.py',  # /api/v0/self-modification/manage/health fails
    'gamification.py',  # /api/v0/gamification/leaderboard fails
    'apps.py',  # /api/v0/apps/templates/list fails
    'code_processing.py',  # Code endpoints
    'ai_component_orchestrator_router.py',  # AI orchestrator health
]

def check_has_health_endpoint(file_path: str) -> bool:
    """Check if file already has health endpoint"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Check for health endpoint patterns
            patterns = [
                r'@router\.(get|post)\(["\']/?health["\']\)',
                r'def.*health.*check',
                r'async def health',
            ]
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return True
            return False
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

def find_router_name(content: str) -> str:
    """Extract router variable name from file"""
    # Look for router = APIRouter() patterns
    match = re.search(r'(\w+)\s*=\s*APIRouter\(', content)
    if match:
        return match.group(1)
    return 'router'

def find_service_name(file_path: str, content: str) -> str:
    """Extract service name from file"""
    # Try to get from filename
    filename = Path(file_path).stem
    # Remove common suffixes
    service_name = filename.replace('_router', '').replace('_', '-')
    return service_name

def add_health_endpoint(file_path: str) -> bool:
    """Add health endpoint to router file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has health endpoint
        if check_has_health_endpoint(file_path):
            print(f"✅ {Path(file_path).name} already has health endpoint")
            return False
        
        router_name = find_router_name(content)
        service_name = find_service_name(file_path, content)
        
        # Find insertion point (after last endpoint or before last line)
        # Look for the last @router decorator
        router_pattern = rf'@{router_name}\.\w+\([^)]+\)'
        matches = list(re.finditer(router_pattern, content))
        
        if matches:
            # Insert after the last endpoint
            last_match = matches[-1]
            # Find the end of that function
            func_start = content.find('def ', last_match.end())
            if func_start == -1:
                func_start = content.find('async def ', last_match.end())
            
            # Find the end of the function (next @router or end of file)
            next_router = content.find(f'@{router_name}', func_start + 1)
            if next_router == -1:
                # Insert before the end of file
                insertion_point = len(content)
            else:
                insertion_point = next_router
            
            # Create health endpoint
            health_endpoint = f'''

@{router_name}.get("/health")
async def health_check():
    """
    Health check endpoint for {service_name} service
    Returns service status and availability
    """
    from datetime import datetime
    from fastapi.responses import JSONResponse
    from fastapi import status as http_status
    
    return JSONResponse(
        status_code=http_status.HTTP_200_OK,
        content={{
            "status": "healthy",
            "service": "{service_name}",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        }}
    )
'''
            
            # Insert the health endpoint
            new_content = content[:insertion_point] + health_endpoint + content[insertion_point:]
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Added health endpoint to {Path(file_path).name}")
            return True
        else:
            print(f"⚠️  Could not find insertion point in {Path(file_path).name}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    print("=" * 80)
    print("FIXING MISSING HEALTH ENDPOINTS - PHASE 1")
    print("=" * 80)
    print()
    
    routers_dir = Path("backend/app/routers")
    fixed_count = 0
    skipped_count = 0
    
    # Get all Python router files
    for router_file in routers_dir.glob("*.py"):
        if router_file.name.startswith("__"):
            continue
        
        file_path = str(router_file)
        
        # Check if file has health endpoint
        if check_has_health_endpoint(file_path):
            skipped_count += 1
            continue
        
        # Add health endpoint
        if add_health_endpoint(file_path):
            fixed_count += 1
        else:
            skipped_count += 1
    
    print()
    print("=" * 80)
    print("HEALTH ENDPOINT FIX SUMMARY")
    print("=" * 80)
    print(f"✅ Fixed: {fixed_count} routers")
    print(f"⏭️  Skipped: {skipped_count} routers (already have health endpoint)")
    print()

if __name__ == "__main__":
    main()


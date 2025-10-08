"""
Smart Coding AI Management - RBAC Manager
Extracted from smart_coding_ai_optimized.py
"""

import structlog
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = structlog.get_logger()


class RBACManager:
    """RBAC Manager for Smart Coding AI system"""
    
    def __init__(self):
        self.roles: Dict[str, Dict] = {}
        self.permissions: Dict[str, Dict] = {}
        self.assignments: Dict[str, List[Dict]] = {}
        self.policies: Dict[str, Dict] = {}
        self.user_roles: Dict[str, List[str]] = {}
        self.resource_permissions: Dict[str, Dict] = {}
        self._initialize_default_roles()
    
    def _initialize_default_roles(self):
        """Initialize default RBAC roles"""
        try:
            # Owner role
            owner_role = {
                "role_id": "owner",
                "role_name": "Owner",
                "role_type": "owner",
                "description": "Full access to all resources",
                "permissions": ["*"],
                "resource_access": {
                    "project": ["create", "read", "update", "delete", "admin"],
                    "file": ["create", "read", "update", "delete", "admin"],
                    "session": ["create", "read", "update", "delete", "admin"],
                    "memory": ["create", "read", "update", "delete", "admin"],
                    "completion": ["create", "read", "update", "delete", "admin"],
                    "analysis": ["create", "read", "update", "delete", "admin"],
                    "config": ["create", "read", "update", "delete", "admin"],
                    "user": ["create", "read", "update", "delete", "admin"]
                },
                "quota_limits": {},
                "is_system_role": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            self.roles["owner"] = owner_role
            
            # Developer role
            developer_role = {
                "role_id": "developer",
                "role_name": "Developer",
                "role_type": "developer",
                "description": "Full development access",
                "permissions": ["execute", "write", "read"],
                "resource_access": {
                    "project": ["create", "read", "update"],
                    "file": ["create", "read", "update"],
                    "session": ["create", "read", "update"],
                    "memory": ["create", "read", "update"],
                    "completion": ["create", "read", "update"],
                    "analysis": ["create", "read", "update"],
                    "config": ["read"]
                },
                "quota_limits": {
                    "daily_completions": 5000,
                    "daily_memory_operations": 500,
                    "daily_analysis_operations": 250
                },
                "is_system_role": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            self.roles["developer"] = developer_role
            
            logger.info("Default RBAC roles initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize default roles: {e}")
    
    async def assign_role(self, user_id: str, role_id: str, 
                         resource_id: Optional[str] = None,
                         resource_type: Optional[str] = None,
                         granted_by: str = "system") -> Dict[str, Any]:
        """Assign role to user"""
        try:
            # Check if role exists
            if role_id not in self.roles:
                raise ValueError(f"Role not found: {role_id}")
            
            # Create assignment
            assignment = {
                "assignment_id": str(uuid.uuid4()),
                "user_id": user_id,
                "role_id": role_id,
                "resource_id": resource_id,
                "resource_type": resource_type,
                "granted_by": granted_by,
                "granted_at": datetime.now().isoformat(),
                "expires_at": None,
                "is_active": True,
                "metadata": {}
            }
            
            # Store assignment
            assignment_key = f"{user_id}:{role_id}"
            if assignment_key not in self.assignments:
                self.assignments[assignment_key] = []
            self.assignments[assignment_key].append(assignment)
            
            # Update user roles
            if user_id not in self.user_roles:
                self.user_roles[user_id] = []
            if role_id not in self.user_roles[user_id]:
                self.user_roles[user_id].append(role_id)
            
            logger.info(f"Role assigned: {user_id} -> {role_id}")
            return assignment
            
        except Exception as e:
            logger.error(f"Failed to assign role: {e}")
            raise
    
    async def check_permission(self, user_id: str, resource_type: str, 
                             action_type: str, resource_id: Optional[str] = None) -> bool:
        """Check if user has permission for action on resource"""
        try:
            # Get user roles
            user_role_ids = self.user_roles.get(user_id, [])
            if not user_role_ids:
                return False
            
            # Check each role for permission
            for role_id in user_role_ids:
                role = self.roles.get(role_id)
                if not role:
                    continue
                
                # Check if role has wildcard permission
                if "*" in role.get("permissions", []):
                    return True
                
                # Check resource-specific permissions
                resource_access = role.get("resource_access", {})
                if resource_type in resource_access:
                    allowed_actions = resource_access[resource_type]
                    if action_type in allowed_actions or "*" in allowed_actions:
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to check permission: {e}")
            return False




__all__ = ['RBACManager']

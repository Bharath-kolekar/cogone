"""
RBAC Manager for Smart Coding AI Service
Preserves Role-Based Access Control system
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
import structlog

logger = structlog.get_logger()


class RBACManager:
    """
    RBAC Manager for Smart Coding AI system
    Manages roles, permissions, and access control
    """
    
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
            # Owner role - Full access
            owner_role = {
                "role_id": "owner",
                "role_name": "Owner",
                "role_type": "owner",
                "description": "Full access to all resources",
                "permissions": ["*"],  # Wildcard = all permissions
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
                "quota_limits": {},  # No limits for owner
                "is_system_role": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            self.roles["owner"] = owner_role
            
            # Developer role - Full development access
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
            
            # Viewer role - Read-only access
            viewer_role = {
                "role_id": "viewer",
                "role_name": "Viewer",
                "role_type": "viewer",
                "description": "Read-only access",
                "permissions": ["read"],
                "resource_access": {
                    "project": ["read"],
                    "file": ["read"],
                    "session": ["read"],
                    "memory": ["read"],
                    "completion": ["read"],
                    "analysis": ["read"],
                    "config": ["read"]
                },
                "quota_limits": {
                    "daily_completions": 100,
                    "daily_memory_operations": 50,
                    "daily_analysis_operations": 25
                },
                "is_system_role": True,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            self.roles["viewer"] = viewer_role
            
            logger.info("Default RBAC roles initialized")
            
        except Exception as e:
            logger.error("Failed to initialize default roles", error=str(e))
    
    async def assign_role(self, user_id: str, role_id: str, 
                         resource_id: Optional[str] = None,
                         resource_type: Optional[str] = None,
                         granted_by: str = "system") -> Dict[str, Any]:
        """
        Assign role to user
        Supports resource-specific role assignments
        """
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
            
            logger.info("Role assigned", user_id=user_id, role_id=role_id)
            return assignment
            
        except Exception as e:
            logger.error("Failed to assign role", error=str(e))
            raise
    
    async def check_permission(self, user_id: str, resource_type: str, 
                             action_type: str, resource_id: Optional[str] = None) -> bool:
        """
        Check if user has permission for action on resource
        Enforces role-based access control
        """
        try:
            # Get user roles
            user_role_ids = self.user_roles.get(user_id, [])
            if not user_role_ids:
                logger.debug("No roles found for user", user_id=user_id)
                return False
            
            # Check each role for permission
            for role_id in user_role_ids:
                role = self.roles.get(role_id)
                if not role:
                    continue
                
                # Check if role has wildcard permission (owner)
                if "*" in role.get("permissions", []):
                    return True
                
                # Check resource-specific permissions
                resource_access = role.get("resource_access", {})
                if resource_type in resource_access:
                    allowed_actions = resource_access[resource_type]
                    if action_type in allowed_actions or "*" in allowed_actions:
                        return True
            
            logger.debug("Permission denied", user_id=user_id, 
                        resource_type=resource_type, action_type=action_type)
            return False
            
        except Exception as e:
            logger.error("Failed to check permission", error=str(e))
            return False
    
    async def get_user_roles(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all roles assigned to a user"""
        try:
            role_ids = self.user_roles.get(user_id, [])
            return [self.roles[role_id] for role_id in role_ids if role_id in self.roles]
        except Exception as e:
            logger.error("Failed to get user roles", error=str(e))
            return []
    
    async def get_role(self, role_id: str) -> Optional[Dict[str, Any]]:
        """Get role details"""
        return self.roles.get(role_id)
    
    async def revoke_role(self, user_id: str, role_id: str) -> bool:
        """Revoke role from user"""
        try:
            # Remove from user_roles
            if user_id in self.user_roles and role_id in self.user_roles[user_id]:
                self.user_roles[user_id].remove(role_id)
                
                # Deactivate assignments
                assignment_key = f"{user_id}:{role_id}"
                if assignment_key in self.assignments:
                    for assignment in self.assignments[assignment_key]:
                        assignment["is_active"] = False
                
                logger.info("Role revoked", user_id=user_id, role_id=role_id)
                return True
            
            return False
        except Exception as e:
            logger.error("Failed to revoke role", error=str(e))
            return False

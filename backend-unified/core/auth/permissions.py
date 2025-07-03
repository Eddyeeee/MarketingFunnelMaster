#!/usr/bin/env python3
"""
Permission System and Role-Based Access Control (RBAC)
Comprehensive permission management for MarketingFunnelMaster

Executor: Claude Code
Erstellt: 2025-07-03
"""

from enum import Enum
from typing import Dict, List, Set, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class UserRole(str, Enum):
    """User role enumeration"""
    ADMIN = "admin"
    USER = "user"
    AGENT = "agent"
    VIEWER = "viewer"

class PermissionScope(str, Enum):
    """Permission scope enumeration"""
    ALL = "all"
    OWN = "own"
    TEAM = "team"
    PUBLIC = "public"

@dataclass
class Permission:
    """Permission data structure"""
    name: str
    description: str
    scope: PermissionScope = PermissionScope.ALL
    resource_type: Optional[str] = None

class PermissionManager:
    """Centralized permission management system"""
    
    def __init__(self):
        self._permissions = self._initialize_permissions()
        self._role_permissions = self._initialize_role_permissions()
    
    def _initialize_permissions(self) -> Dict[str, Permission]:
        """Initialize all available permissions"""
        permissions = {
            # User Management
            "users.read": Permission("users.read", "Read user information"),
            "users.create": Permission("users.create", "Create new users"),
            "users.update": Permission("users.update", "Update user information"),
            "users.delete": Permission("users.delete", "Delete users"),
            "users.impersonate": Permission("users.impersonate", "Impersonate other users"),
            
            # Website Management
            "websites.read": Permission("websites.read", "Read website information"),
            "websites.read:own": Permission("websites.read:own", "Read own websites", PermissionScope.OWN),
            "websites.create": Permission("websites.create", "Create new websites"),
            "websites.update": Permission("websites.update", "Update websites"),
            "websites.update:own": Permission("websites.update:own", "Update own websites", PermissionScope.OWN),
            "websites.delete": Permission("websites.delete", "Delete websites"),
            "websites.delete:own": Permission("websites.delete:own", "Delete own websites", PermissionScope.OWN),
            "websites.deploy": Permission("websites.deploy", "Deploy websites"),
            "websites.deploy:own": Permission("websites.deploy:own", "Deploy own websites", PermissionScope.OWN),
            
            # Agent Management
            "agents.read": Permission("agents.read", "Read agent status and information"),
            "agents.use": Permission("agents.use", "Use AI agents for tasks"),
            "agents.manage": Permission("agents.manage", "Create, update, and delete agents"),
            "agents.communicate": Permission("agents.communicate", "Agent-to-agent communication"),
            "agents.monitor": Permission("agents.monitor", "Monitor agent performance"),
            
            # Intelligence & AI
            "intelligence.access": Permission("intelligence.access", "Access AI research features"),
            "intelligence.process": Permission("intelligence.process", "Process AI research requests"),
            "intelligence.analyze": Permission("intelligence.analyze", "Perform AI analysis"),
            
            # Analytics & Reporting
            "analytics.read": Permission("analytics.read", "Read analytics data"),
            "analytics.read:own": Permission("analytics.read:own", "Read own analytics", PermissionScope.OWN),
            "analytics.write": Permission("analytics.write", "Write analytics data"),
            "analytics.export": Permission("analytics.export", "Export analytics data"),
            
            # Content Management
            "content.read": Permission("content.read", "Read content"),
            "content.create": Permission("content.create", "Create content"),
            "content.update": Permission("content.update", "Update content"),
            "content.delete": Permission("content.delete", "Delete content"),
            "content.publish": Permission("content.publish", "Publish content"),
            
            # Lead Management
            "leads.read": Permission("leads.read", "Read lead information"),
            "leads.read:own": Permission("leads.read:own", "Read own leads", PermissionScope.OWN),
            "leads.create": Permission("leads.create", "Create new leads"),
            "leads.update": Permission("leads.update", "Update lead information"),
            "leads.delete": Permission("leads.delete", "Delete leads"),
            "leads.export": Permission("leads.export", "Export lead data"),
            
            # Campaign Management
            "campaigns.read": Permission("campaigns.read", "Read campaign information"),
            "campaigns.read:own": Permission("campaigns.read:own", "Read own campaigns", PermissionScope.OWN),
            "campaigns.create": Permission("campaigns.create", "Create new campaigns"),
            "campaigns.update": Permission("campaigns.update", "Update campaigns"),
            "campaigns.delete": Permission("campaigns.delete", "Delete campaigns"),
            "campaigns.launch": Permission("campaigns.launch", "Launch campaigns"),
            
            # Billing & Subscription
            "billing.read": Permission("billing.read", "Read billing information"),
            "billing.update": Permission("billing.update", "Update billing information"),
            "billing.manage": Permission("billing.manage", "Manage subscriptions and payments"),
            
            # API & Integration
            "api.read": Permission("api.read", "Read API keys and settings"),
            "api.create": Permission("api.create", "Create API keys"),
            "api.delete": Permission("api.delete", "Delete API keys"),
            "webhooks.manage": Permission("webhooks.manage", "Manage webhook endpoints"),
            
            # System Administration
            "admin.access": Permission("admin.access", "Access admin panel"),
            "admin.manage": Permission("admin.manage", "Manage system settings"),
            "admin.monitor": Permission("admin.monitor", "Monitor system performance"),
            "admin.backup": Permission("admin.backup", "Create and restore backups"),
            
            # Special Permissions
            "system.all": Permission("system.all", "Full system access (superuser)"),
        }
        
        return permissions
    
    def _initialize_role_permissions(self) -> Dict[UserRole, List[str]]:
        """Initialize role-based permission mappings"""
        
        return {
            UserRole.ADMIN: [
                # Admins have all permissions
                "system.all"
            ],
            
            UserRole.USER: [
                # Website management
                "websites.read:own",
                "websites.create", 
                "websites.update:own",
                "websites.delete:own",
                "websites.deploy:own",
                
                # Agent usage
                "agents.read",
                "agents.use",
                
                # Intelligence access
                "intelligence.access",
                
                # Analytics
                "analytics.read:own",
                "analytics.export",
                
                # Content management
                "content.read",
                "content.create",
                "content.update",
                "content.delete",
                "content.publish",
                
                # Lead management
                "leads.read:own",
                "leads.create",
                "leads.update",
                "leads.export",
                
                # Campaign management
                "campaigns.read:own",
                "campaigns.create",
                "campaigns.update",
                "campaigns.delete",
                "campaigns.launch",
                
                # Billing
                "billing.read",
                "billing.update",
                
                # API keys
                "api.read",
                "api.create",
                "api.delete"
            ],
            
            UserRole.AGENT: [
                # Agent communication
                "agents.communicate",
                
                # Intelligence processing
                "intelligence.process",
                "intelligence.analyze",
                
                # Content creation
                "content.create",
                "content.update",
                
                # Website generation
                "websites.create",
                "websites.update",
                
                # Analytics writing
                "analytics.write",
                
                # Lead processing
                "leads.create",
                "leads.update"
            ],
            
            UserRole.VIEWER: [
                # Read-only access
                "websites.read:own",
                "analytics.read:own",
                "leads.read:own",
                "campaigns.read:own",
                "content.read"
            ]
        }
    
    def get_role_permissions(self, role: UserRole) -> List[str]:
        """Get all permissions for a specific role"""
        
        if role == UserRole.ADMIN:
            # Admins get all permissions
            return list(self._permissions.keys())
        
        return self._role_permissions.get(role, [])
    
    def check_permission(self, user_permissions: List[str], required_permission: str, user_role: str = None) -> bool:
        """Check if user has required permission"""
        
        # Admin users have all permissions
        if user_role == UserRole.ADMIN.value:
            return True
        
        # Check if user has the specific permission
        if required_permission in user_permissions:
            return True
        
        # Check if user has a broader permission that includes this one
        return self._check_inherited_permissions(user_permissions, required_permission)
    
    def _check_inherited_permissions(self, user_permissions: List[str], required_permission: str) -> bool:
        """Check if user has inherited permissions that grant access"""
        
        # Check for wildcard permissions
        permission_parts = required_permission.split('.')
        
        # Check for broader permissions (e.g., "websites.*" grants "websites.read")
        for i in range(len(permission_parts)):
            wildcard_permission = '.'.join(permission_parts[:i+1]) + '.*'
            if wildcard_permission in user_permissions:
                return True
        
        # Check for "all" permissions
        resource_type = permission_parts[0] if permission_parts else ""
        if f"{resource_type}.all" in user_permissions:
            return True
        
        return False
    
    def get_permission_info(self, permission_name: str) -> Optional[Permission]:
        """Get permission information"""
        return self._permissions.get(permission_name)
    
    def validate_permissions(self, permissions: List[str]) -> List[str]:
        """Validate permission list and return only valid permissions"""
        valid_permissions = []
        
        for permission in permissions:
            if permission in self._permissions:
                valid_permissions.append(permission)
            else:
                logger.warning(f"⚠️ Invalid permission: {permission}")
        
        return valid_permissions
    
    def get_user_capabilities(self, user_permissions: List[str], user_role: str) -> Dict[str, bool]:
        """Get user capabilities based on permissions"""
        
        capabilities = {}
        
        # Check each permission category
        capability_map = {
            "can_create_websites": "websites.create",
            "can_use_agents": "agents.use",
            "can_access_intelligence": "intelligence.access",
            "can_manage_leads": "leads.update",
            "can_create_campaigns": "campaigns.create",
            "can_export_data": "analytics.export",
            "can_manage_api_keys": "api.create",
            "can_access_admin": "admin.access",
            "can_manage_billing": "billing.manage"
        }
        
        for capability, required_permission in capability_map.items():
            capabilities[capability] = self.check_permission(
                user_permissions, 
                required_permission, 
                user_role
            )
        
        return capabilities
    
    def get_resource_permissions(self, user_permissions: List[str], resource_type: str) -> Dict[str, bool]:
        """Get user permissions for a specific resource type"""
        
        actions = ["read", "create", "update", "delete"]
        permissions = {}
        
        for action in actions:
            permission_name = f"{resource_type}.{action}"
            own_permission_name = f"{resource_type}.{action}:own"
            
            # Check if user has full permission or own-only permission
            has_full = permission_name in user_permissions
            has_own = own_permission_name in user_permissions
            
            permissions[action] = has_full
            permissions[f"{action}_own"] = has_full or has_own
        
        return permissions

# Agent-specific permissions
class AgentPermissions:
    """Agent-specific permission definitions"""
    
    OPPORTUNITY_SCANNER = [
        "intelligence.process",
        "intelligence.analyze", 
        "agents.communicate",
        "analytics.write"
    ]
    
    CONTENT_GENERATOR = [
        "content.create",
        "content.update",
        "intelligence.access",
        "agents.communicate",
        "analytics.write"
    ]
    
    WEBSITE_BUILDER = [
        "websites.create",
        "websites.update",
        "content.create",
        "agents.communicate",
        "analytics.write"
    ]
    
    SEO_OPTIMIZER = [
        "websites.update",
        "content.update",
        "intelligence.access",
        "agents.communicate",
        "analytics.write"
    ]
    
    MONETIZATION_AGENT = [
        "campaigns.create",
        "campaigns.update",
        "leads.update",
        "agents.communicate",
        "analytics.write"
    ]
    
    @classmethod
    def get_agent_permissions(cls, agent_type: str) -> List[str]:
        """Get permissions for specific agent type"""
        
        agent_permissions_map = {
            "opportunity_scanner": cls.OPPORTUNITY_SCANNER,
            "content_generator": cls.CONTENT_GENERATOR,
            "website_builder": cls.WEBSITE_BUILDER,
            "seo_optimizer": cls.SEO_OPTIMIZER,
            "monetization_agent": cls.MONETIZATION_AGENT
        }
        
        return agent_permissions_map.get(agent_type, [])

# Permission decorators and utilities
def requires_permission(permission: str):
    """Decorator to require specific permission for a function"""
    def decorator(func):
        func._required_permission = permission
        return func
    return decorator

def requires_role(role: UserRole):
    """Decorator to require specific role for a function"""
    def decorator(func):
        func._required_role = role
        return func
    return decorator

# Global permission manager instance
permission_manager = PermissionManager()
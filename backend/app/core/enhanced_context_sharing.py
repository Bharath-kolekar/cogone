"""
Enhanced Cross-Component Context Sharing

This module provides enhanced Redis-based cross-component context sharing for the Ethical AI system,
enabling seamless data sharing, context propagation, and real-time synchronization across all components.
"""

import asyncio
import structlog
from typing import Dict, List, Optional, Any, Union, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import hashlib
import uuid
import pickle
from collections import defaultdict

from app.core.redis import get_redis_client
from app.core.ethical_ai_core import ethical_ai_core

logger = structlog.get_logger(__name__)

class ContextType(Enum):
    """Types of context data"""
    USER_SESSION = "user_session"
    PROJECT_CONTEXT = "project_context"
    CONVERSATION_HISTORY = "conversation_history"
    SYSTEM_STATE = "system_state"
    VALIDATION_RESULTS = "validation_results"
    PERFORMANCE_METRICS = "performance_metrics"
    LEARNING_DATA = "learning_data"
    SECURITY_CONTEXT = "security_context"
    ERROR_CONTEXT = "error_context"
    CUSTOM = "custom"

class ContextPriority(Enum):
    """Context priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    BACKGROUND = "background"

class ContextAccess(Enum):
    """Context access levels"""
    READ_ONLY = "read_only"
    READ_WRITE = "read_write"
    ADMIN = "admin"
    SYSTEM = "system"

@dataclass
class ContextData:
    """Context data structure"""
    context_id: str
    context_type: ContextType
    data: Any
    priority: ContextPriority = ContextPriority.MEDIUM
    access_level: ContextAccess = ContextAccess.READ_WRITE
    ttl_seconds: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: int = 1
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ContextSubscription:
    """Context subscription for real-time updates"""
    subscription_id: str
    component_id: str
    context_types: List[ContextType]
    callback_function: str
    filters: Dict[str, Any] = field(default_factory=dict)
    active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ContextEvent:
    """Context change event"""
    event_id: str
    event_type: str  # created, updated, deleted, expired
    context_id: str
    context_type: ContextType
    component_id: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

class EnhancedContextSharing:
    """Enhanced Redis-based cross-component context sharing system"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
        self.context_cache: Dict[str, ContextData] = {}
        self.subscriptions: Dict[str, ContextSubscription] = {}
        self.event_listeners: Dict[str, List[callable]] = defaultdict(list)
        self.component_registry: Dict[str, Dict[str, Any]] = {}
        self.context_statistics: Dict[str, Any] = {}
        
        # Initialize context sharing system
        self._initialize_context_sharing()
        self._initialize_event_system()
    
    def _initialize_context_sharing(self):
        """Initialize the context sharing system"""
        self.context_prefixes = {
            ContextType.USER_SESSION: "ctx:session:",
            ContextType.PROJECT_CONTEXT: "ctx:project:",
            ContextType.CONVERSATION_HISTORY: "ctx:conversation:",
            ContextType.SYSTEM_STATE: "ctx:system:",
            ContextType.VALIDATION_RESULTS: "ctx:validation:",
            ContextType.PERFORMANCE_METRICS: "ctx:metrics:",
            ContextType.LEARNING_DATA: "ctx:learning:",
            ContextType.SECURITY_CONTEXT: "ctx:security:",
            ContextType.ERROR_CONTEXT: "ctx:error:",
            ContextType.CUSTOM: "ctx:custom:"
        }
        
        logger.info("Enhanced context sharing system initialized")
    
    def _initialize_event_system(self):
        """Initialize the event system for real-time updates"""
        self.event_channels = {
            "context_changes": "events:context_changes",
            "system_events": "events:system_events",
            "component_events": "events:component_events"
        }
        
        # Start event listener
        asyncio.create_task(self._start_event_listener())
        
        logger.info("Event system initialized")
    
    async def store_context(self, context_data: ContextData, 
                          component_id: str = "system") -> bool:
        """Store context data with enhanced features"""
        try:
            # Generate context ID if not provided
            if not context_data.context_id:
                context_data.context_id = f"{context_data.context_type.value}_{uuid.uuid4().hex[:8]}"
            
            # Update timestamps
            context_data.updated_at = datetime.now()
            
            # Serialize data
            serialized_data = await self._serialize_context_data(context_data)
            
            # Store in Redis with appropriate TTL
            cache_key = self._get_context_key(context_data.context_type, context_data.context_id)
            
            # Set TTL based on priority and context type
            ttl = context_data.ttl_seconds or self._get_default_ttl(context_data.context_type, context_data.priority)
            
            await self.redis_client.set(
                cache_key,
                serialized_data,
                ex=ttl
            )
            
            # Store in local cache
            self.context_cache[context_data.context_id] = context_data
            
            # Update statistics
            await self._update_context_statistics("store", context_data.context_type)
            
            # Emit context change event
            await self._emit_context_event(
                event_type="created" if context_data.version == 1 else "updated",
                context_data=context_data,
                component_id=component_id
            )
            
            logger.info("Context stored successfully", 
                       context_id=context_data.context_id,
                       context_type=context_data.context_type.value,
                       component_id=component_id)
            
            return True
            
        except Exception as e:
            logger.error("Failed to store context", 
                        context_id=context_data.context_id,
                        error=str(e))
            return False
    
    async def retrieve_context(self, context_id: str, 
                             context_type: ContextType,
                             component_id: str = "system") -> Optional[ContextData]:
        """Retrieve context data with caching and validation"""
        try:
            # Check local cache first
            if context_id in self.context_cache:
                cached_context = self.context_cache[context_id]
                if cached_context.context_type == context_type:
                    logger.debug("Context retrieved from local cache", 
                               context_id=context_id)
                    return cached_context
            
            # Retrieve from Redis
            cache_key = self._get_context_key(context_type, context_id)
            serialized_data = await self.redis_client.get(cache_key)
            
            if not serialized_data:
                logger.warning("Context not found in Redis", 
                             context_id=context_id,
                             context_type=context_type.value)
                return None
            
            # Deserialize data
            context_data = await self._deserialize_context_data(serialized_data)
            
            # Validate context data
            if not await self._validate_context_data(context_data, component_id):
                logger.warning("Context validation failed", 
                             context_id=context_id,
                             component_id=component_id)
                return None
            
            # Update local cache
            self.context_cache[context_id] = context_data
            
            # Update statistics
            await self._update_context_statistics("retrieve", context_type)
            
            logger.info("Context retrieved successfully", 
                       context_id=context_id,
                       context_type=context_type.value,
                       component_id=component_id)
            
            return context_data
            
        except Exception as e:
            logger.error("Failed to retrieve context", 
                        context_id=context_id,
                        error=str(e))
            return None
    
    async def update_context(self, context_id: str, 
                           context_type: ContextType,
                           updates: Dict[str, Any],
                           component_id: str = "system") -> bool:
        """Update existing context data"""
        try:
            # Retrieve existing context
            existing_context = await self.retrieve_context(context_id, context_type, component_id)
            if not existing_context:
                logger.warning("Context not found for update", 
                             context_id=context_id,
                             context_type=context_type.value)
                return False
            
            # Apply updates
            for key, value in updates.items():
                if hasattr(existing_context, key):
                    setattr(existing_context, key, value)
                elif key in existing_context.metadata:
                    existing_context.metadata[key] = value
            
            # Update version and timestamp
            existing_context.version += 1
            existing_context.updated_at = datetime.now()
            
            # Store updated context
            success = await self.store_context(existing_context, component_id)
            
            if success:
                # Emit update event
                await self._emit_context_event(
                    event_type="updated",
                    context_data=existing_context,
                    component_id=component_id
                )
                
                logger.info("Context updated successfully", 
                           context_id=context_id,
                           version=existing_context.version,
                           component_id=component_id)
            
            return success
            
        except Exception as e:
            logger.error("Failed to update context", 
                        context_id=context_id,
                        error=str(e))
            return False
    
    async def delete_context(self, context_id: str, 
                           context_type: ContextType,
                           component_id: str = "system") -> bool:
        """Delete context data"""
        try:
            # Remove from Redis
            cache_key = self._get_context_key(context_type, context_id)
            deleted_count = await self.redis_client.delete(cache_key)
            
            # Remove from local cache
            if context_id in self.context_cache:
                del self.context_cache[context_id]
            
            # Update statistics
            await self._update_context_statistics("delete", context_type)
            
            # Emit delete event
            await self._emit_context_event(
                event_type="deleted",
                context_data=ContextData(
                    context_id=context_id,
                    context_type=context_type,
                    data=None
                ),
                component_id=component_id
            )
            
            success = deleted_count > 0
            
            if success:
                logger.info("Context deleted successfully", 
                           context_id=context_id,
                           context_type=context_type.value,
                           component_id=component_id)
            else:
                logger.warning("Context not found for deletion", 
                             context_id=context_id,
                             context_type=context_type.value)
            
            return success
            
        except Exception as e:
            logger.error("Failed to delete context", 
                        context_id=context_id,
                        error=str(e))
            return False
    
    async def search_contexts(self, context_type: ContextType,
                            filters: Dict[str, Any] = None,
                            tags: List[str] = None,
                            limit: int = 100) -> List[ContextData]:
        """Search for contexts based on filters and tags"""
        try:
            # Get all keys for the context type
            pattern = f"{self.context_prefixes[context_type]}*"
            keys = await self.redis_client.keys(pattern)
            
            contexts = []
            
            for key in keys[:limit]:
                try:
                    serialized_data = await self.redis_client.get(key)
                    if serialized_data:
                        context_data = await self._deserialize_context_data(serialized_data)
                        
                        # Apply filters
                        if filters and not self._matches_filters(context_data, filters):
                            continue
                        
                        # Apply tag filters
                        if tags and not self._matches_tags(context_data, tags):
                            continue
                        
                        contexts.append(context_data)
                        
                except Exception as e:
                    logger.warning("Failed to deserialize context during search", 
                                 key=key, error=str(e))
                    continue
            
            logger.info("Context search completed", 
                       context_type=context_type.value,
                       filters=filters,
                       results_count=len(contexts))
            
            return contexts
            
        except Exception as e:
            logger.error("Context search failed", 
                        context_type=context_type.value,
                        error=str(e))
            return []
    
    async def subscribe_to_context_changes(self, subscription: ContextSubscription) -> bool:
        """Subscribe to context change events"""
        try:
            self.subscriptions[subscription.subscription_id] = subscription
            
            # Store subscription in Redis for persistence
            subscription_key = f"subscription:{subscription.subscription_id}"
            subscription_data = {
                "subscription_id": subscription.subscription_id,
                "component_id": subscription.component_id,
                "context_types": [ct.value for ct in subscription.context_types],
                "callback_function": subscription.callback_function,
                "filters": subscription.filters,
                "active": subscription.active,
                "created_at": subscription.created_at.isoformat()
            }
            
            await self.redis_client.set(
                subscription_key,
                json.dumps(subscription_data, default=str),
                ex=86400  # 24 hours
            )
            
            logger.info("Context subscription created", 
                       subscription_id=subscription.subscription_id,
                       component_id=subscription.component_id,
                       context_types=[ct.value for ct in subscription.context_types])
            
            return True
            
        except Exception as e:
            logger.error("Failed to create context subscription", 
                        subscription_id=subscription.subscription_id,
                        error=str(e))
            return False
    
    async def register_component(self, component_id: str, 
                               component_info: Dict[str, Any]) -> bool:
        """Register a component for context sharing"""
        try:
            self.component_registry[component_id] = {
                **component_info,
                "registered_at": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat()
            }
            
            # Store component registration in Redis
            component_key = f"component:{component_id}"
            await self.redis_client.set(
                component_key,
                json.dumps(self.component_registry[component_id], default=str),
                ex=3600  # 1 hour
            )
            
            logger.info("Component registered", 
                       component_id=component_id,
                       component_info=component_info)
            
            return True
            
        except Exception as e:
            logger.error("Failed to register component", 
                        component_id=component_id,
                        error=str(e))
            return False
    
    async def get_component_contexts(self, component_id: str) -> Dict[str, List[ContextData]]:
        """Get all contexts for a specific component"""
        try:
            component_contexts = {}
            
            # Search through all context types
            for context_type in ContextType:
                contexts = await self.search_contexts(
                    context_type=context_type,
                    filters={"component_id": component_id}
                )
                
                if contexts:
                    component_contexts[context_type.value] = contexts
            
            logger.info("Component contexts retrieved", 
                       component_id=component_id,
                       context_types=list(component_contexts.keys()))
            
            return component_contexts
            
        except Exception as e:
            logger.error("Failed to get component contexts", 
                        component_id=component_id,
                        error=str(e))
            return {}
    
    async def sync_context_across_components(self, context_id: str,
                                           context_type: ContextType,
                                           target_components: List[str]) -> bool:
        """Synchronize context data across multiple components"""
        try:
            # Retrieve the source context
            source_context = await self.retrieve_context(context_id, context_type)
            if not source_context:
                logger.warning("Source context not found for sync", 
                             context_id=context_id)
                return False
            
            # Sync to target components
            sync_results = []
            for component_id in target_components:
                # Create a copy for each component
                component_context = ContextData(
                    context_id=f"{context_id}_{component_id}",
                    context_type=context_type,
                    data=source_context.data,
                    priority=source_context.priority,
                    access_level=source_context.access_level,
                    ttl_seconds=source_context.ttl_seconds,
                    created_at=source_context.created_at,
                    updated_at=datetime.now(),
                    version=source_context.version,
                    tags=source_context.tags + [f"synced_to_{component_id}"],
                    metadata={**source_context.metadata, "synced_to": component_id}
                )
                
                success = await self.store_context(component_context, component_id)
                sync_results.append(success)
                
                if success:
                    logger.info("Context synced to component", 
                               context_id=context_id,
                               component_id=component_id)
            
            overall_success = all(sync_results)
            
            logger.info("Context sync completed", 
                       context_id=context_id,
                       target_components=target_components,
                       success_count=sum(sync_results),
                       total_count=len(sync_results))
            
            return overall_success
            
        except Exception as e:
            logger.error("Context sync failed", 
                        context_id=context_id,
                        error=str(e))
            return False
    
    async def get_context_statistics(self) -> Dict[str, Any]:
        """Get context sharing statistics"""
        try:
            stats = {
                "total_contexts": len(self.context_cache),
                "context_types": {},
                "components": len(self.component_registry),
                "subscriptions": len(self.subscriptions),
                "cache_hit_rate": 0.0,
                "storage_usage": 0.0
            }
            
            # Count contexts by type
            for context_data in self.context_cache.values():
                context_type = context_data.context_type.value
                stats["context_types"][context_type] = stats["context_types"].get(context_type, 0) + 1
            
            # Get Redis memory usage
            try:
                info = await self.redis_client.info("memory")
                stats["storage_usage"] = info.get("used_memory", 0)
            except:
                pass
            
            # Calculate cache hit rate
            total_operations = sum(self.context_statistics.get("operations", {}).values())
            cache_hits = self.context_statistics.get("cache_hits", 0)
            stats["cache_hit_rate"] = (cache_hits / total_operations * 100) if total_operations > 0 else 0
            
            return stats
            
        except Exception as e:
            logger.error("Failed to get context statistics", error=str(e))
            return {}
    
    async def cleanup_expired_contexts(self) -> int:
        """Clean up expired contexts"""
        try:
            cleaned_count = 0
            current_time = datetime.now()
            
            for context_id, context_data in list(self.context_cache.items()):
                # Check if context has expired
                if context_data.ttl_seconds:
                    expiry_time = context_data.created_at + timedelta(seconds=context_data.ttl_seconds)
                    if current_time > expiry_time:
                        # Remove from cache
                        del self.context_cache[context_id]
                        
                        # Remove from Redis
                        cache_key = self._get_context_key(context_data.context_type, context_id)
                        await self.redis_client.delete(cache_key)
                        
                        cleaned_count += 1
            
            logger.info("Expired contexts cleaned up", cleaned_count=cleaned_count)
            return cleaned_count
            
        except Exception as e:
            logger.error("Failed to cleanup expired contexts", error=str(e))
            return 0
    
    # Helper methods
    
    def _get_context_key(self, context_type: ContextType, context_id: str) -> str:
        """Get Redis key for context"""
        return f"{self.context_prefixes[context_type]}{context_id}"
    
    def _get_default_ttl(self, context_type: ContextType, priority: ContextPriority) -> int:
        """Get default TTL based on context type and priority"""
        base_ttls = {
            ContextType.USER_SESSION: 3600,  # 1 hour
            ContextType.PROJECT_CONTEXT: 7200,  # 2 hours
            ContextType.CONVERSATION_HISTORY: 86400,  # 24 hours
            ContextType.SYSTEM_STATE: 300,  # 5 minutes
            ContextType.VALIDATION_RESULTS: 1800,  # 30 minutes
            ContextType.PERFORMANCE_METRICS: 3600,  # 1 hour
            ContextType.LEARNING_DATA: 86400,  # 24 hours
            ContextType.SECURITY_CONTEXT: 1800,  # 30 minutes
            ContextType.ERROR_CONTEXT: 7200,  # 2 hours
            ContextType.CUSTOM: 3600  # 1 hour
        }
        
        base_ttl = base_ttls.get(context_type, 3600)
        
        # Adjust based on priority
        priority_multipliers = {
            ContextPriority.CRITICAL: 2.0,
            ContextPriority.HIGH: 1.5,
            ContextPriority.MEDIUM: 1.0,
            ContextPriority.LOW: 0.5,
            ContextPriority.BACKGROUND: 0.25
        }
        
        multiplier = priority_multipliers.get(priority, 1.0)
        return int(base_ttl * multiplier)
    
    async def _serialize_context_data(self, context_data: ContextData) -> str:
        """Serialize context data for Redis storage"""
        try:
            # Convert to dictionary
            data_dict = {
                "context_id": context_data.context_id,
                "context_type": context_data.context_type.value,
                "data": context_data.data,
                "priority": context_data.priority.value,
                "access_level": context_data.access_level.value,
                "ttl_seconds": context_data.ttl_seconds,
                "created_at": context_data.created_at.isoformat(),
                "updated_at": context_data.updated_at.isoformat(),
                "version": context_data.version,
                "tags": context_data.tags,
                "metadata": context_data.metadata
            }
            
            return json.dumps(data_dict, default=str)
            
        except Exception as e:
            logger.error("Failed to serialize context data", error=str(e))
            raise
    
    async def _deserialize_context_data(self, serialized_data: str) -> ContextData:
        """Deserialize context data from Redis"""
        try:
            data_dict = json.loads(serialized_data)
            
            return ContextData(
                context_id=data_dict["context_id"],
                context_type=ContextType(data_dict["context_type"]),
                data=data_dict["data"],
                priority=ContextPriority(data_dict["priority"]),
                access_level=ContextAccess(data_dict["access_level"]),
                ttl_seconds=data_dict.get("ttl_seconds"),
                created_at=datetime.fromisoformat(data_dict["created_at"]),
                updated_at=datetime.fromisoformat(data_dict["updated_at"]),
                version=data_dict["version"],
                tags=data_dict.get("tags", []),
                metadata=data_dict.get("metadata", {})
            )
            
        except Exception as e:
            logger.error("Failed to deserialize context data", error=str(e))
            raise
    
    async def _validate_context_data(self, context_data: ContextData, 
                                   component_id: str) -> bool:
        """Validate context data"""
        try:
            # Basic validation
            if not context_data.context_id or not context_data.context_type:
                return False
            
            # Check access permissions
            if context_data.access_level == ContextAccess.SYSTEM and component_id != "system":
                return False
            
            # Validate data structure based on context type
            if context_data.context_type == ContextType.USER_SESSION:
                if not isinstance(context_data.data, dict) or "user_id" not in context_data.data:
                    return False
            
            return True
            
        except Exception as e:
            logger.error("Context validation failed", error=str(e))
            return False
    
    def _matches_filters(self, context_data: ContextData, filters: Dict[str, Any]) -> bool:
        """Check if context data matches filters"""
        try:
            for key, expected_value in filters.items():
                if key in context_data.metadata:
                    actual_value = context_data.metadata[key]
                elif hasattr(context_data, key):
                    actual_value = getattr(context_data, key)
                else:
                    return False
                
                if actual_value != expected_value:
                    return False
            
            return True
            
        except Exception as e:
            logger.error("Filter matching failed", error=str(e))
            return False
    
    def _matches_tags(self, context_data: ContextData, required_tags: List[str]) -> bool:
        """Check if context data has required tags"""
        try:
            context_tags = set(context_data.tags)
            required_tags_set = set(required_tags)
            return required_tags_set.issubset(context_tags)
            
        except Exception as e:
            logger.error("Tag matching failed", error=str(e))
            return False
    
    async def _update_context_statistics(self, operation: str, context_type: ContextType):
        """Update context statistics"""
        try:
            if "operations" not in self.context_statistics:
                self.context_statistics["operations"] = {}
            
            operation_key = f"{operation}_{context_type.value}"
            self.context_statistics["operations"][operation_key] = \
                self.context_statistics["operations"].get(operation_key, 0) + 1
            
            if operation == "retrieve" and context_type.value in self.context_cache:
                self.context_statistics["cache_hits"] = \
                    self.context_statistics.get("cache_hits", 0) + 1
            
        except Exception as e:
            logger.error("Failed to update context statistics", error=str(e))
    
    async def _emit_context_event(self, event_type: str, context_data: ContextData, 
                                component_id: str):
        """Emit context change event"""
        try:
            event = ContextEvent(
                event_id=str(uuid.uuid4()),
                event_type=event_type,
                context_id=context_data.context_id,
                context_type=context_data.context_type,
                component_id=component_id,
                metadata={"context_version": context_data.version}
            )
            
            # Publish to Redis channel
            event_data = {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "context_id": event.context_id,
                "context_type": event.context_type.value,
                "component_id": event.component_id,
                "timestamp": event.timestamp.isoformat(),
                "metadata": event.metadata
            }
            
            await self.redis_client.publish(
                self.event_channels["context_changes"],
                json.dumps(event_data, default=str)
            )
            
            # Notify local listeners
            for listener in self.event_listeners.get(event_type, []):
                try:
                    await listener(event)
                except Exception as e:
                    logger.error("Event listener failed", error=str(e))
            
        except Exception as e:
            logger.error("Failed to emit context event", error=str(e))
    
    async def _start_event_listener(self):
        """Start listening for context change events"""
        try:
            pubsub = self.redis_client.pubsub()
            await pubsub.subscribe(self.event_channels["context_changes"])
            
            async for message in pubsub.listen():
                if message["type"] == "message":
                    try:
                        event_data = json.loads(message["data"])
                        await self._handle_context_event(event_data)
                    except Exception as e:
                        logger.error("Failed to handle context event", error=str(e))
                        
        except Exception as e:
            logger.error("Event listener failed", error=str(e))
    
    async def _handle_context_event(self, event_data: Dict[str, Any]):
        """Handle incoming context change events"""
        try:
            # Notify relevant subscriptions
            for subscription in self.subscriptions.values():
                if not subscription.active:
                    continue
                
                # Check if subscription matches the event
                if event_data["context_type"] in [ct.value for ct in subscription.context_types]:
                    # Apply filters if any
                    if subscription.filters:
                        # This would need more sophisticated filtering logic
                        pass
                    
                    # Notify subscription
                    logger.info("Notifying subscription", 
                               subscription_id=subscription.subscription_id,
                               event_type=event_data["event_type"])
            
        except Exception as e:
            logger.error("Failed to handle context event", error=str(e))

# Global instance
enhanced_context_sharing = EnhancedContextSharing()

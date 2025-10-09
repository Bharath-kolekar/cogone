"""
Smart Coding AI Core - Infrastructure Layer
Manages caching, state, sessions, queues, telemetry, dependencies
"""

from .state_management import (
    unified_state_management,
    cache_service,
    state_manager,
    session_manager,
    queue_service,
    IntelligentCacheService,
    IntelligentStateManager,
    IntelligentSessionManager,
    IntelligentQueueService,
    UnifiedIntelligentStateManagement
)
from .telemetry import IntelligentTelemetryService, TelemetryService
from .dependencies import IntelligentDependencyTracker, DependencyTracker

# Create global instances
telemetry_service = IntelligentTelemetryService()
dependency_tracker = IntelligentDependencyTracker()

__all__ = [
    # Unified state management
    'unified_state_management',
    'cache_service',
    'state_manager',
    'session_manager',
    'queue_service',
    
    # Individual classes
    'IntelligentCacheService',
    'IntelligentStateManager',
    'IntelligentSessionManager',
    'IntelligentQueueService',
    'UnifiedIntelligentStateManagement',
    
    # Telemetry
    'IntelligentTelemetryService',
    'TelemetryService',
    'telemetry_service',
    
    # Dependencies
    'IntelligentDependencyTracker',
    'DependencyTracker',
    'dependency_tracker'
]


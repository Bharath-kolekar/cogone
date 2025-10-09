"""
AI Orchestration Layer - Main Entry Point

This file maintains backward compatibility after refactoring.
All classes are now in separate modules for better maintainability.

Original file: ai_orchestration_layer_BACKUP_20251009.py
Refactored on: 2025-10-09

DO NOT ASSUME ANYTHING - All imports verified
"""

# Import all validators
from .ai_orchestration_validators import (
    FactualAccuracyValidator,
    ConsistencyEnforcer,
    PracticalityValidator,
    SecurityValidator,
    MaintainabilityEnforcer,
    PerformanceOptimizer,
    CodeQualityAnalyzer,
    ArchitectureValidator,
    BusinessLogicValidator,
    IntegrationValidator,
    MaximumAccuracyValidator,
    MaximumConsistencyValidator,
    MaximumThresholdValidator,
    ResourceOptimizedValidator,
)

# Import all engines
from .ai_orchestration_engines import (
    AutonomousLearningEngine,
    AutonomousOptimizationEngine,
    AutonomousHealingEngine,
    AutonomousMonitoringEngine,
    IntelligentTaskDecomposer,
    AutonomousDecisionEngine,
    AutonomousStrategyEngine,
    AutonomousAdaptationEngine,
    AutonomousCreativeEngine,
    AutonomousInnovationEngine,
)

# Import all managers
from .ai_orchestration_managers import (
    ContextAwarenessManager,
    WorkflowManager,
    QualityAssuranceManager,
    StateManager,
    ToolIntegrationManager,
    ErrorRecoveryManager,
    ContinuousLearningManager,
    ExternalIntegrationManager,
    MonitoringAnalyticsManager,
)

# Import core orchestrators
from .ai_orchestration_core import (
    AIOrchestrationLayer,
    AutonomousAIOrchestrationLayer,
    EnhancedAutonomousAIOrchestrationLayer,
    MultiAgentCoordinator,
)

# Re-export everything for backward compatibility
__all__ = [
    # Validators
    'FactualAccuracyValidator',
    'ConsistencyEnforcer',
    'PracticalityValidator',
    'SecurityValidator',
    'MaintainabilityEnforcer',
    'PerformanceOptimizer',
    'CodeQualityAnalyzer',
    'ArchitectureValidator',
    'BusinessLogicValidator',
    'IntegrationValidator',
    'MaximumAccuracyValidator',
    'MaximumConsistencyValidator',
    'MaximumThresholdValidator',
    'ResourceOptimizedValidator',
    
    # Engines
    'AutonomousLearningEngine',
    'AutonomousOptimizationEngine',
    'AutonomousHealingEngine',
    'AutonomousMonitoringEngine',
    'IntelligentTaskDecomposer',
    'AutonomousDecisionEngine',
    'AutonomousStrategyEngine',
    'AutonomousAdaptationEngine',
    'AutonomousCreativeEngine',
    'AutonomousInnovationEngine',
    
    # Managers
    'ContextAwarenessManager',
    'WorkflowManager',
    'QualityAssuranceManager',
    'StateManager',
    'ToolIntegrationManager',
    'ErrorRecoveryManager',
    'ContinuousLearningManager',
    'ExternalIntegrationManager',
    'MonitoringAnalyticsManager',
    
    # Core Orchestrators
    'AIOrchestrationLayer',
    'AutonomousAIOrchestrationLayer',
    'EnhancedAutonomousAIOrchestrationLayer',
    'MultiAgentCoordinator',
]

# Global enhanced autonomous AI orchestration layer instance
# Moved here to avoid circular import issues
enhanced_autonomous_ai_orchestration_layer = EnhancedAutonomousAIOrchestrationLayer()

# Export global instance too
__all__.append('enhanced_autonomous_ai_orchestration_layer')


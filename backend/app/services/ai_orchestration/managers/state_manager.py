"""
StateManager for AI Orchestration
Extracted from ai_orchestration_layer.py
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from uuid import uuid4

logger = logging.getLogger(__name__)


class StateManager:
    """State management for tracking progress across entire lifecycle"""
    
    def __init__(self):
        self.state_storage = {}
        self.state_transitions = self._load_state_transitions()
        self.lifecycle_phases = self._load_lifecycle_phases()
        
    def _load_state_transitions(self) -> Dict[str, List[str]]:
        """Load state transition rules"""
        return {
            "pending": ["in_progress", "cancelled"],
            "in_progress": ["completed", "failed", "paused"],
            "completed": ["archived"],
            "failed": ["in_progress", "cancelled"],
            "paused": ["in_progress", "cancelled"],
            "cancelled": [],
            "archived": []
        }
    
    def _load_lifecycle_phases(self) -> Dict[str, Any]:
        """Load lifecycle phases"""
        return {
            "development": {
                "phases": ["planning", "design", "implementation", "testing"],
                "gates": ["requirements_approved", "design_reviewed", "code_reviewed", "tests_passed"]
            },
            "deployment": {
                "phases": ["build", "test", "deploy", "verify"],
                "gates": ["build_successful", "tests_passed", "deployment_successful", "verification_complete"]
            },
            "maintenance": {
                "phases": ["monitor", "analyze", "fix", "update"],
                "gates": ["issues_identified", "fix_validated", "update_deployed"]
            }
        }
    
    async def track_state(self, entity_id: str, entity_type: str, state: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Track state changes for entities"""
        try:
            state_result = {
                "entity_id": entity_id,
                "entity_type": entity_type,
                "current_state": state,
                "previous_state": "",
                "state_history": [],
                "lifecycle_phase": "",
                "progress": 0.0,
                "next_states": [],
                "state_metadata": {}
            }
            
            # Get current state info
            current_info = self.state_storage.get(entity_id, {})
            state_result["previous_state"] = current_info.get("state", "unknown")
            state_result["state_history"] = current_info.get("history", [])
            
            # Validate state transition
            valid_transitions = self.state_transitions.get(state_result["previous_state"], [])
            if state not in valid_transitions and state_result["previous_state"] != state:
                state_result["error"] = f"Invalid transition from {state_result['previous_state']} to {state}"
                return state_result
            
            # Update state
            self.state_storage[entity_id] = {
                "entity_type": entity_type,
                "state": state,
                "timestamp": datetime.now(),
                "context": context,
                "history": state_result["state_history"] + [{
                    "state": state,
                    "timestamp": datetime.now(),
                    "context": context
                }]
            }
            
            # Determine lifecycle phase
            lifecycle_phase = await self._determine_lifecycle_phase(entity_type, state)
            state_result["lifecycle_phase"] = lifecycle_phase
            
            # Calculate progress
            progress = await self._calculate_progress(entity_type, state, lifecycle_phase)
            state_result["progress"] = progress
            
            # Get next possible states
            next_states = self.state_transitions.get(state, [])
            state_result["next_states"] = next_states
            
            # Add state metadata
            state_result["state_metadata"] = {
                "timestamp": datetime.now(),
                "context": context,
                "lifecycle_phase": lifecycle_phase,
                "progress": progress
            }
            
            return state_result
            
        except Exception as e:
            logger.error(f"Error tracking state: {e}")
            return {"error": str(e), "entity_id": entity_id, "current_state": state}
    
    async def _determine_lifecycle_phase(self, entity_type: str, state: str) -> str:
        """Determine lifecycle phase based on entity type and state"""
        if entity_type == "task":
            if state in ["pending", "in_progress"]:
                return "development"
            elif state == "completed":
                return "deployment"
            elif state == "failed":
                return "maintenance"
        elif entity_type == "project":
            if state in ["pending", "in_progress"]:
                return "development"
            elif state == "completed":
                return "deployment"
        
        return "unknown"
    
    async def _calculate_progress(self, entity_type: str, state: str, lifecycle_phase: str) -> float:
        """Calculate progress based on state and lifecycle phase"""
        progress_map = {
            "pending": 0.0,
            "in_progress": 0.5,
            "completed": 1.0,
            "failed": 0.0,
            "cancelled": 0.0,
            "archived": 1.0
        }
        
        base_progress = progress_map.get(state, 0.0)
        
        # Adjust based on lifecycle phase
        if lifecycle_phase == "development":
            return base_progress * 0.6  # 60% of total progress
        elif lifecycle_phase == "deployment":
            return 0.6 + (base_progress * 0.3)  # 60-90% of total progress
        elif lifecycle_phase == "maintenance":
            return 0.9 + (base_progress * 0.1)  # 90-100% of total progress
        
        return base_progress
    
    async def get_state_summary(self, entity_type: str = None) -> Dict[str, Any]:
        """Get summary of all states"""
        try:
            summary = {
                "total_entities": len(self.state_storage),
                "by_state": {},
                "by_entity_type": {},
                "by_lifecycle_phase": {},
                "recent_changes": []
            }
            
            # Analyze states
            for entity_id, info in self.state_storage.items():
                state = info.get("state", "unknown")
                entity_type = info.get("entity_type", "unknown")
                lifecycle_phase = await self._determine_lifecycle_phase(entity_type, state)
                
                # Count by state
                summary["by_state"][state] = summary["by_state"].get(state, 0) + 1
                
                # Count by entity type
                summary["by_entity_type"][entity_type] = summary["by_entity_type"].get(entity_type, 0) + 1
                
                # Count by lifecycle phase
                summary["by_lifecycle_phase"][lifecycle_phase] = summary["by_lifecycle_phase"].get(lifecycle_phase, 0) + 1
            
            # Get recent changes
            recent_changes = []
            for entity_id, info in self.state_storage.items():
                history = info.get("history", [])
                if history:
                    recent_changes.append({
                        "entity_id": entity_id,
                        "latest_state": history[-1]["state"],
                        "timestamp": history[-1]["timestamp"]
                    })
            
            # Sort by timestamp
            recent_changes.sort(key=lambda x: x["timestamp"], reverse=True)
            summary["recent_changes"] = recent_changes[:10]  # Last 10 changes
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting state summary: {e}")
            return {"error": str(e)}

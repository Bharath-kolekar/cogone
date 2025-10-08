"""
Smart Coding AI Management - State Manager
State management for Auth & RBAC system
Extracted from smart_coding_ai_optimized.py
"""

import structlog
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = structlog.get_logger()


class StateManager:
    """StateManager for Auth & RBAC system - Management Systems #5"""
    
    def __init__(self):
        self.state_snapshots: Dict[str, Dict] = {}
        self.state_events: List[Dict] = []
        self.state_transitions: Dict[str, List[Dict]] = {}
        self.state_configs: Dict[str, Dict] = {}
        self.active_states: Dict[str, Dict] = {}
        self.state_history: Dict[str, List[Dict]] = {}
    
    async def initialize_state(self, entity_id: str, entity_type: str, 
                             state_type: str, initial_state: str,
                             state_data: Dict[str, Any] = None,
                             user_id: Optional[str] = None) -> Dict[str, Any]:
        """Initialize state for an entity"""
        try:
            state_key = f"{entity_type}:{entity_id}:{state_type}"
            
            # Check if state already exists
            if state_key in self.state_snapshots:
                current_state = self.state_snapshots[state_key]
                if current_state["status"] == "active":
                    logger.warning(f"State already exists and is active: {state_key}")
                    return current_state
            
            # Create new state snapshot
            state_snapshot = {
                "snapshot_id": str(uuid.uuid4()),
                "entity_id": entity_id,
                "entity_type": entity_type,
                "state_type": state_type,
                "current_state": initial_state,
                "state_data": state_data or {},
                "previous_state": None,
                "status": "active",
                "metadata": {
                    "created_by": user_id,
                    "version": 1
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "expires_at": None
            }
            
            # Store state snapshot
            self.state_snapshots[state_key] = state_snapshot
            self.active_states[state_key] = state_snapshot
            
            # Initialize state history
            if state_key not in self.state_history:
                self.state_history[state_key] = []
            
            self.state_history[state_key].append(state_snapshot.copy())
            
            # Create state event
            await self._create_state_event(
                entity_id, entity_type, "state_initialized", state_type,
                None, initial_state, {"user_id": user_id}, user_id
            )
            
            logger.info(f"State initialized: {state_key} -> {initial_state}")
            return state_snapshot
            
        except Exception as e:
            logger.error(f"Failed to initialize state: {e}")
            raise
    
    async def transition_state(self, entity_id: str, entity_type: str,
                             state_type: str, target_state: str,
                             condition: str = "manual",
                             user_id: Optional[str] = None,
                             event_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Transition entity to a new state"""
        try:
            state_key = f"{entity_type}:{entity_id}:{state_type}"
            
            # Get current state
            if state_key not in self.state_snapshots:
                raise ValueError(f"State not found: {state_key}")
            
            current_snapshot = self.state_snapshots[state_key]
            current_state = current_snapshot["current_state"]
            
            # Check if transition is allowed
            if not await self._is_transition_allowed(state_key, current_state, target_state, condition):
                raise ValueError(f"Transition not allowed: {current_state} -> {target_state}")
            
            # Update state snapshot
            new_snapshot = current_snapshot.copy()
            new_snapshot["snapshot_id"] = str(uuid.uuid4())
            new_snapshot["previous_state"] = current_state
            new_snapshot["current_state"] = target_state
            new_snapshot["updated_at"] = datetime.now().isoformat()
            new_snapshot["metadata"]["version"] = new_snapshot["metadata"].get("version", 1) + 1
            new_snapshot["metadata"]["transitioned_by"] = user_id
            new_snapshot["metadata"]["transition_condition"] = condition
            
            # Update state data if provided
            if event_data:
                new_snapshot["state_data"].update(event_data)
            
            # Store new snapshot
            self.state_snapshots[state_key] = new_snapshot
            self.active_states[state_key] = new_snapshot
            
            # Add to history
            self.state_history[state_key].append(new_snapshot.copy())
            
            # Create state event
            await self._create_state_event(
                entity_id, entity_type, "state_transitioned", state_type,
                current_state, target_state, event_data or {}, user_id
            )
            
            logger.info(f"State transitioned: {state_key} {current_state} -> {target_state}")
            return new_snapshot
            
        except Exception as e:
            logger.error(f"Failed to transition state: {e}")
            raise
    
    async def get_state(self, entity_id: str, entity_type: str, state_type: str) -> Optional[Dict[str, Any]]:
        """Get current state for an entity"""
        try:
            state_key = f"{entity_type}:{entity_id}:{state_type}"
            return self.state_snapshots.get(state_key)
            
        except Exception as e:
            logger.error(f"Failed to get state: {e}")
            return None
    
    async def _is_transition_allowed(self, state_key: str, from_state: str, 
                                   to_state: str, condition: str) -> bool:
        """Check if state transition is allowed"""
        try:
            # Get transition rules for this state type
            transitions = self.state_transitions.get(state_key, [])
            
            # If no specific transitions defined, allow all transitions
            if not transitions:
                return True
            
            # Check if transition is explicitly allowed
            for transition in transitions:
                if (transition["from_state"] == from_state and 
                    transition["to_state"] == to_state and
                    (transition["condition"] == condition or transition["condition"] == "*")):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to check transition: {e}")
            return False
    
    async def _create_state_event(self, entity_id: str, entity_type: str,
                                event_type: str, state_type: str,
                                from_state: Optional[str], to_state: Optional[str],
                                event_data: Dict[str, Any], user_id: Optional[str]):
        """Create state event"""
        try:
            event = {
                "event_id": str(uuid.uuid4()),
                "entity_id": entity_id,
                "entity_type": entity_type,
                "event_type": event_type,
                "state_type": state_type,
                "from_state": from_state,
                "to_state": to_state,
                "event_data": event_data,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "correlation_id": None
            }
            
            self.state_events.append(event)
            
            # Keep only last 10000 events
            if len(self.state_events) > 10000:
                self.state_events = self.state_events[-10000:]
                
        except Exception as e:
            logger.error(f"Failed to create state event: {e}")


# RBACManager extracted to smart_coding_ai_rbacmanager.py



__all__ = ['StateManager']

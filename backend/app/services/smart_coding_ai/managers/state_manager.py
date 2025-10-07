"""
State Manager for Smart Coding AI Service
Preserves state management for Auth & RBAC system
"""

import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
import structlog

logger = structlog.get_logger()


class StateManager:
    """
    StateManager for Auth & RBAC system
    Management Systems #5 - Preserves state transitions and history
    """
    
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
        """
        Initialize state for an entity
        Supports state-based workflow management
        """
        try:
            state_key = f"{entity_type}:{entity_id}:{state_type}"
            
            # Check if state already exists
            if state_key in self.state_snapshots:
                current_state = self.state_snapshots[state_key]
                if current_state["status"] == "active":
                    logger.warning("State already exists and is active", state_key=state_key)
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
            
            logger.info("State initialized", state_key=state_key, initial_state=initial_state)
            return state_snapshot
            
        except Exception as e:
            logger.error("Failed to initialize state", error=str(e))
            raise
    
    async def transition_state(self, entity_id: str, entity_type: str,
                             state_type: str, target_state: str,
                             condition: str = "manual",
                             user_id: Optional[str] = None,
                             event_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Transition entity to a new state
        Maintains state transition history
        """
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
            
            logger.info("State transitioned", state_key=state_key, 
                       from_state=current_state, to_state=target_state)
            return new_snapshot
            
        except Exception as e:
            logger.error("Failed to transition state", error=str(e))
            raise
    
    async def get_state(self, entity_id: str, entity_type: str, state_type: str) -> Optional[Dict[str, Any]]:
        """Get current state for an entity"""
        try:
            state_key = f"{entity_type}:{entity_id}:{state_type}"
            return self.state_snapshots.get(state_key)
            
        except Exception as e:
            logger.error("Failed to get state", error=str(e))
            return None
    
    async def get_state_history(self, entity_id: str, entity_type: str, state_type: str) -> List[Dict[str, Any]]:
        """Get state history for an entity"""
        try:
            state_key = f"{entity_type}:{entity_id}:{state_type}"
            return self.state_history.get(state_key, [])
        except Exception as e:
            logger.error("Failed to get state history", error=str(e))
            return []
    
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
            logger.error("Failed to check transition", error=str(e))
            return False
    
    async def _create_state_event(self, entity_id: str, entity_type: str,
                                event_type: str, state_type: str,
                                from_state: Optional[str], to_state: Optional[str],
                                event_data: Dict[str, Any], user_id: Optional[str]):
        """Create state event for tracking"""
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
            logger.error("Failed to create state event", error=str(e))

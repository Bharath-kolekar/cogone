"""
Observer Pattern Implementation
Follows Observer Pattern for event-driven architecture
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import structlog
import asyncio
from collections import defaultdict

logger = structlog.get_logger()


class EventType(str, Enum):
    """Event types"""
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    AI_AGENT_CREATED = "ai_agent_created"
    AI_AGENT_UPDATED = "ai_agent_updated"
    AI_AGENT_DELETED = "ai_agent_deleted"
    AI_AGENT_EXECUTED = "ai_agent_executed"
    APP_GENERATED = "app_generated"
    APP_DEPLOYED = "app_deployed"
    VOICE_PROCESSED = "voice_processed"
    PAYMENT_COMPLETED = "payment_completed"
    ERROR_OCCURRED = "error_occurred"
    SYSTEM_ALERT = "system_alert"


class EventPriority(str, Enum):
    """Event priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Event:
    """Event data structure"""
    event_id: str
    event_type: EventType
    priority: EventPriority
    data: Dict[str, Any]
    user_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: str = "system"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ObserverResult:
    """Observer execution result"""
    observer_id: str
    success: bool
    execution_time: float
    result: Optional[Any] = None
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.utcnow)


class Observer(ABC):
    """
    Abstract Observer interface
    Follows Observer Pattern
    """
    
    def __init__(self, observer_id: str, name: str):
        self.observer_id = observer_id
        self.name = name
        self.is_active = True
        self.created_at = datetime.utcnow()
    
    @abstractmethod
    async def update(self, event: Event) -> ObserverResult:
        """Update observer with new event"""
        pass
    
    @abstractmethod
    def can_handle(self, event: Event) -> bool:
        """Check if observer can handle the event"""
        pass
    
    def deactivate(self):
        """Deactivate observer"""
        self.is_active = False
        logger.info("Observer deactivated", observer_id=self.observer_id, name=self.name)
    
    def activate(self):
        """Activate observer"""
        self.is_active = True
        logger.info("Observer activated", observer_id=self.observer_id, name=self.name)


class EmailNotificationObserver(Observer):
    """Email notification observer"""
    
    def __init__(self, email_service: Any):
        super().__init__("email_notifier", "Email Notification Observer")
        self.email_service = email_service
        self.subscribed_events = {
            EventType.USER_CREATED,
            EventType.PAYMENT_COMPLETED,
            EventType.ERROR_OCCURRED,
            EventType.SYSTEM_ALERT
        }
    
    async def update(self, event: Event) -> ObserverResult:
        """Send email notification for event"""
        start_time = datetime.utcnow()
        
        try:
            if not self.can_handle(event):
                return ObserverResult(
                    observer_id=self.observer_id,
                    success=False,
                    execution_time=0.0,
                    error="Cannot handle this event type"
                )
            
            # Determine email content based on event type
            email_data = await self._prepare_email_content(event)
            
            # Send email
            success = await self.email_service.send_email(
                to=email_data["to"],
                subject=email_data["subject"],
                body=email_data["body"]
            )
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            logger.info("Email notification sent", 
                       event_type=event.event_type.value,
                       user_id=event.user_id,
                       success=success)
            
            return ObserverResult(
                observer_id=self.observer_id,
                success=success,
                execution_time=execution_time,
                result={"email_sent": success}
            )
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            logger.error("Email notification error", 
                        event_type=event.event_type.value,
                        error=str(e))
            
            return ObserverResult(
                observer_id=self.observer_id,
                success=False,
                execution_time=execution_time,
                error=str(e)
            )
    
    def can_handle(self, event: Event) -> bool:
        """Check if can handle event"""
        return (self.is_active and 
                event.event_type in self.subscribed_events and
                event.priority in [EventPriority.MEDIUM, EventPriority.HIGH, EventPriority.CRITICAL])
    
    async def _prepare_email_content(self, event: Event) -> Dict[str, str]:
        """Prepare email content based on event"""
        templates = {
            EventType.USER_CREATED: {
                "subject": "Welcome to Cognomega AI!",
                "body": f"Welcome! Your account has been created successfully."
            },
            EventType.PAYMENT_COMPLETED: {
                "subject": "Payment Confirmation",
                "body": f"Your payment has been processed successfully."
            },
            EventType.ERROR_OCCURRED: {
                "subject": "System Error Alert",
                "body": f"A system error occurred: {event.data.get('error_message', 'Unknown error')}"
            },
            EventType.SYSTEM_ALERT: {
                "subject": "System Alert",
                "body": f"System alert: {event.data.get('message', 'No details available')}"
            }
        }
        
        template = templates.get(event.event_type, {
            "subject": "System Notification",
            "body": f"Event: {event.event_type.value}"
        })
        
        return {
            "to": event.data.get("email", "admin@cognomega.ai"),
            "subject": template["subject"],
            "body": template["body"]
        }


class AnalyticsObserver(Observer):
    """Analytics tracking observer"""
    
    def __init__(self, analytics_service: Any):
        super().__init__("analytics_tracker", "Analytics Tracking Observer")
        self.analytics_service = analytics_service
        self.subscribed_events = {
            EventType.USER_LOGIN,
            EventType.USER_LOGOUT,
            EventType.AI_AGENT_EXECUTED,
            EventType.APP_GENERATED,
            EventType.VOICE_PROCESSED,
            EventType.PAYMENT_COMPLETED
        }
    
    async def update(self, event: Event) -> ObserverResult:
        """Track analytics event"""
        start_time = datetime.utcnow()
        
        try:
            if not self.can_handle(event):
                return ObserverResult(
                    observer_id=self.observer_id,
                    success=False,
                    execution_time=0.0,
                    error="Cannot handle this event type"
                )
            
            # Track the event
            success = await self.analytics_service.track_event(
                event_name=event.event_type.value,
                user_id=event.user_id,
                metadata={
                    **event.data,
                    "priority": event.priority.value,
                    "source": event.source,
                    "timestamp": event.timestamp.isoformat()
                }
            )
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            logger.info("Analytics event tracked", 
                       event_type=event.event_type.value,
                       user_id=event.user_id,
                       success=success)
            
            return ObserverResult(
                observer_id=self.observer_id,
                success=success,
                execution_time=execution_time,
                result={"event_tracked": success}
            )
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            logger.error("Analytics tracking error", 
                        event_type=event.event_type.value,
                        error=str(e))
            
            return ObserverResult(
                observer_id=self.observer_id,
                success=False,
                execution_time=execution_time,
                error=str(e)
            )
    
    def can_handle(self, event: Event) -> bool:
        """Check if can handle event"""
        return (self.is_active and 
                event.event_type in self.subscribed_events)


class AuditLogObserver(Observer):
    """Audit logging observer"""
    
    def __init__(self, logging_service: Any):
        super().__init__("audit_logger", "Audit Logging Observer")
        self.logging_service = logging_service
        # Subscribe to all events for comprehensive audit logging
        self.subscribed_events = set(EventType)
    
    async def update(self, event: Event) -> ObserverResult:
        """Log audit event"""
        start_time = datetime.utcnow()
        
        try:
            if not self.can_handle(event):
                return ObserverResult(
                    observer_id=self.observer_id,
                    success=False,
                    execution_time=0.0,
                    error="Cannot handle this event type"
                )
            
            # Log the audit event
            await self.logging_service.log_audit(
                action=event.event_type.value,
                user_id=event.user_id,
                metadata={
                    "event_id": event.event_id,
                    "priority": event.priority.value,
                    "source": event.source,
                    "data": event.data,
                    "timestamp": event.timestamp.isoformat()
                }
            )
            
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            logger.debug("Audit event logged", 
                        event_type=event.event_type.value,
                        user_id=event.user_id)
            
            return ObserverResult(
                observer_id=self.observer_id,
                success=True,
                execution_time=execution_time,
                result={"audit_logged": True}
            )
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            logger.error("Audit logging error", 
                        event_type=event.event_type.value,
                        error=str(e))
            
            return ObserverResult(
                observer_id=self.observer_id,
                success=False,
                execution_time=execution_time,
                error=str(e)
            )
    
    def can_handle(self, event: Event) -> bool:
        """Check if can handle event"""
        return self.is_active


class Subject:
    """
    Subject class following Observer Pattern
    Manages observers and notifies them of events
    """
    
    def __init__(self):
        self.observers: Dict[EventType, List[Observer]] = defaultdict(list)
        self.global_observers: List[Observer] = []
        self.event_history: List[Event] = []
        self.max_history_size = 10000
    
    def attach(self, observer: Observer, event_types: Optional[List[EventType]] = None):
        """Attach observer to specific event types or all events"""
        if event_types:
            for event_type in event_types:
                if observer not in self.observers[event_type]:
                    self.observers[event_type].append(observer)
                    logger.info("Observer attached to event type", 
                               observer_id=observer.observer_id,
                               event_type=event_type.value)
        else:
            # Attach to all events
            if observer not in self.global_observers:
                self.global_observers.append(observer)
                logger.info("Observer attached to all events", 
                           observer_id=observer.observer_id)
    
    def detach(self, observer: Observer, event_types: Optional[List[EventType]] = None):
        """Detach observer from specific event types or all events"""
        if event_types:
            for event_type in event_types:
                if observer in self.observers[event_type]:
                    self.observers[event_type].remove(observer)
                    logger.info("Observer detached from event type", 
                               observer_id=observer.observer_id,
                               event_type=event_type.value)
        else:
            # Detach from all events
            if observer in self.global_observers:
                self.global_observers.remove(observer)
                logger.info("Observer detached from all events", 
                           observer_id=observer.observer_id)
            
            # Also remove from specific event types
            for event_type_observers in self.observers.values():
                if observer in event_type_observers:
                    event_type_observers.remove(observer)
    
    async def notify(self, event: Event):
        """Notify all relevant observers of an event"""
        try:
            # Add to event history
            self.event_history.append(event)
            
            # Maintain history size
            if len(self.event_history) > self.max_history_size:
                self.event_history.pop(0)
            
            # Get observers for this event type
            event_observers = self.observers.get(event.event_type, [])
            all_observers = event_observers + self.global_observers
            
            # Remove duplicates while preserving order
            unique_observers = []
            seen = set()
            for observer in all_observers:
                if observer.observer_id not in seen:
                    unique_observers.append(observer)
                    seen.add(observer.observer_id)
            
            # Notify observers
            notification_tasks = []
            for observer in unique_observers:
                if observer.is_active and observer.can_handle(event):
                    task = asyncio.create_task(self._notify_observer(observer, event))
                    notification_tasks.append(task)
            
            # Wait for all notifications to complete
            if notification_tasks:
                results = await asyncio.gather(*notification_tasks, return_exceptions=True)
                
                # Log results
                successful_notifications = sum(1 for result in results if not isinstance(result, Exception))
                logger.info("Event notifications completed", 
                           event_type=event.event_type.value,
                           event_id=event.event_id,
                           total_observers=len(notification_tasks),
                           successful_notifications=successful_notifications)
            
        except Exception as e:
            logger.error("Event notification error", 
                        event_type=event.event_type.value,
                        event_id=event.event_id,
                        error=str(e))
    
    async def _notify_observer(self, observer: Observer, event: Event):
        """Notify a single observer"""
        try:
            result = await observer.update(event)
            
            if not result.success:
                logger.warning("Observer notification failed", 
                              observer_id=observer.observer_id,
                              event_type=event.event_type.value,
                              error=result.error)
            
        except Exception as e:
            logger.error("Observer notification exception", 
                        observer_id=observer.observer_id,
                        event_type=event.event_type.value,
                        error=str(e))
    
    def get_observers_for_event(self, event_type: EventType) -> List[Observer]:
        """Get all observers for a specific event type"""
        event_observers = self.observers.get(event_type, [])
        return event_observers + [obs for obs in self.global_observers if obs.is_active]
    
    def get_event_history(self, event_type: Optional[EventType] = None, limit: int = 100) -> List[Event]:
        """Get event history with optional filtering"""
        events = self.event_history
        
        if event_type:
            events = [event for event in events if event.event_type == event_type]
        
        return events[-limit:]


class EventManager:
    """
    Event Manager following Observer Pattern
    Centralized event management and distribution
    """
    
    def __init__(self):
        self.subject = Subject()
        self.event_counter = 0
    
    def register_observer(
        self, 
        observer: Observer, 
        event_types: Optional[List[EventType]] = None
    ):
        """Register an observer"""
        self.subject.attach(observer, event_types)
        logger.info("Observer registered", 
                   observer_id=observer.observer_id,
                   name=observer.name,
                   event_types=[et.value for et in (event_types or [])])
    
    def unregister_observer(
        self, 
        observer: Observer, 
        event_types: Optional[List[EventType]] = None
    ):
        """Unregister an observer"""
        self.subject.detach(observer, event_types)
        logger.info("Observer unregistered", 
                   observer_id=observer.observer_id,
                   event_types=[et.value for et in (event_types or [])])
    
    async def publish_event(
        self,
        event_type: EventType,
        data: Dict[str, Any],
        user_id: Optional[str] = None,
        priority: EventPriority = EventPriority.MEDIUM,
        source: str = "system",
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Publish an event"""
        self.event_counter += 1
        event_id = f"{event_type.value}_{self.event_counter}_{int(datetime.utcnow().timestamp())}"
        
        event = Event(
            event_id=event_id,
            event_type=event_type,
            priority=priority,
            data=data,
            user_id=user_id,
            source=source,
            metadata=metadata or {}
        )
        
        await self.subject.notify(event)
        
        logger.info("Event published", 
                   event_id=event_id,
                   event_type=event_type.value,
                   priority=priority.value,
                   user_id=user_id)
    
    def get_observers_status(self) -> Dict[str, Any]:
        """Get status of all observers"""
        status = {
            "total_observers": 0,
            "active_observers": 0,
            "observers_by_event_type": {},
            "global_observers": len(self.subject.global_observers)
        }
        
        for event_type, observers in self.subject.observers.items():
            active_count = sum(1 for obs in observers if obs.is_active)
            status["observers_by_event_type"][event_type.value] = {
                "total": len(observers),
                "active": active_count
            }
            status["total_observers"] += len(observers)
            status["active_observers"] += active_count
        
        return status
    
    def get_event_statistics(self) -> Dict[str, Any]:
        """Get event statistics"""
        event_counts = {}
        for event in self.subject.event_history:
            event_type = event.event_type.value
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        return {
            "total_events": len(self.subject.event_history),
            "events_by_type": event_counts,
            "oldest_event": self.subject.event_history[0].timestamp if self.subject.event_history else None,
            "newest_event": self.subject.event_history[-1].timestamp if self.subject.event_history else None
        }


# Global event manager instance
event_manager = EventManager()

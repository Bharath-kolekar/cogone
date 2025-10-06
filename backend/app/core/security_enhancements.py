"""
Security Enhancements System for Cognomega AI
Advanced threat detection, anomaly monitoring, and security optimization
"""

import asyncio
import hashlib
import hmac
import json
import time
import ipaddress
from typing import Any, Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import structlog
import numpy as np
from collections import defaultdict, deque
import re

logger = structlog.get_logger()


class ThreatLevel(str, Enum):
    """Threat severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatType(str, Enum):
    """Types of security threats"""
    BRUTE_FORCE = "brute_force"
    DDoS_ATTACK = "ddos_attack"
    SQL_INJECTION = "sql_injection"
    XSS_ATTACK = "xss_attack"
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"
    SUSPICIOUS_PATTERN = "suspicious_pattern"
    MALICIOUS_PAYLOAD = "malicious_payload"
    GEOGRAPHIC_ANOMALY = "geographic_anomaly"
    BEHAVIORAL_ANOMALY = "behavioral_anomaly"
    AUTHENTICATION_ABUSE = "authentication_abuse"


class SecurityAction(str, Enum):
    """Security actions to take"""
    ALLOW = "allow"
    BLOCK = "block"
    RATE_LIMIT = "rate_limit"
    CAPTCHA = "captcha"
    MFA_REQUIRED = "mfa_required"
    QUARANTINE = "quarantine"
    LOG_ONLY = "log_only"
    ALERT = "alert"


@dataclass
class SecurityEvent:
    """Security event record"""
    event_id: str
    threat_type: ThreatType
    threat_level: ThreatLevel
    source_ip: str
    user_id: Optional[str]
    timestamp: datetime
    description: str
    details: Dict[str, Any] = field(default_factory=dict)
    action_taken: SecurityAction = SecurityAction.LOG_ONLY
    confidence: float = 0.0


@dataclass
class ThreatPattern:
    """Threat pattern definition"""
    pattern_id: str
    name: str
    threat_type: ThreatType
    threat_level: ThreatLevel
    pattern_regex: str
    description: str
    action: SecurityAction
    enabled: bool = True


@dataclass
class SecurityMetrics:
    """Security metrics"""
    total_requests: int = 0
    blocked_requests: int = 0
    suspicious_requests: int = 0
    threat_detections: int = 0
    false_positives: int = 0
    average_response_time: float = 0.0
    security_score: float = 100.0
    last_updated: datetime = field(default_factory=datetime.now)


class SecurityEnhancementEngine:
    """Advanced security enhancement engine"""
    
    def __init__(self):
        # Security state
        self.blocked_ips: Set[str] = set()
        self.rate_limited_ips: Dict[str, datetime] = {}
        self.suspicious_users: Set[str] = set()
        self.quarantined_requests: Dict[str, datetime] = {}
        
        # Request tracking
        self.request_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.user_behavior: Dict[str, Dict[str, Any]] = {}
        self.ip_behavior: Dict[str, Dict[str, Any]] = {}
        
        # Threat patterns
        self.threat_patterns: Dict[str, ThreatPattern] = {}
        self._initialize_threat_patterns()
        
        # Security metrics
        self.security_metrics = SecurityMetrics()
        
        # Configuration
        self.max_requests_per_minute = 100
        self.max_requests_per_hour = 1000
        self.block_duration_minutes = 60
        self.rate_limit_duration_minutes = 15
        self.suspicious_threshold = 5
        self.geographic_anomaly_threshold = 0.8
        
        # Background tasks
        self._monitoring_task = None
        self._cleanup_task = None
        
        # Initialize
        self._start_background_tasks()
    
    def _initialize_threat_patterns(self):
        """Initialize common threat patterns"""
        patterns = [
            ThreatPattern(
                pattern_id="sql_injection_1",
                name="SQL Injection - Basic",
                threat_type=ThreatType.SQL_INJECTION,
                threat_level=ThreatLevel.HIGH,
                pattern_regex=r"(union|select|insert|delete|drop|update|exec|script).*from",
                description="Basic SQL injection attempt",
                action=SecurityAction.BLOCK
            ),
            ThreatPattern(
                pattern_id="sql_injection_2",
                name="SQL Injection - Advanced",
                threat_type=ThreatType.SQL_INJECTION,
                threat_level=ThreatLevel.CRITICAL,
                pattern_regex=r"('|(\\')|(;)|(\\;)|(\\*)|(\\+)|(\\-)|(\\/)|(\\\\)|(\\%)|(\\_))",
                description="Advanced SQL injection attempt",
                action=SecurityAction.BLOCK
            ),
            ThreatPattern(
                pattern_id="xss_1",
                name="XSS Attack - Script Tags",
                threat_type=ThreatType.XSS_ATTACK,
                threat_level=ThreatLevel.HIGH,
                pattern_regex=r"<script[^>]*>.*?</script>",
                description="XSS attack with script tags",
                action=SecurityAction.BLOCK
            ),
            ThreatPattern(
                pattern_id="xss_2",
                name="XSS Attack - Event Handlers",
                threat_type=ThreatType.XSS_ATTACK,
                threat_level=ThreatLevel.HIGH,
                pattern_regex=r"on\w+\s*=",
                description="XSS attack with event handlers",
                action=SecurityAction.BLOCK
            ),
            ThreatPattern(
                pattern_id="path_traversal",
                name="Path Traversal",
                threat_type=ThreatType.SUSPICIOUS_PATTERN,
                threat_level=ThreatLevel.HIGH,
                pattern_regex=r"\.\./|\.\.\\\\",
                description="Path traversal attempt",
                action=SecurityAction.BLOCK
            ),
            ThreatPattern(
                pattern_id="command_injection",
                name="Command Injection",
                threat_type=ThreatType.MALICIOUS_PAYLOAD,
                threat_level=ThreatLevel.CRITICAL,
                pattern_regex=r"[;&|`$(){}]",
                description="Command injection attempt",
                action=SecurityAction.BLOCK
            )
        ]
        
        for pattern in patterns:
            self.threat_patterns[pattern.pattern_id] = pattern
    
    def _start_background_tasks(self):
        """Start background security monitoring tasks"""
        self._monitoring_task = asyncio.create_task(self._monitor_security())
        self._cleanup_task = asyncio.create_task(self._cleanup_expired_entries())
    
    async def _monitor_security(self):
        """Monitor security continuously"""
        while True:
            try:
                await asyncio.sleep(60)  # Monitor every minute
                
                # Update security metrics
                await self._update_security_metrics()
                
                # Analyze behavioral patterns
                await self._analyze_behavioral_patterns()
                
                # Check for geographic anomalies
                await self._check_geographic_anomalies()
                
                # Clean up old data
                await self._cleanup_old_data()
                
            except Exception as e:
                logger.error("Security monitoring error", error=str(e))
                await asyncio.sleep(60)
    
    async def _cleanup_expired_entries(self):
        """Clean up expired security entries"""
        while True:
            try:
                await asyncio.sleep(300)  # Clean up every 5 minutes
                
                current_time = datetime.now()
                
                # Clean up rate limited IPs
                expired_rate_limits = [
                    ip for ip, expiry in self.rate_limited_ips.items()
                    if current_time > expiry
                ]
                for ip in expired_rate_limits:
                    del self.rate_limited_ips[ip]
                
                # Clean up quarantined requests
                expired_quarantines = [
                    req_id for req_id, expiry in self.quarantined_requests.items()
                    if current_time > expiry
                ]
                for req_id in expired_quarantines:
                    del self.quarantined_requests[req_id]
                
                if expired_rate_limits or expired_quarantines:
                    logger.info("Cleaned up expired security entries", 
                               rate_limits=len(expired_rate_limits),
                               quarantines=len(expired_quarantines))
                
            except Exception as e:
                logger.error("Security cleanup error", error=str(e))
                await asyncio.sleep(300)
    
    async def _update_security_metrics(self):
        """Update security metrics"""
        try:
            total_requests = sum(len(requests) for requests in self.request_history.values())
            blocked_requests = len(self.blocked_ips)
            
            # Calculate security score
            if total_requests > 0:
                threat_ratio = self.security_metrics.threat_detections / total_requests
                block_ratio = blocked_requests / total_requests
                
                # Security score based on threat and block ratios
                security_score = max(0, 100 - (threat_ratio * 50 + block_ratio * 30))
            else:
                security_score = 100.0
            
            self.security_metrics.update({
                "total_requests": total_requests,
                "blocked_requests": blocked_requests,
                "suspicious_requests": len(self.suspicious_users),
                "security_score": security_score,
                "last_updated": datetime.now()
            })
            
        except Exception as e:
            logger.error("Security metrics update error", error=str(e))
    
    async def _analyze_behavioral_patterns(self):
        """Analyze user and IP behavioral patterns"""
        try:
            current_time = datetime.now()
            analysis_window = timedelta(hours=1)
            
            for ip, requests in self.request_history.items():
                if not requests:
                    continue
                
                # Filter recent requests
                recent_requests = [
                    req for req in requests
                    if current_time - req.get("timestamp", datetime.min) < analysis_window
                ]
                
                if len(recent_requests) < 5:
                    continue
                
                # Analyze request patterns
                await self._analyze_ip_behavior(ip, recent_requests)
            
            for user_id, behavior in self.user_behavior.items():
                await self._analyze_user_behavior(user_id, behavior)
                
        except Exception as e:
            logger.error("Behavioral pattern analysis error", error=str(e))
    
    async def _analyze_ip_behavior(self, ip: str, requests: List[Dict[str, Any]]):
        """Analyze IP behavioral patterns"""
        try:
            # Calculate request frequency
            request_times = [req.get("timestamp", datetime.now()) for req in requests]
            if len(request_times) < 2:
                return
            
            # Calculate intervals between requests
            intervals = []
            for i in range(1, len(request_times)):
                interval = (request_times[i] - request_times[i-1]).total_seconds()
                intervals.append(interval)
            
            avg_interval = np.mean(intervals)
            std_interval = np.std(intervals)
            
            # Detect automated behavior (very regular intervals)
            if std_interval < avg_interval * 0.1 and avg_interval < 5:
                await self._create_security_event(
                    threat_type=ThreatType.BEHAVIORAL_ANOMALY,
                    threat_level=ThreatLevel.MEDIUM,
                    source_ip=ip,
                    description=f"Automated request pattern detected (avg interval: {avg_interval:.2f}s)",
                    details={"avg_interval": avg_interval, "std_interval": std_interval}
                )
            
            # Detect high-frequency requests
            if len(requests) > self.max_requests_per_minute:
                await self._create_security_event(
                    threat_type=ThreatType.RATE_LIMIT_EXCEEDED,
                    threat_level=ThreatLevel.HIGH,
                    source_ip=ip,
                    description=f"High-frequency requests detected ({len(requests)} requests)",
                    details={"request_count": len(requests), "time_window": "1 hour"}
                )
            
            # Store IP behavior
            self.ip_behavior[ip] = {
                "avg_interval": avg_interval,
                "std_interval": std_interval,
                "request_count": len(requests),
                "last_analyzed": datetime.now()
            }
            
        except Exception as e:
            logger.error("IP behavior analysis error", ip=ip, error=str(e))
    
    async def _analyze_user_behavior(self, user_id: str, behavior: Dict[str, Any]):
        """Analyze user behavioral patterns"""
        try:
            # Check for unusual access patterns
            if behavior.get("failed_logins", 0) > 5:
                await self._create_security_event(
                    threat_type=ThreatType.AUTHENTICATION_ABUSE,
                    threat_level=ThreatLevel.HIGH,
                    user_id=user_id,
                    description=f"Multiple failed login attempts ({behavior['failed_logins']})",
                    details={"failed_logins": behavior["failed_logins"]}
                )
            
            # Check for suspicious user agent patterns
            user_agents = behavior.get("user_agents", [])
            if len(set(user_agents)) > 10:  # Many different user agents
                await self._create_security_event(
                    threat_type=ThreatType.BEHAVIORAL_ANOMALY,
                    threat_level=ThreatLevel.MEDIUM,
                    user_id=user_id,
                    description=f"Multiple user agents detected ({len(set(user_agents))})",
                    details={"unique_user_agents": len(set(user_agents))}
                )
            
        except Exception as e:
            logger.error("User behavior analysis error", user_id=user_id, error=str(e))
    
    async def _check_geographic_anomalies(self):
        """Check for geographic anomalies"""
        try:
            # This would integrate with IP geolocation services
            # For now, we'll simulate the check
            
            for ip, behavior in self.ip_behavior.items():
                # Simulate geographic anomaly detection
                if behavior.get("request_count", 0) > 100:
                    # High request count from single IP might indicate geographic anomaly
                    await self._create_security_event(
                        threat_type=ThreatType.GEOGRAPHIC_ANOMALY,
                        threat_level=ThreatLevel.MEDIUM,
                        source_ip=ip,
                        description=f"High request volume from geographic location",
                        details={"request_count": behavior["request_count"]}
                    )
            
        except Exception as e:
            logger.error("Geographic anomaly check error", error=str(e))
    
    async def _cleanup_old_data(self):
        """Clean up old request history and behavior data"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=24)
            
            # Clean up old request history
            for ip, requests in self.request_history.items():
                while requests and requests[0].get("timestamp", datetime.min) < cutoff_time:
                    requests.popleft()
            
            # Clean up old behavior data
            old_users = [
                user_id for user_id, behavior in self.user_behavior.items()
                if behavior.get("last_activity", datetime.min) < cutoff_time
            ]
            for user_id in old_users:
                del self.user_behavior[user_id]
            
            old_ips = [
                ip for ip, behavior in self.ip_behavior.items()
                if behavior.get("last_analyzed", datetime.min) < cutoff_time
            ]
            for ip in old_ips:
                del self.ip_behavior[ip]
            
            if old_users or old_ips:
                logger.info("Cleaned up old behavior data", 
                           users=len(old_users), 
                           ips=len(old_ips))
            
        except Exception as e:
            logger.error("Data cleanup error", error=str(e))
    
    async def analyze_request(
        self, 
        request_data: Dict[str, Any]
    ) -> Tuple[SecurityAction, Optional[SecurityEvent]]:
        """Analyze incoming request for security threats"""
        try:
            source_ip = request_data.get("source_ip", "unknown")
            user_id = request_data.get("user_id")
            method = request_data.get("method", "GET")
            path = request_data.get("path", "")
            headers = request_data.get("headers", {})
            body = request_data.get("body", "")
            user_agent = headers.get("user-agent", "")
            
            # Check if IP is blocked
            if source_ip in self.blocked_ips:
                return SecurityAction.BLOCK, None
            
            # Check rate limiting
            if await self._check_rate_limit(source_ip):
                return SecurityAction.RATE_LIMIT, None
            
            # Analyze request content for threats
            threat_event = await self._analyze_content_threats(
                source_ip=source_ip,
                user_id=user_id,
                path=path,
                headers=headers,
                body=body,
                user_agent=user_agent
            )
            
            if threat_event:
                # Take action based on threat level
                action = await self._determine_security_action(threat_event)
                
                # Record request
                await self._record_request(request_data)
                
                return action, threat_event
            
            # Record normal request
            await self._record_request(request_data)
            
            return SecurityAction.ALLOW, None
            
        except Exception as e:
            logger.error("Request analysis error", error=str(e))
            return SecurityAction.ALLOW, None
    
    async def _check_rate_limit(self, source_ip: str) -> bool:
        """Check if IP is rate limited"""
        try:
            if source_ip in self.rate_limited_ips:
                expiry = self.rate_limited_ips[source_ip]
                if datetime.now() < expiry:
                    return True
                else:
                    del self.rate_limited_ips[source_ip]
            
            return False
            
        except Exception as e:
            logger.error("Rate limit check error", ip=source_ip, error=str(e))
            return False
    
    async def _analyze_content_threats(
        self, 
        source_ip: str,
        user_id: Optional[str],
        path: str,
        headers: Dict[str, str],
        body: str,
        user_agent: str
    ) -> Optional[SecurityEvent]:
        """Analyze request content for security threats"""
        try:
            # Check threat patterns
            content_to_check = f"{path} {body} {json.dumps(headers)}"
            
            for pattern_id, pattern in self.threat_patterns.items():
                if not pattern.enabled:
                    continue
                
                if re.search(pattern.pattern_regex, content_to_check, re.IGNORECASE):
                    return await self._create_security_event(
                        threat_type=pattern.threat_type,
                        threat_level=pattern.threat_level,
                        source_ip=source_ip,
                        user_id=user_id,
                        description=f"Threat pattern detected: {pattern.name}",
                        details={
                            "pattern_id": pattern_id,
                            "pattern_name": pattern.name,
                            "matched_content": content_to_check[:200]
                        }
                    )
            
            # Check for suspicious user agents
            if self._is_suspicious_user_agent(user_agent):
                return await self._create_security_event(
                    threat_type=ThreatType.SUSPICIOUS_PATTERN,
                    threat_level=ThreatLevel.MEDIUM,
                    source_ip=source_ip,
                    user_id=user_id,
                    description="Suspicious user agent detected",
                    details={"user_agent": user_agent}
                )
            
            return None
            
        except Exception as e:
            logger.error("Content threat analysis error", error=str(e))
            return None
    
    def _is_suspicious_user_agent(self, user_agent: str) -> bool:
        """Check if user agent is suspicious"""
        suspicious_patterns = [
            r"bot", r"crawler", r"spider", r"scraper",
            r"curl", r"wget", r"python", r"java",
            r"automated", r"test", r"scan"
        ]
        
        user_agent_lower = user_agent.lower()
        for pattern in suspicious_patterns:
            if re.search(pattern, user_agent_lower):
                return True
        
        return False
    
    async def _create_security_event(
        self,
        threat_type: ThreatType,
        threat_level: ThreatLevel,
        source_ip: str,
        user_id: Optional[str] = None,
        description: str = "",
        details: Dict[str, Any] = None
    ) -> SecurityEvent:
        """Create a security event"""
        try:
            event_id = hashlib.md5(
                f"{source_ip}_{user_id}_{threat_type}_{datetime.now().isoformat()}".encode()
            ).hexdigest()
            
            event = SecurityEvent(
                event_id=event_id,
                threat_type=threat_type,
                threat_level=threat_level,
                source_ip=source_ip,
                user_id=user_id,
                timestamp=datetime.now(),
                description=description,
                details=details or {},
                confidence=0.8  # Default confidence
            )
            
            logger.warning("Security event detected",
                         event_id=event_id,
                         threat_type=threat_type.value,
                         threat_level=threat_level.value,
                         source_ip=source_ip,
                         user_id=user_id,
                         description=description)
            
            return event
            
        except Exception as e:
            logger.error("Security event creation error", error=str(e))
            raise
    
    async def _determine_security_action(self, event: SecurityEvent) -> SecurityAction:
        """Determine security action based on threat event"""
        try:
            # Default action from threat pattern
            for pattern in self.threat_patterns.values():
                if pattern.threat_type == event.threat_type:
                    return pattern.action
            
            # Override based on threat level
            if event.threat_level == ThreatLevel.CRITICAL:
                return SecurityAction.BLOCK
            elif event.threat_level == ThreatLevel.HIGH:
                return SecurityAction.RATE_LIMIT
            elif event.threat_level == ThreatLevel.MEDIUM:
                return SecurityAction.CAPTCHA
            else:
                return SecurityAction.LOG_ONLY
                
        except Exception as e:
            logger.error("Security action determination error", error=str(e))
            return SecurityAction.LOG_ONLY
    
    async def _record_request(self, request_data: Dict[str, Any]):
        """Record request for analysis"""
        try:
            source_ip = request_data.get("source_ip", "unknown")
            user_id = request_data.get("user_id")
            
            # Add timestamp
            request_data["timestamp"] = datetime.now()
            
            # Record in request history
            self.request_history[source_ip].append(request_data)
            
            # Update user behavior
            if user_id:
                if user_id not in self.user_behavior:
                    self.user_behavior[user_id] = {
                        "request_count": 0,
                        "failed_logins": 0,
                        "user_agents": [],
                        "last_activity": datetime.now()
                    }
                
                behavior = self.user_behavior[user_id]
                behavior["request_count"] += 1
                behavior["last_activity"] = datetime.now()
                
                # Track user agents
                user_agent = request_data.get("headers", {}).get("user-agent", "")
                if user_agent:
                    behavior["user_agents"].append(user_agent)
                    if len(behavior["user_agents"]) > 20:
                        behavior["user_agents"].pop(0)
                
                # Track failed logins
                if request_data.get("status_code") == 401:
                    behavior["failed_logins"] += 1
            
        except Exception as e:
            logger.error("Request recording error", error=str(e))
    
    async def block_ip(self, ip: str, duration_minutes: int = None):
        """Block an IP address"""
        try:
            if duration_minutes is None:
                duration_minutes = self.block_duration_minutes
            
            self.blocked_ips.add(ip)
            
            # Schedule unblock
            asyncio.create_task(self._schedule_unblock(ip, duration_minutes))
            
            logger.info("IP blocked", ip=ip, duration_minutes=duration_minutes)
            
        except Exception as e:
            logger.error("IP block error", ip=ip, error=str(e))
    
    async def _schedule_unblock(self, ip: str, duration_minutes: int):
        """Schedule IP unblock"""
        await asyncio.sleep(duration_minutes * 60)
        self.blocked_ips.discard(ip)
        logger.info("IP unblocked", ip=ip)
    
    async def rate_limit_ip(self, ip: str, duration_minutes: int = None):
        """Rate limit an IP address"""
        try:
            if duration_minutes is None:
                duration_minutes = self.rate_limit_duration_minutes
            
            expiry = datetime.now() + timedelta(minutes=duration_minutes)
            self.rate_limited_ips[ip] = expiry
            
            logger.info("IP rate limited", ip=ip, duration_minutes=duration_minutes)
            
        except Exception as e:
            logger.error("IP rate limit error", ip=ip, error=str(e))
    
    async def get_security_status(self) -> Dict[str, Any]:
        """Get current security status"""
        try:
            return {
                "security_metrics": {
                    "total_requests": self.security_metrics.total_requests,
                    "blocked_requests": self.security_metrics.blocked_requests,
                    "suspicious_requests": self.security_metrics.suspicious_requests,
                    "threat_detections": self.security_metrics.threat_detections,
                    "security_score": self.security_metrics.security_score,
                    "last_updated": self.security_metrics.last_updated.isoformat()
                },
                "active_blocks": {
                    "blocked_ips": len(self.blocked_ips),
                    "rate_limited_ips": len(self.rate_limited_ips),
                    "suspicious_users": len(self.suspicious_users),
                    "quarantined_requests": len(self.quarantined_requests)
                },
                "threat_patterns": {
                    "total_patterns": len(self.threat_patterns),
                    "enabled_patterns": len([p for p in self.threat_patterns.values() if p.enabled])
                },
                "monitoring_status": {
                    "monitoring_active": self._monitoring_task is not None and not self._monitoring_task.done(),
                    "cleanup_active": self._cleanup_task is not None and not self._cleanup_task.done()
                },
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error("Security status error", error=str(e))
            return {}


# Global security enhancement engine instance
security_enhancement_engine = SecurityEnhancementEngine()


# Convenience functions
async def analyze_request_security(request_data: Dict[str, Any]) -> Tuple[SecurityAction, Optional[SecurityEvent]]:
    """Analyze request for security threats"""
    return await security_enhancement_engine.analyze_request(request_data)


async def get_security_status() -> Dict[str, Any]:
    """Get current security status"""
    return await security_enhancement_engine.get_security_status()


async def block_ip_address(ip: str, duration_minutes: int = None):
    """Block an IP address"""
    await security_enhancement_engine.block_ip(ip, duration_minutes)


async def rate_limit_ip_address(ip: str, duration_minutes: int = None):
    """Rate limit an IP address"""
    await security_enhancement_engine.rate_limit_ip(ip, duration_minutes)

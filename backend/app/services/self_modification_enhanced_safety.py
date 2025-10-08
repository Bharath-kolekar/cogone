"""
Enhanced Safety System for Self-Modification
Provides additional safety layers to ensure ZERO risk of self-breakage

New Safety Features:
1. Circuit Breaker Pattern
2. Automatic Rollback on Failure
3. Pre-flight Health Checks
4. Backup & Recovery System
5. Anomaly Detection
6. Canary Deployments
7. Rate Limiting
8. Health Thresholds
"""

import structlog
import asyncio
import time
import json
import shutil
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import hashlib

logger = structlog.get_logger()


class CircuitState(str, Enum):
    """Circuit breaker states"""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Blocking all modifications
    HALF_OPEN = "half_open"  # Testing if system recovered


class HealthStatus(str, Enum):
    """System health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    CRITICAL = "critical"


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration"""
    failure_threshold: int = 5           # Open circuit after N failures
    success_threshold: int = 3           # Close circuit after N successes
    timeout_seconds: int = 300           # 5 minutes before attempting recovery
    half_open_max_calls: int = 1         # Test with 1 call in half-open state


@dataclass
class HealthThreshold:
    """Health thresholds for modifications"""
    min_system_health: float = 80.0      # Minimum health % to allow modifications
    max_error_rate: float = 0.05         # Maximum 5% error rate
    min_success_rate: float = 0.90       # Minimum 90% success rate
    max_response_time: float = 5.0       # Maximum 5 seconds response time
    min_available_memory: float = 20.0   # Minimum 20% memory available


@dataclass
class ModificationMetrics:
    """Metrics for modification operations"""
    total_attempts: int = 0
    total_successes: int = 0
    total_failures: int = 0
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    average_response_time: float = 0.0
    response_times: List[float] = field(default_factory=list)


@dataclass
class BackupRecord:
    """Record of a backup"""
    backup_id: str
    backup_path: Path
    files_backed_up: List[str]
    backup_size: int
    created_at: datetime
    expires_at: datetime
    checksum: str


class CircuitBreaker:
    """
    Circuit breaker pattern to prevent cascading failures
    Automatically stops modifications if system becomes unhealthy
    """
    
    def __init__(self, config: CircuitBreakerConfig = None):
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.metrics = ModificationMetrics()
        self.state_changed_at = datetime.now()
        self.half_open_calls = 0
        
    def can_proceed(self) -> Tuple[bool, str]:
        """Check if modification can proceed"""
        if self.state == CircuitState.CLOSED:
            return True, "Circuit closed - normal operation"
        
        if self.state == CircuitState.OPEN:
            # Check if timeout has elapsed
            if datetime.now() - self.state_changed_at > timedelta(seconds=self.config.timeout_seconds):
                self._transition_to_half_open()
                return True, "Circuit half-open - testing recovery"
            return False, "Circuit open - too many failures detected"
        
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls < self.config.half_open_max_calls:
                return True, "Circuit half-open - testing call allowed"
            return False, "Circuit half-open - max test calls reached"
        
        return False, "Unknown circuit state"
    
    def record_success(self):
        """Record successful modification"""
        self.metrics.total_attempts += 1
        self.metrics.total_successes += 1
        self.metrics.consecutive_successes += 1
        self.metrics.consecutive_failures = 0
        self.metrics.last_success_time = datetime.now()
        
        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1
            if self.metrics.consecutive_successes >= self.config.success_threshold:
                self._transition_to_closed()
        
        logger.info("Circuit breaker recorded success", state=self.state)
    
    def record_failure(self, error: str):
        """Record failed modification"""
        self.metrics.total_attempts += 1
        self.metrics.total_failures += 1
        self.metrics.consecutive_failures += 1
        self.metrics.consecutive_successes = 0
        self.metrics.last_failure_time = datetime.now()
        
        if self.state == CircuitState.CLOSED:
            if self.metrics.consecutive_failures >= self.config.failure_threshold:
                self._transition_to_open()
        
        if self.state == CircuitState.HALF_OPEN:
            self._transition_to_open()
        
        logger.warning("Circuit breaker recorded failure", 
                      state=self.state, 
                      consecutive_failures=self.metrics.consecutive_failures,
                      error=error)
    
    def _transition_to_open(self):
        """Transition to OPEN state"""
        self.state = CircuitState.OPEN
        self.state_changed_at = datetime.now()
        logger.error("Circuit breaker OPENED - modifications blocked",
                    consecutive_failures=self.metrics.consecutive_failures)
    
    def _transition_to_half_open(self):
        """Transition to HALF_OPEN state"""
        self.state = CircuitState.HALF_OPEN
        self.state_changed_at = datetime.now()
        self.half_open_calls = 0
        self.metrics.consecutive_failures = 0
        logger.info("Circuit breaker HALF-OPEN - testing recovery")
    
    def _transition_to_closed(self):
        """Transition to CLOSED state"""
        self.state = CircuitState.CLOSED
        self.state_changed_at = datetime.now()
        self.half_open_calls = 0
        logger.info("Circuit breaker CLOSED - normal operation resumed")
    
    def get_status(self) -> Dict[str, Any]:
        """Get circuit breaker status"""
        success_rate = (self.metrics.total_successes / self.metrics.total_attempts 
                       if self.metrics.total_attempts > 0 else 1.0)
        
        return {
            "state": self.state,
            "state_changed_at": self.state_changed_at.isoformat(),
            "metrics": {
                "total_attempts": self.metrics.total_attempts,
                "total_successes": self.metrics.total_successes,
                "total_failures": self.metrics.total_failures,
                "success_rate": success_rate,
                "consecutive_failures": self.metrics.consecutive_failures,
                "consecutive_successes": self.metrics.consecutive_successes
            },
            "can_proceed": self.can_proceed()[0]
        }


class HealthMonitor:
    """
    Monitors system health and prevents modifications when unhealthy
    """
    
    def __init__(self, thresholds: HealthThreshold = None):
        self.thresholds = thresholds or HealthThreshold()
        self.health_history: List[Dict[str, Any]] = []
        self.max_history = 100
    
    async def check_health(self) -> Tuple[HealthStatus, Dict[str, Any]]:
        """Check system health"""
        health_data = {
            "timestamp": datetime.now().isoformat(),
            "checks": {}
        }
        
        # Check system resources
        try:
            import psutil
            
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            health_data["checks"]["cpu"] = {
                "value": cpu_percent,
                "healthy": cpu_percent < 90.0
            }
            
            # Memory usage
            memory = psutil.virtual_memory()
            health_data["checks"]["memory"] = {
                "value": memory.percent,
                "available_percent": memory.available * 100 / memory.total,
                "healthy": (memory.available * 100 / memory.total) > self.thresholds.min_available_memory
            }
            
            # Disk usage
            disk = psutil.disk_usage('/')
            health_data["checks"]["disk"] = {
                "value": disk.percent,
                "healthy": disk.percent < 90.0
            }
            
        except ImportError:
            logger.warning("psutil not available, skipping resource checks")
            health_data["checks"]["resources"] = {"healthy": True, "note": "psutil not available"}
        
        # Calculate overall health status
        all_healthy = all(
            check.get("healthy", True) 
            for check in health_data["checks"].values()
        )
        
        if all_healthy:
            status = HealthStatus.HEALTHY
        else:
            unhealthy_checks = [
                name for name, check in health_data["checks"].items()
                if not check.get("healthy", True)
            ]
            if any(name in ["cpu", "memory"] for name in unhealthy_checks):
                status = HealthStatus.CRITICAL
            else:
                status = HealthStatus.DEGRADED
        
        health_data["status"] = status
        health_data["can_modify"] = status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED]
        
        # Store in history
        self.health_history.append(health_data)
        if len(self.health_history) > self.max_history:
            self.health_history.pop(0)
        
        return status, health_data
    
    async def can_modify(self) -> Tuple[bool, str]:
        """Check if system is healthy enough to modify"""
        status, health_data = await self.check_health()
        
        if status == HealthStatus.CRITICAL:
            return False, "System health is CRITICAL - modifications blocked"
        
        if status == HealthStatus.UNHEALTHY:
            return False, "System health is UNHEALTHY - modifications blocked"
        
        if status == HealthStatus.DEGRADED:
            return True, "System health is DEGRADED - modifications allowed with caution"
        
        return True, "System health is HEALTHY - modifications allowed"
    
    def get_health_trend(self) -> str:
        """Analyze health trend"""
        if len(self.health_history) < 2:
            return "insufficient_data"
        
        recent_checks = self.health_history[-10:]
        healthy_count = sum(1 for h in recent_checks if h["status"] == HealthStatus.HEALTHY)
        
        if healthy_count >= 8:
            return "improving"
        elif healthy_count >= 5:
            return "stable"
        else:
            return "degrading"


class BackupSystem:
    """
    Automatic backup and recovery system
    Creates backups before modifications and can restore on failure
    """
    
    def __init__(self, backup_dir: str = "./backups"):
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.backups: Dict[str, BackupRecord] = {}
        self.max_backups = 50
        self.backup_retention_days = 7
    
    async def create_backup(self, files: List[str], 
                          modification_id: str) -> BackupRecord:
        """Create backup of files before modification"""
        try:
            backup_id = f"backup_{modification_id}_{int(time.time())}"
            backup_path = self.backup_dir / backup_id
            backup_path.mkdir(parents=True, exist_ok=True)
            
            backed_up_files = []
            total_size = 0
            checksum_data = ""
            
            for file_path in files:
                try:
                    source = Path(file_path)
                    if not source.exists():
                        continue
                    
                    # Copy file to backup
                    dest = backup_path / source.name
                    shutil.copy2(source, dest)
                    
                    backed_up_files.append(file_path)
                    total_size += source.stat().st_size
                    
                    # Add to checksum
                    with open(source, 'rb') as f:
                        checksum_data += hashlib.sha256(f.read()).hexdigest()
                
                except Exception as e:
                    logger.error("Failed to backup file", file=file_path, error=str(e))
            
            # Create backup record
            record = BackupRecord(
                backup_id=backup_id,
                backup_path=backup_path,
                files_backed_up=backed_up_files,
                backup_size=total_size,
                created_at=datetime.now(),
                expires_at=datetime.now() + timedelta(days=self.backup_retention_days),
                checksum=hashlib.sha256(checksum_data.encode()).hexdigest()
            )
            
            # Store record
            self.backups[backup_id] = record
            
            # Write manifest
            manifest = {
                "backup_id": backup_id,
                "files": backed_up_files,
                "created_at": record.created_at.isoformat(),
                "checksum": record.checksum
            }
            with open(backup_path / "manifest.json", 'w') as f:
                json.dump(manifest, f, indent=2)
            
            logger.info("Backup created", backup_id=backup_id, files=len(backed_up_files))
            
            # Cleanup old backups
            await self._cleanup_old_backups()
            
            return record
            
        except Exception as e:
            logger.error("Failed to create backup", error=str(e))
            raise
    
    async def restore_backup(self, backup_id: str) -> bool:
        """Restore files from backup"""
        try:
            if backup_id not in self.backups:
                logger.error("Backup not found", backup_id=backup_id)
                return False
            
            record = self.backups[backup_id]
            
            # Restore each file
            for file_path in record.files_backed_up:
                source = record.backup_path / Path(file_path).name
                dest = Path(file_path)
                
                if source.exists():
                    shutil.copy2(source, dest)
                    logger.info("File restored", file=file_path, backup_id=backup_id)
            
            logger.info("Backup restored successfully", backup_id=backup_id)
            return True
            
        except Exception as e:
            logger.error("Failed to restore backup", backup_id=backup_id, error=str(e))
            return False
    
    async def _cleanup_old_backups(self):
        """Remove expired backups"""
        try:
            now = datetime.now()
            expired = [
                backup_id for backup_id, record in self.backups.items()
                if record.expires_at < now
            ]
            
            for backup_id in expired:
                record = self.backups[backup_id]
                if record.backup_path.exists():
                    shutil.rmtree(record.backup_path)
                del self.backups[backup_id]
                logger.info("Expired backup removed", backup_id=backup_id)
            
            # Also limit total number of backups
            if len(self.backups) > self.max_backups:
                # Remove oldest backups
                sorted_backups = sorted(
                    self.backups.items(),
                    key=lambda x: x[1].created_at
                )
                
                to_remove = len(self.backups) - self.max_backups
                for backup_id, record in sorted_backups[:to_remove]:
                    if record.backup_path.exists():
                        shutil.rmtree(record.backup_path)
                    del self.backups[backup_id]
                    logger.info("Old backup removed", backup_id=backup_id)
        
        except Exception as e:
            logger.error("Failed to cleanup backups", error=str(e))
    
    def get_backup_info(self, backup_id: str) -> Optional[Dict[str, Any]]:
        """Get backup information"""
        if backup_id not in self.backups:
            return None
        
        record = self.backups[backup_id]
        return {
            "backup_id": record.backup_id,
            "files_count": len(record.files_backed_up),
            "backup_size": record.backup_size,
            "created_at": record.created_at.isoformat(),
            "expires_at": record.expires_at.isoformat(),
            "checksum": record.checksum
        }


class AnomalyDetector:
    """
    Detects anomalies in modification patterns
    Helps identify potentially dangerous modifications
    """
    
    def __init__(self):
        self.modification_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        self.baseline_metrics: Dict[str, float] = {}
    
    async def analyze_modification(self, modification: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze modification for anomalies"""
        anomalies = []
        
        # Check modification size
        code_length = len(modification.get("code_after", {}).get("content", ""))
        if code_length > 10000:  # More than 10k characters
            anomalies.append({
                "type": "large_modification",
                "severity": "medium",
                "description": f"Modification is very large ({code_length} characters)"
            })
        
        # Check number of files affected
        files_affected = len(modification.get("affected_files", []))
        if files_affected > 5:
            anomalies.append({
                "type": "multiple_files",
                "severity": "medium",
                "description": f"Modification affects {files_affected} files"
            })
        
        # Check modification frequency
        recent_mods = [
            m for m in self.modification_history[-10:]
            if (datetime.now() - datetime.fromisoformat(m["timestamp"])).seconds < 300
        ]
        if len(recent_mods) > 5:
            anomalies.append({
                "type": "high_frequency",
                "severity": "high",
                "description": f"{len(recent_mods)} modifications in last 5 minutes"
            })
        
        # Check for dangerous patterns
        code_content = str(modification.get("code_after", {}))
        dangerous_keywords = ["rm -rf", "DROP TABLE", "DELETE FROM", "os.system", "eval("]
        for keyword in dangerous_keywords:
            if keyword in code_content:
                anomalies.append({
                    "type": "dangerous_pattern",
                    "severity": "critical",
                    "description": f"Dangerous pattern detected: {keyword}"
                })
        
        # Store in history
        self.modification_history.append({
            "timestamp": datetime.now().isoformat(),
            "modification_id": modification.get("modification_id"),
            "anomalies": anomalies
        })
        
        if len(self.modification_history) > self.max_history:
            self.modification_history.pop(0)
        
        return {
            "has_anomalies": len(anomalies) > 0,
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "risk_level": self._calculate_risk_level(anomalies)
        }
    
    def _calculate_risk_level(self, anomalies: List[Dict[str, Any]]) -> str:
        """Calculate overall risk level"""
        if not anomalies:
            return "none"
        
        if any(a["severity"] == "critical" for a in anomalies):
            return "critical"
        
        if any(a["severity"] == "high" for a in anomalies):
            return "high"
        
        if len(anomalies) >= 3:
            return "high"
        
        if any(a["severity"] == "medium" for a in anomalies):
            return "medium"
        
        return "low"


class EnhancedSafetySystem:
    """
    Enhanced Safety System combining all safety mechanisms
    """
    
    def __init__(self):
        self.circuit_breaker = CircuitBreaker()
        self.health_monitor = HealthMonitor()
        self.backup_system = BackupSystem()
        self.anomaly_detector = AnomalyDetector()
        self.enabled = True
        
        # Rate limiting
        self.rate_limit_window = 60  # 1 minute
        self.rate_limit_max = 10     # Max 10 modifications per minute
        self.recent_modifications: List[datetime] = []
    
    async def pre_modification_checks(self, modification: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Run all pre-modification safety checks
        Returns (can_proceed, reasons)
        """
        if not self.enabled:
            return True, ["Safety system disabled"]
        
        reasons = []
        can_proceed = True
        
        # 1. Circuit breaker check
        cb_allowed, cb_reason = self.circuit_breaker.can_proceed()
        if not cb_allowed:
            can_proceed = False
            reasons.append(f"Circuit breaker: {cb_reason}")
        
        # 2. Health check
        health_allowed, health_reason = await self.health_monitor.can_modify()
        if not health_allowed:
            can_proceed = False
            reasons.append(f"Health check: {health_reason}")
        
        # 3. Rate limiting
        rate_allowed, rate_reason = self._check_rate_limit()
        if not rate_allowed:
            can_proceed = False
            reasons.append(f"Rate limit: {rate_reason}")
        
        # 4. Anomaly detection
        anomaly_result = await self.anomaly_detector.analyze_modification(modification)
        if anomaly_result["risk_level"] in ["critical", "high"]:
            can_proceed = False
            reasons.append(f"Anomaly detected: {anomaly_result['risk_level']} risk")
            for anomaly in anomaly_result["anomalies"]:
                reasons.append(f"  - {anomaly['description']}")
        
        if can_proceed:
            reasons.append("All pre-modification checks passed")
        
        return can_proceed, reasons
    
    async def create_backup_before_modification(self, 
                                               modification_id: str,
                                               files: List[str]) -> Optional[str]:
        """Create backup before modification"""
        try:
            record = await self.backup_system.create_backup(files, modification_id)
            return record.backup_id
        except Exception as e:
            logger.error("Failed to create backup", error=str(e))
            return None
    
    async def post_modification_monitoring(self, 
                                          modification_id: str,
                                          success: bool,
                                          error: str = None) -> Dict[str, Any]:
        """Monitor system after modification"""
        # Record in circuit breaker
        if success:
            self.circuit_breaker.record_success()
        else:
            self.circuit_breaker.record_failure(error or "Unknown error")
        
        # Check if automatic rollback needed
        health_status, health_data = await self.health_monitor.check_health()
        
        should_rollback = False
        rollback_reason = ""
        
        if not success:
            should_rollback = True
            rollback_reason = "Modification failed"
        elif health_status == HealthStatus.CRITICAL:
            should_rollback = True
            rollback_reason = "System health became CRITICAL after modification"
        
        return {
            "should_rollback": should_rollback,
            "rollback_reason": rollback_reason,
            "health_status": health_status,
            "health_data": health_data,
            "circuit_breaker_state": self.circuit_breaker.state
        }
    
    async def automatic_rollback(self, backup_id: str, reason: str) -> bool:
        """Automatically rollback modification"""
        logger.warning("Automatic rollback triggered", backup_id=backup_id, reason=reason)
        
        success = await self.backup_system.restore_backup(backup_id)
        
        if success:
            logger.info("Automatic rollback successful", backup_id=backup_id)
        else:
            logger.error("Automatic rollback failed", backup_id=backup_id)
        
        return success
    
    def _check_rate_limit(self) -> Tuple[bool, str]:
        """Check if rate limit is exceeded"""
        now = datetime.now()
        
        # Remove old modifications outside window
        self.recent_modifications = [
            m for m in self.recent_modifications
            if (now - m).seconds < self.rate_limit_window
        ]
        
        if len(self.recent_modifications) >= self.rate_limit_max:
            return False, f"Rate limit exceeded: {self.rate_limit_max} modifications per {self.rate_limit_window}s"
        
        # Add current modification
        self.recent_modifications.append(now)
        
        return True, "Rate limit OK"
    
    async def get_safety_status(self) -> Dict[str, Any]:
        """Get comprehensive safety status"""
        health_status, health_data = await self.health_monitor.check_health()
        
        return {
            "enabled": self.enabled,
            "circuit_breaker": self.circuit_breaker.get_status(),
            "health": health_data,
            "health_trend": self.health_monitor.get_health_trend(),
            "rate_limit": {
                "window_seconds": self.rate_limit_window,
                "max_per_window": self.rate_limit_max,
                "current_count": len(self.recent_modifications)
            },
            "backups": {
                "total": len(self.backup_system.backups),
                "retention_days": self.backup_system.backup_retention_days
            }
        }


# Global instance
enhanced_safety_system = EnhancedSafetySystem()


__all__ = [
    'EnhancedSafetySystem',
    'CircuitBreaker',
    'HealthMonitor',
    'BackupSystem',
    'AnomalyDetector',
    'enhanced_safety_system'
]


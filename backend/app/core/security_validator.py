"""
Security Validator

This module provides comprehensive security validation for the Ethical AI system,
including code security analysis, configuration validation, and threat detection.
"""

import re
import hashlib
import structlog
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json
import secrets
import base64

from app.core.redis import get_redis_client
from app.core.ethical_ai_core import ethical_ai_core

logger = structlog.get_logger(__name__)

class SecurityLevel(Enum):
    """Security validation levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ThreatType(Enum):
    """Types of security threats"""
    SQL_INJECTION = "sql_injection"
    XSS = "cross_site_scripting"
    CSRF = "cross_site_request_forgery"
    PATH_TRAVERSAL = "path_traversal"
    COMMAND_INJECTION = "command_injection"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    SECRET_EXPOSURE = "secret_exposure"
    WEAK_AUTHENTICATION = "weak_authentication"
    INSECURE_COMMUNICATION = "insecure_communication"
    DATA_EXPOSURE = "data_exposure"

class ValidationResult(Enum):
    """Validation results"""
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"
    CRITICAL = "critical"

@dataclass
class SecurityIssue:
    """Security issue representation"""
    issue_id: str
    threat_type: ThreatType
    severity: SecurityLevel
    description: str
    location: Optional[str] = None
    line_number: Optional[int] = None
    code_snippet: Optional[str] = None
    remediation: Optional[str] = None
    cve_references: List[str] = field(default_factory=list)
    confidence: float = 1.0

@dataclass
class SecurityValidationReport:
    """Security validation report"""
    validation_id: str
    timestamp: datetime
    overall_score: float
    validation_result: ValidationResult
    issues_found: List[SecurityIssue]
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)

class SecurityValidator:
    """Comprehensive security validation system"""
    
    def __init__(self):
        self.redis_client = get_redis_client()
        self.threat_patterns = self._initialize_threat_patterns()
        self.secret_patterns = self._initialize_secret_patterns()
        self.validation_cache: Dict[str, SecurityValidationReport] = {}
        
    def _initialize_threat_patterns(self) -> Dict[ThreatType, List[str]]:
        """Initialize threat detection patterns"""
        return {
            ThreatType.SQL_INJECTION: [
                r"(?i)(union\s+select|drop\s+table|delete\s+from|insert\s+into)",
                r"(?i)(or\s+1\s*=\s*1|and\s+1\s*=\s*1)",
                r"(?i)(exec\s*\(|execute\s*\()",
                r"(?i)(sp_executesql|xp_cmdshell)"
            ],
            ThreatType.XSS: [
                r"(?i)(<script[^>]*>.*?</script>)",
                r"(?i)(javascript\s*:)",
                r"(?i)(onload\s*=|onclick\s*=|onerror\s*=)",
                r"(?i)(document\.write|innerHTML\s*=)",
                r"(?i)(eval\s*\()"
            ],
            ThreatType.PATH_TRAVERSAL: [
                r"(\.\.\/|\.\.\\\\)",
                r"(?i)(\.\.%2f|\.\.%5c)",
                r"(?i)(%2e%2e%2f|%2e%2e%5c)",
                r"(?i)(\.\.%252f|\.\.%255c)"
            ],
            ThreatType.COMMAND_INJECTION: [
                r"(?i)(system\s*\(|exec\s*\(|shell_exec\s*\()",
                r"(?i)(cmd\.exe|powershell|bash|sh)",
                r"(?i)(&&|\|\|)",
                r"(?i)(;.*?$)"
            ],
            ThreatType.INSECURE_DESERIALIZATION: [
                r"(?i)(pickle\.loads|unserialize\s*\(|ObjectInputStream)",
                r"(?i)(yaml\.load|json\.loads.*__import__)",
                r"(?i)(eval\s*\()"
            ]
        }
    
    def _initialize_secret_patterns(self) -> Dict[str, List[str]]:
        """Initialize secret detection patterns"""
        return {
            "api_keys": [
                r"(?i)(api[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?)",
                r"(?i)(secret[_-]?key\s*[=:]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?)",
                r"(?i)(access[_-]?token\s*[=:]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?)"
            ],
            "passwords": [
                r"(?i)(password\s*[=:]\s*['\"]?[^'\"]{8,}['\"]?)",
                r"(?i)(pwd\s*[=:]\s*['\"]?[^'\"]{8,}['\"]?)",
                r"(?i)(pass\s*[=:]\s*['\"]?[^'\"]{8,}['\"]?)"
            ],
            "database_credentials": [
                r"(?i)(database[_-]?url\s*[=:]\s*['\"]?[^'\"]+['\"]?)",
                r"(?i)(db[_-]?password\s*[=:]\s*['\"]?[^'\"]{8,}['\"]?)",
                r"(?i)(connection[_-]?string\s*[=:]\s*['\"]?[^'\"]+['\"]?)"
            ],
            "jwt_secrets": [
                r"(?i)(jwt[_-]?secret\s*[=:]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?)",
                r"(?i)(token[_-]?secret\s*[=:]\s*['\"]?[a-zA-Z0-9]{20,}['\"]?)"
            ]
        }
    
    async def validate_code_security(self, code: str, language: str = "python") -> SecurityValidationReport:
        """Validate code for security issues"""
        try:
            validation_id = f"code_{hashlib.md5(code.encode()).hexdigest()[:8]}"
            
            # Check cache first
            cache_key = f"security_validation:{validation_id}"
            cached_result = await self.redis_client.get(cache_key)
            if cached_result:
                cached_data = json.loads(cached_result)
                return SecurityValidationReport(**cached_data)
            
            issues_found = []
            
            # Check for SQL injection
            sql_issues = await self._check_sql_injection(code)
            issues_found.extend(sql_issues)
            
            # Check for XSS vulnerabilities
            xss_issues = await self._check_xss_vulnerabilities(code)
            issues_found.extend(xss_issues)
            
            # Check for path traversal
            path_traversal_issues = await self._check_path_traversal(code)
            issues_found.extend(path_traversal_issues)
            
            # Check for command injection
            command_injection_issues = await self._check_command_injection(code)
            issues_found.extend(command_injection_issues)
            
            # Check for insecure deserialization
            deserialization_issues = await self._check_insecure_deserialization(code)
            issues_found.extend(deserialization_issues)
            
            # Check for secret exposure
            secret_issues = await self._check_secret_exposure(code)
            issues_found.extend(secret_issues)
            
            # Calculate overall score
            overall_score = self._calculate_security_score(issues_found)
            validation_result = self._determine_validation_result(overall_score, issues_found)
            
            # Generate recommendations
            recommendations = self._generate_security_recommendations(issues_found)
            
            # Create report
            report = SecurityValidationReport(
                validation_id=validation_id,
                timestamp=datetime.now(),
                overall_score=overall_score,
                validation_result=validation_result,
                issues_found=issues_found,
                recommendations=recommendations,
                metadata={
                    "language": language,
                    "code_length": len(code),
                    "lines_analyzed": len(code.split('\n'))
                }
            )
            
            # Cache result
            await self._cache_validation_result(cache_key, report)
            
            logger.info("Code security validation completed", 
                       validation_id=validation_id,
                       overall_score=overall_score,
                       issues_count=len(issues_found))
            
            return report
            
        except Exception as e:
            logger.error("Code security validation failed", error=str(e))
            raise
    
    async def _check_sql_injection(self, code: str) -> List[SecurityIssue]:
        """Check for SQL injection vulnerabilities"""
        issues = []
        patterns = self.threat_patterns[ThreatType.SQL_INJECTION]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    issue = SecurityIssue(
                        issue_id=f"sql_injection_{i}_{match.start()}",
                        threat_type=ThreatType.SQL_INJECTION,
                        severity=SecurityLevel.HIGH,
                        description="Potential SQL injection vulnerability detected",
                        location=f"Line {i}",
                        line_number=i,
                        code_snippet=line.strip(),
                        remediation="Use parameterized queries or prepared statements",
                        confidence=0.9
                    )
                    issues.append(issue)
        
        return issues
    
    async def _check_xss_vulnerabilities(self, code: str) -> List[SecurityIssue]:
        """Check for XSS vulnerabilities"""
        issues = []
        patterns = self.threat_patterns[ThreatType.XSS]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    issue = SecurityIssue(
                        issue_id=f"xss_{i}_{match.start()}",
                        threat_type=ThreatType.XSS,
                        severity=SecurityLevel.HIGH,
                        description="Potential XSS vulnerability detected",
                        location=f"Line {i}",
                        line_number=i,
                        code_snippet=line.strip(),
                        remediation="Sanitize user input and use proper output encoding",
                        confidence=0.8
                    )
                    issues.append(issue)
        
        return issues
    
    async def _check_path_traversal(self, code: str) -> List[SecurityIssue]:
        """Check for path traversal vulnerabilities"""
        issues = []
        patterns = self.threat_patterns[ThreatType.PATH_TRAVERSAL]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    issue = SecurityIssue(
                        issue_id=f"path_traversal_{i}_{match.start()}",
                        threat_type=ThreatType.PATH_TRAVERSAL,
                        severity=SecurityLevel.MEDIUM,
                        description="Potential path traversal vulnerability detected",
                        location=f"Line {i}",
                        line_number=i,
                        code_snippet=line.strip(),
                        remediation="Validate and sanitize file paths",
                        confidence=0.7
                    )
                    issues.append(issue)
        
        return issues
    
    async def _check_command_injection(self, code: str) -> List[SecurityIssue]:
        """Check for command injection vulnerabilities"""
        issues = []
        patterns = self.threat_patterns[ThreatType.COMMAND_INJECTION]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    issue = SecurityIssue(
                        issue_id=f"command_injection_{i}_{match.start()}",
                        threat_type=ThreatType.COMMAND_INJECTION,
                        severity=SecurityLevel.CRITICAL,
                        description="Potential command injection vulnerability detected",
                        location=f"Line {i}",
                        line_number=i,
                        code_snippet=line.strip(),
                        remediation="Avoid executing user input as system commands",
                        confidence=0.9
                    )
                    issues.append(issue)
        
        return issues
    
    async def _check_insecure_deserialization(self, code: str) -> List[SecurityIssue]:
        """Check for insecure deserialization vulnerabilities"""
        issues = []
        patterns = self.threat_patterns[ThreatType.INSECURE_DESERIALIZATION]
        
        for i, line in enumerate(code.split('\n'), 1):
            for pattern in patterns:
                matches = re.finditer(pattern, line)
                for match in matches:
                    issue = SecurityIssue(
                        issue_id=f"deserialization_{i}_{match.start()}",
                        threat_type=ThreatType.INSECURE_DESERIALIZATION,
                        severity=SecurityLevel.HIGH,
                        description="Potential insecure deserialization vulnerability detected",
                        location=f"Line {i}",
                        line_number=i,
                        code_snippet=line.strip(),
                        remediation="Use safe deserialization methods or validate input",
                        confidence=0.8
                    )
                    issues.append(issue)
        
        return issues
    
    async def _check_secret_exposure(self, code: str) -> List[SecurityIssue]:
        """Check for secret exposure"""
        issues = []
        
        for secret_type, patterns in self.secret_patterns.items():
            for i, line in enumerate(code.split('\n'), 1):
                for pattern in patterns:
                    matches = re.finditer(pattern, line)
                    for match in matches:
                        issue = SecurityIssue(
                            issue_id=f"secret_{secret_type}_{i}_{match.start()}",
                            threat_type=ThreatType.SECRET_EXPOSURE,
                            severity=SecurityLevel.CRITICAL,
                            description=f"Potential {secret_type.replace('_', ' ')} exposure detected",
                            location=f"Line {i}",
                            line_number=i,
                            code_snippet=line.strip(),
                            remediation="Move secrets to environment variables or secure configuration",
                            confidence=0.95
                        )
                        issues.append(issue)
        
        return issues
    
    def _calculate_security_score(self, issues: List[SecurityIssue]) -> float:
        """Calculate overall security score"""
        if not issues:
            return 100.0
        
        score = 100.0
        for issue in issues:
            if issue.severity == SecurityLevel.CRITICAL:
                score -= 25
            elif issue.severity == SecurityLevel.HIGH:
                score -= 15
            elif issue.severity == SecurityLevel.MEDIUM:
                score -= 10
            elif issue.severity == SecurityLevel.LOW:
                score -= 5
        
        return max(0.0, score)
    
    def _determine_validation_result(self, score: float, issues: List[SecurityIssue]) -> ValidationResult:
        """Determine validation result based on score and issues"""
        critical_issues = [i for i in issues if i.severity == SecurityLevel.CRITICAL]
        high_issues = [i for i in issues if i.severity == SecurityLevel.HIGH]
        
        if critical_issues:
            return ValidationResult.CRITICAL
        elif score < 50 or len(high_issues) > 5:
            return ValidationResult.FAIL
        elif score < 80 or len(high_issues) > 2:
            return ValidationResult.WARNING
        else:
            return ValidationResult.PASS
    
    def _generate_security_recommendations(self, issues: List[SecurityIssue]) -> List[str]:
        """Generate security recommendations based on issues found"""
        recommendations = []
        
        # Collect unique remediation advice
        remediations = set()
        for issue in issues:
            if issue.remediation:
                remediations.add(issue.remediation)
        
        recommendations.extend(list(remediations))
        
        # Add general recommendations
        if not recommendations:
            recommendations.append("No specific security issues found - maintain current security practices")
        
        recommendations.extend([
            "Regular security audits and penetration testing",
            "Implement automated security scanning in CI/CD pipeline",
            "Keep dependencies updated and patch security vulnerabilities",
            "Use security headers and HTTPS for web applications",
            "Implement proper authentication and authorization mechanisms"
        ])
        
        return recommendations
    
    async def _cache_validation_result(self, cache_key: str, report: SecurityValidationReport):
        """Cache validation result in Redis"""
        try:
            cache_data = {
                "validation_id": report.validation_id,
                "timestamp": report.timestamp.isoformat(),
                "overall_score": report.overall_score,
                "validation_result": report.validation_result.value,
                "issues_found": [
                    {
                        "issue_id": issue.issue_id,
                        "threat_type": issue.threat_type.value,
                        "severity": issue.severity.value,
                        "description": issue.description,
                        "location": issue.location,
                        "line_number": issue.line_number,
                        "code_snippet": issue.code_snippet,
                        "remediation": issue.remediation,
                        "confidence": issue.confidence
                    }
                    for issue in report.issues_found
                ],
                "recommendations": report.recommendations,
                "metadata": report.metadata
            }
            
            await self.redis_client.set(
                cache_key,
                json.dumps(cache_data, default=str),
                ex=3600  # Cache for 1 hour
            )
            
        except Exception as e:
            logger.error("Failed to cache validation result", error=str(e))
    
    async def validate_configuration_security(self, config: Dict[str, Any]) -> SecurityValidationReport:
        """Validate configuration for security issues"""
        try:
            validation_id = f"config_{hashlib.md5(str(config).encode()).hexdigest()[:8]}"
            
            issues_found = []
            
            # Check for hardcoded secrets in configuration
            config_str = json.dumps(config, indent=2)
            secret_issues = await self._check_secret_exposure(config_str)
            issues_found.extend(secret_issues)
            
            # Check for insecure configurations
            insecure_configs = await self._check_insecure_configurations(config)
            issues_found.extend(insecure_configs)
            
            # Calculate overall score
            overall_score = self._calculate_security_score(issues_found)
            validation_result = self._determine_validation_result(overall_score, issues_found)
            
            # Generate recommendations
            recommendations = self._generate_security_recommendations(issues_found)
            
            # Create report
            report = SecurityValidationReport(
                validation_id=validation_id,
                timestamp=datetime.now(),
                overall_score=overall_score,
                validation_result=validation_result,
                issues_found=issues_found,
                recommendations=recommendations,
                metadata={
                    "config_keys": list(config.keys()),
                    "config_size": len(config_str)
                }
            )
            
            logger.info("Configuration security validation completed", 
                       validation_id=validation_id,
                       overall_score=overall_score,
                       issues_count=len(issues_found))
            
            return report
            
        except Exception as e:
            logger.error("Configuration security validation failed", error=str(e))
            raise
    
    async def _check_insecure_configurations(self, config: Dict[str, Any]) -> List[SecurityIssue]:
        """Check for insecure configuration settings"""
        issues = []
        
        # Check for debug mode in production
        if config.get("DEBUG") == True or config.get("debug") == True:
            issues.append(SecurityIssue(
                issue_id="debug_mode_enabled",
                threat_type=ThreatType.DATA_EXPOSURE,
                severity=SecurityLevel.MEDIUM,
                description="Debug mode is enabled",
                remediation="Disable debug mode in production environments",
                confidence=1.0
            ))
        
        # Check for weak authentication settings
        if config.get("AUTH_REQUIRED") == False or config.get("auth_required") == False:
            issues.append(SecurityIssue(
                issue_id="auth_disabled",
                threat_type=ThreatType.WEAK_AUTHENTICATION,
                severity=SecurityLevel.HIGH,
                description="Authentication is disabled",
                remediation="Enable authentication for all protected endpoints",
                confidence=1.0
            ))
        
        # Check for insecure communication
        if config.get("HTTPS_ONLY") == False or config.get("https_only") == False:
            issues.append(SecurityIssue(
                issue_id="insecure_communication",
                threat_type=ThreatType.INSECURE_COMMUNICATION,
                severity=SecurityLevel.MEDIUM,
                description="HTTPS is not enforced",
                remediation="Enforce HTTPS for all communications",
                confidence=1.0
            ))
        
        return issues
    
    async def generate_security_token(self, length: int = 32) -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(length)
    
    async def hash_sensitive_data(self, data: str) -> str:
        """Hash sensitive data using secure hashing"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', data.encode(), salt.encode(), 100000)
        return f"{salt}:{hash_obj.hex()}"
    
    async def verify_hash(self, data: str, hash_value: str) -> bool:
        """Verify hashed sensitive data"""
        try:
            salt, hash_hex = hash_value.split(':')
            hash_obj = hashlib.pbkdf2_hmac('sha256', data.encode(), salt.encode(), 100000)
            return hash_obj.hex() == hash_hex
        except:
            return False
    
    async def get_security_metrics(self) -> Dict[str, Any]:
        """Get security validation metrics"""
        try:
            # Get cached validation results
            cache_keys = await self.redis_client.keys("security_validation:*")
            
            total_validations = len(cache_keys)
            passed_validations = 0
            failed_validations = 0
            critical_issues = 0
            
            for key in cache_keys:
                cached_data = await self.redis_client.get(key)
                if cached_data:
                    data = json.loads(cached_data)
                    if data.get("validation_result") == "pass":
                        passed_validations += 1
                    elif data.get("validation_result") == "critical":
                        failed_validations += 1
                        critical_issues += len([i for i in data.get("issues_found", []) 
                                              if i.get("severity") == "critical"])
            
            return {
                "total_validations": total_validations,
                "passed_validations": passed_validations,
                "failed_validations": failed_validations,
                "critical_issues": critical_issues,
                "success_rate": (passed_validations / total_validations * 100) if total_validations > 0 else 0
            }
            
        except Exception as e:
            logger.error("Failed to get security metrics", error=str(e))
            return {}

# Global instance
security_validator = SecurityValidator()

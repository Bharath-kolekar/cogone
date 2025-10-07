"""
Advanced Compliance Engine - Multi-dimensional compliance checking and enforcement
"""

import structlog
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import uuid
import json

logger = structlog.get_logger()


class ComplianceLevel(str, Enum):
    """Compliance level definitions"""
    FULLY_COMPLIANT = "fully_compliant"
    MOSTLY_COMPLIANT = "mostly_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"
    CRITICAL_NON_COMPLIANT = "critical_non_compliant"


class ComplianceCategory(str, Enum):
    """Compliance categories"""
    ETHICAL = "ethical"
    SECURITY = "security"
    PERFORMANCE = "performance"
    QUALITY = "quality"
    BUSINESS = "business"
    REGULATORY = "regulatory"
    OPERATIONAL = "operational"


@dataclass
class ComplianceResult:
    """Compliance checking result"""
    category: ComplianceCategory
    level: ComplianceLevel
    score: float
    details: Dict[str, Any]
    violations: List[str]
    recommendations: List[str]
    checked_at: datetime
    next_check: datetime


@dataclass
class ComplianceReport:
    """Comprehensive compliance report"""
    overall_score: float
    overall_level: ComplianceLevel
    category_results: Dict[ComplianceCategory, ComplianceResult]
    critical_issues: List[str]
    recommendations: List[str]
    generated_at: datetime
    valid_until: datetime


class ComplianceEngine:
    """Advanced compliance checking and enforcement"""
    
    def __init__(self):
        self.compliance_rules = {}
        self.compliance_history = []
        self.active_checks = {}
        
    async def initialize(self):
        """Initialize compliance engine"""
        await self._load_compliance_rules()
        logger.info("Compliance engine initialized")
    
    async def _load_compliance_rules(self):
        """Load compliance rules from configuration"""
        self.compliance_rules = {
            ComplianceCategory.ETHICAL: {
                'principles': ['non_harm', 'truthfulness', 'fairness', 'autonomy', 'beneficence', 'accountability'],
                'thresholds': {'min_score': 95.0, 'critical_threshold': 80.0},
                'enforcement': 'strict'
            },
            ComplianceCategory.SECURITY: {
                'requirements': ['encryption', 'access_control', 'vulnerability_scan', 'audit_trail'],
                'thresholds': {'min_score': 98.0, 'critical_threshold': 90.0},
                'enforcement': 'strict'
            },
            ComplianceCategory.PERFORMANCE: {
                'metrics': ['response_time', 'throughput', 'resource_usage', 'error_rate'],
                'thresholds': {'min_score': 90.0, 'critical_threshold': 75.0},
                'enforcement': 'strict'
            },
            ComplianceCategory.QUALITY: {
                'standards': ['code_quality', 'documentation', 'testing', 'maintainability'],
                'thresholds': {'min_score': 85.0, 'critical_threshold': 70.0},
                'enforcement': 'strict'
            },
            ComplianceCategory.BUSINESS: {
                'criteria': ['roi', 'stakeholder_satisfaction', 'business_value', 'risk_management'],
                'thresholds': {'min_score': 80.0, 'critical_threshold': 60.0},
                'enforcement': 'moderate'
            },
            ComplianceCategory.REGULATORY: {
                'standards': ['gdpr', 'sox', 'hipaa', 'pci_dss', 'iso27001'],
                'thresholds': {'min_score': 100.0, 'critical_threshold': 95.0},
                'enforcement': 'strict'
            },
            ComplianceCategory.OPERATIONAL: {
                'aspects': ['uptime', 'reliability', 'scalability', 'monitoring'],
                'thresholds': {'min_score': 95.0, 'critical_threshold': 85.0},
                'enforcement': 'strict'
            }
        }
    
    async def check_compliance(self, operation: str, context: Dict[str, Any]) -> ComplianceReport:
        """Perform comprehensive compliance checking"""
        try:
            category_results = {}
            critical_issues = []
            all_recommendations = []
            
            # Check each compliance category
            for category in ComplianceCategory:
                result = await self._check_category_compliance(category, operation, context)
                category_results[category] = result
                
                if result.level in [ComplianceLevel.NON_COMPLIANT, ComplianceLevel.CRITICAL_NON_COMPLIANT]:
                    critical_issues.extend(result.violations)
                
                all_recommendations.extend(result.recommendations)
            
            # Calculate overall compliance
            overall_score = self._calculate_overall_score(category_results)
            overall_level = self._determine_overall_level(overall_score, critical_issues)
            
            report = ComplianceReport(
                overall_score=overall_score,
                overall_level=overall_level,
                category_results=category_results,
                critical_issues=critical_issues,
                recommendations=list(set(all_recommendations)),
                generated_at=datetime.utcnow(),
                valid_until=datetime.utcnow() + timedelta(hours=1)
            )
            
            # Store in history
            self.compliance_history.append(report)
            
            logger.info("Compliance check completed", 
                       operation=operation,
                       overall_score=overall_score,
                       overall_level=overall_level.value,
                       critical_issues_count=len(critical_issues))
            
            return report
            
        except Exception as e:
            logger.error("Error in compliance checking", operation=operation, error=str(e))
            raise
    
    async def _check_category_compliance(self, category: ComplianceCategory, operation: str, context: Dict[str, Any]) -> ComplianceResult:
        """Check compliance for a specific category"""
        try:
            rules = self.compliance_rules.get(category, {})
            violations = []
            recommendations = []
            
            if category == ComplianceCategory.ETHICAL:
                score, violations, recommendations = await self._check_ethical_compliance(operation, context)
            elif category == ComplianceCategory.SECURITY:
                score, violations, recommendations = await self._check_security_compliance(operation, context)
            elif category == ComplianceCategory.PERFORMANCE:
                score, violations, recommendations = await self._check_performance_compliance(operation, context)
            elif category == ComplianceCategory.QUALITY:
                score, violations, recommendations = await self._check_quality_compliance(operation, context)
            elif category == ComplianceCategory.BUSINESS:
                score, violations, recommendations = await self._check_business_compliance(operation, context)
            elif category == ComplianceCategory.REGULATORY:
                score, violations, recommendations = await self._check_regulatory_compliance(operation, context)
            elif category == ComplianceCategory.OPERATIONAL:
                score, violations, recommendations = await self._check_operational_compliance(operation, context)
            else:
                score = 100.0
            
            level = self._determine_compliance_level(score, rules.get('thresholds', {}))
            
            return ComplianceResult(
                category=category,
                level=level,
                score=score,
                details={'operation': operation, 'context': context},
                violations=violations,
                recommendations=recommendations,
                checked_at=datetime.utcnow(),
                next_check=datetime.utcnow() + timedelta(minutes=30)
            )
            
        except Exception as e:
            logger.error(f"Error checking {category.value} compliance", error=str(e))
            return ComplianceResult(
                category=category,
                level=ComplianceLevel.NON_COMPLIANT,
                score=0.0,
                details={'error': str(e)},
                violations=[f"Error checking {category.value} compliance: {str(e)}"],
                recommendations=["Fix compliance checking error"],
                checked_at=datetime.utcnow(),
                next_check=datetime.utcnow() + timedelta(minutes=5)
            )
    
    async def _check_ethical_compliance(self, operation: str, context: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """Check ethical compliance"""
        violations = []
        recommendations = []
        score = 100.0
        
        try:
            # Check non-harm principle
            if not await self._check_non_harm_principle(operation, context):
                violations.append("Non-harm principle violation detected")
                score -= 20.0
                recommendations.append("Review operation for potential harm and implement safeguards")
            
            # Check truthfulness
            if not await self._check_truthfulness(operation, context):
                violations.append("Truthfulness principle violation detected")
                score -= 15.0
                recommendations.append("Ensure all information is accurate and transparent")
            
            # Check fairness
            if not await self._check_fairness(operation, context):
                violations.append("Fairness principle violation detected")
                score -= 15.0
                recommendations.append("Implement bias detection and fairness measures")
            
            # Check autonomy
            if not await self._check_autonomy(operation, context):
                violations.append("Autonomy principle violation detected")
                score -= 10.0
                recommendations.append("Ensure user control and choice in operations")
            
            # Check beneficence
            if not await self._check_beneficence(operation, context):
                violations.append("Beneficence principle violation detected")
                score -= 10.0
                recommendations.append("Optimize operations for user benefit")
            
            # Check accountability
            if not await self._check_accountability(operation, context):
                violations.append("Accountability principle violation detected")
                score -= 10.0
                recommendations.append("Implement comprehensive logging and audit trails")
            
            return max(0.0, score), violations, recommendations
            
        except Exception as e:
            logger.error("Error checking ethical compliance", error=str(e))
            return 0.0, [f"Ethical compliance check failed: {str(e)}"], ["Fix ethical compliance checking"]
    
    async def _check_security_compliance(self, operation: str, context: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """Check security compliance"""
        violations = []
        recommendations = []
        score = 100.0
        
        try:
            # Check encryption
            if not await self._check_encryption_compliance(operation, context):
                violations.append("Encryption compliance failure")
                score -= 25.0
                recommendations.append("Implement proper encryption for data at rest and in transit")
            
            # Check access control
            if not await self._check_access_control_compliance(operation, context):
                violations.append("Access control compliance failure")
                score -= 25.0
                recommendations.append("Implement proper authentication and authorization")
            
            # Check vulnerability scanning
            if not await self._check_vulnerability_scanning(operation, context):
                violations.append("Vulnerability scanning compliance failure")
                score -= 20.0
                recommendations.append("Implement regular vulnerability scanning")
            
            # Check audit trail
            if not await self._check_audit_trail_compliance(operation, context):
                violations.append("Audit trail compliance failure")
                score -= 15.0
                recommendations.append("Implement comprehensive audit logging")
            
            # Check data protection
            if not await self._check_data_protection_compliance(operation, context):
                violations.append("Data protection compliance failure")
                score -= 15.0
                recommendations.append("Implement data protection measures")
            
            return max(0.0, score), violations, recommendations
            
        except Exception as e:
            logger.error("Error checking security compliance", error=str(e))
            return 0.0, [f"Security compliance check failed: {str(e)}"], ["Fix security compliance checking"]
    
    async def _check_performance_compliance(self, operation: str, context: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """Check performance compliance"""
        violations = []
        recommendations = []
        score = 100.0
        
        try:
            # Check response time
            response_time = await self._get_response_time(operation, context)
            if response_time > 200:  # 200ms threshold
                violations.append(f"Response time {response_time}ms exceeds 200ms threshold")
                score -= 20.0
                recommendations.append("Optimize response time through caching and performance tuning")
            
            # Check throughput
            throughput = await self._get_throughput(operation, context)
            if throughput < 1000:  # 1000 RPS threshold
                violations.append(f"Throughput {throughput} RPS below 1000 RPS threshold")
                score -= 20.0
                recommendations.append("Scale resources to improve throughput")
            
            # Check resource usage
            cpu_usage = await self._get_cpu_usage(operation, context)
            memory_usage = await self._get_memory_usage(operation, context)
            
            if cpu_usage > 80:
                violations.append(f"CPU usage {cpu_usage}% exceeds 80% threshold")
                score -= 15.0
                recommendations.append("Optimize CPU usage or scale resources")
            
            if memory_usage > 85:
                violations.append(f"Memory usage {memory_usage}% exceeds 85% threshold")
                score -= 15.0
                recommendations.append("Optimize memory usage or scale resources")
            
            # Check error rate
            error_rate = await self._get_error_rate(operation, context)
            if error_rate > 0.1:  # 0.1% threshold
                violations.append(f"Error rate {error_rate}% exceeds 0.1% threshold")
                score -= 30.0
                recommendations.append("Investigate and fix error sources")
            
            return max(0.0, score), violations, recommendations
            
        except Exception as e:
            logger.error("Error checking performance compliance", error=str(e))
            return 0.0, [f"Performance compliance check failed: {str(e)}"], ["Fix performance compliance checking"]
    
    async def _check_quality_compliance(self, operation: str, context: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """Check quality compliance"""
        violations = []
        recommendations = []
        score = 100.0
        
        try:
            # Check code quality
            code_quality_score = await self._get_code_quality_score(operation, context)
            if code_quality_score < 90:
                violations.append(f"Code quality score {code_quality_score} below 90 threshold")
                score -= 25.0
                recommendations.append("Improve code quality through refactoring and best practices")
            
            # Check documentation coverage
            doc_coverage = await self._get_documentation_coverage(operation, context)
            if doc_coverage < 95:
                violations.append(f"Documentation coverage {doc_coverage}% below 95% threshold")
                score -= 20.0
                recommendations.append("Improve documentation coverage")
            
            # Check test coverage
            test_coverage = await self._get_test_coverage(operation, context)
            if test_coverage < 90:
                violations.append(f"Test coverage {test_coverage}% below 90% threshold")
                score -= 20.0
                recommendations.append("Increase test coverage")
            
            # Check maintainability
            maintainability_score = await self._get_maintainability_score(operation, context)
            if maintainability_score < 85:
                violations.append(f"Maintainability score {maintainability_score} below 85 threshold")
                score -= 15.0
                recommendations.append("Improve code maintainability")
            
            return max(0.0, score), violations, recommendations
            
        except Exception as e:
            logger.error("Error checking quality compliance", error=str(e))
            return 0.0, [f"Quality compliance check failed: {str(e)}"], ["Fix quality compliance checking"]
    
    async def _check_business_compliance(self, operation: str, context: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """Check business compliance"""
        violations = []
        recommendations = []
        score = 100.0
        
        try:
            # Check ROI
            roi = await self._get_roi(operation, context)
            if roi < 1.0:  # 100% ROI threshold
                violations.append(f"ROI {roi} below 100% threshold")
                score -= 30.0
                recommendations.append("Improve return on investment")
            
            # Check stakeholder satisfaction
            stakeholder_satisfaction = await self._get_stakeholder_satisfaction(operation, context)
            if stakeholder_satisfaction < 80:
                violations.append(f"Stakeholder satisfaction {stakeholder_satisfaction}% below 80% threshold")
                score -= 25.0
                recommendations.append("Improve stakeholder satisfaction")
            
            # Check business value
            business_value = await self._get_business_value(operation, context)
            if business_value < 70:
                violations.append(f"Business value {business_value}% below 70% threshold")
                score -= 25.0
                recommendations.append("Increase business value creation")
            
            # Check risk management
            risk_score = await self._get_risk_score(operation, context)
            if risk_score > 30:  # Lower is better
                violations.append(f"Risk score {risk_score} above 30 threshold")
                score -= 20.0
                recommendations.append("Improve risk management")
            
            return max(0.0, score), violations, recommendations
            
        except Exception as e:
            logger.error("Error checking business compliance", error=str(e))
            return 0.0, [f"Business compliance check failed: {str(e)}"], ["Fix business compliance checking"]
    
    async def _check_regulatory_compliance(self, operation: str, context: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """Check regulatory compliance"""
        violations = []
        recommendations = []
        score = 100.0
        
        try:
            # Check GDPR compliance
            if not await self._check_gdpr_compliance(operation, context):
                violations.append("GDPR compliance failure")
                score -= 25.0
                recommendations.append("Implement GDPR compliance measures")
            
            # Check SOX compliance
            if not await self._check_sox_compliance(operation, context):
                violations.append("SOX compliance failure")
                score -= 25.0
                recommendations.append("Implement SOX compliance measures")
            
            # Check HIPAA compliance
            if not await self._check_hipaa_compliance(operation, context):
                violations.append("HIPAA compliance failure")
                score -= 25.0
                recommendations.append("Implement HIPAA compliance measures")
            
            # Check PCI DSS compliance
            if not await self._check_pci_dss_compliance(operation, context):
                violations.append("PCI DSS compliance failure")
                score -= 25.0
                recommendations.append("Implement PCI DSS compliance measures")
            
            return max(0.0, score), violations, recommendations
            
        except Exception as e:
            logger.error("Error checking regulatory compliance", error=str(e))
            return 0.0, [f"Regulatory compliance check failed: {str(e)}"], ["Fix regulatory compliance checking"]
    
    async def _check_operational_compliance(self, operation: str, context: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """Check operational compliance"""
        violations = []
        recommendations = []
        score = 100.0
        
        try:
            # Check uptime
            uptime = await self._get_uptime(operation, context)
            if uptime < 99.9:  # 99.9% uptime threshold
                violations.append(f"Uptime {uptime}% below 99.9% threshold")
                score -= 30.0
                recommendations.append("Improve system uptime")
            
            # Check reliability
            reliability = await self._get_reliability(operation, context)
            if reliability < 99.0:  # 99% reliability threshold
                violations.append(f"Reliability {reliability}% below 99% threshold")
                score -= 25.0
                recommendations.append("Improve system reliability")
            
            # Check scalability
            scalability = await self._get_scalability(operation, context)
            if scalability < 90:
                violations.append(f"Scalability score {scalability} below 90 threshold")
                score -= 20.0
                recommendations.append("Improve system scalability")
            
            # Check monitoring
            monitoring_score = await self._get_monitoring_score(operation, context)
            if monitoring_score < 95:
                violations.append(f"Monitoring score {monitoring_score} below 95 threshold")
                score -= 25.0
                recommendations.append("Improve system monitoring")
            
            return max(0.0, score), violations, recommendations
            
        except Exception as e:
            logger.error("Error checking operational compliance", error=str(e))
            return 0.0, [f"Operational compliance check failed: {str(e)}"], ["Fix operational compliance checking"]
    
    def _calculate_overall_score(self, category_results: Dict[ComplianceCategory, ComplianceResult]) -> float:
        """Calculate overall compliance score"""
        if not category_results:
            return 0.0
        
        total_score = sum(result.score for result in category_results.values())
        return total_score / len(category_results)
    
    def _determine_overall_level(self, overall_score: float, critical_issues: List[str]) -> ComplianceLevel:
        """Determine overall compliance level"""
        if critical_issues:
            return ComplianceLevel.CRITICAL_NON_COMPLIANT
        elif overall_score >= 95.0:
            return ComplianceLevel.FULLY_COMPLIANT
        elif overall_score >= 85.0:
            return ComplianceLevel.MOSTLY_COMPLIANT
        elif overall_score >= 70.0:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.NON_COMPLIANT
    
    def _determine_compliance_level(self, score: float, thresholds: Dict[str, float]) -> ComplianceLevel:
        """Determine compliance level for a category"""
        min_score = thresholds.get('min_score', 90.0)
        critical_threshold = thresholds.get('critical_threshold', 70.0)
        
        if score >= min_score:
            return ComplianceLevel.FULLY_COMPLIANT
        elif score >= critical_threshold:
            return ComplianceLevel.PARTIALLY_COMPLIANT
        else:
            return ComplianceLevel.CRITICAL_NON_COMPLIANT
    
    # Placeholder methods for actual compliance checking
    async def _check_non_harm_principle(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check non-harm principle compliance"""
        return True  # Placeholder
    
    async def _check_truthfulness(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check truthfulness compliance"""
        return True  # Placeholder
    
    async def _check_fairness(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check fairness compliance"""
        return True  # Placeholder
    
    async def _check_autonomy(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check autonomy compliance"""
        return True  # Placeholder
    
    async def _check_beneficence(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check beneficence compliance"""
        return True  # Placeholder
    
    async def _check_accountability(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check accountability compliance"""
        return True  # Placeholder
    
    # Security compliance methods
    async def _check_encryption_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check encryption compliance"""
        return True  # Placeholder
    
    async def _check_access_control_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check access control compliance"""
        return True  # Placeholder
    
    async def _check_vulnerability_scanning(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check vulnerability scanning compliance"""
        return True  # Placeholder
    
    async def _check_audit_trail_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check audit trail compliance"""
        return True  # Placeholder
    
    async def _check_data_protection_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check data protection compliance"""
        return True  # Placeholder
    
    # Performance metrics methods
    async def _get_response_time(self, operation: str, context: Dict[str, Any]) -> float:
        """Get response time for operation"""
        return 150.0  # Placeholder
    
    async def _get_throughput(self, operation: str, context: Dict[str, Any]) -> float:
        """Get throughput for operation"""
        return 1200.0  # Placeholder
    
    async def _get_cpu_usage(self, operation: str, context: Dict[str, Any]) -> float:
        """Get CPU usage for operation"""
        return 65.0  # Placeholder
    
    async def _get_memory_usage(self, operation: str, context: Dict[str, Any]) -> float:
        """Get memory usage for operation"""
        return 70.0  # Placeholder
    
    async def _get_error_rate(self, operation: str, context: Dict[str, Any]) -> float:
        """Get error rate for operation"""
        return 0.05  # Placeholder
    
    # Quality metrics methods
    async def _get_code_quality_score(self, operation: str, context: Dict[str, Any]) -> float:
        """Get code quality score"""
        return 95.0  # Placeholder
    
    async def _get_documentation_coverage(self, operation: str, context: Dict[str, Any]) -> float:
        """Get documentation coverage"""
        return 98.0  # Placeholder
    
    async def _get_test_coverage(self, operation: str, context: Dict[str, Any]) -> float:
        """Get test coverage"""
        return 92.0  # Placeholder
    
    async def _get_maintainability_score(self, operation: str, context: Dict[str, Any]) -> float:
        """Get maintainability score"""
        return 88.0  # Placeholder
    
    # Business metrics methods
    async def _get_roi(self, operation: str, context: Dict[str, Any]) -> float:
        """Get return on investment"""
        return 1.5  # Placeholder
    
    async def _get_stakeholder_satisfaction(self, operation: str, context: Dict[str, Any]) -> float:
        """Get stakeholder satisfaction"""
        return 85.0  # Placeholder
    
    async def _get_business_value(self, operation: str, context: Dict[str, Any]) -> float:
        """Get business value score"""
        return 80.0  # Placeholder
    
    async def _get_risk_score(self, operation: str, context: Dict[str, Any]) -> float:
        """Get risk score"""
        return 15.0  # Placeholder
    
    # Regulatory compliance methods
    async def _check_gdpr_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check GDPR compliance"""
        return True  # Placeholder
    
    async def _check_sox_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check SOX compliance"""
        return True  # Placeholder
    
    async def _check_hipaa_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check HIPAA compliance"""
        return True  # Placeholder
    
    async def _check_pci_dss_compliance(self, operation: str, context: Dict[str, Any]) -> bool:
        """Check PCI DSS compliance"""
        return True  # Placeholder
    
    # Operational metrics methods
    async def _get_uptime(self, operation: str, context: Dict[str, Any]) -> float:
        """Get system uptime"""
        return 99.95  # Placeholder
    
    async def _get_reliability(self, operation: str, context: Dict[str, Any]) -> float:
        """Get system reliability"""
        return 99.5  # Placeholder
    
    async def _get_scalability(self, operation: str, context: Dict[str, Any]) -> float:
        """Get scalability score"""
        return 95.0  # Placeholder
    
    async def _get_monitoring_score(self, operation: str, context: Dict[str, Any]) -> float:
        """Get monitoring score"""
        return 98.0  # Placeholder
    
    async def get_compliance_history(self, limit: int = 100) -> List[ComplianceReport]:
        """Get compliance history"""
        return self.compliance_history[-limit:]
    
    async def get_compliance_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get compliance trends over time"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        recent_reports = [r for r in self.compliance_history if r.generated_at >= cutoff_date]
        
        if not recent_reports:
            return {'trend': 'no_data', 'average_score': 0.0}
        
        scores = [r.overall_score for r in recent_reports]
        average_score = sum(scores) / len(scores)
        
        # Calculate trend
        if len(scores) >= 2:
            trend = 'improving' if scores[-1] > scores[0] else 'declining'
        else:
            trend = 'stable'
        
        return {
            'trend': trend,
            'average_score': average_score,
            'reports_count': len(recent_reports),
            'latest_score': scores[-1] if scores else 0.0
        }


# Global instance
compliance_engine = ComplianceEngine()

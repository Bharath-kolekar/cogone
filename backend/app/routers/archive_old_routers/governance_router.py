"""
Governance Router - API endpoints for governance management and monitoring
"""

import structlog
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import uuid

from app.core.governance_monitor import governance_monitor, GovernanceViolation, GovernanceSeverity
from app.core.compliance_engine import compliance_engine, ComplianceReport, ComplianceCategory
from app.core.governance_dashboard import governance_dashboard, GovernanceAlert
from app.core.dependencies import get_current_user
from app.models.user import User

logger = structlog.get_logger()

router = APIRouter(prefix="/api/v0/governance", tags=["governance"])


# Request/Response Models
class GovernanceViolationRequest(BaseModel):
    """Request to create a governance violation"""
    component: str
    rule_id: str
    severity: str
    description: str
    context: Dict[str, Any] = Field(default_factory=dict)


class GovernanceViolationResponse(BaseModel):
    """Response for governance violation"""
    id: str
    component: str
    rule_id: str
    severity: str
    description: str
    context: Dict[str, Any]
    detected_at: datetime
    resolved_at: Optional[datetime] = None
    remediation_actions: List[str] = Field(default_factory=list)
    impact_score: float


class ComplianceCheckRequest(BaseModel):
    """Request for compliance checking"""
    operation: str
    context: Dict[str, Any] = Field(default_factory=dict)
    categories: List[str] = Field(default_factory=list)


class ComplianceCheckResponse(BaseModel):
    """Response for compliance checking"""
    overall_score: float
    overall_level: str
    category_results: Dict[str, Any]
    critical_issues: List[str]
    recommendations: List[str]
    generated_at: datetime
    valid_until: datetime


class GovernanceMetricsResponse(BaseModel):
    """Response for governance metrics"""
    overall_score: float
    compliance_rate: float
    violation_count: int
    critical_violations: int
    high_violations: int
    medium_violations: int
    low_violations: int
    avg_remediation_time: float
    policy_coverage: float
    last_updated: datetime


class DashboardResponse(BaseModel):
    """Response for dashboard data"""
    widgets: Dict[str, Any]
    alerts: List[Dict[str, Any]]
    last_updated: str
    dashboard_status: str


class AlertRequest(BaseModel):
    """Request to create an alert"""
    severity: str
    title: str
    message: str
    component: str


class AlertResponse(BaseModel):
    """Response for alert operations"""
    id: str
    severity: str
    title: str
    message: str
    component: str
    created_at: datetime
    acknowledged: bool
    resolved: bool


# Governance Management Endpoints
@router.post("/enforce-policy")
async def enforce_policy(
    policy_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Enforce governance policy"""
    try:
        # Initialize governance monitor if not already done
        if not governance_monitor.monitoring_active:
            await governance_monitor.initialize()
        
        # Enforce policy based on policy data
        result = await governance_monitor._check_governance_compliance()
        
        logger.info("Policy enforcement completed", 
                   user_id=current_user.id,
                   policy_data=policy_data)
        
        return {
            "status": "success",
            "message": "Policy enforcement completed",
            "result": result
        }
        
    except Exception as e:
        logger.error("Error enforcing policy", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compliance-status")
async def get_compliance_status(
    current_user: User = Depends(get_current_user)
):
    """Get current compliance status"""
    try:
        # Initialize compliance engine if not already done
        if not compliance_engine.compliance_rules:
            await compliance_engine.initialize()
        
        # Get compliance status
        compliance_status = await compliance_engine.get_compliance_history(limit=1)
        
        if compliance_status:
            latest_report = compliance_status[0]
            return {
                "status": "success",
                "compliance_status": {
                    "overall_score": latest_report.overall_score,
                    "overall_level": latest_report.overall_level.value,
                    "critical_issues": latest_report.critical_issues,
                    "recommendations": latest_report.recommendations,
                    "generated_at": latest_report.generated_at.isoformat()
                }
            }
        else:
            return {
                "status": "success",
                "compliance_status": {
                    "overall_score": 0.0,
                    "overall_level": "unknown",
                    "critical_issues": [],
                    "recommendations": [],
                    "generated_at": datetime.utcnow().isoformat()
                }
            }
        
    except Exception as e:
        logger.error("Error getting compliance status", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/violation-report")
async def report_violation(
    violation_data: GovernanceViolationRequest,
    current_user: User = Depends(get_current_user)
):
    """Report a governance violation"""
    try:
        # Initialize governance monitor if not already done
        if not governance_monitor.monitoring_active:
            await governance_monitor.initialize()
        
        # Create violation
        await governance_monitor._create_violation(
            component=violation_data.component,
            rule_id=violation_data.rule_id,
            severity=GovernanceSeverity(violation_data.severity),
            description=violation_data.description,
            context=violation_data.context
        )
        
        logger.info("Governance violation reported", 
                   user_id=current_user.id,
                   component=violation_data.component,
                   severity=violation_data.severity)
        
        return {
            "status": "success",
            "message": "Violation reported successfully"
        }
        
    except Exception as e:
        logger.error("Error reporting violation", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics")
async def get_governance_metrics(
    current_user: User = Depends(get_current_user)
):
    """Get governance metrics"""
    try:
        # Initialize governance monitor if not already done
        if not governance_monitor.monitoring_active:
            await governance_monitor.initialize()
        
        # Get governance metrics
        metrics = await governance_monitor.get_governance_metrics()
        
        return {
            "status": "success",
            "metrics": {
                "overall_score": metrics.overall_score,
                "compliance_rate": metrics.compliance_rate,
                "violation_count": metrics.violation_count,
                "critical_violations": metrics.critical_violations,
                "high_violations": metrics.high_violations,
                "medium_violations": metrics.medium_violations,
                "low_violations": metrics.low_violations,
                "avg_remediation_time": metrics.avg_remediation_time,
                "policy_coverage": metrics.policy_coverage,
                "last_updated": metrics.last_updated.isoformat()
            }
        }
        
    except Exception as e:
        logger.error("Error getting governance metrics", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Policy Management Endpoints
@router.post("/policies/create")
async def create_policy(
    policy_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Create a new governance policy"""
    try:
        # Initialize governance monitor if not already done
        if not governance_monitor.monitoring_active:
            await governance_monitor.initialize()
        
        # Add policy to governance rules
        policy_id = policy_data.get('id', str(uuid.uuid4()))
        policy_type = policy_data.get('type', 'custom')
        
        if policy_type not in governance_monitor.governance_rules:
            governance_monitor.governance_rules[policy_type] = {}
        
        governance_monitor.governance_rules[policy_type][policy_id] = policy_data
        
        logger.info("Governance policy created", 
                   user_id=current_user.id,
                   policy_id=policy_id,
                   policy_type=policy_type)
        
        return {
            "status": "success",
            "message": "Policy created successfully",
            "policy_id": policy_id
        }
        
    except Exception as e:
        logger.error("Error creating policy", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/policies/update")
async def update_policy(
    policy_id: str,
    policy_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Update an existing governance policy"""
    try:
        # Initialize governance monitor if not already done
        if not governance_monitor.monitoring_active:
            await governance_monitor.initialize()
        
        # Update policy in governance rules
        policy_type = policy_data.get('type', 'custom')
        
        if policy_type in governance_monitor.governance_rules and policy_id in governance_monitor.governance_rules[policy_type]:
            governance_monitor.governance_rules[policy_type][policy_id].update(policy_data)
            
            logger.info("Governance policy updated", 
                       user_id=current_user.id,
                       policy_id=policy_id,
                       policy_type=policy_type)
            
            return {
                "status": "success",
                "message": "Policy updated successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Policy not found")
        
    except Exception as e:
        logger.error("Error updating policy", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/policies/list")
async def list_policies(
    current_user: User = Depends(get_current_user)
):
    """List all governance policies"""
    try:
        # Initialize governance monitor if not already done
        if not governance_monitor.monitoring_active:
            await governance_monitor.initialize()
        
        # Get all policies
        policies = {}
        for policy_type, policy_rules in governance_monitor.governance_rules.items():
            policies[policy_type] = policy_rules
        
        return {
            "status": "success",
            "policies": policies
        }
        
    except Exception as e:
        logger.error("Error listing policies", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/policies/delete")
async def delete_policy(
    policy_id: str,
    policy_type: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a governance policy"""
    try:
        # Initialize governance monitor if not already done
        if not governance_monitor.monitoring_active:
            await governance_monitor.initialize()
        
        # Delete policy from governance rules
        if policy_type in governance_monitor.governance_rules and policy_id in governance_monitor.governance_rules[policy_type]:
            del governance_monitor.governance_rules[policy_type][policy_id]
            
            logger.info("Governance policy deleted", 
                       user_id=current_user.id,
                       policy_id=policy_id,
                       policy_type=policy_type)
            
            return {
                "status": "success",
                "message": "Policy deleted successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Policy not found")
        
    except Exception as e:
        logger.error("Error deleting policy", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Compliance Monitoring Endpoints
@router.get("/compliance/dashboard")
async def get_compliance_dashboard(
    current_user: User = Depends(get_current_user)
):
    """Get compliance dashboard data"""
    try:
        # Initialize compliance engine if not already done
        if not compliance_engine.compliance_rules:
            await compliance_engine.initialize()
        
        # Get compliance trends
        trends = await compliance_engine.get_compliance_trends(days=30)
        
        # Get compliance history
        history = await compliance_engine.get_compliance_history(limit=10)
        
        return {
            "status": "success",
            "dashboard": {
                "trends": trends,
                "history": [
                    {
                        "overall_score": report.overall_score,
                        "overall_level": report.overall_level.value,
                        "generated_at": report.generated_at.isoformat()
                    }
                    for report in history
                ]
            }
        }
        
    except Exception as e:
        logger.error("Error getting compliance dashboard", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compliance/trends")
async def get_compliance_trends(
    days: int = 30,
    current_user: User = Depends(get_current_user)
):
    """Get compliance trends"""
    try:
        # Initialize compliance engine if not already done
        if not compliance_engine.compliance_rules:
            await compliance_engine.initialize()
        
        # Get compliance trends
        trends = await compliance_engine.get_compliance_trends(days=days)
        
        return {
            "status": "success",
            "trends": trends
        }
        
    except Exception as e:
        logger.error("Error getting compliance trends", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/compliance/reports")
async def get_compliance_reports(
    limit: int = 100,
    current_user: User = Depends(get_current_user)
):
    """Get compliance reports"""
    try:
        # Initialize compliance engine if not already done
        if not compliance_engine.compliance_rules:
            await compliance_engine.initialize()
        
        # Get compliance history
        history = await compliance_engine.get_compliance_history(limit=limit)
        
        reports = []
        for report in history:
            reports.append({
                "overall_score": report.overall_score,
                "overall_level": report.overall_level.value,
                "category_results": {
                    category.value: {
                        "level": result.level.value,
                        "score": result.score,
                        "violations": result.violations,
                        "recommendations": result.recommendations
                    }
                    for category, result in report.category_results.items()
                },
                "critical_issues": report.critical_issues,
                "recommendations": report.recommendations,
                "generated_at": report.generated_at.isoformat(),
                "valid_until": report.valid_until.isoformat()
            })
        
        return {
            "status": "success",
            "reports": reports
        }
        
    except Exception as e:
        logger.error("Error getting compliance reports", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Dashboard Endpoints
@router.get("/dashboard")
async def get_governance_dashboard(
    current_user: User = Depends(get_current_user)
):
    """Get governance dashboard data"""
    try:
        # Initialize dashboard if not already done
        if not governance_dashboard.dashboard_active:
            await governance_dashboard.initialize()
        
        # Get dashboard data
        dashboard_data = await governance_dashboard.get_dashboard_data()
        
        return {
            "status": "success",
            "dashboard": dashboard_data
        }
        
    except Exception as e:
        logger.error("Error getting governance dashboard", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/widget/{widget_id}")
async def get_dashboard_widget(
    widget_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get specific dashboard widget data"""
    try:
        # Initialize dashboard if not already done
        if not governance_dashboard.dashboard_active:
            await governance_dashboard.initialize()
        
        # Get widget data
        widget_data = await governance_dashboard.get_widget_data(widget_id)
        
        if widget_data:
            return {
                "status": "success",
                "widget": widget_data
            }
        else:
            raise HTTPException(status_code=404, detail="Widget not found")
        
    except Exception as e:
        logger.error("Error getting dashboard widget", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Alert Management Endpoints
@router.post("/alerts/create")
async def create_alert(
    alert_data: AlertRequest,
    current_user: User = Depends(get_current_user)
):
    """Create a governance alert"""
    try:
        # Initialize dashboard if not already done
        if not governance_dashboard.dashboard_active:
            await governance_dashboard.initialize()
        
        # Create alert
        alert_id = await governance_dashboard.create_alert(
            severity=alert_data.severity,
            title=alert_data.title,
            message=alert_data.message,
            component=alert_data.component
        )
        
        logger.info("Governance alert created", 
                   user_id=current_user.id,
                   alert_id=alert_id,
                   severity=alert_data.severity)
        
        return {
            "status": "success",
            "message": "Alert created successfully",
            "alert_id": alert_id
        }
        
    except Exception as e:
        logger.error("Error creating alert", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
async def get_alerts(
    severity: Optional[str] = None,
    acknowledged: Optional[bool] = None,
    current_user: User = Depends(get_current_user)
):
    """Get governance alerts"""
    try:
        # Initialize dashboard if not already done
        if not governance_dashboard.dashboard_active:
            await governance_dashboard.initialize()
        
        # Get alerts
        alerts = await governance_dashboard.get_alerts(severity=severity, acknowledged=acknowledged)
        
        alert_list = []
        for alert in alerts:
            alert_list.append({
                "id": alert.id,
                "severity": alert.severity,
                "title": alert.title,
                "message": alert.message,
                "component": alert.component,
                "created_at": alert.created_at.isoformat(),
                "acknowledged": alert.acknowledged,
                "resolved": alert.resolved
            })
        
        return {
            "status": "success",
            "alerts": alert_list
        }
        
    except Exception as e:
        logger.error("Error getting alerts", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user)
):
    """Acknowledge an alert"""
    try:
        # Initialize dashboard if not already done
        if not governance_dashboard.dashboard_active:
            await governance_dashboard.initialize()
        
        # Acknowledge alert
        success = await governance_dashboard.acknowledge_alert(alert_id)
        
        if success:
            logger.info("Alert acknowledged", 
                       user_id=current_user.id,
                       alert_id=alert_id)
            
            return {
                "status": "success",
                "message": "Alert acknowledged successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Alert not found")
        
    except Exception as e:
        logger.error("Error acknowledging alert", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user)
):
    """Resolve an alert"""
    try:
        # Initialize dashboard if not already done
        if not governance_dashboard.dashboard_active:
            await governance_dashboard.initialize()
        
        # Resolve alert
        success = await governance_dashboard.resolve_alert(alert_id)
        
        if success:
            logger.info("Alert resolved", 
                       user_id=current_user.id,
                       alert_id=alert_id)
            
            return {
                "status": "success",
                "message": "Alert resolved successfully"
            }
        else:
            raise HTTPException(status_code=404, detail="Alert not found")
        
    except Exception as e:
        logger.error("Error resolving alert", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Comprehensive Compliance Check
@router.post("/comprehensive/check")
async def comprehensive_compliance_check(
    check_request: ComplianceCheckRequest,
    current_user: User = Depends(get_current_user)
):
    """Perform comprehensive compliance checking"""
    try:
        # Initialize compliance engine if not already done
        if not compliance_engine.compliance_rules:
            await compliance_engine.initialize()
        
        # Perform compliance check
        report = await compliance_engine.check_compliance(
            operation=check_request.operation,
            context=check_request.context
        )
        
        logger.info("Comprehensive compliance check completed", 
                   user_id=current_user.id,
                   operation=check_request.operation,
                   overall_score=report.overall_score)
        
        return {
            "status": "success",
            "compliance_report": {
                "overall_score": report.overall_score,
                "overall_level": report.overall_level.value,
                "category_results": {
                    category.value: {
                        "level": result.level.value,
                        "score": result.score,
                        "violations": result.violations,
                        "recommendations": result.recommendations
                    }
                    for category, result in report.category_results.items()
                },
                "critical_issues": report.critical_issues,
                "recommendations": report.recommendations,
                "generated_at": report.generated_at.isoformat(),
                "valid_until": report.valid_until.isoformat()
            }
        }
        
    except Exception as e:
        logger.error("Error in comprehensive compliance check", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Health Check
@router.get("/health")
async def governance_health_check():
    """Health check for governance system"""
    try:
        health_status = {
            "governance_monitor": governance_monitor.monitoring_active,
            "compliance_engine": bool(compliance_engine.compliance_rules),
            "governance_dashboard": governance_dashboard.dashboard_active,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        overall_health = all([
            health_status["governance_monitor"],
            health_status["compliance_engine"],
            health_status["governance_dashboard"]
        ])
        
        return {
            "status": "healthy" if overall_health else "degraded",
            "components": health_status
        }
        
    except Exception as e:
        logger.error("Error in governance health check", error=str(e))
        return {
            "status": "unhealthy",
            "error": str(e)
        }

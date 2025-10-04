"""
Architecture Generator Pydantic Models
Advanced system architecture generation models
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


# ============================================================================
# ARCHITECTURE GENERATOR ENUMS
# ============================================================================

class ArchitectureType(str, Enum):
    """Architecture type enumeration"""
    MICROSERVICES = "microservices"
    MONOLITH = "monolith"
    SERVERLESS = "serverless"
    EVENT_DRIVEN = "event_driven"
    LAYERED = "layered"
    HEXAGONAL = "hexagonal"
    CLEAN_ARCHITECTURE = "clean_architecture"
    DDD = "domain_driven_design"
    CQRS = "cqrs"
    EVENT_SOURCING = "event_sourcing"
    SWARM_AI = "swarm_ai"
    MULTI_AGENT = "multi_agent"


class DiagramType(str, Enum):
    """Mermaid diagram type enumeration"""
    FLOWCHART = "flowchart"
    SEQUENCE = "sequence"
    CLASS = "class"
    STATE = "state"
    ER = "er"
    USER_JOURNEY = "user_journey"
    GANTT = "gantt"
    PIE = "pie"
    GITGRAPH = "gitgraph"
    MINDMAP = "mindmap"
    TIMELINE = "timeline"
    QUADRANT = "quadrant"
    REQUIREMENT = "requirement"


class ComponentType(str, Enum):
    """Component type enumeration"""
    SERVICE = "service"
    DATABASE = "database"
    API = "api"
    QUEUE = "queue"
    CACHE = "cache"
    LOAD_BALANCER = "load_balancer"
    GATEWAY = "gateway"
    AUTHENTICATION = "authentication"
    MONITORING = "monitoring"
    LOGGING = "logging"
    AI_AGENT = "ai_agent"
    SWARM = "swarm"
    ORCHESTRATOR = "orchestrator"


class RelationshipType(str, Enum):
    """Relationship type enumeration"""
    DEPENDS_ON = "depends_on"
    COMMUNICATES_WITH = "communicates_with"
    AGGREGATES = "aggregates"
    COMPOSES = "composes"
    INHERITS = "inherits"
    IMPLEMENTS = "implements"
    USES = "uses"
    CALLS = "calls"
    STORES = "stores"
    CACHES = "caches"
    LOADS = "loads"
    MONITORS = "monitors"
    COORDINATES = "coordinates"
    MANAGES = "manages"
    ROUTES_TO = "routes_to"
    PUBLISHES_TO = "publishes_to"
    STORES_IN = "stores_in"


class RepairType(str, Enum):
    """AI diagram repair type enumeration"""
    SYNTAX_FIX = "syntax_fix"
    LOGIC_CORRECTION = "logic_correction"
    OPTIMIZATION = "optimization"
    ENHANCEMENT = "enhancement"
    VALIDATION = "validation"
    COMPLETION = "completion"


# ============================================================================
# ARCHITECTURE MODELS
# ============================================================================

class ArchitectureCreateRequest(BaseModel):
    """Request to create a new architecture"""
    name: str = Field(..., description="Architecture name")
    architecture_type: str = Field(..., description="Type of architecture")
    description: str = Field(..., description="Architecture description")
    requirements: List[str] = Field(default_factory=list, description="Architecture requirements")
    tags: List[str] = Field(default_factory=list, description="Architecture tags")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ArchitectureResponse(BaseModel):
    """Architecture response model"""
    architecture_id: str = Field(..., description="Architecture identifier")
    name: str = Field(..., description="Architecture name")
    architecture_type: str = Field(..., description="Architecture type")
    description: str = Field(..., description="Architecture description")
    component_count: int = Field(..., description="Number of components")
    relationship_count: int = Field(..., description="Number of relationships")
    created_at: datetime = Field(..., description="Creation timestamp")
    status: str = Field(..., description="Architecture status")


class ArchitectureListResponse(BaseModel):
    """Architecture list response model"""
    architectures: List[Dict[str, Any]] = Field(..., description="List of architectures")
    total_count: int = Field(..., description="Total number of architectures")


# ============================================================================
# DIAGRAM MODELS
# ============================================================================

class DiagramGenerateRequest(BaseModel):
    """Request to generate a diagram"""
    diagram_type: str = Field(..., description="Type of diagram to generate")
    title: Optional[str] = Field(None, description="Diagram title")
    description: Optional[str] = Field(None, description="Diagram description")
    options: Dict[str, Any] = Field(default_factory=dict, description="Generation options")


class DiagramResponse(BaseModel):
    """Diagram response model"""
    diagram_id: str = Field(..., description="Diagram identifier")
    architecture_id: str = Field(..., description="Architecture identifier")
    diagram_type: str = Field(..., description="Diagram type")
    title: str = Field(..., description="Diagram title")
    content: str = Field(..., description="Mermaid diagram content")
    description: str = Field(..., description="Diagram description")
    created_at: datetime = Field(..., description="Creation timestamp")


class DiagramListResponse(BaseModel):
    """Diagram list response model"""
    diagrams: List[Dict[str, Any]] = Field(..., description="List of diagrams")
    total_count: int = Field(..., description="Total number of diagrams")


# ============================================================================
# ANALYSIS MODELS
# ============================================================================

class AnalysisResponse(BaseModel):
    """Analysis response model"""
    analysis_id: str = Field(..., description="Analysis identifier")
    architecture_id: str = Field(..., description="Architecture identifier")
    analysis_type: str = Field(..., description="Type of analysis")
    findings: List[str] = Field(..., description="Analysis findings")
    recommendations: List[str] = Field(..., description="Analysis recommendations")
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Overall quality score")
    complexity_score: float = Field(..., ge=0.0, le=1.0, description="Complexity score")
    maintainability_score: float = Field(..., ge=0.0, le=1.0, description="Maintainability score")
    scalability_score: float = Field(..., ge=0.0, le=1.0, description="Scalability score")
    security_score: float = Field(..., ge=0.0, le=1.0, description="Security score")
    performance_score: float = Field(..., ge=0.0, le=1.0, description="Performance score")
    created_at: datetime = Field(..., description="Analysis timestamp")


class AnalysisListResponse(BaseModel):
    """Analysis list response model"""
    analyses: List[Dict[str, Any]] = Field(..., description="List of analyses")
    total_count: int = Field(..., description="Total number of analyses")


# ============================================================================
# COMPONENT MODELS
# ============================================================================

class ComponentCreateRequest(BaseModel):
    """Request to create a component"""
    name: str = Field(..., description="Component name")
    component_type: str = Field(..., description="Component type")
    description: str = Field(..., description="Component description")
    responsibilities: List[str] = Field(default_factory=list, description="Component responsibilities")
    interfaces: List[str] = Field(default_factory=list, description="Component interfaces")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Component properties")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ComponentResponse(BaseModel):
    """Component response model"""
    component_id: str = Field(..., description="Component identifier")
    name: str = Field(..., description="Component name")
    component_type: str = Field(..., description="Component type")
    description: str = Field(..., description="Component description")
    responsibilities: List[str] = Field(..., description="Component responsibilities")
    interfaces: List[str] = Field(..., description="Component interfaces")
    properties: Dict[str, Any] = Field(..., description="Component properties")
    metadata: Dict[str, Any] = Field(..., description="Component metadata")
    created_at: datetime = Field(..., description="Creation timestamp")


# ============================================================================
# RELATIONSHIP MODELS
# ============================================================================

class RelationshipCreateRequest(BaseModel):
    """Request to create a relationship"""
    source_component: str = Field(..., description="Source component identifier")
    target_component: str = Field(..., description="Target component identifier")
    relationship_type: str = Field(..., description="Relationship type")
    description: str = Field(..., description="Relationship description")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Relationship properties")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class RelationshipResponse(BaseModel):
    """Relationship response model"""
    relationship_id: str = Field(..., description="Relationship identifier")
    source_component: str = Field(..., description="Source component identifier")
    target_component: str = Field(..., description="Target component identifier")
    relationship_type: str = Field(..., description="Relationship type")
    description: str = Field(..., description="Relationship description")
    properties: Dict[str, Any] = Field(..., description="Relationship properties")
    metadata: Dict[str, Any] = Field(..., description="Relationship metadata")
    created_at: datetime = Field(..., description="Creation timestamp")


# ============================================================================
# BATCH OPERATION MODELS
# ============================================================================

class BatchDiagramGenerateRequest(BaseModel):
    """Request to generate multiple diagrams"""
    diagram_types: List[str] = Field(..., description="List of diagram types to generate")
    options: Dict[str, Any] = Field(default_factory=dict, description="Generation options")


class BatchDiagramResponse(BaseModel):
    """Batch diagram generation response"""
    architecture_id: str = Field(..., description="Architecture identifier")
    generated_diagrams: List[Dict[str, Any]] = Field(..., description="Generated diagrams")
    total_count: int = Field(..., description="Total number of generated diagrams")
    created_at: datetime = Field(..., description="Creation timestamp")


# ============================================================================
# TEMPLATE MODELS
# ============================================================================

class ArchitectureTemplate(BaseModel):
    """Architecture template model"""
    template_id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Template name")
    architecture_type: str = Field(..., description="Architecture type")
    description: str = Field(..., description="Template description")
    components: List[Dict[str, Any]] = Field(..., description="Template components")
    relationships: List[Dict[str, Any]] = Field(..., description="Template relationships")
    use_cases: List[str] = Field(..., description="Template use cases")
    benefits: List[str] = Field(..., description="Template benefits")
    trade_offs: List[str] = Field(..., description="Template trade-offs")
    created_at: datetime = Field(..., description="Creation timestamp")


class TemplateListResponse(BaseModel):
    """Template list response model"""
    templates: List[ArchitectureTemplate] = Field(..., description="List of templates")
    total_count: int = Field(..., description="Total number of templates")


# ============================================================================
# EXPORT MODELS
# ============================================================================

class ArchitectureExportRequest(BaseModel):
    """Request to export architecture"""
    export_format: str = Field(..., description="Export format (json, yaml, xml, mermaid)")
    include_diagrams: bool = Field(default=True, description="Include diagrams in export")
    include_analysis: bool = Field(default=False, description="Include analysis in export")
    options: Dict[str, Any] = Field(default_factory=dict, description="Export options")


class ArchitectureExportResponse(BaseModel):
    """Architecture export response"""
    export_id: str = Field(..., description="Export identifier")
    architecture_id: str = Field(..., description="Architecture identifier")
    export_format: str = Field(..., description="Export format")
    content: str = Field(..., description="Exported content")
    file_size: int = Field(..., description="File size in bytes")
    created_at: datetime = Field(..., description="Export timestamp")


# ============================================================================
# VALIDATION MODELS
# ============================================================================

class ArchitectureValidationRequest(BaseModel):
    """Request to validate architecture"""
    validation_rules: List[str] = Field(default_factory=list, description="Validation rules to apply")
    strict_mode: bool = Field(default=False, description="Enable strict validation")
    options: Dict[str, Any] = Field(default_factory=dict, description="Validation options")


class ArchitectureValidationResponse(BaseModel):
    """Architecture validation response"""
    validation_id: str = Field(..., description="Validation identifier")
    architecture_id: str = Field(..., description="Architecture identifier")
    is_valid: bool = Field(..., description="Whether architecture is valid")
    validation_score: float = Field(..., ge=0.0, le=1.0, description="Validation score")
    issues: List[Dict[str, Any]] = Field(..., description="Validation issues")
    recommendations: List[str] = Field(..., description="Validation recommendations")
    created_at: datetime = Field(..., description="Validation timestamp")


# ============================================================================
# METRICS MODELS
# ============================================================================

class ArchitectureMetrics(BaseModel):
    """Architecture metrics model"""
    architecture_id: str = Field(..., description="Architecture identifier")
    total_components: int = Field(..., description="Total number of components")
    total_relationships: int = Field(..., description="Total number of relationships")
    complexity_score: float = Field(..., ge=0.0, le=1.0, description="Complexity score")
    maintainability_score: float = Field(..., ge=0.0, le=1.0, description="Maintainability score")
    scalability_score: float = Field(..., ge=0.0, le=1.0, description="Scalability score")
    security_score: float = Field(..., ge=0.0, le=1.0, description="Security score")
    performance_score: float = Field(..., ge=0.0, le=1.0, description="Performance score")
    overall_score: float = Field(..., ge=0.0, le=1.0, description="Overall score")
    last_updated: datetime = Field(..., description="Last update timestamp")


class MetricsResponse(BaseModel):
    """Metrics response model"""
    metrics: ArchitectureMetrics = Field(..., description="Architecture metrics")
    trends: Dict[str, List[float]] = Field(..., description="Performance trends")
    recommendations: List[str] = Field(..., description="Improvement recommendations")
    last_updated: datetime = Field(..., description="Last update timestamp")


# ============================================================================
# ERROR MODELS
# ============================================================================

class ArchitectureError(BaseModel):
    """Architecture error model"""
    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Error message")
    error_details: Dict[str, Any] = Field(..., description="Error details")
    timestamp: datetime = Field(..., description="Error timestamp")
    architecture_id: Optional[str] = Field(None, description="Architecture identifier")


class ValidationError(BaseModel):
    """Validation error model"""
    field: str = Field(..., description="Field name")
    error_type: str = Field(..., description="Error type")
    error_message: str = Field(..., description="Error message")
    suggested_value: Optional[Any] = Field(None, description="Suggested value")
    timestamp: datetime = Field(..., description="Error timestamp")


# ============================================================================
# AI DIAGRAM REPAIR MODELS
# ============================================================================

class DiagramRepairRequest(BaseModel):
    """Request for AI diagram repair"""
    diagram_content: str = Field(..., description="Original diagram content")
    diagram_type: DiagramType = Field(..., description="Type of diagram to repair")
    repair_type: RepairType = Field(..., description="Type of repair to perform")
    issues: List[str] = Field(default_factory=list, description="Known issues to fix")
    requirements: List[str] = Field(default_factory=list, description="Requirements for repair")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class DiagramRepairResponse(BaseModel):
    """Response for AI diagram repair"""
    repair_id: str = Field(..., description="Unique repair identifier")
    original_diagram: str = Field(..., description="Original diagram content")
    repaired_diagram: str = Field(..., description="Repaired diagram content")
    repair_type: RepairType = Field(..., description="Type of repair performed")
    issues_found: List[str] = Field(..., description="Issues found in original diagram")
    fixes_applied: List[str] = Field(..., description="Fixes applied to diagram")
    improvements: List[str] = Field(..., description="Improvements made to diagram")
    confidence_score: float = Field(..., description="Confidence score for repair quality")
    validation_passed: bool = Field(..., description="Whether validation passed")
    performance_metrics: Dict[str, float] = Field(..., description="Performance metrics")
    created_at: datetime = Field(..., description="Repair timestamp")


class DiagramAnalysisRequest(BaseModel):
    """Request for diagram analysis"""
    diagram_content: str = Field(..., description="Diagram content to analyze")
    diagram_type: DiagramType = Field(..., description="Type of diagram")
    analysis_depth: str = Field(default="standard", description="Depth of analysis")
    focus_areas: List[str] = Field(default_factory=list, description="Areas to focus on")


class DiagramAnalysisResponse(BaseModel):
    """Response for diagram analysis"""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    syntax_valid: bool = Field(..., description="Whether syntax is valid")
    logic_consistent: bool = Field(..., description="Whether logic is consistent")
    completeness_score: float = Field(..., description="Completeness score (0-1)")
    optimization_opportunities: List[str] = Field(..., description="Optimization opportunities")
    best_practices_compliance: float = Field(..., description="Best practices compliance score")
    complexity_analysis: Dict[str, Any] = Field(..., description="Complexity analysis results")
    recommendations: List[str] = Field(..., description="Improvement recommendations")
    quality_score: float = Field(..., description="Overall quality score")
    created_at: datetime = Field(..., description="Analysis timestamp")


class DiagramOptimizationRequest(BaseModel):
    """Request for diagram optimization"""
    diagram_content: str = Field(..., description="Diagram content to optimize")
    diagram_type: DiagramType = Field(..., description="Type of diagram")
    optimization_goals: List[str] = Field(..., description="Optimization goals")
    constraints: List[str] = Field(default_factory=list, description="Optimization constraints")


class DiagramOptimizationResponse(BaseModel):
    """Response for diagram optimization"""
    optimization_id: str = Field(..., description="Unique optimization identifier")
    original_diagram: str = Field(..., description="Original diagram content")
    optimized_diagram: str = Field(..., description="Optimized diagram content")
    optimization_goals: List[str] = Field(..., description="Optimization goals applied")
    improvements: List[str] = Field(..., description="Improvements made")
    performance_gains: Dict[str, float] = Field(..., description="Performance gains achieved")
    quality_score: float = Field(..., description="Quality score improvement")
    created_at: datetime = Field(..., description="Optimization timestamp")

# Cognomega AI - Complete API Documentation

## 🚀 Overview

This document provides comprehensive API documentation for all Cognomega AI systems, including the latest features: Smart Coding AI, Swarm AI, Architecture Generator, Agent Mode, and Unified Meta AI Orchestrator.

## 📋 API Endpoints Summary

| System | Base Path | Description |
|--------|-----------|-------------|
| Authentication | `/api/v0/auth` | User authentication and management |
| Voice Processing | `/api/v0/voice` | Voice-to-text and intent processing |
| Payments | `/api/v0/payments` | Payment processing and billing |
| Apps | `/api/v0/apps` | App generation and management |
| Admin | `/api/v0/admin` | Administrative functions |
| Smart Coding AI | `/api/v0/smart-coding-ai` | Code completion and suggestions |
| AI Agents | `/api/v0/ai-agents` | AI agent management and interaction |
| Meta Orchestrator | `/api/v0/meta-orchestrator` | Meta AI orchestration |
| Swarm AI | `/api/v0/swarm-ai` | Multi-agent collaboration |
| Architecture Generator | `/api/v0/architecture-generator` | System architecture generation |
| Agent Mode | `/api/v0/agent-mode` | Autonomous development assistance |

## 🔐 Authentication

All API endpoints require authentication unless specified otherwise. Use JWT tokens obtained from the authentication endpoints.

### Authentication Headers
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

## 🤖 Smart Coding AI - GitHub Copilot-like Features

### Base Path: `/api/v0/smart-coding-ai`

#### **In-line Code Completion**

**POST** `/inline-completion`
```json
{
  "code": "def calculate_sum(",
  "language": "python",
  "context": "math operations",
  "max_tokens": 100,
  "temperature": 0.1
}
```

**Response:**
```json
{
  "completion": "a, b):\n    return a + b",
  "confidence": 0.95,
  "metadata": {
    "language": "python",
    "context_aware": true,
    "performance_metrics": {
      "response_time": 0.2,
      "tokens_generated": 15
    }
  }
}
```

#### **Streaming Completions**

**POST** `/inline-completion/stream`
```json
{
  "code": "async def fetch_data(",
  "language": "python",
  "stream": true
}
```

**Response:** Server-Sent Events stream

#### **Context-Aware Completions**

**POST** `/inline-completion/context-aware`
```json
{
  "code": "class UserService:",
  "language": "python",
  "context": {
    "file_type": "service",
    "framework": "fastapi",
    "patterns": ["dependency_injection", "async_operations"]
  }
}
```

#### **Intelligent Completions**

**POST** `/inline-completion/intelligent`
```json
{
  "code": "def process_payment(",
  "language": "python",
  "intelligence_level": "high",
  "optimization": true
}
```

#### **Multiple Suggestions**

**POST** `/inline-completion/suggestions`
```json
{
  "code": "def validate_email(",
  "language": "python",
  "max_suggestions": 5
}
```

**Response:**
```json
{
  "suggestions": [
    {
      "completion": "email: str) -> bool:",
      "confidence": 0.92,
      "description": "Type hint with validation"
    },
    {
      "completion": "email: str) -> bool:\n    import re\n    pattern = r'^[\\w\\.-]+@[\\w\\.-]+\\.\\w+$'",
      "confidence": 0.88,
      "description": "Full implementation with regex"
    }
  ]
}
```

#### **Confidence Scoring**

**POST** `/inline-completion/confidence`
```json
{
  "completion": "def calculate_tax(amount: float) -> float:",
  "language": "python",
  "context": "financial calculations"
}
```

**Response:**
```json
{
  "confidence_score": 0.94,
  "factors": {
    "syntax_correctness": 0.98,
    "context_relevance": 0.92,
    "pattern_matching": 0.96,
    "semantic_understanding": 0.90
  }
}
```

#### **Performance Metrics**

**GET** `/inline-completion/performance`

**Response:**
```json
{
  "metrics": {
    "average_response_time": 0.15,
    "throughput": 1000,
    "accuracy_rate": 0.96,
    "cache_hit_rate": 0.78,
    "error_rate": 0.02
  }
}
```

#### **Service Status**

**GET** `/inline-completion/status`

**Response:**
```json
{
  "status": "operational",
  "version": "1.0.0",
  "features": {
    "streaming": true,
    "context_aware": true,
    "intelligent": true,
    "multi_suggestions": true
  }
}
```

## 🐝 Swarm AI - Multi-Agent Collaboration

### Base Path: `/api/v0/swarm-ai`

#### **Swarm Management**

**POST** `/swarms`
```json
{
  "name": "Code Review Swarm",
  "description": "Multi-agent code review and optimization",
  "max_agents": 5,
  "specialization": "code_analysis",
  "consensus_threshold": 0.8
}
```

**Response:**
```json
{
  "swarm_id": "swarm_123",
  "name": "Code Review Swarm",
  "status": "active",
  "agents": [],
  "created_at": "2024-01-01T00:00:00Z"
}
```

**GET** `/swarms`
**GET** `/swarms/{swarm_id}`
**PUT** `/swarms/{swarm_id}`
**DELETE** `/swarms/{swarm_id}`

#### **Agent Management**

**POST** `/swarms/{swarm_id}/agents`
```json
{
  "name": "Syntax Validator",
  "role": "syntax_validation",
  "capabilities": ["python", "javascript", "typescript"],
  "specialization": "code_quality"
}
```

**Response:**
```json
{
  "agent_id": "agent_456",
  "name": "Syntax Validator",
  "role": "syntax_validation",
  "status": "active",
  "performance_metrics": {
    "accuracy": 0.98,
    "response_time": 0.1,
    "tasks_completed": 0
  }
}
```

#### **Task Execution**

**POST** `/swarms/{swarm_id}/tasks`
```json
{
  "description": "Review and optimize this Python function",
  "code": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
  "language": "python",
  "requirements": ["performance", "readability", "best_practices"]
}
```

**Response:**
```json
{
  "task_id": "task_789",
  "status": "in_progress",
  "agents_assigned": ["agent_456", "agent_789"],
  "estimated_completion": "2024-01-01T00:05:00Z"
}
```

**GET** `/swarms/{swarm_id}/tasks/{task_id}`

**Response:**
```json
{
  "task_id": "task_789",
  "status": "completed",
  "result": {
    "optimized_code": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b",
    "improvements": [
      "Changed from recursive to iterative approach",
      "Reduced time complexity from O(2^n) to O(n)",
      "Added proper variable naming"
    ],
    "consensus_score": 0.92,
    "agent_contributions": {
      "agent_456": "Performance optimization",
      "agent_789": "Code readability improvements"
    }
  }
}
```

#### **Batch Operations**

**POST** `/swarms/{swarm_id}/batch`
```json
{
  "tasks": [
    {
      "description": "Optimize function A",
      "code": "def func_a(): ..."
    },
    {
      "description": "Review function B", 
      "code": "def func_b(): ..."
    }
  ],
  "parallel": true
}
```

#### **Health Monitoring**

**GET** `/swarms/{swarm_id}/health`

**Response:**
```json
{
  "swarm_health": "healthy",
  "agents": [
    {
      "agent_id": "agent_456",
      "status": "active",
      "performance": {
        "cpu_usage": 0.15,
        "memory_usage": 0.23,
        "response_time": 0.1
      }
    }
  ],
  "overall_metrics": {
    "active_agents": 5,
    "average_response_time": 0.12,
    "success_rate": 0.98
  }
}
```

## 🏗️ Architecture Generator

### Base Path: `/api/v0/architecture-generator`

#### **Architecture Management**

**POST** `/architectures`
```json
{
  "name": "E-commerce Platform",
  "type": "microservices",
  "description": "Scalable e-commerce platform architecture",
  "components": [
    {
      "name": "user-service",
      "type": "service",
      "responsibilities": ["authentication", "user_management"]
    },
    {
      "name": "product-service", 
      "type": "service",
      "responsibilities": ["product_catalog", "inventory"]
    }
  ],
  "requirements": ["scalability", "high_availability", "security"]
}
```

**Response:**
```json
{
  "architecture_id": "arch_123",
  "name": "E-commerce Platform",
  "type": "microservices",
  "status": "generated",
  "components": [
    {
      "name": "user-service",
      "type": "service",
      "dependencies": ["database", "redis"],
      "endpoints": ["/auth", "/users"]
    }
  ],
  "diagram_url": "/api/v0/architecture-generator/diagrams/arch_123"
}
```

#### **Diagram Generation**

**POST** `/diagrams`
```json
{
  "architecture_id": "arch_123",
  "format": "mermaid",
  "style": "modern",
  "include_relationships": true
}
```

**Response:**
```json
{
  "diagram_id": "diagram_456",
  "format": "mermaid",
  "content": "graph TD\n    A[User Service] --> B[Database]\n    A --> C[Redis]",
  "image_url": "/api/v0/architecture-generator/diagrams/diagram_456/image",
  "svg_url": "/api/v0/architecture-generator/diagrams/diagram_456/svg"
}
```

#### **Architecture Analysis**

**POST** `/architectures/{architecture_id}/analyze`
```json
{
  "analysis_type": "performance",
  "focus_areas": ["scalability", "bottlenecks"]
}
```

**Response:**
```json
{
  "analysis_id": "analysis_789",
  "type": "performance",
  "results": {
    "scalability_score": 8.5,
    "bottlenecks": [
      {
        "component": "database",
        "issue": "Single point of failure",
        "recommendation": "Implement database clustering"
      }
    ],
    "recommendations": [
      "Add load balancer",
      "Implement caching layer",
      "Use microservices pattern"
    ]
  }
}
```

#### **Template Library**

**GET** `/templates`
**GET** `/templates/{template_id}`

**Response:**
```json
{
  "templates": [
    {
      "id": "template_1",
      "name": "REST API Microservices",
      "type": "microservices",
      "description": "Standard REST API microservices architecture",
      "components": ["api_gateway", "user_service", "product_service"],
      "use_cases": ["web_applications", "mobile_backends"]
    }
  ]
}
```

## 🤖 Agent Mode - Autonomous Development

### Base Path: `/api/v0/agent-mode`

#### **Codebase Analysis**

**POST** `/analyze`
```json
{
  "description": "Add user authentication with Supabase, including login, signup, and protected routes",
  "context": {
    "project_type": "nextjs",
    "framework": "react",
    "database": "supabase",
    "auth_provider": "supabase"
  },
  "requirements": ["secure", "scalable", "user_friendly"]
}
```

**Response:**
```json
{
  "analysis_id": "analysis_123",
  "status": "analyzing",
  "estimated_time": "2-3 minutes",
  "files_to_modify": [
    "app/auth/page.tsx",
    "lib/auth.ts", 
    "components/AuthForm.tsx"
  ],
  "dependencies_to_add": ["@supabase/supabase-js", "@supabase/auth-helpers-nextjs"]
}
```

#### **Implementation Planning**

**GET** `/analyze/{analysis_id}`

**Response:**
```json
{
  "analysis_id": "analysis_123",
  "status": "completed",
  "plan": {
    "steps": [
      {
        "step": 1,
        "action": "Install dependencies",
        "files": ["package.json"],
        "commands": ["npm install @supabase/supabase-js"]
      },
      {
        "step": 2,
        "action": "Create auth configuration",
        "files": ["lib/supabase.ts"],
        "description": "Set up Supabase client configuration"
      }
    ],
    "estimated_duration": "15 minutes",
    "complexity": "medium"
  }
}
```

#### **Autonomous Implementation**

**POST** `/implement`
```json
{
  "analysis_id": "analysis_123",
  "auto_implement": true,
  "backup_original": true,
  "add_comments": true
}
```

**Response:**
```json
{
  "implementation_id": "impl_456",
  "status": "implementing",
  "progress": 0.0,
  "files_modified": [],
  "dependencies_added": [],
  "tests_created": []
}
```

#### **Implementation Status**

**GET** `/implement/{implementation_id}`

**Response:**
```json
{
  "implementation_id": "impl_456",
  "status": "completed",
  "progress": 1.0,
  "files_modified": [
    {
      "file": "app/auth/page.tsx",
      "changes": "Added login/signup forms",
      "lines_added": 45,
      "lines_modified": 0
    }
  ],
  "dependencies_added": ["@supabase/supabase-js"],
  "tests_created": ["__tests__/auth.test.tsx"],
  "comments_added": 12,
  "verification_status": "passed"
}
```

#### **Verification & Testing**

**POST** `/verify`
```json
{
  "implementation_id": "impl_456",
  "run_tests": true,
  "check_syntax": true,
  "validate_imports": true
}
```

**Response:**
```json
{
  "verification_id": "verify_789",
  "status": "completed",
  "results": {
    "syntax_check": "passed",
    "import_validation": "passed",
    "tests_passed": 5,
    "tests_failed": 0,
    "coverage": 0.85
  }
}
```

## 🎯 Meta AI Orchestrator

### Base Path: `/api/v0/meta-orchestrator`

#### **Orchestration Status**

**GET** `/status`

**Response:**
```json
{
  "status": "operational",
  "version": "1.0.0",
  "components": {
    "smart_coding_ai": {
      "status": "healthy",
      "accuracy": 100.0,
      "performance": "optimal"
    },
    "swarm_ai": {
      "status": "healthy", 
      "active_swarms": 3,
      "performance": "optimal"
    },
    "architecture_generator": {
      "status": "healthy",
      "generated_architectures": 15,
      "performance": "optimal"
    }
  },
  "overall_harmony": 99.8,
  "governance_compliance": 100.0
}
```

#### **Performance Optimization**

**POST** `/optimize`
```json
{
  "target_component": "smart_coding_ai",
  "optimization_level": "maximum",
  "focus_areas": ["accuracy", "response_time"]
}
```

**Response:**
```json
{
  "optimization_id": "opt_123",
  "status": "in_progress",
  "estimated_duration": "5 minutes",
  "target_improvements": {
    "accuracy": "100%",
    "response_time": "0.1s"
  }
}
```

#### **Governance Rules**

**GET** `/governance/rules`
**POST** `/governance/rules`
**PUT** `/governance/rules/{rule_id}`
**DELETE** `/governance/rules/{rule_id}`

#### **Harmony Monitoring**

**GET** `/harmony`

**Response:**
```json
{
  "harmony_score": 99.8,
  "components": {
    "smart_coding_ai": 100.0,
    "swarm_ai": 99.5,
    "architecture_generator": 100.0,
    "agent_mode": 99.0
  },
  "recommendations": [
    "Agent Mode performance can be improved",
    "Consider optimizing response times"
  ]
}
```

## 📊 System Status

### **GET** `/api/v0/status`

**Response:**
```json
{
  "api": "Voice-to-App SaaS Platform",
  "version": "1.0.0",
  "status": "operational",
  "features": {
    "voice_processing": true,
    "app_generation": true,
    "payments": true,
    "gamification": true,
    "smart_coding_ai": true,
    "ai_agents": true,
    "meta_orchestrator": true,
    "swarm_ai": true,
    "architecture_generator": true,
    "agent_mode": true,
    "local_ai": true,
    "cloud_ai": true
  },
  "endpoints": {
    "auth": "/api/v0/auth",
    "voice": "/api/v0/voice",
    "payments": "/api/v0/payments",
    "apps": "/api/v0/apps",
    "admin": "/api/v0/admin",
    "smart_coding_ai": "/api/v0/smart-coding-ai",
    "ai_agents": "/api/v0/ai-agents",
    "meta_orchestrator": "/api/v0/meta-orchestrator",
    "swarm_ai": "/api/v0/swarm-ai",
    "architecture_generator": "/api/v0/architecture-generator",
    "agent_mode": "/api/v0/agent-mode"
  }
}
```

## 🔧 Error Handling

All API endpoints return consistent error responses:

```json
{
  "error": true,
  "message": "Error description",
  "status_code": 400,
  "path": "/api/v0/endpoint",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Common HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## 🚀 Rate Limiting

All endpoints are rate-limited:
- **Standard endpoints**: 100 requests/minute
- **AI endpoints**: 50 requests/minute
- **Streaming endpoints**: 10 concurrent connections

Rate limit headers:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

## 📝 Authentication & Authorization

### JWT Token Structure
```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "role": "user",
  "permissions": ["read", "write"],
  "exp": 1640995200,
  "iat": 1640908800
}
```

### Required Headers
```http
Authorization: Bearer <jwt_token>
Content-Type: application/json
X-API-Version: v0
```

---

**Last Updated**: January 2024  
**Version**: 1.0.0  
**Maintainer**: Cognomega AI Team

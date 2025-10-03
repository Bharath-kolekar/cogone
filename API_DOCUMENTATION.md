# API Documentation - Voice-to-App SaaS Platform

## Base URLs
- **Development**: `http://localhost:8000`
- **Production**: `https://your-api-domain.com`

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Response Format
All API responses follow this format:
```json
{
  "data": {},
  "message": "Success message",
  "status": "success|error"
}
```

## Authentication Endpoints

### POST /auth/register
Register a new user account.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe"
}
```

**Response**:
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe",
    "created_at": "2025-10-03T00:00:00Z"
  },
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "expires_in": 3600
}
```

### POST /auth/login
Login with email and password.

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "two_factor_code": "123456" // Optional, required if 2FA enabled
}
```

**Response**:
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "full_name": "John Doe"
  },
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "expires_in": 3600,
  "requires_2fa": false // true if 2FA code required
}
```

### POST /auth/refresh
Refresh access token using refresh token.

**Request Body**:
```json
{
  "refresh_token": "refresh_token"
}
```

## Two-Factor Authentication Endpoints

### POST /auth/2fa/setup
Setup 2FA for authenticated user.

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "secret": "TOTP_SECRET",
  "qr_code": "data:image/png;base64,iVBOR...",
  "backup_codes": ["12345678", "87654321"],
  "manual_entry_key": "TOTP_SECRET"
}
```

### POST /auth/2fa/verify
Verify 2FA setup with TOTP code.

**Request Body**:
```json
{
  "code": "123456"
}
```

**Response**:
```json
{
  "success": true,
  "message": "2FA enabled successfully"
}
```

### GET /auth/2fa/status
Get 2FA status for authenticated user.

**Response**:
```json
{
  "enabled": true,
  "backup_codes_count": 8,
  "verified_at": "2025-10-03T00:00:00Z",
  "created_at": "2025-10-03T00:00:00Z"
}
```

### DELETE /auth/2fa/disable
Disable 2FA for authenticated user.

**Response**:
```json
{
  "success": true,
  "message": "2FA disabled successfully"
}
```

### POST /auth/2fa/backup-codes
Regenerate backup codes for 2FA.

**Response**:
```json
{
  "backup_codes": ["new12345", "new54321"]
}
```

### POST /auth/2fa/verify-login
Verify 2FA code during login.

**Request Body**:
```json
{
  "user_id": "uuid",
  "code": "123456"
}
```

**Response**:
```json
{
  "success": true,
  "requires_2fa": false,
  "message": "Login successful"
}
```

## User Management Endpoints

### GET /users/me
Get current user profile.

**Headers**: `Authorization: Bearer <token>`

**Response**:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "full_name": "John Doe",
  "created_at": "2025-10-03T00:00:00Z",
  "updated_at": "2025-10-03T00:00:00Z"
}
```

### PUT /users/me
Update current user profile.

**Request Body**:
```json
{
  "full_name": "John Smith",
  "email": "newemail@example.com"
}
```

## Voice Processing Endpoints

### POST /voice/record
Start voice recording session.

**Request Body**:
```json
{
  "language": "en-IN",
  "duration_limit": 60
}
```

**Response**:
```json
{
  "session_id": "uuid",
  "status": "recording",
  "expires_at": "2025-10-03T00:01:00Z"
}
```

### POST /voice/process
Process recorded voice and generate transcript.

**Request Body**:
```json
{
  "session_id": "uuid",
  "audio_data": "base64_encoded_audio"
}
```

**Response**:
```json
{
  "transcript": "Create a todo app with authentication",
  "confidence": 0.95,
  "language": "en-IN"
}
```

### POST /voice/generate-app
Generate app from voice command.

**Request Body**:
```json
{
  "transcript": "Create a todo app with authentication",
  "session_id": "uuid"
}
```

**Response**:
```json
{
  "app_id": "uuid",
  "status": "generating",
  "estimated_completion": "2025-10-03T00:05:00Z"
}
```

## App Management Endpoints

### GET /apps
Get user's generated apps.

**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10)
- `status`: Filter by status (draft, generating, completed, failed)

**Response**:
```json
{
  "apps": [
    {
      "id": "uuid",
      "title": "Todo App",
      "description": "A simple todo application",
      "status": "completed",
      "preview_url": "https://preview.example.com/app/uuid",
      "created_at": "2025-10-03T00:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "limit": 10
}
```

### GET /apps/{app_id}
Get specific app details.

**Response**:
```json
{
  "id": "uuid",
  "title": "Todo App",
  "description": "A simple todo application",
  "status": "completed",
  "preview_url": "https://preview.example.com/app/uuid",
  "source_code_url": "https://github.com/user/todo-app",
  "created_at": "2025-10-03T00:00:00Z",
  "updated_at": "2025-10-03T00:00:00Z"
}
```

### DELETE /apps/{app_id}
Delete an app.

**Response**:
```json
{
  "success": true,
  "message": "App deleted successfully"
}
```

## Payment Endpoints

### POST /payments/create-intent
Create payment intent for subscription.

**Request Body**:
```json
{
  "plan_id": "pro_monthly",
  "amount": 2999,
  "currency": "INR"
}
```

**Response**:
```json
{
  "client_secret": "pi_xxx_secret_xxx",
  "payment_intent_id": "pi_xxx"
}
```

### POST /payments/confirm
Confirm payment after successful processing.

**Request Body**:
```json
{
  "payment_intent_id": "pi_xxx",
  "subscription_id": "sub_xxx"
}
```

**Response**:
```json
{
  "success": true,
  "subscription": {
    "id": "sub_xxx",
    "status": "active",
    "plan": "pro_monthly",
    "current_period_end": "2025-11-03T00:00:00Z"
  }
}
```

### GET /payments/subscription
Get current user's subscription status.

**Response**:
```json
{
  "subscription": {
    "id": "sub_xxx",
    "status": "active",
    "plan": "pro_monthly",
    "current_period_end": "2025-11-03T00:00:00Z"
  }
}
```

## Goal Integrity Endpoints

### POST /goals/define
Define a new goal for the system.

**Request Body**:
```json
{
  "name": "response_time_goal",
  "type": "performance",
  "description": "Maintain API response time under 200ms",
  "target_value": 200,
  "unit": "milliseconds",
  "priority": "high"
}
```

**Response**:
```json
{
  "goal_id": "uuid",
  "status": "active",
  "created_at": "2025-10-03T00:00:00Z"
}
```

### GET /goals
Get all defined goals.

**Response**:
```json
{
  "goals": [
    {
      "id": "uuid",
      "name": "response_time_goal",
      "type": "performance",
      "status": "active",
      "current_value": 150,
      "target_value": 200,
      "last_checked": "2025-10-03T00:00:00Z"
    }
  ]
}
```

### POST /goals/{goal_id}/verify
Manually verify goal integrity.

**Response**:
```json
{
  "goal_id": "uuid",
  "status": "compliant",
  "value": 150,
  "checked_at": "2025-10-03T00:00:00Z"
}
```

### GET /goals/{goal_id}/violations
Get violations for a specific goal.

**Response**:
```json
{
  "violations": [
    {
      "id": "uuid",
      "goal_id": "uuid",
      "severity": "medium",
      "description": "API response time exceeded 200ms",
      "detected_at": "2025-10-03T00:00:00Z",
      "resolved": false
    }
  ]
}
```

## Webhook Endpoints

### POST /webhooks/stripe
Handle Stripe webhook events.

**Headers**:
```
Stripe-Signature: t=timestamp,v1=signature
```

### POST /webhooks/razorpay
Handle Razorpay webhook events.

## Error Responses

### 400 Bad Request
```json
{
  "error": "Validation Error",
  "message": "Invalid request data",
  "details": {
    "field": "email",
    "error": "Invalid email format"
  }
}
```

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Resource not found"
}
```

### 429 Rate Limited
```json
{
  "error": "Rate Limited",
  "message": "Too many requests",
  "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## Rate Limiting
- **Authentication endpoints**: 5 requests per minute
- **General API**: 100 requests per minute
- **Voice processing**: 10 requests per minute
- **Payment endpoints**: 20 requests per minute

## WebSocket Endpoints

### WS /ws/voice/{session_id}
Real-time voice recording and processing updates.

**Messages**:
```json
{
  "type": "recording_started",
  "session_id": "uuid",
  "timestamp": "2025-10-03T00:00:00Z"
}
```

```json
{
  "type": "transcript_update",
  "session_id": "uuid",
  "transcript": "partial transcript",
  "confidence": 0.8
}
```

```json
{
  "type": "app_generation_progress",
  "app_id": "uuid",
  "progress": 75,
  "status": "generating"
}
```

---
## 🤖 AI Agent System API

### Agent Management

#### POST /ai-agents
Create a new AI agent.

**Request Body**:
```json
{
  "name": "My AI Assistant",
  "description": "A helpful assistant for daily tasks",
  "type": "personal_assistant",
  "capabilities": ["natural_language", "scheduling"],
  "system_prompt": "You are a helpful personal assistant.",
  "is_public": false
}
```

#### GET /ai-agents
List AI agents with filtering and pagination.

#### POST /ai-agents/{agent_id}/interact
Send a message to an AI agent.

**Request Body**:
```json
{
  "agent_id": "uuid",
  "message": "Hello, how can you help me?",
  "context": {"user_id": "uuid"},
  "session_id": "session_123"
}
```

#### POST /ai-agents/{agent_id}/tasks
Create a new task for an AI agent.

#### GET /ai-agents/{agent_id}/analytics
Get analytics for a specific agent.

### AI Agent Features
- **Zero-Cost Infrastructure**: Local LLM models with no cloud costs
- **Multiple Agent Types**: Voice Assistant, Code Generator, Data Analyzer, Content Creator, Personal Assistant
- **Real-time Chat**: Live conversation interface with streaming responses
- **Memory & Learning**: Conversation memory and pattern learning
- **Task Automation**: Automated task execution and workflow management
- **Analytics Dashboard**: Performance metrics and usage monitoring

---

**Last Updated**: December 2024  
**API Version**: 1.0

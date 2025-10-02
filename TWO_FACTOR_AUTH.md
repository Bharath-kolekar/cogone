# Two-Factor Authentication (2FA) Implementation

This document describes the implementation of Two-Factor Authentication (2FA) using TOTP (Time-based One-Time Password) for the Voice-to-App SaaS Platform.

## Features

- **TOTP-based 2FA**: Uses industry-standard TOTP for generating time-based codes
- **QR Code Setup**: Easy setup with QR codes for authenticator apps
- **Backup Codes**: One-time backup codes for account recovery
- **Secure Storage**: TOTP secrets encrypted and stored securely
- **User-Friendly Interface**: Intuitive setup and management interface

## Architecture

### Backend Components

1. **TOTP Service** (`backend/app/services/totp_service.py`)
   - Generates TOTP secrets
   - Creates QR codes for setup
   - Verifies TOTP codes
   - Manages backup codes
   - Handles 2FA status

2. **Database Schema** (`supabase/schema.sql`)
   - `user_2fa` table stores TOTP secrets and backup codes
   - Row-level security policies for data protection
   - Proper indexing for performance

3. **API Endpoints** (`backend/app/routers/auth.py`)
   - `POST /auth/2fa/setup` - Initialize 2FA setup
   - `POST /auth/2fa/verify` - Verify and enable 2FA
   - `GET /auth/2fa/status` - Get 2FA status
   - `DELETE /auth/2fa/disable` - Disable 2FA
   - `POST /auth/2fa/backup-codes` - Regenerate backup codes
   - `POST /auth/2fa/verify-login` - Verify 2FA during login

4. **Authentication Flow** (`backend/app/services/auth_service.py`)
   - Modified login flow to check for 2FA
   - Returns appropriate responses based on 2FA status

### Frontend Components

1. **TwoFactorSetup** (`frontend/components/TwoFactorSetup.tsx`)
   - QR code display for authenticator setup
   - Manual key entry option
   - Step-by-step setup process
   - Backup codes display and download

2. **TwoFactorLogin** (`frontend/components/TwoFactorLogin.tsx`)
   - 2FA code input during login
   - Supports both TOTP codes and backup codes

3. **TwoFactorSettings** (`frontend/components/TwoFactorSettings.tsx`)
   - 2FA status display
   - Enable/disable 2FA
   - Backup codes management

4. **Settings Page** (`frontend/app/settings/page.tsx`)
   - Complete settings interface
   - Integration with 2FA components

## Setup Process

### 1. User Initiates 2FA Setup
```typescript
// User clicks "Enable 2FA" in settings
const response = await fetch('/api/auth/2fa/setup', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
```

### 2. QR Code Generation
- Backend generates a TOTP secret
- Creates QR code with TOTP URI
- Returns QR code image and manual entry key

### 3. User Scans QR Code
- User opens authenticator app (Google Authenticator, Authy, etc.)
- Scans QR code to add account
- Or manually enters the secret key

### 4. Verification
```typescript
// User enters 6-digit code from authenticator
const response = await fetch('/api/auth/2fa/verify', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
  },
  body: JSON.stringify({ code: '123456' }),
});
```

### 5. Backup Codes
- System generates 10 backup codes
- User downloads and stores them securely
- Each backup code can only be used once

## Login Flow with 2FA

### 1. Initial Login
```typescript
const response = await fetch('/api/auth/login', {
  method: 'POST',
  body: JSON.stringify({ email, password }),
});
```

### 2. 2FA Check
- Backend checks if user has 2FA enabled
- If enabled, returns `requires_2fa: true`

### 3. 2FA Verification
```typescript
const response = await fetch('/api/auth/2fa/verify-login', {
  method: 'POST',
  body: JSON.stringify({ user_id, code }),
});
```

### 4. Complete Login
- If 2FA code is valid, login completes
- User receives access and refresh tokens

## Security Features

### 1. TOTP Implementation
- Uses `pyotp` library for RFC 6238 compliance
- 30-second time windows
- 6-digit codes
- SHA-1 algorithm (industry standard)

### 2. Secret Management
- TOTP secrets stored in database
- No secrets transmitted in API responses
- Proper encryption and access controls

### 3. Backup Codes
- Cryptographically secure random generation
- One-time use only
- Automatic regeneration available

### 4. Database Security
- Row-level security policies
- User can only access their own 2FA data
- Service role has full access for operations

## API Reference

### Setup 2FA
```http
POST /auth/2fa/setup
Authorization: Bearer <token>

Response:
{
  "secret": "base32_secret",
  "qr_code": "data:image/png;base64,...",
  "backup_codes": ["ABC123", "DEF456", ...],
  "manual_entry_key": "base32_secret"
}
```

### Verify 2FA Setup
```http
POST /auth/2fa/verify
Authorization: Bearer <token>
Content-Type: application/json

{
  "code": "123456"
}

Response:
{
  "success": true,
  "message": "2FA has been successfully enabled"
}
```

### Get 2FA Status
```http
GET /auth/2fa/status
Authorization: Bearer <token>

Response:
{
  "enabled": true,
  "backup_codes_count": 8,
  "verified_at": "2024-01-01T12:00:00Z",
  "created_at": "2024-01-01T11:30:00Z"
}
```

### Verify 2FA During Login
```http
POST /auth/2fa/verify-login
Content-Type: application/json

{
  "user_id": "user_uuid",
  "code": "123456"
}

Response:
{
  "success": true,
  "message": "2FA verification successful"
}
```

## Dependencies

### Backend
- `pyotp==2.9.0` - TOTP implementation
- `qrcode[pil]==7.4.2` - QR code generation

### Frontend
- React components for UI
- Fetch API for HTTP requests
- Local storage for token management

## Testing

### Manual Testing
1. Enable 2FA for a user account
2. Scan QR code with authenticator app
3. Verify setup with TOTP code
4. Test login with 2FA enabled
5. Test backup code usage
6. Test 2FA disable functionality

### Security Testing
- Verify TOTP codes expire after 30 seconds
- Test invalid code rejection
- Verify backup codes are single-use
- Test unauthorized access prevention

## Deployment Notes

1. **Environment Variables**
   - Set `BACKEND_URL` in frontend environment
   - Ensure database migrations are applied
   - Configure proper CORS settings

2. **Database Migration**
   ```sql
   -- Apply the user_2fa table creation
   -- Run the schema updates from supabase/schema.sql
   ```

3. **Dependencies**
   ```bash
   # Backend
   pip install pyotp qrcode[pil]
   
   # Frontend dependencies should already be installed
   ```

## Troubleshooting

### Common Issues

1. **QR Code Not Working**
   - Check if authenticator app supports TOTP
   - Verify manual entry key format
   - Ensure proper base32 encoding

2. **Invalid TOTP Code**
   - Check device time synchronization
   - Verify 30-second time window
   - Ensure correct secret key

3. **Backup Codes Not Working**
   - Verify codes haven't been used already
   - Check for typos in code entry
   - Ensure proper code format

### Error Handling

The system includes comprehensive error handling:
- Invalid TOTP codes return appropriate error messages
- Network failures are handled gracefully
- Database errors are logged and reported
- User-friendly error messages in UI

## Future Enhancements

1. **SMS 2FA**: Add SMS-based 2FA as alternative
2. **Hardware Keys**: Support for FIDO2/WebAuthn
3. **Push Notifications**: Mobile app push-based 2FA
4. **Advanced Policies**: Configurable 2FA requirements per user tier
5. **Audit Logging**: Track 2FA events for security monitoring

## Security Considerations

1. **Rate Limiting**: Implement rate limiting for 2FA attempts
2. **Lockout Policies**: Temporary account lockout after failed attempts
3. **Device Management**: Track trusted devices
4. **Emergency Access**: Admin override capabilities
5. **Compliance**: Ensure GDPR/CCPA compliance for data handling

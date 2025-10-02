"""
TOTP (Time-based One-Time Password) service for 2FA
"""

import pyotp
import qrcode
import base64
import io
import secrets
import structlog
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.database import get_supabase_client

logger = structlog.get_logger()


class TOTPService:
    """TOTP service for 2FA authentication"""
    
    def __init__(self):
        self.supabase = get_supabase_client()
        self.issuer_name = getattr(settings, 'APP_NAME', 'Voice-to-App SaaS')
    
    def generate_secret(self) -> str:
        """Generate a new TOTP secret"""
        return pyotp.random_base32()
    
    def generate_qr_code(self, user_email: str, secret: str) -> str:
        """Generate QR code for authenticator app setup"""
        try:
            # Create TOTP URI
            totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
                name=user_email,
                issuer_name=self.issuer_name
            )
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(totp_uri)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64 string
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            return f"data:image/png;base64,{img_base64}"
            
        except Exception as e:
            logger.error("QR code generation failed", error=str(e))
            raise e
    
    def verify_totp_code(self, secret: str, code: str, window: int = 1) -> bool:
        """Verify TOTP code"""
        try:
            totp = pyotp.TOTP(secret)
            return totp.verify(code, valid_window=window)
        except Exception as e:
            logger.error("TOTP verification failed", error=str(e))
            return False
    
    def generate_backup_codes(self, count: int = 10) -> List[str]:
        """Generate backup codes for 2FA"""
        return [secrets.token_hex(4).upper() for _ in range(count)]
    
    async def setup_2fa(self, user_id: str, user_email: str) -> Dict[str, Any]:
        """Setup 2FA for user"""
        try:
            # Generate secret and QR code
            secret = self.generate_secret()
            qr_code = self.generate_qr_code(user_email, secret)
            backup_codes = self.generate_backup_codes()
            
            # Store in database (temporarily, will be activated after verification)
            self.supabase.table("user_2fa").insert({
                "user_id": user_id,
                "totp_secret": secret,
                "backup_codes": backup_codes,
                "is_enabled": False,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }).execute()
            
            logger.info("2FA setup initiated", user_id=user_id)
            
            return {
                "secret": secret,
                "qr_code": qr_code,
                "backup_codes": backup_codes,
                "manual_entry_key": secret
            }
            
        except Exception as e:
            logger.error("2FA setup failed", error=str(e))
            raise e
    
    async def verify_and_enable_2fa(self, user_id: str, code: str) -> bool:
        """Verify TOTP code and enable 2FA"""
        try:
            # Get user's 2FA setup
            result = self.supabase.table("user_2fa").select("*").eq("user_id", user_id).eq("is_enabled", False).execute()
            
            if not result.data:
                raise Exception("2FA setup not found or already enabled")
            
            totp_data = result.data[0]
            secret = totp_data["totp_secret"]
            
            # Verify the code
            if not self.verify_totp_code(secret, code):
                raise Exception("Invalid TOTP code")
            
            # Enable 2FA
            self.supabase.table("user_2fa").update({
                "is_enabled": True,
                "verified_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }).eq("user_id", user_id).execute()
            
            logger.info("2FA enabled successfully", user_id=user_id)
            return True
            
        except Exception as e:
            logger.error("2FA verification failed", error=str(e))
            raise e
    
    async def disable_2fa(self, user_id: str) -> bool:
        """Disable 2FA for user"""
        try:
            # Delete 2FA record
            self.supabase.table("user_2fa").delete().eq("user_id", user_id).execute()
            
            logger.info("2FA disabled", user_id=user_id)
            return True
            
        except Exception as e:
            logger.error("2FA disable failed", error=str(e))
            raise e
    
    async def verify_2fa_code(self, user_id: str, code: str) -> bool:
        """Verify 2FA code for login"""
        try:
            # Get user's 2FA data
            result = self.supabase.table("user_2fa").select("*").eq("user_id", user_id).eq("is_enabled", True).execute()
            
            if not result.data:
                return False  # 2FA not enabled
            
            totp_data = result.data[0]
            secret = totp_data["totp_secret"]
            backup_codes = totp_data.get("backup_codes", [])
            
            # Check if it's a backup code
            if code in backup_codes:
                # Remove used backup code
                updated_backup_codes = [bc for bc in backup_codes if bc != code]
                self.supabase.table("user_2fa").update({
                    "backup_codes": updated_backup_codes,
                    "updated_at": datetime.utcnow().isoformat()
                }).eq("user_id", user_id).execute()
                
                logger.info("Backup code used", user_id=user_id)
                return True
            
            # Verify TOTP code
            if self.verify_totp_code(secret, code):
                logger.info("2FA verification successful", user_id=user_id)
                return True
            
            logger.warning("Invalid 2FA code", user_id=user_id)
            return False
            
        except Exception as e:
            logger.error("2FA verification failed", error=str(e))
            return False
    
    async def get_2fa_status(self, user_id: str) -> Dict[str, Any]:
        """Get 2FA status for user"""
        try:
            result = self.supabase.table("user_2fa").select("*").eq("user_id", user_id).execute()
            
            if not result.data:
                return {"enabled": False}
            
            totp_data = result.data[0]
            return {
                "enabled": totp_data["is_enabled"],
                "backup_codes_count": len(totp_data.get("backup_codes", [])),
                "verified_at": totp_data.get("verified_at"),
                "created_at": totp_data.get("created_at")
            }
            
        except Exception as e:
            logger.error("Failed to get 2FA status", error=str(e))
            return {"enabled": False}
    
    async def regenerate_backup_codes(self, user_id: str) -> List[str]:
        """Regenerate backup codes for user"""
        try:
            # Generate new backup codes
            new_backup_codes = self.generate_backup_codes()
            
            # Update in database
            self.supabase.table("user_2fa").update({
                "backup_codes": new_backup_codes,
                "updated_at": datetime.utcnow().isoformat()
            }).eq("user_id", user_id).eq("is_enabled", True).execute()
            
            logger.info("Backup codes regenerated", user_id=user_id)
            return new_backup_codes
            
        except Exception as e:
            logger.error("Backup codes regeneration failed", error=str(e))
            raise e

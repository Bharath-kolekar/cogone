"""
OAuth Service for Smart Coding AI
Preserves OAuth authentication capabilities
"""

import os
import secrets
import httpx
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from urllib.parse import urlencode
import structlog

logger = structlog.get_logger()


class OAuthService:
    """
    OAuth service for Smart Coding AI authentication
    Supports Google and GitHub OAuth providers
    """
    
    def __init__(self):
        self.oauth_configs = {
            "google": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
                "auth_url": "https://accounts.google.com/o/oauth2/v2/auth",
                "token_url": "https://oauth2.googleapis.com/token",
                "user_info_url": "https://www.googleapis.com/oauth2/v2/userinfo",
                "scopes": ["openid", "email", "profile"]
            },
            "github": {
                "client_id": os.getenv("GITHUB_CLIENT_ID", ""),
                "client_secret": os.getenv("GITHUB_CLIENT_SECRET", ""),
                "auth_url": "https://github.com/login/oauth/authorize",
                "token_url": "https://github.com/login/oauth/access_token",
                "user_info_url": "https://api.github.com/user",
                "scopes": ["user:email", "read:user"]
            }
        }
        self.state_store = {}  # In production, use Redis or database
    
    async def get_oauth_url(self, provider: str, redirect_uri: str = None) -> Dict[str, Any]:
        """
        Generate OAuth authorization URL
        Supports secure OAuth flow
        """
        try:
            if provider not in self.oauth_configs:
                raise ValueError(f"Unsupported OAuth provider: {provider}")
            
            config = self.oauth_configs[provider]
            
            # Generate state parameter for security
            state = secrets.token_urlsafe(32)
            
            # Store state temporarily
            self.state_store[state] = {
                "provider": provider,
                "redirect_uri": redirect_uri,
                "created_at": datetime.now(),
                "expires_at": datetime.now() + timedelta(minutes=10)
            }
            
            # Build authorization URL
            params = {
                "client_id": config["client_id"],
                "response_type": "code",
                "state": state,
                "scope": " ".join(config["scopes"])
            }
            
            if redirect_uri:
                params["redirect_uri"] = redirect_uri
            
            auth_url = f"{config['auth_url']}?{urlencode(params)}"
            
            logger.info("OAuth URL generated", provider=provider)
            return {
                "auth_url": auth_url,
                "state": state,
                "expires_at": datetime.now() + timedelta(minutes=10),
                "provider": provider
            }
            
        except Exception as e:
            logger.error(f"Failed to generate OAuth URL: {e}")
            raise
    
    async def handle_oauth_callback(self, provider: str, code: str, state: str) -> Dict[str, Any]:
        """
        Handle OAuth callback and exchange code for tokens
        Completes OAuth authentication flow
        """
        try:
            # Verify state parameter
            if state not in self.state_store:
                raise ValueError("Invalid state parameter")
            
            stored_state = self.state_store[state]
            if datetime.now() > stored_state["expires_at"]:
                del self.state_store[state]
                raise ValueError("State parameter expired")
            
            if stored_state["provider"] != provider:
                raise ValueError("Provider mismatch")
            
            # Clean up state
            del self.state_store[state]
            
            if provider not in self.oauth_configs:
                raise ValueError(f"Unsupported OAuth provider: {provider}")
            
            config = self.oauth_configs[provider]
            
            # Exchange code for access token
            token_data = await self._exchange_code_for_token(config, code, stored_state.get("redirect_uri"))
            
            # Get user information
            user_info = await self._get_user_info(config, token_data["access_token"])
            
            logger.info("OAuth callback handled successfully", provider=provider)
            return {
                "token_data": token_data,
                "user_info": user_info,
                "provider": provider
            }
            
        except Exception as e:
            logger.error(f"OAuth callback failed: {e}")
            raise
    
    async def refresh_oauth_token(self, provider: str, refresh_token: str) -> Dict[str, Any]:
        """Refresh OAuth access token"""
        try:
            if provider not in self.oauth_configs:
                raise ValueError(f"Unsupported OAuth provider: {provider}")
            
            config = self.oauth_configs[provider]
            
            token_data = {
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "refresh_token": refresh_token,
                "grant_type": "refresh_token"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(config["token_url"], data=token_data)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Token refresh failed: {e}")
            raise
    
    async def _exchange_code_for_token(self, config: Dict[str, Any], code: str, redirect_uri: str = None) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        try:
            token_data = {
                "client_id": config["client_id"],
                "client_secret": config["client_secret"],
                "code": code,
                "grant_type": "authorization_code"
            }
            
            if redirect_uri:
                token_data["redirect_uri"] = redirect_uri
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    config["token_url"],
                    data=token_data,
                    headers={"Accept": "application/json"}
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Token exchange failed: {e}")
            raise
    
    async def _get_user_info(self, config: Dict[str, Any], access_token: str) -> Dict[str, Any]:
        """Get user information from OAuth provider"""
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            
            async with httpx.AsyncClient() as client:
                response = await client.get(config["user_info_url"], headers=headers)
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
            raise

"""
OAuth2 Authentication Module for Business Integration Dashboard

This module provides OAuth2 authentication for various business systems
including Salesforce, Shopify, HubSpot, Zendesk, Slack, and Calendly.
"""

import base64
import hashlib
import secrets
import urllib.parse
import os
import json
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import requests
import logging

logger = logging.getLogger(__name__)

@dataclass
class OAuth2Config:
    """OAuth2 configuration for each service"""
    client_id: str
    client_secret: str
    authorization_url: str
    token_url: str
    redirect_uri: str
    scope: str
    service_name: str

@dataclass
class OAuth2Token:
    """OAuth2 token data"""
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    token_type: str = "Bearer"
    scope: Optional[str] = None

class OAuth2Manager:
    """Manages OAuth2 authentication for multiple services with optional disk persistence.

    Token persistence:
        - File path configurable via env var `OAUTH2_TOKEN_STORE` (default: .oauth_tokens.json)
        - Stores: access_token, refresh_token, expires_at (isoformat), token_type, scope
        - Persistence is best-effort: failures log warnings but do not raise.
    """

    def __init__(self, token_store_path: Optional[str] = None):
        self.tokens: Dict[str, OAuth2Token] = {}
        self.configs: Dict[str, OAuth2Config] = {}
        self.token_store_path = token_store_path or os.getenv("OAUTH2_TOKEN_STORE", ".oauth_tokens.json")
        self._load_tokens()
        
    def add_service_config(self, service_name: str, config: OAuth2Config):
        """Add OAuth2 configuration for a service"""
        self.configs[service_name] = config
        
    def generate_authorization_url(self, service_name: str, state: Optional[str] = None) -> Tuple[str, str]:
        """
        Generate authorization URL for OAuth2 flow
        
        Returns:
            Tuple of (authorization_url, state)
        """
        if service_name not in self.configs:
            raise ValueError(f"Service {service_name} not configured")
            
        config = self.configs[service_name]
        
        # Generate state parameter for CSRF protection
        if not state:
            state = secrets.token_urlsafe(32)
            
        # Generate PKCE code verifier and challenge for enhanced security
        code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        
        params = {
            'response_type': 'code',
            'client_id': config.client_id,
            'redirect_uri': config.redirect_uri,
            'scope': config.scope,
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }
        
        # Store code verifier for later use
        self._store_code_verifier(service_name, state, code_verifier)
        
        auth_url = f"{config.authorization_url}?{urllib.parse.urlencode(params)}"
        return auth_url, state
        
    def exchange_code_for_token(self, service_name: str, authorization_code: str, state: str) -> OAuth2Token:
        """
        Exchange authorization code for access token
        """
        if service_name not in self.configs:
            raise ValueError(f"Service {service_name} not configured")
            
        config = self.configs[service_name]
        code_verifier = self._get_code_verifier(service_name, state)
        
        data = {
            'grant_type': 'authorization_code',
            'client_id': config.client_id,
            'client_secret': config.client_secret,
            'code': authorization_code,
            'redirect_uri': config.redirect_uri,
            'code_verifier': code_verifier
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(config.token_url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            # Calculate expiration time
            expires_at = None
            if 'expires_in' in token_data:
                expires_at = datetime.now() + timedelta(seconds=int(token_data['expires_in']))
            
            token = OAuth2Token(
                access_token=token_data['access_token'],
                refresh_token=token_data.get('refresh_token'),
                expires_at=expires_at,
                token_type=token_data.get('token_type', 'Bearer'),
                scope=token_data.get('scope')
            )
            
            # Store token
            self.tokens[service_name] = token
            self._save_tokens()
            
            logger.info(f"Successfully obtained OAuth2 token for {service_name}")
            return token
            
        except requests.RequestException as e:
            logger.error(f"Failed to exchange code for token for {service_name}: {str(e)}")
            raise
            
    def refresh_token(self, service_name: str) -> OAuth2Token:
        """
        Refresh an expired access token
        """
        if service_name not in self.configs:
            raise ValueError(f"Service {service_name} not configured")
            
        if service_name not in self.tokens:
            raise ValueError(f"No token available for {service_name}")
            
        config = self.configs[service_name]
        current_token = self.tokens[service_name]
        
        if not current_token.refresh_token:
            raise ValueError(f"No refresh token available for {service_name}")
            
        data = {
            'grant_type': 'refresh_token',
            'client_id': config.client_id,
            'client_secret': config.client_secret,
            'refresh_token': current_token.refresh_token
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        try:
            response = requests.post(config.token_url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            
            # Calculate expiration time
            expires_at = None
            if 'expires_in' in token_data:
                expires_at = datetime.now() + timedelta(seconds=int(token_data['expires_in']))
            
            # Update token
            current_token.access_token = token_data['access_token']
            current_token.expires_at = expires_at
            
            # Update refresh token if provided
            if 'refresh_token' in token_data:
                current_token.refresh_token = token_data['refresh_token']
                
            logger.info(f"Successfully refreshed OAuth2 token for {service_name}")
            self._save_tokens()
            return current_token
            
        except requests.RequestException as e:
            logger.error(f"Failed to refresh token for {service_name}: {str(e)}")
            raise
            
    def get_valid_token(self, service_name: str) -> Optional[OAuth2Token]:
        """
        Get a valid access token, refreshing if necessary
        """
        if service_name not in self.tokens:
            return None
            
        token = self.tokens[service_name]
        
        # Check if token is expired
        if token.expires_at and datetime.now() >= token.expires_at:
            try:
                return self.refresh_token(service_name)
            except Exception as e:
                logger.error(f"Failed to refresh expired token for {service_name}: {str(e)}")
                return None
                
        return token
        
    def is_authenticated(self, service_name: str) -> bool:
        """Check if service is authenticated with valid token"""
        token = self.get_valid_token(service_name)
        return token is not None
        
    def revoke_token(self, service_name: str):
        """Revoke and remove stored token for a service"""
        if service_name in self.tokens:
            del self.tokens[service_name]
            logger.info(f"Revoked token for {service_name}")
            self._save_tokens()
            
    def _store_code_verifier(self, service_name: str, state: str, code_verifier: str):
        """Store PKCE code verifier temporarily"""
        # In production, store this in a secure cache/database
        if not hasattr(self, '_code_verifiers'):
            self._code_verifiers = {}
        self._code_verifiers[f"{service_name}:{state}"] = code_verifier
        
    def _get_code_verifier(self, service_name: str, state: str) -> str:
        """Retrieve stored PKCE code verifier"""
        if not hasattr(self, '_code_verifiers'):
            raise ValueError("No code verifier found")
        key = f"{service_name}:{state}"
        if key not in self._code_verifiers:
            raise ValueError("Invalid state parameter")
        return self._code_verifiers.pop(key)

    # ------------------------------
    # Persistence Helpers
    # ------------------------------
    def _save_tokens(self):
        """Persist tokens to disk (best-effort)."""
        if not self.token_store_path:
            return
        try:
            serializable = {}
            for svc, tok in self.tokens.items():
                serializable[svc] = {
                    "access_token": tok.access_token,
                    "refresh_token": tok.refresh_token,
                    "expires_at": tok.expires_at.isoformat() if tok.expires_at else None,
                    "token_type": tok.token_type,
                    "scope": tok.scope,
                }
            with open(self.token_store_path, 'w', encoding='utf-8') as f:
                json.dump(serializable, f, indent=2)
        except Exception as e:  # noqa
            logger.warning(f"Failed to save OAuth2 tokens: {e}")

    def _load_tokens(self):
        """Load tokens from disk if present."""
        path = self.token_store_path
        if not path or not os.path.exists(path):
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for svc, tok in data.items():
                expires_at = tok.get("expires_at")
                self.tokens[svc] = OAuth2Token(
                    access_token=tok.get("access_token"),
                    refresh_token=tok.get("refresh_token"),
                    expires_at=datetime.fromisoformat(expires_at) if expires_at else None,
                    token_type=tok.get("token_type", "Bearer"),
                    scope=tok.get("scope"),
                )
            logger.info(f"Loaded persisted OAuth2 tokens for services: {list(self.tokens.keys())}")
        except Exception as e:  # noqa
            logger.warning(f"Failed to load persisted OAuth2 tokens: {e}")

class ServiceOAuth2Configs:
    """Predefined OAuth2 configurations for supported services"""
    
    @staticmethod
    def salesforce(client_id: str, client_secret: str, redirect_uri: str, is_sandbox: bool = False) -> OAuth2Config:
        """Salesforce OAuth2 configuration"""
        base_url = "https://test.salesforce.com" if is_sandbox else "https://login.salesforce.com"
        return OAuth2Config(
            client_id=client_id,
            client_secret=client_secret,
            authorization_url=f"{base_url}/services/oauth2/authorize",
            token_url=f"{base_url}/services/oauth2/token",
            redirect_uri=redirect_uri,
            scope="api refresh_token offline_access",
            service_name="salesforce"
        )
    
    @staticmethod
    def shopify(client_id: str, client_secret: str, redirect_uri: str, shop_domain: str) -> OAuth2Config:
        """Shopify OAuth2 configuration"""
        return OAuth2Config(
            client_id=client_id,
            client_secret=client_secret,
            authorization_url=f"https://{shop_domain}/admin/oauth/authorize",
            token_url=f"https://{shop_domain}/admin/oauth/access_token",
            redirect_uri=redirect_uri,
            scope="read_orders,write_orders,read_products,write_products,read_customers,write_customers",
            service_name="shopify"
        )
    
    @staticmethod
    def hubspot(client_id: str, client_secret: str, redirect_uri: str) -> OAuth2Config:
        """HubSpot OAuth2 configuration"""
        return OAuth2Config(
            client_id=client_id,
            client_secret=client_secret,
            authorization_url="https://app.hubspot.com/oauth/authorize",
            token_url="https://api.hubapi.com/oauth/v1/token",
            redirect_uri=redirect_uri,
            scope="contacts,crm.objects.contacts.read,crm.objects.contacts.write",
            service_name="hubspot"
        )
    
    @staticmethod
    def slack(client_id: str, client_secret: str, redirect_uri: str) -> OAuth2Config:
        """Slack OAuth2 configuration"""
        return OAuth2Config(
            client_id=client_id,
            client_secret=client_secret,
            authorization_url="https://slack.com/oauth/v2/authorize",
            token_url="https://slack.com/api/oauth.v2.access",
            redirect_uri=redirect_uri,
            scope="chat:write,channels:read,files:write",
            service_name="slack"
        )
    
    @staticmethod
    def calendly(client_id: str, client_secret: str, redirect_uri: str) -> OAuth2Config:
        """Calendly OAuth2 configuration"""
        return OAuth2Config(
            client_id=client_id,
            client_secret=client_secret,
            authorization_url="https://auth.calendly.com/oauth/authorize",
            token_url="https://auth.calendly.com/oauth/token",
            redirect_uri=redirect_uri,
            scope="default",
            service_name="calendly"
        )
    
    @staticmethod
    def zendesk(client_id: str, client_secret: str, redirect_uri: str, subdomain: str) -> OAuth2Config:
        """Zendesk OAuth2 configuration"""
        return OAuth2Config(
            client_id=client_id,
            client_secret=client_secret,
            authorization_url=f"https://{subdomain}.zendesk.com/oauth/authorizations/new",
            token_url=f"https://{subdomain}.zendesk.com/oauth/tokens",
            redirect_uri=redirect_uri,
            scope="read write",
            service_name="zendesk"
        )

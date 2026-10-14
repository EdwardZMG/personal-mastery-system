"""
Feishu Bot Service for sending messages and handling bot operations.

This service provides methods to:
- Send text/card messages to users or groups
- Get tenant access token (auto-refresh)
- Handle message templates
"""
import requests
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from app.config import settings


class FeishuBotService:
    """Service for interacting with Feishu Open API."""
    
    BASE_URL = "https://open.feishu.cn/open-apis"
    
    def __init__(self):
        self.app_id = settings.FEISHU_APP_ID
        self.app_secret = settings.FEISHU_APP_SECRET
        self._token_cache: Dict[str, Any] = {}
    
    def _get_tenant_access_token(self) -> str:
        """
        Get tenant access token with caching.
        
        Tokens are cached and refreshed when expired (every ~2 hours).
        """
        cache_key = "tenant_access_token"
        
        # Check cache
        if cache_key in self._token_cache:
            token_info = self._token_cache[cache_key]
            if datetime.now() < token_info["expires_at"]:
                return token_info["access_token"]
        
        # Request new token
        url = f"{self.BASE_URL}/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") != 0:
            raise Exception(f"Failed to get tenant access token: {data}")
        
        # Cache token (expires in 2 hours, refresh at 1h50m)
        expires_in = data.get("expire", 7200)
        self._token_cache[cache_key] = {
            "access_token": data["tenant_access_token"],
            "expires_at": datetime.now() + timedelta(seconds=expires_in - 600)
        }
        
        return data["tenant_access_token"]
    
    def send_message(
        self,
        chat_id: str,
        content: str,
        msg_type: str = "text",
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Send a message to a chat or user.
        
        Args:
            chat_id: Chat ID (for group messages) or user open_id (for P2P)
            content: Message content (text or JSON for card messages)
            msg_type: Message type ("text" or "interactive")
            user_id: User open_id (required if chat_id is not provided)
            
        Returns:
            Response data from Feishu API
            
        Raises:
            Exception: If API call fails
        """
        token = self._get_tenant_access_token()
        
        # Determine receive_id_type based on chat_id format
        if chat_id.startswith("oc_"):
            receive_id_type = "chat_id"
        elif chat_id.startswith("ou_"):
            receive_id_type = "open_id"
        else:
            # Default to chat_id
            receive_id_type = "chat_id"
        
        url = f"{self.BASE_URL}/im/v1/messages"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # Build message payload
        if msg_type == "text":
            content_obj = {"text": content}
        elif msg_type == "interactive":
            # Content should already be JSON string for interactive cards
            content_obj = content if isinstance(content, dict) else {"text": content}
        else:
            raise ValueError(f"Unsupported msg_type: {msg_type}")
        
        payload = {
            "receive_id_type": receive_id_type,
            "receive_id": chat_id,
            "msg_type": msg_type,
            "content": content_obj if isinstance(content_obj, str) else str(content_obj).replace("'", '"')
        }
        
        # For P2P messages, use user_id as receive_id
        if receive_id_type == "open_id":
            payload["receive_id"] = user_id or chat_id
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") != 0:
            raise Exception(f"Failed to send message: {data}")
        
        return data
    
    def send_text_message(self, user_open_id: str, text: str) -> Dict[str, Any]:
        """
        Send a simple text message to a user.
        
        Args:
            user_open_id: User's open_id
            text: Message text
            
        Returns:
            Response data
        """
        return self.send_message(
            chat_id=user_open_id,
            content=text,
            msg_type="text",
            user_id=user_open_id
        )
    
    def send_card_message(self, user_open_id: str, card_content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send an interactive card message to a user.
        
        Args:
            user_open_id: User's open_id
            card_content: Card structure as dict
            
        Returns:
            Response data
        """
        return self.send_message(
            chat_id=user_open_id,
            content=card_content,
            msg_type="interactive",
            user_id=user_open_id
        )
    
    def get_user_info(self, user_open_id: str) -> Dict[str, Any]:
        """
        Get user information by open_id.
        
        Args:
            user_open_id: User's open_id
            
        Returns:
            User info dict
        """
        token = self._get_tenant_access_token()
        url = f"{self.BASE_URL}/contact/v3/users/{user_open_id}"
        
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if data.get("code") != 0:
            raise Exception(f"Failed to get user info: {data}")
        
        return data.get("data", {}).get("user", {})

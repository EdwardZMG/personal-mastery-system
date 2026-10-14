import time
import json
import httpx
from app.config import settings
from typing import Optional, Dict, List


class FeishuWebhookService:
    """Approach B: Feishu Group Webhook"""

    @staticmethod
    async def send_message(text: str, title: str = "Edward 成长系统") -> bool:
        if not settings.FEISHU_WEBHOOK_URL:
            print("Warning: FEISHU_WEBHOOK_URL not configured")
            return False

        payload = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": title
                    },
                    "template": "blue"
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": text
                        }
                    }
                ]
            }
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    settings.FEISHU_WEBHOOK_URL,
                    json=payload
                )
                return response.status_code == 200
        except Exception as e:
            print(f"Feishu webhook error: {e}")
            return False


class ServerJiangService:
    """Approach C: WeChat Push via ServerJiang"""

    @staticmethod
    async def send_message(title: str, content: str) -> bool:
        if not settings.SERVERJIANG_SENDKEY:
            print("Warning: SERVERJIANG_SENDKEY not configured")
            return False

        url = f"https://sctapi.ftqq.com/{settings.SERVERJIANG_SENDKEY}.send"
        payload = {
            "title": title,
            "desp": content
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, data=payload)
                result = response.json()
                return result.get("code") == 0
        except Exception as e:
            print(f"ServerJiang error: {e}")
            return False


class FeishuBotService:
    """Approach A: Custom Feishu Bot with OAuth"""

    _access_token: Optional[str] = None
    _token_expire: int = 0

    @staticmethod
    async def get_access_token() -> Optional[str]:
        if not settings.FEISHU_APP_ID or not settings.FEISHU_APP_SECRET:
            print("Warning: Feishu bot credentials not configured")
            return None

        # Simple token caching (in production, use Redis)
        if FeishuBotService._access_token and time.time() < FeishuBotService._token_expire:
            return FeishuBotService._access_token

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": settings.FEISHU_APP_ID,
            "app_secret": settings.FEISHU_APP_SECRET
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(url, json=payload)
                result = response.json()
                if result.get("code") == 0:
                    FeishuBotService._access_token = result["tenant_access_token"]
                    FeishuBotService._token_expire = time.time() + result.get("expire", 7200) - 300
                    return FeishuBotService._access_token
                else:
                    print(f"Feishu auth error: {result}")
                    return None
        except Exception as e:
            print(f"Feishu auth exception: {e}")
            return None

    @staticmethod
    async def send_message(text: str, title: str = "Edward 成长系统") -> bool:
        token = await FeishuBotService.get_access_token()
        if not token:
            return False

        card = json.dumps({
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": "blue"
            },
            "elements": [{
                "tag": "div",
                "text": {"tag": "lark_md", "content": text}
            }]
        })

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        targets = []
        if settings.FEISHU_CHAT_ID:
            targets.append(("chat_id", settings.FEISHU_CHAT_ID))
        if settings.FEISHU_USER_OPEN_ID:
            targets.append(("open_id", settings.FEISHU_USER_OPEN_ID))

        for id_type, receive_id in targets:
            url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={id_type}"
            payload = {"receive_id": receive_id, "msg_type": "interactive", "content": card}
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    response = await client.post(url, json=payload, headers=headers)
                    result = response.json()
                    if result.get("code") == 0:
                        return True
                    print(f"Feishu send ({id_type}) error: {result.get('msg')}")
            except Exception as e:
                print(f"Feishu bot send error: {e}")
        return False


async def push_to_all_channels(title: str, content: str) -> Dict[str, bool]:
    """Push message to all configured channels"""
    results = {}

    # Approach A: Custom Feishu Bot
    if settings.FEISHU_APP_ID and settings.FEISHU_APP_SECRET:
        results["feishu_bot"] = await FeishuBotService.send_message(content, title)

    # Approach B: Feishu Group Webhook
    if settings.FEISHU_WEBHOOK_URL:
        results["feishu_webhook"] = await FeishuWebhookService.send_message(content, title)

    # Approach C: ServerJiang WeChat
    if settings.SERVERJIANG_SENDKEY:
        results["wechat"] = await ServerJiangService.send_message(title, content)

    return results

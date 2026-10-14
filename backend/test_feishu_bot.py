#!/usr/bin/env python3
"""
Test script to get Edward's Feishu Open ID and test push notification
"""
import httpx
import asyncio

APP_ID = "cli_aa410c43d4b8dcb8"
APP_SECRET = "YOUR_FEISHU_APP_SECRET"


async def get_access_token():
    """Get Feishu tenant access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload)
        result = response.json()

        if result.get("code") == 0:
            print(f"✅ Access Token获取成功: {result['tenant_access_token'][:20]}...")
            return result["tenant_access_token"]
        else:
            print(f"❌ 获取Token失败: {result}")
            return None


async def get_user_info(token):
    """Get current user info (requires user to send message to bot first)"""
    # This endpoint requires the user to have interacted with the bot
    # Alternative: use contact API to search by phone/email
    print("\n📋 请执行以下操作获取你的Open ID:")
    print("1. 在飞书中找到'Edward成长系统'应用")
    print("2. 发送任意消息（如'测试'）给该应用")
    print("3. 访问 https://open.feishu.cn/app/cli_aa410c43d4b8dcb8/event")
    print("4. 查看事件日志，找到你的Open ID（格式：ou_xxxxxxxxxxxxxxxx）")
    print("\n或者，如果你有飞书手机号/邮箱，我可以直接查询：")

    # Try to get user by phone (you need to provide your phone number)
    phone = input("请输入你的飞书手机号（留空则跳过）: ").strip()

    if phone:
        url = f"https://open.feishu.cn/open-apis/contact/v3/users?mobile={phone}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=headers)
            result = response.json()

            if result.get("code") == 0 and result.get("data", {}).get("items"):
                user = result["data"]["items"][0]
                open_id = user.get("open_id")
                print(f"\n✅ 找到你的Open ID: {open_id}")
                print(f"姓名: {user.get('name')}")
                return open_id
            else:
                print(f"❌ 未找到用户: {result}")
                return None
    else:
        return None


async def test_send_message(token, open_id):
    """Test sending message to user"""
    if not open_id:
        print("❌ 缺少Open ID，无法发送测试消息")
        return False

    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    payload = {
        "receive_id": open_id,
        "msg_type": "interactive",
        "content": {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": "🧪 Edward成长系统测试"
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**推送测试成功！**\n\n如果你看到这条消息，说明飞书自定义Bot配置正确。\n\n明天早上6点，你将收到第一条晨间推送 ☀️"
                    }
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload, headers=headers)
        result = response.json()

        if result.get("code") == 0:
            print("\n✅ 测试消息发送成功！请检查飞书是否收到消息")
            return True
        else:
            print(f"\n❌ 发送失败: {result}")
            return False


async def main():
    print("🚀 开始测试飞书自定义Bot...\n")

    # Step 1: Get access token
    print("Step 1: 获取Access Token")
    token = await get_access_token()
    if not token:
        return

    # Step 2: Get user Open ID
    print("\nStep 2: 获取用户Open ID")
    open_id = await get_user_info(token)

    if not open_id:
        print("\n⚠️ 未能自动获取Open ID")
        open_id = input("请手动输入你的Open ID（格式：ou_xxxxxxxxxxxxxxxx）: ").strip()

    # Step 3: Test send message
    print("\nStep 3: 发送测试消息")
    success = await test_send_message(token, open_id)

    if success:
        print("\n" + "="*60)
        print("🎉 配置完成！")
        print("="*60)
        print(f"\n请将以下信息保存到.env文件:")
        print(f"FEISHU_APP_ID={APP_ID}")
        print(f"FEISHU_APP_SECRET={APP_SECRET}")
        print(f"FEISHU_USER_OPEN_ID={open_id}")
        print("\n部署到服务器后，你将每天收到3次推送！")
    else:
        print("\n❌ 测试失败，请检查应用权限和Open ID是否正确")


if __name__ == "__main__":
    try:
        import httpx
        asyncio.run(main())
    except ImportError:
        print("❌ 缺少httpx库，请先安装: pip install httpx")

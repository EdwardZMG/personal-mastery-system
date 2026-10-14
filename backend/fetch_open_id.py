#!/usr/bin/env python3
"""
Fetch Edward's Feishu Open ID by mobile number and test push notification
"""
import httpx
import asyncio

APP_ID = "cli_aa410c43d4b8dcb8"
APP_SECRET = "YOUR_FEISHU_APP_SECRET"
MOBILE = "+8619575352625"


async def get_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload)
        result = response.json()

        if result.get("code") == 0:
            print(f"✅ Access Token获取成功")
            return result["tenant_access_token"]
        else:
            print(f"❌ 获取Token失败: {result}")
            return None


async def get_user_by_mobile(token):
    url = "https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "mobiles": [MOBILE]
    }

    print(f"\n正在查询手机号: {MOBILE}")
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload, headers=headers)
        result = response.json()

        if result.get("code") == 0:
            user_list = result.get("data", {}).get("user_list", [])
            if user_list:
                user = user_list[0]
                open_id = user.get("user_id")
                print(f"✅ 找到用户!")
                print(f"   Open ID: {open_id}")
                print(f"   User ID: {user.get('union_id', 'N/A')}")
                return open_id
            else:
                print(f"❌ 未找到用户，请确认：")
                print(f"   1. 手机号 {MOBILE} 是否已注册飞书")
                print(f"   2. 飞书应用是否有 contact:user.base:readonly 权限")
                return None
        else:
            print(f"❌ 查询失败: {result}")
            return None


async def send_test_message(token, open_id):
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
                    "content": "🎉 Edward成长系统配置成功"
                },
                "template": "green"
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": "**恭喜你，Edward！**\n\n飞书自定义Bot已配置成功。\n\n明天早上6点，你将收到第一条晨间推送 ☀️\n\n**今日建议：**\n• 🧘‍♂️ 晨间冥想10分钟\n• 📖 阅读20分钟\n• 🏃 运动30分钟"
                    }
                }
            ]
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    print("\n正在发送测试消息...")
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload, headers=headers)
        result = response.json()

        if result.get("code") == 0:
            print("✅ 测试消息发送成功！")
            print("   请检查飞书是否收到消息")
            return True
        else:
            print(f"❌ 发送失败: {result}")
            if result.get("code") == 99991672:
                print("   错误原因：应用缺少 im:message 权限")
                print("   解决方法：访问 https://open.feishu.cn/app/cli_aa410c43d4b8dcb8/permissions 开通权限")
            return False


async def main():
    print("="*60)
    print("🚀 Edward成长系统 - 获取Open ID并测试推送")
    print("="*60)
    print()

    # Step 1: Get token
    token = await get_access_token()
    if not token:
        return

    # Step 2: Get user by mobile
    open_id = await get_user_by_mobile(token)
    if not open_id:
        return

    # Step 3: Test message
    success = await send_test_message(token, open_id)

    if success:
        print("\n" + "="*60)
        print("🎉 配置完成！")
        print("="*60)
        print(f"\n请将以下信息保存到.env文件:")
        print(f"FEISHU_APP_ID={APP_ID}")
        print(f"FEISHU_APP_SECRET={APP_SECRET}")
        print(f"FEISHU_USER_OPEN_ID={open_id}")
        print("\n部署到服务器后，你将每天收到3次推送！")
        print("明天早上6点将收到第一条晨间推送 ☀️")
    else:
        print("\n⚠️ 测试消息发送失败，请检查应用权限")


if __name__ == "__main__":
    try:
        import httpx
        asyncio.run(main())
    except ImportError:
        print("❌ 缺少httpx库，请先安装: pip install httpx")

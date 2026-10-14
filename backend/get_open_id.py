#!/usr/bin/env python3
"""
一键获取飞书Open ID并测试推送
"""
import httpx
import asyncio
import json

APP_ID = "cli_aa410c43d4b8dcb8"
APP_SECRET = "YOUR_FEISHU_APP_SECRET"


async def get_access_token():
    """获取飞书tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload)
        result = response.json()

        if result.get("code") == 0:
            return result["tenant_access_token"]
        else:
            print(f"❌ 获取Token失败: {result}")
            return None


async def search_user_by_email(token, email):
    """通过邮箱搜索用户"""
    url = f"https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "emails": [email]
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload, headers=headers)
        result = response.json()

        if result.get("code") == 0:
            user_list = result.get("data", {}).get("user_list", [])
            if user_list:
                user = user_list[0]
                open_id = user.get("user_id")
                return open_id
        return None


async def search_user_by_mobile(token, mobile):
    """通过手机号搜索用户"""
    url = f"https://open.feishu.cn/open-apis/contact/v3/users/batch_get_id?user_id_type=open_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "mobiles": [mobile]
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload, headers=headers)
        result = response.json()

        if result.get("code") == 0:
            user_list = result.get("data", {}).get("user_list", [])
            if user_list:
                user = user_list[0]
                open_id = user.get("user_id")
                return open_id
        return None


async def send_test_message(token, open_id):
    """发送测试消息"""
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

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload, headers=headers)
        result = response.json()

        if result.get("code") == 0:
            return True
        else:
            print(f"❌ 发送失败: {result}")
            return False


async def main():
    print("="*60)
    print("🚀 Edward成长系统 - 获取飞书Open ID工具")
    print("="*60)
    print()

    # Step 1: Get token
    print("Step 1: 获取Access Token...")
    token = await get_access_token()
    if not token:
        return

    print("✅ Token获取成功")
    print()

    # Step 2: Ask for contact info
    print("Step 2: 请输入你的飞书联系方式（二选一）：")
    print()
    email = input("你的飞书邮箱（留空则用手机号）: ").strip()
    mobile = ""

    if not email:
        mobile = input("你的飞书手机号（带区号，如+8613800138000）: ").strip()

    if not email and not mobile:
        print("\n❌ 请提供邮箱或手机号")
        return

    # Step 3: Search user
    print("\nStep 3: 查询用户信息...")
    open_id = None

    if email:
        print(f"正在通过邮箱查询: {email}")
        open_id = await search_user_by_email(token, email)
    elif mobile:
        print(f"正在通过手机号查询: {mobile}")
        open_id = await search_user_by_mobile(token, mobile)

    if open_id:
        print(f"\n✅ 找到你的Open ID: {open_id}")
        print()

        # Step 4: Test message
        print("Step 4: 发送测试消息...")
        success = await send_test_message(token, open_id)

        if success:
            print("\n" + "="*60)
            print("🎉 配置完成！")
            print("="*60)
            print(f"\n请将以下信息保存到.env文件:")
            print(f"FEISHU_APP_ID={APP_ID}")
            print(f"FEISHU_APP_SECRET={APP_SECRET}")
            print(f"FEISHU_USER_OPEN_ID={open_id}")
            print("\n检查飞书是否收到测试消息！")
            print("明天早上6点将收到第一条晨间推送 ☀️")
        else:
            print("\n❌ 测试消息发送失败")
    else:
        print("\n❌ 未找到用户，请检查：")
        print("1. 邮箱/手机号是否正确")
        print("2. 该账号是否已注册飞书")
        print("3. 飞书应用是否有contact:user.base:readonly权限")
        print()
        print("备选方案：")
        print("1. 在飞书中向'Edward成长系统'发送任意消息")
        print("2. 访问 https://open.feishu.cn/app/cli_aa410c43d4b8dcb8/event")
        print("3. 查看事件日志，复制sender.open_id")


if __name__ == "__main__":
    try:
        import httpx
        asyncio.run(main())
    except ImportError:
        print("❌ 缺少httpx库，请先安装: pip install httpx")

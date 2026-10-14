#!/usr/bin/env python3
"""
Test Feishu push notification with Edward's Open ID
"""
import httpx
import asyncio

APP_ID = "cli_aa410c43d4b8dcb8"
APP_SECRET = "YOUR_FEISHU_APP_SECRET"
OPEN_ID = "ou_c2210b26a863b40a09fc55b76526099a"


async def get_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
        result = response.json()
        if result.get("code") == 0:
            return result["tenant_access_token"]
        return None


async def send_test():
    token = await get_token()
    if not token:
        print("❌ 获取Token失败")
        return

    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    payload = {
        "receive_id": OPEN_ID,
        "msg_type": "interactive",
        "content": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": "🎉 Edward成长系统配置成功"},
                "template": "green"
            },
            "elements": [{
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "**恭喜你，Edward！**\n\n✅ 飞书自定义Bot已配置成功\n✅ Open ID: ou_c2210b26a863b40a09fc55b76526099a\n\n**明天早上6点，你将收到第一条晨间推送 ☀️**\n\n**今日建议：**\n• 🧘‍♂️ 晨间冥想10分钟（提升Mindset）\n• 📖 阅读《AI时代》20分钟（Knowledge）\n• 🏃 晨跑30分钟（身体健康）\n• 🎯 今日要事：完成AI项目原型设计\n\n**记住：** 做正确的事，把事情做正确！"
                }
            }]
        }
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload, headers=headers)
        result = response.json()

        if result.get("code") == 0:
            print("✅ 测试消息发送成功！")
            print("   请检查飞书是否收到消息")
            print("\n" + "="*60)
            print("🎉 配置完成！后端代码已就绪")
            print("="*60)
            print(f"\nOpen ID: {OPEN_ID}")
            print("\n下一步：部署到服务器")
            print("参考文档: backend/DEPLOYMENT_INSTRUCTIONS.md")
        else:
            print(f"❌ 发送失败: {result}")


if __name__ == "__main__":
    try:
        import httpx
        asyncio.run(send_test())
    except ImportError:
        print("❌ 缺少httpx库: pip install httpx")

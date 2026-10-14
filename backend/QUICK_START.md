# Edward成长系统 - 快速启动指南

## 当前状态

✅ **已完成配置：**
- 飞书应用App ID: `cli_aa410c43d4b8dcb8`
- 飞书应用Secret: `YOUR_FEISHU_APP_SECRET`

⏳ **待完成：**
- 获取你的飞书Open ID
- （可选）配置飞书群Webhook
- （可选）配置Server酱微信推送

---

## 立即获取你的飞书Open ID（2种方法）

### 方法1：通过应用事件日志（推荐）

1. **在飞书中找到应用**
   - 打开飞书桌面端或手机端
   - 搜索"Edward成长系统"或从工作台找到该应用

2. **发送测试消息**
   - 向"Edward成长系统"发送任意消息，如："测试"

3. **查看事件日志**
   - 访问 https://open.feishu.cn/app/cli_aa410c43d4b8dcb8/event
   - 使用飞书扫码登录
   - 在"事件订阅"页面查看最新消息
   - 找到你刚才发送的消息，复制`sender.open_id`（格式：`ou_xxxxxxxxxxxxxxxx`）

### 方法2：运行测试脚本自动获取

```bash
# 进入backend目录
cd backend

# 安装依赖
pip install httpx

# 运行测试脚本
python test_feishu_bot.py
```

脚本会提示你输入手机号，自动查询Open ID并发送测试消息。

---

## 获取Open ID后立即操作

### Step 1: 更新.env文件

编辑 `backend/.env`，将`FEISHU_USER_OPEN_ID`改为你的实际Open ID：

```ini
FEISHU_USER_OPEN_ID=ou_xxxxxxxxxxxxxxxx  # 替换为你的Open ID
```

### Step 2: 本地测试（可选）

```bash
cd backend
python test_feishu_bot.py
```

如果看到"✅ 测试消息发送成功"，说明配置正确！

### Step 3: 部署到服务器

按照 `DEPLOYMENT_INSTRUCTIONS.md` 的步骤部署到Linux服务器。

---

## （可选）配置飞书群Webhook

如果你希望在飞书群中也收到推送：

1. 打开飞书群 → 点击右上角"..." → "添加机器人"
2. 选择"自定义机器人" → 设置名称为"Edward成长系统"
3. 复制Webhook地址
4. 添加到 `.env` 文件：
   ```ini
   FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxx
   ```

---

## （可选）配置Server酱微信推送

如果你希望在微信中也收到推送：

1. 访问 https://sct.ftqq.com/
2. 微信扫码登录
3. 复制SendKey
4. 添加到 `.env` 文件：
   ```ini
   SERVERJIANG_SENDKEY=SCTxxxxxxxxxxxxxxxxxxx
   ```
5. 关注"方糖"公众号接收消息

---

## 定时推送时间表

配置完成后，你将每天收到以下推送：

| 时间 | 内容 | 理论框架 |
|------|------|----------|
| ☀️ 6:00 AM | 晨间提醒 + 今日计划 | MASK Mindset + 要事第一 |
| 🌞 12:30 PM | 午间复盘 + 能量检查 | 7个习惯之反思 |
| 🌙 9:00 PM | 晚间总结 + 明日规划 | Maslow需求检查 |
| 📅 周日8:00 PM | 周复盘 | Covey 7 Habits完整复盘 |
| 🎯 每月1日9:00 AM | 月度里程碑检查 | SMART目标 + MASK维度评估 |
| ⚠️ 每晚10:00 PM | 预警提醒（如有连续未打卡） | 激励机制 |

---

## 下一步行动

**现在就去做：**

1. ✅ 打开飞书，向"Edward成长系统"发送消息
2. ✅ 访问 https://open.feishu.cn/app/cli_aa410c43d4b8dcb8/event 获取Open ID
3. ✅ 更新 `backend/.env` 中的 `FEISHU_USER_OPEN_ID`
4. ✅ 运行 `python test_feishu_bot.py` 测试推送
5. ✅ 部署到服务器（参考DEPLOYMENT_INSTRUCTIONS.md）

**明天早上6点，你就会收到第一条晨间推送！**

---

## 遇到问题？

查看完整文档：
- `DEPLOYMENT_INSTRUCTIONS.md` - 详细部署步骤
- `../API_DOCUMENTATION.md` - API接口文档
- `../EDWARD_GROWTH_SYSTEM_ARCHITECTURE.md` - 系统架构说明

或直接问我，我会帮你解决！

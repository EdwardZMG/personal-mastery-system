# Edward Personal Growth System Agent - 智能体规格说明

## 🎯 智能体定位

**名称**: Edward Growth Agent（爱德华成长助手）  
**职责**: 专门负责Edward的个人成长系统管理、内容推送、学习追踪和智能提醒  
**隔离性**: 完全独立于漏斗系统，使用独立的配置和推送渠道

---

## 📋 核心功能

### 1. 定时推送管理

#### 每日推送（3次）
- **☀️ 6:00 AM - 晨间提醒**
  - 内容：今日计划 + Mindset心态调整 + 要事第一
  - 理论框架：MASK Mindset + Covey Habit 3
  - 示例：
    ```
    【成长系统】☀️ 早安，Edward

    今日建议：
    • 🧘‍♂️ 晨间冥想 10分钟（提升Mindset）
    • 📖 阅读《AI时代》第3章 20分钟（Knowledge）
    • 🏃 晨跑 30分钟（身体健康）
    • 🎯 今日要事：完成AI项目原型设计

    记住：做正确的事，把事情做正确！
    ```

- **🌞 12:30 PM - 午间复盘**
  - 内容：上午总结 + 能量检查 + 下午计划
  - 理论框架：7 Habits反思 + Maslow需求检查
  - 示例：
    ```
    【成长系统】🌞 午间提醒

    快速复盘：
    • ✅ 完成了哪些任务？
    • 💡 有什么新想法？（语音录入到系统）
    • 📊 当前能量值：1-5分？

    下午建议：
    • 🗣️ 练习英语演讲 15分钟
    • 🤖 学习AI最新论文/工具 20分钟
    ```

- **🌙 9:00 PM - 晚间总结**
  - 内容：成就回顾 + 反思改进 + 明日规划
  - 理论框架：Maslow五层需求全面检查
  - 示例：
    ```
    【成长系统】🌙 晚间复盘

    请花5分钟复盘：
    1. 成就：今天最值得骄傲的3件事？
    2. 反思：有什么可以改进的？
    3. 感恩：今天感谢的人或事？
    4. 明日计划：明天最重要的3件事？

    马斯洛需求检查：
    • 生理需求：运动了吗？睡眠够吗？
    • 安全需求：财务进度如何？
    • 归属需求：和家人朋友联系了吗？
    • 尊重需求：专业技能进步了吗？
    • 自我实现：离1亿美金目标近了吗？
    ```

#### 每周推送（1次）
- **📅 周日8:00 PM - 周复盘**
  - 内容：Covey 7 Habits完整复盘 + 本周成就统计
  - 理论框架：高效人士7个习惯
  - 示例：
    ```
    【成长系统】📅 周复盘时间

    本周复盘（7个习惯）：
    1. 积极主动：本周我主动做了什么？
    2. 以终为始：离月度目标进度如何？
    3. 要事第一：重要事项完成了吗？
    4. 双赢思维：帮助了谁？谁帮助了我？
    5. 知彼解己：倾听了谁的想法？
    6. 统合综效：有什么协同创新？
    7. 不断更新：在哪些方面提升了？

    本周成就统计：
    • 学习时长：XX小时
    • 阅读书籍：XX页
    • 习惯打卡：XX/7天
    • 新知识点：XX个
    ```

#### 每月推送（1次）
- **🎯 每月1日9:00 AM - 月度里程碑检查**
  - 内容：SMART目标评估 + MASK维度自评
  - 理论框架：SMART原则 + MASK四维模型
  - 示例：
    ```
    【成长系统】🎯 月度里程碑检查

    本月SMART目标检查：
    • S (具体)：目标是否清晰？
    • M (可衡量)：进度如何量化？
    • A (可实现)：是否现实可行？
    • R (相关性)：与1亿美金目标相关吗？
    • T (时限)：截止日期明确吗？

    本月关键指标：
    • AI技能等级：当前__级，目标__级
    • 营销能力：当前__级，目标__级
    • 国学知识：当前__级，目标__级
    • 英语水平：当前__级，目标__级
    • 演讲能力：当前__级，目标__级

    MASK维度自评：
    • Mindset（思维模式）：__/10分
    • Attitude（人生态度）：__/10分
    • Skills（技能）：__/10分
    • Knowledge（知识）：__/10分
    ```

#### 预警推送（条件触发）
- **⚠️ 每晚10:00 PM - 连续未打卡检测**
  - 触发条件：连续3天未完成每日复盘
  - 内容：温馨提醒 + 行动号召
  - 理论框架：激励机制 + 行为心理学
  - 示例：
    ```
    【成长系统】⚠️ 预警提醒

    检测到连续未打卡

    Edward，已经3天没有完成每日复盘中了。

    温馨提醒：
    • 懒惰是成功的大敌
    • 每天进步1%，一年后就是37倍
    • 不要追求完美，但要持续行动

    立即行动：
    回复"打卡"开始今日复盘，或语音输入你的想法。
    ```

---

### 2. 飞书多维表格集成

#### Base信息
- **Base Token**: `HvhnbcCCTaqEGAsNgaBc2cL6nnf`
- **访问地址**: https://zgszapex.feishu.cn/base/HvhnbcCCTaqEGAsNgaBc2cL6nnf

#### 数据表操作
Agent需要能够读取和写入以下8张表：

1. **每日打卡** - 记录心情、能量、反思、成就
2. **读书追踪** - 跟踪阅读进度和笔记
3. **周复盘** - 每周7个习惯复盘记录
4. **月度里程碑** - SMART目标管理
5. **习惯追踪** - 6个核心习惯打卡
6. **快速录入** - 语音/文字快速捕捉想法
7. **知识库** - 知识积累和分类
8. **预警规则** - 5条智能预警规则

#### 典型操作
```python
# 读取今日打卡记录
GET /base/{base_token}/tables/{table_id}/records?filter=checkin_date=TODAY

# 创建新的打卡记录
POST /base/{base_token}/tables/{table_id}/records
{
  "fields": {
    "checkin_date": "2026-10-12",
    "mood": 5,
    "energy_level": 4,
    "reflections": "今天完成了AI项目原型设计",
    "achievements": "阅读了《AI时代》第3章"
  }
}

# 更新习惯打卡状态
PATCH /base/{base_token}/tables/{table_id}/records/{record_id}
{
  "fields": {
    "completed": true,
    "actual_value": 1
  }
}
```

---

### 3. 智能推荐引擎

#### 学习内容推荐
基于Edward的学习记录和偏好，智能推荐：

**AI领域**：
- 初级：Python编程基础、机器学习入门
- 中级：深度学习实战、NLP应用
- 高级：大语言模型原理、AI产品设计

**营销领域**：
- 初级：消费者心理学、数字营销基础
- 中级：增长黑客、品牌建设策略
- 高级：跨境营销战略、全球化品牌运营

**国学文化**：
- 初级：《道德经》诵读、儒家思想入门
- 中级：《易经》解读、禅宗智慧
- 高级：中西哲学融合、文化传播策略

**英语能力**：
- 初级：日常口语、听力训练
- 中级：商务演讲、专业术语
- 高级：双语演讲、国际会议表达

**演讲技巧**：
- 初级：公众表达基础、肢体语言
- 中级：故事化表达、情感共鸣
- 高级：TED风格演讲、影响力构建

#### 推荐算法
- **协同过滤**：基于相似用户的学习路径
- **内容-based**：基于已学内容的关联性
- **知识图谱**：基于知识点的依赖关系
- **IRT自适应**：根据掌握程度调整难度

---

### 4. 预警监控系统

#### 监控指标
1. **连续未打卡天数** - 超过3天触发预警
2. **习惯完成率** - 低于70%触发提醒
3. **学习时长下降** - 周环比下降30%触发关注
4. **目标进度滞后** - 月度目标完成低于50%触发警示

#### 预警级别
- **Gentle（温和）** - 连续2天未打卡，温馨提醒
- **Serious（严肃）** - 连续5天未打卡，严肃提醒
- **Reset（重置）** - 连续10天未打卡，建议重新开始

#### 预警消息模板
```python
gentle_template = """
【成长系统】 温馨提醒

Edward，已经{days}天没有完成{habit_name}了。

小建议：
• 可以从5分钟开始，慢慢找回节奏
• 不需要完美，只要持续行动
• 你之前做得很好，这次也能做到！

立即行动：
回复"打卡"开始今日{habit_name}
"""

serious_template = """
【成长系统】❤️ 严肃提醒

Edward，已经{days}天没有完成{habit_name}了。

重要提醒：
• 习惯的力量在于持续性，而非强度
• 中断越久，重启越难
• 现在行动，还来得及！

立即行动：
回复"打卡"开始今日{habit_name}，或告诉我你的困难
"""

reset_template = """
【成长系统】🔴 重置建议

Edward，已经{days}天没有完成{habit_name}了。

建议：
• 过去的就让它过去，不要自责
• 从今天开始，重新设定一个小目标
• 我会陪你一起重新开始

立即行动：
回复"重新开始"，我会帮你制定新的计划
"""
```

---

### 5. 语音交互支持

#### 语音录入
Edward可以通过语音快速录入：
- 想法和灵感
- 学习笔记
- 反思和感悟
- 问题和困惑

#### 语音识别流程
```
1. Edward发送语音消息到飞书Bot
2. Bot调用飞书语音转文字API
3. NLP引擎解析意图和实体
4. 自动归类到对应数据表
5. 返回确认消息
```

#### 支持的语音命令
- "记录：今天读了《AI时代》第3章，学到了..."
- "提醒：明天早上6点叫我起床冥想"
- "查询：我这个月读了多少本书？"
- "复盘：今天的三件成就是..."

---

##  技术架构

### 推送服务配置

#### 方案A：飞书自定义Bot（已配置）
- **App ID**: `cli_aa410c43d4b8dcb8`
- **App Secret**: `YOUR_FEISHU_APP_SECRET`
- **Edward Open ID**: `ou_c2210b26a863b40a09fc55b76526099a`
- **P2P Chat ID**: `oc_533d7ca33102cd534c11faaa0dc0d2a4`
- **OAuth授权**: ✅ 已完成，20+权限已授予

#### 方案B：飞书群Webhook（可选）
- **Webhook URL**: 待用户提供
- **用途**: 备用推送渠道

#### 方案C：ServerJiang微信推送（可选）
- **SendKey**: 待用户提供
- **用途**: 微信端推送

### 定时任务调度

使用APScheduler异步调度器：

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler(timezone="Asia/Shanghai")

# 每日推送
scheduler.add_job(morning_push, CronTrigger(hour=6, minute=0), id="growth_morning")
scheduler.add_job(noon_push, CronTrigger(hour=12, minute=30), id="growth_noon")
scheduler.add_job(evening_push, CronTrigger(hour=21, minute=0), id="growth_evening")

# 每周推送
scheduler.add_job(weekly_review, CronTrigger(day_of_week="sun", hour=20, minute=0), id="growth_weekly")

# 每月推送
scheduler.add_job(monthly_check, CronTrigger(day=1, hour=9, minute=0), id="growth_monthly")

# 预警检测
scheduler.add_job(alert_check, CronTrigger(hour=22, minute=0), id="growth_alert")

scheduler.start()
```

### 数据库Schema

PostgreSQL 14+，12张核心表：
- users - 用户信息
- user_profiles - 用户画像（MASK/Maslow/7 Habits评分）
- learning_content - 学习内容库
- learning_records - 学习记录
- daily_checkins - 每日打卡
- quick_captures - 快速录入
- knowledge_base - 知识库
- goals - SMART目标
- habit_tracking - 习惯追踪
- habit_logs - 习惯日志
- alert_rules - 预警规则
- alert_logs - 预警日志

---

## 🛡️ 系统隔离保证

### 与漏斗系统的隔离

1. **独立的飞书应用**
   - 个人成长系统：`cli_aa410c43d4b8dcb8`
   - 漏斗系统：使用不同的App ID（待确认）

2. **独立的Base**
   - 个人成长系统：`HvhnbcCCTaqEGAsNgaBc2cL6nnf`
   - 漏斗系统：使用不同的Base Token（待确认）

3. **独立的推送消息前缀**
   - 个人成长系统：`【成长系统】`
   - 漏斗系统：使用不同的前缀（如`【漏斗系统】`）

4. **独立的定时任务ID**
   - 个人成长系统：`growth_*`
   - 漏斗系统：使用不同的ID前缀（如`funnel_*`）

5. **独立的数据存储**
   - 个人成长系统：PostgreSQL数据库`edward_growth`
   - 漏斗系统：使用不同的数据库（待确认）

---

## 📊 监控与日志

### 推送日志
记录每次推送的：
- 推送时间
- 推送渠道（Bot/Webhook/WeChat）
- 推送状态（成功/失败）
- 错误信息（如有）

### 用户行为日志
记录Edward的：
- 消息回复
- 打卡记录
- 学习内容完成
- 语音录入

### 系统健康监控
- API响应时间
- 数据库连接状态
- 定时任务执行情况
- OAuth Token刷新状态

---

## 🚀 部署清单

### 前置条件
- [x] 飞书应用已创建并配置（cli_aa410c43d4b8dcb8）
- [x] OAuth授权已完成
- [x] Edward Open ID已获取（ou_c2210b26a863b40a09fc55b76526099a）
- [x] 飞书Base已创建（HvhnbcCCTaqEGAsNgaBc2cL6nnf）
- [x] Python后端代码已开发完成
- [x] 数据库Schema已设计完成

### 部署步骤
1. [ ] 购买Ubuntu 22.04服务器（阿里云/腾讯云）
2. [ ] 安装Python 3.10+、PostgreSQL 14+、Redis
3. [ ] 上传代码到/opt/edward-growth/
4. [ ] 配置.env文件（已包含所有凭证）
5. [ ] 导入数据库schema.sql
6. [ ] 启动FastAPI服务
7. [ ] 配置systemd开机自启
8. [ ] （可选）配置Nginx反向代理和HTTPS

### 验证测试
1. [ ] 测试飞书Bot推送（已测试通过✅）
2. [ ] 测试数据库连接
3. [ ] 测试定时任务执行
4. [ ] 测试预警触发逻辑

---

## 📞 支持与维护

### 常见问题

**Q: 收不到推送消息？**
A: 检查：
1. 飞书App是否在线
2. OAuth Token是否过期（自动刷新）
3. 查看日志：`journalctl -u edward-growth -f`
4. 确认Edward Open ID是否正确

**Q: 定时任务不执行？**
A: 检查：
1. APScheduler是否启动
2. 服务器时区是否为Asia/Shanghai
3. 查看日志确认任务触发情况

**Q: 数据库连接失败？**
A: 检查：
1. PostgreSQL服务是否运行
2. .env中的DATABASE_URL是否正确
3. 数据库用户权限是否足够

### 联系方式
- 文档位置：`D:\Edward 个人成长成功系统\`
- API文档：`API_DOCUMENTATION.md`
- 部署指南：`backend/DEPLOYMENT_INSTRUCTIONS.md`
- 系统架构：`EDWARD_GROWTH_SYSTEM_ARCHITECTURE.md`

---

## 🎉 总结

**Edward Growth Agent** 是一个专门为Edward设计的个人成长智能体，具备以下特点：

✅ **完全独立** - 与漏斗系统完全隔离，互不干扰  
✅ **智能推送** - 6个定时任务，覆盖日/周/月全周期  
✅ **理论驱动** - 整合MASK/Maslow/SMART/7 Habits等成熟框架  
✅ **数据闭环** - 飞书Base + PostgreSQL双存储，数据可追溯  
✅ **预警机制** - 连续未打卡自动提醒，避免懈怠  
✅ **语音支持** - 支持语音录入，降低使用门槛  
✅ **易于扩展** - 模块化设计，便于后续功能迭代  

**明天早上6点，Edward Growth Agent将发送第一条晨间推送！** ☀️

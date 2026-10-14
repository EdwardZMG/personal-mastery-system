# Edward 智能成长系统 v5.0

> AI驱动的个性化成长引擎，让每位创业者/高管在90天内实现认知升级和能力突破。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)

##  目录

- [功能特性](#功能特性)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [部署指南](#部署指南)
- [API文档](#api文档)
- [数据库设计](#数据库设计)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## ✨ 功能特性

### 核心功能

- **每日三次学习推送** - 晨间（6:00）、午间（12:30）、晚间（21:00）
- **多通道触达** - 飞书Bot、微信推送、Web App、Mobile App
- **智能内容推荐** - 基于用户画像的个性化推荐
- **语音录入** - 支持语音转文字快速记录
- **知识库管理** - 结构化知识积累与检索
- **习惯追踪** - 6大核心习惯养成
- **目标管理** - SMART原则目标设定与追踪
- **预警系统** - 连续懈怠自动提醒

### 理论框架整合

- ✅ **MASK维度** - Mindset/Attitude/Skills/Knowledge四维度追踪
- ✅ **马斯洛需求** - 五层需求满足度评估
- ✅ **SMART原则** - 目标设定验证系统
- ✅ **效能矩阵** - 做正确的事vs把事情做正确
- ✅ **要事第一** - 每日3件要事系统
- ✅ **统筹综效** - 1+1>2合作机会识别
- ✅ **7个习惯** - 每周习惯焦点训练

### 智能化能力

- 🤖 **推荐系统** - 协同过滤 + 内容-based + 知识图谱混合推荐
-  **NLP引擎** - 意图识别、实体提取、情感分析、内容分类
- ️ **知识图谱** - 结构化知识体系，智能路径规划
-  **自适应学习** - IRT模型动态调整难度

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                    用户触达层                            │
│  ┌──────────┐  ┌──────────┐  ──────────┐  ┌──────── │
│  │ 飞书Bot  │  │ 微信推送 │  │ Web App  │  │Mobile  │ │
│  ──────────┘  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  交互层 (Interaction)                    │
│  多模态输入 | 智能对话 | 推送引擎                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                业务逻辑层 (Business Logic)               │
│  学习引擎 | 内容引擎 | 预警引擎 | 进化引擎               │
└─────────────────────────────────────────────────────────┘
                          ↓
─────────────────────────────────────────────────────────┐
│                   数据层 (Data Layer)                    │
│  PostgreSQL | Redis | Elasticsearch | S3               │
└─────────────────────────────────────────────────────────┘
                          ↓
─────────────────────────────────────────────────────────┐
│                   分析层 (Analytics)                     │
│  学习分析 | 行为分析 | 效果评估 | 预测模型              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 智能化层 (AI/ML Layer)                   │
│  推荐系统 | NLP引擎 | 知识图谱 | 自适应学习             │
└─────────────────────────────────────────────────────────┘
```

### 技术栈

| 层级 | 技术选型 |
|------|----------|
| 前端 | Vue 3 + Vite + Ant Design Vue 4.x + TypeScript (VBEN ADMIN 风格) |
| 后端 | Python 3.10+ (FastAPI 0.109) |
| 数据库 | PostgreSQL 14+ |
| 缓存 | Redis 6+ |
| 容器化 | Docker + Docker Compose |
| 推送 | 飞书 Bot + Webhook + Server酱(微信) |
| NLP | 规则引擎（意图分类 + 领域识别 + 实体提取） |
| 推荐 | 基于内容的推荐 + 难度匹配 + 新鲜度加权 |

---

## 🚀 快速开始

### 前置条件

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 6+（可选，用于缓存）

### 方式一：一键启动（Windows）

```bash
# 同时启动后端 + 前端
start-all.bat

# 或分别启动：
cd backend && start.bat dev    # 后端: http://localhost:8000
start-frontend.bat             # 前端: http://localhost:5173
```

### 方式二：手动启动

#### 1. 后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env     # Windows，编辑 .env 填入实际凭证
# cp .env.example .env     # macOS/Linux

# 初始化数据库（首次运行）
python init_db.py

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 2. 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

#### 3. 访问

- **前端界面**: http://localhost:5173
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health

### 方式三：Docker Compose

```bash
# 一键启动全部服务（PostgreSQL + Redis + API + Frontend）
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

### 环境变量配置

编辑 `backend/.env`：

```env
# 数据库
DATABASE_URL=postgresql://edward:your_password@localhost:5432/edward_growth

# 飞书应用凭证
FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxx
FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FEISHU_USER_OPEN_ID=ou_xxxxxxxxxxxxxxxx

# JWT 密钥（请生成强随机字符串）
SECRET_KEY=your-strong-random-secret-key
```

### 运维脚本

```bash
# 健康检查
bash scripts/health_check.sh

# 数据库备份
bash scripts/backup.sh

# 数据库恢复
bash scripts/restore.sh ./backups/edward_growth_20261012_120000.sql.gz
```

---

## 📦 部署指南

详细部署步骤请参考 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

### 快速部署（Docker）

```bash
# 使用Docker Compose一键部署
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 生产环境部署

1. **准备服务器** - Ubuntu 22.04, 2核2G+
2. **安装依赖** - Python, PostgreSQL, Redis, Nginx
3. **配置环境变量** - `.env`文件
4. **启动服务** - Systemd或Docker
5. **配置反向代理** - Nginx + HTTPS
6. **设置监控** - Prometheus + Grafana

---

## 📚 API文档

完整API文档请参考 [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

### 主要接口

所有接口前缀：`/api/v1/`

| 模块 | 接口 | 描述 |
|------|------|------|
| 认证 | `POST /auth/login` | 登录获取JWT |
| 认证 | `POST /auth/register` | 注册新用户 |
| 仪表盘 | `GET /dashboard/overview` | 总览数据 |
| 知识 | `POST /insights/capture` | 捕获知识洞察 |
| 知识 | `POST /insights/structure` | 结构化知识 |
| 学习 | `GET /learning/content` | 内容库列表 |
| 学习 | `POST /learning/record` | 记录学习活动 |
| 复盘 | `POST /review/trigger` | 触发复盘会话 |
| 演讲 | `POST /speech/generate` | 生成演讲稿 |
| 目标 | `GET /goals/` | 目标列表 |
| 习惯 | `POST /habits/` | 创建习惯 |
| 国学 | `GET /classics/progress` | 国学学习进度 |
| 打卡 | `POST /checkins/` | 每日打卡 |
| 推荐 | `GET /recommendations/` | 个性化推荐 |
| 管理 | `GET /admin/stats` | 系统统计 |

### SDK示例

**Python:**

```python
from edward_growth import EdwardGrowthClient

client = EdwardGrowthClient(api_key="your-api-key")

# 获取每日内容
content = client.get_daily_content(day=15)
print(content['morning']['topic'])

# 记录完成
result = client.record_completion(
    content_id="uuid-here",
    duration_minutes=20,
    feedback_score=5
)
print(f"Streak: {result['streak_days']}")
```

**JavaScript:**

```javascript
import { EdwardGrowthClient } from 'edward-growth-js';

const client = new EdwardGrowthClient('your-api-key');

// 获取每日内容
const content = await client.getDailyContent(15);
console.log(content.morning.topic);
```

---

## 🗄️ 数据库设计

完整数据库Schema请参考 [database/schema.sql](database/schema.sql)

### 核心表结构（26张表）

**基础表（12张）：**

| 表名 | 描述 |
|------|------|
| users | 用户基础信息 |
| user_profiles | 用户画像（MASK/马斯洛/7习惯评分） |
| learning_content | 学习内容库 |
| learning_records | 学习记录 |
| daily_checkins | 每日打卡 |
| quick_captures | 快速录入 |
| knowledge_base | 知识库 |
| goals | SMART目标 |
| habit_tracking | 习惯追踪 |
| habit_logs | 习惯日志 |
| alert_rules | 预警规则 |
| alert_logs | 预警日志 |

**扩展表（14张）：**

| 表名 | 描述 |
|------|------|
| knowledge_insights | 原始知识洞察 |
| structured_knowledge | 结构化知识（含掌握度追踪） |
| knowledge_graph_nodes | 知识图谱节点 |
| knowledge_graph_edges | 知识图谱边 |
| review_sessions | 复盘会话 |
| review_summaries | 复盘总结 |
| speech_drafts | 演讲稿（TED/Toastmasters/电梯/故事） |
| bilingual_speeches | 双语演讲 |
| speech_materials | 演讲素材库 |
| knowledge_applications | 知识应用记录 |
| application_stats | 应用统计 |
| chinese_classics_progress | 国学经典学习进度 |

### 数据关系

```
users (1) ─── (1) user_profiles
users (1) ── (N) learning_records
users (1) ─── (N) daily_checkins
users (1) ─── (N) quick_captures
users (1) ─── (N) knowledge_base
users (1) ─── (N) goals
users (1) ─── (N) habit_tracking
learning_content (1) ─── (N) learning_records
habit_tracking (1) ─── (N) habit_logs
alert_rules (1) ─── (N) alert_logs
```

---

## 🎯 90天学习路径

### Phase 1: 基础期（Day 1-30）

**主题：** 建立知识框架

- **AI领域**: LLM原理、AI产品化、行业应用案例
- **营销领域**: 经典营销理论、消费者心理、品牌基础
- **国学领域**: 论语精选、道德经核心、儒家思想
- **演讲领域**: 发音纠正、基础表达、演讲结构

**目标：**
- 完成率 > 70%
- 读书 9本
- 运动 36次
- 习惯养成 4个

### Phase 2: 进阶期（Day 31-60）

**主题：** 深度理解 + 实战

- **AI领域**: AI战略、投资逻辑、技术前沿
- **营销领域**: 数字营销、AI营销、增长黑客
- **国学领域**: 大学中庸、孟子、孙子兵法
- **演讲领域**: 故事讲述、英文演讲、跨文化沟通

**目标：**
- 完成率 > 75%
- 输出 3篇行业文章
- 做 1次公开演讲
- 认识 3位行业大佬

### Phase 3: 专家期（Day 61-90）

**主题：** 融会贯通 + 创新

- **AI领域**: AI+产业融合、未来趋势、个人AI哲学
- **营销领域**: 品牌战略、个人IP、营销哲学
- **国学领域**: 史记智慧、诗词境界、茶道书法
- **演讲领域**: 大型演讲实战、个人风格、影响力

**目标：**
- 完成率 > 80%
- 出版 1本书
- 做 1场5000人+演讲
- 启动个人项目

---

##  贡献指南

我们欢迎所有形式的贡献！

### 提交Bug报告

请在 [Issues](https://github.com/edward-growth/edward-growth-system/issues) 中提交Bug报告，包含：
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（OS、Python版本等）

### 提交功能建议

请在 [Issues](https://github.com/edward-growth/edward-growth-system/issues) 中提交功能建议，包含：
- 功能描述
- 使用场景
- 预期效果

### 提交代码

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交Pull Request

### 代码规范

- 遵循 [PEP 8](https://pep8.org/) Python代码规范
- 添加必要的注释和文档字符串
- 编写单元测试
- 确保所有测试通过

---

##  更新日志

### v5.0 (2026-10-11)
- ✨ 完整数据库Schema（12张表）
- ✨ 完整API文档（100+接口）
- ✨ MASK/马斯洛/SMART/7个习惯理论整合
- ✨ 推荐系统/NLP引擎/知识图谱/自适应学习
- ✨ 飞书Bot + 微信推送双通道
- ✨ 预警系统 + 自动进化机制

### v4.0 (2026-09-01)
- ✨ 习惯追踪功能
- ✨ SMART目标管理
- ✨ 改进推送系统

### v3.0 (2026-08-01)
- ✨ 知识库管理
- ✨ 快速录入（语音/文字）
- ✨ 用户画像系统

### v2.0 (2026-07-01)
- ✨ 学习记录追踪
- ✨ 每日打卡系统
- ✨ 基础数据分析

### v1.0 (2026-06-01)
- ✨ 初始版本发布
-  用户注册/登录
- ✨ 基础内容推送

---

## 🙏 致谢

感谢以下开源项目：
- [FastAPI](https://fastapi.tiangolo.com/) - 高性能Web框架
- [HuggingFace](https://huggingface.co/) - NLP模型库
- [PostgreSQL](https://www.postgresql.org/) - 关系型数据库
- [Redis](https://redis.io/) - 内存数据库

感谢所有贡献者！

---

## 📜 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系我们

- 项目主页：https://github.com/edward-growth/edward-growth-system
- 问题反馈：https://github.com/edward-growth/edward-growth-system/issues
- 邮箱：support@edward-growth.com

---

## ⭐ Star History

如果这个项目对你有帮助，请给我们一个Star！

[![Star History Chart](https://api.star-history.com/svg?repos=edward-growth/edward-growth-system&type=Date)](https://star-history.com/#edward-growth/edward-growth-system&Date)

---

<p align="center">Made with ❤️ by Edward Growth Team</p>

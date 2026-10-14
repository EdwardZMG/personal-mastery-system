# Edward 个人成长成功系统 — 总体规划文档

> **版本**: 3.0 | **日期**: 2026-10-12 | **状态**: 待Edward审阅确认

---

## 一、项目总览

Edward 个人成长成功系统是一个 AI 驱动的个人发展平台，集成自动学习推送、知识结晶、演讲输出、国学经典学习、习惯追踪于一体，通过飞书多维表格 + Web 管理后台双端触达。

### 1.1 技术栈全景

```
┌─────────────────────────────────────────────────────────────┐
│                      用户触达层                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ VBEN ADMIN   │  │ 飞书多维表格  │  │ 飞书Bot/微信推送  │   │
│  │ Vue3+Vite    │  │ (已有8张表)   │  │ (3通道)           │   │
│  │ Ant Design   │  │              │  │                   │   │
│  └──────┬───────┘  └──────┬───────┘  └────────┬──────────┘   │
│         │                 │                    │              │
├─────────┼─────────────────┼────────────────────┼──────────────┤
│         │          API 网关层 (Nginx)          │              │
│         │    反向代理 / SPA回退 / Gzip / SSL    │              │
│         └─────────────────┼────────────────────┘              │
│                           │                                   │
├───────────────────────────┼───────────────────────────────────┤
│                    业务服务层 (FastAPI)                         │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐   │
│  │认证模块│ │知识管理│ │学习引擎│ │复盘系统│ │演讲生成  │   │
│  │JWT Auth│ │NLP+图谱│ │推荐算法│ │日/周/月│ │TED/双语  │   │
│  └────────┘ └────────┘ └────────┘ └────────┘ └──────────┘   │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌──────────┐   │
│  │国学经典│ │习惯追踪│ │目标管理│ │预警系统│ │爬虫调度  │   │
│  │6部经典 │ │打卡+streak│ │SMART │ │三级预警│ │5领域RSS  │   │
│  └────────┘ └────────┘ └────────┘ └────────┘ └──────────┘   │
│                           │                                   │
├───────────────────────────┼───────────────────────────────────┤
│                      数据存储层                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │ PostgreSQL 14│  │   Redis 7    │  │  飞书Base(云端)   │   │
│  │ 26张表       │  │  缓存/去重    │  │  8张表            │   │
│  └──────────────┘  └──────────────┘  └──────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 专家评估得分

| 维度 | 评分 | 关键发现 |
|------|------|----------|
| 架构完整性 | 78/100 | 5大模块设计齐全，模块间接口未定义 |
| 后端代码 | 48/100 | 4个运行时崩溃BUG + 无认证 + 推荐引擎缺失 |
| 部署就绪度 | 62/100 | 密钥泄露到5+文档 + Docker配置有误 |
| 飞书集成 | 65/100 | App ID不一致 + Token缓存BUG |
| 前端（规划中） | — | VBEN ADMIN，10模块38页面50+API |

---

## 二、项目组织结构

```
D:\Edward 个人成长成功系统\
│
├── .gitignore                              # [新增] Git忽略规则
├── .dockerignore                           # [新增] Docker构建排除
├── .env.example                            # [新增] 环境变量模板
├── docker-compose.yml                      # [修复] 4容器编排
├── README.md                               # [更新] 统一入口
│
├── docs/                                   # [新增] 设计文档归档
│   ├── architecture/
│   │   ├── EDWARD_GROWTH_SYSTEM_ARCHITECTURE.md
│   │   ├── AGENT_SPEC.md
│   │   └── SYSTEM_ISOLATION.md
│   ├── api/
│   │   └── API_DOCUMENTATION.md
│   ├── plans/
│   │   ├── IMPLEMENTATION_ROADMAP.md
│   │   ├── CHINESE_CLASSICS_LEARNING_PLAN.md
│   │   └── MIGRATION_PLAN.md
│   ├── features/
│   │   ├── AUTO_LEARNING_SYSTEM_DESIGN.md
│   │   ├── KNOWLEDGE_CRYSTALLIZATION_AND_SPEECH_SYSTEM.md
│   │   └── FEISHU_CONFIG_COMPLETE.md
│   └── operations/
│       ├── DEPLOYMENT_GUIDE.md
│       ├── USER_MANUAL.md
│       └── VERIFICATION_CHECKLIST.md
│
├── backend/                                # FastAPI 后端
│   ├── Dockerfile                          # [修复] 多阶段构建
│   ├── docker-entrypoint.sh                # [新增] 智能启动脚本
│   ├── requirements.txt                    # [修复] 移除torch/uuid/datetime
│   ├── .env                                # 真实凭证（不入git）
│   ├── .env.example                        # [新增] 凭证模板
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                         # [修复] 路由注册+CORS+异常处理
│   │   ├── config.py                       # [修复] pydantic-settings
│   │   ├── database.py                     # [修复] 连接池优化
│   │   ├── models.py                       # 基础12模型
│   │   ├── models_extended.py              # [修复] Date导入
│   │   │
│   │   ├── schemas/                        # [新增] Pydantic模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── knowledge.py
│   │   │   ├── learning.py
│   │   │   ├── review.py
│   │   │   ├── speech.py
│   │   │   ├── goal.py
│   │   │   ├── habit.py
│   │   │   ├── classics.py
│   │   │   └── common.py
│   │   │
│   │   ├── core/                           # [新增] 核心基础设施
│   │   │   ├── __init__.py
│   │   │   ├── security.py                 # JWT生成/验证
│   │   │   ├── exceptions.py               # 统一异常处理
│   │   │   └── middleware.py               # 请求日志+耗时统计
│   │   │
│   │   ├── services/                       # [新增] 业务逻辑层
│   │   │   ├── __init__.py
│   │   │   ├── knowledge_service.py
│   │   │   ├── learning_service.py
│   │   │   ├── review_service.py
│   │   │   ├── speech_service.py
│   │   │   ├── habit_service.py
│   │   │   ├── goal_service.py
│   │   │   ├── classics_service.py
│   │   │   ├── alert_service.py
│   │   │   └── notification_service.py
│   │   │
│   │   ├── routes/                         # [重构] 路由模块化
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                     # [新增] 认证路由
│   │   │   ├── knowledge.py                # [修复] BUG
│   │   │   ├── review.py                   # [修复] 字段不匹配
│   │   │   ├── speech.py                   # [修复] speech_id→speech_draft_id
│   │   │   ├── application.py              # [修复] 字段不匹配
│   │   │   ├── learning.py                 # [新增]
│   │   │   ├── checkins.py                 # [新增]
│   │   │   ├── goals.py                    # [新增]
│   │   │   ├── habits.py                   # [新增]
│   │   │   ├── classics.py                 # [新增]
│   │   │   ├── dashboard.py                # [新增] 聚合统计
│   │   │   ├── crawler.py                  # [新增] 爬虫管理
│   │   │   ├── recommendations.py          # [新增]
│   │   │   └── admin.py                    # [新增]
│   │   │
│   │   ├── nlp.py                          # [增强] 意图+领域+实体
│   │   ├── crawler.py                      # [完善] 3个实际爬虫
│   │   ├── recommender.py                  # [新增] 轻量推荐引擎
│   │   ├── push_services.py                # [修复] Token缓存BUG
│   │   └── scheduler.py                    # [完善] 6个定时任务
│   │
│   ├── init_db.py                          # [修复] 移除HabitTemplate引用
│   └── tests/                              # [新增]
│       ├── __init__.py
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_knowledge.py
│       └── test_nlp.py
│
├── frontend/                               # [新增] VBEN ADMIN 前端
│   ├── Dockerfile                          # Node构建 + Nginx运行
│   ├── nginx.conf                          # SPA回退 + API代理
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   │
│   └── src/
│       ├── api/                            # 12个API模块
│       │   ├── index.ts                    # Axios实例+拦截器
│       │   ├── auth.ts
│       │   ├── knowledge.ts
│       │   ├── learning.ts
│       │   ├── review.ts
│       │   ├── speech.ts
│       │   ├── habits.ts
│       │   ├── goals.ts
│       │   ├── classics.ts
│       │   ├── dashboard.ts
│       │   └── system.ts
│       │
│       ├── views/                          # 38个页面
│       │   ├── dashboard/index.vue
│       │   ├── learning/    (4 pages)
│       │   ├── knowledge/   (5 pages)
│       │   ├── review/      (5 pages)
│       │   ├── speech/      (3 pages)
│       │   ├── application/ (2 pages)
│       │   ├── classics/    (3 pages)
│       │   ├── habits/      (3 pages)
│       │   ├── goals/       (2 pages)
│       │   ├── system/      (4 pages)
│       │   └── analytics/   (4 pages)
│       │
│       ├── components/                     # 通用组件
│       │   ├── charts/  (RadarChart, LineTrend, HeatmapCalendar, ForceGraph)
│       │   ├── cards/   (StatCard, HabitCard, GoalCard)
│       │   └── forms/   (SmartGoalForm, ReviewForm, SpeechEditor)
│       │
│       ├── router/                         # 路由配置
│       ├── store/                          # Pinia状态管理
│       ├── composables/                    # 组合式函数
│       └── utils/                          # 工具函数
│
├── database/
│   ├── schema.sql                          # 基础12表
│   ├── schema_extended.sql                 # 扩展14表
│   └── seed_data.sql                       # [新增] 种子数据
│
└── scripts/                                # [新增] 运维脚本
    ├── backup.sh
    ├── health_check.sh
    └── init_dev.sh
```

---

## 三、Docker 本地运行架构

### 3.1 四容器编排

```
                    ┌─────────────────────────────────────┐
                    │     Docker Network: edward-net       │
                    │                                      │
  浏览器 :80 ──────────► frontend (Nginx)                  │
                    │    │ 静态文件 + SPA回退               │
                    │    │ /api/* 反向代理                  │
                    │    ▼                                 │
  开发者 :8000 ────────► api (FastAPI/Uvicorn)             │
                    │    │                                 │
                    │    ├────► postgres :5432              │
                    │    │      (26张表 + 自动初始化)       │
                    │    │                                 │
                    │    └────► redis :6379                 │
                    │           (缓存/去重/会话)            │
                    │                                      │
                    └─────────────────────────────────────┘
                    
  宿主机端口映射:
  ┌──────┬──────────┬──────────────────────────┐
  │ 端口 │ 服务      │ 用途                      │
  ├──────┼──────────┼──────────────────────────┤
  │ 80   │ frontend │ 前端管理后台               │
  │ 8000 │ api      │ 后端API（开发/调试）        │
  │ 5432 │ postgres │ 数据库（开发调试用）         │
  │ 6379 │ redis    │ 缓存（开发调试用）           │
  └──────┴──────────┴──────────────────────────┘
```

### 3.2 启动顺序

```
postgres (healthy) ──┐
                     ├──► api (healthy) ──► frontend
redis (healthy) ─────┘
```

### 3.3 Docker未安装的替代方案

由于Edward本地Docker尚未安装，提供直接运行方案：

```bash
# 1. 安装并启动 PostgreSQL（本地安装或远程）
# 2. 安装并启动 Redis（本地安装或远程）

# 3. 启动后端
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload --port 8000

# 4. 启动前端（开发模式）
cd frontend
pnpm install
pnpm dev                     # Vite开发服务器 :5173
```

---

## 四、前端页面结构（VBEN ADMIN）

### 4.1 页面树形结构

```
Edward 个人成长系统
│
├── 首页 Dashboard                          /dashboard
│   ├── 成长概览卡片（连续天数/完成率/知识总量/目标进度）
│   ├── 今日学习任务（晨间/午间/晚间三段式）
│   ├── 学习趋势迷你图（近7日折线）
│   └── 快捷入口（录入/打卡/复盘/演讲）
│
├── 学习中心 Learning                       /learning
│   ├── 今日学习任务                        /learning/today
│   ├── 学习内容库                          /learning/content
│   ├── 学习记录                            /learning/records
│   └── 每日打卡                            /learning/checkin
│
├── 知识管理 Knowledge                      /knowledge
│   ├── 快速录入（文字/语音）                /knowledge/capture
│   ├── 知识洞察列表                        /knowledge/insights
│   ├── 结构化知识库                        /knowledge/structured
│   ├── 知识库浏览                          /knowledge/library
│   └── 知识图谱可视化（ECharts力导向图）     /knowledge/graph
│
├── 复盘系统 Review                         /review
│   ├── 复盘会话列表                        /review/sessions
│   ├── 每日复盘（5个核心问题）              /review/daily
│   ├── 每周复盘（MASK维度对比）             /review/weekly
│   ├── 月度/季度复盘（SMART+Maslow）        /review/periodic
│   └── 复盘总结归档                        /review/summaries
│
├── 演讲工坊 Speech                         /speech
│   ├── 演讲稿管理（TED/Toastmasters/电梯/故事） /speech/drafts
│   ├── 双语演讲（中英对照）                 /speech/bilingual
│   └── 素材库（故事/名言/案例/数据/类比）     /speech/materials
│
├── 应用追踪 Application                    /application
│   ├── 知识应用记录                        /application/logs
│   └── 应用统计分析                        /application/stats
│
├── 国学经典 Classics                       /classics
│   ├── 学习进度总览（6部经典进度卡）         /classics/progress
│   ├── 经典详情（原文+译文+解读三栏）        /classics/detail/:id
│   └── 读书笔记                            /classics/notes
│
├── 习惯追踪 Habits                         /habits
│   ├── 习惯管理（CRUD+streak）              /habits/manage
│   ├── 打卡日历（GitHub风格热力图）          /habits/calendar
│   └── 统计分析（完成率+趋势）              /habits/stats
│
├── 目标管理 Goals                          /goals
│   ├── 目标列表（SMART表单）               /goals/list
│   └── 里程碑追踪（时间线）                 /goals/milestones/:id
│
├── 系统管理 System                         /system
│   ├── 用户设置（画像+偏好+雷达图）          /system/profile
│   ├── 推送配置（渠道开关+时间+免打扰）      /system/push
│   ├── 爬虫管理（状态+手动触发）             /system/crawler
│   └── 预警规则（三级预警CRUD）              /system/alerts
│
└── 数据分析 Analytics                      /analytics
    ├── 成长仪表盘（大数字+ROI+AI评语）       /analytics/dashboard
    ├── 领域完成度雷达图（MASK/Maslow/7Habits） /analytics/radar
    ├── 行为模式分析（活跃时段热力图）         /analytics/patterns
    └── 趋势分析（时长/完成率/知识积累曲线）   /analytics/trends
```

### 4.2 技术选型

| 维度 | 选型 |
|------|------|
| 框架 | Vue Vben Admin v2.11+ (Vue 3) |
| UI库 | Ant Design Vue 4.x |
| 构建 | Vite 5.x |
| 语言 | TypeScript 5.x |
| 状态 | Pinia 2.x |
| 图表 | ECharts 5.5 + vue-echarts |
| 知识图谱 | ECharts Graph (力导向图) |
| 打卡热力图 | ECharts Calendar + Heatmap |

---

## 五、后端 API 端点矩阵（60+）

### 5.1 已有（需修复）

| 模块 | 端点 | 状态 |
|------|------|------|
| 认证 | `POST /api/v1/auth/login` | 需新增 |
| 用户 | `GET/PUT /api/v1/users/profile` | 需新增 |
| 知识 | `POST /api/insights/capture` | 需修复NLP |
| 知识 | `GET /api/insights/` | 可用 |
| 知识 | `POST /api/insights/structure` | 可用 |
| 复盘 | `POST /api/review/trigger` | 可用 |
| 复盘 | `POST /api/review/{id}/respond` | 可用 |
| 复盘 | `POST /api/review/summary` | **有BUG** |
| 演讲 | `POST /api/speech/generate` | 可用 |
| 演讲 | `GET /api/speech/bilingual/{id}` | **有BUG** |
| 应用 | `GET /api/application/stats` | **有BUG** |
| 打卡 | `POST /checkins/` | 可用 |
| 录入 | `POST /captures/` | 可用 |
| 推送 | `POST /test-push/` | 需修Token |

### 5.2 需新增

| 模块 | 端点 | 用途 |
|------|------|------|
| 习惯 | `GET /habits` | 习惯列表 |
| 习惯 | `POST /habits/{id}/log` | 习惯打卡 |
| 目标 | `GET /goals` | 目标列表 |
| 目标 | `PUT /goals/{id}/progress` | 更新进度 |
| 国学 | `GET /api/classics/progress` | 经典进度 |
| 国学 | `GET /api/classics/{name}/{chapter}` | 章节内容 |
| 仪表盘 | `GET /api/v1/dashboard/overview` | 总览数据 |
| 仪表盘 | `GET /api/v1/dashboard/maslow` | Maslow评分 |
| 仪表盘 | `GET /api/v1/dashboard/mask` | MASK评分 |
| 推荐 | `GET /api/v1/recommendations/daily` | 每日推荐 |
| 爬虫 | `GET /api/crawler/status` | 爬虫状态 |
| 爬虫 | `POST /api/crawler/{name}/run` | 运行爬虫 |
| 预警 | `GET/POST/PUT /api/alerts/rules` | 预警规则CRUD |
| 图谱 | `GET /api/insights/graph` | 知识图谱数据 |

---

## 六、实施路线图

### 6.1 四阶段执行计划

```
第1阶段 [P0] 基础修复与安全保障           预计 2-3 小时
├── 安全加固：.gitignore + 文档脱敏 + 强密钥
├── BUG修复：init_db.py / review.py / speech.py / application.py
├── 依赖精简：移除uuid/datetime/torch
├── 项目结构：创建docs/ + frontend/ + scripts/ 目录
└── Docker修复：docker-compose.yml + Dockerfile + entrypoint

第2阶段 [P0] 后端功能补全                预计 3-4 小时
├── 核心层：schemas/ + core/security + dependencies
├── 路由重构：模块化拆分 + /api/v1/ 统一前缀
├── 新增路由：habits + goals + classics + dashboard + crawler
├── 业务层：services/ 知识/学习/复盘/演讲/习惯/目标
├── NLP增强：意图分类 + 领域识别 + 实体提取
├── 推荐引擎：内容based + 难度匹配 + 新鲜度
└── 飞书修复：Token缓存 + App ID统一 + 推送测试

第3阶段 [P0] 前端开发                    预计 4-6 小时
├── 项目初始化：clone VBEN ADMIN + 依赖安装
├── API层：Axios封装 + 12个API模块
├── 路由配置：10个模块路由 + 守卫
├── 核心页面：Dashboard + 知识管理 + 学习中心 + 习惯打卡
├── 进阶页面：复盘系统 + 演讲工坊 + 国学经典 + 目标管理
├── 分析页面：雷达图 + 趋势图 + 热力图 + 知识图谱
└── Docker化：前端Dockerfile + nginx.conf

第4阶段 [P1] 集成验证                    预计 1-2 小时
├── Docker全链路启动验证
├── 前后端联调测试
├── 飞书推送端到端测试
├── 数据库初始化 + 种子数据
└── 文档更新 + CHANGELOG
```

### 6.2 交付物清单

| 交付物 | 数量 | 说明 |
|--------|------|------|
| 修复的BUG | 5个 | init_db/review/speech/application/models |
| 新增后端文件 | ~30个 | schemas/core/services/routes/tests |
| 新增前端文件 | ~60个 | views/api/components/router/store |
| 修复的配置文件 | 5个 | docker-compose/Dockerfile/requirements/.env |
| 新增运维文件 | 5个 | scripts/backup/health/init |
| 文档归档 | 20+个 | 移入docs/分目录 |

---

## 七、风险与对策

| 风险 | 影响 | 对策 |
|------|------|------|
| Docker未安装 | 无法容器化运行 | 提供直接Python+Node.js运行方案 |
| 飞书授权过期 | 推送中断 | Refresh Token 7天后过期，需提前刷新 |
| 密钥已泄露 | 安全风险 | 文档脱敏 + 建议轮换App Secret |
| torch依赖过大 | 镜像>5GB | 移除torch，用规则引擎替代NLP |
| 前端开发量大 | 60+文件 | 利用VBEN模板，优先核心页面 |

---

**Edward，请审阅此规划。确认后我立即启动4阶段并行执行。**

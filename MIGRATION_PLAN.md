# Edward 个人成长成功系统 — 完整迁移优化计划

**日期**: 2026-10-12
**目标**: 将会话 14fabd93 的所有成果完整迁移到 `D:\Edward 个人成长成功系统\`，并从专家角度优化补全至可部署运行状态

---

## 一、当前状态诊断

### 专家团评估汇总

| 维度 | 评分 | 核心问题 |
|------|------|----------|
| 架构完整性 | 78/100 | 设计文档齐全，但模块间接口未明确定义 |
| 部署就绪度 | 62/100 | 密钥泄露严重，Docker配置有误，依赖包不合理 |
| 后端代码 | 48/100 | 4个运行时崩溃BUG + 业务逻辑仅30% + 无认证 |
| 飞书集成 | 65/100 | App ID不一致 + Token缓存BUG + 授权7天后过期 |

### 发现的关键BUG（阻塞系统运行）

| BUG | 位置 | 影响 |
|-----|------|------|
| init_db.py 引用不存在的 HabitTemplate 模型 | init_db.py | 数据库初始化直接崩溃 |
| ReviewSummary 字段不匹配（period_start等不存在） | routes/review.py | 创建复盘总结时报错 |
| BilingualSpeech.speech_id 应为 speech_draft_id | routes/speech.py | 查询双语演讲时报错 |
| ApplicationStats 缺少 avg_effectiveness 等字段 | routes/application.py | 统计更新时报错 |
| models_extended.py 未导入 Date 类型 | models_extended.py | 模型加载可能失败 |

### 安全隐患
- 所有API无认证保护，user_id硬编码为固定UUID
- CORS配置 `allow_origins=["*"]` + `allow_credentials=True`
- 飞书App Secret明文出现在5+个文档文件中
- 数据库密码 `edward123` 为弱密码且广泛暴露

### 已有资产（无需重建）
- 20+ 设计文档（架构、API、部署、学习计划等）
- backend/ Python代码骨架（main.py, config.py, models.py等）
- database/ SQL schema（26张表）
- docker-compose.yml + Dockerfile

---

## 二、迁移优化工作分解（6个Phase）

### Phase 0: 安全加固 [P0-紧急]
**目标**: 清除所有泄露的密钥，建立安全基线

| 任务 | 说明 |
|------|------|
| 0.1 创建 `.gitignore` | 排除 .env, __pycache__, *.pyc, .git |
| 0.2 创建 `.dockerignore` | 排除 .env, .git, __pycache__, *.md |
| 0.3 文档脱敏 | 将所有 .md 文件中的真实 App Secret、Open ID、Chat ID 替换为占位符 `${FEISHU_APP_SECRET}` 等 |
| 0.4 生成强密钥 | 替换弱密码 `edward123` 和弱 JWT Secret |
| 0.5 凭证集中管理 | 确保所有敏感信息仅在 `.env` 中存在 |

### Phase 1: 项目结构重组 [P0]
**目标**: 建立清晰的项目目录结构，补全缺失文件

```
D:\Edward 个人成长成功系统\
├── .gitignore                    # 新增
├── .dockerignore                 # 新增
├── .env.example                  # 新增（模板，不含真实值）
├── README.md                     # 更新（统一入口）
├── docs/                         # 新增：所有设计文档归入
│   ├── ARCHITECTURE.md
│   ├── AGENT_SPEC.md
│   ├── AUTO_LEARNING_SYSTEM.md
│   ├── KNOWLEDGE_CRYSTALLIZATION.md
│   ├── CHINESE_CLASSICS_PLAN.md
│   ├── IMPLEMENTATION_ROADMAP.md
│   ├── API_DOCUMENTATION.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── SYSTEM_ISOLATION.md
│   ├── USER_MANUAL.md
│   └── CHANGELOG.md              # 新增
├── backend/
│   ├── .env                      # 真实凭证（不入git）
│   ├── .env.example              # 模板
│   ├── requirements.txt          # 精简（移除torch/transformers/uuid/datetime）
│   ├── Dockerfile                # 修复
│   ├── docker-compose.yml        # 修复（移到根目录）
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py               # 完善路由注册
│   │   ├── config.py             # 使用pydantic-settings
│   │   ├── database.py           # 连接池优化
│   │   ├── models.py             # 基础模型
│   │   ├── models_extended.py    # 扩展模型
│   │   ├── schemas.py            # 新增：Pydantic请求/响应模型
│   │   ├── dependencies.py       # 新增：依赖注入
│   │   ├── nlp.py                # 增强：意图分类+实体提取
│   │   ├── crawler.py            # 完善：实际内容源
│   │   ├── recommender.py        # 新增：推荐引擎
│   │   ├── push_services.py      # 完善推送逻辑
│   │   ├── scheduler.py          # 完善定时任务
│   │   └── routes/               # 新增：路由模块化
│   │       ├── __init__.py
│   │       ├── knowledge.py      # 知识管理API
│   │       ├── review.py         # 复盘系统API
│   │       ├── speech.py         # 演讲生成API
│   │       ├── application.py    # 应用追踪API
│   │       ├── classics.py       # 国学学习API
│   │       └── push.py           # 推送测试API
│   ├── init_db.py
│   ├── start.sh
│   └── tests/                    # 新增：测试目录
│       ├── __init__.py
│       ├── test_api.py
│       ├── test_nlp.py
│       └── test_crawler.py
├── database/
│   ├── schema.sql                # 基础12表
│   ├── schema_extended.sql       # 扩展14表
│   └── seed_data.sql             # 新增：种子数据（演讲模板、国学章节）
└── scripts/                      # 新增：运维脚本
    ├── backup.sh                 # 数据库备份
    ├── restore.sh                # 数据库恢复
    └── health_check.sh           # 健康检查
```

### Phase 2: 后端BUG修复与代码补全 [P0]
**目标**: 修复4个运行时崩溃BUG，补全核心功能，让系统可实际运行

**2A - 紧急BUG修复（阻塞运行）：**

| 任务 | 说明 |
|------|------|
| 2A.1 修复 init_db.py | 移除 HabitTemplate 引用，修正 User/UserProfile 字段匹配ORM模型 |
| 2A.2 修复 routes/review.py | ReviewSummary 字段映射对齐ORM模型（period_start/period_end等） |
| 2A.3 修复 routes/speech.py | `speech_id` → `speech_draft_id` 字段名修正 |
| 2A.4 修复 routes/application.py | ApplicationStats 移除不存在的字段（avg_effectiveness等） |
| 2A.5 修复 models_extended.py | 补充 `from sqlalchemy import Date` 导入 |

**2B - 核心功能补全：**

| 任务 | 说明 |
|------|------|
| 2B.1 精简 requirements.txt | 移除 uuid/datetime（标准库）; torch/transformers 标记可选 |
| 2B.2 创建 schemas.py | Pydantic 请求/响应模型 |
| 2B.3 创建 dependencies.py | 数据库会话依赖注入 |
| 2B.4 路由模块化 | main.py 路由拆分到 routes/ 子模块 |
| 2B.5 完善 main.py | 路由注册 + CORS安全配置 + 全局异常处理 |
| 2B.6 增强 nlp.py | 意图分类（6类）+ 领域识别（5领域）+ 实体提取 |
| 2B.7 完善 crawler.py | 实现3个实际爬虫（ArXiv RSS、国学经典、TED RSS） |
| 2B.8 新增 recommender.py | 轻量推荐引擎（内容based + 难度匹配 + 新鲜度） |
| 2B.9 完善 push_services.py | 修复Token缓存 + 错误处理 + 重试机制 |
| 2B.10 完善 scheduler.py | 6个定时任务的实际业务逻辑 |
| 2B.11 新增习惯/目标管理API | 模型已存在但缺少API端点 |
| 2B.12 新增国学学习API | 支持12个月学习计划的进度追踪 |

### Phase 3: 飞书集成修复 [P1]
**目标**: 统一App ID，修复Token缓存BUG，验证推送链路

| 任务 | 说明 |
|------|------|
| 3.1 统一 lark-cli App ID | 将 lark-cli 从旧应用 `cli_aa49e73345f9dcc5` 重新配置为新应用 `cli_aa410c43d4b8dcb8` |
| 3.2 修复 Token 缓存 BUG | push_services.py 中 `_token_expire` 改为存储绝对时间戳，判断条件改为 `time.time() < _token_expire` |
| 3.3 刷新 User Token | Refresh Token 7天后过期（至10-19），需触发自动刷新或重新授权 |
| 3.4 验证 Base 表结构 | 8张表已确认完整匹配（每日打卡/读书追踪/周复盘/月度里程碑/习惯追踪/快速录入/知识库/预警规则） |
| 3.5 端到端推送测试 | 运行 test_feishu_bot.py 验证新 App ID 的消息发送 |
| 3.6 建立数据同步机制 | 明确 PostgreSQL ↔ 飞书Base 的同步方向和触发机制 |

### Phase 4: Docker与部署修复 [P1]
**目标**: Docker配置可直接使用

| 任务 | 说明 |
|------|------|
| 4.1 修复 docker-compose.yml | 路径修正、env_file引入、密码变量化 |
| 4.2 修复 Dockerfile | 分离初始化与运行阶段，使用entrypoint脚本 |
| 4.3 创建 entrypoint.sh | 启动前自动执行数据库迁移 |
| 4.4 统一文档 | 合并矛盾的部署说明，一份权威文档 |

### Phase 5: 运维脚本与监控 [P2]
**目标**: 基本的运维保障

| 任务 | 说明 |
|------|------|
| 5.1 数据库备份脚本 | scripts/backup.sh |
| 5.2 健康检查脚本 | scripts/health_check.sh |
| 5.3 创建 CHANGELOG.md | 记录本次迁移变更 |

---

## 三、执行策略

### 并行执行计划

```
第1波（并行）:
  ├── Agent A: Phase 0 安全加固（.gitignore + 文档脱敏 + 强密钥）
  ├── Agent B: Phase 1 项目结构重组（创建目录、移动文档）
  └── Agent C: Phase 2 后端代码补全（requirements + config + schemas）

第2波（并行，依赖第1波）:
  ├── Agent D: Phase 2 续（routes/ + nlp + crawler + recommender）
  ├── Agent E: Phase 3 飞书集成修复
  └── Agent F: Phase 4 Docker修复

第3波:
  └── Agent G: Phase 5 运维脚本 + 最终验证 + CHANGELOG
```

### 不做的事
- 不重建已有的设计文档（仅整理归档）
- 不实现前端UI（飞书Base即前端）
- 不引入 torch/transformers（用轻量规则引擎替代）
- 不改变飞书App ID/Base Token等核心标识

---

## 四、预期交付物

完成后你将拥有：
1. 结构清晰、密钥安全的项目目录
2. 可直接 `docker-compose up` 启动的完整后端
3. 24个API端点全部可调用
4. 飞书推送链路验证通过
5. 6个定时任务配置就绪
6. 基本运维脚本

---

**Edward，请确认此计划是否可以开始执行，或需要调整？**

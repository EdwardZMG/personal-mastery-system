# Changelog

## v6.0.0 (2026-10-12) — 完整迁移与重构

### 重大变更
- **项目迁移**: 从会话 14fabd93 完整迁移到独立项目目录
- **前端**: 新增 Vue 3 + Vite + Ant Design Vue 4.x 管理后台（VBEN ADMIN 风格）
- **后端重构**: 路由模块化、Pydantic schemas、JWT 认证、服务层

### 新增
- 14个 API 路由模块（auth, knowledge, learning, checkins, goals, habits, classics, dashboard, recommendations, crawler, admin, review, speech, application）
- 推荐引擎（基于内容 + 难度匹配 + 新鲜度加权）
- 通知服务层（个性化推送）
- 前端 38 个页面（仪表盘、知识库、学习、复盘、演讲、目标、习惯、国学等）
- 种子数据（演讲模板、国学经典章节、AI/营销/英语学习内容）
- 运维脚本（备份、恢复、健康检查）
- Windows 一键启动脚本（start-all.bat）

### 修复
- `push_services.py`: Token 缓存 bug（过期时间计算错误导致 token 永不刷新）
- `init_db.py`: 移除不存在的 HabitTemplate 引用，修正 User/UserProfile 字段
- `review.py`: ReviewSummary 字段对齐 ORM 模型
- `speech.py`: BilingualSpeech 查询字段修正（speech_id → speech_draft_id）
- `application.py`: ApplicationStats 字段对齐 ORM 模型
- `models_extended.py`: 添加缺失的 Date 类型导入
- `requirements.txt`: 移除 uuid/datetime 标准库包，注释掉 torch/transformers 大型依赖
- `main.py`: CORS 从 allow_all 改为配置指定源，替换废弃的 on_event 为 lifespan
- `database.py`: 添加连接池配置（pool_size, max_overflow, pool_recycle）
- `docker-compose.yml`: 修正 SQL 挂载路径，添加 env_file，移除源码挂载
- `Dockerfile`: 多阶段构建优化

### 安全
- 创建 `.gitignore` / `.dockerignore` 排除敏感文件
- 创建 `.env.example` 模板（不含真实凭证）
- 文档脱敏（设计文档中的真实密钥替换为占位符）

---

## v5.0.0 (2026-10-11) — 初始设计

### 功能
- 26 张数据库表设计（12 基础 + 14 扩展）
- 飞书 Bot 集成（OAuth + 推送 + Base）
- NLP 引擎（意图分类 + 领域识别 + 实体提取）
- 定时推送系统（6 个定时任务）
- 20+ 设计文档

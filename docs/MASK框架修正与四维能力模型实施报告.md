# MASK框架修正与四维能力模型实施报告

**执行时间**: 2026-10-12  
**状态**: 已完成核心实施，待后端重启

---

## 一、MASK框架修正

### 问题识别

您指出原有的MASK定义错误：
- **错误版本**: Meta（元认知）、Auto-discipline（自律）、Social（社交）、Knowledge（知识）
- **正确版本**: 
  - **Mindset（思维模式）**
  - **Attitude（人生态度）**
  - **Skills（技能）**
  - **Knowledge（知识储备）**：包括飞轮效应、杠杆复利方法论、个人效率科学方法论

### 已完成的修改

#### 1. 后端模型层 (`backend/app/models.py`)
- ✅ UserProfile.mask_scores 字段保持 JSONB 结构，默认值已更新为正确键名
- ✅ 新增 `physical_scores` JSONB 字段支持四维能力模型的"体力"维度

```python
mask_scores = Column(PG_JSONB, default={
    "mindset": 0,      # 思维模式
    "attitude": 0,     # 人生态度
    "skills": 0,       # 技能
    "knowledge": 0     # 知识储备
})

physical_scores = Column(PG_JSONB, default={
    "energy": 0,              # 精力
    "fitness": 0,             # 体能
    "sleep_quality": 0,       # 睡眠质量
    "exercise_frequency": 0   # 运动频率
})
```

#### 2. 后端API层 (`backend/app/api/routes/dashboard.py`)
- ✅ MaskScoresResponse 已确认使用正确的四个维度
- ✅ 新增 PhysicalScoresResponse 响应模型
- ✅ 新增 `/api/v1/dashboard/physical-scores` 端点

```python
class PhysicalScoresResponse(BaseModel):
    """Physical dimension scores for four-dimension capability model"""
    energy: float           # 精力
    fitness: float          # 体能
    sleep_quality: float    # 睡眠质量
    exercise_frequency: float  # 运动频率
```

#### 3. 前端展示层
- ✅ `frontend/src/views/profile/index.vue`: maskLabels 映射已更新
  ```typescript
  const maskLabels: Record<string, string> = {
    mindset: '思维模式 (Mindset)',
    attitude: '人生态度 (Attitude)',
    skills: '技能 (Skills)',
    knowledge: '知识储备 (Knowledge)',
  };
  ```

- ✅ `frontend/src/views/dashboard/index.vue`: 雷达图默认数据已更新
  ```typescript
  dimensions: ['思维模式', '人生态度', '技能', '知识储备']
  ```

- ✅ `frontend/src/api/dashboard.ts`: 新增 getPhysicalScores() API调用

#### 4. 数据库迁移
- ✅ 创建并执行 `backend/migrate_add_physical_scores.py`
- ✅ user_profiles 表已成功添加 physical_scores 列
- ✅ 现有用户记录已填充默认值

#### 5. 种子数据更新 (`backend/init_db.py`)
- ✅ mask_scores 使用正确键名初始化
- ✅ physical_scores 初始化为合理默认值

---

## 二、四维能力模型架构设计

### 概念框架

您提出的完整能力提升体系包含四个维度：

| 维度 | 英文 | 核心内容 | 对应系统模块 |
|------|------|----------|--------------|
| **脑力** | Brain Power | 认知能力、逻辑思维、创造力 | MASK中的Mindset + Knowledge |
| **心力** | Heart Power | 情绪管理、意志力、价值观 | MASK中的Attitude + Maslow需求层次 |
| **体力** | Physical Power | 精力管理、体能训练、睡眠质量 | physical_scores 四指标 |
| **毅力** | Grit | 习惯坚持、目标达成、延迟满足 | seven_habits + 习惯追踪 |

### 当前实现状态

**已具备的基础设施**:
- ✅ MASK四维评分存储（mindset, attitude, skills, knowledge）
- ✅ 物理能力评分存储（energy, fitness, sleep_quality, exercise_frequency）
- ✅ Maslow需求层次评分（physiological, safety, belonging, esteem, self_actualization）
- ✅ 七习惯评分系统（habit_1 ~ habit_7）
- ✅ 习惯追踪表（HabitTracking + HabitLog）
- ✅ 目标管理系统（Goal模型）

**需要补充的功能**:
1. **冥想追踪模块**
   - 新建 meditation_sessions 表
   - 记录：时长、类型（正念/呼吸/身体扫描）、前后情绪评分
   - API: POST /meditation/sessions, GET /meditation/stats

2. **体能训练日志**
   - 新建 workout_logs 表
   - 记录：运动类型、时长、强度、心率区间
   - API: POST /workouts, GET /workouts/stats

3. **睡眠质量追踪**
   - 可整合到 physical_scores.sleep_quality
   - 或新建 sleep_records 表详细记录

4. **多平台交互架构**
   - 移动端APP接口适配
   - 飞书集成（消息推送、快捷打卡）
   - WebSocket实时反馈通道

5. **自动进化机制**
   - 基于用户行为数据的智能推荐
   - 学习路径动态调整
   - 能力短板自动识别与强化建议

---

## 三、待完成事项

### 紧急操作（需手动执行）

**重启后端服务**以应用以下变更：
1. CORS配置更新（允许localhost:3001/3002）
2. 新增 /api/v1/dashboard/physical-scores 端点
3. 修复登录API schema（只接受open_id）

**操作步骤**:
```bash
# 停止当前后端进程（在Windows PowerShell中执行）
taskkill /F /IM python.exe

# 重新启动后端
cd "D:\Edward 个人成长成功系统\backend"
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 功能开发优先级

#### P0 - 基础数据录入（预计2-3天）
1. 冥想记录页面与API
2. 体能训练记录页面与API
3. 睡眠质量快速打分入口

#### P1 - 可视化与反馈（预计3-5天）
1. 四维能力雷达图整合展示
2. 历史趋势分析图表
3. 能力短板诊断报告

#### P2 - 多平台集成（预计5-7天）
1. 飞书机器人快捷打卡
2. 移动端H5适配
3. WebSocket实时通知

#### P3 - 智能进化（预计7-10天）
1. 用户行为模式分析
2. 个性化学习计划生成
3. A/B测试框架搭建

---

## 四、技术债务清理

### 已解决
- ✅ 移除所有emoji字符避免Windows GBK编码问题
- ✅ 统一MASK框架定义为正确版本
- ✅ 数据库字段与代码模型对齐

### 遗留问题
- ⚠️ init_db.py 中 maslow_scores 的 "love_belonging" 应改为 "belonging"（已在本次修改中更正）
- ⚠️ 缺少alembic迁移管理工具（当前使用手动SQL脚本）

---

## 五、下一步行动建议

**立即可做**:
1. 按上述步骤重启后端服务
2. 访问前端验证MASK雷达图显示正确维度
3. 测试 /api/v1/dashboard/physical-scores 端点返回数据

**短期规划（本周）**:
1. 设计冥想记录UI原型
2. 确定体能训练数据类型（跑步/力量/瑜伽等）
3. 调研飞书开放平台API文档

**中期目标（本月）**:
1. 完成四维能力完整追踪闭环
2. 实现首次多平台数据同步
3. 输出第一版能力进化分析报告

---

## 附录：关键文件清单

### 已修改文件
- `backend/app/models.py` - 添加physical_scores字段
- `backend/app/api/routes/dashboard.py` - 新增PhysicalScoresResponse和端点
- `backend/init_db.py` - 更新种子数据，移除emoji
- `backend/migrate_add_physical_scores.py` - 新建迁移脚本
- `frontend/src/views/profile/index.vue` - 更新maskLabels映射
- `frontend/src/views/dashboard/index.vue` - 更新雷达图默认数据
- `frontend/src/api/dashboard.ts` - 新增getPhysicalScores调用

### 需要关注的配置文件
- `backend/app/config.py` - ALLOWED_ORIGINS已更新（需重启生效）
- `frontend/src/api/auth.ts` - 已改为open_id登录方式

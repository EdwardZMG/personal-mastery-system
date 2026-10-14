# Edward 智能成长系统 - 完整架构设计 v5.0

## 一、系统总览

```
┌─────────────────────────────────────────────────────────┐
│                    用户触达层                            │
│  ┌──────────┐  ┌──────────  ┌──────────┐  ┌────────┐ │
│  │ 飞书Bot  │  │ 微信推送 │  │ Web App  │  │Mobile  │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    交互层 (Interaction)                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 多模态输入：文字/语音/图片                        │   │
│  │ 智能对话：NLP + 意图识别 + 情感分析              │   │
│  │ 推送引擎：定时 + 触发 + 个性化                   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  业务逻辑层 (Business Logic)             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ────────┐ │
│  │ 学习引擎 │  │ 内容引擎 │  │ 预警引擎 │  │进化引擎│ │
│  └──────────┘  ──────────┘  └──────────┘  └───────┘ │
─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    数据层 (Data Layer)                   │
│  ┌──────────  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ PostgreSQL│ │  Redis   │  │ElasticS. │  │   S3   │ │
│  │ 主数据库  │ │  缓存    │  │ 搜索引擎 │  │文件存储│ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    分析层 (Analytics)                    │
│  ┌──────────┐  ┌──────────  ┌──────────┐  ────────┐ │
│  │ 学习分析 │  │ 行为分析 │  │ 效果评估 │  │预测模型│ │
│  └──────────┘  └──────────┘  └──────────  └────────┘ │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  智能化层 (AI/ML Layer)                  │
│  ──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ 推荐系统 │  │ NLP引擎  │  │ 知识图谱 │  │自适应  │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 二、数据层设计 (Data Layer)

### 2.1 核心数据模型

#### 用户表 (users)
```sql
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100),
    name VARCHAR(50) NOT NULL,
    avatar_url TEXT,
    birth_date DATE,
    industry VARCHAR(50),
    role VARCHAR(50),  -- CEO/Founder/Executive/Learner
    goals TEXT[],  -- 学习目标数组
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_email ON users(email);
```

#### 用户画像表 (user_profiles)
```sql
CREATE TABLE user_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) UNIQUE,
    
    -- 学习风格
    learning_style VARCHAR(20),  -- visual/auditory/reading/kinesthetic
    
    -- 时间偏好
    preferred_push_times TIME[],  -- 活跃时间段
    timezone VARCHAR(50) DEFAULT 'Asia/Shanghai',
    
    -- 完成度统计
    completion_rate DECIMAL(5,2) DEFAULT 0.00,  -- 历史完成率
    streak_days INT DEFAULT 0,  -- 连续学习天数
    longest_streak INT DEFAULT 0,
    total_study_hours DECIMAL(10,2) DEFAULT 0.00,
    
    -- 专业水平（0-10分）
    expertise_levels JSONB DEFAULT '{
        "AI": 0,
        "marketing": 0,
        "chinese_classics": 0,
        "speaking": 0
    }'::jsonb,
    
    -- 内容偏好
    content_preferences JSONB DEFAULT '{
        "AI": 0.25,
        "marketing": 0.25,
        "chinese_classics": 0.25,
        "speaking": 0.25
    }'::jsonb,
    
    -- 马斯洛需求满足度
    maslow_scores JSONB DEFAULT '{
        "physiological": 0,
        "safety": 0,
        "love_belonging": 0,
        "esteem": 0,
        "self_actualization": 0
    }'::jsonb,
    
    -- MASK维度评分
    mask_scores JSONB DEFAULT '{
        "mindset": 0,
        "attitude": 0,
        "skills": 0,
        "knowledge": 0
    }'::jsonb,
    
    -- 7个习惯践行度
    seven_habits_scores JSONB DEFAULT '{
        "habit_1": 0,
        "habit_2": 0,
        "habit_3": 0,
        "habit_4": 0,
        "habit_5": 0,
        "habit_6": 0,
        "habit_7": 0
    }'::jsonb,
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_completion_rate ON user_profiles(completion_rate);
```

#### 学习内容库 (learning_content)
```sql
CREATE TABLE learning_content (
    content_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- 基本信息
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(20) NOT NULL,  -- AI/marketing/chinese_classics/speaking
    subcategory VARCHAR(50),
    content_type VARCHAR(20) NOT NULL,  -- concept/case_study/action_task/quote
    
    -- 难度与时长
    difficulty_level INT CHECK (difficulty_level BETWEEN 1 AND 5),
    duration_minutes INT CHECK (duration_minutes BETWEEN 1 AND 120),
    
    -- 内容
    content_text TEXT NOT NULL,
    media_urls TEXT[],
    tags TEXT[],
    
    -- 来源
    source VARCHAR(200),
    author VARCHAR(100),
    
    -- 质量评估
    quality_score DECIMAL(3,2) CHECK (quality_score BETWEEN 0 AND 1),
    usage_count INT DEFAULT 0,
    effectiveness_score DECIMAL(3,2) DEFAULT 0.00,  -- 用户反馈效果
    
    -- 关联
    related_content_ids UUID[],
    prerequisites UUID[],
    
    -- 元数据
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(user_id)
);

-- 索引
CREATE INDEX idx_learning_content_category ON learning_content(category);
CREATE INDEX idx_learning_content_type ON learning_content(content_type);
CREATE INDEX idx_learning_content_difficulty ON learning_content(difficulty_level);
CREATE INDEX idx_learning_content_tags ON learning_content USING GIN(tags);
```

#### 学习记录表 (learning_records)
```sql
CREATE TABLE learning_records (
    record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    content_id UUID REFERENCES learning_content(content_id) NOT NULL,
    
    -- 学习过程
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_minutes INT,
    
    -- 完成状态
    completion_status VARCHAR(20) CHECK (completion_status IN ('completed', 'partial', 'skipped')),
    
    -- 互动数据
    engagement_score DECIMAL(3,2) CHECK (engagement_score BETWEEN 0 AND 1),
    feedback_score INT CHECK (feedback_score BETWEEN 1 AND 5),
    notes TEXT,
    
    -- 上下文
    device_type VARCHAR(20),  -- mobile/desktop/tablet
    location VARCHAR(100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_learning_records_user_id ON learning_records(user_id);
CREATE INDEX idx_learning_records_content_id ON learning_records(content_id);
CREATE INDEX idx_learning_records_completed_at ON learning_records(completed_at);
CREATE INDEX idx_learning_records_user_content ON learning_records(user_id, content_id);
```

#### 每日打卡表 (daily_checkins)
```sql
CREATE TABLE daily_checkins (
    checkin_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    checkin_date DATE NOT NULL,
    
    -- 三次推送记录
    morning_session JSONB,  -- {content_id, completed, duration, feedback}
    noon_session JSONB,
    evening_session JSONB,
    
    -- 汇总数据
    total_duration_minutes INT DEFAULT 0,
    completion_rate DECIMAL(5,2) DEFAULT 0.00,
    
    -- 状态指标
    mood_score INT CHECK (mood_score BETWEEN 1 AND 5),
    energy_level INT CHECK (energy_level BETWEEN 1 AND 5),
    
    -- 今日三件事
    top_3_tasks JSONB,  -- [{task, quadrant, completed}]
    
    -- 备注
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, checkin_date)
);

-- 索引
CREATE INDEX idx_daily_checkins_user_date ON daily_checkins(user_id, checkin_date DESC);
CREATE INDEX idx_daily_checkins_date ON daily_checkins(checkin_date);
```

#### 快速录入表 (quick_captures)
```sql
CREATE TABLE quick_captures (
    capture_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    -- 内容
    content TEXT NOT NULL,
    input_type VARCHAR(20) CHECK (input_type IN ('text', 'voice', 'image', 'file')),
    
    -- 分类
    category VARCHAR(20),  -- AI/marketing/chinese_classics/speaking/idea/other
    capture_type VARCHAR(20),  -- idea/case/resource/question/action
    
    -- 状态
    status VARCHAR(20) DEFAULT 'pending',  -- pending/processed/archived
    processed_at TIMESTAMP WITH TIME ZONE,
    processed_by UUID REFERENCES users(user_id),
    
    -- AI自动打标
    ai_tags TEXT[],
    ai_summary TEXT,
    ai_category_suggestion VARCHAR(20),
    
    -- 关联
    related_knowledge_id UUID,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_quick_captures_user_id ON quick_captures(user_id);
CREATE INDEX idx_quick_captures_status ON quick_captures(status);
CREATE INDEX idx_quick_captures_created ON quick_captures(created_at DESC);
CREATE INDEX idx_quick_captures_ai_tags ON quick_captures USING GIN(ai_tags);
```

#### 知识库表 (knowledge_base)
```sql
CREATE TABLE knowledge_base (
    knowledge_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    -- 基本信息
    title VARCHAR(200) NOT NULL,
    category VARCHAR(20) NOT NULL,  -- AI/marketing/chinese_classics/speaking
    content_type VARCHAR(20),  -- article/book/video/podcast/course
    
    -- 内容
    source_url TEXT,
    summary TEXT,  -- 核心观点（3句话）
    application TEXT,  -- 应用场景
    full_content TEXT,
    
    -- 评估
    importance_level INT CHECK (importance_level BETWEEN 1 AND 3),
    status VARCHAR(20) DEFAULT 'to_read',  -- to_read/read/practiced
    
    -- 标签
    tags TEXT[],
    
    -- 关联
    related_to_goal_id UUID,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_knowledge_base_user_id ON knowledge_base(user_id);
CREATE INDEX idx_knowledge_base_category ON knowledge_base(category);
CREATE INDEX idx_knowledge_base_status ON knowledge_base(status);
CREATE INDEX idx_knowledge_base_tags ON knowledge_base USING GIN(tags);
```

#### 目标表 (goals)
```sql
CREATE TABLE goals (
    goal_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    -- SMART原则
    title VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Specific
    specific_details TEXT,
    
    -- Measurable
    measurable_metrics JSONB,  -- {metric: value, unit: ""}
    
    -- Achievable
    achievability_score INT CHECK (achievability_score BETWEEN 1 AND 10),
    
    -- Relevant
    relevance_to_vision TEXT,
    relevant_categories TEXT[],
    
    -- Time-bound
    deadline DATE NOT NULL,
    milestones JSONB,  -- [{date, target, completed}]
    
    -- 状态
    status VARCHAR(20) DEFAULT 'active',  -- active/completed/paused/cancelled
    progress DECIMAL(5,2) DEFAULT 0.00,  -- 0-100%
    
    -- 关联
    parent_goal_id UUID REFERENCES goals(goal_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_goals_status ON goals(status);
CREATE INDEX idx_goals_deadline ON goals(deadline);
```

#### 习惯追踪表 (habit_tracking)
```sql
CREATE TABLE habit_tracking (
    habit_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    -- 习惯定义
    habit_name VARCHAR(100) NOT NULL,
    description TEXT,
    frequency VARCHAR(20) CHECK (frequency IN ('daily', 'weekly', 'monthly')),
    target_count INT DEFAULT 1,
    
    -- 统计数据
    current_streak INT DEFAULT 0,
    longest_streak INT DEFAULT 0,
    total_completions INT DEFAULT 0,
    
    -- 状态
    status VARCHAR(20) DEFAULT 'active',  -- active/paused/completed
    
    -- 关联
    related_to_goal_id UUID REFERENCES goals(goal_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_habit_tracking_user_id ON habit_tracking(user_id);
CREATE INDEX idx_habit_tracking_status ON habit_tracking(status);
```

#### 习惯打卡记录 (habit_logs)
```sql
CREATE TABLE habit_logs (
    log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    habit_id UUID REFERENCES habit_tracking(habit_id) NOT NULL,
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    log_date DATE NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(habit_id, log_date)
);

-- 索引
CREATE INDEX idx_habit_logs_habit_date ON habit_logs(habit_id, log_date DESC);
CREATE INDEX idx_habit_logs_user_date ON habit_logs(user_id, log_date DESC);
```

#### 预警规则表 (alert_rules)
```sql
CREATE TABLE alert_rules (
    rule_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    rule_name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- 触发条件
    trigger_condition JSONB NOT NULL,  -- {type: "consecutive_days", value: 3}
    
    -- 预警级别
    alert_level VARCHAR(20) CHECK (alert_level IN ('gentle', 'serious', 'reset')),
    
    -- 预警内容
    alert_content TEXT NOT NULL,
    
    -- 状态
    is_active BOOLEAN DEFAULT TRUE,
    
    -- 统计
    triggered_count INT DEFAULT 0,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_alert_rules_active ON alert_rules(is_active);
CREATE INDEX idx_alert_rules_level ON alert_rules(alert_level);
```

#### 预警日志表 (alert_logs)
```sql
CREATE TABLE alert_logs (
    alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    rule_id UUID REFERENCES alert_rules(rule_id) NOT NULL,
    
    triggered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    alert_content TEXT NOT NULL,
    
    -- 用户响应
    user_response VARCHAR(20),  -- acknowledged/dismissed/acted
    responded_at TIMESTAMP WITH TIME ZONE,
    
    -- 效果
    effectiveness_score INT CHECK (effectiveness_score BETWEEN 1 AND 5),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_alert_logs_user_id ON alert_logs(user_id);
CREATE INDEX idx_alert_logs_triggered ON alert_logs(triggered_at DESC);
```

### 2.2 数据流转设计

```
用户输入 → API Gateway → NLP处理 → 意图识别 → 数据分类 → 存储到对应表
    ↓
行为日志 → 模式识别 → 更新user_profiles → 触发推荐引擎 → 生成个性化内容
    ↓
学习记录 → 计算完成率 → 更新expertise_levels → 调整学习路径 → 进化引擎
    ↓
每日打卡 → 计算streak → 检查预警规则 → 触发预警 → 发送通知
```

### 2.3 数据安全与隐私

- **加密存储**：敏感字段使用AES-256加密
- **访问控制**：RBAC权限模型
- **数据备份**：每日自动备份，30天保留
- **隐私合规**：GDPR/个人信息保护法合规
- **数据导出**：用户可随时导出个人数据（JSON/CSV格式）

---

## 三、交互层设计 (Interaction Layer)

### 3.1 多通道触达

| 渠道 | 适用场景 | 优先级 | 技术实现 |
|------|----------|--------|----------|
| 飞书Bot | 企业用户、团队协作 | ⭐⭐ | 飞书开放平台API |
| 微信推送 | 个人用户、日常推送 | ⭐⭐ | Server酱/PushPlus |
| Web App | 深度学习、数据查看 | ⭐⭐ | React + Next.js |
| Mobile App | 随时随地、语音录入 | ⭐⭐ | React Native |
| Email | 周报、月报、重要通知 | ⭐ | SendGrid/AWS SES |
| SMS | 紧急预警、重要提醒 | ⭐ | 阿里云短信服务 |

### 3.2 交互模式设计

#### 模式1：主动推送式（默认）
```
系统 → 用户：晨间学习推送（卡片消息）
用户 → 系统：✅ 完成 / 💬 想法 / ️ 跳过
系统 → 用户：确认 + 记录到learning_records
```

#### 模式2：语音交互式
```
用户 → 系统：[语音] "今天学到AI Agent可以自动调用工具"
系统 → [ASR] 语音转文字
系统 → [NLP] 意图识别 + 实体提取
系统 → 用户：[文字] "已记录到AI分类。要添加到知识库吗？"
用户 → 系统：[语音] "好的，标记为重要"
系统 → 用户：[文字] "已添加到知识库，3星重要度"
```

#### 模式3：对话探索式
```
用户 → 系统："我想了解AI在营销中的应用"
系统 → [NLP] 意图识别：learn_topic
系统 → [推荐引擎] 检索相关内容
系统 → 用户：[推荐3个相关内容] + [1个行动建议]
用户 → 系统："第二个案例很有意思"
系统 → 用户：[深度展开] + [相关问题]
```

#### 模式4：协作学习式（企业版）
```
用户A → 系统：分享学习笔记
系统 → 团队：推送给同组学员
用户B → 系统：评论 + 补充
系统 → 用户A：收到反馈，更新笔记
系统 → 知识库：合并多人智慧
```

### 3.3 推送策略引擎

```python
class PushStrategyEngine:
    def __init__(self, user_profile):
        self.user = user_profile
        self.time_preferences = user.preferred_push_times
        self.content_preferences = user.content_preferences
        self.completion_history = user.completion_rate
    
    def determine_push_time(self):
        """根据用户活跃时间决定推送时间"""
        if self.completion_history > 0.8:
            return self.time_preferences.peak_hours
        else:
            return self.time_preferences.default_hours
    
    def determine_content_type(self):
        """根据完成率调整内容类型"""
        if self.completion_history < 0.5:
            return "light"  # 轻松内容
        elif self.completion_history < 0.8:
            return "standard"  # 标准内容
        else:
            return "challenging"  # 挑战内容
    
    def determine_frequency(self):
        """根据参与度调整推送频率"""
        engagement = self.user.recent_engagement
        if engagement > 0.9:
            return "3_times_daily"
        elif engagement > 0.7:
            return "2_times_daily"
        else:
            return "1_time_daily"
    
    def personalize_content(self, base_content):
        """个性化内容"""
        # 根据expertise_level调整难度
        if self.user.expertise_levels[base_content.category] < 2:
            return self.simplify_content(base_content)
        elif self.user.expertise_levels[base_content.category] > 4:
            return self.enhance_content(base_content)
        else:
            return base_content
```

---

## 四、分析层设计 (Analytics Layer)

### 4.1 学习分析仪表盘

```python
class LearningAnalytics:
    def get_user_dashboard(self, user_id, period="week"):
        """获取用户学习仪表盘"""
        data = {
            "overview": {
                "total_study_hours": self.get_total_hours(user_id, period),
                "completion_rate": self.get_completion_rate(user_id, period),
                "current_streak": self.get_streak(user_id),
                "content_consumed": self.get_content_count(user_id, period)
            },
            "by_category": {
                "AI": self.get_category_stats(user_id, "AI", period),
                "marketing": self.get_category_stats(user_id, "marketing", period),
                "chinese_classics": self.get_category_stats(user_id, "chinese_classics", period),
                "speaking": self.get_category_stats(user_id, "speaking", period)
            },
            "progress": {
                "learning_path": self.get_path_progress(user_id),
                "goals": self.get_goal_progress(user_id),
                "habits": self.get_habit_stats(user_id)
            },
            "maslow_needs": self.get_maslow_scores(user_id),
            "mask_dimensions": self.get_mask_scores(user_id),
            "seven_habits": self.get_habits_scores(user_id),
            "insights": self.generate_insights(user_id, period)
        }
        return data
    
    def generate_insights(self, user_id, period):
        """生成学习洞察"""
        insights = []
        
        # 完成率洞察
        rate = self.get_completion_rate(user_id, period)
        if rate > 0.8:
            insights.append(" 你的完成率超过80%，状态极佳！")
        elif rate < 0.5:
            insights.append("⚠️ 完成率偏低，建议降低每日目标")
        
        # 偏好洞察
        top_category = self.get_top_category(user_id, period)
        insights.append(f" 你最近对{top_category}最感兴趣")
        
        # 时间洞察
        peak_time = self.get_peak_time(user_id)
        insights.append(f"⏰ 你在{peak_time}学习效率最高")
        
        # 马斯洛需求洞察
        lowest_need = self.get_lowest_maslow_need(user_id)
        insights.append(f" 建议关注{lowest_need}需求的满足")
        
        return insights
```

### 4.2 行为分析模型

```python
class BehaviorAnalytics:
    def analyze_patterns(self, user_id):
        """分析用户行为模式"""
        history = get_learning_history(user_id, days=90)
        
        patterns = {
            "temporal_patterns": self.find_temporal_patterns(history),
            "content_preferences": self.find_content_preferences(history),
            "engagement_triggers": self.find_engagement_triggers(history),
            "drop_off_risks": self.predict_drop_off_risk(history),
            "optimal_push_times": self.calculate_optimal_push_times(history)
        }
        
        return patterns
    
    def predict_drop_off_risk(self, history):
        """预测流失风险"""
        recent_completion = history.last_7_days.completion_rate
        previous_completion = history.previous_7_days.completion_rate
        
        decline_rate = (previous_completion - recent_completion) / previous_completion
        
        if decline_rate > 0.3:
            return {"risk": "high", "reason": "完成率大幅下降"}
        elif decline_rate > 0.1:
            return {"risk": "medium", "reason": "完成率小幅下降"}
        else:
            return {"risk": "low", "reason": "完成率稳定"}
    
    def calculate_optimal_push_times(self, history):
        """计算最佳推送时间"""
        # 分析用户回复率最高的时间段
        time_slots = {}
        for record in history.records:
            hour = record.completed_at.hour
            if hour not in time_slots:
                time_slots[hour] = {"count": 0, "engagement": 0}
            
            time_slots[hour]["count"] += 1
            time_slots[hour]["engagement"] += record.engagement_score
        
        # 计算每个时间段的平均参与度
        for hour, data in time_slots.items():
            data["avg_engagement"] = data["engagement"] / data["count"]
        
        # 返回Top 3时间段
        sorted_times = sorted(time_slots.items(), 
                             key=lambda x: x[1]["avg_engagement"], 
                             reverse=True)
        
        return [hour for hour, _ in sorted_times[:3]]
```

### 4.3 效果评估体系

```python
class EffectivenessEvaluation:
    def evaluate_user_progress(self, user_id, period="90_days"):
        """评估用户进步"""
        baseline = get_baseline(user_id)  # 开始时的水平
        current = get_current_level(user_id)
        
        improvement = {
            "AI": current.expertise_levels["AI"] - baseline.expertise_levels["AI"],
            "marketing": current.expertise_levels["marketing"] - baseline.expertise_levels["marketing"],
            "chinese_classics": current.expertise_levels["chinese_classics"] - baseline.expertise_levels["chinese_classics"],
            "speaking": current.expertise_levels["speaking"] - baseline.expertise_levels["speaking"]
        }
        
        roi = {
            "time_invested": get_total_hours(user_id, period),
            "content_consumed": get_content_count(user_id, period),
            "skills_improved": sum(1 for v in improvement.values() if v > 0),
            "goals_achieved": get_achieved_goals_count(user_id, period),
            "habits_formed": get_formed_habits_count(user_id, period)
        }
        
        # 计算综合分数
        overall_score = self.calculate_overall_score(improvement, roi)
        
        return {
            "improvement": improvement,
            "roi": roi,
            "overall_score": overall_score,
            "testimonial": self.generate_testimonial(user_id, improvement)
        }
    
    def calculate_overall_score(self, improvement, roi):
        """计算综合分数"""
        weights = {
            "improvement": 0.4,
            "completion_rate": 0.2,
            "streak": 0.15,
            "goals_achieved": 0.15,
            "habits_formed": 0.1
        }
        
        score = 0
        score += np.mean(list(improvement.values())) * weights["improvement"]
        score += roi["completion_rate"] * weights["completion_rate"]
        score += min(roi["streak"] / 90, 1) * weights["streak"]
        score += min(roi["goals_achieved"] / 10, 1) * weights["goals_achieved"]
        score += min(roi["habits_formed"] / 6, 1) * weights["habits_formed"]
        
        return round(score * 100, 2)
```

---

## 五、智能化层设计 (AI/ML Layer)

### 5.1 推荐系统

```python
class RecommendationEngine:
    def __init__(self):
        self.content_embeddings = load_content_embeddings()
        self.user_embeddings = load_user_embeddings()
        self.knowledge_graph = load_knowledge_graph()
    
    def recommend_content(self, user_id, context):
        """推荐学习内容"""
        user = get_user(user_id)
        
        # 1. 协同过滤
        similar_users = self.find_similar_users(user)
        collaborative_recs = self.get_collaborative_recommendations(similar_users)
        
        # 2. 内容-based推荐
        content_based_recs = self.get_content_based_recommendations(user)
        
        # 3. 知识图谱推荐
        knowledge_recs = self.get_knowledge_graph_recommendations(user)
        
        # 4. 混合推荐
        final_recs = self.hybrid_recommend(
            collaborative_recs,
            content_based_recs,
            knowledge_recs,
            weights=[0.4, 0.4, 0.2]
        )
        
        # 5. 去重 + 多样性
        final_recs = self.add_diversity(final_recs, user.recent_content)
        
        # 6. 个性化排序
        final_recs = self.personalize_rank(final_recs, user)
        
        return final_recs[:5]  # 返回Top 5
    
    def find_similar_users(self, user):
        """找到相似用户"""
        user_vector = self.user_embeddings[user.id]
        similarities = cosine_similarity(user_vector, self.user_embeddings)
        top_similar = np.argsort(similarities)[-10:]
        return top_similar
    
    def hybrid_recommend(self, collab_recs, content_recs, knowledge_recs, weights):
        """混合推荐"""
        all_recs = {}
        
        for rec in collab_recs:
            all_recs[rec.content_id] = all_recs.get(rec.content_id, 0) + rec.score * weights[0]
        
        for rec in content_recs:
            all_recs[rec.content_id] = all_recs.get(rec.content_id, 0) + rec.score * weights[1]
        
        for rec in knowledge_recs:
            all_recs[rec.content_id] = all_recs.get(rec.content_id, 0) + rec.score * weights[2]
        
        # 排序
        sorted_recs = sorted(all_recs.items(), key=lambda x: x[1], reverse=True)
        
        return [Recommendation(content_id=k, score=v) for k, v in sorted_recs]
```

### 5.2 NLP引擎

```python
class NLPEngine:
    def __init__(self):
        self.intent_classifier = load_intent_model()
        self.ner = load_ner_model()
        self.sentiment = load_sentiment_model()
        self.summarizer = load_summarization_model()
        self.classifier = load_text_classification_model()
    
    def classify_intent(self, text):
        """意图分类"""
        intents = {
            "learn": "想要学习某个主题",
            "record": "记录想法/资料",
            "question": "提出问题",
            "feedback": "给予反馈",
            "navigate": "导航到某个功能",
            "social": "社交/分享"
        }
        
        intent = self.intent_classifier.predict(text)
        return intents[intent]
    
    def extract_entities(self, text):
        """实体提取"""
        entities = self.ner.extract(text)
        return {
            "topics": entities["topics"],
            "people": entities["people"],
            "organizations": entities["organizations"],
            "concepts": entities["concepts"]
        }
    
    def analyze_sentiment(self, text):
        """情感分析"""
        sentiment = self.sentiment.predict(text)
        return {
            "polarity": sentiment["polarity"],  # -1 to 1
            "emotion": sentiment["emotion"],  # joy/sadness/anger/fear/surprise
            "confidence": sentiment["confidence"]
        }
    
    def summarize_content(self, text, max_length=100):
        """内容摘要"""
        summary = self.summarizer.summarize(text, max_length)
        return summary
    
    def classify_content(self, text):
        """内容分类"""
        categories = ["AI", "marketing", "chinese_classics", "speaking", "idea", "other"]
        probs = self.classifier.predict_proba(text)
        
        return {
            "category": categories[np.argmax(probs)],
            "confidence": max(probs),
            "all_probs": dict(zip(categories, probs))
        }
```

### 5.3 知识图谱

```python
class KnowledgeGraph:
    def __init__(self):
        self.graph = load_knowledge_graph()
    
    def get_related_concepts(self, concept, depth=2):
        """获取相关概念"""
        related = self.graph.get_neighbors(concept, depth)
        return related
    
    def find_learning_path(self, start_concept, end_concept):
        """找到学习路径"""
        path = self.graph.shortest_path(start_concept, end_concept)
        return path
    
    def recommend_next_topic(self, user_current_topics):
        """推荐下一个学习主题"""
        # 基于知识图谱的拓扑排序
        next_topics = []
        for topic in user_current_topics:
            neighbors = self.graph.get_neighbors(topic, depth=1)
            next_topics.extend(neighbors)
        
        # 去重 + 评分
        next_topics = self.score_and_rank(next_topics)
        return next_topics[:3]
    
    def build_from_content(self, content_list):
        """从内容构建知识图谱"""
        for content in content_list:
            # 提取实体
            entities = self.nlp.extract_entities(content.text)
            
            # 添加节点
            for entity in entities["concepts"]:
                self.graph.add_node(entity, type="concept")
            
            # 添加边
            for i, entity1 in enumerate(entities["concepts"]):
                for entity2 in entities["concepts"][i+1:]:
                    self.graph.add_edge(entity1, entity2, type="related")
```

### 5.4 自适应学习系统

```python
class AdaptiveLearningSystem:
    def __init__(self, user_id):
        self.user = get_user(user_id)
        self.ils = ItemResponseTheory()  # 项目反应理论
    
    def adapt_difficulty(self, content_id, user_response):
        """自适应调整难度"""
        # 使用IRT模型估计用户能力
        user_ability = self.ils.estimate_ability(
            self.user.id,
            self.user.response_history
        )
        
        # 估计内容难度
        content_difficulty = self.ils.estimate_difficulty(
            content_id,
            get_all_responses(content_id)
        )
        
        # 计算最佳难度
        optimal_difficulty = user_ability + 0.5  # 略高于当前水平
        
        # 推荐合适内容
        recommended = self.find_content_by_difficulty(optimal_difficulty)
        return recommended
    
    def update_mastery_level(self, user_id, concept_id, performance):
        """更新掌握程度"""
        current_mastery = get_mastery(user_id, concept_id)
        
        # 使用贝叶斯更新
        updated_mastery = bayesian_update(
            current_mastery,
            performance,
            prior_strength=0.3
        )
        
        save_mastery(user_id, concept_id, updated_mastery)
    
    def personalize_learning_path(self, user_id):
        """个性化学习路径"""
        user = get_user(user_id)
        
        # 根据expertise_level选择路径
        if user.expertise_levels["AI"] < 2:
            return "beginner_AI_path"
        elif user.expertise_levels["AI"] < 4:
            return "intermediate_AI_path"
        else:
            return "advanced_AI_path"
```

---

## 六、技术架构 (Technical Architecture)

### 6.1 系统架构图

见上方"系统总览"部分。

### 6.2 技术栈选择

| 层级 | 技术选型 | 理由 |
|------|----------|------|
| 前端 | React Native + Next.js | 跨平台 + SEO友好 |
| 后端 | Python (FastAPI) + Node.js | AI生态 + 高并发 |
| 数据库 | PostgreSQL + Redis | 关系型 + 缓存 |
| 搜索 | Elasticsearch | 全文搜索 + 分析 |
| 消息队列 | RabbitMQ/Kafka | 异步处理 + 解耦 |
| 缓存 | Redis + Memcached | 高性能缓存 |
| 文件存储 | AWS S3 / 阿里云OSS | 对象存储 |
| CDN | CloudFront / 阿里云CDN | 全球加速 |
| 容器化 | Docker + Kubernetes | 微服务部署 |
| CI/CD | GitHub Actions / GitLab CI | 自动化部署 |
| 监控 | Prometheus + Grafana | 系统监控 |
| 日志 | ELK Stack | 日志分析 |
| AI/ML | PyTorch + TensorFlow | 深度学习 |
| NLP | HuggingFace + spaCy | 自然语言处理 |
| 推荐系统 | Surprise + LightFM | 协同过滤 |

### 6.3 部署架构

```
生产环境（Production）：
- 阿里云/ AWS 多可用区部署
- 自动扩缩容（Auto Scaling）
- 蓝绿部署 / 金丝雀发布
- 数据库主从复制 + 自动故障转移

开发环境（Development）：
- Docker Compose 本地开发
- 特性分支 + PR审查
- 自动化测试（单元/集成/E2E）

测试环境（Staging）：
- 与生产环境一致的配置
- 压力测试 + 性能测试
- 用户验收测试（UAT）
```

---

## 七、MVP实施计划

### Phase 1: 基础版（Month 1）

**核心功能：**
- ✅ 用户注册/登录
- ✅ 每日学习推送（3次/天）
- ✅ 学习记录追踪
- ✅ 基础数据分析
- ✅ 飞书/微信Bot集成

**技术实现：**
- 单体应用（Monolith）
- PostgreSQL数据库
- 简单推送服务
- 基础Web界面

**目标用户：** 100个种子用户（免费）

---

### Phase 2: 增强版（Month 2）

**新增功能：**
- ✅ 语音输入支持
- ✅ 智能内容推荐
- ✅ 预警系统
- ✅ 知识库管理
- ✅ 移动端App（React Native）

**技术升级：**
- 微服务拆分
- Redis缓存
- NLP引擎集成
- 推荐算法V1

**目标用户：** 500个付费用户（¥299/月）

---

### Phase 3: 智能版（Month 3）

**新增功能：**
- ✅ 自适应学习系统
- ✅ 知识图谱
- ✅ 团队学习功能
- ✅ 企业版功能
- ✅ 高级数据分析

**技术升级：**
- Kubernetes部署
- ML模型训练
- 实时分析引擎
- 多租户架构

**目标用户：** 1000个付费用户 + 10个企业客户

---

Edward，这个架构设计包含了：

✅ **数据层** - 完整的数据模型（12张表），支持MASK/马斯洛/SMART/7个习惯
✅ **交互层** - 多通道触达（飞书/微信/Web/Mobile），4种交互模式
✅ **分析层** - 学习分析/行为分析/效果评估，生成个性化洞察
✅ **智能层** - 推荐系统/NLP引擎/知识图谱/自适应学习

**这是一个真正的企业级系统，不是简单的Bot。**

现在请你提供：
1. 飞书群Webhook URL
2. Server酱SendKey
3. 飞书应用App ID + App Secret

我立即配置推送系统，让你明天就能开始使用！

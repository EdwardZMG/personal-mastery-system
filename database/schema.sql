-- Edward Growth System - Complete Database Schema v5.0
-- PostgreSQL 14+

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- 1. USERS & PROFILES
-- ============================================

-- Users table
CREATE TABLE users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100),
    name VARCHAR(50) NOT NULL,
    avatar_url TEXT,
    birth_date DATE,
    industry VARCHAR(50),
    role VARCHAR(50),  -- CEO/Founder/Executive/Learner
    goals TEXT[],  -- Learning goals array
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_phone ON users(phone);
CREATE INDEX idx_users_email ON users(email);

-- User profiles table
CREATE TABLE user_profiles (
    profile_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) UNIQUE,
    
    -- Learning style
    learning_style VARCHAR(20),  -- visual/auditory/reading/kinesthetic
    
    -- Time preferences
    preferred_push_times TIME[],  -- Active time slots
    timezone VARCHAR(50) DEFAULT 'Asia/Shanghai',
    
    -- Completion statistics
    completion_rate DECIMAL(5,2) DEFAULT 0.00,  -- Historical completion rate
    streak_days INT DEFAULT 0,  -- Consecutive learning days
    longest_streak INT DEFAULT 0,
    total_study_hours DECIMAL(10,2) DEFAULT 0.00,
    
    -- Expertise levels (0-10)
    expertise_levels JSONB DEFAULT '{
        "AI": 0,
        "marketing": 0,
        "chinese_classics": 0,
        "speaking": 0
    }'::jsonb,
    
    -- Content preferences
    content_preferences JSONB DEFAULT '{
        "AI": 0.25,
        "marketing": 0.25,
        "chinese_classics": 0.25,
        "speaking": 0.25
    }'::jsonb,
    
    -- Maslow needs satisfaction
    maslow_scores JSONB DEFAULT '{
        "physiological": 0,
        "safety": 0,
        "love_belonging": 0,
        "esteem": 0,
        "self_actualization": 0
    }'::jsonb,
    
    -- MASK dimensions
    mask_scores JSONB DEFAULT '{
        "mindset": 0,
        "attitude": 0,
        "skills": 0,
        "knowledge": 0
    }'::jsonb,
    
    -- 7 Habits scores
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

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_completion_rate ON user_profiles(completion_rate);

-- ============================================
-- 2. LEARNING CONTENT
-- ============================================

-- Learning content library
CREATE TABLE learning_content (
    content_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Basic info
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(20) NOT NULL,  -- AI/marketing/chinese_classics/speaking
    subcategory VARCHAR(50),
    content_type VARCHAR(20) NOT NULL,  -- concept/case_study/action_task/quote
    
    -- Difficulty & duration
    difficulty_level INT CHECK (difficulty_level BETWEEN 1 AND 5),
    duration_minutes INT CHECK (duration_minutes BETWEEN 1 AND 120),
    
    -- Content
    content_text TEXT NOT NULL,
    media_urls TEXT[],
    tags TEXT[],
    
    -- Source
    source VARCHAR(200),
    author VARCHAR(100),
    
    -- Quality assessment
    quality_score DECIMAL(3,2) CHECK (quality_score BETWEEN 0 AND 1),
    usage_count INT DEFAULT 0,
    effectiveness_score DECIMAL(3,2) DEFAULT 0.00,  -- User feedback
    
    -- Relations
    related_content_ids UUID[],
    prerequisites UUID[],
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(user_id)
);

CREATE INDEX idx_learning_content_category ON learning_content(category);
CREATE INDEX idx_learning_content_type ON learning_content(content_type);
CREATE INDEX idx_learning_content_difficulty ON learning_content(difficulty_level);
CREATE INDEX idx_learning_content_tags ON learning_content USING GIN(tags);

-- ============================================
-- 3. LEARNING RECORDS
-- ============================================

-- Learning records
CREATE TABLE learning_records (
    record_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    content_id UUID REFERENCES learning_content(content_id) NOT NULL,
    
    -- Learning process
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_minutes INT,
    
    -- Completion status
    completion_status VARCHAR(20) CHECK (completion_status IN ('completed', 'partial', 'skipped')),
    
    -- Engagement data
    engagement_score DECIMAL(3,2) CHECK (engagement_score BETWEEN 0 AND 1),
    feedback_score INT CHECK (feedback_score BETWEEN 1 AND 5),
    notes TEXT,
    
    -- Context
    device_type VARCHAR(20),  -- mobile/desktop/tablet
    location VARCHAR(100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_learning_records_user_id ON learning_records(user_id);
CREATE INDEX idx_learning_records_content_id ON learning_records(content_id);
CREATE INDEX idx_learning_records_completed_at ON learning_records(completed_at);
CREATE INDEX idx_learning_records_user_content ON learning_records(user_id, content_id);

-- ============================================
-- 4. DAILY CHECKINS
-- ============================================

-- Daily checkins
CREATE TABLE daily_checkins (
    checkin_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    checkin_date DATE NOT NULL,
    
    -- Three push sessions
    morning_session JSONB,  -- {content_id, completed, duration, feedback}
    noon_session JSONB,
    evening_session JSONB,
    
    -- Summary data
    total_duration_minutes INT DEFAULT 0,
    completion_rate DECIMAL(5,2) DEFAULT 0.00,
    
    -- State indicators
    mood_score INT CHECK (mood_score BETWEEN 1 AND 5),
    energy_level INT CHECK (energy_level BETWEEN 1 AND 5),
    
    -- Top 3 tasks
    top_3_tasks JSONB,  -- [{task, quadrant, completed}]
    
    -- Notes
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, checkin_date)
);

CREATE INDEX idx_daily_checkins_user_date ON daily_checkins(user_id, checkin_date DESC);
CREATE INDEX idx_daily_checkins_date ON daily_checkins(checkin_date);

-- ============================================
-- 5. QUICK CAPTURES
-- ============================================

-- Quick captures (voice/text input)
CREATE TABLE quick_captures (
    capture_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    -- Content
    content TEXT NOT NULL,
    input_type VARCHAR(20) CHECK (input_type IN ('text', 'voice', 'image', 'file')),
    
    -- Classification
    category VARCHAR(20),  -- AI/marketing/chinese_classics/speaking/idea/other
    capture_type VARCHAR(20),  -- idea/case/resource/question/action
    
    -- Status
    status VARCHAR(20) DEFAULT 'pending',  -- pending/processed/archived
    processed_at TIMESTAMP WITH TIME ZONE,
    processed_by UUID REFERENCES users(user_id),
    
    -- AI auto-tagging
    ai_tags TEXT[],
    ai_summary TEXT,
    ai_category_suggestion VARCHAR(20),
    
    -- Relations
    related_knowledge_id UUID,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_quick_captures_user_id ON quick_captures(user_id);
CREATE INDEX idx_quick_captures_status ON quick_captures(status);
CREATE INDEX idx_quick_captures_created ON quick_captures(created_at DESC);
CREATE INDEX idx_quick_captures_ai_tags ON quick_captures USING GIN(ai_tags);

-- ============================================
-- 6. KNOWLEDGE BASE
-- ============================================

-- Knowledge base
CREATE TABLE knowledge_base (
    knowledge_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    -- Basic info
    title VARCHAR(200) NOT NULL,
    category VARCHAR(20) NOT NULL,  -- AI/marketing/chinese_classics/speaking
    content_type VARCHAR(20),  -- article/book/video/podcast/course
    
    -- Content
    source_url TEXT,
    summary TEXT,  -- Core insights (3 sentences)
    application TEXT,  -- Application scenarios
    full_content TEXT,
    
    -- Assessment
    importance_level INT CHECK (importance_level BETWEEN 1 AND 3),
    status VARCHAR(20) DEFAULT 'to_read',  -- to_read/read/practiced
    
    -- Tags
    tags TEXT[],
    
    -- Relations
    related_to_goal_id UUID,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_knowledge_base_user_id ON knowledge_base(user_id);
CREATE INDEX idx_knowledge_base_category ON knowledge_base(category);
CREATE INDEX idx_knowledge_base_status ON knowledge_base(status);
CREATE INDEX idx_knowledge_base_tags ON knowledge_base USING GIN(tags);

-- ============================================
-- 7. GOALS (SMART)
-- ============================================

-- Goals table
CREATE TABLE goals (
    goal_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    -- SMART principles
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
    
    -- Status
    status VARCHAR(20) DEFAULT 'active',  -- active/completed/paused/cancelled
    progress DECIMAL(5,2) DEFAULT 0.00,  -- 0-100%
    
    -- Relations
    parent_goal_id UUID REFERENCES goals(goal_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_goals_user_id ON goals(user_id);
CREATE INDEX idx_goals_status ON goals(status);
CREATE INDEX idx_goals_deadline ON goals(deadline);

-- ============================================
-- 8. HABIT TRACKING
-- ============================================

-- Habit tracking
CREATE TABLE habit_tracking (
    habit_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    -- Habit definition
    habit_name VARCHAR(100) NOT NULL,
    description TEXT,
    frequency VARCHAR(20) CHECK (frequency IN ('daily', 'weekly', 'monthly')),
    target_count INT DEFAULT 1,
    
    -- Statistics
    current_streak INT DEFAULT 0,
    longest_streak INT DEFAULT 0,
    total_completions INT DEFAULT 0,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active',  -- active/paused/completed
    
    -- Relations
    related_to_goal_id UUID REFERENCES goals(goal_id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_habit_tracking_user_id ON habit_tracking(user_id);
CREATE INDEX idx_habit_tracking_status ON habit_tracking(status);

-- Habit logs
CREATE TABLE habit_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    habit_id UUID REFERENCES habit_tracking(habit_id) NOT NULL,
    user_id UUID REFERENCES users(user_id) NOT NULL,
    
    log_date DATE NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(habit_id, log_date)
);

CREATE INDEX idx_habit_logs_habit_date ON habit_logs(habit_id, log_date DESC);
CREATE INDEX idx_habit_logs_user_date ON habit_logs(user_id, log_date DESC);

-- ============================================
-- 9. ALERT SYSTEM
-- ============================================

-- Alert rules
CREATE TABLE alert_rules (
    rule_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    rule_name VARCHAR(100) NOT NULL,
    description TEXT,
    
    -- Trigger condition
    trigger_condition JSONB NOT NULL,  -- {type: "consecutive_days", value: 3}
    
    -- Alert level
    alert_level VARCHAR(20) CHECK (alert_level IN ('gentle', 'serious', 'reset')),
    
    -- Alert content
    alert_content TEXT NOT NULL,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Statistics
    triggered_count INT DEFAULT 0,
    last_triggered_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_alert_rules_active ON alert_rules(is_active);
CREATE INDEX idx_alert_rules_level ON alert_rules(alert_level);

-- Alert logs
CREATE TABLE alert_logs (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) NOT NULL,
    rule_id UUID REFERENCES alert_rules(rule_id) NOT NULL,
    
    triggered_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    alert_content TEXT NOT NULL,
    
    -- User response
    user_response VARCHAR(20),  -- acknowledged/dismissed/acted
    responded_at TIMESTAMP WITH TIME ZONE,
    
    -- Effectiveness
    effectiveness_score INT CHECK (effectiveness_score BETWEEN 1 AND 5),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_alert_logs_user_id ON alert_logs(user_id);
CREATE INDEX idx_alert_logs_triggered ON alert_logs(triggered_at DESC);

-- ============================================
-- 10. VIEWS & FUNCTIONS
-- ============================================

-- View: User dashboard summary
CREATE VIEW user_dashboard_summary AS
SELECT 
    u.user_id,
    u.name,
    up.completion_rate,
    up.streak_days,
    up.total_study_hours,
    up.expertise_levels,
    up.maslow_scores,
    up.mask_scores,
    COUNT(DISTINCT lr.record_id) as total_records,
    COUNT(DISTINCT kb.knowledge_id) as knowledge_items,
    COUNT(DISTINCT g.goal_id) FILTER (WHERE g.status = 'active') as active_goals,
    COUNT(DISTINCT ht.habit_id) FILTER (WHERE ht.status = 'active') as active_habits
FROM users u
LEFT JOIN user_profiles up ON u.user_id = up.user_id
LEFT JOIN learning_records lr ON u.user_id = lr.user_id
LEFT JOIN knowledge_base kb ON u.user_id = kb.user_id
LEFT JOIN goals g ON u.user_id = g.user_id
LEFT JOIN habit_tracking ht ON u.user_id = ht.user_id
GROUP BY u.user_id, u.name, up.completion_rate, up.streak_days, 
         up.total_study_hours, up.expertise_levels, up.maslow_scores, up.mask_scores;

-- Function: Update user completion rate
CREATE OR REPLACE FUNCTION update_user_completion_rate()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE user_profiles
    SET completion_rate = (
        SELECT 
            COUNT(*) FILTER (WHERE completion_status = 'completed')::DECIMAL / 
            NULLIF(COUNT(*), 0) * 100
        FROM learning_records
        WHERE user_id = NEW.user_id
    ),
    updated_at = NOW()
    WHERE user_id = NEW.user_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger: Auto-update completion rate
CREATE TRIGGER trg_update_completion_rate
AFTER INSERT OR UPDATE ON learning_records
FOR EACH ROW
EXECUTE FUNCTION update_user_completion_rate();

-- Function: Calculate streak
CREATE OR REPLACE FUNCTION calculate_streak(p_user_id UUID)
RETURNS INT AS $$
DECLARE
    v_streak INT := 0;
    v_check_date DATE := CURRENT_DATE;
BEGIN
    LOOP
        IF EXISTS (
            SELECT 1 FROM daily_checkins 
            WHERE user_id = p_user_id 
            AND checkin_date = v_check_date
            AND completion_rate >= 0.5
        ) THEN
            v_streak := v_streak + 1;
            v_check_date := v_check_date - INTERVAL '1 day';
        ELSE
            EXIT;
        END IF;
    END LOOP;
    
    RETURN v_streak;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 11. SEED DATA
-- ============================================

-- Insert default alert rules
INSERT INTO alert_rules (rule_name, description, trigger_condition, alert_level, alert_content, is_active) VALUES
('连续懈怠-温和提醒', '连续3天未学习', '{"type": "consecutive_days", "value": 3}', 'gentle', 
 'Edward，已经3天没看到你的学习了。没关系，每个人都有状态不好的时候。今天只做一个动作：打开飞书，看一眼今日推送。就这一个动作，够了。', TRUE),
('连续懈怠-严肃警告', '连续5天未学习', '{"type": "consecutive_days", "value": 5}', 'serious',
 'Edward，5天了。你的大学梦想不会等你。39岁到49岁这10年，决定了你是普通人还是传奇。今天必须做一个选择：继续还是放弃？如果继续，回复"重启"，我们重新开始。', TRUE),
('连续懈怠-重启日', '连续7天未学习', '{"type": "consecutive_days", "value": 7}', 'reset',
 'Edward，7天没学习。现在是重启日。今天只做一件事：重新读一遍你的大学梦想清单。然后回复我：我还要继续吗？', TRUE),
('完成率低-调整目标', '周完成率<50%', '{"type": "weekly_completion", "operator": "<", "value": 0.5}', 'gentle',
 'Edward，这周完成率不到50%。没关系，我们调整一下。下周目标减半，先建立信心。记住：完美是执行的敌人。', TRUE),
('完成率高-提高挑战', '周完成率>80%', '{"type": "weekly_completion", "operator": ">", "value": 0.8}', 'gentle',
 'Edward，这周完成率超过80%！太棒了！下周我们提高挑战，增加20%的学习量。你正在成为那个你梦想成为的人。', TRUE);

-- ============================================
-- 12. COMMENTS
-- ============================================

COMMENT ON TABLE users IS '用户基础信息表';
COMMENT ON TABLE user_profiles IS '用户画像表（包含MASK/马斯洛/7个习惯评分）';
COMMENT ON TABLE learning_content IS '学习内容库';
COMMENT ON TABLE learning_records IS '学习记录表';
COMMENT ON TABLE daily_checkins IS '每日打卡表';
COMMENT ON TABLE quick_captures IS '快速录入表（语音/文字）';
COMMENT ON TABLE knowledge_base IS '知识库表';
COMMENT ON TABLE goals IS '目标表（SMART原则）';
COMMENT ON TABLE habit_tracking IS '习惯追踪表';
COMMENT ON TABLE habit_logs IS '习惯打卡记录表';
COMMENT ON TABLE alert_rules IS '预警规则表';
COMMENT ON TABLE alert_logs IS '预警日志表';

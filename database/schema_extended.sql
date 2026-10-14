-- Edward Growth System - Extended Database Schema for Knowledge & Speech
-- PostgreSQL 14+
-- This extends the base schema with knowledge capture, speech generation, and application tracking

-- ============================================
-- 3. KNOWLEDGE CAPTURE & INSIGHTS
-- ============================================

-- Knowledge insights table (raw captured insights)
CREATE TABLE knowledge_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Content
    content TEXT NOT NULL,  -- Original insight content
    
    -- Classification
    domain VARCHAR(50),  -- AI/marketing/chinese_classics/english/speaking/general
    intent VARCHAR(50),  -- idea/question/note/task/reflection/insight
    
    -- NLP extracted data
    key_points JSONB,  -- Array of key points
    entities JSONB,  -- Extracted entities (concepts, keywords, examples)
    connections JSONB,  -- Related concepts/knowledge
    
    -- Metadata
    tags JSONB DEFAULT '[]'::jsonb,  -- User or auto-generated tags
    source VARCHAR(50),  -- voice/text/manual
    language VARCHAR(10) DEFAULT 'zh',  -- zh/en
    
    -- Status
    status VARCHAR(50) DEFAULT 'raw',  -- raw → structured → crystallized → shared
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_knowledge_insights_user_id ON knowledge_insights(user_id);
CREATE INDEX idx_knowledge_insights_domain ON knowledge_insights(domain);
CREATE INDEX idx_knowledge_insights_status ON knowledge_insights(status);
CREATE INDEX idx_knowledge_insights_created_at ON knowledge_insights(created_at DESC);
CREATE INDEX idx_knowledge_insights_content_gin ON knowledge_insights USING GIN(to_tsvector('chinese', content));

-- Structured knowledge table (processed and organized knowledge units)
CREATE TABLE structured_knowledge (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    insight_id UUID REFERENCES knowledge_insights(id) ON DELETE CASCADE,
    
    -- Core information
    title VARCHAR(500) NOT NULL,
    domain VARCHAR(50) NOT NULL,
    core_concept VARCHAR(200),  -- Main concept/idea
    
    -- Content
    explanation TEXT,  -- Detailed explanation in own words
    examples JSONB,  -- Array of examples
    applications JSONB,  -- Practical application scenarios
    connections JSONB,  -- Related concepts
    
    -- Assessment
    difficulty INTEGER CHECK (difficulty BETWEEN 1 AND 5),  -- 1=easy, 5=hard
    importance INTEGER CHECK (importance BETWEEN 1 AND 5),  -- 1=low, 5=critical
    mastery_level DECIMAL(3,2) DEFAULT 0.50 CHECK (mastery_level BETWEEN 0 AND 1),  -- 0-1
    
    -- Review tracking
    last_reviewed TIMESTAMP WITH TIME ZONE,
    review_count INTEGER DEFAULT 1,
    next_review_date DATE,  -- For spaced repetition
    
    -- Status
    status VARCHAR(50) DEFAULT 'structured',  -- structured → reviewed → mastered
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_structured_knowledge_insight_id ON structured_knowledge(insight_id);
CREATE INDEX idx_structured_knowledge_domain ON structured_knowledge(domain);
CREATE INDEX idx_structured_knowledge_mastery ON structured_knowledge(mastery_level);
CREATE INDEX idx_structured_knowledge_next_review ON structured_knowledge(next_review_date);

-- ============================================
-- 4. KNOWLEDGE GRAPH
-- ============================================

-- Knowledge graph nodes
CREATE TABLE knowledge_graph_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Node information
    domain VARCHAR(50) NOT NULL,
    concept VARCHAR(200) NOT NULL,
    title VARCHAR(500),
    
    -- Metrics
    mastery_level DECIMAL(3,2) DEFAULT 0.50 CHECK (mastery_level BETWEEN 0 AND 1),
    centrality_score DECIMAL(5,4),  -- Graph centrality (importance in network)
    connection_count INTEGER DEFAULT 0,  -- Number of edges
    
    -- Metadata
    structured_knowledge_id UUID REFERENCES structured_knowledge(id),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_knowledge_graph_nodes_user_domain ON knowledge_graph_nodes(user_id, domain);
CREATE INDEX idx_knowledge_graph_nodes_concept ON knowledge_graph_nodes(concept);
CREATE INDEX idx_knowledge_graph_nodes_centrality ON knowledge_graph_nodes(centrality_score DESC);

-- Knowledge graph edges (relationships between nodes)
CREATE TABLE knowledge_graph_edges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Edge endpoints
    source_id UUID REFERENCES knowledge_graph_nodes(id) ON DELETE CASCADE,
    target_id UUID REFERENCES knowledge_graph_nodes(id) ON DELETE CASCADE,
    
    -- Edge properties
    edge_type VARCHAR(50),  -- related_to/prerequisite/part_of/causes/conflicts_with
    strength DECIMAL(3,2) DEFAULT 0.80 CHECK (strength BETWEEN 0 AND 1),
    bidirectional BOOLEAN DEFAULT false,
    
    -- Metadata
    description TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_knowledge_graph_edges_source ON knowledge_graph_edges(source_id);
CREATE INDEX idx_knowledge_graph_edges_target ON knowledge_graph_edges(target_id);
CREATE INDEX idx_knowledge_graph_edges_type ON knowledge_graph_edges(edge_type);

-- Ensure no duplicate edges
CREATE UNIQUE INDEX idx_knowledge_graph_edges_unique 
ON knowledge_graph_edges(source_id, target_id, edge_type);

-- ============================================
-- 5. REVIEW SYSTEM
-- ============================================

-- Review sessions table
CREATE TABLE review_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Session metadata
    review_type VARCHAR(50) NOT NULL,  -- daily/weekly/monthly/quarterly
    scheduled_time TIMESTAMP WITH TIME ZONE,
    completed_time TIMESTAMP WITH TIME ZONE,
    
    -- Content
    insights_json JSONB,  -- Insights covered in this review
    questions_json JSONB,  -- Review questions asked
    responses TEXT,  -- User's responses (can be long text)
    
    -- Analysis
    summary TEXT,  -- AI-generated summary
    new_insights_json JSONB,  -- New insights extracted from responses
    mastery_updates JSONB,  -- Mastery level changes
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending',  -- pending → in_progress → completed
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_review_sessions_user_id ON review_sessions(user_id);
CREATE INDEX idx_review_sessions_type ON review_sessions(review_type);
CREATE INDEX idx_review_sessions_scheduled ON review_sessions(scheduled_time);
CREATE INDEX idx_review_sessions_status ON review_sessions(status);

-- Review summaries (aggregated insights from reviews)
CREATE TABLE review_summaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID REFERENCES review_sessions(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Summary content
    summary TEXT NOT NULL,
    key_learnings JSONB,  -- Top 3-5 learnings
    action_items JSONB,  -- Action items for next period
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_review_summaries_session_id ON review_summaries(session_id);
CREATE INDEX idx_review_summaries_user_id ON review_summaries(user_id);

-- ============================================
-- 6. SPEECH GENERATION
-- ============================================

-- Speech drafts table
CREATE TABLE speech_drafts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Speech metadata
    topic VARCHAR(500) NOT NULL,
    template_type VARCHAR(50),  -- ted_talk/toastmasters/elevator_pitch/storytelling
    estimated_duration INTEGER,  -- Minutes
    
    -- Content
    draft_json JSONB,  -- Section-by-section draft
    full_speech TEXT,  -- Complete speech text
    speaker_notes TEXT,  -- Speaker notes and cues
    
    -- Related content
    related_insights JSONB,  -- Insight IDs used in this speech
    related_knowledge JSONB,  -- Structured knowledge IDs
    
    -- Status
    status VARCHAR(50) DEFAULT 'draft',  -- draft → reviewed → finalized → delivered
    
    -- Feedback
    feedback_score DECIMAL(3,2),  -- 0-5 rating from audience
    feedback_comments TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    delivered_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_speech_drafts_user_id ON speech_drafts(user_id);
CREATE INDEX idx_speech_drafts_topic ON speech_drafts(topic);
CREATE INDEX idx_speech_drafts_template ON speech_drafts(template_type);
CREATE INDEX idx_speech_drafts_status ON speech_drafts(status);

-- Bilingual speeches table
CREATE TABLE bilingual_speeches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    speech_draft_id UUID REFERENCES speech_drafts(id) ON DELETE CASCADE,
    
    -- Language settings
    primary_language VARCHAR(10) DEFAULT 'zh',
    secondary_language VARCHAR(10) DEFAULT 'en',
    
    -- Bilingual content
    bilingual_version JSONB,  -- Section-by-section bilingual content
    switching_cues JSONB,  -- Language switching hints
    
    -- Quality metrics
    translation_quality DECIMAL(3,2),  -- 0-5 rating
    naturalness_score DECIMAL(3,2),  -- How natural the English sounds
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bilingual_speeches_user_id ON bilingual_speeches(user_id);
CREATE INDEX idx_bilingual_speeches_draft_id ON bilingual_speeches(speech_draft_id);

-- Speech materials library (reusable stories, quotes, cases)
CREATE TABLE speech_materials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Material metadata
    material_type VARCHAR(50),  -- story/quote/case/data_point/analogy
    title VARCHAR(500),
    content TEXT NOT NULL,
    
    -- Classification
    domain VARCHAR(50),
    tags JSONB DEFAULT '[]'::jsonb,
    
    -- Usage tracking
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,
    effectiveness_score DECIMAL(3,2),  -- 0-5 based on feedback
    
    -- Source
    source VARCHAR(200),  -- Where this material came from
    source_url TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_speech_materials_user_id ON speech_materials(user_id);
CREATE INDEX idx_speech_materials_type ON speech_materials(material_type);
CREATE INDEX idx_speech_materials_domain ON speech_materials(domain);
CREATE INDEX idx_speech_materials_usage ON speech_materials(usage_count DESC);

-- ============================================
-- 7. APPLICATION TRACKING
-- ============================================

-- Knowledge applications table (tracking real-world usage)
CREATE TABLE knowledge_applications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    knowledge_id UUID REFERENCES structured_knowledge(id) ON DELETE CASCADE,
    
    -- Application details
    scenario TEXT NOT NULL,  -- Description of where/how applied
    outcome TEXT,  -- Result/outcome
    lessons_learned TEXT,  -- What was learned from this application
    
    -- Assessment
    effectiveness DECIMAL(3,2) CHECK (effectiveness BETWEEN 0 AND 5),  -- 0-5 rating
    confidence_level DECIMAL(3,2) CHECK (confidence_level BETWEEN 0 AND 1),  -- 0-1
    
    -- Context
    context_tags JSONB DEFAULT '[]'::jsonb,  -- work/personal/leadership/strategy etc.
    stakeholders TEXT[],  -- People involved
    
    -- Follow-up
    follow_up_needed BOOLEAN DEFAULT false,
    follow_up_notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_knowledge_applications_user_id ON knowledge_applications(user_id);
CREATE INDEX idx_knowledge_applications_knowledge_id ON knowledge_applications(knowledge_id);
CREATE INDEX idx_knowledge_applications_effectiveness ON knowledge_applications(effectiveness DESC);
CREATE INDEX idx_knowledge_applications_created ON knowledge_applications(created_at DESC);

-- Application statistics (aggregated metrics)
CREATE TABLE application_stats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) UNIQUE,
    
    -- Overall stats
    total_applications INTEGER DEFAULT 0,
    successful_applications INTEGER DEFAULT 0,
    success_rate DECIMAL(5,4) DEFAULT 0.0000,
    
    -- By domain
    applications_by_domain JSONB DEFAULT '{
        "AI": 0,
        "marketing": 0,
        "chinese_classics": 0,
        "english": 0,
        "speaking": 0
    }'::jsonb,
    
    -- Recent activity
    last_application_date DATE,
    applications_last_30_days INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_application_stats_user_id ON application_stats(user_id);

-- ============================================
-- 8. LEARNING CONTENT EXTENSIONS
-- ============================================

-- Extend learning_content table with additional fields
ALTER TABLE learning_content ADD COLUMN IF NOT EXISTS mask_dimension VARCHAR(50);
ALTER TABLE learning_content ADD COLUMN IF NOT EXISTS maslow_level VARCHAR(50);
ALTER TABLE learning_content ADD COLUMN IF NOT EXISTS chinese_classic VARCHAR(100);  -- For classics like 道德经/金刚经
ALTER TABLE learning_content ADD COLUMN IF NOT EXISTS classic_chapter VARCHAR(50);  -- Chapter number/name

CREATE INDEX idx_learning_content_mask ON learning_content(mask_dimension);
CREATE INDEX idx_learning_content_maslow ON learning_content(maslow_level);
CREATE INDEX idx_learning_content_classic ON learning_content(chinese_classic);

-- ============================================
-- 9. CHINESE CLASSICS LEARNING
-- ============================================

-- Chinese classics reading progress
CREATE TABLE chinese_classics_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    
    -- Classic identification
    classic_name VARCHAR(100) NOT NULL,  -- 道德经/金刚经/坛经/资治通鉴/易经/孙子兵法
    chapter_number INTEGER,  -- Chapter/section number
    chapter_name VARCHAR(200),  -- Chapter name if applicable
    
    -- Progress tracking
    original_text TEXT,  -- Original classical text
    translation TEXT,  -- Modern Chinese translation
    interpretation TEXT,  -- Personal interpretation/notes
    
    -- Learning status
    status VARCHAR(50) DEFAULT 'not_started',  -- not_started → reading → completed → reviewed
    completion_date DATE,
    mastery_level DECIMAL(3,2) DEFAULT 0.00 CHECK (mastery_level BETWEEN 0 AND 1),
    
    -- Review tracking
    review_count INTEGER DEFAULT 0,
    last_review_date DATE,
    next_review_date DATE,  -- For spaced repetition
    
    -- Applications
    modern_applications JSONB,  -- How this applies to modern life/work
    
    -- Timestamps
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_chinese_classics_progress_user ON chinese_classics_progress(user_id);
CREATE INDEX idx_chinese_classics_progress_classic ON chinese_classics_progress(classic_name);
CREATE INDEX idx_chinese_classics_progress_status ON chinese_classics_progress(status);
CREATE INDEX idx_chinese_classics_progress_mastery ON chinese_classics_progress(mastery_level DESC);

-- Ensure unique progress per user per chapter
CREATE UNIQUE INDEX idx_chinese_classics_unique_progress 
ON chinese_classics_progress(user_id, classic_name, chapter_number);

-- ============================================
-- 10. FUNCTIONS & TRIGGERS
-- ============================================

-- Function to update structured knowledge mastery when application is logged
CREATE OR REPLACE FUNCTION update_mastery_from_application()
RETURNS TRIGGER AS $$
BEGIN
    -- Increase mastery level based on successful application
    UPDATE structured_knowledge
    SET 
        mastery_level = LEAST(1.0, mastery_level + 0.05 * NEW.effectiveness / 5.0),
        last_reviewed = NOW(),
        review_count = review_count + 1,
        updated_at = NOW()
    WHERE id = NEW.knowledge_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the function
CREATE TRIGGER trg_update_mastery_on_application
AFTER INSERT ON knowledge_applications
FOR EACH ROW
EXECUTE FUNCTION update_mastery_from_application();

-- Function to update application stats
CREATE OR REPLACE FUNCTION update_application_stats()
RETURNS TRIGGER AS $$
DECLARE
    app_domain VARCHAR(50);
BEGIN
    -- Get domain from structured_knowledge
    SELECT domain INTO app_domain FROM structured_knowledge WHERE id = NEW.knowledge_id;
    
    -- Update or create stats record
    INSERT INTO application_stats (user_id, total_applications, successful_applications, applications_by_domain, last_application_date, applications_last_30_days)
    VALUES (
        NEW.user_id,
        1,
        CASE WHEN NEW.effectiveness >= 3 THEN 1 ELSE 0 END,
        jsonb_build_object(app_domain, 1),
        CURRENT_DATE,
        1
    )
    ON CONFLICT (user_id) DO UPDATE SET
        total_applications = application_stats.total_applications + 1,
        successful_applications = application_stats.successful_applications + CASE WHEN NEW.effectiveness >= 3 THEN 1 ELSE 0 END,
        applications_by_domain = jsonb_set(
            application_stats.applications_by_domain,
            ARRAY[app_domain],
            COALESCE((application_stats.applications_by_domain->>app_domain)::int, 0)::text::jsonb + 1
        ),
        last_application_date = CURRENT_DATE,
        applications_last_30_days = application_stats.applications_last_30_days + 1,
        updated_at = NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update stats
CREATE TRIGGER trg_update_application_stats
AFTER INSERT ON knowledge_applications
FOR EACH ROW
EXECUTE FUNCTION update_application_stats();

-- Function to calculate success rate
CREATE OR REPLACE FUNCTION calculate_success_rate()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE application_stats
    SET 
        success_rate = CASE 
            WHEN total_applications > 0 THEN successful_applications::DECIMAL / total_applications
            ELSE 0
        END,
        updated_at = NOW()
    WHERE user_id = NEW.user_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to recalculate success rate
CREATE TRIGGER trg_calculate_success_rate
AFTER INSERT OR UPDATE ON application_stats
FOR EACH ROW
EXECUTE FUNCTION calculate_success_rate();

-- ============================================
-- 11. VIEWS FOR ANALYTICS
-- ============================================

-- View: User knowledge dashboard
CREATE OR REPLACE VIEW user_knowledge_dashboard AS
SELECT 
    u.user_id,
    u.name,
    COUNT(DISTINCT ki.id) AS total_insights,
    COUNT(DISTINCT sk.id) AS structured_knowledge_count,
    AVG(sk.mastery_level) AS avg_mastery_level,
    COUNT(DISTINCT kgn.id) AS knowledge_graph_nodes,
    COUNT(DISTINCT ka.id) AS total_applications,
    ast.success_rate,
    COUNT(DISTINCT sd.id) AS speech_drafts_count,
    MAX(sd.created_at) AS last_speech_date
FROM users u
LEFT JOIN knowledge_insights ki ON u.user_id = ki.user_id
LEFT JOIN structured_knowledge sk ON ki.id = sk.insight_id
LEFT JOIN knowledge_graph_nodes kgn ON sk.id = kgn.structured_knowledge_id
LEFT JOIN knowledge_applications ka ON sk.id = ka.knowledge_id
LEFT JOIN application_stats ast ON u.user_id = ast.user_id
LEFT JOIN speech_drafts sd ON u.user_id = sd.user_id
GROUP BY u.user_id, u.name, ast.success_rate;

-- View: Domain knowledge completion
CREATE OR REPLACE VIEW domain_knowledge_completion AS
SELECT 
    user_id,
    domain,
    COUNT(*) AS knowledge_count,
    AVG(mastery_level) AS avg_mastery,
    MAX(mastery_level) AS max_mastery,
    MIN(mastery_level) AS min_mastery,
    COUNT(CASE WHEN mastery_level >= 0.8 THEN 1 END) AS mastered_count,
    COUNT(CASE WHEN mastery_level < 0.5 THEN 1 END) AS needs_review_count
FROM structured_knowledge
GROUP BY user_id, domain;

-- View: Recent learning activity
CREATE OR REPLACE VIEW recent_learning_activity AS
SELECT 
    u.user_id,
    u.name,
    ki.content AS insight_content,
    ki.domain,
    ki.created_at AS insight_date,
    sk.title AS knowledge_title,
    sk.mastery_level,
    ka.scenario AS application_scenario,
    ka.effectiveness,
    ka.created_at AS application_date
FROM users u
LEFT JOIN knowledge_insights ki ON u.user_id = ki.user_id
LEFT JOIN structured_knowledge sk ON ki.id = sk.insight_id
LEFT JOIN knowledge_applications ka ON sk.id = ka.knowledge_id
WHERE ki.created_at >= NOW() - INTERVAL '30 days'
ORDER BY ki.created_at DESC;

-- ============================================
-- 12. SEED DATA (Optional)
-- ============================================

-- Insert default speech templates metadata
INSERT INTO speech_materials (material_type, title, content, domain, tags, source) VALUES
('template', 'TED Talk Opening Hook', 'Start with a shocking fact, personal story, or provocative question...', 'speaking', '["opening", "hook", "TED"]', 'System'),
('template', 'Toastmasters Structure', 'Introduction → Point 1 → Point 2 → Point 3 → Conclusion...', 'speaking', '["structure", "Toastmasters"]', 'System'),
('template', 'Story Arc Template', 'Ordinary World → Call to Adventure → Challenge → Resolution...', 'speaking', '["storytelling", "hero journey"]', 'System');

-- Insert default Chinese classics structure
INSERT INTO chinese_classics_progress (user_id, classic_name, chapter_number, chapter_name, status)
SELECT 
    u.user_id,
    c.classic_name,
    c.chapter_number,
    c.chapter_name,
    'not_started'
FROM users u
CROSS JOIN (
    -- Tao Te Ching: 81 chapters
    SELECT '道德经' AS classic_name, generate_series(1, 81) AS chapter_number, 
           '第' || generate_series(1, 81) || '章' AS chapter_name
    UNION ALL
    -- Diamond Sutra: 32 sections
    SELECT '金刚经', generate_series(1, 32), '第' || generate_series(1, 32) || '品'
    UNION ALL
    -- Platform Sutra: 10 sections
    SELECT '六祖坛经', generate_series(1, 10), '第' || generate_series(1, 10) || '品'
    UNION ALL
    -- I Ching: 64 hexagrams
    SELECT '易经', generate_series(1, 64), '第' || generate_series(1, 64) || '卦'
    UNION ALL
    -- Art of War: 13 chapters
    SELECT '孙子兵法', generate_series(1, 13), '第' || generate_series(1, 13) || '篇'
) c
WHERE NOT EXISTS (
    SELECT 1 FROM chinese_classics_progress ccp 
    WHERE ccp.user_id = u.user_id AND ccp.classic_name = c.classic_name AND ccp.chapter_number = c.chapter_number
);

COMMENT ON TABLE knowledge_insights IS 'Raw captured insights from user (voice/text input)';
COMMENT ON TABLE structured_knowledge IS 'Processed and organized knowledge units with mastery tracking';
COMMENT ON TABLE knowledge_graph_nodes IS 'Nodes in the knowledge graph representing concepts';
COMMENT ON TABLE knowledge_graph_edges IS 'Relationships between knowledge concepts';
COMMENT ON TABLE review_sessions IS 'Scheduled review sessions (daily/weekly/monthly/quarterly)';
COMMENT ON TABLE speech_drafts IS 'Generated speech drafts using international templates';
COMMENT ON TABLE bilingual_speeches IS 'Bilingual (Chinese-English) speech versions';
COMMENT ON TABLE speech_materials IS 'Reusable speech materials (stories, quotes, cases)';
COMMENT ON TABLE knowledge_applications IS 'Real-world applications of learned knowledge';
COMMENT ON TABLE application_stats IS 'Aggregated statistics on knowledge applications';
COMMENT ON TABLE chinese_classics_progress IS 'Progress tracking for Chinese classics reading';

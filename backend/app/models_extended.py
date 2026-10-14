"""
Extended SQLAlchemy Models for Edward Growth System
Supports: Knowledge Capture, Speech Generation, Application Tracking, Chinese Classics
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Date, Float, Text, ForeignKey, Index, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB
from sqlalchemy.sql import func
from app.database import Base
import uuid
from datetime import date


# ============================================
# KNOWLEDGE CAPTURE & INSIGHTS
# ============================================

class KnowledgeInsight(Base):
    """Raw captured insights from user (voice/text input)"""
    __tablename__ = "knowledge_insights"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Content
    content = Column(Text, nullable=False)
    
    # Classification
    domain = Column(String(50))  # AI/marketing/chinese_classics/english/speaking/general
    intent = Column(String(50))  # idea/question/note/task/reflection/insight
    
    # NLP extracted data
    key_points = Column(PG_JSONB)
    entities = Column(PG_JSONB)
    connections = Column(PG_JSONB)
    
    # Metadata
    tags = Column(PG_JSONB, default=[])
    source = Column(String(50))  # voice/text/manual
    language = Column(String(10), default='zh')
    
    # Status
    status = Column(String(50), default='raw')  # raw → structured → crystallized → shared
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_knowledge_insights_user_domain', 'user_id', 'domain'),
        Index('idx_knowledge_insights_status', 'status'),
    )


class StructuredKnowledge(Base):
    """Processed and organized knowledge units with mastery tracking"""
    __tablename__ = "structured_knowledge"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    insight_id = Column(PG_UUID(as_uuid=True), ForeignKey("knowledge_insights.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Core information
    title = Column(String(500), nullable=False)
    domain = Column(String(50), nullable=False)
    core_concept = Column(String(200))
    
    # Content
    explanation = Column(Text)
    examples = Column(PG_JSONB)
    applications = Column(PG_JSONB)
    connections = Column(PG_JSONB)
    
    # Assessment
    difficulty = Column(Integer, CheckConstraint('difficulty BETWEEN 1 AND 5'))
    importance = Column(Integer, CheckConstraint('importance BETWEEN 1 AND 5'))
    mastery_level = Column(Float, CheckConstraint('mastery_level BETWEEN 0 AND 1'), default=0.50)
    
    # Review tracking
    last_reviewed = Column(DateTime(timezone=True))
    review_count = Column(Integer, default=1)
    next_review_date = Column(Date)
    
    # Status
    status = Column(String(50), default='structured')  # structured → reviewed → mastered
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_structured_knowledge_domain', 'domain'),
        Index('idx_structured_knowledge_mastery', 'mastery_level'),
        Index('idx_structured_knowledge_next_review', 'next_review_date'),
    )


# ============================================
# KNOWLEDGE GRAPH
# ============================================

class KnowledgeGraphNode(Base):
    """Nodes in the knowledge graph representing concepts"""
    __tablename__ = "knowledge_graph_nodes"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Node information
    domain = Column(String(50), nullable=False)
    concept = Column(String(200), nullable=False)
    title = Column(String(500))
    
    # Metrics
    mastery_level = Column(Float, CheckConstraint('mastery_level BETWEEN 0 AND 1'), default=0.50)
    centrality_score = Column(Float)
    connection_count = Column(Integer, default=0)
    
    # Metadata
    structured_knowledge_id = Column(PG_UUID(as_uuid=True), ForeignKey("structured_knowledge.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_knowledge_graph_nodes_user_domain', 'user_id', 'domain'),
        Index('idx_knowledge_graph_nodes_centrality', 'centrality_score'),
    )


class KnowledgeGraphEdge(Base):
    """Relationships between knowledge concepts"""
    __tablename__ = "knowledge_graph_edges"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Edge endpoints
    source_id = Column(PG_UUID(as_uuid=True), ForeignKey("knowledge_graph_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    target_id = Column(PG_UUID(as_uuid=True), ForeignKey("knowledge_graph_nodes.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Edge properties
    edge_type = Column(String(50))  # related_to/prerequisite/part_of/causes/conflicts_with
    strength = Column(Float, CheckConstraint('strength BETWEEN 0 AND 1'), default=0.80)
    bidirectional = Column(Boolean, default=False)
    
    # Metadata
    description = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    __table_args__ = (
        Index('idx_knowledge_graph_edges_type', 'edge_type'),
        UniqueConstraint('source_id', 'target_id', 'edge_type', name='uq_edge_unique'),
    )


# ============================================
# REVIEW SYSTEM
# ============================================

class ReviewSession(Base):
    """Scheduled review sessions (daily/weekly/monthly/quarterly)"""
    __tablename__ = "review_sessions"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Session metadata
    review_type = Column(String(50), nullable=False)  # daily/weekly/monthly/quarterly
    scheduled_time = Column(DateTime(timezone=True))
    completed_time = Column(DateTime(timezone=True))
    
    # Content
    insights_json = Column(PG_JSONB)
    questions_json = Column(PG_JSONB)
    responses = Column(Text)
    
    # Analysis
    summary = Column(Text)
    new_insights_json = Column(PG_JSONB)
    mastery_updates = Column(PG_JSONB)
    
    # Status
    status = Column(String(50), default='pending')  # pending → in_progress → completed
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_review_sessions_type', 'review_type'),
        Index('idx_review_sessions_scheduled', 'scheduled_time'),
        Index('idx_review_sessions_status', 'status'),
    )


class ReviewSummary(Base):
    """Aggregated insights from reviews"""
    __tablename__ = "review_summaries"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(PG_UUID(as_uuid=True), ForeignKey("review_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Summary content
    summary = Column(Text, nullable=False)
    key_learnings = Column(PG_JSONB)
    action_items = Column(PG_JSONB)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================
# SPEECH GENERATION
# ============================================

class SpeechDraft(Base):
    """Generated speech drafts using international templates"""
    __tablename__ = "speech_drafts"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Speech metadata
    topic = Column(String(500), nullable=False)
    template_type = Column(String(50))  # ted_talk/toastmasters/elevator_pitch/storytelling
    estimated_duration = Column(Integer)
    
    # Content
    draft_json = Column(PG_JSONB)
    full_speech = Column(Text)
    speaker_notes = Column(Text)
    
    # Related content
    related_insights = Column(PG_JSONB)
    related_knowledge = Column(PG_JSONB)
    
    # Status
    status = Column(String(50), default='draft')  # draft → reviewed → finalized → delivered
    
    # Feedback
    feedback_score = Column(Float)
    feedback_comments = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    delivered_at = Column(DateTime(timezone=True))
    
    __table_args__ = (
        Index('idx_speech_drafts_topic', 'topic'),
        Index('idx_speech_drafts_template', 'template_type'),
        Index('idx_speech_drafts_status', 'status'),
    )


class BilingualSpeech(Base):
    """Bilingual (Chinese-English) speech versions"""
    __tablename__ = "bilingual_speeches"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    speech_draft_id = Column(PG_UUID(as_uuid=True), ForeignKey("speech_drafts.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Language settings
    primary_language = Column(String(10), default='zh')
    secondary_language = Column(String(10), default='en')
    
    # Bilingual content
    bilingual_version = Column(PG_JSONB)
    switching_cues = Column(PG_JSONB)
    
    # Quality metrics
    translation_quality = Column(Float)
    naturalness_score = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SpeechMaterial(Base):
    """Reusable speech materials (stories, quotes, cases)"""
    __tablename__ = "speech_materials"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Material metadata
    material_type = Column(String(50))  # story/quote/case/data_point/analogy
    title = Column(String(500))
    content = Column(Text, nullable=False)
    
    # Classification
    domain = Column(String(50))
    tags = Column(PG_JSONB, default=[])
    
    # Usage tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime(timezone=True))
    effectiveness_score = Column(Float)
    
    # Source
    source = Column(String(200))
    source_url = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_speech_materials_type', 'material_type'),
        Index('idx_speech_materials_domain', 'domain'),
        Index('idx_speech_materials_usage', 'usage_count'),
    )


# ============================================
# APPLICATION TRACKING
# ============================================

class KnowledgeApplication(Base):
    """Real-world applications of learned knowledge"""
    __tablename__ = "knowledge_applications"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    knowledge_id = Column(PG_UUID(as_uuid=True), ForeignKey("structured_knowledge.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Application details
    scenario = Column(Text, nullable=False)
    outcome = Column(Text)
    lessons_learned = Column(Text)
    
    # Assessment
    effectiveness = Column(Float, CheckConstraint('effectiveness BETWEEN 0 AND 5'))
    confidence_level = Column(Float, CheckConstraint('confidence_level BETWEEN 0 AND 1'))
    
    # Context
    context_tags = Column(PG_JSONB, default=[])
    stakeholders = Column(PG_JSONB)  # Array of people involved
    
    # Follow-up
    follow_up_needed = Column(Boolean, default=False)
    follow_up_notes = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_knowledge_applications_effectiveness', 'effectiveness'),
        Index('idx_knowledge_applications_created', 'created_at'),
    )


class ApplicationStats(Base):
    """Aggregated statistics on knowledge applications"""
    __tablename__ = "application_stats"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), unique=True, index=True)
    
    # Overall stats
    total_applications = Column(Integer, default=0)
    successful_applications = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    
    # By domain
    applications_by_domain = Column(PG_JSONB, default={
        "AI": 0,
        "marketing": 0,
        "chinese_classics": 0,
        "english": 0,
        "speaking": 0
    })
    
    # Recent activity
    last_application_date = Column(Date)
    applications_last_30_days = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ============================================
# CHINESE CLASSICS LEARNING
# ============================================

class ChineseClassicsProgress(Base):
    """Progress tracking for Chinese classics reading"""
    __tablename__ = "chinese_classics_progress"
    
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Classic identification
    classic_name = Column(String(100), nullable=False)  # 道德经/金刚经/坛经/资治通鉴/易经/孙子兵法
    chapter_number = Column(Integer)
    chapter_name = Column(String(200))
    
    # Progress tracking
    original_text = Column(Text)
    translation = Column(Text)
    interpretation = Column(Text)
    
    # Learning status
    status = Column(String(50), default='not_started')  # not_started → reading → completed → reviewed
    completion_date = Column(Date)
    mastery_level = Column(Float, CheckConstraint('mastery_level BETWEEN 0 AND 1'), default=0.0)
    
    # Review tracking
    review_count = Column(Integer, default=0)
    last_review_date = Column(Date)
    next_review_date = Column(Date)
    
    # Applications
    modern_applications = Column(PG_JSONB)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_chinese_classics_progress_classic', 'classic_name'),
        Index('idx_chinese_classics_progress_status', 'status'),
        Index('idx_chinese_classics_progress_mastery', 'mastery_level'),
        UniqueConstraint('user_id', 'classic_name', 'chapter_number', name='uq_classics_progress_unique'),
    )


# ============================================
# GAMIFICATION SYSTEM
# ============================================

class UserLevel(Base):
    """User level and XP tracking"""
    __tablename__ = "user_levels"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    current_level = Column(Integer, default=1)
    total_xp = Column(Integer, default=0)
    level_title = Column(String(50), default="成长新手")
    xp_to_next_level = Column(Integer, default=100)
    unlock_features = Column(PG_JSONB, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Achievement(Base):
    """Achievement definitions"""
    __tablename__ = "achievements"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    icon = Column(String(50))
    category = Column(String(50))  # learning/review/habit/social/special
    xp_reward = Column(Integer, default=0)
    unlock_condition = Column(PG_JSONB)  # {"type": "streak", "value": 7}
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UserAchievement(Base):
    """User's unlocked achievements"""
    __tablename__ = "user_achievements"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    achievement_id = Column(PG_UUID(as_uuid=True), ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False, index=True)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())
    progress_percent = Column(Integer, default=0)
    is_new = Column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),
    )


class DailyQuest(Base):
    """Daily quests for users"""
    __tablename__ = "daily_quests"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    quest_date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    quest_type = Column(String(50), nullable=False)  # main/side/challenge
    description = Column(String(200), nullable=False)
    xp_reward = Column(Integer, default=10)
    target_value = Column(Integer, default=1)
    current_value = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_daily_quest_user_date", "user_id", "quest_date"),
    )


class StreakRecord(Base):
    """Streak tracking for various activities"""
    __tablename__ = "streak_records"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    streak_type = Column(String(50), nullable=False)  # checkin/review/learning/habit
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_active_date = Column(String(10))  # YYYY-MM-DD
    streak_freeze_count = Column(Integer, default=2)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "streak_type", name="uq_user_streak_type"),
    )


# ============================================
# EBBINGHAUS REVIEW SYSTEM
# ============================================

class ReviewCard(Base):
    """Spaced repetition review cards"""
    __tablename__ = "review_cards"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    knowledge_id = Column(PG_UUID(as_uuid=True), ForeignKey("structured_knowledge.id", ondelete="CASCADE"), nullable=False, index=True)
    card_type = Column(String(50), nullable=False)  # concept/application/connection/reflection/challenge
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    difficulty = Column(Integer, default=3)  # 1-5

    # SM-2 Algorithm parameters
    ease_factor = Column(Float, default=2.5)
    interval_days = Column(Integer, default=1)
    next_review_date = Column(String(10), index=True)  # YYYY-MM-DD
    review_count = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    last_quality_score = Column(Integer, default=0)  # 0-5

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_review_card_user_next", "user_id", "next_review_date"),
    )


# ============================================
# SOCIAL SHARING SYSTEM
# ============================================

class ShareRecord(Base):
    """Social sharing records"""
    __tablename__ = "share_records"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    share_type = Column(String(50), nullable=False)  # level_up/achievement/streak/daily_report/weekly_report
    share_content = Column(PG_JSONB)  # {"title": "...", "stats": {...}, "image_url": "..."}
    platform = Column(String(50))  # wechat_moments/wechat_group/friends
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    click_count = Column(Integer, default=0)
    new_user_count = Column(Integer, default=0)


class InviteCode(Base):
    """User invite codes for referral"""
    __tablename__ = "invite_codes"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), nullable=False, unique=True, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    used_by = Column(PG_JSONB, default=list)  # List of user_ids who used this code
    total_invites = Column(Integer, default=0)
    xp_earned = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ============================================
# EXPORT ALL MODELS
# ============================================

__all__ = [
    # Knowledge Capture
    "KnowledgeInsight",
    "StructuredKnowledge",

    # Knowledge Graph
    "KnowledgeGraphNode",
    "KnowledgeGraphEdge",

    # Review System
    "ReviewSession",
    "ReviewSummary",

    # Speech Generation
    "SpeechDraft",
    "BilingualSpeech",
    "SpeechMaterial",

    # Application Tracking
    "KnowledgeApplication",
    "ApplicationStats",

    # Chinese Classics
    "ChineseClassicsProgress",

    # Gamification
    "UserLevel",
    "Achievement",
    "UserAchievement",
    "DailyQuest",
    "StreakRecord",

    # Ebbinghaus Review
    "ReviewCard",

    # Social Sharing
    "ShareRecord",
    "InviteCode",
]

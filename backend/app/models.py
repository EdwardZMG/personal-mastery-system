from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, Text, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB
from sqlalchemy.sql import func
from app.database import Base
import uuid


class User(Base):
    __tablename__ = "users"

    user_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    open_id = Column(String(100), unique=True, nullable=False, index=True)
    union_id = Column(String(100), unique=True)
    name = Column(String(100))
    avatar_url = Column(String(500))
    email = Column(String(200))
    phone = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), unique=True)
    bio = Column(Text)
    expertise_levels = Column(PG_JSONB, default={"AI": 0, "marketing": 0, "chinese_classics": 0, "english": 0, "speaking": 0})
    learning_preferences = Column(PG_JSONB, default={"preferred_time": "morning", "difficulty": "medium"})
    maslow_scores = Column(PG_JSONB, default={"physiological": 0, "safety": 0, "belonging": 0, "esteem": 0, "self_actualization": 0})
    mask_scores = Column(PG_JSONB, default={"mindset": 0, "attitude": 0, "skills": 0, "knowledge": 0})
    physical_scores = Column(PG_JSONB, default={"energy": 0, "fitness": 0, "sleep_quality": 0, "exercise_frequency": 0})
    seven_habits_scores = Column(PG_JSONB, default={"habit_1": 0, "habit_2": 0, "habit_3": 0, "habit_4": 0, "habit_5": 0, "habit_6": 0, "habit_7": 0})
    current_level = Column(String(50), default="beginner")
    # Gamification fields
    total_xp = Column(Integer, default=0)
    gamification_level = Column(Integer, default=1)
    level_title = Column(String(50), default="成长新手")
    streak_days = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    freeze_tokens = Column(Integer, default=2)
    invite_code = Column(String(20), unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class LearningContent(Base):
    __tablename__ = "learning_content"

    content_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    content_type = Column(String(50), nullable=False)  # article, video, audio, book, podcast
    category = Column(String(100), nullable=False)  # AI, marketing, chinese_classics, english, speaking, health
    difficulty_level = Column(Integer, default=1)  # 1-5
    estimated_minutes = Column(Integer, default=15)
    source_url = Column(String(1000))
    tags = Column(PG_JSONB, default=[])
    mask_dimension = Column(String(50))  # mindset, attitude, skills, knowledge
    maslow_level = Column(String(50))  # physiological, safety, belonging, esteem, self_actualization
    # Gamification fields
    dimension = Column(String(50))  # brain/heart/voice/body/grit/social
    sub_category = Column(String(100))  # AI/classics/english/leadership/etc.
    xp_reward = Column(Integer, default=10)
    prerequisite_ids = Column(PG_JSONB, default=[])  # List of prerequisite content IDs
    is_locked = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_content_category", "category"),
        Index("idx_content_difficulty", "difficulty_level"),
    )


class LearningRecord(Base):
    __tablename__ = "learning_records"

    record_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    content_id = Column(PG_UUID(as_uuid=True), ForeignKey("learning_content.content_id"), nullable=False, index=True)
    status = Column(String(50), default="pending")  # pending, in_progress, completed
    progress_percent = Column(Integer, default=0)
    duration_minutes = Column(Integer, default=0)
    feedback_score = Column(Integer)  # 1-5
    notes = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class DailyCheckin(Base):
    __tablename__ = "daily_checkins"

    checkin_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    checkin_date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    mood = Column(Integer)  # 1-5
    energy_level = Column(Integer)  # 1-5
    focus_areas = Column(PG_JSONB, default=[])
    reflections = Column(Text)
    achievements = Column(Text)
    challenges = Column(Text)
    tomorrow_plan = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        Index("idx_checkin_user_date", "user_id", "checkin_date", unique=True),
    )


class QuickCapture(Base):
    __tablename__ = "quick_captures"

    capture_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    capture_type = Column(String(50))  # idea, question, note, task
    category = Column(String(100))
    priority = Column(String(20), default="medium")  # low, medium, high
    status = Column(String(50), default="new")  # new, processed, archived
    processed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_capture_user_status", "user_id", "status"),
    )


class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    kb_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    category = Column(String(100))
    tags = Column(PG_JSONB, default=[])
    source = Column(String(200))
    importance = Column(Integer, default=3)  # 1-5
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Goal(Base):
    __tablename__ = "goals"

    goal_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    specific = Column(Text)
    measurable = Column(Text)
    achievable = Column(Text)
    relevant = Column(Text)
    time_bound = Column(String(50))
    start_date = Column(String(10))
    end_date = Column(String(10))
    progress_percent = Column(Integer, default=0)
    status = Column(String(50), default="active")  # active, completed, archived
    priority = Column(String(20), default="medium")
    intent_version = Column(Integer)
    evidence_rule = Column(Text)
    exit_conditions = Column(Text)
    version = Column(Integer, default=1, nullable=False)
    completion_confirmed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class HabitTracking(Base):
    __tablename__ = "habit_tracking"

    habit_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    category = Column(String(100))
    frequency = Column(String(50), default="daily")  # daily, weekly, monthly
    target_value = Column(Integer, default=1)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class HabitLog(Base):
    __tablename__ = "habit_logs"

    log_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    habit_id = Column(PG_UUID(as_uuid=True), ForeignKey("habit_tracking.habit_id"), nullable=False, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    log_date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    completed = Column(Boolean, default=False)
    actual_value = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_habit_log_user_date", "user_id", "log_date"),
    )


class AlertRule(Base):
    __tablename__ = "alert_rules"

    rule_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    rule_name = Column(String(200), nullable=False)
    trigger_type = Column(String(50), nullable=False)  # consecutive_miss, low_completion, milestone
    threshold = Column(Integer)
    alert_level = Column(String(20), default="gentle")  # gentle, serious, reset
    message_template = Column(Text)
    channels = Column(PG_JSONB, default=["feishu", "wechat"])
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AlertLog(Base):
    __tablename__ = "alert_logs"

    alert_id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rule_id = Column(PG_UUID(as_uuid=True), ForeignKey("alert_rules.rule_id"), nullable=False, index=True)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    triggered_at = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(Text)
    channel = Column(String(50))
    status = Column(String(50), default="sent")  # sent, failed

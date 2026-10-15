"""
V4 Models: Personal Mastery System
Personal Intent, Domains, Competencies, Practice, Evidence, Principles
"""
from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Date, Float, Text,
    ForeignKey, Index, CheckConstraint, UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB as PG_JSONB
from sqlalchemy.sql import func
from app.database import Base
import uuid


class PersonalIntentVersion(Base):
    __tablename__ = "personal_intent_versions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    raw_text = Column(Text)
    dreams = Column(PG_JSONB)
    roles = Column(PG_JSONB)
    values = Column(PG_JSONB)
    boundaries = Column(PG_JSONB)
    stage = Column(PG_JSONB)
    status = Column(String(20), default="draft", nullable=False)
    version = Column(Integer, default=1, nullable=False)
    effective_at = Column(DateTime(timezone=True))
    superseded_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("status IN ('draft','confirmed','superseded')", name="chk_intent_status"),
        Index("idx_intent_user_status", "user_id", "status"),
    )


class Domain(Base):
    __tablename__ = "domains"

    id = Column(String(50), primary_key=True)
    title = Column(String(100), nullable=False)
    direction = Column(Text)
    sample_artifacts = Column(PG_JSONB)
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id = Column(String(50), ForeignKey("domains.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    observable_outcome = Column(Text)
    difficulty_stage = Column(String(30))
    prerequisite_ids = Column(PG_JSONB)
    allowed_template_ids = Column(PG_JSONB)
    source_refs = Column(PG_JSONB)
    framework_tags = Column(PG_JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Framework(Base):
    __tablename__ = "frameworks"

    id = Column(String(50), primary_key=True)
    version = Column(String(20), default="v1", nullable=False)
    title = Column(String(200), nullable=False)
    evidence_kind = Column(String(50))
    fields = Column(PG_JSONB)
    limitations = Column(PG_JSONB)
    source_refs = Column(PG_JSONB)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(50), primary_key=True)
    title = Column(String(500), nullable=False)
    publisher = Column(String(200))
    url = Column(Text)
    published_at = Column(Date)
    retrieved_at = Column(DateTime(timezone=True))
    source_kind = Column(String(50))
    jurisdiction = Column(String(50))
    language = Column(String(10))
    supported_claims = Column(PG_JSONB)
    location_ref = Column(Text)
    verification_status = Column(String(20), default="unverified")
    content_hash = Column(String(64))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "verification_status IN ('unverified','verified','needs_update','deprecated')",
            name="chk_source_status",
        ),
    )


class PracticeTask(Base):
    __tablename__ = "practice_tasks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    domain_id = Column(String(50), ForeignKey("domains.id"))
    competency_id = Column(PG_UUID(as_uuid=True), ForeignKey("competencies.id"))
    goal_id = Column(PG_UUID(as_uuid=True), ForeignKey("goals.goal_id"))
    intent_version = Column(Integer)
    template_id = Column(String(100), nullable=False)
    template_version = Column(String(20), default="v1")
    prompt = Column(Text)
    required_points = Column(PG_JSONB)
    estimated_minutes = Column(Integer)
    training_mode = Column(String(20), default="independent")
    source_refs = Column(PG_JSONB)
    framework_tags = Column(PG_JSONB)
    status = Column(String(20), default="pending")
    input_snapshot = Column(PG_JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending','in_progress','completed','cancelled')",
            name="chk_task_status",
        ),
        CheckConstraint(
            "training_mode IN ('independent','synthetic','historical','user_reflection')",
            name="chk_training_mode",
        ),
    )


class ArtifactVersion(Base):
    __tablename__ = "artifact_versions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    root_artifact_id = Column(PG_UUID(as_uuid=True))
    task_id = Column(PG_UUID(as_uuid=True), ForeignKey("practice_tasks.id"))
    revision = Column(Integer, default=1, nullable=False)
    body = Column(Text, nullable=False)
    assistance_mode = Column(String(30), default="independent")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "assistance_mode IN ('independent','hinted','reference_visible','ai_assisted','unknown')",
            name="chk_assistance_mode",
        ),
        Index("idx_artifact_root", "root_artifact_id"),
    )


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artifact_version_id = Column(PG_UUID(as_uuid=True), ForeignKey("artifact_versions.id"), nullable=False, index=True)
    rubric_version = Column(String(20), default="v1")
    dimension_scores = Column(PG_JSONB)
    candidate_feedback = Column(Text)
    user_result = Column(Text)
    evaluator = Column(String(20), default="ai_candidate")
    status = Column(String(20), default="candidate")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "evaluator IN ('ai_candidate','user_self','confirmed')",
            name="chk_evaluator",
        ),
        CheckConstraint(
            "status IN ('candidate','user_accepted','superseded')",
            name="chk_eval_status",
        ),
    )


class PrincipleVersion(Base):
    __tablename__ = "principle_versions"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    statement = Column(Text, nullable=False)
    scope = Column(Text)
    supporting_evidence_ids = Column(PG_JSONB)
    counterexample_refs = Column(PG_JSONB)
    uncertainties = Column(PG_JSONB)
    confirmation_status = Column(String(20), default="proposed")
    version = Column(Integer, default=1, nullable=False)
    review_at = Column(Date)
    supersedes_id = Column(PG_UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "confirmation_status IN ('proposed','confirmed','revised','retired')",
            name="chk_principle_status",
        ),
    )


class BackgroundTaskRecord(Base):
    __tablename__ = "background_tasks"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    task_key = Column(String(200), unique=True, nullable=False)
    input_refs = Column(PG_JSONB)
    input_versions = Column(PG_JSONB)
    status = Column(String(20), default="queued")
    attempts = Column(Integer, default=0)
    max_attempts = Column(Integer, default=3)
    epoch = Column(Integer, default=1)
    lease_expires_at = Column(DateTime(timezone=True))
    result_ref = Column(PG_JSONB)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint(
            "status IN ('queued','running','succeeded','failed','cancelled')",
            name="chk_bg_status",
        ),
    )


class LearningEvent(Base):
    __tablename__ = "learning_events"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)
    object_ref = Column(PG_UUID(as_uuid=True))
    idempotency_key = Column(String(200), nullable=False, unique=True)
    payload = Column(PG_JSONB)
    local_date = Column(Date)
    timezone = Column(String(50), default="Asia/Shanghai")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        Index("idx_event_user_type", "user_id", "event_type"),
    )


class RewardLedger(Base):
    __tablename__ = "reward_ledger"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, index=True)
    event_id = Column(PG_UUID(as_uuid=True), nullable=False)
    rule_version = Column(String(20), nullable=False)
    delta = Column(Integer, default=0)
    category = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("event_id", "rule_version", name="uq_reward_event_rule"),
    )

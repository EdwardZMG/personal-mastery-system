"""Dashboard aggregation API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func as sql_func
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import (
    User, UserProfile, LearningContent, LearningRecord,
    DailyCheckin, Goal, HabitTracking, HabitLog, KnowledgeBase,
)
from app.models_extended import (
    StructuredKnowledge, KnowledgeInsight, KnowledgeApplication,
    ApplicationStats, ReviewSession, ChineseClassicsProgress,
)

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


# Pydantic schemas
class DashboardOverview(BaseModel):
    """Full dashboard overview"""
    knowledge_count: int
    insights_count: int
    learning_hours_total: float
    learning_hours_this_week: float
    habit_streak_best: int
    active_habits: int
    goals_active: int
    goals_completed: int
    goal_avg_progress: float
    checkin_streak: int
    applications_count: int
    classics_chapters: int
    recent_activity: List[dict]


class KnowledgeDomainStats(BaseModel):
    """Knowledge domain distribution and mastery"""
    domain: str
    count: int
    avg_mastery: float


class KnowledgeStatsResponse(BaseModel):
    """Knowledge statistics response"""
    total_insights: int
    total_structured: int
    total_applications: int
    by_domain: List[KnowledgeDomainStats]
    mastery_trend: List[dict]


class TimelineEntry(BaseModel):
    """A single entry in the learning timeline"""
    date: str
    learning_minutes: int
    items_completed: int
    checkin_done: bool


class LearningTimelineResponse(BaseModel):
    """Learning timeline response"""
    period: str
    entries: List[TimelineEntry]
    total_minutes: int
    total_items: int


class MaskScoresResponse(BaseModel):
    """MASK dimension scores"""
    mindset: float
    attitude: float
    skills: float
    knowledge: float


class PhysicalScoresResponse(BaseModel):
    """Physical dimension scores for four-dimension capability model"""
    energy: float
    fitness: float
    sleep_quality: float
    exercise_frequency: float


class MaslowScoresResponse(BaseModel):
    """Maslow need-level scores"""
    physiological: float
    safety: float
    belonging: float
    esteem: float
    self_actualization: float


@router.get("/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    db: Session = Depends(get_db),
):
    """
    Get a full dashboard overview.

    Aggregates data from knowledge, learning, habits, goals, check-ins,
    applications, and classics modules into a single response.
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    # Knowledge counts
    insights_count = db.query(KnowledgeInsight).filter(KnowledgeInsight.user_id == user_id).count()
    structured_count = (
        db.query(StructuredKnowledge)
        .join(KnowledgeInsight, StructuredKnowledge.insight_id == KnowledgeInsight.id)
        .filter(KnowledgeInsight.user_id == user_id)
        .count()
    )

    # Learning hours
    records = db.query(LearningRecord).filter(LearningRecord.user_id == user_id).all()
    total_minutes = sum(r.duration_minutes or 0 for r in records)
    week_ago = datetime.now() - timedelta(days=7)
    week_minutes = sum(r.duration_minutes or 0 for r in records if r.created_at and r.created_at >= week_ago)

    # Habits
    habits = db.query(HabitTracking).filter(HabitTracking.user_id == user_id, HabitTracking.is_active == True).all()
    best_streak = max((h.longest_streak or 0 for h in habits), default=0)

    # Goals
    goals = db.query(Goal).filter(Goal.user_id == user_id).all()
    active_goals = [g for g in goals if g.status == "active"]
    completed_goals = [g for g in goals if g.status == "completed"]
    avg_progress = sum(g.progress_percent or 0 for g in active_goals) / len(active_goals) if active_goals else 0.0

    # Check-in streak
    checkins = (
        db.query(DailyCheckin)
        .filter(DailyCheckin.user_id == user_id)
        .order_by(DailyCheckin.checkin_date.desc())
        .all()
    )
    checkin_streak = 0
    check_date = date.today()
    checkin_dates = {c.checkin_date for c in checkins}
    while str(check_date) in checkin_dates:
        checkin_streak += 1
        check_date -= timedelta(days=1)

    # Applications
    app_count = db.query(KnowledgeApplication).filter(KnowledgeApplication.user_id == user_id).count()

    # Classics
    classics_count = (
        db.query(ChineseClassicsProgress)
        .filter(ChineseClassicsProgress.user_id == user_id)
        .count()
    )

    # Recent activity (last 10 events across modules)
    recent = _build_recent_activity(user_id, db, limit=10)

    return DashboardOverview(
        knowledge_count=structured_count,
        insights_count=insights_count,
        learning_hours_total=round(total_minutes / 60, 1),
        learning_hours_this_week=round(week_minutes / 60, 1),
        habit_streak_best=best_streak,
        active_habits=len(habits),
        goals_active=len(active_goals),
        goals_completed=len(completed_goals),
        goal_avg_progress=round(avg_progress, 1),
        checkin_streak=checkin_streak,
        applications_count=app_count,
        classics_chapters=classics_count,
        recent_activity=recent,
    )


def _build_recent_activity(user_id: UUID, db: Session, limit: int = 10) -> List[dict]:
    """Build a merged recent activity feed."""
    activities = []

    # Recent learning records
    records = (
        db.query(LearningRecord)
        .filter(LearningRecord.user_id == user_id)
        .order_by(LearningRecord.created_at.desc())
        .limit(5)
        .all()
    )
    for r in records:
        activities.append({
            "type": "learning",
            "date": r.created_at.isoformat() if r.created_at else None,
            "detail": f"Learning record: {r.status} ({r.duration_minutes or 0} min)",
        })

    # Recent check-ins
    checkins = (
        db.query(DailyCheckin)
        .filter(DailyCheckin.user_id == user_id)
        .order_by(DailyCheckin.checkin_date.desc())
        .limit(3)
        .all()
    )
    for c in checkins:
        activities.append({
            "type": "checkin",
            "date": c.created_at.isoformat() if c.created_at else None,
            "detail": f"Daily check-in: mood {c.mood}, energy {c.energy_level}",
        })

    # Recent applications
    apps = (
        db.query(KnowledgeApplication)
        .filter(KnowledgeApplication.user_id == user_id)
        .order_by(KnowledgeApplication.created_at.desc())
        .limit(3)
        .all()
    )
    for a in apps:
        activities.append({
            "type": "application",
            "date": a.created_at.isoformat() if a.created_at else None,
            "detail": f"Knowledge applied (effectiveness: {a.effectiveness})",
        })

    # Sort by date descending and truncate
    activities.sort(key=lambda x: x.get("date") or "", reverse=True)
    return activities[:limit]


@router.get("/knowledge-stats", response_model=KnowledgeStatsResponse)
async def get_knowledge_stats(
    db: Session = Depends(get_db),
):
    """
    Get knowledge domain distribution and mastery trends.

    Returns counts and average mastery per domain, plus a simplified
    mastery trend over recent reviews.
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    insights_count = db.query(KnowledgeInsight).filter(KnowledgeInsight.user_id == user_id).count()
    app_count = db.query(KnowledgeApplication).filter(KnowledgeApplication.user_id == user_id).count()

    # Get all insights for this user to find their structured knowledge
    user_insights = db.query(KnowledgeInsight).filter(KnowledgeInsight.user_id == user_id).all()
    insight_ids = [i.id for i in user_insights]

    structured = (
        db.query(StructuredKnowledge)
        .filter(StructuredKnowledge.insight_id.in_(insight_ids))
        .all()
    ) if insight_ids else []

    # Group by domain
    domain_map: dict = {}
    for sk in structured:
        d = sk.domain or "unknown"
        if d not in domain_map:
            domain_map[d] = {"count": 0, "total_mastery": 0.0}
        domain_map[d]["count"] += 1
        domain_map[d]["total_mastery"] += sk.mastery_level or 0.5

    by_domain = [
        KnowledgeDomainStats(
            domain=d,
            count=v["count"],
            avg_mastery=round(v["total_mastery"] / v["count"], 3) if v["count"] else 0.0,
        )
        for d, v in domain_map.items()
    ]

    # Simplified mastery trend (last 10 reviewed items)
    reviewed = sorted(
        [sk for sk in structured if sk.last_reviewed],
        key=lambda x: x.last_reviewed,
        reverse=True,
    )[:10]
    mastery_trend = [
        {
            "title": sk.title,
            "mastery_level": sk.mastery_level,
            "reviewed_at": sk.last_reviewed.isoformat() if sk.last_reviewed else None,
        }
        for sk in reviewed
    ]

    return KnowledgeStatsResponse(
        total_insights=insights_count,
        total_structured=len(structured),
        total_applications=app_count,
        by_domain=by_domain,
        mastery_trend=mastery_trend,
    )


@router.get("/learning-timeline", response_model=LearningTimelineResponse)
async def get_learning_timeline(
    period: str = "weekly",
    db: Session = Depends(get_db),
):
    """
    Get learning activity over time.

    Query parameters:
    - period: 'weekly' (last 7 days) or 'monthly' (last 30 days)
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    days = 7 if period == "weekly" else 30
    start = datetime.now() - timedelta(days=days)

    records = (
        db.query(LearningRecord)
        .filter(LearningRecord.user_id == user_id, LearningRecord.created_at >= start)
        .all()
    )

    checkins = (
        db.query(DailyCheckin)
        .filter(DailyCheckin.user_id == user_id, DailyCheckin.created_at >= start)
        .all()
    )
    checkin_dates = {c.checkin_date for c in checkins}

    # Build day-by-day entries
    entries = []
    today = date.today()
    total_minutes = 0
    total_items = 0

    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        day_str = str(d)
        day_records = [
            r for r in records
            if r.created_at and r.created_at.date() == d
        ]
        day_minutes = sum(r.duration_minutes or 0 for r in day_records)
        day_items = sum(1 for r in day_records if r.status == "completed")

        total_minutes += day_minutes
        total_items += day_items

        entries.append(TimelineEntry(
            date=day_str,
            learning_minutes=day_minutes,
            items_completed=day_items,
            checkin_done=day_str in checkin_dates,
        ))

    return LearningTimelineResponse(
        period=period,
        entries=entries,
        total_minutes=total_minutes,
        total_items=total_items,
    )


@router.get("/mask-scores", response_model=MaskScoresResponse)
async def get_mask_scores(
    db: Session = Depends(get_db),
):
    """
    Get current MASK dimension scores.

    MASK = Mindset (思维模式), Attitude (人生态度), Skills (技能), Knowledge (知识储备)
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile or not profile.mask_scores:
        return MaskScoresResponse(mindset=0, attitude=0, skills=0, knowledge=0)

    scores = profile.mask_scores
    return MaskScoresResponse(
        mindset=scores.get("mindset", 0),
        attitude=scores.get("attitude", 0),
        skills=scores.get("skills", 0),
        knowledge=scores.get("knowledge", 0),
    )


@router.get("/physical-scores", response_model=PhysicalScoresResponse)
async def get_physical_scores(
    db: Session = Depends(get_db),
):
    """
    Get current physical dimension scores for four-dimension capability model.

    Physical dimensions: energy (精力), fitness (体能), sleep_quality (睡眠质量), exercise_frequency (运动频率)
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile or not profile.physical_scores:
        return PhysicalScoresResponse(energy=0, fitness=0, sleep_quality=0, exercise_frequency=0)

    scores = profile.physical_scores
    return PhysicalScoresResponse(
        energy=scores.get("energy", 0),
        fitness=scores.get("fitness", 0),
        sleep_quality=scores.get("sleep_quality", 0),
        exercise_frequency=scores.get("exercise_frequency", 0),
    )


@router.get("/maslow-scores", response_model=MaslowScoresResponse)
async def get_maslow_scores(
    db: Session = Depends(get_db),
):
    """
    Get current Maslow need-level scores.

    Levels: physiological, safety, belonging, esteem, self_actualization
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile or not profile.maslow_scores:
        return MaslowScoresResponse(
            physiological=0, safety=0, belonging=0, esteem=0, self_actualization=0,
        )

    scores = profile.maslow_scores
    return MaslowScoresResponse(
        physiological=scores.get("physiological", 0),
        safety=scores.get("safety", 0),
        belonging=scores.get("belonging", 0),
        esteem=scores.get("esteem", 0),
        self_actualization=scores.get("self_actualization", 0),
    )

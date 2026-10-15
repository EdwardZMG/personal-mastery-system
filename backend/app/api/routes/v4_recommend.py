"""Recommendation & Learning Events API — V4"""
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models_v4 import (
    PracticeTask, ArtifactVersion, Evaluation,
    PersonalIntentVersion, LearningEvent, Domain, Competency,
)
from app.training_templates import TRAINING_TEMPLATES

router = APIRouter(prefix="/api/v1/v4/recommend", tags=["v4-recommend"])


class RecommendationItem(BaseModel):
    template_id: str
    domain_id: str
    title: str
    reason: str
    estimated_minutes: int
    priority: str


class RecommendationResponse(BaseModel):
    recommendations: List[RecommendationItem]
    generated_at: datetime
    intent_version: Optional[int]
    active_goal_count: int
    practice_count_7d: int


@router.get("/next", response_model=RecommendationResponse)
async def get_recommendations(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_uuid = UUID(user_id)

    intent = (
        db.query(PersonalIntentVersion)
        .filter(PersonalIntentVersion.user_id == user_uuid, PersonalIntentVersion.status == "confirmed")
        .first()
    )
    intent_version = intent.version if intent else None

    recent_tasks = (
        db.query(PracticeTask)
        .filter(PracticeTask.user_id == user_uuid)
        .order_by(PracticeTask.created_at.desc())
        .limit(20)
        .all()
    )
    completed_domains = set()
    for t in recent_tasks:
        if t.status == "completed" and t.domain_id:
            completed_domains.add(t.domain_id)

    from datetime import timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)
    practice_count_7d = (
        db.query(PracticeTask)
        .filter(PracticeTask.user_id == user_uuid, PracticeTask.created_at >= week_ago)
        .count()
    )

    from app.models import Goal
    active_goal_count = (
        db.query(Goal)
        .filter(Goal.user_id == user_uuid, Goal.status == "active")
        .count()
    )

    all_domains = db.query(Domain).filter(Domain.is_active == True).order_by(Domain.sort_order).all()

    recommendations = []
    for domain in all_domains:
        templates = [t for t in TRAINING_TEMPLATES.values() if t["domain_id"] == domain.id]
        if not templates:
            continue

        done_templates = {t.template_id for t in recent_tasks if t.domain_id == domain.id}
        undone = [t for t in templates if t["id"] not in done_templates]
        if not undone:
            undone = templates

        chosen = undone[0]
        if domain.id in completed_domains:
            priority = "maintenance"
            reason = f"{domain.title}已有练习记录，建议持续巩固"
        elif not intent:
            priority = "low"
            reason = "建议先确认个人方向，以便获得更精准的推荐"
        else:
            priority = "recommended"
            reason = f"基于{domain.title}领域的能力发展路径推荐"

        recommendations.append(RecommendationItem(
            template_id=chosen["id"],
            domain_id=domain.id,
            title=chosen["title"],
            reason=reason,
            estimated_minutes=chosen.get("estimated_minutes", 15),
            priority=priority,
        ))

    priority_order = {"recommended": 0, "maintenance": 1, "low": 2}
    recommendations.sort(key=lambda r: priority_order.get(r.priority, 9))

    return RecommendationResponse(
        recommendations=recommendations[:5],
        generated_at=datetime.utcnow(),
        intent_version=intent_version,
        active_goal_count=active_goal_count,
        practice_count_7d=practice_count_7d,
    )


class LearningEventCreate(BaseModel):
    event_type: str
    object_ref: Optional[UUID] = None
    idempotency_key: str
    payload: Optional[Any] = None
    local_date: Optional[date] = None


class LearningEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    event_type: str
    object_ref: Optional[UUID]
    idempotency_key: str
    payload: Optional[Any]
    local_date: Optional[date]
    timezone: str
    created_at: Optional[datetime]


@router.post("/events", response_model=LearningEventResponse, status_code=status.HTTP_201_CREATED)
async def record_learning_event(
    request: LearningEventCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    existing = db.query(LearningEvent).filter(
        LearningEvent.idempotency_key == request.idempotency_key
    ).first()
    if existing:
        return existing

    event = LearningEvent(
        user_id=UUID(user_id),
        event_type=request.event_type,
        object_ref=request.object_ref,
        idempotency_key=request.idempotency_key,
        payload=request.payload,
        local_date=request.local_date or date.today(),
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/events", response_model=List[LearningEventResponse])
async def list_learning_events(
    event_type: Optional[str] = None,
    days: int = 7,
    limit: int = 50,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    since = datetime.utcnow() - __import__("datetime").timedelta(days=days)
    query = db.query(LearningEvent).filter(
        LearningEvent.user_id == UUID(user_id),
        LearningEvent.created_at >= since,
    )
    if event_type:
        query = query.filter(LearningEvent.event_type == event_type)
    return query.order_by(LearningEvent.created_at.desc()).limit(limit).all()


@router.get("/summary")
async def get_learning_summary(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_uuid = UUID(user_id)
    from datetime import timedelta
    week_ago = datetime.utcnow() - timedelta(days=7)

    total_tasks = db.query(PracticeTask).filter(PracticeTask.user_id == user_uuid).count()
    completed_tasks = (
        db.query(PracticeTask)
        .filter(PracticeTask.user_id == user_uuid, PracticeTask.status == "completed")
        .count()
    )
    tasks_7d = (
        db.query(PracticeTask)
        .filter(PracticeTask.user_id == user_uuid, PracticeTask.created_at >= week_ago)
        .count()
    )
    total_artifacts = (
        db.query(ArtifactVersion).filter(ArtifactVersion.user_id == user_uuid).count()
    )
    events_7d = (
        db.query(LearningEvent)
        .filter(LearningEvent.user_id == user_uuid, LearningEvent.created_at >= week_ago)
        .count()
    )

    domain_stats = {}
    for domain in db.query(Domain).filter(Domain.is_active == True).all():
        count = (
            db.query(PracticeTask)
            .filter(PracticeTask.user_id == user_uuid, PracticeTask.domain_id == domain.id, PracticeTask.status == "completed")
            .count()
        )
        if count > 0:
            domain_stats[domain.id] = {"title": domain.title, "completed": count}

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "tasks_last_7d": tasks_7d,
        "total_artifacts": total_artifacts,
        "events_last_7d": events_7d,
        "domain_breakdown": domain_stats,
    }

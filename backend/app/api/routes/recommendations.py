"""Content recommendation API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import LearningContent, LearningRecord, UserProfile
from app.models_extended import StructuredKnowledge, KnowledgeInsight

router = APIRouter(prefix="/api/v1/recommendations", tags=["recommendations"])


# Pydantic schemas
class RecommendationItem(BaseModel):
    """A single recommended content item"""
    content_id: UUID
    title: str
    category: str
    difficulty_level: int
    estimated_minutes: int
    mask_dimension: Optional[str]
    reason: str
    score: float


class RecommendationsResponse(BaseModel):
    """Response schema for content recommendations"""
    recommendations: List[RecommendationItem]
    generated_at: datetime
    strategy: str


class NextReviewItem(BaseModel):
    """An item due for spaced repetition review"""
    knowledge_id: UUID
    title: str
    domain: str
    mastery_level: float
    next_review_date: Optional[str]
    review_count: int
    urgency: str


class NextReviewResponse(BaseModel):
    """Response schema for next review items"""
    items: List[NextReviewItem]
    total_due: int
    checked_at: datetime


@router.get("/", response_model=RecommendationsResponse)
async def get_recommendations(
    category: Optional[str] = None,
    max_difficulty: Optional[int] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    """
    Get personalized content recommendations.

    Uses a simple rule-based strategy:
    1. Match content category to user's expertise_levels (recommend
       domains where the user has lower expertise to encourage growth).
    2. Filter by difficulty -- prefer content slightly above the user's
       current level.
    3. Exclude content already completed by the user.
    4. Sort by a freshness + relevance score.

    Query parameters:
    - category: Restrict to a specific category
    - max_difficulty: Maximum difficulty level (1-5, default 5)
    - limit: Number of recommendations (default 10, max 50)
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    # Fetch user profile for expertise levels
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    expertise = profile.expertise_levels if profile and profile.expertise_levels else {}

    # Get completed content IDs to exclude
    completed_records = (
        db.query(LearningRecord)
        .filter(LearningRecord.user_id == user_id, LearningRecord.status == "completed")
        .all()
    )
    completed_ids = {r.content_id for r in completed_records}

    # Build base query
    query = db.query(LearningContent).filter(LearningContent.is_active == True)

    if category:
        query = query.filter(LearningContent.category == category)
    if max_difficulty is not None:
        query = query.filter(LearningContent.difficulty_level <= max_difficulty)

    candidates = query.all()

    # Score each candidate
    scored: List[dict] = []
    for content in candidates:
        if content.content_id in completed_ids:
            continue

        # Base score from category expertise gap (lower expertise = higher score)
        cat = content.category or "general"
        user_expertise = expertise.get(cat, 0.5)
        relevance_score = max(0, 1.0 - user_expertise)

        # Difficulty bonus: prefer content slightly above current level
        difficulty = content.difficulty_level or 1
        difficulty_score = 1.0 - abs(difficulty - 3) / 5.0  # prefer medium difficulty

        # Freshness bonus
        age_days = (datetime.now() - content.created_at).days if content.created_at else 30
        freshness_score = max(0, 1.0 - age_days / 90.0)

        total_score = round(relevance_score * 0.5 + difficulty_score * 0.3 + freshness_score * 0.2, 3)

        # Determine reason
        reasons = []
        if relevance_score > 0.5:
            reasons.append(f"Matches growth area: {cat}")
        if difficulty_score > 0.6:
            reasons.append("Appropriate difficulty")
        if freshness_score > 0.7:
            reasons.append("Recently added")
        reason = "; ".join(reasons) if reasons else "General recommendation"

        scored.append({
            "content": content,
            "score": total_score,
            "reason": reason,
        })

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)

    recommendations = [
        RecommendationItem(
            content_id=s["content"].content_id,
            title=s["content"].title,
            category=s["content"].category,
            difficulty_level=s["content"].difficulty_level,
            estimated_minutes=s["content"].estimated_minutes,
            mask_dimension=s["content"].mask_dimension,
            reason=s["reason"],
            score=s["score"],
        )
        for s in scored[:limit]
    ]

    return RecommendationsResponse(
        recommendations=recommendations,
        generated_at=datetime.now(),
        strategy="rule_based_expertise_gap",
    )


@router.get("/next-review", response_model=NextReviewResponse)
async def get_next_review(
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """
    Get items due for spaced repetition review.

    Returns structured knowledge items whose next_review_date has passed
    or is today, sorted by urgency (overdue items first, then by
    lowest mastery).

    Query parameters:
    - limit: Maximum items to return (default 20, max 100)
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    today = date.today()

    # Get user's insight IDs
    user_insights = db.query(KnowledgeInsight).filter(KnowledgeInsight.user_id == user_id).all()
    insight_ids = [i.id for i in user_insights]

    if not insight_ids:
        return NextReviewResponse(items=[], total_due=0, checked_at=datetime.now())

    # Find knowledge due for review
    due_items = (
        db.query(StructuredKnowledge)
        .filter(
            StructuredKnowledge.insight_id.in_(insight_ids),
            StructuredKnowledge.status.in_(["structured", "reviewed"]),
        )
        .all()
    )

    review_items = []
    for sk in due_items:
        next_review = sk.next_review_date
        is_overdue = next_review and next_review <= today
        is_due = next_review is None or is_overdue

        if not is_due:
            continue

        # Calculate urgency
        if next_review and is_overdue:
            days_overdue = (today - next_review).days
            if days_overdue > 7:
                urgency = "critical"
            elif days_overdue > 3:
                urgency = "high"
            else:
                urgency = "medium"
        else:
            urgency = "low"

        review_items.append({
            "item": sk,
            "urgency": urgency,
        })

    # Sort: critical > high > medium > low, then by mastery ascending
    urgency_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    review_items.sort(key=lambda x: (urgency_order.get(x["urgency"], 4), x["item"].mastery_level or 0))

    items = [
        NextReviewItem(
            knowledge_id=ri["item"].id,
            title=ri["item"].title,
            domain=ri["item"].domain,
            mastery_level=ri["item"].mastery_level or 0,
            next_review_date=str(ri["item"].next_review_date) if ri["item"].next_review_date else None,
            review_count=ri["item"].review_count or 0,
            urgency=ri["urgency"],
        )
        for ri in review_items[:limit]
    ]

    return NextReviewResponse(
        items=items,
        total_due=len(review_items),
        checked_at=datetime.now(),
    )

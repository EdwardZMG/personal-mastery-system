"""
Ebbinghaus spaced repetition review API
SM-2 algorithm for optimal review scheduling
"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date, timedelta
import math

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from pydantic import BaseModel, Field

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models_extended import ReviewCard, StructuredKnowledge, KnowledgeInsight

router = APIRouter(prefix="/api/v1/spaced-repetition", tags=["spaced-repetition"])

EBBINGHAUS_INTERVALS = [1, 2, 4, 7, 15, 30]


class ReviewAnswer(BaseModel):
    card_id: UUID
    quality: int = Field(..., ge=0, le=5, description="0=blackout, 5=perfect")


class ReviewSessionRequest(BaseModel):
    card_ids: Optional[List[UUID]] = None
    max_cards: int = Field(default=20, ge=1, le=50)


class CardCreate(BaseModel):
    knowledge_id: UUID
    card_type: str = Field(..., description="concept/application/connection/reflection/challenge")
    question: str
    answer: str
    difficulty: int = Field(default=3, ge=1, le=5)


class CardResponse(BaseModel):
    id: UUID
    card_type: str
    question: str
    answer: str
    difficulty: int
    ease_factor: float
    interval_days: int
    next_review_date: Optional[str]
    review_count: int
    correct_count: int
    is_due: bool = False

    class Config:
        from_attributes = True


class ReviewResult(BaseModel):
    card_id: UUID
    new_ease_factor: float
    new_interval: int
    next_review_date: str
    was_correct: bool


class SessionStats(BaseModel):
    total_cards: int
    reviewed: int
    correct: int
    accuracy: float
    xp_earned: int
    streak_updated: bool


def sm2_update(ease_factor: float, interval: int, quality: int, review_count: int):
    """
    SM-2 algorithm update.
    quality: 0-5 (0=complete blackout, 5=perfect response)
    Returns (new_ease_factor, new_interval_days)
    """
    if quality < 3:
        return max(1.3, ease_factor - 0.2), 1

    ef = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ef = max(1.3, ef)

    if review_count == 0:
        new_interval = 1
    elif review_count == 1:
        new_interval = 2
    else:
        new_interval = round(interval * ef)

    return ef, max(1, new_interval)


def is_card_due(card: ReviewCard) -> bool:
    if not card.next_review_date:
        return True
    try:
        next_date = datetime.fromisoformat(card.next_review_date).date()
        return date.today() >= next_date
    except (ValueError, TypeError):
        return True


@router.get("/due", response_model=List[CardResponse])
async def get_due_cards(
    max_cards: int = 20,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_id = UUID(user_id)
    today_str = date.today().isoformat()
    cards = db.query(ReviewCard).filter(
        ReviewCard.user_id == user_id,
        ReviewCard.is_active == True,
    ).filter(
        (ReviewCard.next_review_date == None) |
        (ReviewCard.next_review_date <= today_str)
    ).order_by(ReviewCard.next_review_date.asc()).limit(max_cards).all()

    return [CardResponse(
        id=c.id, card_type=c.card_type, question=c.question, answer=c.answer,
        difficulty=c.difficulty, ease_factor=c.ease_factor,
        interval_days=c.interval_days, next_review_date=c.next_review_date,
        review_count=c.review_count, correct_count=c.correct_count,
        is_due=True,
    ) for c in cards]


@router.get("/cards", response_model=List[CardResponse])
async def get_all_cards(
    card_type: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_id = UUID(user_id)
    query = db.query(ReviewCard).filter(
        ReviewCard.user_id == user_id,
        ReviewCard.is_active == True,
    )
    if card_type:
        query = query.filter(ReviewCard.card_type == card_type)

    cards = query.order_by(ReviewCard.next_review_date.asc()).all()
    today_str = date.today().isoformat()

    return [CardResponse(
        id=c.id, card_type=c.card_type, question=c.question, answer=c.answer,
        difficulty=c.difficulty, ease_factor=c.ease_factor,
        interval_days=c.interval_days, next_review_date=c.next_review_date,
        review_count=c.review_count, correct_count=c.correct_count,
        is_due=(c.next_review_date or "") <= today_str if c.next_review_date else True,
    ) for c in cards]


@router.post("/cards", response_model=CardResponse, status_code=status.HTTP_201_CREATED)
async def create_card(
    req: CardCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_id = UUID(user_id)
    knowledge = db.query(StructuredKnowledge).filter(
        StructuredKnowledge.id == req.knowledge_id).first()
    if not knowledge:
        raise HTTPException(404, "Knowledge not found")

    next_review = (date.today() + timedelta(days=1)).isoformat()
    card = ReviewCard(
        user_id=user_id,
        knowledge_id=req.knowledge_id,
        card_type=req.card_type,
        question=req.question,
        answer=req.answer,
        difficulty=req.difficulty,
        next_review_date=next_review,
    )
    db.add(card)
    db.commit()
    db.refresh(card)

    return CardResponse(
        id=card.id, card_type=card.card_type, question=card.question, answer=card.answer,
        difficulty=card.difficulty, ease_factor=card.ease_factor,
        interval_days=card.interval_days, next_review_date=card.next_review_date,
        review_count=card.review_count, correct_count=card.correct_count,
        is_due=False,
    )


@router.post("/session/start", response_model=List[CardResponse])
async def start_review_session(
    req: ReviewSessionRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_id = UUID(user_id)
    if req.card_ids:
        cards = db.query(ReviewCard).filter(
            ReviewCard.id.in_(req.card_ids),
            ReviewCard.user_id == user_id,
            ReviewCard.is_active == True,
        ).all()
    else:
        today_str = date.today().isoformat()
        cards = db.query(ReviewCard).filter(
            ReviewCard.user_id == user_id,
            ReviewCard.is_active == True,
        ).filter(
            (ReviewCard.next_review_date == None) |
            (ReviewCard.next_review_date <= today_str)
        ).order_by(ReviewCard.next_review_date.asc()).limit(req.max_cards).all()

    return [CardResponse(
        id=c.id, card_type=c.card_type, question=c.question, answer=c.answer,
        difficulty=c.difficulty, ease_factor=c.ease_factor,
        interval_days=c.interval_days, next_review_date=c.next_review_date,
        review_count=c.review_count, correct_count=c.correct_count,
        is_due=True,
    ) for c in cards]


@router.post("/session/answer", response_model=ReviewResult)
async def answer_card(
    req: ReviewAnswer,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_id = UUID(user_id)
    card = db.query(ReviewCard).filter(
        ReviewCard.id == req.card_id,
        ReviewCard.user_id == user_id).first()
    if not card:
        raise HTTPException(404, "Card not found")

    was_correct = req.quality >= 3
    new_ef, new_interval = sm2_update(
        card.ease_factor, card.interval_days, req.quality, card.review_count)

    card.ease_factor = new_ef
    card.interval_days = new_interval
    card.review_count += 1
    card.last_quality_score = req.quality
    if was_correct:
        card.correct_count += 1

    next_date = date.today() + timedelta(days=new_interval)
    card.next_review_date = next_date.isoformat()

    knowledge = db.query(StructuredKnowledge).filter(
        StructuredKnowledge.id == card.knowledge_id).first()
    if knowledge:
        knowledge.review_count = (knowledge.review_count or 0) + 1
        knowledge.last_reviewed = datetime.now()
        knowledge.next_review_date = next_date

    db.commit()

    return ReviewResult(
        card_id=card.id,
        new_ease_factor=round(new_ef, 2),
        new_interval=new_interval,
        next_review_date=card.next_review_date,
        was_correct=was_correct,
    )


@router.post("/session/complete", response_model=SessionStats)
async def complete_session(
    results: List[ReviewAnswer],
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_id = UUID(user_id)
    total = len(results)
    correct = sum(1 for r in results if r.quality >= 3)
    accuracy = correct / total if total > 0 else 0.0
    xp = int(10 + accuracy * 20)

    from app.models import UserProfile
    from app.models_extended import UserLevel, StreakRecord
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    level = db.query(UserLevel).filter(UserLevel.user_id == user_id).first()
    if profile:
        profile.total_xp = (profile.total_xp or 0) + xp
    if level:
        level.total_xp = (level.total_xp or 0) + xp

    sr = db.query(StreakRecord).filter(
        StreakRecord.user_id == user_id,
        StreakRecord.streak_type == "review").first()
    streak_updated = False
    if not sr:
        sr = StreakRecord(user_id=user_id, streak_type="review")
        db.add(sr)
        db.commit()
        db.refresh(sr)

    today_str = date.today().isoformat()
    yesterday_str = (date.today() - timedelta(days=1)).isoformat()
    if sr.last_active_date != today_str:
        if sr.last_active_date == yesterday_str:
            sr.current_streak += 1
        else:
            sr.current_streak = 1
        sr.longest_streak = max(sr.longest_streak, sr.current_streak)
        sr.last_active_date = today_str
        streak_updated = True

    db.commit()

    return SessionStats(
        total_cards=total,
        reviewed=total,
        correct=correct,
        accuracy=round(accuracy, 2),
        xp_earned=xp,
        streak_updated=streak_updated,
    )


@router.get("/stats")
async def get_review_stats(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    total_cards = db.query(ReviewCard).filter(
        ReviewCard.user_id == user_id, ReviewCard.is_active == True).count()

    today_str = date.today().isoformat()
    due_today = db.query(ReviewCard).filter(
        ReviewCard.user_id == user_id,
        ReviewCard.is_active == True,
    ).filter(
        (ReviewCard.next_review_date == None) |
        (ReviewCard.next_review_date <= today_str)
    ).count()

    total_reviews = db.query(ReviewCard).filter(
        ReviewCard.user_id == user_id).with_entities(
        ReviewCard.review_count).all()
    total_review_count = sum(r[0] for r in total_reviews) if total_reviews else 0

    total_correct = db.query(ReviewCard).filter(
        ReviewCard.user_id == user_id).with_entities(
        ReviewCard.correct_count).all()
    total_correct_count = sum(r[0] for r in total_correct) if total_correct else 0

    from app.models_extended import StreakRecord
    sr = db.query(StreakRecord).filter(
        StreakRecord.user_id == user_id,
        StreakRecord.streak_type == "review").first()

    return {
        "total_cards": total_cards,
        "due_today": due_today,
        "total_reviews": total_review_count,
        "total_correct": total_correct_count,
        "overall_accuracy": round(total_correct_count / total_review_count, 2) if total_review_count > 0 else 0,
        "review_streak": sr.current_streak if sr else 0,
        "longest_review_streak": sr.longest_streak if sr else 0,
    }


@router.post("/cards/generate-from-knowledge")
async def generate_cards_from_knowledge(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_id = UUID(user_id)
    knowledge_items = db.query(StructuredKnowledge).join(
        KnowledgeInsight, StructuredKnowledge.insight_id == KnowledgeInsight.id
    ).filter(KnowledgeInsight.user_id == user_id).all()

    created = 0
    for k in knowledge_items:
        existing = db.query(ReviewCard).filter(
            ReviewCard.user_id == user_id,
            ReviewCard.knowledge_id == k.id).first()
        if existing:
            continue

        card_type = "concept"
        question = f"请简述：{k.title}"
        answer = k.explanation or k.core_concept or k.title

        if not answer:
            continue

        next_review = (date.today() + timedelta(days=1)).isoformat()
        card = ReviewCard(
            user_id=user_id,
            knowledge_id=k.id,
            card_type=card_type,
            question=question,
            answer=answer[:500],
            difficulty=k.difficulty or 3,
            next_review_date=next_review,
        )
        db.add(card)
        created += 1

    db.commit()
    return {"message": f"Generated {created} review cards", "cards_created": created}


@router.delete("/cards/{card_id}")
async def delete_card(card_id: UUID, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user_id = UUID(user_id)
    card = db.query(ReviewCard).filter(
        ReviewCard.id == card_id,
        ReviewCard.user_id == user_id).first()
    if not card:
        raise HTTPException(404, "Card not found")
    card.is_active = False
    db.commit()
    return {"message": "Card archived"}

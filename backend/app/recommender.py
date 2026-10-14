"""
Lightweight rule-based content recommendation engine for Edward Growth System.
Recommends learning content based on user expertise, difficulty matching,
freshness, and consumption history.
"""
from datetime import datetime, date
from typing import List
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import LearningContent, LearningRecord, UserProfile


class ContentRecommender:
    """Rule-based content recommendation engine"""

    def get_recommendations(self, db: Session, user_id: UUID, limit: int = 10) -> List[LearningContent]:
        """
        Recommend learning content based on:
        1. User's expertise levels (prioritize weaker domains)
        2. Difficulty matching (user level +/- 1)
        3. Freshness (prefer newer content)
        4. Not-yet-consumed content
        """
        # Get user profile for expertise levels
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile or not profile.expertise_levels:
            # Fallback: return newest active content
            return (
                db.query(LearningContent)
                .filter(LearningContent.is_active == True)
                .order_by(LearningContent.created_at.desc())
                .limit(limit)
                .all()
            )

        expertise = profile.expertise_levels  # {"AI": 0, "marketing": 0, ...}

        # Get content IDs already consumed by user
        consumed_ids = set(
            r[0]
            for r in db.query(LearningRecord.content_id)
            .filter(LearningRecord.user_id == user_id)
            .all()
        )

        # Query active content not yet consumed
        candidates = (
            db.query(LearningContent)
            .filter(
                LearningContent.is_active == True,
                ~LearningContent.content_id.in_(consumed_ids) if consumed_ids else True,
            )
            .all()
        )

        # Score each candidate
        scored = []
        for content in candidates:
            category = content.category or ""
            difficulty = content.difficulty_level or 1

            # Domain need: lower expertise => higher need (0-1 scale, inverted)
            expertise_level = expertise.get(category, 0)
            domain_need = 1.0 - (expertise_level / 5.0)

            # Difficulty match: prefer content within +/- 1 of user level
            diff_gap = abs(difficulty - (expertise_level + 1))
            difficulty_match = max(0.0, 1.0 - diff_gap * 0.3)

            # Freshness: newer content scores higher
            created = content.created_at or datetime(2024, 1, 1)
            age_days = max(1, (datetime.now() - created.replace(tzinfo=None)).days)
            freshness = 1.0 / (1.0 + age_days * 0.01)

            score = domain_need * 0.5 + difficulty_match * 0.3 + freshness * 0.2
            scored.append((score, content))

        # Sort by score descending, return top N
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

    def get_review_items(self, db: Session, user_id: UUID) -> List:
        """
        Get structured knowledge items due for spaced repetition review.
        Uses next_review_date <= today.
        """
        from app.models_extended import StructuredKnowledge

        today = date.today()
        items = (
            db.query(StructuredKnowledge)
            .filter(
                StructuredKnowledge.insight_id.isnot(None),
                StructuredKnowledge.next_review_date.isnot(None),
                StructuredKnowledge.next_review_date <= today,
                StructuredKnowledge.status.in_(["structured", "reviewed"]),
            )
            .order_by(StructuredKnowledge.next_review_date.asc())
            .all()
        )
        return items
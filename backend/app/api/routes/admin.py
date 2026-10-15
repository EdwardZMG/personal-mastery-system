"""Admin / system management API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models import (
    User, UserProfile, LearningContent, LearningRecord,
    DailyCheckin, Goal, HabitTracking, KnowledgeBase,
)
from app.models_extended import (
    KnowledgeInsight, StructuredKnowledge, KnowledgeApplication,
    ReviewSession, SpeechDraft, ChineseClassicsProgress,
)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


# Pydantic schemas
class SystemStatsResponse(BaseModel):
    """System-wide statistics"""
    total_users: int
    total_content: int
    total_insights: int
    total_structured_knowledge: int
    total_learning_records: int
    total_checkins: int
    total_goals: int
    total_habits: int
    total_applications: int
    total_reviews: int
    total_speeches: int
    total_classics_progress: int


class ContentCreate(BaseModel):
    """Request schema for creating learning content"""
    title: str = Field(..., description="Content title")
    description: Optional[str] = Field(None, description="Content description")
    content_type: str = Field(..., description="Type: article / video / audio / book / podcast")
    category: str = Field(..., description="Category: AI / marketing / chinese_classics / english / speaking / health")
    difficulty_level: int = Field(1, ge=1, le=5, description="Difficulty 1-5")
    estimated_minutes: int = Field(15, ge=1, description="Estimated reading/viewing time in minutes")
    source_url: Optional[str] = Field(None, description="Source URL")
    tags: Optional[List[str]] = Field(None, description="Tags for searchability")
    mask_dimension: Optional[str] = Field(None, description="MASK dimension: mindset / attitude / skills / knowledge")
    maslow_level: Optional[str] = Field(None, description="Maslow level: physiological / safety / belonging / esteem / self_actualization")


class ContentUpdate(BaseModel):
    """Request schema for updating learning content"""
    title: Optional[str] = None
    description: Optional[str] = None
    content_type: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[int] = Field(None, ge=1, le=5)
    estimated_minutes: Optional[int] = Field(None, ge=1)
    source_url: Optional[str] = None
    tags: Optional[List[str]] = None
    mask_dimension: Optional[str] = None
    maslow_level: Optional[str] = None
    is_active: Optional[bool] = None


class ContentResponse(BaseModel):
    """Response schema for learning content"""
    content_id: UUID
    title: str
    description: Optional[str]
    content_type: str
    category: str
    difficulty_level: int
    estimated_minutes: int
    source_url: Optional[str]
    tags: Optional[list]
    mask_dimension: Optional[str]
    maslow_level: Optional[str]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """
    Get system-wide statistics.

    Returns aggregate counts across all major entities in the system.
    """
    return SystemStatsResponse(
        total_users=db.query(User).count(),
        total_content=db.query(LearningContent).count(),
        total_insights=db.query(KnowledgeInsight).count(),
        total_structured_knowledge=db.query(StructuredKnowledge).count(),
        total_learning_records=db.query(LearningRecord).count(),
        total_checkins=db.query(DailyCheckin).count(),
        total_goals=db.query(Goal).count(),
        total_habits=db.query(HabitTracking).count(),
        total_applications=db.query(KnowledgeApplication).count(),
        total_reviews=db.query(ReviewSession).count(),
        total_speeches=db.query(SpeechDraft).count(),
        total_classics_progress=db.query(ChineseClassicsProgress).count(),
    )


@router.get("/content/", response_model=List[ContentResponse])
async def list_content(
    content_type: Optional[str] = None,
    is_active: Optional[bool] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """List learning content with optional filtering."""
    query = db.query(LearningContent)
    if content_type:
        query = query.filter(LearningContent.content_type == content_type)
    if is_active is not None:
        query = query.filter(LearningContent.is_active == is_active)
    return query.order_by(LearningContent.created_at.desc()).offset(offset).limit(limit).all()


@router.post("/content/", response_model=ContentResponse, status_code=status.HTTP_201_CREATED)
async def create_content(
    request: ContentCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """
    Create new learning content (admin operation).

    Learning content is the core curriculum of the growth system --
    articles, videos, books, podcasts, etc. that users study and track.
    """
    content = LearningContent(
        title=request.title,
        description=request.description,
        content_type=request.content_type,
        category=request.category,
        difficulty_level=request.difficulty_level,
        estimated_minutes=request.estimated_minutes,
        source_url=request.source_url,
        tags=request.tags or [],
        mask_dimension=request.mask_dimension,
        maslow_level=request.maslow_level,
        is_active=True,
    )
    db.add(content)
    db.commit()
    db.refresh(content)
    return content


@router.put("/content/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: UUID,
    request: ContentUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """
    Update existing learning content (admin operation).

    Accepts partial updates -- only provided fields are changed.
    """
    content = db.query(LearningContent).filter(LearningContent.content_id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Learning content not found")

    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(content, field, value)

    db.commit()
    db.refresh(content)
    return content


@router.delete("/content/{content_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_content(
    content_id: UUID,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id),
):
    """
    Delete learning content (admin operation).

    Performs a hard delete.  Associated learning records are NOT
    cascade-deleted (foreign key constraint should be handled at DB
    level).
    """
    content = db.query(LearningContent).filter(LearningContent.content_id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Learning content not found")

    db.delete(content)
    db.commit()

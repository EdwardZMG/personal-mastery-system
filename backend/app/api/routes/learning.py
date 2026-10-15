"""Learning content and activity tracking API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models import LearningContent, LearningRecord

router = APIRouter(prefix="/api/v1/learning", tags=["learning"])


# Pydantic schemas
class LearningContentResponse(BaseModel):
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

    class Config:
        from_attributes = True


class LearningContentDetailResponse(LearningContentResponse):
    """Extended response with all fields for content detail"""
    updated_at: Optional[datetime]


class LearningRecordCreate(BaseModel):
    """Request schema for logging a learning activity"""
    content_id: UUID
    status: str = Field("in_progress", description="Status: pending / in_progress / completed")
    duration_minutes: Optional[int] = Field(0, description="Time spent in minutes")
    progress_percent: Optional[int] = Field(0, ge=0, le=100, description="Progress percentage")
    feedback_score: Optional[int] = Field(None, ge=1, le=5, description="User rating 1-5")
    notes: Optional[str] = None


class LearningRecordResponse(BaseModel):
    """Response schema for learning records"""
    record_id: UUID
    user_id: UUID
    content_id: UUID
    status: str
    progress_percent: int
    duration_minutes: int
    feedback_score: Optional[int]
    notes: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/content", response_model=List[LearningContentResponse])
async def list_learning_content(
    category: Optional[str] = None,
    difficulty: Optional[int] = None,
    content_type: Optional[str] = None,
    mask_dimension: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    List available learning content with optional filters.

    Query parameters:
    - category: Filter by category (AI / marketing / chinese_classics / english / speaking / health)
    - difficulty: Filter by difficulty level (1-5)
    - content_type: Filter by type (article / video / audio / book / podcast)
    - mask_dimension: Filter by MASK dimension (mindset / attitude / skills / knowledge)
    - limit: Number of results (default 20, max 200)
    - offset: Pagination offset
    """
    query = db.query(LearningContent).filter(LearningContent.is_active == True)

    if category:
        query = query.filter(LearningContent.category == category)
    if difficulty is not None:
        query = query.filter(LearningContent.difficulty_level == difficulty)
    if content_type:
        query = query.filter(LearningContent.content_type == content_type)
    if mask_dimension:
        query = query.filter(LearningContent.mask_dimension == mask_dimension)

    contents = query.order_by(LearningContent.created_at.desc()).offset(offset).limit(limit).all()
    return contents


@router.get("/content/{content_id}", response_model=LearningContentDetailResponse)
async def get_learning_content(
    content_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Get detailed information about a specific learning content item."""
    content = db.query(LearningContent).filter(LearningContent.content_id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Learning content not found")
    return content


@router.post("/record", response_model=LearningRecordResponse, status_code=status.HTTP_201_CREATED)
async def log_learning_activity(
    request: LearningRecordCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Log a learning activity for a content item.

    Creates a new learning record or updates an existing in-progress record
    for the same content.  When status is set to 'completed', the
    completed_at timestamp is recorded automatically.
    """
    user_id_uuid = UUID(user_id)

    # Verify content exists
    content = db.query(LearningContent).filter(LearningContent.content_id == request.content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Learning content not found")

    # Check for existing in-progress record
    existing = (
        db.query(LearningRecord)
        .filter(
            LearningRecord.user_id == user_id_uuid,
            LearningRecord.content_id == request.content_id,
            LearningRecord.status == "in_progress",
        )
        .first()
    )

    if existing:
        # Update existing record
        existing.status = request.status
        existing.progress_percent = request.progress_percent
        existing.duration_minutes = (existing.duration_minutes or 0) + (request.duration_minutes or 0)
        existing.feedback_score = request.feedback_score or existing.feedback_score
        existing.notes = request.notes or existing.notes
        if request.status == "completed":
            existing.completed_at = datetime.now()
        db.commit()
        db.refresh(existing)
        return existing

    # Create new record
    record = LearningRecord(
        user_id=user_id_uuid,
        content_id=request.content_id,
        status=request.status,
        progress_percent=request.progress_percent,
        duration_minutes=request.duration_minutes or 0,
        feedback_score=request.feedback_score,
        notes=request.notes,
        started_at=datetime.now(),
        completed_at=datetime.now() if request.status == "completed" else None,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/records", response_model=List[LearningRecordResponse])
async def get_learning_history(
    status_filter: Optional[str] = None,
    content_id: Optional[UUID] = None,
    limit: int = 50,
    offset: int = 0,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Get the current user's learning history.

    Query parameters:
    - status_filter: Filter by status (pending / in_progress / completed)
    - content_id: Filter by specific content
    - limit: Number of results (default 50, max 200)
    - offset: Pagination offset
    """
    query = db.query(LearningRecord).filter(LearningRecord.user_id == UUID(user_id))

    if status_filter:
        query = query.filter(LearningRecord.status == status_filter)
    if content_id:
        query = query.filter(LearningRecord.content_id == content_id)

    records = query.order_by(LearningRecord.created_at.desc()).offset(offset).limit(limit).all()
    return records

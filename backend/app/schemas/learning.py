from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class LearningRecordCreate(BaseModel):
    content_id: UUID
    duration_minutes: Optional[int] = Field(None, ge=0)
    progress_percent: Optional[float] = Field(None, ge=0, le=100)
    feedback_score: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class LearningRecordResponse(BaseModel):
    record_id: UUID
    user_id: UUID
    content_id: UUID
    status: str
    progress_percent: float
    duration_minutes: int
    feedback_score: Optional[int] = None
    notes: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ContentResponse(BaseModel):
    content_id: UUID
    title: str
    description: Optional[str] = None
    content_type: str
    category: str
    difficulty_level: int
    estimated_minutes: int
    source_url: Optional[str] = None
    tags: Optional[list] = None
    mask_dimension: Optional[str] = None
    maslow_level: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime, date


class ClassicsProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    classic_name: str
    chapter_number: Optional[int] = None
    chapter_name: Optional[str] = None
    original_text: Optional[str] = None
    translation: Optional[str] = None
    interpretation: Optional[str] = None
    status: str
    completion_date: Optional[date] = None
    mastery_level: float
    review_count: int
    last_review_date: Optional[date] = None
    next_review_date: Optional[date] = None
    modern_applications: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ClassicsProgressUpdate(BaseModel):
    status: Optional[str] = None
    mastery_level: Optional[float] = None
    review_count: Optional[int] = None
    last_review_date: Optional[date] = None
    next_review_date: Optional[date] = None
    modern_applications: Optional[Dict[str, Any]] = None

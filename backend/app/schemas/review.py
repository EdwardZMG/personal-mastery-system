from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime


class ReviewTrigger(BaseModel):
    review_type: str = Field(..., pattern="^(daily|weekly|monthly|quarterly)$")
    scheduled_time: Optional[datetime] = None


class ReviewRespond(BaseModel):
    responses: Dict[str, Any] = Field(..., description="User answers to review questions")
    summary: Optional[str] = None


class ReviewResponse(BaseModel):
    id: UUID
    user_id: UUID
    review_type: str
    scheduled_time: Optional[datetime] = None
    completed_time: Optional[datetime] = None
    questions_json: Optional[Dict[str, Any]] = None
    responses: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

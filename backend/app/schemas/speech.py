from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime


class SpeechGenerate(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    template_type: str = Field(
        ...,
        pattern="^(ted_talk|toastmasters|elevator_pitch|storytelling)$",
    )
    estimated_duration: Optional[int] = Field(15, ge=1, le=60)
    related_insights: Optional[List[UUID]] = None
    related_knowledge: Optional[List[UUID]] = None
    language: Optional[str] = Field("zh", pattern="^(zh|en|bilingual)$")


class SpeechResponse(BaseModel):
    id: UUID
    user_id: UUID
    topic: str
    template_type: str
    estimated_duration: Optional[int] = None
    draft_json: Optional[Dict[str, Any]] = None
    full_speech: Optional[str] = None
    speaker_notes: Optional[str] = None
    related_insights: Optional[Dict[str, Any]] = None
    related_knowledge: Optional[Dict[str, Any]] = None
    status: str
    feedback_score: Optional[float] = None
    feedback_comments: Optional[str] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SpeechMaterialCreate(BaseModel):
    material_type: str = Field(
        ...,
        pattern="^(story|quote|case|data_point|analogy)$",
    )
    title: str = Field(..., max_length=300)
    content: str = Field(..., min_length=1)
    domain: Optional[str] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    source_url: Optional[str] = None

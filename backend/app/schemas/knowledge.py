from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime


class InsightCapture(BaseModel):
    content: str = Field(..., min_length=1)
    domain: Optional[str] = Field(None, pattern="^(AI|marketing|chinese_classics|english|speaking|general)$")
    intent: Optional[str] = Field(None, pattern="^(idea|question|note|task|reflection|insight)$")
    source: Optional[str] = Field("text", pattern="^(voice|text|manual)$")
    tags: Optional[List[str]] = []


class InsightResponse(BaseModel):
    id: UUID
    user_id: UUID
    content: str
    domain: Optional[str] = None
    intent: Optional[str] = None
    key_points: Optional[Dict[str, Any]] = None
    entities: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    source: Optional[str] = None
    language: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InsightListResponse(BaseModel):
    items: List[InsightResponse]
    total: int
    limit: int
    offset: int


class StructureRequest(BaseModel):
    insight_id: UUID
    title: Optional[str] = None
    domain: Optional[str] = None
    core_concept: Optional[str] = None
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    importance: Optional[int] = Field(None, ge=1, le=5)


class KnowledgeResponse(BaseModel):
    id: UUID
    insight_id: UUID
    title: Optional[str] = None
    domain: Optional[str] = None
    core_concept: Optional[str] = None
    explanation: Optional[str] = None
    examples: Optional[Dict[str, Any]] = None
    applications: Optional[Dict[str, Any]] = None
    connections: Optional[Dict[str, Any]] = None
    difficulty: Optional[int] = None
    importance: Optional[int] = None
    mastery_level: float
    review_count: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

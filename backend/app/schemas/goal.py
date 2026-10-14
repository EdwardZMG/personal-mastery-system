from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime, date


class GoalCreate(BaseModel):
    title: str = Field(..., max_length=300)
    description: Optional[str] = None
    category: Optional[str] = None
    specific: Optional[str] = None
    measurable: Optional[str] = None
    achievable: Optional[str] = None
    relevant: Optional[str] = None
    time_bound: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    priority: Optional[str] = Field("medium", pattern="^(low|medium|high)$")
    milestones: Optional[List[Dict[str, Any]]] = None


class GoalUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=300)
    description: Optional[str] = None
    progress_percent: Optional[float] = Field(None, ge=0, le=100)
    status: Optional[str] = Field(None, pattern="^(active|completed|archived)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    milestones: Optional[List[Dict[str, Any]]] = None


class GoalResponse(BaseModel):
    goal_id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    specific: Optional[str] = None
    measurable: Optional[str] = None
    achievable: Optional[str] = None
    relevant: Optional[str] = None
    time_bound: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    progress_percent: float
    status: str
    priority: Optional[str] = None
    milestones: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

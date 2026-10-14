from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime, date


class HabitCreate(BaseModel):
    name: str = Field(..., max_length=200)
    category: Optional[str] = None
    frequency: str = Field("daily", pattern="^(daily|weekly|monthly)$")
    target_value: Optional[float] = None
    description: Optional[str] = None


class HabitLogCreate(BaseModel):
    log_date: Optional[date] = None
    completed: bool = True
    actual_value: Optional[float] = None
    notes: Optional[str] = None


class HabitResponse(BaseModel):
    habit_id: UUID
    user_id: UUID
    name: str
    category: Optional[str] = None
    frequency: str
    target_value: Optional[float] = None
    current_streak: int
    longest_streak: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class HabitLogResponse(BaseModel):
    log_id: UUID
    habit_id: UUID
    log_date: date
    completed: bool
    actual_value: Optional[float] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

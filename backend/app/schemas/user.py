from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime


class UserCreate(BaseModel):
    open_id: str = Field(..., max_length=100)
    union_id: Optional[str] = Field(None, max_length=100)
    name: Optional[str] = Field(None, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    email: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=50)


class UserResponse(BaseModel):
    user_id: UUID
    open_id: str
    union_id: Optional[str] = None
    name: Optional[str] = None
    avatar_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    bio: Optional[str] = None
    expertise_levels: Optional[Dict[str, float]] = None
    learning_preferences: Optional[Dict[str, Any]] = None
    maslow_scores: Optional[Dict[str, float]] = None
    mask_scores: Optional[Dict[str, float]] = None
    seven_habits_scores: Optional[Dict[str, float]] = None
    current_level: Optional[str] = Field(None, pattern="^(beginner|intermediate|advanced|expert)$")


class UserProfileResponse(BaseModel):
    profile_id: UUID
    user_id: UUID
    bio: Optional[str] = None
    expertise_levels: Optional[Dict[str, float]] = None
    learning_preferences: Optional[Dict[str, Any]] = None
    maslow_scores: Optional[Dict[str, float]] = None
    mask_scores: Optional[Dict[str, float]] = None
    seven_habits_scores: Optional[Dict[str, float]] = None
    current_level: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

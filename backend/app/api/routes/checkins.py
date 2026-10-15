"""Daily check-in API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models import DailyCheckin

router = APIRouter(prefix="/api/v1/checkins", tags=["checkins"])


# Pydantic schemas
class CheckinCreate(BaseModel):
    """Request schema for creating a daily check-in"""
    mood: Optional[int] = Field(None, ge=1, le=5, description="Mood rating 1-5")
    energy_level: Optional[int] = Field(None, ge=1, le=5, description="Energy level 1-5")
    focus_areas: Optional[List[str]] = Field(None, description="Areas to focus on today")
    reflections: Optional[str] = Field(None, description="Daily reflections")
    achievements: Optional[str] = Field(None, description="Today's achievements")
    challenges: Optional[str] = Field(None, description="Challenges faced today")
    tomorrow_plan: Optional[str] = Field(None, description="Plan for tomorrow")


class CheckinResponse(BaseModel):
    """Response schema for daily check-in"""
    checkin_id: UUID
    user_id: UUID
    checkin_date: str
    mood: Optional[int]
    energy_level: Optional[int]
    focus_areas: Optional[list]
    reflections: Optional[str]
    achievements: Optional[str]
    challenges: Optional[str]
    tomorrow_plan: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.post("/", response_model=CheckinResponse, status_code=status.HTTP_201_CREATED)
async def create_checkin(
    request: CheckinCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Create a daily check-in.

    Records mood, energy level, reflections, achievements, challenges,
    and a plan for tomorrow.  Only one check-in per user per day is
    allowed; attempting to check in again returns a 400 error.
    """
    user_id_uuid = UUID(user_id)
    checkin_date = str(date.today())

    existing = (
        db.query(DailyCheckin)
        .filter(
            DailyCheckin.user_id == user_id_uuid,
            DailyCheckin.checkin_date == checkin_date,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already checked in today. Use PUT to update.")

    checkin = DailyCheckin(
        user_id=user_id_uuid,
        checkin_date=checkin_date,
        mood=request.mood,
        energy_level=request.energy_level,
        focus_areas=request.focus_areas or [],
        reflections=request.reflections,
        achievements=request.achievements,
        challenges=request.challenges,
        tomorrow_plan=request.tomorrow_plan,
    )
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin


@router.get("/", response_model=List[CheckinResponse])
async def list_checkins(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 30,
    offset: int = 0,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    List check-in history with optional date range filtering.

    Query parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - limit: Number of results (default 30, max 365)
    - offset: Pagination offset
    """
    query = db.query(DailyCheckin).filter(DailyCheckin.user_id == UUID(user_id))

    if start_date:
        query = query.filter(DailyCheckin.checkin_date >= start_date)
    if end_date:
        query = query.filter(DailyCheckin.checkin_date <= end_date)

    checkins = query.order_by(DailyCheckin.checkin_date.desc()).offset(offset).limit(limit).all()
    return checkins


@router.get("/today", response_model=CheckinResponse)
async def get_today_checkin(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Get today's check-in status.

    Returns the current user's check-in for today or 404 if not yet
    checked in.
    """
    checkin_date = str(date.today())

    checkin = (
        db.query(DailyCheckin)
        .filter(
            DailyCheckin.user_id == UUID(user_id),
            DailyCheckin.checkin_date == checkin_date,
        )
        .first()
    )
    if not checkin:
        raise HTTPException(status_code=404, detail="No check-in found for today")
    return checkin

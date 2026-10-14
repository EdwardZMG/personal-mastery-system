"""Habit tracking API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, date, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import HabitTracking, HabitLog

router = APIRouter(prefix="/api/v1/habits", tags=["habits"])


# Pydantic schemas
class HabitCreate(BaseModel):
    """Request schema for creating a habit"""
    name: str = Field(..., description="Habit name")
    category: Optional[str] = Field(None, description="Category (e.g. health, learning, mindfulness)")
    frequency: str = Field("daily", description="Frequency: daily / weekly / monthly")
    target_value: int = Field(1, ge=1, description="Target completions per period")


class HabitResponse(BaseModel):
    """Response schema for habits"""
    habit_id: UUID
    user_id: UUID
    name: str
    category: Optional[str]
    frequency: str
    target_value: int
    current_streak: int
    longest_streak: int
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class HabitLogCreate(BaseModel):
    """Request schema for logging habit completion"""
    log_date: Optional[str] = Field(None, description="Date (YYYY-MM-DD), defaults to today")
    completed: bool = Field(True, description="Whether the habit was completed")
    actual_value: int = Field(1, ge=0, description="Actual count / value achieved")
    notes: Optional[str] = None


class HabitLogResponse(BaseModel):
    """Response schema for habit logs"""
    log_id: UUID
    habit_id: UUID
    user_id: UUID
    log_date: str
    completed: bool
    actual_value: int
    notes: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class HabitStatsResponse(BaseModel):
    """Response schema for habit statistics"""
    habit_id: UUID
    name: str
    category: Optional[str]
    frequency: str
    current_streak: int
    longest_streak: int
    total_logs: int
    completed_count: int
    completion_rate: float
    last_7_days: List[dict]


@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
async def create_habit(
    request: HabitCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new habit to track.

    Habits can be tracked daily, weekly, or monthly.  The system
    automatically maintains streak counters.
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    habit = HabitTracking(
        user_id=user_id,
        name=request.name,
        category=request.category,
        frequency=request.frequency,
        target_value=request.target_value,
        current_streak=0,
        longest_streak=0,
        is_active=True,
    )
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.get("/", response_model=List[HabitResponse])
async def list_habits(
    category: Optional[str] = None,
    frequency: Optional[str] = None,
    active_only: bool = True,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    List tracked habits with optional filtering.

    Query parameters:
    - category: Filter by category
    - frequency: Filter by frequency (daily / weekly / monthly)
    - active_only: Only show active habits (default true)
    - limit: Number of results (default 50, max 200)
    - offset: Pagination offset
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    query = db.query(HabitTracking).filter(HabitTracking.user_id == user_id)

    if category:
        query = query.filter(HabitTracking.category == category)
    if frequency:
        query = query.filter(HabitTracking.frequency == frequency)
    if active_only:
        query = query.filter(HabitTracking.is_active == True)

    habits = query.order_by(HabitTracking.created_at.desc()).offset(offset).limit(limit).all()
    return habits


@router.post("/{habit_id}/log", response_model=HabitLogResponse, status_code=status.HTTP_201_CREATED)
async def log_habit_completion(
    habit_id: UUID,
    request: HabitLogCreate,
    db: Session = Depends(get_db),
):
    """
    Log a habit completion (or miss) for a given date.

    Automatically updates the habit's current streak and longest streak.
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")
    log_date = request.log_date or str(date.today())

    # Verify habit exists and belongs to user
    habit = (
        db.query(HabitTracking)
        .filter(HabitTracking.habit_id == habit_id, HabitTracking.user_id == user_id)
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    # Check for duplicate log
    existing = (
        db.query(HabitLog)
        .filter(HabitLog.habit_id == habit_id, HabitLog.log_date == log_date)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail=f"Habit already logged for {log_date}")

    # Create log entry
    log = HabitLog(
        habit_id=habit_id,
        user_id=user_id,
        log_date=log_date,
        completed=request.completed,
        actual_value=request.actual_value,
        notes=request.notes,
    )
    db.add(log)

    # Update streaks
    _update_streaks(habit, db)

    db.commit()
    db.refresh(log)
    return log


def _update_streaks(habit: HabitTracking, db: Session):
    """Recalculate current and longest streak for a habit."""
    logs = (
        db.query(HabitLog)
        .filter(HabitLog.habit_id == habit.habit_id, HabitLog.completed == True)
        .order_by(HabitLog.log_date.desc())
        .all()
    )

    if not logs:
        habit.current_streak = 0
        return

    # Calculate current streak from today backwards
    current_streak = 0
    check_date = date.today()
    log_dates = {datetime.fromisoformat(l.log_date + "T00:00:00").date() if isinstance(l.log_date, str) else l.log_date for l in logs}

    while check_date in log_dates:
        current_streak += 1
        check_date -= timedelta(days=1)

    habit.current_streak = current_streak
    if current_streak > (habit.longest_streak or 0):
        habit.longest_streak = current_streak


@router.get("/{habit_id}/logs", response_model=List[HabitLogResponse])
async def get_habit_logs(
    habit_id: UUID,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 60,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    Get habit completion logs with optional date range.

    Query parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - limit: Number of results (default 60, max 365)
    - offset: Pagination offset
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    # Verify habit ownership
    habit = (
        db.query(HabitTracking)
        .filter(HabitTracking.habit_id == habit_id, HabitTracking.user_id == user_id)
        .first()
    )
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    query = db.query(HabitLog).filter(HabitLog.habit_id == habit_id)

    if start_date:
        query = query.filter(HabitLog.log_date >= start_date)
    if end_date:
        query = query.filter(HabitLog.log_date <= end_date)

    logs = query.order_by(HabitLog.log_date.desc()).offset(offset).limit(limit).all()
    return logs


@router.get("/stats", response_model=List[HabitStatsResponse])
async def get_habit_stats(
    db: Session = Depends(get_db),
):
    """
    Get statistics for all active habits.

    Returns per-habit stats including streaks, completion rate, and a
    summary of the last 7 days.
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    habits = (
        db.query(HabitTracking)
        .filter(HabitTracking.user_id == user_id, HabitTracking.is_active == True)
        .all()
    )

    stats_list = []
    today = date.today()
    seven_days_ago = today - timedelta(days=6)

    for habit in habits:
        all_logs = db.query(HabitLog).filter(HabitLog.habit_id == habit.habit_id).all()
        total = len(all_logs)
        completed = sum(1 for l in all_logs if l.completed)
        rate = round(completed / total, 2) if total > 0 else 0.0

        # Last 7 days summary
        recent_logs = [
            l for l in all_logs
            if l.log_date >= str(seven_days_ago) and l.log_date <= str(today)
        ]
        last_7 = []
        for i in range(7):
            d = today - timedelta(days=6 - i)
            day_log = next((l for l in recent_logs if l.log_date == str(d)), None)
            last_7.append({
                "date": str(d),
                "completed": day_log.completed if day_log else False,
                "actual_value": day_log.actual_value if day_log else 0,
            })

        stats_list.append(HabitStatsResponse(
            habit_id=habit.habit_id,
            name=habit.name,
            category=habit.category,
            frequency=habit.frequency,
            current_streak=habit.current_streak,
            longest_streak=habit.longest_streak,
            total_logs=total,
            completed_count=completed,
            completion_rate=rate,
            last_7_days=last_7,
        ))

    return stats_list

"""Goal management API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models import Goal

router = APIRouter(prefix="/api/v1/goals", tags=["goals"])


# Pydantic schemas
class GoalCreate(BaseModel):
    """Request schema for creating a SMART goal"""
    title: str = Field(..., description="Goal title")
    description: Optional[str] = Field(None, description="Goal description")
    category: Optional[str] = Field(None, description="Category (e.g. career, health, learning)")
    specific: Optional[str] = Field(None, description="SMART: What exactly do you want to accomplish?")
    measurable: Optional[str] = Field(None, description="SMART: How will you measure progress?")
    achievable: Optional[str] = Field(None, description="SMART: How will you achieve this?")
    relevant: Optional[str] = Field(None, description="SMART: Why is this important?")
    time_bound: Optional[str] = Field(None, description="SMART: What is the deadline?")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date / deadline (YYYY-MM-DD)")
    priority: Optional[str] = Field("medium", description="Priority: low / medium / high")


class GoalUpdate(BaseModel):
    """Request schema for updating a goal"""
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    specific: Optional[str] = None
    measurable: Optional[str] = None
    achievable: Optional[str] = None
    relevant: Optional[str] = None
    time_bound: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    progress_percent: Optional[int] = Field(None, ge=0, le=100)
    status: Optional[str] = Field(None, description="Status: active / completed / archived")
    priority: Optional[str] = None


class GoalResponse(BaseModel):
    """Response schema for goals"""
    goal_id: UUID
    user_id: UUID
    title: str
    description: Optional[str]
    category: Optional[str]
    specific: Optional[str]
    measurable: Optional[str]
    achievable: Optional[str]
    relevant: Optional[str]
    time_bound: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    progress_percent: int
    status: str
    priority: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    request: GoalCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new SMART goal.

    SMART goals have five components:
    - **Specific**: Clearly defined outcome
    - **Measurable**: Quantifiable progress indicators
    - **Achievable**: Realistic action plan
    - **Relevant**: Aligned with broader objectives
    - **Time-bound**: Clear deadline
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    goal = Goal(
        user_id=user_id,
        title=request.title,
        description=request.description,
        category=request.category,
        specific=request.specific,
        measurable=request.measurable,
        achievable=request.achievable,
        relevant=request.relevant,
        time_bound=request.time_bound,
        start_date=request.start_date,
        end_date=request.end_date,
        priority=request.priority,
        progress_percent=0,
        status="active",
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.get("/", response_model=List[GoalResponse])
async def list_goals(
    status_filter: Optional[str] = None,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    List goals with optional filtering.

    Query parameters:
    - status_filter: Filter by status (active / completed / archived)
    - category: Filter by category
    - priority: Filter by priority (low / medium / high)
    - limit: Number of results (default 20, max 100)
    - offset: Pagination offset
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    query = db.query(Goal).filter(Goal.user_id == user_id)

    if status_filter:
        query = query.filter(Goal.status == status_filter)
    if category:
        query = query.filter(Goal.category == category)
    if priority:
        query = query.filter(Goal.priority == priority)

    goals = query.order_by(Goal.created_at.desc()).offset(offset).limit(limit).all()
    return goals


@router.get("/{goal_id}", response_model=GoalResponse)
async def get_goal(
    goal_id: UUID,
    db: Session = Depends(get_db),
):
    """Get a specific goal by ID."""
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    goal = (
        db.query(Goal)
        .filter(Goal.goal_id == goal_id, Goal.user_id == user_id)
        .first()
    )
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.put("/{goal_id}", response_model=GoalResponse)
async def update_goal(
    goal_id: UUID,
    request: GoalUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing goal.

    Accepts partial updates -- only provided fields are changed.
    When progress_percent reaches 100 the status is automatically set
    to 'completed'.
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    goal = (
        db.query(Goal)
        .filter(Goal.goal_id == goal_id, Goal.user_id == user_id)
        .first()
    )
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    update_data = request.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(goal, field, value)

    # Auto-complete when progress hits 100%
    if goal.progress_percent >= 100:
        goal.status = "completed"

    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_goal(
    goal_id: UUID,
    db: Session = Depends(get_db),
):
    """Delete a goal by ID."""
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    goal = (
        db.query(Goal)
        .filter(Goal.goal_id == goal_id, Goal.user_id == user_id)
        .first()
    )
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    db.delete(goal)
    db.commit()

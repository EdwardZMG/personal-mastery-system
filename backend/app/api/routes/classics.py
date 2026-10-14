"""Chinese classics learning progress API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models_extended import ChineseClassicsProgress

router = APIRouter(prefix="/api/v1/classics", tags=["classics"])

# Supported classics
CLASSICS_LIST = [
    "道德经", "金刚经", "坛经", "资治通鉴", "易经", "孙子兵法",
    "论语", "孟子", "大学", "中庸", "庄子", "史记",
]


# Pydantic schemas
class ClassicsProgressResponse(BaseModel):
    """Response schema for a single classics progress entry"""
    id: UUID
    user_id: UUID
    classic_name: str
    chapter_number: Optional[int]
    chapter_name: Optional[str]
    original_text: Optional[str]
    translation: Optional[str]
    interpretation: Optional[str]
    status: str
    completion_date: Optional[str]
    mastery_level: float
    review_count: int
    last_review_date: Optional[str]
    next_review_date: Optional[str]
    modern_applications: Optional[dict]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


class ClassicsProgressUpdate(BaseModel):
    """Request schema for updating classics learning progress"""
    classic_name: str = Field(..., description="Name of the classic")
    chapter_number: Optional[int] = Field(None, description="Chapter / verse number")
    chapter_name: Optional[str] = Field(None, description="Chapter name")
    original_text: Optional[str] = Field(None, description="Original classical Chinese text")
    translation: Optional[str] = Field(None, description="Modern Chinese translation")
    interpretation: Optional[str] = Field(None, description="Personal interpretation / notes")
    status: Optional[str] = Field(None, description="Status: not_started / reading / completed / reviewed")
    mastery_level: Optional[float] = Field(None, ge=0.0, le=1.0, description="Mastery level 0-1")
    modern_applications: Optional[dict] = Field(None, description="Modern-day applications of the teaching")


class ClassicSummaryResponse(BaseModel):
    """Summary of progress for a single classic"""
    classic_name: str
    total_chapters: int
    completed_chapters: int
    avg_mastery: float
    status: str
    last_studied: Optional[datetime]


class ClassicsOverallStats(BaseModel):
    """Overall statistics across all classics"""
    total_classics: int
    classics_started: int
    classics_completed: int
    total_chapters_studied: int
    overall_mastery: float
    by_classic: List[ClassicSummaryResponse]
    recent_activity: Optional[datetime]


@router.get("/progress", response_model=List[ClassicsProgressResponse])
async def get_all_classics_progress(
    status_filter: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db),
):
    """
    Get learning progress for all Chinese classics.

    Query parameters:
    - status_filter: Filter by status (not_started / reading / completed / reviewed)
    - limit: Number of results (default 100, max 500)
    - offset: Pagination offset
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    query = db.query(ChineseClassicsProgress).filter(
        ChineseClassicsProgress.user_id == user_id
    )

    if status_filter:
        query = query.filter(ChineseClassicsProgress.status == status_filter)

    records = query.order_by(ChineseClassicsProgress.classic_name, ChineseClassicsProgress.chapter_number).offset(offset).limit(limit).all()
    return records


@router.get("/{classic_name}", response_model=List[ClassicsProgressResponse])
async def get_classic_progress(
    classic_name: str,
    db: Session = Depends(get_db),
):
    """
    Get progress for a specific classic.

    Returns all chapter-level progress records for the given classic.
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    records = (
        db.query(ChineseClassicsProgress)
        .filter(
            ChineseClassicsProgress.user_id == user_id,
            ChineseClassicsProgress.classic_name == classic_name,
        )
        .order_by(ChineseClassicsProgress.chapter_number)
        .all()
    )

    if not records:
        raise HTTPException(status_code=404, detail=f"No progress found for '{classic_name}'")
    return records


@router.put("/progress", response_model=ClassicsProgressResponse)
async def update_classics_progress(
    request: ClassicsProgressUpdate,
    db: Session = Depends(get_db),
):
    """
    Create or update learning progress for a classic chapter.

    Uses upsert logic: if a record exists for the same user + classic +
    chapter_number it is updated; otherwise a new record is created.
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    # Look for existing record
    existing = None
    if request.chapter_number is not None:
        existing = (
            db.query(ChineseClassicsProgress)
            .filter(
                ChineseClassicsProgress.user_id == user_id,
                ChineseClassicsProgress.classic_name == request.classic_name,
                ChineseClassicsProgress.chapter_number == request.chapter_number,
            )
            .first()
        )

    if existing:
        # Update existing record
        if request.chapter_name is not None:
            existing.chapter_name = request.chapter_name
        if request.original_text is not None:
            existing.original_text = request.original_text
        if request.translation is not None:
            existing.translation = request.translation
        if request.interpretation is not None:
            existing.interpretation = request.interpretation
        if request.status is not None:
            existing.status = request.status
        if request.mastery_level is not None:
            existing.mastery_level = request.mastery_level
        if request.modern_applications is not None:
            existing.modern_applications = request.modern_applications

        # Auto-update review tracking
        existing.review_count = (existing.review_count or 0) + 1
        existing.last_review_date = datetime.now().date()

        # Auto-complete
        if request.status == "completed" and not existing.completed_at:
            existing.completed_at = datetime.now()
            existing.completion_date = datetime.now().date()

        db.commit()
        db.refresh(existing)
        return existing

    # Create new record
    record = ChineseClassicsProgress(
        user_id=user_id,
        classic_name=request.classic_name,
        chapter_number=request.chapter_number,
        chapter_name=request.chapter_name,
        original_text=request.original_text,
        translation=request.translation,
        interpretation=request.interpretation,
        status=request.status or "reading",
        mastery_level=request.mastery_level or 0.0,
        modern_applications=request.modern_applications,
        review_count=1,
        last_review_date=datetime.now().date(),
        started_at=datetime.now(),
    )

    if record.status == "completed":
        record.completed_at = datetime.now()
        record.completion_date = datetime.now().date()

    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/stats", response_model=ClassicsOverallStats)
async def get_classics_stats(
    db: Session = Depends(get_db),
):
    """
    Get overall statistics for Chinese classics learning.

    Returns a summary across all classics including total chapters
    studied, average mastery, and per-classic breakdowns.
    """
    # TODO: Replace with real JWT auth dependency
    user_id = UUID("00000000-0000-0000-0000-000000000001")

    all_records = (
        db.query(ChineseClassicsProgress)
        .filter(ChineseClassicsProgress.user_id == user_id)
        .all()
    )

    # Group by classic name
    by_classic: dict = {}
    for rec in all_records:
        name = rec.classic_name
        if name not in by_classic:
            by_classic[name] = []
        by_classic[name].append(rec)

    summaries = []
    total_chapters = 0
    total_mastery = 0.0

    for name, records in by_classic.items():
        completed = sum(1 for r in records if r.status in ("completed", "reviewed"))
        avg_mastery = sum(r.mastery_level or 0 for r in records) / len(records) if records else 0.0
        last_studied = max((r.updated_at for r in records if r.updated_at), default=None)

        summaries.append(ClassicSummaryResponse(
            classic_name=name,
            total_chapters=len(records),
            completed_chapters=completed,
            avg_mastery=round(avg_mastery, 3),
            status="completed" if completed == len(records) and len(records) > 0 else "in_progress",
            last_studied=last_studied,
        ))

        total_chapters += len(records)
        total_mastery += sum(r.mastery_level or 0 for r in records)

    classics_started = len(by_classic)
    classics_completed = sum(1 for s in summaries if s.status == "completed")
    overall_mastery = round(total_mastery / total_chapters, 3) if total_chapters > 0 else 0.0
    recent = max((r.updated_at for r in all_records if r.updated_at), default=None)

    return ClassicsOverallStats(
        total_classics=len(CLASSICS_LIST),
        classics_started=classics_started,
        classics_completed=classics_completed,
        total_chapters_studied=total_chapters,
        overall_mastery=overall_mastery,
        by_classic=summaries,
        recent_activity=recent,
    )

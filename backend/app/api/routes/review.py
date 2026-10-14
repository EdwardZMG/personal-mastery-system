"""Review session management API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models_extended import ReviewSession, ReviewSummary, StructuredKnowledge
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/review", tags=["review"])


# Pydantic schemas
class ReviewTriggerRequest(BaseModel):
    """Request schema for triggering a review session"""
    review_type: str = Field(..., description="Type: daily/weekly/monthly/quarterly")
    scheduled_time: Optional[datetime] = None


class ReviewResponse(BaseModel):
    """Response schema for review sessions"""
    id: UUID
    user_id: UUID
    review_type: str
    scheduled_time: Optional[datetime]
    completed_time: Optional[datetime]
    insights_json: Optional[dict]
    questions_json: Optional[dict]
    responses: Optional[str]
    summary: Optional[str]
    new_insights_json: Optional[dict]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewSubmitRequest(BaseModel):
    """Request schema for submitting review responses"""
    responses: str = Field(..., description="User's review responses in text format")
    new_insights: Optional[dict] = Field(None, description="New insights discovered during review")


class ReviewSummaryCreate(BaseModel):
    """Request schema for creating review summaries"""
    session_id: UUID
    key_learnings: Optional[List[str]] = None
    action_items: Optional[List[str]] = None
    summary: str


class ReviewSummaryResponse(BaseModel):
    """Response schema for review summaries"""
    id: UUID
    session_id: UUID
    user_id: UUID
    summary: str
    key_learnings: Optional[list]
    action_items: Optional[list]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/trigger", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def trigger_review(
    request: ReviewTriggerRequest,
    db: Session = Depends(get_db)
):
    """
    Trigger a new review session (daily/weekly/monthly/quarterly)
    
    This endpoint creates a review session with appropriate questions and insights
    based on the review type:
    
    - **Daily**: Focus on today's learnings, habit check-in, quick reflection
    - **Weekly**: Summarize week's progress, identify patterns, plan next week
    - **Monthly**: Deep dive into monthly goals, SMART assessment, MASK evaluation
    - **Quarterly**: Strategic review, long-term progress, course correction
    
    The review session includes pre-populated questions and relevant knowledge items
    for reflection.
    """
    # Generate appropriate questions based on review type
    questions = generate_review_questions(request.review_type)
    
    # Gather relevant insights for this review period
    insights = gather_review_insights(request.review_type, db)
    
    # Create review session
    review = ReviewSession(
        user_id=UUID("00000000-0000-0000-0000-000000000001"),  # TODO: Get from JWT auth
        review_type=request.review_type,
        scheduled_time=request.scheduled_time or datetime.now(),
        insights_json=insights,
        questions_json=questions,
        status="pending"
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    return review


def generate_review_questions(review_type: str) -> dict:
    """Generate review questions based on type"""
    questions = {
        "daily": {
            "q1": "今天学习了什么新知识？",
            "q2": "有什么启发或感悟？",
            "q3": "如何应用到实际中？",
            "q4": "今天的习惯打卡完成了吗？",
            "q5": "明天的学习计划是什么？"
        },
        "weekly": {
            "q1": "本周完成了哪些学习目标？",
            "q2": "遇到了什么挑战？如何克服的？",
            "q3": "MASK四个维度有哪些提升？",
            "q4": "知识掌握程度如何变化？",
            "q5": "下周的重点是什么？",
            "q6": "需要调整学习策略吗？"
        },
        "monthly": {
            "q1": "本月SMART目标完成度如何？",
            "q2": "各领域的专精等级有何进步？",
            "q3": "积累了多少条知识和洞察？",
            "q4": "有多少次实际应用？效果如何？",
            "q5": "马斯洛需求层次的满足情况？",
            "q6": "下月的关键里程碑是什么？"
        },
        "quarterly": {
            "q1": "季度大目标进展如何？",
            "q2": "能力矩阵有哪些显著变化？",
            "q3": "知识体系的完整性如何？",
            "q4": "实际应用场景和成果有哪些？",
            "q5": "长期愿景的推进情况？",
            "q6": "战略方向需要调整吗？"
        }
    }
    return questions.get(review_type, questions["daily"])


def gather_review_insights(review_type: str, db: Session) -> dict:
    """Gather relevant insights for the review period"""
    from datetime import timedelta
    
    # Calculate time range based on review type
    now = datetime.now()
    if review_type == "daily":
        start_date = now - timedelta(days=1)
    elif review_type == "weekly":
        start_date = now - timedelta(weeks=1)
    elif review_type == "monthly":
        start_date = now - timedelta(days=30)
    elif review_type == "quarterly":
        start_date = now - timedelta(days=90)
    else:
        start_date = now - timedelta(days=1)
    
    # Query structured knowledge created/updated in this period
    recent_knowledge = db.query(StructuredKnowledge).filter(
        StructuredKnowledge.last_reviewed >= start_date
    ).all()
    
    return {
        "total_items": len(recent_knowledge),
        "by_domain": {},  # TODO: Aggregate by domain
        "recent_titles": [k.title for k in recent_knowledge[:10]]
    }


@router.post("/{review_id}/respond", response_model=ReviewResponse)
async def submit_review_response(
    review_id: UUID,
    request: ReviewSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Submit responses to a review session
    
    This endpoint records the user's answers to review questions and can:
    - Update mastery levels based on self-reflection
    - Extract new insights from responses
    - Schedule follow-up reviews
    - Generate review summaries
    
    The responses are analyzed (via NLP module) to identify:
    - Knowledge gaps
    - Mastery improvements
    - Action items
    - New learning opportunities
    """
    review = db.query(ReviewSession).filter(ReviewSession.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review session not found")
    
    # Update review with responses
    review.responses = request.responses
    review.new_insights_json = request.new_insights or {}
    review.completed_time = datetime.now()
    review.status = "completed"
    
    # TODO: Run NLP analysis on responses to extract insights
    # TODO: Update mastery levels in StructuredKnowledge
    # TODO: Schedule next review if needed
    
    db.commit()
    db.refresh(review)
    
    return review


@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review_session(
    review_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific review session by ID"""
    review = db.query(ReviewSession).filter(ReviewSession.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review session not found")
    return review


@router.get("/", response_model=List[ReviewResponse])
async def list_reviews(
    review_type: Optional[str] = None,
    status_filter: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List review sessions with optional filtering
    
    Query parameters:
    - review_type: Filter by type (daily/weekly/monthly/quarterly)
    - status: Filter by status (pending/completed/missed)
    - limit: Number of results (default 20, max 100)
    - offset: Pagination offset
    """
    query = db.query(ReviewSession)
    
    if review_type:
        query = query.filter(ReviewSession.review_type == review_type)
    if status_filter:
        query = query.filter(ReviewSession.status == status_filter)
    
    reviews = query.order_by(ReviewSession.scheduled_time.desc()).offset(offset).limit(limit).all()
    return reviews


@router.post("/summary", response_model=ReviewSummaryResponse, status_code=status.HTTP_201_CREATED)
async def create_review_summary(
    request: ReviewSummaryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a summary for a completed review session
    
    This endpoint generates a structured summary capturing:
    - Key learnings from the review period
    - Mastery level improvements across domains
    - Action items for the next period
    - Overall reflection and insights
    
    The summary serves as a historical record and can be referenced
    in future reviews or speech generation.
    """
    # Verify review exists and is completed
    review = db.query(ReviewSession).filter(ReviewSession.id == request.session_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review session not found")
    if review.status != "completed":
        raise HTTPException(status_code=400, detail="Review must be completed before creating summary")
    
    # Create summary
    summary = ReviewSummary(
        session_id=request.session_id,
        user_id=review.user_id,
        summary=request.summary,
        key_learnings=request.key_learnings,
        action_items=request.action_items
    )
    
    db.add(summary)
    db.commit()
    db.refresh(summary)
    
    return summary

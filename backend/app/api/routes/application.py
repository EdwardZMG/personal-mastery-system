"""Knowledge application tracking API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models_extended import KnowledgeApplication, ApplicationStats, StructuredKnowledge
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/application", tags=["application"])


# Pydantic schemas
class ApplicationLogRequest(BaseModel):
    """Request schema for logging knowledge applications"""
    knowledge_id: UUID
    scenario: str = Field(..., description="Real-world application scenario description")
    outcome: Optional[str] = Field(None, description="Result/outcome of the application")
    lessons_learned: Optional[str] = Field(None, description="Key lessons from this application")
    effectiveness: Optional[float] = Field(None, ge=0, le=5, description="Effectiveness rating (0-5)")
    confidence_level: Optional[float] = Field(None, ge=0, le=1, description="Confidence level in applying this knowledge (0-1)")
    context_tags: Optional[List[str]] = Field(None, description="Contextual tags for categorization")
    stakeholders: Optional[List[str]] = Field(None, description="People involved in this application")
    follow_up_needed: Optional[bool] = Field(False, description="Whether follow-up action is needed")


class ApplicationResponse(BaseModel):
    """Response schema for knowledge applications"""
    id: UUID
    user_id: UUID
    knowledge_id: UUID
    scenario: str
    outcome: Optional[str]
    lessons_learned: Optional[str]
    effectiveness: Optional[float]
    confidence_level: Optional[float]
    context_tags: Optional[list]
    stakeholders: Optional[list]
    follow_up_needed: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ApplicationStatsResponse(BaseModel):
    """Response schema for application statistics"""
    id: UUID
    user_id: UUID
    total_applications: int
    successful_applications: int
    success_rate: float
    applications_by_domain: Optional[dict]
    last_application_date: Optional[datetime]
    applications_last_30_days: int
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.post("/log", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def log_application(
    request: ApplicationLogRequest,
    db: Session = Depends(get_db)
):
    """
    Log a real-world application of structured knowledge
    
    This endpoint tracks when and how you apply learned knowledge in practice:
    
    - **Scenario**: Describe the situation where you applied the knowledge
    - **Outcome**: What happened as a result?
    - **Lessons Learned**: What did you discover or improve?
    - **Effectiveness**: Rate the effectiveness (0-5 stars)
    - **Confidence**: How confident were you in applying it? (0-1)
    - **Context Tags**: Categorize the application context
    - **Stakeholders**: Who was involved?
    
    Each application:
    1. Updates the mastery level of the associated knowledge
    2. Increments application statistics
    3. Provides data for future recommendations
    4. Builds your practical knowledge portfolio
    
    The system uses application history to:
    - Identify high-value knowledge areas
    - Suggest knowledge that needs more practice
    - Generate success stories for speeches
    - Track real-world impact of learning
    """
    # Verify knowledge exists
    knowledge = db.query(StructuredKnowledge).filter(StructuredKnowledge.id == request.knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Structured knowledge not found")
    
    # Create application record
    application = KnowledgeApplication(
        user_id=UUID("00000000-0000-0000-0000-000000000001"),  # TODO: Get from JWT auth
        knowledge_id=request.knowledge_id,
        scenario=request.scenario,
        outcome=request.outcome,
        lessons_learned=request.lessons_learned,
        effectiveness=request.effectiveness,
        confidence_level=request.confidence_level,
        context_tags=request.context_tags or [],
        stakeholders=request.stakeholders or [],
        follow_up_needed=request.follow_up_needed
    )
    
    db.add(application)
    
    # Update application stats
    update_application_stats(application.user_id, db)
    
    # Update knowledge mastery level based on application
    if request.effectiveness and request.confidence_level:
        # Calculate mastery boost: effectiveness * confidence * decay factor
        mastery_boost = (request.effectiveness / 5.0) * request.confidence_level * 0.1
        current_mastery = knowledge.mastery_level or 0.5
        new_mastery = min(current_mastery + mastery_boost, 1.0)
        
        knowledge.mastery_level = new_mastery
        knowledge.last_reviewed = datetime.now()
        knowledge.review_count = (knowledge.review_count or 1) + 1
    
    db.commit()
    db.refresh(application)
    
    return application


def update_application_stats(user_id: UUID, db: Session):
    """Update or create application statistics for a user"""
    # Query all applications for this user
    applications = db.query(KnowledgeApplication).filter(
        KnowledgeApplication.user_id == user_id
    ).all()
    
    if not applications:
        return
    
    # Calculate statistics
    total = len(applications)
    successful = sum(1 for app in applications if app.effectiveness and app.effectiveness >= 3)
    success_rate = successful / total if total > 0 else 0
    
    # Aggregate by domain
    by_domain = {}
    for app in applications:
        # Get domain from associated knowledge
        knowledge = db.query(StructuredKnowledge).filter(
            StructuredKnowledge.id == app.knowledge_id
        ).first()
        if knowledge:
            domain = knowledge.domain
            if domain not in by_domain:
                by_domain[domain] = {"total": 0, "successful": 0}
            by_domain[domain]["total"] += 1
            if app.effectiveness and app.effectiveness >= 3:
                by_domain[domain]["successful"] += 1
    
    # Calculate success rate per domain
    for domain in by_domain:
        total_domain = by_domain[domain]["total"]
        successful_domain = by_domain[domain]["successful"]
        by_domain[domain]["success_rate"] = successful_domain / total_domain if total_domain > 0 else 0
    
    # Calculate applications in last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_count = sum(1 for app in applications if app.created_at and app.created_at >= thirty_days_ago)
    
    # Get most recent application date
    most_recent = max((app.created_at for app in applications if app.created_at), default=None)
    
    # Update or create stats record
    stats = db.query(ApplicationStats).filter(ApplicationStats.user_id == user_id).first()
    if stats:
        stats.total_applications = total
        stats.successful_applications = successful
        stats.success_rate = success_rate
        stats.applications_by_domain = by_domain
        stats.last_application_date = most_recent.date() if most_recent else None
        stats.applications_last_30_days = recent_count
    else:
        stats = ApplicationStats(
            user_id=user_id,
            total_applications=total,
            successful_applications=successful,
            success_rate=success_rate,
            applications_by_domain=by_domain,
            last_application_date=most_recent.date() if most_recent else None,
            applications_last_30_days=recent_count
        )
        db.add(stats)


@router.get("/stats", response_model=ApplicationStatsResponse)
async def get_application_stats(
    db: Session = Depends(get_db)
):
    """
    Get comprehensive application statistics
    
    Returns detailed statistics about knowledge applications including:
    - Total applications logged
    - Success rate and average effectiveness
    - Breakdown by knowledge domain
    - Recent activity timeline
    
    Use this data to:
    - Track your practical progress
    - Identify strong/weak areas
    - Measure real-world impact of learning
    - Generate progress reports for reviews
    """
    user_id = UUID("00000000-0000-0000-0000-000000000001")  # TODO: Get from JWT auth
    
    stats = db.query(ApplicationStats).filter(ApplicationStats.user_id == user_id).first()
    if not stats:
        # Return empty stats if no applications yet
        return ApplicationStatsResponse(
            id=UUID("00000000-0000-0000-0000-000000000000"),
            user_id=user_id,
            total_applications=0,
            successful_applications=0,
            success_rate=0.0,
            applications_by_domain={},
            applications_last_30_days=0,
            updated_at=datetime.now()
        )
    
    return stats


@router.get("/", response_model=List[ApplicationResponse])
async def list_applications(
    knowledge_id: Optional[UUID] = None,
    effectiveness_min: Optional[float] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List knowledge applications with optional filtering
    
    Query parameters:
    - knowledge_id: Filter by specific knowledge item
    - effectiveness_min: Filter by minimum effectiveness rating (0-5)
    - limit: Number of results (default 50, max 200)
    - offset: Pagination offset
    """
    query = db.query(KnowledgeApplication)
    
    if knowledge_id:
        query = query.filter(KnowledgeApplication.knowledge_id == knowledge_id)
    if effectiveness_min is not None:
        query = query.filter(KnowledgeApplication.effectiveness >= effectiveness_min)
    
    applications = query.order_by(KnowledgeApplication.created_at.desc()).offset(offset).limit(limit).all()
    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(
    application_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific application record by ID"""
    application = db.query(KnowledgeApplication).filter(KnowledgeApplication.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application record not found")
    return application

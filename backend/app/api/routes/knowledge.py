"""Knowledge capture and structuring API endpoints"""
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models_extended import KnowledgeInsight, StructuredKnowledge
from app.nlp import NLPPipeline
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/knowledge", tags=["knowledge"])

# Initialize NLP pipeline
nlp_pipeline = NLPPipeline()


# Pydantic schemas
class InsightCaptureRequest(BaseModel):
    """Request schema for capturing knowledge insights"""
    content: str = Field(..., description="Raw insight content (voice/text)")
    domain: Optional[str] = Field(None, description="Domain category: AI/marketing/chinese_classics/english/speaking/general")
    source: Optional[str] = Field(None, description="Source: voice_input/text_input/crawler/manual")
    language: Optional[str] = Field("zh", description="Language code: zh/en")


class InsightResponse(BaseModel):
    """Response schema for knowledge insights"""
    id: UUID
    user_id: UUID
    content: str
    domain: Optional[str]
    intent: Optional[str]
    key_points: Optional[dict]
    entities: Optional[dict]
    connections: Optional[dict]
    tags: Optional[list]
    source: Optional[str]
    language: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class StructuredKnowledgeRequest(BaseModel):
    """Request schema for converting insights to structured knowledge"""
    insight_id: UUID
    title: str
    core_concept: str
    explanation: str
    examples: Optional[list] = None
    applications: Optional[list] = None
    difficulty: int = Field(3, ge=1, le=5)
    importance: int = Field(3, ge=1, le=5)


class StructuredKnowledgeResponse(BaseModel):
    """Response schema for structured knowledge"""
    id: UUID
    insight_id: UUID
    title: str
    domain: str
    core_concept: Optional[str]
    explanation: Optional[str]
    examples: Optional[list]
    applications: Optional[list]
    connections: Optional[dict]
    difficulty: Optional[int]
    importance: Optional[int]
    mastery_level: float
    last_reviewed: Optional[datetime]
    review_count: int
    next_review_date: Optional[datetime]
    status: str

    class Config:
        from_attributes = True


@router.post("/capture", response_model=InsightResponse, status_code=status.HTTP_201_CREATED)
async def capture_insight(
    request: InsightCaptureRequest,
    db: Session = Depends(get_db)
):
    """
    Capture a new knowledge insight from voice or text input
    
    This endpoint accepts raw content and performs intelligent classification:
    - Intent detection (idea/question/note/task/reflection/insight)
    - Domain classification (AI/marketing/chinese_classics/english/speaking/general)
    - Entity extraction (people, organizations, concepts, dates)
    - Tag generation for searchability
    
    The insight is stored with status='raw' for later processing.
    """
    # Run NLP pipeline for automatic classification
    nlp_results = nlp_pipeline.process(request.content, request.language)
    
    # Use NLP results, but allow manual override if domain is provided
    domain = request.domain or nlp_results['domain']
    intent = nlp_results['intent']
    
    # Create insight record with NLP-enriched data
    insight = KnowledgeInsight(
        user_id=UUID("00000000-0000-0000-0000-000000000001"),  # TODO: Get from JWT auth
        content=request.content,
        domain=domain,
        intent=intent,
        key_points={
            "word_count": nlp_results['word_count'],
            "intent_confidence": nlp_results['intent_confidence'],
            "domain_confidence": nlp_results['domain_confidence']
        },
        entities=nlp_results['entities'],
        connections={},  # TODO: Find related knowledge via graph
        tags=nlp_results['tags'],
        source=request.source or "manual",
        language=request.language
    )
    
    db.add(insight)
    db.commit()
    db.refresh(insight)
    
    return insight


@router.get("/{insight_id}", response_model=InsightResponse)
async def get_insight(
    insight_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific knowledge insight by ID"""
    insight = db.query(KnowledgeInsight).filter(KnowledgeInsight.id == insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    return insight


@router.get("/", response_model=List[InsightResponse])
async def list_insights(
    domain: Optional[str] = None,
    intent: Optional[str] = None,
    status_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List knowledge insights with optional filtering
    
    Query parameters:
    - domain: Filter by domain (AI/marketing/chinese_classics/english/speaking/general)
    - intent: Filter by intent type (idea/question/note/task/reflection/insight)
    - status: Filter by status (raw/structured/archived)
    - limit: Number of results (default 50, max 200)
    - offset: Pagination offset
    """
    query = db.query(KnowledgeInsight)
    
    if domain:
        query = query.filter(KnowledgeInsight.domain == domain)
    if intent:
        query = query.filter(KnowledgeInsight.intent == intent)
    if status_filter:
        query = query.filter(KnowledgeInsight.status == status_filter)
    
    insights = query.order_by(KnowledgeInsight.created_at.desc()).offset(offset).limit(limit).all()
    return insights


@router.post("/structure", response_model=StructuredKnowledgeResponse, status_code=status.HTTP_201_CREATED)
async def structure_knowledge(
    request: StructuredKnowledgeRequest,
    db: Session = Depends(get_db)
):
    """
    Convert a raw insight into structured knowledge
    
    This endpoint transforms unstructured insights into organized knowledge units with:
    - Clear title and core concept
    - Detailed explanation
    - Practical examples
    - Application scenarios
    - Difficulty and importance ratings
    
    The structured knowledge is ready for review scheduling and mastery tracking.
    """
    # Verify insight exists
    insight = db.query(KnowledgeInsight).filter(KnowledgeInsight.id == request.insight_id).first()
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    
    # Create structured knowledge
    structured = StructuredKnowledge(
        insight_id=request.insight_id,
        title=request.title,
        domain=insight.domain,
        core_concept=request.core_concept,
        explanation=request.explanation,
        examples=request.examples or [],
        applications=request.applications or [],
        connections={},  # TODO: Build connections via knowledge graph
        difficulty=request.difficulty,
        importance=request.importance,
        mastery_level=0.50,  # Start at 50% mastery
        status="structured"
    )
    
    # Update insight status
    insight.status = "structured"
    
    db.add(structured)
    db.commit()
    db.refresh(structured)
    
    return structured


@router.get("/knowledge/{knowledge_id}", response_model=StructuredKnowledgeResponse)
async def get_structured_knowledge(
    knowledge_id: UUID,
    db: Session = Depends(get_db)
):
    """Get structured knowledge by ID"""
    knowledge = db.query(StructuredKnowledge).filter(StructuredKnowledge.id == knowledge_id).first()
    if not knowledge:
        raise HTTPException(status_code=404, detail="Structured knowledge not found")
    return knowledge

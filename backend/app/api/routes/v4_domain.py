"""Domain, Competency, Framework API — V4"""
from typing import List, Optional, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.database import get_db
from app.models_v4 import Domain, Competency, Framework, Source

router = APIRouter(prefix="/api/v1/v4", tags=["v4"])


class DomainResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    direction: Optional[str]
    sample_artifacts: Optional[Any]
    is_active: bool
    sort_order: int


class CompetencyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    domain_id: str
    title: str
    observable_outcome: Optional[str]
    difficulty_stage: Optional[str]
    source_refs: Optional[Any]
    framework_tags: Optional[Any]
    is_active: bool


class FrameworkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    version: str
    title: str
    evidence_kind: Optional[str]
    fields: Optional[Any]
    limitations: Optional[Any]
    source_refs: Optional[Any]
    is_active: bool


class SourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    publisher: Optional[str]
    source_kind: Optional[str]
    verification_status: Optional[str]


@router.get("/domains", response_model=List[DomainResponse])
async def list_domains(db: Session = Depends(get_db)):
    return (
        db.query(Domain)
        .filter(Domain.is_active == True)
        .order_by(Domain.sort_order)
        .all()
    )


@router.get("/domains/{domain_id}", response_model=DomainResponse)
async def get_domain(domain_id: str, db: Session = Depends(get_db)):
    domain = db.query(Domain).filter(Domain.id == domain_id).first()
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return domain


@router.get("/domains/{domain_id}/competencies", response_model=List[CompetencyResponse])
async def list_competencies(
    domain_id: str,
    difficulty_stage: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(Competency)
        .filter(Competency.domain_id == domain_id, Competency.is_active == True)
    )
    if difficulty_stage:
        query = query.filter(Competency.difficulty_stage == difficulty_stage)
    return query.order_by(Competency.created_at).all()


@router.get("/competencies", response_model=List[CompetencyResponse])
async def list_all_competencies(db: Session = Depends(get_db)):
    return (
        db.query(Competency)
        .filter(Competency.is_active == True)
        .order_by(Competency.domain_id, Competency.created_at)
        .all()
    )


@router.get("/frameworks", response_model=List[FrameworkResponse])
async def list_frameworks(db: Session = Depends(get_db)):
    return (
        db.query(Framework)
        .filter(Framework.is_active == True)
        .all()
    )


@router.get("/frameworks/{framework_id}", response_model=FrameworkResponse)
async def get_framework(framework_id: str, db: Session = Depends(get_db)):
    fw = db.query(Framework).filter(Framework.id == framework_id).first()
    if not fw:
        raise HTTPException(status_code=404, detail="Framework not found")
    return fw


@router.get("/sources", response_model=List[SourceResponse])
async def list_sources(db: Session = Depends(get_db)):
    return db.query(Source).all()

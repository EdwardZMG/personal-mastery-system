"""Principle Cognition API — V4
Propose → Confirm → Revise → Retire lifecycle for personal principles.
"""
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models_v4 import PrincipleVersion

router = APIRouter(prefix="/api/v1/v4/principles", tags=["v4-principles"])


class PrincipleCreateRequest(BaseModel):
    statement: str
    scope: Optional[str] = None
    supporting_evidence_ids: Optional[Any] = None
    uncertainties: Optional[Any] = None


class PrincipleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    statement: str
    scope: Optional[str]
    supporting_evidence_ids: Optional[Any]
    counterexample_refs: Optional[Any]
    uncertainties: Optional[Any]
    confirmation_status: str
    version: int
    review_at: Optional[date]
    supersedes_id: Optional[UUID]
    created_at: Optional[datetime]


class PrincipleUpdateRequest(BaseModel):
    statement: Optional[str] = None
    scope: Optional[str] = None
    counterexample_refs: Optional[Any] = None
    uncertainties: Optional[Any] = None
    review_at: Optional[date] = None


@router.get("/", response_model=List[PrincipleResponse])
async def list_principles(
    status_filter: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    query = db.query(PrincipleVersion).filter(PrincipleVersion.user_id == UUID(user_id))
    if status_filter:
        query = query.filter(PrincipleVersion.confirmation_status == status_filter)
    return query.order_by(PrincipleVersion.created_at.desc()).all()


@router.post("/", response_model=PrincipleResponse, status_code=status.HTTP_201_CREATED)
async def propose_principle(
    request: PrincipleCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    latest = (
        db.query(PrincipleVersion)
        .filter(PrincipleVersion.user_id == UUID(user_id))
        .order_by(PrincipleVersion.version.desc())
        .first()
    )
    next_version = (latest.version + 1) if latest else 1

    principle = PrincipleVersion(
        user_id=UUID(user_id),
        statement=request.statement,
        scope=request.scope,
        supporting_evidence_ids=request.supporting_evidence_ids,
        uncertainties=request.uncertainties,
        confirmation_status="proposed",
        version=next_version,
    )
    db.add(principle)
    db.commit()
    db.refresh(principle)
    return principle


@router.post("/{principle_id}/confirm", response_model=PrincipleResponse)
async def confirm_principle(
    principle_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    principle = db.query(PrincipleVersion).filter(
        PrincipleVersion.id == principle_id,
        PrincipleVersion.user_id == UUID(user_id),
    ).first()
    if not principle:
        raise HTTPException(status_code=404, detail="Principle not found")
    principle.confirmation_status = "confirmed"
    db.commit()
    db.refresh(principle)
    return principle


@router.post("/{principle_id}/revise", response_model=PrincipleResponse)
async def revise_principle(
    principle_id: UUID,
    request: PrincipleUpdateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    old = db.query(PrincipleVersion).filter(
        PrincipleVersion.id == principle_id,
        PrincipleVersion.user_id == UUID(user_id),
    ).first()
    if not old:
        raise HTTPException(status_code=404, detail="Principle not found")

    old.confirmation_status = "revised"

    update_data = request.model_dump(exclude_unset=True)
    new = PrincipleVersion(
        user_id=UUID(user_id),
        statement=update_data.get("statement", old.statement),
        scope=update_data.get("scope", old.scope),
        supporting_evidence_ids=old.supporting_evidence_ids,
        counterexample_refs=update_data.get("counterexample_refs", old.counterexample_refs),
        uncertainties=update_data.get("uncertainties", old.uncertainties),
        confirmation_status="proposed",
        version=old.version + 1,
        review_at=update_data.get("review_at"),
        supersedes_id=old.id,
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new


@router.post("/{principle_id}/retire", response_model=PrincipleResponse)
async def retire_principle(
    principle_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    principle = db.query(PrincipleVersion).filter(
        PrincipleVersion.id == principle_id,
        PrincipleVersion.user_id == UUID(user_id),
    ).first()
    if not principle:
        raise HTTPException(status_code=404, detail="Principle not found")
    principle.confirmation_status = "retired"
    db.commit()
    db.refresh(principle)
    return principle

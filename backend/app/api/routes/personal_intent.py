"""Personal Intent & Direction API — V4"""
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models_v4 import PersonalIntentVersion

router = APIRouter(prefix="/api/v1/personal-intent", tags=["personal-intent"])


class IntentCreateRequest(BaseModel):
    raw_text: Optional[str] = None
    dreams: Optional[dict] = None
    roles: Optional[dict] = None
    values: Optional[dict] = None
    boundaries: Optional[dict] = None
    stage: Optional[dict] = None


class IntentResponse(BaseModel):
    id: UUID
    user_id: UUID
    raw_text: Optional[str]
    dreams: Optional[dict]
    roles: Optional[dict]
    values: Optional[dict]
    boundaries: Optional[dict]
    stage: Optional[dict]
    status: str
    version: int
    effective_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


@router.get("/", response_model=List[IntentResponse])
async def list_intents(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_uuid = UUID(user_id)
    intents = (
        db.query(PersonalIntentVersion)
        .filter(PersonalIntentVersion.user_id == user_uuid)
        .order_by(PersonalIntentVersion.version.desc())
        .all()
    )
    return intents


@router.get("/current", response_model=IntentResponse)
async def get_current_intent(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_uuid = UUID(user_id)
    intent = (
        db.query(PersonalIntentVersion)
        .filter(
            PersonalIntentVersion.user_id == user_uuid,
            PersonalIntentVersion.status == "confirmed",
        )
        .first()
    )
    if not intent:
        intent = (
            db.query(PersonalIntentVersion)
            .filter(
                PersonalIntentVersion.user_id == user_uuid,
                PersonalIntentVersion.status == "draft",
            )
            .order_by(PersonalIntentVersion.version.desc())
            .first()
        )
    if not intent:
        raise HTTPException(status_code=404, detail="No intent version found")
    return intent


@router.post("/", response_model=IntentResponse, status_code=status.HTTP_201_CREATED)
async def create_intent(
    request: IntentCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_uuid = UUID(user_id)

    max_version = (
        db.query(PersonalIntentVersion)
        .filter(PersonalIntentVersion.user_id == user_uuid)
        .with_entities(
            db.query(PersonalIntentVersion.version)
            .filter(PersonalIntentVersion.user_id == user_uuid)
            .order_by(PersonalIntentVersion.version.desc())
            .limit(1)
            .scalar_subquery()
        )
        .first()
    )
    latest = (
        db.query(PersonalIntentVersion)
        .filter(PersonalIntentVersion.user_id == user_uuid)
        .order_by(PersonalIntentVersion.version.desc())
        .first()
    )
    next_version = (latest.version + 1) if latest else 1

    intent = PersonalIntentVersion(
        user_id=user_uuid,
        raw_text=request.raw_text,
        dreams=request.dreams,
        roles=request.roles,
        values=request.values,
        boundaries=request.boundaries,
        stage=request.stage,
        status="draft",
        version=next_version,
    )
    db.add(intent)
    db.commit()
    db.refresh(intent)
    return intent


@router.post("/{intent_id}/confirm", response_model=IntentResponse)
async def confirm_intent(
    intent_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user_uuid = UUID(user_id)
    intent = (
        db.query(PersonalIntentVersion)
        .filter(
            PersonalIntentVersion.id == intent_id,
            PersonalIntentVersion.user_id == user_uuid,
        )
        .first()
    )
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")

    if intent.status == "confirmed":
        return intent

    existing_confirmed = (
        db.query(PersonalIntentVersion)
        .filter(
            PersonalIntentVersion.user_id == user_uuid,
            PersonalIntentVersion.status == "confirmed",
        )
        .first()
    )
    if existing_confirmed:
        existing_confirmed.status = "superseded"
        existing_confirmed.superseded_at = datetime.utcnow()

    intent.status = "confirmed"
    intent.effective_at = datetime.utcnow()
    db.commit()
    db.refresh(intent)
    return intent

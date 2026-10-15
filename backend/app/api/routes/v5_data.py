"""Data Export & Restore API — V5"""
from typing import Optional, Any, Dict, List
from uuid import UUID
from datetime import datetime
import json

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models import Goal, HabitTracking, HabitLog, KnowledgeBase, DailyCheckin, LearningRecord
from app.models_v4 import (
    PersonalIntentVersion, PracticeTask, ArtifactVersion, Evaluation,
    PrincipleVersion, LearningEvent, RewardLedger,
)

router = APIRouter(prefix="/api/v1/data", tags=["data"])


def _serialize_row(row) -> dict:
    d = {}
    for c in row.__table__.columns:
        v = getattr(row, c.name)
        if isinstance(v, (datetime,)):
            d[c.name] = v.isoformat()
        elif isinstance(v, UUID):
            d[c.name] = str(v)
        else:
            d[c.name] = v
    return d


EXPORT_SECTIONS = {
    "goals": (Goal, "user_id"),
    "habits": (HabitTracking, "user_id"),
    "habit_logs": (HabitLog, "user_id"),
    "knowledge": (KnowledgeBase, "user_id"),
    "checkins": (DailyCheckin, "user_id"),
    "learning_records": (LearningRecord, "user_id"),
    "intent_versions": (PersonalIntentVersion, "user_id"),
    "practice_tasks": (PracticeTask, "user_id"),
    "artifact_versions": (ArtifactVersion, "user_id"),
    "evaluations": (Evaluation, "join"),
    "principle_versions": (PrincipleVersion, "user_id"),
    "learning_events": (LearningEvent, "user_id"),
    "reward_ledger": (RewardLedger, "user_id"),
}


@router.get("/export")
async def export_user_data(
    sections: Optional[str] = None,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Export all (or selected) user data as structured JSON.

    Query param `sections`: comma-separated list of section names.
    Omit to export everything.
    """
    user_uuid = UUID(user_id)
    wanted = set(sections.split(",")) if sections else set(EXPORT_SECTIONS.keys())

    unknown = wanted - set(EXPORT_SECTIONS.keys())
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown sections: {unknown}")

    result = {
        "export_version": "1.0",
        "exported_at": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "sections": {},
    }

    for name in wanted:
        model, filter_type = EXPORT_SECTIONS[name]
        if filter_type == "join":
            artifact_ids = [r.id for r in db.query(ArtifactVersion.id).filter(ArtifactVersion.user_id == user_uuid).all()]
            if artifact_ids:
                rows = db.query(model).filter(model.artifact_version_id.in_(artifact_ids)).all()
            else:
                rows = []
        else:
            rows = db.query(model).filter(model.user_id == user_uuid).all()
        result["sections"][name] = [_serialize_row(r) for r in rows]

    return result


RESTORE_MODELS = {
    "goals": Goal,
    "habits": HabitTracking,
    "habit_logs": HabitLog,
    "knowledge": KnowledgeBase,
    "checkins": DailyCheckin,
    "learning_records": LearningRecord,
    "intent_versions": PersonalIntentVersion,
    "practice_tasks": PracticeTask,
    "artifact_versions": ArtifactVersion,
    "evaluations": Evaluation,
    "principle_versions": PrincipleVersion,
    "learning_events": LearningEvent,
    "reward_ledger": RewardLedger,
}


class RestoreRequest(BaseModel):
    data: Dict[str, Any]
    mode: str = "merge"


@router.post("/restore")
async def restore_user_data(
    request: RestoreRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    Restore user data from a previously exported JSON payload.

    mode:
    - "merge" (default): skip records whose PK already exists, insert the rest
    - "replace": delete existing user data in each section, then insert
    """
    user_uuid = UUID(user_id)
    mode = request.mode
    if mode not in ("merge", "replace"):
        raise HTTPException(status_code=400, detail="mode must be 'merge' or 'replace'")

    payload = request.data
    if "sections" not in payload:
        raise HTTPException(status_code=400, detail="Invalid export payload: missing 'sections'")

    summary = {}

    for section_name, rows in payload["sections"].items():
        if section_name not in RESTORE_MODELS:
            summary[section_name] = "skipped: unknown section"
            continue

        model = RESTORE_MODELS[section_name]
        pk_col = model.__table__.primary_key.columns[0].name
        has_user_id = hasattr(model, "user_id")

        if mode == "replace" and has_user_id:
            db.query(model).filter(model.user_id == user_uuid).delete()
            db.flush()

        inserted = 0
        skipped = 0
        for row_data in rows:
            pk_val = row_data.get(pk_col)
            if mode == "merge" and pk_val:
                existing = db.query(model).filter(
                    getattr(model, pk_col) == pk_val
                ).first()
                if existing:
                    skipped += 1
                    continue

            if has_user_id:
                row_data["user_id"] = str(user_uuid)
            obj = model(**row_data)
            db.add(obj)
            inserted += 1

        summary[section_name] = {"inserted": inserted, "skipped": skipped}

    db.commit()
    return {"status": "ok", "mode": mode, "summary": summary}


@router.post("/restore/upload")
async def restore_from_upload(
    file: UploadFile = File(...),
    mode: str = "merge",
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Restore from an uploaded JSON file."""
    content = await file.read()
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")

    req = RestoreRequest(data=payload, mode=mode)
    return await restore_user_data(req, user_id=user_id, db=db)


@router.get("/export/summary")
async def export_summary(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """Return record counts per section (no data)."""
    user_uuid = UUID(user_id)
    counts = {}
    for name, (model, filter_type) in EXPORT_SECTIONS.items():
        if filter_type == "join":
            artifact_ids = [r.id for r in db.query(ArtifactVersion.id).filter(ArtifactVersion.user_id == user_uuid).all()]
            counts[name] = db.query(Evaluation).filter(Evaluation.artifact_version_id.in_(artifact_ids)).count() if artifact_ids else 0
        else:
            counts[name] = db.query(model).filter(model.user_id == user_uuid).count()
    return {"user_id": user_id, "counts": counts}

"""Practice Task & Artifact API — V4"""
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, ConfigDict

from app.database import get_db
from app.dependencies import get_current_user_id
from app.models_v4 import PracticeTask, ArtifactVersion, Evaluation
from app.training_templates import TRAINING_TEMPLATES, UNIVERSAL_RUBRIC

router = APIRouter(prefix="/api/v1/v4/practice", tags=["v4-practice"])


class TaskCreateRequest(BaseModel):
    template_id: str
    domain_id: Optional[str] = None
    competency_id: Optional[UUID] = None
    goal_id: Optional[UUID] = None
    prompt: Optional[str] = None
    input_snapshot: Optional[Any] = None
    training_mode: Optional[str] = "independent"


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    domain_id: Optional[str]
    competency_id: Optional[UUID]
    goal_id: Optional[UUID]
    intent_version: Optional[int]
    template_id: str
    template_version: str
    prompt: Optional[str]
    required_points: Optional[Any]
    estimated_minutes: Optional[int]
    training_mode: str
    status: str
    input_snapshot: Optional[Any]
    created_at: Optional[datetime]
    completed_at: Optional[datetime]


class ArtifactSubmitRequest(BaseModel):
    body: str
    assistance_mode: str = Field("independent", description="independent/hinted/reference_visible/ai_assisted/unknown")
    root_artifact_id: Optional[UUID] = None


class ArtifactResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    root_artifact_id: Optional[UUID]
    task_id: Optional[UUID]
    revision: int
    body: str
    assistance_mode: str
    created_at: Optional[datetime]


class EvaluationRequest(BaseModel):
    dimension_scores: Any
    candidate_feedback: Optional[str] = None
    user_result: Optional[str] = None
    evaluator: str = "ai_candidate"


class EvaluationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    artifact_version_id: UUID
    rubric_version: str
    dimension_scores: Optional[Any]
    candidate_feedback: Optional[str]
    user_result: Optional[str]
    evaluator: str
    status: str
    created_at: Optional[datetime]


@router.get("/templates")
async def list_templates(domain_id: Optional[str] = None):
    templates = list(TRAINING_TEMPLATES.values())
    if domain_id:
        templates = [t for t in templates if t["domain_id"] == domain_id]
    return templates


@router.get("/rubric")
async def get_rubric():
    return UNIVERSAL_RUBRIC


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if request.template_id not in TRAINING_TEMPLATES:
        raise HTTPException(status_code=400, detail=f"Unknown template: {request.template_id}")

    template = TRAINING_TEMPLATES[request.template_id]
    task = PracticeTask(
        user_id=UUID(user_id),
        domain_id=request.domain_id or template["domain_id"],
        competency_id=request.competency_id,
        goal_id=request.goal_id,
        template_id=request.template_id,
        template_version=template["version"],
        prompt=request.prompt,
        required_points=template.get("required_output"),
        estimated_minutes=template.get("estimated_minutes"),
        training_mode=request.training_mode,
        input_snapshot=request.input_snapshot,
        status="pending",
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(
    status_filter: Optional[str] = None,
    domain_id: Optional[str] = None,
    limit: int = 20,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    query = db.query(PracticeTask).filter(PracticeTask.user_id == UUID(user_id))
    if status_filter:
        query = query.filter(PracticeTask.status == status_filter)
    if domain_id:
        query = query.filter(PracticeTask.domain_id == domain_id)
    return query.order_by(PracticeTask.created_at.desc()).limit(limit).all()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    task = db.query(PracticeTask).filter(
        PracticeTask.id == task_id, PracticeTask.user_id == UUID(user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks/{task_id}/start", response_model=TaskResponse)
async def start_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    task = db.query(PracticeTask).filter(
        PracticeTask.id == task_id, PracticeTask.user_id == UUID(user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "in_progress"
    db.commit()
    db.refresh(task)
    return task


@router.post("/tasks/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    task = db.query(PracticeTask).filter(
        PracticeTask.id == task_id, PracticeTask.user_id == UUID(user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "completed"
    task.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task


@router.post("/tasks/{task_id}/artifacts", response_model=ArtifactResponse, status_code=status.HTTP_201_CREATED)
async def submit_artifact(
    task_id: UUID,
    request: ArtifactSubmitRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    task = db.query(PracticeTask).filter(
        PracticeTask.id == task_id, PracticeTask.user_id == UUID(user_id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    latest = (
        db.query(ArtifactVersion)
        .filter(ArtifactVersion.task_id == task_id)
        .order_by(ArtifactVersion.revision.desc())
        .first()
    )
    next_revision = (latest.revision + 1) if latest else 1

    root_id = request.root_artifact_id
    if root_id is None and latest and latest.root_artifact_id:
        root_id = latest.root_artifact_id
    elif root_id is None:
        root_id = None

    artifact = ArtifactVersion(
        user_id=UUID(user_id),
        root_artifact_id=root_id,
        task_id=task_id,
        revision=next_revision,
        body=request.body,
        assistance_mode=request.assistance_mode,
    )
    db.add(artifact)
    db.commit()
    db.refresh(artifact)

    if artifact.root_artifact_id is None:
        artifact.root_artifact_id = artifact.id
        db.commit()
        db.refresh(artifact)

    return artifact


@router.get("/tasks/{task_id}/artifacts", response_model=List[ArtifactResponse])
async def list_artifacts(
    task_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    return (
        db.query(ArtifactVersion)
        .filter(ArtifactVersion.task_id == task_id, ArtifactVersion.user_id == UUID(user_id))
        .order_by(ArtifactVersion.revision)
        .all()
    )


@router.post("/artifacts/{artifact_id}/evaluate", response_model=EvaluationResponse, status_code=status.HTTP_201_CREATED)
async def evaluate_artifact(
    artifact_id: UUID,
    request: EvaluationRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    artifact = db.query(ArtifactVersion).filter(
        ArtifactVersion.id == artifact_id, ArtifactVersion.user_id == UUID(user_id)
    ).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")

    evaluation = Evaluation(
        artifact_version_id=artifact_id,
        dimension_scores=request.dimension_scores,
        candidate_feedback=request.candidate_feedback,
        user_result=request.user_result,
        evaluator=request.evaluator,
        status="candidate",
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation


@router.get("/artifacts/{artifact_id}/evaluations", response_model=List[EvaluationResponse])
async def list_evaluations(
    artifact_id: UUID,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    artifact = db.query(ArtifactVersion).filter(
        ArtifactVersion.id == artifact_id, ArtifactVersion.user_id == UUID(user_id)
    ).first()
    if not artifact:
        raise HTTPException(status_code=404, detail="Artifact not found")
    return (
        db.query(Evaluation)
        .filter(Evaluation.artifact_version_id == artifact_id)
        .order_by(Evaluation.created_at)
        .all()
    )

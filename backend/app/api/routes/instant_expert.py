"""
Instant Expert API - 即时专家
Input a keyword, get a 50-100 word expert explanation ready to read aloud
"""
from uuid import UUID
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.database import get_db
from app.models_extended import KnowledgeInsight
from app.services.ai_service import generate_expert_explanation

router = APIRouter(prefix="/api/v1/expert", tags=["instant-expert"])

DEFAULT_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


class ExpertRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100, description="陌生词汇/概念")
    context: Optional[str] = Field(None, max_length=200, description="场景：聊天/新闻/会议等")


class ExpertResponse(BaseModel):
    keyword: str
    explanation: str
    generated_at: str
    saved: bool = False


@router.post("/", response_model=ExpertResponse)
async def get_expert_explanation(
    req: ExpertRequest,
    user_id: UUID = DEFAULT_USER_ID,
    db: Session = Depends(get_db),
):
    explanation = await generate_expert_explanation(req.keyword, req.context or "")

    insight = KnowledgeInsight(
        user_id=user_id,
        content=f"[即时专家] {req.keyword}: {explanation}",
        domain="general",
        intent="insight",
        key_points={"keyword": req.keyword, "context": req.context, "explanation": explanation},
        tags=["instant_expert", req.keyword],
        source="expert_api",
        language="zh",
        status="structured",
    )
    db.add(insight)
    db.commit()

    return ExpertResponse(
        keyword=req.keyword,
        explanation=explanation,
        generated_at=datetime.now().isoformat(),
        saved=True,
    )


@router.get("/history")
async def get_expert_history(
    limit: int = 20,
    user_id: UUID = DEFAULT_USER_ID,
    db: Session = Depends(get_db),
):
    insights = db.query(KnowledgeInsight).filter(
        KnowledgeInsight.user_id == user_id,
        KnowledgeInsight.source == "expert_api",
    ).order_by(KnowledgeInsight.created_at.desc()).limit(limit).all()

    return [
        {
            "keyword": (i.key_points or {}).get("keyword", ""),
            "explanation": (i.key_points or {}).get("explanation", ""),
            "context": (i.key_points or {}).get("context", ""),
            "created_at": i.created_at.isoformat() if i.created_at else None,
        }
        for i in insights
    ]

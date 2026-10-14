"""
API route exports for Edward Growth System.

All route modules are importable from this package.  Each module exposes
a ``router`` (``fastapi.APIRouter``) that should be included in the main
FastAPI application via ``app.include_router(...)``.
"""

from app.api.routes.knowledge import router as knowledge_router
from app.api.routes.review import router as review_router
from app.api.routes.speech import router as speech_router
from app.api.routes.application import router as application_router
from app.api.routes.auth import router as auth_router
from app.api.routes.learning import router as learning_router
from app.api.routes.checkins import router as checkins_router
from app.api.routes.goals import router as goals_router
from app.api.routes.habits import router as habits_router
from app.api.routes.classics import router as classics_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.crawler import router as crawler_router
from app.api.routes.admin import router as admin_router
from app.api.routes.feishu_bot import router as feishu_bot_router
from app.api.routes.gamification import router as gamification_router
from app.api.routes.ebbinghaus_review import router as ebbinghaus_review_router
from app.api.routes.instant_expert import router as instant_expert_router

__all__ = [
    "knowledge_router",
    "review_router",
    "speech_router",
    "application_router",
    "auth_router",
    "learning_router",
    "checkins_router",
    "goals_router",
    "habits_router",
    "classics_router",
    "dashboard_router",
    "recommendations_router",
    "crawler_router",
    "admin_router",
    "feishu_bot_router",
    "gamification_router",
    "ebbinghaus_review_router",
    "instant_expert_router",
]

"""
API package for Edward Growth System.

Re-exports all route routers for convenient inclusion in the main app.
"""

from app.api.routes import (
    knowledge_router,
    review_router,
    speech_router,
    application_router,
    auth_router,
    learning_router,
    checkins_router,
    goals_router,
    habits_router,
    classics_router,
    dashboard_router,
    recommendations_router,
    crawler_router,
    admin_router,
)

ALL_ROUTERS = [
    knowledge_router,
    review_router,
    speech_router,
    application_router,
    auth_router,
    learning_router,
    checkins_router,
    goals_router,
    habits_router,
    classics_router,
    dashboard_router,
    recommendations_router,
    crawler_router,
    admin_router,
]

__all__ = ["ALL_ROUTERS"]

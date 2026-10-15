from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.database import engine, Base
from app.config import settings
from app.scheduler import start_scheduler, stop_scheduler
from app.core.exceptions import BusinessError, NotFoundError, AuthError
from app.core.middleware import setup_request_logging
from app.models_v4 import (  # noqa: F401 — ensure V4 tables are created
    PersonalIntentVersion, Domain, Competency, Framework, Source,
    PracticeTask, ArtifactVersion, Evaluation, PrincipleVersion,
    BackgroundTaskRecord, LearningEvent, RewardLedger,
)

# Import all route modules
from app.api.routes import (
    knowledge, review, speech, application,
    auth, learning, checkins, goals, habits,
    classics, dashboard, recommendations, crawler, admin, feishu_bot_router as feishu_bot,
    gamification, ebbinghaus_review, instant_expert, personal_intent, v4_domain, v4_practice,
    v4_principles, v4_recommend, v5_data,
)


# ---------------------------------------------------------------------------
# Lifespan (replaces deprecated @app.on_event)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: security checks
    if settings.SECRET_KEY in (
        "your-secret-key-change-in-production",
        "edward-growth-secret-key-2026-change-in-production",
    ):
        raise RuntimeError(
            "SECRET_KEY is using a default/insecure value. "
            "Set a strong random key in .env before starting the server."
        )
    # Startup: database
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables verified")
    except Exception as e:
        print(f"Warning: Could not connect to database: {e}")
        print("Server will start but database operations will fail")
    start_scheduler()
    print("Edward Growth System started")
    yield
    # Shutdown
    stop_scheduler()
    print("Edward Growth System stopped")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Edward Growth System API",
    description="Personal growth tracking and push notification system with knowledge crystallization and speech generation",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware — specific origins from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
setup_request_logging(app)


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------

@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(status_code=400, content=exc.detail)


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content=exc.detail)


@app.exception_handler(AuthError)
async def auth_error_handler(request: Request, exc: AuthError):
    return JSONResponse(
        status_code=401,
        content=exc.detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled error on {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url.path)},
    )


# ---------------------------------------------------------------------------
# Inline endpoints (root + health only)
# ---------------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Edward Growth System API v2.0",
        "version": "2.0.0",
        "status": "running",
        "modules": [
            "knowledge_capture",
            "review_system",
            "speech_generation",
            "application_tracking",
            "push_notifications",
        ],
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ---------------------------------------------------------------------------
# Register API route modules
# ---------------------------------------------------------------------------

# Legacy route modules (original v1 prefixes)
app.include_router(knowledge.router)
app.include_router(review.router)
app.include_router(speech.router)
app.include_router(application.router)

# New v1 route modules
app.include_router(auth.router)
app.include_router(learning.router)
app.include_router(checkins.router)
app.include_router(goals.router)
app.include_router(habits.router)
app.include_router(classics.router)
app.include_router(dashboard.router)
app.include_router(recommendations.router)
app.include_router(crawler.router)
app.include_router(admin.router)
app.include_router(feishu_bot)  # feishu_bot is already the router object
app.include_router(gamification.router)
app.include_router(ebbinghaus_review.router)
app.include_router(instant_expert.router)
app.include_router(personal_intent.router)
app.include_router(v4_domain.router)
app.include_router(v4_practice.router)
app.include_router(v4_principles.router)
app.include_router(v4_recommend.router)
app.include_router(v5_data.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

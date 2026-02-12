"""
Floyd AI Inquiry Capture & Conversion Engine
Main FastAPI application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.config import get_settings
from app.routes import router
from app.services.scheduler import start_scheduler, shutdown_scheduler
from app.limiter import limiter

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

settings = get_settings()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    logger.info(
        "Starting SheersSoft AI Engine",
        environment=settings.environment,
    )

    # Ensure pgvector extension exists on startup
    from app.database import engine
    from sqlalchemy import text

    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        logger.info("pgvector extension ready")

    # Create tables if they don't exist (for development)
    if not settings.is_production:
        from app.models import Base
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created (dev mode)")

    # Start scheduler
    await start_scheduler()

    yield

    # Shutdown scheduler
    await shutdown_scheduler()
    logger.info("Shutting down SheersSoft AI Engine")


app = FastAPI(
    title="SheersSoft AI Inquiry Capture Engine",
    description="AI-powered hotel inquiry capture and conversion system",
    version="0.1.0",
    dependencies=[],
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — allow all origins in dev, restrict in production
origins = settings.allowed_origins.split(",") if settings.is_production else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Mount static files (for widget.js)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {
        "name": "SheersSoft AI Inquiry Capture Engine",
        "version": "0.1.0",
        "status": "running",
    }

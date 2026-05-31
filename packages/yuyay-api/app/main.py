"""YUYAY Intelligence Framework — FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.db import init_db
from app.logger import configure_logging, get_logger
from app.routers import (
    archetypes,
    compare,
    evaluate,
    metrics,
    query,
    sessions,
    transformers,
    wheel,
)

logger = get_logger(__name__)
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="YUYAY Intelligence API",
    description="REST API for the YUYAY Intelligence Framework — UN Office of the Future",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.unofficeofthefuture.org",
        "https://unofficeofthefuture.org",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize the database and logging on application startup."""
    configure_logging()
    await init_db()
    logger.info("startup_complete", version="0.1.0")


app.include_router(archetypes.router)
app.include_router(compare.router)
app.include_router(transformers.router)
app.include_router(evaluate.router)
app.include_router(wheel.router)
app.include_router(sessions.router)
app.include_router(metrics.router)
app.include_router(query.router)


@app.get("/api/v1/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for monitoring.

    Returns:
        A dict with status and version information.
    """
    return {"status": "ok", "version": "0.1.0"}

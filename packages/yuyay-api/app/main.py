"""YUYAY Intelligence Framework — FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from app.db import init_db
from app.routers import (
    archetypes,
    auth,
    evaluate,
    metrics,
    sessions,
    transformers,
    wheel,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

app = FastAPI(
    title="YUYAY Intelligence API",
    description="REST API for the YUYAY Intelligence Framework — UN Office of the Future",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize the database on application startup."""
    await init_db()


app.include_router(archetypes.router)
app.include_router(transformers.router)
app.include_router(evaluate.router)
app.include_router(wheel.router)
app.include_router(sessions.router)
app.include_router(metrics.router)
app.include_router(auth.router)


@app.get("/api/v1/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for monitoring.

    Returns:
        A dict with status and version information.
    """
    return {"status": "ok", "version": "0.1.0"}

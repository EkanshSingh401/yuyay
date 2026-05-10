"""YUYAY Intelligence Framework — FastAPI application entry point."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import archetypes, evaluate, transformers, wheel

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

app.include_router(archetypes.router)
app.include_router(transformers.router)
app.include_router(evaluate.router)
app.include_router(wheel.router)


@app.get("/api/v1/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for monitoring.

    Returns:
        A dict with status and version information.
    """
    return {"status": "ok", "version": "0.1.0"}

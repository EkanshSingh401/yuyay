"""YUYAY Intelligence Framework — FastAPI application entry point."""

from __future__ import annotations

import os
import time
from typing import Any

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.db import init_db
from app.logger import configure_logging, get_logger
from app.prometheus import http_request_duration_seconds, http_requests_total
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

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[
        FastApiIntegration(),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
    enable_logs=True,
    environment=os.environ.get("ENVIRONMENT", "production"),
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


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next: Any) -> Any:
    """Track request count and duration for Prometheus.

    Args:
        request: The incoming HTTP request.
        call_next: The next middleware or endpoint handler.

    Returns:
        The HTTP response.
    """
    start_time = time.monotonic()
    response = await call_next(request)
    duration = time.monotonic() - start_time

    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=str(response.status_code),
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)

    return response


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


@app.get("/api/v1/prometheus")
async def prometheus_metrics() -> Response:
    """Expose Prometheus metrics in text format.

    Returns:
        Prometheus-formatted metrics as plain text.
    """
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )

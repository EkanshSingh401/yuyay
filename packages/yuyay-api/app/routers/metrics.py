"""Metrics router for the YUYAY Intelligence API."""

from __future__ import annotations

import time

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["metrics"])

_start_time = time.monotonic()


class MetricsResponse(BaseModel):
    """JSON metrics response for the dashboard.

    Attributes:
        uptime_seconds: Server uptime in seconds.
        version: Current API version.
        prometheus_url: URL to Prometheus metrics endpoint.
    """

    uptime_seconds: float
    version: str
    prometheus_url: str


@router.get("/metrics")
async def get_metrics(
    current_user: str = Depends(get_current_user),
) -> MetricsResponse:
    """Return basic server metrics and link to Prometheus endpoint.

    Returns:
        A MetricsResponse with uptime and Prometheus URL.
    """
    return MetricsResponse(
        uptime_seconds=round(time.monotonic() - _start_time, 2),
        version="0.1.0",
        prometheus_url="/api/v1/prometheus",
    )

"""Metrics router for the YUYAY Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["metrics"])


class MetricsResponse(BaseModel):
    """Prometheus-compatible metrics response.

    Attributes:
        requests_total: Total number of requests served.
        uptime_seconds: Server uptime in seconds.
        version: Current API version.
    """

    requests_total: int
    uptime_seconds: float
    version: str


@router.get("/metrics")
async def get_metrics() -> MetricsResponse:
    """Return Prometheus-compatible metrics.

    Returns:
        A MetricsResponse with basic server metrics.
    """
    return MetricsResponse(
        requests_total=0,
        uptime_seconds=0.0,
        version="0.1.0",
    )

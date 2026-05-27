"""Integration tests for the metrics endpoint."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_metrics_requires_auth(client: AsyncClient) -> None:
    """Metrics endpoint returns 401 without token."""
    response = await client.get("/api/v1/metrics")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_metrics_returns_200(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Metrics endpoint returns 200 with valid token."""
    response = await client.get("/api/v1/metrics", headers=auth_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_metrics_returns_version(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Metrics endpoint returns version field."""
    response = await client.get("/api/v1/metrics", headers=auth_headers)
    assert "version" in response.json()


@pytest.mark.asyncio
async def test_metrics_returns_requests_total(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Metrics endpoint returns requests_total field."""
    response = await client.get("/api/v1/metrics", headers=auth_headers)
    assert "requests_total" in response.json()

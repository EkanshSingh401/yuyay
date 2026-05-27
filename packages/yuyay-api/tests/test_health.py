"""Integration tests for the health check endpoint."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_returns_200(client: AsyncClient) -> None:
    """Health endpoint returns 200 OK."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_returns_ok_status(client: AsyncClient) -> None:
    """Health endpoint returns status ok."""
    response = await client.get("/api/v1/health")
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_health_returns_version(client: AsyncClient) -> None:
    """Health endpoint returns version string."""
    response = await client.get("/api/v1/health")
    assert "version" in response.json()


@pytest.mark.asyncio
async def test_health_is_public(client: AsyncClient) -> None:
    """Health endpoint is accessible without authentication."""
    response = await client.get("/api/v1/health")
    assert response.status_code != 401

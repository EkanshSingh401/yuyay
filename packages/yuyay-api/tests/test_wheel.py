"""Integration tests for the wheel endpoint."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_wheel_synthesize_requires_auth(client: AsyncClient) -> None:
    """Wheel synthesize returns 401 without token."""
    response = await client.post(
        "/api/v1/wheel/synthesize",
        json={
            "sectors_addressed": ["Justice", "Health"],
            "sector": "Justice",
            "worldview_alignment": True,
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_wheel_synthesize_valid(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Wheel synthesize returns 200 with valid data."""
    response = await client.post(
        "/api/v1/wheel/synthesize",
        json={
            "sectors_addressed": ["Justice", "Health", "Education"],
            "sector": "Justice",
            "worldview_alignment": True,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_wheel_synthesize_correct_score(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Wheel synthesize returns correct whole system score."""
    response = await client.post(
        "/api/v1/wheel/synthesize",
        json={
            "sectors_addressed": ["Justice", "Health", "Education"],
            "sector": "Justice",
            "worldview_alignment": True,
        },
        headers=auth_headers,
    )
    assert response.json()["whole_system_score"] == 3


@pytest.mark.asyncio
async def test_wheel_synthesize_invalid_sector(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Wheel synthesize returns 404 for invalid primary sector."""
    response = await client.post(
        "/api/v1/wheel/synthesize",
        json={
            "sectors_addressed": ["Justice"],
            "sector": "FakeSector",
            "worldview_alignment": True,
        },
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_wheel_synthesize_returns_all_sectors(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Wheel synthesize returns all 12 sectors in response."""
    response = await client.post(
        "/api/v1/wheel/synthesize",
        json={
            "sectors_addressed": ["Justice"],
            "sector": "Justice",
            "worldview_alignment": False,
        },
        headers=auth_headers,
    )
    assert len(response.json()["all_sectors"]) == 12

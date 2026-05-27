"""Integration tests for the archetypes endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_archetypes_returns_200(client: AsyncClient) -> None:
    """List archetypes returns 200."""
    response = await client.get("/api/v1/archetypes/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_archetypes_returns_12(client: AsyncClient) -> None:
    """List archetypes returns all 12 archetypes."""
    response = await client.get("/api/v1/archetypes/")
    assert len(response.json()) == 12


@pytest.mark.asyncio
async def test_list_archetypes_is_public(client: AsyncClient) -> None:
    """List archetypes is accessible without authentication."""
    response = await client.get("/api/v1/archetypes/")
    assert response.status_code != 401


@pytest.mark.asyncio
async def test_get_archetype_by_name(client: AsyncClient) -> None:
    """Get single archetype by name returns correct data."""
    response = await client.get("/api/v1/archetypes/The Seer")
    assert response.status_code == 200
    assert response.json()["name"] == "The Seer"


@pytest.mark.asyncio
async def test_get_archetype_not_found(client: AsyncClient) -> None:
    """Get archetype with invalid name returns 404."""
    response = await client.get("/api/v1/archetypes/FakeArchetype")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_archetype_has_required_fields(client: AsyncClient) -> None:
    """Each archetype has name, function, gifts, and shadow fields."""
    response = await client.get("/api/v1/archetypes/")
    archetype = response.json()[0]
    assert "name" in archetype
    assert "function" in archetype
    assert "gifts" in archetype
    assert "shadow" in archetype

"""Integration tests for the transformers endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_transformers_returns_200(client: AsyncClient) -> None:
    """List transformers returns 200."""
    response = await client.get("/api/v1/transformers/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_transformers_is_public(client: AsyncClient) -> None:
    """List transformers is accessible without authentication."""
    response = await client.get("/api/v1/transformers/")
    assert response.status_code != 401


@pytest.mark.asyncio
async def test_list_transformers_returns_12(client: AsyncClient) -> None:
    """List transformers returns all 12 transformer questions."""
    response = await client.get("/api/v1/transformers/")
    assert len(response.json()) == 12


@pytest.mark.asyncio
async def test_transformer_has_required_fields(client: AsyncClient) -> None:
    """Each transformer has id and question fields."""
    response = await client.get("/api/v1/transformers/")
    transformer = response.json()[0]
    assert "id" in transformer
    assert "question" in transformer


@pytest.mark.asyncio
async def test_run_transformer_requires_auth(client: AsyncClient) -> None:
    """Run transformer returns 401 without token."""
    response = await client.post(
        "/api/v1/transformers/run",
        params={"transformer_id": "1a", "input_text": "test"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_run_transformer_valid(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Run transformer returns 200 with valid id."""
    response = await client.post(
        "/api/v1/transformers/run",
        params={"transformer_id": "1a", "input_text": "test input"},
        headers=auth_headers,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_run_transformer_not_found(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Run transformer returns 404 for invalid id."""
    response = await client.post(
        "/api/v1/transformers/run",
        params={"transformer_id": "99", "input_text": "test"},
        headers=auth_headers,
    )
    assert response.status_code == 404

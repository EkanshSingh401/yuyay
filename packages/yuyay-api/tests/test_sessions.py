"""Integration tests for the sessions endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_sessions_requires_auth(client: AsyncClient) -> None:
    """List sessions returns 401 without token."""
    response = await client.get("/api/v1/sessions/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_sessions_returns_200(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """List sessions returns 200 with valid token."""
    response = await client.get("/api/v1/sessions/", headers=auth_headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_sessions_returns_list(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """List sessions returns a list."""
    response = await client.get("/api/v1/sessions/", headers=auth_headers)
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_session_after_evaluate(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Session created by evaluate is retrievable by ID."""
    evaluate_response = await client.post(
        "/api/v1/evaluate",
        json={"responses": {"1a": "YES", "1b": "NO"}},
        headers=auth_headers,
    )
    session_id = evaluate_response.json()["session_id"]

    session_response = await client.get(
        f"/api/v1/sessions/{session_id}",
        headers=auth_headers,
    )
    assert session_response.status_code == 200
    assert session_response.json()["id"] == session_id


@pytest.mark.asyncio
async def test_get_session_not_found(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Get session with invalid ID returns 404."""
    response = await client.get(
        "/api/v1/sessions/nonexistent-id",
        headers=auth_headers,
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_session_has_correct_responses(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Session stores and returns the original responses."""
    evaluate_response = await client.post(
        "/api/v1/evaluate",
        json={"responses": {"1a": "YES", "1b": "NO"}},
        headers=auth_headers,
    )
    session_id = evaluate_response.json()["session_id"]

    session_response = await client.get(
        f"/api/v1/sessions/{session_id}",
        headers=auth_headers,
    )
    responses = session_response.json()["responses"]
    assert responses["1a"] == "YES"
    assert responses["1b"] == "NO"

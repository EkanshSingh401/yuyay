"""Integration tests for the evaluate endpoint."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_evaluate_requires_auth(client: AsyncClient) -> None:
    """Evaluate endpoint returns 401 without token."""
    response = await client.post(
        "/api/v1/evaluate",
        json={"responses": {"1a": "YES"}},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_evaluate_valid_responses(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Evaluate returns 200 with valid YES/NO/PO responses."""
    response = await client.post(
        "/api/v1/evaluate",
        json={"responses": {"1a": "YES", "1b": "NO", "2a": "PO"}},
        headers=auth_headers,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_evaluate_returns_correct_counts(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Evaluate returns correct YES/NO/PO counts."""
    response = await client.post(
        "/api/v1/evaluate",
        json={"responses": {"1a": "YES", "1b": "NO", "2a": "PO"}},
        headers=auth_headers,
    )
    data = response.json()
    assert data["yes_count"] == 1
    assert data["no_count"] == 1
    assert data["po_count"] == 1
    assert data["total"] == 3


@pytest.mark.asyncio
async def test_evaluate_returns_session_id(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Evaluate returns a session_id for the saved session."""
    response = await client.post(
        "/api/v1/evaluate",
        json={"responses": {"1a": "YES"}},
        headers=auth_headers,
    )
    assert "session_id" in response.json()


@pytest.mark.asyncio
async def test_evaluate_invalid_response_value(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Evaluate returns 422 for invalid response values."""
    response = await client.post(
        "/api/v1/evaluate",
        json={"responses": {"1a": "MAYBE"}},
        headers=auth_headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_evaluate_flags_no_and_po(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Evaluate flags NO and PO responses."""
    response = await client.post(
        "/api/v1/evaluate",
        json={"responses": {"1a": "YES", "1b": "NO", "2a": "PO"}},
        headers=auth_headers,
    )
    flags = response.json()["flags"]
    assert "1b" in flags
    assert "2a" in flags
    assert "1a" not in flags

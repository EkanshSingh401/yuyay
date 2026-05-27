"""Integration tests for the auth endpoints."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_valid_credentials(client: AsyncClient) -> None:
    """Login with valid credentials returns 200 and a token."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "yuyay2026"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient) -> None:
    """Login with wrong password returns 401."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "admin", "password": "wrongpassword"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_invalid_username(client: AsyncClient) -> None:
    """Login with unknown username returns 401."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "nobody", "password": "yuyay2026"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_without_token(client: AsyncClient) -> None:
    """Protected endpoint returns 401 without a token."""
    response = await client.get("/api/v1/sessions/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_with_invalid_token(client: AsyncClient) -> None:
    """Protected endpoint returns 401 with an invalid token."""
    response = await client.get(
        "/api/v1/sessions/",
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_endpoint_with_valid_token(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Protected endpoint returns 200 with a valid token."""
    response = await client.get("/api/v1/sessions/", headers=auth_headers)
    assert response.status_code == 200

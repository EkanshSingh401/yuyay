"""Integration tests for the FIOS query endpoint."""

from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_query_requires_auth(client: AsyncClient) -> None:
    """Query endpoint returns 401 without token."""
    response = await client.post(
        "/api/v1/query",
        json={"prompt": "test", "provider": "mock", "model": "mock-model"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_query_mock_provider(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Query with mock provider returns 200."""
    response = await client.post(
        "/api/v1/query",
        json={"prompt": "What is wisdom?", "provider": "mock", "model": "mock-model"},
        headers=auth_headers,
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_query_returns_response(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Query returns a non-empty response string."""
    response = await client.post(
        "/api/v1/query",
        json={"prompt": "What is wisdom?", "provider": "mock", "model": "mock-model"},
        headers=auth_headers,
    )
    assert len(response.json()["response"]) > 0


@pytest.mark.asyncio
async def test_query_returns_coherence_score(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Query returns a coherence score between 0 and 100."""
    response = await client.post(
        "/api/v1/query",
        json={"prompt": "test", "provider": "mock", "model": "mock-model"},
        headers=auth_headers,
    )
    score = response.json()["coherence_score"]
    assert 0 <= score <= 100


@pytest.mark.asyncio
async def test_query_prompt_contains_yuyay_context(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Query enriches prompt with YUYAY context."""
    response = await client.post(
        "/api/v1/query",
        json={"prompt": "test", "provider": "mock", "model": "mock-model"},
        headers=auth_headers,
    )
    assert "YUYAY" in response.json()["prompt"]


@pytest.mark.asyncio
async def test_query_invalid_provider(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Query with invalid provider returns 400."""
    response = await client.post(
        "/api/v1/query",
        json={"prompt": "test", "provider": "banana", "model": "banana-3"},
        headers=auth_headers,
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_query_returns_token_counts(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Query returns input, output, and total token counts."""
    response = await client.post(
        "/api/v1/query",
        json={"prompt": "test", "provider": "mock", "model": "mock-model"},
        headers=auth_headers,
    )
    data = response.json()
    assert "input_tokens" in data
    assert "output_tokens" in data
    assert "total_tokens" in data
    assert data["total_tokens"] == data["input_tokens"] + data["output_tokens"]


@pytest.mark.asyncio
async def test_query_returns_cost(
    client: AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Query returns estimated cost in USD."""
    response = await client.post(
        "/api/v1/query",
        json={"prompt": "test", "provider": "mock", "model": "mock-model"},
        headers=auth_headers,
    )
    assert "estimated_cost_usd" in response.json()

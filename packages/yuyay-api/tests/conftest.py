"""Shared test fixtures for the YUYAY Intelligence API test suite."""

from __future__ import annotations

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import get_session
from app.main import app
from app.models import Base

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
test_session_factory = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_session() -> AsyncSession:
    """Override the real database session with a test session.

    Yields:
        An async SQLAlchemy session connected to the in-memory test database.
    """
    async with test_session_factory() as session:
        yield session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database() -> None:
    """Create all tables in the in-memory test database before tests run."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    """Provide an async HTTP test client with the test database injected.

    Returns:
        An AsyncClient configured to call the FastAPI app directly.
    """
    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient) -> dict[str, str]:
    """Log in and return Authorization headers for protected endpoints.

    Args:
        client: The async test client fixture.

    Returns:
        A dict with the Authorization Bearer header.
    """
    from app.auth import create_access_token

    token = create_access_token({"sub": "admin"})
    return {"Authorization": f"Bearer {token}"}

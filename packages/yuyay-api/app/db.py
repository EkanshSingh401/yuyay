"""Database connection and session management for the YUYAY Intelligence API."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models import Base

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "sqlite+aiosqlite:///./yuyay.db",
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Create all database tables if they don't exist.

    This should be called once on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a database session for use in FastAPI dependency injection.

    Yields:
        An async SQLAlchemy session.
    """
    async with async_session_factory() as session:
        yield session

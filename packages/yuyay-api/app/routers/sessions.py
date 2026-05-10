"""Sessions router for the YUYAY Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import EvaluationSession

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


class SessionSummary(BaseModel):
    """Summary of a single evaluation session.

    Attributes:
        id: Unique session identifier.
        status: Current status of the session.
        total_responses: Number of responses recorded.
    """

    id: str
    status: str
    total_responses: int


class SessionDetail(BaseModel):
    """Detailed view of a single evaluation session.

    Attributes:
        id: Unique session identifier.
        status: Current status of the session.
        total_responses: Number of responses recorded.
        responses: The actual responses dict.
    """

    id: str
    status: str
    total_responses: int
    responses: dict[str, str]


@router.get("/")
async def list_sessions(
    db: AsyncSession = Depends(get_session),
) -> list[SessionSummary]:
    """List all evaluation sessions.

    Args:
        db: The database session injected by FastAPI.

    Returns:
        A list of session summaries.
    """
    result = await db.execute(select(EvaluationSession))
    sessions = result.scalars().all()
    return [
        SessionSummary(
            id=s.id,
            status=s.status,
            total_responses=s.total_responses,
        )
        for s in sessions
    ]


@router.get("/{session_id}")
async def get_session_by_id(
    session_id: str,
    db: AsyncSession = Depends(get_session),
) -> SessionDetail:
    """Get a single session by id.

    Args:
        session_id: The session identifier to look up.
        db: The database session injected by FastAPI.

    Returns:
        Full session detail with responses.

    Raises:
        HTTPException: 404 if session not found.
    """
    result = await db.execute(
        select(EvaluationSession).where(EvaluationSession.id == session_id)
    )
    session = result.scalar_one_or_none()
    if session is None:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found.",
        )
    return SessionDetail(
        id=session.id,
        status=session.status,
        total_responses=session.total_responses,
        responses=session.responses,
    )

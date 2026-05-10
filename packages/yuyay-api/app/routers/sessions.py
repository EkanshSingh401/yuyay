"""Sessions router for the YUYAY Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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
async def list_sessions() -> list[SessionSummary]:
    """List all evaluation sessions.

    Returns:
        A list of session summaries.
    """
    return [
        SessionSummary(id="session-001", status="complete", total_responses=12),
        SessionSummary(id="session-002", status="in_progress", total_responses=5),
    ]


@router.get("/{session_id}")
async def get_session(session_id: str) -> SessionDetail:
    """Get a single session by id.

    Args:
        session_id: The session identifier to look up.

    Returns:
        Full session detail with responses.

    Raises:
        HTTPException: 404 if session not found.
    """
    mock_sessions: dict[str, SessionDetail] = {
        "session-001": SessionDetail(
            id="session-001",
            status="complete",
            total_responses=12,
            responses={"1a": "YES", "1b": "NO", "2a": "PO"},
        ),
    }
    session = mock_sessions.get(session_id)
    if session is None:
        raise HTTPException(
            status_code=404,
            detail=f"Session '{session_id}' not found.",
        )
    return session

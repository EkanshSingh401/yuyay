"""Evaluate router for the YUYAY Intelligence API."""

from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from yuyay.exceptions import InvalidResponseError
from yuyay.questionnaire import process_responses

from app.auth import get_current_user
from app.db import get_session
from app.logger import get_logger
from app.models import EvaluationSession
from app.prometheus import (
    evaluations_total,
    no_responses_total,
    po_responses_total,
    yes_responses_total,
)

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1", tags=["evaluate"])


class EvaluateRequest(BaseModel):
    """Request body for the evaluate endpoint.

    Attributes:
        responses: A dict mapping question id to YES, NO, or PO.
    """

    responses: dict[str, str]


class EvaluateResponse(BaseModel):
    """Response body for the evaluate endpoint.

    Attributes:
        session_id: The id of the saved evaluation session.
        yes_count: Number of YES responses.
        no_count: Number of NO responses.
        po_count: Number of PO responses.
        total: Total responses processed.
        flags: Question ids that returned NO or PO.
        summary: Human readable summary string.
    """

    session_id: str
    yes_count: int
    no_count: int
    po_count: int
    total: int
    flags: list[str]
    summary: str


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(
    request: EvaluateRequest,
    db: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
) -> EvaluateResponse:
    """Submit questionnaire responses and return YES/NO/PO analysis.

    Args:
        request: The request body containing responses dict.
        db: The database session injected by FastAPI.

    Returns:
        An EvaluateResponse with session id, counts, flags, and summary.

    Raises:
        HTTPException: 422 if any response value is invalid.
    """
    try:
        report = process_responses(request.responses)
    except InvalidResponseError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    session = EvaluationSession(
        status="complete",
        responses=request.responses,
        yes_count=report.yes_count,
        no_count=report.no_count,
        po_count=report.po_count,
        total_responses=report.total,
        flags=report.flags,
        completed_at=datetime.utcnow(),
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    logger.info(
        "evaluation_complete",
        session_id=session.id,
        yes_count=report.yes_count,
        no_count=report.no_count,
        po_count=report.po_count,
        total=report.total,
        user=current_user,
    )

    evaluations_total.inc()
    yes_responses_total.inc(report.yes_count)
    no_responses_total.inc(report.no_count)
    po_responses_total.inc(report.po_count)

    return EvaluateResponse(
        session_id=session.id,
        yes_count=report.yes_count,
        no_count=report.no_count,
        po_count=report.po_count,
        total=report.total,
        flags=report.flags,
        summary=report.summary(),
    )

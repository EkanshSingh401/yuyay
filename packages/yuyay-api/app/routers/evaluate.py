"""Evaluate router for the YUYAY Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from yuyay.exceptions import InvalidResponseError
from yuyay.questionnaire import process_responses

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
        yes_count: Number of YES responses.
        no_count: Number of NO responses.
        po_count: Number of PO responses.
        total: Total responses processed.
        flags: Question ids that returned NO or PO.
        summary: Human readable summary string.
    """

    yes_count: int
    no_count: int
    po_count: int
    total: int
    flags: list[str]
    summary: str


@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(request: EvaluateRequest) -> EvaluateResponse:
    """Submit questionnaire responses and return YES/NO/PO analysis.

    Args:
        request: The request body containing responses dict.

    Returns:
        An EvaluateResponse with counts, flags, and summary.

    Raises:
        HTTPException: 422 if any response value is invalid.
    """
    try:
        report = process_responses(request.responses)
    except InvalidResponseError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return EvaluateResponse(
        yes_count=report.yes_count,
        no_count=report.no_count,
        po_count=report.po_count,
        total=report.total,
        flags=report.flags,
        summary=report.summary(),
    )

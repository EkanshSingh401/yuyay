"""Wheel router for the YUYAY Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from yuyay.wheel import WHEEL_SECTORS, evaluate_whole_system, get_sector

router = APIRouter(prefix="/api/v1/wheel", tags=["wheel"])


class WheelSynthesizeRequest(BaseModel):
    """Request body for the wheel synthesize endpoint.

    Attributes:
        sectors_addressed: List of Co-Creation Wheel sectors being addressed.
        sector: The primary sector to evaluate.
        worldview_alignment: Whether the input aligns with the Worldview center.
    """

    sectors_addressed: list[str]
    sector: str
    worldview_alignment: bool


class WheelSynthesizeResponse(BaseModel):
    """Response body for the wheel synthesize endpoint.

    Attributes:
        sector: The primary sector evaluated.
        worldview_alignment: Whether aligned with Worldview.
        whole_system_score: Score from 0 to 12.
        all_sectors: Full list of valid wheel sectors.
        summary: Human readable summary.
    """

    sector: str
    worldview_alignment: bool
    whole_system_score: int
    all_sectors: list[str]
    summary: str


@router.post("/synthesize")
async def synthesize(request: WheelSynthesizeRequest) -> WheelSynthesizeResponse:
    """Run the Co-Creation Wheel on a set of sectors.

    Args:
        request: The request body with sectors and alignment.

    Returns:
        A WheelSynthesizeResponse with score and summary.

    Raises:
        HTTPException: 404 if the primary sector is not found.
    """
    sector = get_sector(request.sector)
    if sector is None:
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{request.sector}' not found.",
        )
    score = evaluate_whole_system(request.sectors_addressed)
    alignment = "aligned" if request.worldview_alignment else "not aligned"
    summary = f"[{sector}] Worldview: {alignment} | Whole System Score: {score}/12"
    return WheelSynthesizeResponse(
        sector=sector,
        worldview_alignment=request.worldview_alignment,
        whole_system_score=score,
        all_sectors=WHEEL_SECTORS,
        summary=summary,
    )

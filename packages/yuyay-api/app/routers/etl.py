"""ETL router — trigger data pipeline manually."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.db import get_session
from app.etl import run_etl_pipeline

router = APIRouter(prefix="/api/v1", tags=["etl"])


@router.post("/etl/run")
async def run_etl(
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> dict[str, int]:
    """Trigger the ETL pipeline manually.

    Returns:
        Dict with sessions_processed count.
    """
    return await run_etl_pipeline(db)

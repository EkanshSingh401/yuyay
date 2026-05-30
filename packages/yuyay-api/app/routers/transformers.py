"""Transformers router for the YUYAY Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from yuyay.transformers import ALL_TRANSFORMERS, get_transformer_by_id

from app.auth import get_current_user

router = APIRouter(prefix="/api/v1/transformers", tags=["transformers"])


@router.get("/")
async def list_transformers() -> list[dict[str, str]]:
    """Return all 12 transformer questions.

    Returns:
        A list of transformer dicts with id and question.
    """
    return [{"id": t.id, "question": t.question} for t in ALL_TRANSFORMERS]


@router.post("/run")
async def run_transformer(
    transformer_id: str,
    input_text: str,
    current_user: str = Depends(get_current_user),
) -> dict[str, str]:
    """Run a transformer question against input text.

    Args:
        transformer_id: The id of the transformer to run e.g. '1a'.
        input_text: The text to evaluate against the transformer question.

    Returns:
        A dict with the transformer question and input text.

    Raises:
        HTTPException: 404 if transformer not found.
    """
    transformer = get_transformer_by_id(transformer_id)
    if transformer is None:
        raise HTTPException(
            status_code=404,
            detail=f"Transformer '{transformer_id}' not found.",
        )
    return {
        "id": transformer.id,
        "question": transformer.question,
        "input": input_text,
        "summary": transformer.summary(),
    }

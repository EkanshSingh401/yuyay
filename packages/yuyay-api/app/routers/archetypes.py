"""Archetypes router for the YUYAY Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from yuyay.archetypes import ALL_ARCHETYPES, get_archetype_by_name

router = APIRouter(prefix="/api/v1/archetypes", tags=["archetypes"])


@router.get("/")
async def list_archetypes() -> list[dict[str, str | list[str]]]:
    """Return all 12 YUYAY archetypes.

    Returns:
        A list of archetype summaries with name, function, gifts, and shadow.
    """
    return [
        {
            "name": a.name,
            "function": a.function,
            "gifts": a.gifts,
            "shadow": a.shadow,
        }
        for a in ALL_ARCHETYPES
    ]


@router.get("/{name}")
async def get_archetype(name: str) -> dict[str, str | list[str]]:
    """Return a single archetype by name.

    Args:
        name: The archetype name to look up.

    Returns:
        The archetype detail dict.

    Raises:
        HTTPException: 404 if archetype not found.
    """
    archetype = get_archetype_by_name(name)
    if archetype is None:
        raise HTTPException(status_code=404, detail=f"Archetype '{name}' not found.")
    return {
        "name": archetype.name,
        "function": archetype.function,
        "gifts": archetype.gifts,
        "shadow": archetype.shadow,
    }

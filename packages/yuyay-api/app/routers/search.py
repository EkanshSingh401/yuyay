"""Semantic search router — pgvector archetype similarity search."""

from __future__ import annotations

import os

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_user
from app.db import get_session
from app.models import ArchetypeEmbedding

router = APIRouter(prefix="/api/v1/archetypes", tags=["search"])


class SearchRequest(BaseModel):
    """Request body for semantic archetype search.

    Attributes:
        query: Natural language query to search with.
        limit: Maximum number of results to return.
    """

    query: str
    limit: int = 3


class SearchResult(BaseModel):
    """A single semantic search result.

    Attributes:
        archetype_name: Name of the matching archetype.
        description: The archetype description.
        similarity: Cosine similarity score from 0 to 1.
    """

    archetype_name: str
    description: str
    similarity: float


async def get_embedding(text_input: str) -> list[float]:
    """Generate an embedding vector using OpenAI text-embedding-3-small.

    Args:
        text_input: The text to embed.

    Returns:
        A list of 1536 floats representing the embedding vector.
    """
    import openai

    client = openai.AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text_input,
    )
    return response.data[0].embedding


@router.post("/embed")
async def seed_embeddings(
    db: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
) -> dict:
    """Generate and store embeddings for all 12 YUYAY archetypes.

    This endpoint is idempotent — calling it multiple times will
    upsert embeddings rather than creating duplicates.

    Args:
        db: The database session.
        current_user: The authenticated user.

    Returns:
        A dict with the count of embeddings created or updated.
    """
    from yuyay.archetypes import ALL_ARCHETYPES

    await db.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    await db.commit()

    count = 0
    for archetype in ALL_ARCHETYPES:
        description = (
            f"{archetype.name}: {archetype.function}. "
            f"Gifts: {', '.join(archetype.gifts)}. "
            f"Shadow: {archetype.shadow}"
        )
        embedding = await get_embedding(description)

        existing = await db.execute(
            select(ArchetypeEmbedding).where(
                ArchetypeEmbedding.archetype_name == archetype.name
            )
        )
        record = existing.scalar_one_or_none()

        if record:
            record.embedding = embedding
            record.description = description
        else:
            db.add(
                ArchetypeEmbedding(
                    archetype_name=archetype.name,
                    embedding=embedding,
                    description=description,
                )
            )
        count += 1

    await db.commit()
    return {"embeddings_seeded": count}


@router.post("/search", response_model=list[SearchResult])
async def search_archetypes(
    request: SearchRequest,
    db: AsyncSession = Depends(get_session),
    current_user: str = Depends(get_current_user),
) -> list[SearchResult]:
    """Find archetypes semantically similar to the query.

    Embeds the query using text-embedding-3-small and returns
    the most similar archetypes by cosine distance.

    Args:
        request: Search request with query string and limit.
        db: The database session.
        current_user: The authenticated user.

    Returns:
        A list of SearchResult objects ordered by similarity.

    Raises:
        HTTPException: 400 if no embeddings have been seeded yet.
        HTTPException: 500 if the embedding API call fails.
    """
    count = await db.execute(text("SELECT COUNT(*) FROM archetype_embeddings"))
    if count.scalar() == 0:
        raise HTTPException(
            status_code=400,
            detail="No embeddings seeded yet. Call POST /api/v1/archetypes/embed first.",
        )

    try:
        query_embedding = await get_embedding(request.query)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Embedding API call failed: {str(e)}",
        ) from e

    results = await db.execute(
        text("""
            SELECT archetype_name, description,
                   1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
            FROM archetype_embeddings
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """),
        {"embedding": str(query_embedding), "limit": request.limit},
    )

    return [
        SearchResult(
            archetype_name=row.archetype_name,
            description=row.description,
            similarity=round(row.similarity, 4),
        )
        for row in results.fetchall()
    ]

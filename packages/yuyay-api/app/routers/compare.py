"""Compare router — multi-provider FIOS comparison endpoint."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from yuyay.fios import FIOS, FIOSConfig

from app.auth import get_current_user

router = APIRouter(prefix="/api/v1", tags=["compare"])

limiter = Limiter(key_func=get_remote_address)


class ProviderConfig(BaseModel):
    """Configuration for a single provider in a comparison.

    Attributes:
        provider: The LLM provider name.
        model: The specific model to use.
        api_key: The API key for the provider.
    """

    provider: str
    model: str
    api_key: str = ""


class CompareRequest(BaseModel):
    """Request body for the compare endpoint.

    Attributes:
        prompt: The user query to send to all providers.
        providers: List of provider configurations to compare.
    """

    prompt: str
    providers: list[ProviderConfig]


class CompareResult(BaseModel):
    """Result from a single provider in a comparison.

    Attributes:
        provider: The LLM provider used.
        model: The specific model used.
        response: The raw LLM response.
        coherence_score: YUYAY coherence score from 0 to 100.
        flags: List of missing YUYAY concepts.
        total_tokens: Total tokens used.
        latency_ms: Time taken in milliseconds.
        estimated_cost_usd: Estimated cost in USD.
        summary: Human readable summary.
    """

    provider: str
    model: str
    response: str
    coherence_score: int
    flags: list[str]
    total_tokens: int
    latency_ms: float
    estimated_cost_usd: float
    summary: str


class CompareResponse(BaseModel):
    """Response body for the compare endpoint.

    Attributes:
        prompt: The original user query.
        results: List of results from each provider.
        best_provider: The provider with the highest coherence score.
    """

    prompt: str
    results: list[CompareResult]
    best_provider: str


@router.post("/compare", response_model=CompareResponse)
@limiter.limit("5/minute")
async def compare(
    request: Request,
    request_body: CompareRequest,
    current_user: str = Depends(get_current_user),
) -> CompareResponse:
    """Query multiple LLM providers concurrently and compare results.

    Sends the same prompt to all configured providers simultaneously,
    evaluates each response for YUYAY coherence, and returns all results
    with the best provider identified.

    Args:
        request: The incoming HTTP request for rate limiting.
        request_body: The request body with prompt and provider configs.
        current_user: The authenticated user from JWT token.

    Returns:
        A CompareResponse with all provider results and the best provider.

    Raises:
        HTTPException: 400 if no valid providers are configured.
        HTTPException: 429 if rate limit is exceeded.
        HTTPException: 500 if all providers fail.
    """
    if not request_body.providers:
        raise HTTPException(
            status_code=400,
            detail="At least one provider must be configured.",
        )

    configs = [
        FIOSConfig(
            provider=p.provider,
            model=p.model,
            api_key=p.api_key,
        )
        for p in request_body.providers
    ]

    try:
        fios = FIOS(configs[0])
        results = await fios.query_all_providers(request_body.prompt, configs)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Comparison failed: {str(e)}",
        ) from e

    if not results:
        raise HTTPException(
            status_code=500,
            detail="All providers failed to respond.",
        )

    best = max(results, key=lambda r: r.coherence_score)

    return CompareResponse(
        prompt=request_body.prompt,
        results=[
            CompareResult(
                provider=r.provider,
                model=r.model,
                response=r.response,
                coherence_score=r.coherence_score,
                flags=r.flags,
                total_tokens=r.total_tokens,
                latency_ms=r.latency_ms,
                estimated_cost_usd=r.estimated_cost_usd,
                summary=r.summary(),
            )
            for r in results
        ],
        best_provider=best.provider,
    )

"""Query router — FIOS LLM orchestration endpoint for the YUYAY Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from slowapi import Limiter
from tenacity import RetryError
from yuyay.fios import FIOS, FIOSConfig

from app.auth import get_current_user
from app.prometheus import (
    llm_cost_usd_total,
    llm_queries_total,
    llm_query_duration_seconds,
)

router = APIRouter(prefix="/api/v1", tags=["query"])


def get_user_key(request: Request) -> str:
    """Rate limit by user token instead of IP address.
    Falls back to IP if no auth header present.
    """
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return f"user:{auth.split(' ')[1][:20]}"
    return request.client.host if request.client else "unknown"


limiter = Limiter(key_func=get_user_key)


class QueryRequest(BaseModel):
    """Request body for the query endpoint.

    Attributes:
        prompt: The user query to send through FIOS.
        provider: The LLM provider to use — anthropic, openai, google, or mock.
        model: The specific model to use.
        api_key: The API key for the provider.
    """

    prompt: str
    provider: str = "mock"
    model: str = "mock-model"
    api_key: str = ""


class QueryResponse(BaseModel):
    """Response body for the query endpoint.

    Attributes:
        provider: The LLM provider used.
        model: The specific model used.
        prompt: The enriched prompt sent to the LLM.
        response: The raw LLM response.
        input_tokens: Number of input tokens used.
        output_tokens: Number of output tokens used.
        total_tokens: Total tokens used.
        latency_ms: Time taken in milliseconds.
        coherence_score: YUYAY coherence score from 0 to 100.
        flags: List of missing YUYAY concepts.
        estimated_cost_usd: Estimated cost in USD.
        summary: Human readable summary.
    """

    provider: str
    model: str
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency_ms: float
    coherence_score: int
    flags: list[str]
    estimated_cost_usd: float
    summary: str


@router.post("/query", response_model=QueryResponse)
@limiter.limit("3/minute;20/day")
async def query(
    request: Request,
    request_body: QueryRequest,
    current_user: str = Depends(get_current_user),
) -> QueryResponse:
    """Send a prompt through FIOS and return an evaluated LLM response.

    Enriches the prompt with YUYAY framework context, sends it to the
    configured LLM provider, and evaluates the response for coherence.

    Args:
        request: The incoming HTTP request, required by slowapi for rate limiting.
        request_body: The request body with prompt, provider, model, and api_key.
        current_user: The authenticated user from JWT token.

    Returns:
        A QueryResponse with the LLM response and full evaluation metadata.

    Raises:
        HTTPException: 400 if the provider is invalid.
        HTTPException: 429 if rate limit is exceeded.
        HTTPException: 500 if the LLM query fails.
    """
    try:
        config = FIOSConfig(
            provider=request_body.provider,
            model=request_body.model,
            api_key=request_body.api_key,
        )
        fios = FIOS(config)
        result = await fios.query(request_body.prompt)
        llm_queries_total.labels(provider=request_body.provider).inc()
        llm_query_duration_seconds.labels(provider=request_body.provider).observe(
            result.latency_ms / 1000
        )
        llm_cost_usd_total.labels(provider=request_body.provider).inc(
            result.estimated_cost_usd
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RetryError as e:
        cause = e.last_attempt.exception()
        raise HTTPException(
            status_code=500,
            detail=f"LLM query failed after retries: {cause}",
        ) from cause
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"LLM query failed: {str(e)}",
        ) from e

    return QueryResponse(
        provider=result.provider,
        model=result.model,
        prompt=result.prompt,
        response=result.response,
        input_tokens=result.input_tokens,
        output_tokens=result.output_tokens,
        total_tokens=result.total_tokens,
        latency_ms=result.latency_ms,
        coherence_score=result.coherence_score,
        flags=result.flags,
        estimated_cost_usd=result.estimated_cost_usd,
        summary=result.summary(),
    )

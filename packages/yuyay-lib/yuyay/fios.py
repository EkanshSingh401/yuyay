"""FIOS — Foundational Intelligent OS for the YUYAY Intelligence Framework.

FIOS is an LLM orchestration layer that injects YUYAY framework context into
any LLM provider query and evaluates the response against YUYAY coherence metrics.
"""

from __future__ import annotations

import abc
import asyncio
import os
import time
from dataclasses import dataclass, field
from enum import Enum

from tenacity import (
    retry,
    retry_if_not_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from yuyay.archetypes import ALL_ARCHETYPES
from yuyay.transformers import ALL_TRANSFORMERS


@dataclass
class FIOSConfig:
    """Configuration for a FIOS provider.

    Attributes:
        provider: The LLM provider name — anthropic, openai, or google.
        model: The specific model to use.
        max_tokens: Maximum tokens in the response.
        temperature: Sampling temperature from 0.0 to 1.0.
        api_key: The API key for the provider.
    """

    provider: str
    model: str
    max_tokens: int = 1000
    temperature: float = 0.7
    api_key: str = ""


@dataclass
class FIOSResult:
    """Result of a FIOS query.

    Attributes:
        provider: The LLM provider used.
        model: The specific model used.
        prompt: The full enriched prompt sent to the LLM.
        response: The raw response from the LLM.
        input_tokens: Number of input tokens used.
        output_tokens: Number of output tokens used.
        latency_ms: Time taken for the API call in milliseconds.
        coherence_score: YUYAY coherence score from 0 to 100.
        flags: List of coherence issues found in the response.
    """

    provider: str
    model: str
    prompt: str
    response: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    coherence_score: int
    flags: list[str] = field(default_factory=list)
    estimated_cost_usd: float = 0.0

    @property
    def total_tokens(self) -> int:
        """Total tokens used in this query.

        Returns:
            Sum of input and output tokens.
        """
        return self.input_tokens + self.output_tokens

    def summary(self) -> str:
        """Return a formatted summary of this FIOS result.

        Returns:
            A string showing provider, tokens, latency, and coherence score.
        """
        return (
            f"[{self.provider}/{self.model}] "
            f"Tokens: {self.total_tokens} | "
            f"Latency: {self.latency_ms:.0f}ms | "
            f"Coherence: {self.coherence_score}/100 | "
            f"Cost: ${self.estimated_cost_usd:.6f}"
        )


COST_PER_MILLION_TOKENS: dict[str, dict[str, float]] = {
    "anthropic": {"input": 3.0, "output": 15.0},
    "openai": {"input": 30.0, "output": 60.0},
    "google": {"input": 0.075, "output": 0.075},
    "mock": {"input": 0.0, "output": 0.0},
}


def estimate_cost(provider: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate the cost of a query in USD.

    Args:
        provider: The LLM provider name.
        input_tokens: Number of input tokens used.
        output_tokens: Number of output tokens used.

    Returns:
        Estimated cost in USD rounded to 6 decimal places.
    """
    rates = COST_PER_MILLION_TOKENS.get(provider, {"input": 0.0, "output": 0.0})
    input_cost = (input_tokens / 1_000_000) * rates["input"]
    output_cost = (output_tokens / 1_000_000) * rates["output"]
    return round(input_cost + output_cost, 6)


class CircuitState(Enum):
    """States for the circuit breaker pattern.

    Attributes:
        CLOSED: Circuit is closed — requests flow through normally.
        OPEN: Circuit is open — requests are blocked immediately.
        HALF_OPEN: Circuit is testing — one request allowed through.
    """

    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Circuit breaker for LLM provider calls.

    Tracks failures across requests and opens the circuit when too many
    failures occur, preventing cascading failures and wasted resources.

    Attributes:
        failure_threshold: Number of failures before opening the circuit.
        recovery_timeout: Seconds to wait before trying again after opening.
        provider: The provider name this circuit breaker protects.
    """

    def __init__(
        self,
        provider: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
    ) -> None:
        """Initialize the circuit breaker.

        Args:
            provider: The provider name this circuit breaker protects.
            failure_threshold: Failures before opening. Defaults to 5.
            recovery_timeout: Seconds before half-open retry. Defaults to 60.
        """
        self.provider = provider
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float = 0.0

    @property
    def state(self) -> CircuitState:
        """Return the current circuit state, updating if recovery timeout passed.

        Returns:
            The current CircuitState.
        """
        if (
            self._state == CircuitState.OPEN
            and time.monotonic() - self._last_failure_time >= self.recovery_timeout
        ):
            self._state = CircuitState.HALF_OPEN
        return self._state

    def record_success(self) -> None:
        """Record a successful call — reset failure count and close circuit."""
        self._failure_count = 0
        self._state = CircuitState.CLOSED

    def record_failure(self) -> None:
        """Record a failed call — increment count and open circuit if threshold hit."""
        self._failure_count += 1
        self._last_failure_time = time.monotonic()
        if self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN

    def is_open(self) -> bool:
        """Check if the circuit is open and requests should be blocked.

        Returns:
            True if the circuit is open, False otherwise.
        """
        return self.state == CircuitState.OPEN


def build_yuyay_context() -> str:
    """Build the YUYAY framework context string for prompt injection.

    Combines all archetypes and transformer questions into a system context
    that gets prepended to every LLM query.

    Returns:
        A formatted string containing the full YUYAY framework context.
    """
    archetype_context = "\n".join(f"- {a.name}: {a.function}" for a in ALL_ARCHETYPES)
    transformer_context = "\n".join(
        f"- [{t.id}] {t.question}" for t in ALL_TRANSFORMERS
    )
    return f"""You are operating within the YUYAY Intelligence Framework.

YUYAY ARCHETYPES (12 dimensions of human potential):
{archetype_context}

TRANSFORMER QUESTIONS (apply these to your response):
{transformer_context}

When responding, consider all 12 archetype dimensions and apply the transformer
questions to ensure your response serves the highest purpose, is wise, compassionate,
and contributes to healing the planet. Use PO lateral thinking when facing uncertainty."""


def evaluate_coherence(response: str) -> tuple[int, list[str]]:
    """Evaluate a response against YUYAY coherence metrics.

    Checks whether the response demonstrates awareness of key YUYAY concepts
    like wisdom, compassion, purpose, and planetary healing.

    Args:
        response: The raw LLM response text to evaluate.

    Returns:
        A tuple of (score from 0 to 100, list of flags for missing concepts).
    """
    response_lower = response.lower()
    score = 100
    flags: list[str] = []

    checks = [
        ("purpose", ["purpose", "goal", "mission", "serve"]),
        ("wisdom", ["wisdom", "wise", "reflect", "consider"]),
        ("compassion", ["compassion", "empathy", "care", "mercy"]),
        ("planetary", ["planet", "earth", "heal", "future", "generation"]),
        ("balance", ["balance", "harmony", "whole", "system"]),
    ]

    for concept, keywords in checks:
        if not any(kw in response_lower for kw in keywords):
            score -= 20
            flags.append(f"missing_{concept}")

    return max(0, score), flags


class LLMProvider(abc.ABC):
    """Abstract base class for all FIOS LLM provider adapters.

    All concrete provider implementations must inherit from this class
    and implement the query method.
    """

    def __init__(self, config: FIOSConfig) -> None:
        """Initialize the provider with a config.

        Args:
            config: The FIOSConfig for this provider.
        """
        self.config = config
        self.circuit_breaker = CircuitBreaker(provider=config.provider)

    @abc.abstractmethod
    async def query(self, prompt: str) -> FIOSResult:
        """Send a prompt to the LLM and return a FIOSResult.

        Args:
            prompt: The full enriched prompt to send.

        Returns:
            A FIOSResult with the response and metadata.
        """
        ...


class AnthropicAdapter(LLMProvider):
    """FIOS adapter for Anthropic Claude API."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_not_exception_type(RuntimeError),
    )
    async def query(self, prompt: str) -> FIOSResult:
        """Send a prompt to Claude and return a FIOSResult.

        Retries up to 3 times with exponential backoff on failure.

        Args:
            prompt: The full enriched prompt to send.

        Returns:
            A FIOSResult with Claude's response, token usage, and cost.

        Raises:
            RuntimeError: If the circuit breaker is open.
        """
        if self.circuit_breaker.is_open():
            raise RuntimeError(
                f"Circuit breaker open for {self.config.provider} — "
                f"too many failures, try again later."
            )
        try:
            import anthropic

            client = anthropic.AsyncAnthropic(
                api_key=self.config.api_key or os.environ.get("ANTHROPIC_API_KEY")
            )
            context = build_yuyay_context()
            full_prompt = f"{context}\n\nUser Query: {prompt}"

            start = time.monotonic()
            message = await client.messages.create(
                model=self.config.model,
                max_tokens=self.config.max_tokens,
                messages=[{"role": "user", "content": full_prompt}],
            )
            latency_ms = (time.monotonic() - start) * 1000

            response_text = message.content[0].text
            coherence_score, flags = evaluate_coherence(response_text)
            cost = estimate_cost(
                "anthropic",
                message.usage.input_tokens,
                message.usage.output_tokens,
            )
            self.circuit_breaker.record_success()
            return FIOSResult(
                provider="anthropic",
                model=self.config.model,
                prompt=full_prompt,
                response=response_text,
                input_tokens=message.usage.input_tokens,
                output_tokens=message.usage.output_tokens,
                latency_ms=latency_ms,
                coherence_score=coherence_score,
                flags=flags,
                estimated_cost_usd=cost,
            )
        except RuntimeError:
            raise
        except Exception as e:
            self.circuit_breaker.record_failure()
            raise e


class OpenAIAdapter(LLMProvider):
    """FIOS adapter for OpenAI GPT API."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_not_exception_type(RuntimeError),
    )
    async def query(self, prompt: str) -> FIOSResult:
        """Send a prompt to GPT and return a FIOSResult.

        Retries up to 3 times with exponential backoff on failure.

        Args:
            prompt: The full enriched prompt to send.

        Returns:
            A FIOSResult with GPT's response, token usage, and cost.

        Raises:
            RuntimeError: If the circuit breaker is open.
        """
        if self.circuit_breaker.is_open():
            raise RuntimeError(
                f"Circuit breaker open for {self.config.provider} — "
                f"too many failures, try again later."
            )
        try:
            import openai

            client = openai.AsyncOpenAI(
                api_key=self.config.api_key or os.environ.get("OPENAI_API_KEY")
            )
            context = build_yuyay_context()

            start = time.monotonic()
            completion = await client.chat.completions.create(
                model=self.config.model,
                max_completion_tokens=self.config.max_tokens,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": prompt},
                ],
            )
            latency_ms = (time.monotonic() - start) * 1000

            response_text = completion.choices[0].message.content or ""
            input_tokens = completion.usage.prompt_tokens if completion.usage else 0
            output_tokens = (
                completion.usage.completion_tokens if completion.usage else 0
            )
            coherence_score, flags = evaluate_coherence(response_text)
            cost = estimate_cost("openai", input_tokens, output_tokens)
            self.circuit_breaker.record_success()
            return FIOSResult(
                provider="openai",
                model=self.config.model,
                prompt=prompt,
                response=response_text,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
                coherence_score=coherence_score,
                flags=flags,
                estimated_cost_usd=cost,
            )
        except RuntimeError:
            raise
        except Exception as e:
            self.circuit_breaker.record_failure()
            raise e


class GoogleAdapter(LLMProvider):
    """FIOS adapter for Google Gemini API."""

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        retry=retry_if_not_exception_type(RuntimeError),
    )
    async def query(self, prompt: str) -> FIOSResult:
        """Send a prompt to Gemini and return a FIOSResult.

        Retries up to 3 times with exponential backoff on failure.

        Args:
            prompt: The full enriched prompt to send.

        Returns:
            A FIOSResult with Gemini's response and cost.

        Raises:
            RuntimeError: If the circuit breaker is open.
        """
        if self.circuit_breaker.is_open():
            raise RuntimeError(
                f"Circuit breaker open for {self.config.provider} — "
                f"too many failures, try again later."
            )
        try:
            from google import genai

            client = genai.Client(
                api_key=self.config.api_key or os.environ.get("GOOGLE_API_KEY")
            )
            context = build_yuyay_context()
            full_prompt = f"{context}\n\nUser Query: {prompt}"

            start = time.monotonic()
            response = await client.aio.models.generate_content(
                model=self.config.model,
                contents=full_prompt,
            )
            latency_ms = (time.monotonic() - start) * 1000

            response_text = response.text or ""
            coherence_score, flags = evaluate_coherence(response_text)
            usage = response.usage_metadata
            input_tokens = usage.prompt_token_count or 0 if usage else 0
            output_tokens = usage.candidates_token_count or 0 if usage else 0
            cost = estimate_cost("google", input_tokens, output_tokens)
            self.circuit_breaker.record_success()
            return FIOSResult(
                provider="google",
                model=self.config.model,
                prompt=full_prompt,
                response=response_text,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_ms=latency_ms,
                coherence_score=coherence_score,
                flags=flags,
                estimated_cost_usd=cost,
            )
        except RuntimeError:
            raise
        except Exception as e:
            self.circuit_breaker.record_failure()
            raise e


class MockAdapter(LLMProvider):
    """Mock FIOS adapter for testing without real API calls."""

    async def query(self, prompt: str) -> FIOSResult:
        """Return a mock response for testing.

        Args:
            prompt: The prompt — ignored in mock mode.

        Returns:
            A FIOSResult with fake data for testing.

        Raises:
            RuntimeError: If the circuit breaker is open.
        """
        if self.circuit_breaker.is_open():
            raise RuntimeError(
                f"Circuit breaker open for {self.config.provider} — "
                f"too many failures, try again later."
            )
        context = build_yuyay_context()
        mock_response = (
            "This response demonstrates wisdom, compassion, and purpose. "
            "It considers the balance and harmony of whole systems, "
            "and aims to heal the planet for future generations."
        )
        coherence_score, flags = evaluate_coherence(mock_response)
        self.circuit_breaker.record_success()
        return FIOSResult(
            provider="mock",
            model="mock-model",
            prompt=f"{context}\n\nUser Query: {prompt}",
            response=mock_response,
            input_tokens=100,
            output_tokens=50,
            latency_ms=10.0,
            coherence_score=coherence_score,
            flags=flags,
            estimated_cost_usd=0.0,
        )


class FIOS:
    """Foundational Intelligent OS — main orchestrator for LLM queries.

    FIOS manages provider selection, prompt enrichment with YUYAY context,
    response evaluation, and result aggregation.

    Attributes:
        config: The FIOSConfig defining provider and model settings.
        provider: The concrete LLMProvider adapter instance.
    """

    PROVIDER_MAP: dict[str, type[LLMProvider]] = {
        "anthropic": AnthropicAdapter,
        "openai": OpenAIAdapter,
        "google": GoogleAdapter,
        "mock": MockAdapter,
    }

    def __init__(self, config: FIOSConfig) -> None:
        """Initialize FIOS with a provider config.

        Args:
            config: The FIOSConfig specifying which provider and model to use.

        Raises:
            ValueError: If the provider name is not supported.
        """
        if config.provider not in self.PROVIDER_MAP:
            raise ValueError(
                f"Unsupported provider '{config.provider}'. "
                f"Must be one of: {list(self.PROVIDER_MAP.keys())}"
            )
        self.config = config
        self.provider = self.PROVIDER_MAP[config.provider](config)

    async def query(self, prompt: str) -> FIOSResult:
        """Send a prompt through FIOS and return an evaluated result.

        Enriches the prompt with YUYAY context, sends it to the configured
        provider, and evaluates the response for coherence.

        Args:
            prompt: The user query to send.

        Returns:
            A FIOSResult with the response and evaluation metadata.
        """
        return await self.provider.query(prompt)

    async def query_all_providers(
        self,
        prompt: str,
        configs: list[FIOSConfig],
    ) -> list[FIOSResult]:
        """Query multiple LLM providers concurrently and return all results.

        Sends the same prompt to all configured providers simultaneously
        using asyncio.gather for concurrent execution. Results include
        coherence scores for comparison across providers.

        Args:
            prompt: The user query to send to all providers.
            configs: List of FIOSConfig objects for each provider to query.

        Returns:
            A list of FIOSResult objects, one per provider, in the same
            order as the configs list. Failed providers return None results
            are excluded from the output.
        """

        async def query_single(config: FIOSConfig) -> FIOSResult | None:
            """Query a single provider and handle failures gracefully.

            Args:
                config: The FIOSConfig for this provider.

            Returns:
                A FIOSResult or None if the query failed.
            """
            try:
                fios = FIOS(config)
                return await fios.query(prompt)
            except Exception:
                return None

        results = await asyncio.gather(
            *[query_single(config) for config in configs],
        )
        return [r for r in results if r is not None]

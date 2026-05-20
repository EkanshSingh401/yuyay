"""Tests for yuyay.fios — FIOS orchestration layer.

All tests use MockAdapter to avoid real API calls.
Async tests use pytest-asyncio.
"""

from __future__ import annotations

import pytest

from yuyay.fios import (
    FIOS,
    FIOSConfig,
    FIOSResult,
    MockAdapter,
    build_yuyay_context,
    evaluate_coherence,
)

# ── FIOSConfig ───────────────────────────────────────────────────────────────


class TestFIOSConfig:
    def test_required_fields(self) -> None:
        """Provider and model are stored correctly."""
        config = FIOSConfig(provider="mock", model="mock-model")
        assert config.provider == "mock"
        assert config.model == "mock-model"

    def test_defaults(self) -> None:
        """Optional fields have the expected default values."""
        config = FIOSConfig(provider="mock", model="mock-model")
        assert config.max_tokens == 1000
        assert config.temperature == 0.7
        assert config.api_key == ""

    def test_custom_values_override_defaults(self) -> None:
        """Explicitly provided values override every default."""
        config = FIOSConfig(
            provider="anthropic",
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.2,
            api_key="sk-test",
        )
        assert config.max_tokens == 500
        assert config.temperature == 0.2
        assert config.api_key == "sk-test"


# ── FIOSResult ───────────────────────────────────────────────────────────────


class TestFIOSResult:
    def _make_result(self, **kwargs: object) -> FIOSResult:
        """Factory helper — build a FIOSResult with sensible test defaults."""
        defaults: dict[str, object] = dict(
            provider="mock",
            model="mock-model",
            prompt="test prompt",
            response="test response",
            input_tokens=100,
            output_tokens=50,
            latency_ms=10.0,
            coherence_score=80,
            flags=[],
        )
        defaults.update(kwargs)
        return FIOSResult(**defaults)  # type: ignore[arg-type]

    def test_total_tokens(self) -> None:
        """total_tokens returns the sum of input and output tokens."""
        result = self._make_result(input_tokens=100, output_tokens=50)
        assert result.total_tokens == 150

    def test_total_tokens_zero(self) -> None:
        """total_tokens returns 0 when both counts are 0."""
        result = self._make_result(input_tokens=0, output_tokens=0)
        assert result.total_tokens == 0

    def test_summary_contains_provider_and_model(self) -> None:
        """summary() includes the provider/model label."""
        result = self._make_result(provider="mock", model="mock-model")
        assert "mock/mock-model" in result.summary()

    def test_summary_contains_total_tokens(self) -> None:
        """summary() includes the total token count."""
        result = self._make_result(input_tokens=100, output_tokens=50)
        assert "150" in result.summary()

    def test_summary_contains_latency(self) -> None:
        """summary() includes latency rounded to milliseconds."""
        result = self._make_result(latency_ms=123.0)
        assert "123ms" in result.summary()

    def test_summary_contains_coherence_score(self) -> None:
        """summary() includes the coherence score out of 100."""
        result = self._make_result(coherence_score=80)
        assert "80/100" in result.summary()

    def test_flags_default_empty(self) -> None:
        """flags defaults to an empty list when not provided."""
        result = self._make_result()
        assert result.flags == []

    def test_flags_stored_correctly(self) -> None:
        """flags are stored and accessible after construction."""
        result = self._make_result(flags=["missing_wisdom", "missing_compassion"])
        assert "missing_wisdom" in result.flags
        assert "missing_compassion" in result.flags
        assert len(result.flags) == 2

    def test_estimated_cost_defaults_to_zero(self) -> None:
        """estimated_cost_usd defaults to 0.0 when not provided."""
        result = self._make_result()
        assert result.estimated_cost_usd == 0.0

    def test_estimated_cost_stored_correctly(self) -> None:
        """estimated_cost_usd is stored and accessible after construction."""
        result = self._make_result(estimated_cost_usd=0.000045)
        assert result.estimated_cost_usd == 0.000045

    def test_summary_contains_cost(self) -> None:
        """summary() includes the estimated cost."""
        result = self._make_result(estimated_cost_usd=0.000045)
        assert "Cost" in result.summary()


# ── FIOSResult ───────────────────────────────────────────────────────────────


class TestEstimateCost:
    def test_mock_provider_costs_zero(self) -> None:
        """Mock provider always costs zero."""
        from yuyay.fios import estimate_cost

        assert estimate_cost("mock", 1000, 500) == 0.0

    def test_anthropic_cost_calculation(self) -> None:
        """Anthropic cost is calculated correctly per million tokens."""
        from yuyay.fios import estimate_cost

        cost = estimate_cost("anthropic", 1_000_000, 0)
        assert cost == 3.0

    def test_openai_cost_calculation(self) -> None:
        """OpenAI cost is calculated correctly per million tokens."""
        from yuyay.fios import estimate_cost

        cost = estimate_cost("openai", 1_000_000, 0)
        assert cost == 30.0

    def test_unknown_provider_costs_zero(self) -> None:
        """Unknown provider defaults to zero cost."""
        from yuyay.fios import estimate_cost

        assert estimate_cost("unknown", 1000, 500) == 0.0

    def test_cost_rounds_to_six_decimal_places(self) -> None:
        """Cost is rounded to 6 decimal places."""
        from yuyay.fios import estimate_cost

        cost = estimate_cost("anthropic", 100, 50)
        assert len(str(cost).split(".")[-1]) <= 6


# ── build_yuyay_context ──────────────────────────────────────────────────────


class TestBuildYuyayContext:
    def test_returns_string(self) -> None:
        """build_yuyay_context() returns a non-empty string."""
        ctx = build_yuyay_context()
        assert isinstance(ctx, str)
        assert len(ctx) > 0

    def test_contains_yuyay_header(self) -> None:
        """Output includes the YUYAY framework header."""
        ctx = build_yuyay_context()
        assert "YUYAY" in ctx

    def test_contains_all_archetype_names(self) -> None:
        """Every archetype name from ALL_ARCHETYPES appears in the context."""
        from yuyay.archetypes import ALL_ARCHETYPES

        ctx = build_yuyay_context()
        for archetype in ALL_ARCHETYPES:
            assert archetype.name in ctx, f"Missing archetype: {archetype.name}"

    def test_contains_all_transformer_ids(self) -> None:
        """Every transformer ID from ALL_TRANSFORMERS appears in the context."""
        from yuyay.transformers import ALL_TRANSFORMERS

        ctx = build_yuyay_context()
        for transformer in ALL_TRANSFORMERS:
            assert (
                str(transformer.id) in ctx
            ), f"Missing transformer id: {transformer.id}"

    def test_contains_po_mention(self) -> None:
        """PO lateral thinking is referenced in the context."""
        ctx = build_yuyay_context()
        assert "PO" in ctx

    def test_contains_archetype_section_header(self) -> None:
        """The archetypes section header is present."""
        ctx = build_yuyay_context()
        assert "YUYAY ARCHETYPES" in ctx

    def test_contains_transformer_section_header(self) -> None:
        """The transformer questions section header is present."""
        ctx = build_yuyay_context()
        assert "TRANSFORMER QUESTIONS" in ctx


# ── evaluate_coherence ───────────────────────────────────────────────────────


class TestEvaluateCoherence:
    def test_perfect_score_all_concepts_present(self) -> None:
        """A response hitting all 5 concepts scores 100 with no flags."""
        response = (
            "With wisdom and purpose, we serve with compassion "
            "to heal the planet and restore balance."
        )
        score, flags = evaluate_coherence(response)
        assert score == 100
        assert flags == []

    def test_missing_one_concept_deducts_20(self) -> None:
        """Each missing concept deducts exactly 20 points."""
        # Has: wisdom, compassion, planetary, balance — missing: purpose
        response = (
            "With wisdom and compassion we heal the planet "
            "and maintain balance and harmony."
        )
        score, flags = evaluate_coherence(response)
        assert score == 80
        assert "missing_purpose" in flags
        assert len(flags) == 1

    def test_missing_all_concepts_returns_zero(self) -> None:
        """A response with none of the concepts scores 0."""
        response = "The quick brown fox jumps over the lazy dog."
        score, flags = evaluate_coherence(response)
        assert score == 0
        assert len(flags) == 5

    def test_all_five_flag_names_on_empty_response(self) -> None:
        """All five expected flag names are returned when everything is missing."""
        _, flags = evaluate_coherence("The quick brown fox jumps over the lazy dog.")
        expected = {
            "missing_purpose",
            "missing_wisdom",
            "missing_compassion",
            "missing_planetary",
            "missing_balance",
        }
        assert set(flags) == expected

    def test_case_insensitive_matching(self) -> None:
        """Keywords are matched regardless of capitalisation."""
        response = "WISDOM and COMPASSION guide our PURPOSE toward BALANCE and HEALING the PLANET."
        score, flags = evaluate_coherence(response)
        assert score == 100
        assert flags == []

    def test_score_cannot_go_below_zero(self) -> None:
        """Score is floored at 0 even for an empty string."""
        score, _ = evaluate_coherence("")
        assert score >= 0

    def test_alternate_keywords_trigger_concept(self) -> None:
        """Synonyms like 'serve' and 'goal' satisfy the purpose check."""
        response = "Our goal is to serve, reflect with care, future generations on earth, whole system."
        score, flags = evaluate_coherence(response)
        assert score == 100
        assert flags == []


# ── MockAdapter ──────────────────────────────────────────────────────────────


class TestMockAdapter:
    @pytest.mark.asyncio
    async def test_query_returns_fios_result(self) -> None:
        """query() returns a FIOSResult instance."""
        config = FIOSConfig(provider="mock", model="mock-model")
        result = await MockAdapter(config).query("test prompt")
        assert isinstance(result, FIOSResult)

    @pytest.mark.asyncio
    async def test_query_provider_is_mock(self) -> None:
        """Result provider and model fields match the config."""
        config = FIOSConfig(provider="mock", model="mock-model")
        result = await MockAdapter(config).query("anything")
        assert result.provider == "mock"
        assert result.model == "mock-model"

    @pytest.mark.asyncio
    async def test_query_prompt_contains_user_input(self) -> None:
        """The user's question appears somewhere in the enriched prompt."""
        config = FIOSConfig(provider="mock", model="mock-model")
        result = await MockAdapter(config).query("what is the meaning of life?")
        assert "what is the meaning of life?" in result.prompt

    @pytest.mark.asyncio
    async def test_query_prompt_contains_yuyay_context(self) -> None:
        """The enriched prompt also contains the YUYAY framework context."""
        config = FIOSConfig(provider="mock", model="mock-model")
        result = await MockAdapter(config).query("test")
        assert "YUYAY" in result.prompt

    @pytest.mark.asyncio
    async def test_query_token_counts(self) -> None:
        """Mock token counts are exactly 100 input and 50 output."""
        config = FIOSConfig(provider="mock", model="mock-model")
        result = await MockAdapter(config).query("test")
        assert result.input_tokens == 100
        assert result.output_tokens == 50

    @pytest.mark.asyncio
    async def test_query_latency_is_positive(self) -> None:
        """Latency value is a positive number."""
        config = FIOSConfig(provider="mock", model="mock-model")
        result = await MockAdapter(config).query("test")
        assert result.latency_ms > 0

    @pytest.mark.asyncio
    async def test_query_perfect_coherence_score(self) -> None:
        """The mock response is crafted to achieve a perfect coherence score."""
        config = FIOSConfig(provider="mock", model="mock-model")
        result = await MockAdapter(config).query("test")
        assert result.coherence_score == 100
        assert result.flags == []


# ── FIOS (main orchestrator) ─────────────────────────────────────────────────


class TestFIOS:
    def test_init_valid_provider_stores_config(self) -> None:
        """Config is stored on the instance after a valid init."""
        config = FIOSConfig(provider="mock", model="mock-model")
        fios = FIOS(config)
        assert fios.config == config

    def test_init_valid_provider_creates_correct_adapter(self) -> None:
        """Using provider='mock' creates a MockAdapter instance."""
        config = FIOSConfig(provider="mock", model="mock-model")
        fios = FIOS(config)
        assert isinstance(fios.provider, MockAdapter)

    def test_init_invalid_provider_raises_value_error(self) -> None:
        """An unrecognised provider name raises ValueError."""
        config = FIOSConfig(provider="banana", model="banana-3")
        with pytest.raises(ValueError, match="Unsupported provider"):
            FIOS(config)

    def test_init_invalid_provider_error_lists_valid_options(self) -> None:
        """The ValueError message names at least one valid provider."""
        config = FIOSConfig(provider="banana", model="banana-3")
        with pytest.raises(ValueError, match="anthropic"):
            FIOS(config)

    def test_provider_map_contains_all_four_providers(self) -> None:
        """PROVIDER_MAP contains exactly the four expected keys."""
        expected = {"anthropic", "openai", "google", "mock"}
        assert set(FIOS.PROVIDER_MAP.keys()) == expected

    @pytest.mark.asyncio
    async def test_query_returns_fios_result(self) -> None:
        """FIOS.query() returns a FIOSResult."""
        config = FIOSConfig(provider="mock", model="mock-model")
        fios = FIOS(config)
        result = await fios.query("test question")
        assert isinstance(result, FIOSResult)

    @pytest.mark.asyncio
    async def test_query_delegates_to_provider(self) -> None:
        """FIOS.query() passes the prompt through to the underlying provider."""
        config = FIOSConfig(provider="mock", model="mock-model")
        fios = FIOS(config)
        result = await fios.query("what is wisdom?")
        assert result.provider == "mock"
        assert "what is wisdom?" in result.prompt

    @pytest.mark.asyncio
    async def test_query_result_has_coherence_score(self) -> None:
        """The returned FIOSResult always has a coherence_score between 0 and 100."""
        config = FIOSConfig(provider="mock", model="mock-model")
        fios = FIOS(config)
        result = await fios.query("test")
        assert 0 <= result.coherence_score <= 100


# ── Real Adapters (mocked) ───────────────────────────────────────────────────


class TestAnthropicAdapter:
    @pytest.mark.asyncio
    async def test_query_returns_fios_result(self) -> None:
        """AnthropicAdapter.query() returns a FIOSResult using a mocked client."""
        from unittest.mock import AsyncMock, MagicMock, patch

        mock_message = MagicMock()
        mock_message.content = [
            MagicMock(text="wisdom compassion purpose balance heal planet")
        ]
        mock_message.usage.input_tokens = 200
        mock_message.usage.output_tokens = 80

        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(return_value=mock_message)

        mock_anthropic = MagicMock()
        mock_anthropic.AsyncAnthropic.return_value = mock_client

        with patch.dict("sys.modules", {"anthropic": mock_anthropic}):
            from yuyay.fios import AnthropicAdapter

            config = FIOSConfig(
                provider="anthropic",
                model="claude-3-5-sonnet-20241022",
                api_key="sk-fake",
            )
            adapter = AnthropicAdapter(config)
            result = await adapter.query("test prompt")

        assert isinstance(result, FIOSResult)
        assert result.provider == "anthropic"
        assert result.input_tokens == 200
        assert result.output_tokens == 80

    @pytest.mark.asyncio
    async def test_query_prompt_contains_user_input(self) -> None:
        """AnthropicAdapter includes the user query in the enriched prompt."""
        from unittest.mock import AsyncMock, MagicMock, patch

        mock_message = MagicMock()
        mock_message.content = [
            MagicMock(text="wisdom compassion purpose balance heal planet")
        ]
        mock_message.usage.input_tokens = 100
        mock_message.usage.output_tokens = 50

        mock_client = MagicMock()
        mock_client.messages.create = AsyncMock(return_value=mock_message)

        mock_anthropic = MagicMock()
        mock_anthropic.AsyncAnthropic.return_value = mock_client

        with patch.dict("sys.modules", {"anthropic": mock_anthropic}):
            from yuyay.fios import AnthropicAdapter

            config = FIOSConfig(
                provider="anthropic",
                model="claude-3-5-sonnet-20241022",
                api_key="sk-fake",
            )
            adapter = AnthropicAdapter(config)
            result = await adapter.query("what is wisdom?")

        assert "what is wisdom?" in result.prompt


class TestOpenAIAdapter:
    @pytest.mark.asyncio
    async def test_query_returns_fios_result(self) -> None:
        """OpenAIAdapter.query() returns a FIOSResult using a mocked client."""
        from unittest.mock import AsyncMock, MagicMock, patch

        mock_choice = MagicMock()
        mock_choice.message.content = "wisdom compassion purpose balance heal planet"

        mock_usage = MagicMock()
        mock_usage.prompt_tokens = 150
        mock_usage.completion_tokens = 60

        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_completion.usage = mock_usage

        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)

        mock_openai = MagicMock()
        mock_openai.AsyncOpenAI.return_value = mock_client

        with patch.dict("sys.modules", {"openai": mock_openai}):
            from yuyay.fios import OpenAIAdapter

            config = FIOSConfig(provider="openai", model="gpt-4", api_key="sk-fake")
            adapter = OpenAIAdapter(config)
            result = await adapter.query("test prompt")

        assert isinstance(result, FIOSResult)
        assert result.provider == "openai"
        assert result.input_tokens == 150
        assert result.output_tokens == 60

    @pytest.mark.asyncio
    async def test_query_handles_none_usage(self) -> None:
        """OpenAIAdapter defaults token counts to 0 when usage is None."""
        from unittest.mock import AsyncMock, MagicMock, patch

        mock_choice = MagicMock()
        mock_choice.message.content = "wisdom compassion purpose balance heal planet"

        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]
        mock_completion.usage = None

        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)

        mock_openai = MagicMock()
        mock_openai.AsyncOpenAI.return_value = mock_client

        with patch.dict("sys.modules", {"openai": mock_openai}):
            from yuyay.fios import OpenAIAdapter

            config = FIOSConfig(provider="openai", model="gpt-4", api_key="sk-fake")
            adapter = OpenAIAdapter(config)
            result = await adapter.query("test prompt")

        assert result.input_tokens == 0
        assert result.output_tokens == 0


# pragma: no cover for class TestGoogleAdapter

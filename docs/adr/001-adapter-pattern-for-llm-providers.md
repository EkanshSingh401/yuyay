# ADR-001: Adapter Pattern for LLM Providers

**Status:** Accepted  
**Date:** 2026-03  
**Author:** Ekansh Singh

## Context

FIOS needs to support multiple LLM providers — Anthropic, OpenAI, and Google Gemini. Each has a different SDK, different API shapes, different authentication, and different response formats. We needed a way to abstract across all three so the business logic (YUYAY context injection, coherence scoring) doesn't care which provider is used.

## Decision

Use the **adapter pattern** — an abstract base class `BaseFIOSAdapter` with a single `query()` method, and three concrete implementations: `AnthropicAdapter`, `OpenAIAdapter`, `GoogleAdapter`. The `FIOS` class accepts a config and instantiates the right adapter internally.

## Alternatives Considered

**Hardcoded provider logic with if/else** — simple but violates open/closed principle. Adding a fourth provider would require modifying existing code.

**LangChain** — provides provider abstraction but adds a heavy dependency with its own abstractions that don't map cleanly to YUYAY's evaluation pipeline. Overkill for our use case.

**LiteLLM** — lightweight provider abstraction, but we needed custom coherence scoring and YUYAY context injection that are easier to implement in our own adapter layer.

## Consequences

- Adding a new provider requires only a new adapter class — no changes to existing code
- Each adapter can be tested independently with mocks
- Provider-specific features (streaming, function calling) can be exposed without breaking the common interface
- Slightly more boilerplate than a direct integration
# ADR-002: FastAPI over Django for REST API

**Status:** Accepted  
**Date:** 2026-03  
**Author:** Ekansh Singh

## Context

We needed a Python web framework for the REST API. The two main options were FastAPI and Django REST Framework.

## Decision

Use **FastAPI** with Pydantic v2 for request/response validation.

## Alternatives Considered

**Django REST Framework** — battle-tested, large ecosystem, built-in admin panel. However it uses synchronous ORM by default, has heavier overhead for a pure API service, and its request validation is less ergonomic than Pydantic v2.

**Flask** — lightweight but requires adding many libraries manually (validation, serialization, OpenAPI). More assembly required.

## Consequences

- Automatic OpenAPI spec generation and Swagger UI at /docs with zero configuration
- Native async support enables concurrent LLM queries via asyncio
- Pydantic v2 validation is faster and more expressive than DRF serializers
- Smaller community than Django for some edge cases
- No built-in admin panel (acceptable — we built our own analytics)
# ADR-003: PostgreSQL with Async SQLAlchemy

**Status:** Accepted  
**Date:** 2026-03  
**Author:** Ekansh Singh

## Context

We needed a persistent data store for evaluation sessions, archetype scores, FIOS queries, and analytics. The choice was between a managed relational database and alternatives like MongoDB or a pure ORM approach.

## Decision

Use **PostgreSQL** as the database with **SQLAlchemy 2.0 async** as the ORM layer and **Alembic** for migrations. SQLite for local development.

## Alternatives Considered

**MongoDB** — flexible schema is appealing for early-stage projects but YUYAY's evaluation data is highly structured and relational (sessions → archetype scores → analytics). A relational schema is a better fit.

**Supabase** — managed PostgreSQL with a nice dashboard, but Railway's integrated PostgreSQL is simpler to configure in the same deployment environment.

**Synchronous SQLAlchemy** — simpler to reason about, but blocks the event loop during database queries. Since we're already using async FastAPI and async LLM calls, async SQLAlchemy was the consistent choice.

## Consequences

- Full ACID compliance for evaluation data integrity
- Alembic migrations provide a versioned, reproducible schema evolution path
- Async SQLAlchemy requires careful handling of lazy loading (use `noload` for relationships not needed in the request path)
- SQLite fallback for local dev eliminates the need for a local PostgreSQL install
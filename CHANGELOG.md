# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-05-27

### Added
- Docker multi-stage Dockerfile for API
- Docker Compose with PostgreSQL for local development
- Deployed API to Railway with managed PostgreSQL
- JWT authentication with bcrypt
- Rate limiting via slowapi with per-endpoint limits
- Alembic database migrations
- Structured logging via structlog
- API integration tests — 52 tests passing
- POST /api/v1/query FIOS endpoint wiring FIOS to API
- Circuit breaker pattern in FIOS
- Cost estimation per LLM provider
- Retry logic with exponential backoff
- All 11 API endpoints complete

## [0.1.0] - 2026-04-26

### Added
- `archetypes.py` — 12 YUYAY archetypes with light/shadow aspects
- `transformers.py` — 10 transformer questions with lookup function
- `wheel.py` — Co-Creation Wheel integration engine with 12 sectors
- `questionnaire.py` — YES/NO/PO response processor with scoring
- `po.py` — Edward de Bono PO lateral thinking logic
- `exceptions.py` — custom exception hierarchy
- `config.py` — environment-based configuration management
- 100% test coverage across all modules
- pre-commit hooks with black, ruff, mypy, isort
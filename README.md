# YUYAY Intelligence Framework

[![CI](https://github.com/EkanshSingh401/yuyay/actions/workflows/ci.yml/badge.svg)](https://github.com/EkanshSingh401/yuyay/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)](https://github.com/EkanshSingh401/yuyay)
[![PyPI version](https://img.shields.io/pypi/v/yuyay)](https://pypi.org/project/yuyay/)
[![Python versions](https://img.shields.io/pypi/pyversions/yuyay)](https://pypi.org/project/yuyay/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-github--pages-blue)](https://ekanshsingh401.github.io/yuyay/)
[![License](https://img.shields.io/badge/license-MIT-blue)](https://github.com/EkanshSingh401/yuyay/blob/main/LICENSE)

A multi-dimensional intelligence framework for evaluating alignment across 12 archetype dimensions — developed for the UN Office of the Future by Mitchell Gold.

**Live platform:** [unofficeofthefuture.org](https://www.unofficeofthefuture.org)  
**API docs:** [yuyay-production-2e45.up.railway.app/docs](https://yuyay-production-2e45.up.railway.app/docs)  
**PyPI:** [pypi.org/project/yuyay](https://pypi.org/project/yuyay/)  
**GitHub:** [github.com/EkanshSingh401/yuyay](https://github.com/EkanshSingh401/yuyay)
- **Docs:** [ekanshsingh401.github.io/yuyay](https://ekanshsingh401.github.io/yuyay/)

---

## Overview

YUYAY — from the Quechua word for knowledge — is a self-assessment framework built on twelve dimensions of human potential. From Vision and Structure to Compassion and Planetary Stewardship, every decision can be weighed against the full spectrum of what it means to act wisely in the world.

The framework integrates:
- **12 Archetypes** — dimensions of human potential with gifts and shadows
- **10 Transformer Questions** — YES/NO/PO self-reflection evaluation
- **Co-Creation Wheel** — 12 societal sectors for whole-system thinking
- **PO Lateral Thinking** — Edward de Bono's provocation operator
- **FIOS** — Foundational Intelligent OS for LLM orchestration

---

## Architecture
┌─────────────────────────────────────────────────────────┐
│                    Next.js Frontend                      │
│          unofficeofthefuture.org (Vercel)               │
└──────────────────────┬──────────────────────────────────┘
│ HTTPS
┌──────────────────────▼──────────────────────────────────┐
│                  FastAPI Backend                         │
│         yuyay-production-2e45.up.railway.app            │
│                                                          │
│  ┌─────────────┐  ┌──────────┐  ┌─────────────────────┐ │
│  │  Evaluate   │  │  FIOS    │  │    ETL Pipeline     │ │
│  │  Endpoint   │  │  Query   │  │  Extract→Transform  │ │
│  └─────────────┘  └──────────┘  │    →Load→Validate   │ │
│                                  └─────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
│
┌──────────────────────▼──────────────────────────────────┐
│              PostgreSQL (Railway)                        │
│  evaluation_sessions │ archetype_scores                 │
│  transformer_results │ fios_queries                     │
│  archetype_analytics │ daily_metrics                    │
└─────────────────────────────────────────────────────────┘
│
┌──────────────────────▼──────────────────────────────────┐
│           yuyay Python Library (PyPI)                   │
│  archetypes │ transformers │ wheel │ fios │ po          │
└─────────────────────────────────────────────────────────┘

**Three-layer architecture:**

- **Library** (`pip install yuyay`) — domain logic, published to PyPI, used by both the API and directly via CLI
- **API** (FastAPI + PostgreSQL) — REST service with JWT auth, rate limiting, ETL pipeline, Prometheus metrics
- **Frontend** (Next.js) — interactive evaluation tool, session history, multi-provider LLM queries

---

## Quickstart

### Install the library

```bash
pip install yuyay
```

### Use the CLI

```bash
# List all 12 archetypes
yuyay archetypes

# List all 10 transformer questions
yuyay transformers

# Run an evaluation
yuyay evaluate --responses "1a=YES,1b=NO,2a=PO,2b=YES,3=NO,4=YES,5=NO,6=PO,7=YES,8=NO,9=YES,10=NO"

# Query the FIOS intelligence layer
yuyay query --prompt "What is wisdom?" --provider anthropic
```

### Use the Python API

```python
from yuyay.questionnaire import process_responses
from yuyay.fios import FIOS, FIOSConfig

# Run an evaluation
report = process_responses({"1a": "YES", "1b": "NO", "2a": "PO"})
print(report.yes_count, report.no_count, report.po_count)
print(report.flags)

# Query FIOS
config = FIOSConfig(provider="anthropic", model="claude-sonnet-4-6")
fios = FIOS(config)
result = await fios.query("What does it mean to act with wisdom?")
print(result.response)
print(f"Coherence: {result.coherence_score}/100")
```

---

## API Reference

Base URL: `https://yuyay-production-2e45.up.railway.app`

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/evaluate` | Submit YES/NO/PO responses, get analysis |
| POST | `/api/v1/query` | Query FIOS LLM layer with YUYAY context |
| POST | `/api/v1/compare` | Compare same query across multiple providers |
| GET | `/api/v1/archetypes` | List all 12 archetypes |
| POST | `/api/v1/transformers/run` | Run a transformer question |
| GET | `/api/v1/wheel/synthesize` | Run Co-Creation Wheel synthesis |
| GET | `/api/v1/sessions` | List evaluation sessions |
| GET | `/api/v1/sessions/{id}` | Get session detail |
| POST | `/api/v1/etl/run` | Trigger ETL pipeline |
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/metrics` | Platform metrics |
| GET | `/api/v1/prometheus` | Prometheus metrics endpoint |
| GET | `/api/v1/archetypes/{name}` | Get single archetype by name |
| GET | `/api/v1/sessions/{id}` | Get session detail |

Full interactive docs at [/docs](https://yuyay-production-2e45.up.railway.app/docs).

---

## Library Modules

| Module | Purpose |
|--------|---------|
| `archetypes.py` | 12 YUYAY archetypes with light/shadow aspects |
| `transformers.py` | 10 self-reflection transformer questions |
| `wheel.py` | Co-Creation Wheel integration engine |
| `questionnaire.py` | YES/NO/PO response processor with scoring |
| `po.py` | Edward de Bono PO lateral thinking operator |
| `fios.py` | FIOS LLM orchestration layer (OpenAI, Anthropic, Google) |
| `exceptions.py` | Custom exception hierarchy |
| `config.py` | Configuration management |
| `cli.py` | Typer CLI tool |

---

## Development Setup

See [CONTRIBUTING.md](CONTRIBUTING.md) for full setup instructions.

```bash
# Library
cd packages/yuyay-lib && pip install -e ".[dev]"

# API
cd packages/yuyay-api && pip install -e ".[dev]"
uvicorn app.main:app --reload

# Frontend
cd packages/yuyay-web && npm install && npm run dev
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+, TypeScript |
| API Framework | FastAPI + Pydantic v2 |
| Frontend | Next.js 16 + Tailwind CSS |
| Database | PostgreSQL + SQLAlchemy 2.0 async |
| Migrations | Alembic |
| Auth | Clerk + JWT |
| LLM Providers | OpenAI, Anthropic, Google Gemini |
| Monitoring | Prometheus + Grafana Cloud |
| Error Tracking | Sentry |
| CI/CD | GitHub Actions |
| Hosting | Railway (API) + Vercel (frontend) |
| Package | PyPI |

---

## Metrics

- **13,285** total lines of code
- **90%+** test coverage
- **8** PostgreSQL tables
- **15** API endpoints
- **3** LLM providers
- **12** archetype dimensions
- **227MB** Docker image (multi-stage build)
- **p95 response time:** 230ms (health/simple endpoints), 400ms (DB-backed endpoints)
- **Throughput:** 4.4 req/s under 10 concurrent users, 0% error rate
- **Load tested** with Locust — 127 requests, 0 failures across 10 concurrent users

---

## License

MIT — see [LICENSE](LICENSE).
## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker + Docker Compose
- Git

---

## Setting Up the Library

```bash
cd packages/yuyay-lib
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

Run tests:

```bash
pytest --cov=yuyay --cov-report=term-missing
```

---

## Setting Up the API

```bash
cd packages/yuyay-api
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Copy the environment file and fill in your keys:

```bash
cp .env.example .env
```

Run the API locally:

```bash
uvicorn app.main:app --reload
```

Run migrations:

```bash
alembic upgrade head
```

Run tests:

```bash
pytest
```

---

## Setting Up the Frontend

```bash
cd packages/yuyay-web
npm install
npm run dev
```

---

## Code Standards

All Python code must pass:

- **black** — formatting
- **ruff** — linting
- **mypy** — strict type checking
- **isort** — import ordering

These run automatically via pre-commit hooks. To run manually:

```bash
black .
ruff check .
mypy .
isort .
```

---

## Submitting Changes

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make your changes with tests
3. Ensure all pre-commit hooks pass: `git commit`
4. Push and open a pull request against `main`
5. CI must pass before merging

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `CLERK_JWKS_URL` | Clerk JWKS endpoint for JWT verification |
| `ANTHROPIC_API_KEY` | Anthropic API key for FIOS |
| `OPENAI_API_KEY` | OpenAI API key for FIOS |
| `GOOGLE_API_KEY` | Google API key for FIOS |
| `SENTRY_DSN` | Sentry DSN for error tracking |
| `GRAFANA_API_TOKEN` | Grafana Cloud API token |

---

## Questions

Open an issue or reach out via the repository.
# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install the yuyay library first
COPY yuyay-lib /app/yuyay-lib
RUN pip install --no-cache-dir /app/yuyay-lib

# Copy API dependencies and install
COPY yuyay-api/pyproject.toml .
RUN pip install --no-cache-dir ".[dev]"

# Copy application code
COPY yuyay-api/app ./app
COPY yuyay-api/alembic ./alembic
COPY yuyay-api/alembic.ini .
COPY yuyay-api/alloy ./alloy

# ── Stage 2: Production ───────────────────────────────────────────────────────
FROM python:3.12-slim AS production

WORKDIR /app

# Create non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Install Grafana Alloy
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    && wget -q https://github.com/grafana/alloy/releases/latest/download/alloy-linux-amd64.zip -O alloy.zip \
    && unzip alloy.zip \
    && mv alloy /usr/local/bin/alloy \
    && chmod +x /usr/local/bin/alloy \
    && rm alloy.zip \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=builder /app/app ./app
COPY --from=builder /app/alembic ./alembic
COPY --from=builder /app/alembic.ini .
COPY --from=builder /app/alloy ./alloy

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run Alloy and uvicorn together
CMD ["sh", "-c", "alloy run ./alloy/config.alloy & uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
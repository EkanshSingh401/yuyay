# ADR-005: Railway for API Deployment

**Status:** Accepted  
**Date:** 2026-04  
**Author:** Ekansh Singh

## Context

The FastAPI backend needed a hosting platform that could run Docker containers, provide managed PostgreSQL, and support zero-downtime deploys from GitHub.

## Decision

Use **Railway** for the API and PostgreSQL, **Vercel** for the Next.js frontend.

## Alternatives Considered

**AWS (EC2 + RDS)** — maximum control and the Anduril signal, but significant ops overhead for a solo internship project. VPC setup, IAM roles, security groups — weeks of work before the first deploy.

**Heroku** — familiar but removed its free tier. Paid plans start higher than Railway.

**Fly.io** — strong Docker support and good free tier, but Railway's integrated PostgreSQL and GitHub deploy integration are simpler for this use case.

**Render** — similar to Railway but slightly less ergonomic GitHub integration.

## Consequences

- GitHub push triggers automatic deploy with zero configuration
- Integrated PostgreSQL on the same private network as the API (no external DB connection)
- Grafana Alloy for metrics shipping required subprocess management since Railway doesn't support multi-process containers natively
- $5/month base cost, reimbursed by the project
- Private networking via `.railway.internal` DNS for DB connection security
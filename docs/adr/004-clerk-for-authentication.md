# ADR-004: Clerk for Authentication

**Status:** Accepted  
**Date:** 2026-04  
**Author:** Ekansh Singh

## Context

The platform needed user authentication for protecting the /evaluate, /query, /sessions, and /compare endpoints. We needed sign-up, sign-in, session management, and JWT token issuance.

## Decision

Use **Clerk** for authentication with JWT verification via **python-jose** on the API side.

## Alternatives Considered

**Rolling our own auth** — bcrypt passwords, JWT issuance, session management. Significant scope and security risk for a 6-month project. Auth is not a differentiator here.

**Auth0** — industry standard but more complex configuration and higher cost at scale.

**Supabase Auth** — tightly coupled to Supabase's database offering, which we weren't using.

## Consequences

- Sign-up, sign-in, OAuth, and session management handled entirely by Clerk
- Frontend integration via @clerk/nextjs is seamless with Next.js App Router
- API verifies JWTs against Clerk's JWKS endpoint — stateless, scalable
- Production domain configuration (unofficeofthefuture.org) required DNS CNAME setup
- Token expiry of 60 seconds requires fresh tokens for each API call in testing
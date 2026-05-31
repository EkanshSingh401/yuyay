"""Clerk JWT authentication for the YUYAY Intelligence API."""

from __future__ import annotations

import os
from typing import Any

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWT
from jwt.algorithms import RSAAlgorithm

CLERK_JWKS_URL = os.environ.get(
    "CLERK_JWKS_URL",
    "https://grown-reptile-47.clerk.accounts.dev/.well-known/jwks.json",
)

security = HTTPBearer()

_jwks_cache: dict[str, Any] | None = None


async def get_jwks() -> dict[str, Any]:
    """Fetch Clerk's public keys for JWT verification.

    Caches the keys in memory to avoid fetching on every request.

    Returns:
        The JWKS dict containing Clerk's public keys.
    """
    global _jwks_cache
    if _jwks_cache is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(CLERK_JWKS_URL)
            response.raise_for_status()
            _jwks_cache = response.json()
    return _jwks_cache


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Verify a Clerk JWT token and return the user ID.

    Args:
        credentials: The Bearer token from the Authorization header.

    Returns:
        The Clerk user ID (sub claim) from the verified token.

    Raises:
        HTTPException: 401 if the token is invalid or expired.
    """
    token = credentials.credentials
    try:
        jwks = await get_jwks()
        signing_key = RSAAlgorithm.from_jwk(
            next(key for key in jwks["keys"] if key.get("use") == "sig")
        )
        payload = PyJWT().decode(
            token,
            signing_key,
            algorithms=["RS256"],
            options={"verify_aud": False},
        )
        user_id: str = payload.get("sub", "")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token — no subject claim.",
            )
        return user_id
    except StopIteration:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No signing key found in JWKS.",
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
        )

"""Authentication router for the YUYAY Intelligence API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.auth import FAKE_USERS_DB, create_access_token, decode_token, verify_password

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

limiter = Limiter(key_func=get_remote_address)


class Token(BaseModel):
    """Response body for the login endpoint.

    Attributes:
        access_token: The signed JWT token string.
        token_type: Always 'bearer' for JWT.
    """

    access_token: str
    token_type: str


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Dependency that extracts and validates the current user from a JWT token.

    Args:
        token: The JWT token from the Authorization header.

    Returns:
        The username of the authenticated user.

    Raises:
        HTTPException: 401 if the token is invalid or expired.
    """
    username = decode_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """Authenticate a user and return a JWT access token.

    Args:
        request: The incoming HTTP request, required by slowapi for rate limiting.
        form_data: The username and password from the request form.

    Returns:
        A Token with the access token and token type.

    Raises:
        HTTPException: 401 if credentials are invalid.
        HTTPException: 429 if rate limit is exceeded.
    """
    user = FAKE_USERS_DB.get(form_data.username)
    if user is None or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": form_data.username})
    return Token(access_token=token, token_type="bearer")

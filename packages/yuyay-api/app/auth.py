"""JWT authentication for the YUYAY Intelligence API."""

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt

SECRET_KEY = os.environ.get("SECRET_KEY", "yuyay-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt.

    Args:
        password: The plain text password to hash.

    Returns:
        The bcrypt hashed password string.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.

    Args:
        plain_password: The raw password from the user.
        hashed_password: The bcrypt hashed password from the database.

    Returns:
        True if the password matches, False otherwise.
    """
    return bool(bcrypt.checkpw(plain_password.encode(), hashed_password.encode()))


FAKE_USERS_DB: dict[str, dict[str, Any]] = {
    "admin": {
        "username": "admin",
        "hashed_password": hash_password("yuyay2026"),
    }
}


def create_access_token(data: dict[str, Any]) -> str:
    """Create a signed JWT access token.

    Args:
        data: The payload to encode into the token.

    Returns:
        A signed JWT token string.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return str(jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM))


def decode_token(token: str) -> str | None:
    """Decode and verify a JWT token.

    Args:
        token: The JWT token string to decode.

    Returns:
        The username from the token, or None if invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        return username
    except JWTError:
        return None

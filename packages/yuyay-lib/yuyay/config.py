"""Configuration management for the YUYAY library."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class YUYAYConfig:
    """Configuration settings for the YUYAY library.

    Attributes:
        provider: The LLM provider to use. One of 'openai', 'anthropic', 'google'.
        database_url: SQLAlchemy-compatible database connection string.
        debug: Whether to enable debug logging.
    """

    provider: str = "anthropic"
    database_url: str = "sqlite:///yuyay.db"
    debug: bool = False


def load_config() -> YUYAYConfig:
    """Load configuration from environment variables with sensible defaults.

    Returns:
        A YUYAYConfig instance populated from environment variables.
    """
    return YUYAYConfig(
        provider=os.environ.get("YUYAY_PROVIDER", "anthropic"),
        database_url=os.environ.get("YUYAY_DATABASE_URL", "sqlite:///yuyay.db"),
        debug=os.environ.get("YUYAY_DEBUG", "false").lower() == "true",
    )

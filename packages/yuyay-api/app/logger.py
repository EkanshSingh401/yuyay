"""Structured logging configuration for the YUYAY Intelligence API."""

from __future__ import annotations

import structlog


def configure_logging() -> None:
    """Configure structlog for JSON structured logging.

    Sets up structlog with timestamps, log levels, and JSON output.
    Should be called once on application startup.
    """
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance.

    Args:
        name: The name of the logger, typically the module name.

    Returns:
        A configured structlog BoundLogger instance.
    """
    return structlog.get_logger(name)

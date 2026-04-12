"""Tests for the YUYAY configuration management module."""

from __future__ import annotations

import pytest

from yuyay.config import YUYAYConfig, load_config


def test_default_provider() -> None:
    """YUYAYConfig defaults to anthropic provider."""
    config = YUYAYConfig()
    assert config.provider == "anthropic"


def test_default_database_url() -> None:
    """YUYAYConfig defaults to SQLite database URL."""
    config = YUYAYConfig()
    assert config.database_url == "sqlite:///yuyay.db"


def test_default_debug() -> None:
    """YUYAYConfig defaults to debug disabled."""
    config = YUYAYConfig()
    assert config.debug is False


def test_load_config_returns_yuyay_config() -> None:
    """load_config returns a YUYAYConfig instance."""
    config = load_config()
    assert isinstance(config, YUYAYConfig)


def test_load_config_reads_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    """load_config reads YUYAY_PROVIDER from environment."""
    monkeypatch.setenv("YUYAY_PROVIDER", "openai")
    config = load_config()
    assert config.provider == "openai"


def test_load_config_reads_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """load_config reads YUYAY_DATABASE_URL from environment."""
    monkeypatch.setenv("YUYAY_DATABASE_URL", "postgresql://localhost/yuyay")
    config = load_config()
    assert config.database_url == "postgresql://localhost/yuyay"


def test_load_config_reads_debug_true(monkeypatch: pytest.MonkeyPatch) -> None:
    """load_config sets debug to True when YUYAY_DEBUG is 'true'."""
    monkeypatch.setenv("YUYAY_DEBUG", "true")
    config = load_config()
    assert config.debug is True


def test_load_config_reads_debug_case_insensitive(monkeypatch: pytest.MonkeyPatch) -> None:
    """load_config handles uppercase YUYAY_DEBUG value."""
    monkeypatch.setenv("YUYAY_DEBUG", "TRUE")
    config = load_config()
    assert config.debug is True
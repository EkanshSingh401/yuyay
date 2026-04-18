"""Tests for the transformers module."""

from __future__ import annotations

from yuyay.transformers import ALL_TRANSFORMERS, Transformer, get_transformer_by_id


def test_transformer_is_dataclass_instance() -> None:
    transformer = ALL_TRANSFORMERS[0]
    assert isinstance(transformer, Transformer)


def test_all_transformers_length() -> None:
    assert len(ALL_TRANSFORMERS) == 12


def test_transformer_has_id() -> None:
    transformer = ALL_TRANSFORMERS[0]
    assert transformer.id == "1a"


def test_transformer_has_question() -> None:
    transformer = ALL_TRANSFORMERS[0]
    assert isinstance(transformer.question, str)
    assert len(transformer.question) > 0


def test_summary_format() -> None:
    transformer = ALL_TRANSFORMERS[0]
    assert (
        transformer.summary()
        == "[1a] Does the idea, good, service or issue serve my highest purpose?"
    )


def test_summary_returns_str() -> None:
    transformer = ALL_TRANSFORMERS[0]
    assert isinstance(transformer.summary(), str)


def test_get_transformer_by_id_found() -> None:
    transformer = get_transformer_by_id("1a")
    assert transformer is not None
    assert transformer.id == "1a"


def test_get_transformer_by_id_not_found() -> None:
    transformer = get_transformer_by_id("99")
    assert transformer is None


def test_get_transformer_by_id_last() -> None:
    transformer = get_transformer_by_id("10")
    assert transformer is not None
    assert transformer.id == "10"


def test_all_transformer_ids_are_unique() -> None:
    ids = [t.id for t in ALL_TRANSFORMERS]
    assert len(ids) == len(set(ids))

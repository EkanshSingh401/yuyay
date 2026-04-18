"""Tests for the wheel module."""

from __future__ import annotations

from yuyay.wheel import (
    WHEEL_SECTORS,
    WheelResult,
    evaluate_whole_system,
    get_sector,
)


def test_wheel_sectors_length() -> None:
    assert len(WHEEL_SECTORS) == 12


def test_wheel_sectors_contains_justice() -> None:
    assert "Justice" in WHEEL_SECTORS


def test_wheel_sectors_are_strings() -> None:
    for sector in WHEEL_SECTORS:
        assert isinstance(sector, str)


def test_wheel_result_is_dataclass() -> None:
    result = WheelResult(
        sector="Justice", worldview_alignment=True, whole_system_score=10
    )
    assert isinstance(result, WheelResult)


def test_wheel_result_summary_aligned() -> None:
    result = WheelResult(
        sector="Justice", worldview_alignment=True, whole_system_score=10
    )
    assert (
        result.summary() == "[Justice] Worldview: aligned | Whole System Score: 10/12"
    )


def test_wheel_result_summary_not_aligned() -> None:
    result = WheelResult(
        sector="Health", worldview_alignment=False, whole_system_score=5
    )
    assert (
        result.summary() == "[Health] Worldview: not aligned | Whole System Score: 5/12"
    )


def test_wheel_result_default_notes() -> None:
    result = WheelResult(sector="Arts", worldview_alignment=True, whole_system_score=8)
    assert result.notes == ""


def test_get_sector_found() -> None:
    assert get_sector("Justice") == "Justice"


def test_get_sector_case_insensitive() -> None:
    assert get_sector("justice") == "Justice"


def test_get_sector_not_found() -> None:
    assert get_sector("FakeSector") is None


def test_evaluate_whole_system_full() -> None:
    assert evaluate_whole_system(WHEEL_SECTORS) == 12


def test_evaluate_whole_system_partial() -> None:
    assert evaluate_whole_system(["Justice", "Health", "Arts"]) == 3


def test_evaluate_whole_system_empty() -> None:
    assert evaluate_whole_system([]) == 0


def test_evaluate_whole_system_duplicates() -> None:
    assert evaluate_whole_system(["Justice", "Justice", "Health"]) == 2

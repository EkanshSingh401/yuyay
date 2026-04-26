"""Tests for the po module."""

from __future__ import annotations

from yuyay.po import POResult, po_challenge, po_reframe


def test_po_reframe_returns_poresult() -> None:
    result = po_reframe("profit first", "people first", "profit is the goal")
    assert isinstance(result, POResult)


def test_po_reframe_original() -> None:
    result = po_reframe("profit first", "people first", "profit is the goal")
    assert result.original == "profit first"


def test_po_reframe_reframed() -> None:
    result = po_reframe("profit first", "people first", "profit is the goal")
    assert result.reframed == "people first"


def test_po_reframe_challenge() -> None:
    result = po_reframe("profit first", "people first", "profit is the goal")
    assert result.challenge == "profit is the goal"


def test_po_result_summary_format() -> None:
    result = POResult(
        original="profit first",
        reframed="people first",
        challenge="profit is the goal",
    )
    expected = (
        "Original: profit first\n"
        "Challenge: profit is the goal\n"
        "Reframed: people first"
    )
    assert result.summary() == expected


def test_po_challenge_returns_string() -> None:
    result = po_challenge("profit always comes first")
    assert isinstance(result, str)


def test_po_challenge_format() -> None:
    result = po_challenge("profit always comes first")
    assert (
        result == "PO: What if the opposite of 'profit always comes first' were true?"
    )


def test_po_challenge_includes_assumption() -> None:
    result = po_challenge("speed matters most")
    assert "speed matters most" in result

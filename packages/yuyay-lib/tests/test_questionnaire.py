"""Tests for the questionnaire module."""

from __future__ import annotations

import pytest

from yuyay.exceptions import InvalidResponseError
from yuyay.questionnaire import QuestionnaireReport, process_responses


def test_process_responses_all_yes() -> None:
    responses = {"1a": "YES", "1b": "YES", "2a": "YES"}
    report = process_responses(responses)
    assert report.yes_count == 3
    assert report.no_count == 0
    assert report.po_count == 0


def test_process_responses_all_no() -> None:
    responses = {"1a": "NO", "1b": "NO"}
    report = process_responses(responses)
    assert report.no_count == 2
    assert report.yes_count == 0


def test_process_responses_all_po() -> None:
    responses = {"1a": "PO", "1b": "PO"}
    report = process_responses(responses)
    assert report.po_count == 2
    assert report.yes_count == 0


def test_process_responses_mixed() -> None:
    responses = {"1a": "YES", "1b": "NO", "2a": "PO"}
    report = process_responses(responses)
    assert report.yes_count == 1
    assert report.no_count == 1
    assert report.po_count == 1


def test_process_responses_total() -> None:
    responses = {"1a": "YES", "1b": "NO", "2a": "PO"}
    report = process_responses(responses)
    assert report.total == 3


def test_process_responses_flags_no_and_po() -> None:
    responses = {"1a": "YES", "1b": "NO", "2a": "PO"}
    report = process_responses(responses)
    assert "1b" in report.flags
    assert "2a" in report.flags
    assert "1a" not in report.flags


def test_process_responses_case_insensitive() -> None:
    responses = {"1a": "yes", "1b": "no", "2a": "po"}
    report = process_responses(responses)
    assert report.yes_count == 1
    assert report.no_count == 1
    assert report.po_count == 1


def test_process_responses_invalid_raises() -> None:
    with pytest.raises(InvalidResponseError):
        process_responses({"1a": "MAYBE"})


def test_process_responses_empty() -> None:
    report = process_responses({})
    assert report.total == 0
    assert report.yes_count == 0
    assert report.flags == []


def test_questionnaire_report_summary() -> None:
    report = QuestionnaireReport(
        yes_count=3, no_count=1, po_count=1, total=5, flags=["1b", "2a"]
    )
    assert report.summary() == "YES: 3 | NO: 1 | PO: 1 | Total: 5 | Flagged: 2"


def test_questionnaire_report_default_flags() -> None:
    report = QuestionnaireReport(yes_count=2, no_count=0, po_count=0, total=2)
    assert report.flags == []

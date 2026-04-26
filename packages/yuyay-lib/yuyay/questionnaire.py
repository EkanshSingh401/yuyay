"""Questionnaire processor for the YUYAY Intelligence Framework."""

from __future__ import annotations

from dataclasses import dataclass, field

from yuyay.exceptions import InvalidResponseError

VALID_RESPONSES: set[str] = {"YES", "NO", "PO"}


@dataclass
class QuestionnaireReport:
    """Result of processing a set of questionnaire responses.

    Attributes:
        yes_count: Number of YES responses.
        no_count: Number of NO responses.
        po_count: Number of PO responses.
        total: Total number of responses processed.
        flags: List of question ids that returned NO or PO.
    """

    yes_count: int
    no_count: int
    po_count: int
    total: int
    flags: list[str] = field(default_factory=list)

    def summary(self) -> str:
        """Return a formatted summary of the questionnaire report.

        Returns:
            A string showing YES/NO/PO counts and flagged questions.
        """
        return (
            f"YES: {self.yes_count} | NO: {self.no_count} | PO: {self.po_count} "
            f"| Total: {self.total} | Flagged: {len(self.flags)}"
        )


def process_responses(responses: dict[str, str]) -> QuestionnaireReport:
    """Process a set of transformer question responses.

    Args:
        responses: A dict mapping question id to response string (YES, NO, or PO).

    Returns:
        A QuestionnaireReport with counts and flagged question ids.

    Raises:
        InvalidResponseError: If any response value is not YES, NO, or PO.
    """
    yes_count = 0
    no_count = 0
    po_count = 0
    flags: list[str] = []

    for question_id, response in responses.items():
        normalized = response.strip().upper()
        if normalized not in VALID_RESPONSES:
            raise InvalidResponseError(
                f"Invalid response '{response}' for question '{question_id}'. "
                f"Must be YES, NO, or PO."
            )
        if normalized == "YES":
            yes_count += 1
        elif normalized == "NO":
            no_count += 1
            flags.append(question_id)
        else:
            po_count += 1
            flags.append(question_id)

    return QuestionnaireReport(
        yes_count=yes_count,
        no_count=no_count,
        po_count=po_count,
        total=len(responses),
        flags=flags,
    )

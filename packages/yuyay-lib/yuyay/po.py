"""Edward de Bono PO lateral thinking logic for the YUYAY Intelligence Framework."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class POResult:
    """Result of a PO lateral thinking operation.

    Attributes:
        original: The original statement or idea.
        reframed: The reframed version using PO logic.
        challenge: The assumption being challenged.
    """

    original: str
    reframed: str
    challenge: str

    def summary(self) -> str:
        """Return a formatted summary of this PO result.

        Returns:
            A string showing the original, challenge, and reframe.
        """
        return (
            f"Original: {self.original}\n"
            f"Challenge: {self.challenge}\n"
            f"Reframed: {self.reframed}"
        )


def po_reframe(statement: str, reframe: str, challenge: str) -> POResult:
    """Apply PO lateral thinking to reframe a statement.

    Args:
        statement: The original idea or statement to reframe.
        reframe: The new perspective or alternative framing.
        challenge: The assumption being challenged by PO.

    Returns:
        A POResult containing the original, reframe, and challenge.
    """
    return POResult(
        original=statement,
        reframed=reframe,
        challenge=challenge,
    )


def po_challenge(assumption: str) -> str:
    """Generate a PO challenge prompt for a given assumption.

    Args:
        assumption: The assumption to challenge.

    Returns:
        A string prompting lateral thinking about the assumption.
    """
    return f"PO: What if the opposite of '{assumption}' were true?"

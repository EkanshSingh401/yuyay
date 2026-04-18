"""Co-Creation Wheel integration engine for the YUYAY Intelligence Framework."""

from __future__ import annotations

from dataclasses import dataclass

WHEEL_SECTORS: list[str] = [
    "Justice",
    "Health",
    "Spirituality",
    "Infrastructure",
    "Environment",
    "Media",
    "Governance",
    "Relations",
    "Arts",
    "Economics",
    "Science",
    "Education",
]


@dataclass
class WheelResult:
    """Result of a Co-Creation Wheel integration.

    Attributes:
        sector: The wheel sector being evaluated.
        worldview_alignment: Whether the input aligns with the Worldview center.
        whole_system_score: Score from 0 to 12 based on sectors addressed.
        notes: Optional contextual notes about the result.
    """

    sector: str
    worldview_alignment: bool
    whole_system_score: int
    notes: str = ""

    def summary(self) -> str:
        """Return a formatted summary of this wheel result.

        Returns:
            A string describing the sector, alignment, and score.
        """
        alignment = "aligned" if self.worldview_alignment else "not aligned"
        return (
            f"[{self.sector}] Worldview: {alignment} | "
            f"Whole System Score: {self.whole_system_score}/12"
        )


def get_sector(sector_name: str) -> str | None:
    """Look up a wheel sector by name.

    Args:
        sector_name: The name of the sector to search for.

    Returns:
        The matching sector name, or None if not found.
    """
    for sector in WHEEL_SECTORS:
        if sector.lower() == sector_name.lower():
            return sector
    return None


def evaluate_whole_system(sectors_addressed: list[str]) -> int:
    """Score how many valid wheel sectors are addressed.

    Args:
        sectors_addressed: List of sector names provided by the user.

    Returns:
        Integer score from 0 to 12 representing coverage.
    """
    valid = {s.lower() for s in WHEEL_SECTORS}
    addressed = {s.lower() for s in sectors_addressed}
    return len(valid & addressed)

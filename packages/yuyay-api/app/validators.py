"""Pandera data validation schemas for the YUYAY ETL pipeline.

Validates evaluation responses and archetype scores before
loading into PostgreSQL to ensure data integrity.
"""

from __future__ import annotations

import pandas as pd
import pandera as pa

VALID_QUESTION_IDS = ["1a", "1b", "2a", "2b", "3", "4", "5", "6", "7", "8", "9", "10"]
VALID_RESPONSES = ["YES", "NO", "PO"]
VALID_ARCHETYPES = [
    "The Seer",
    "The Architect",
    "The Bridgebuilder",
    "The Steward",
    "The Navigator",
    "The Maker",
    "The Catalyst",
    "The Harmonizer",
    "The Sage",
    "The Oracle",
    "The Alchemist",
    "The Weaver",
]

evaluation_response_schema = pa.DataFrameSchema(
    {
        "session_id": pa.Column(str, pa.Check(lambda s: s.str.len() > 0)),
        "question_id": pa.Column(str, pa.Check.isin(VALID_QUESTION_IDS)),
        "response": pa.Column(str, pa.Check.isin(VALID_RESPONSES)),
    },
    strict=True,
    coerce=True,
)

archetype_score_schema = pa.DataFrameSchema(
    {
        "session_id": pa.Column(str, pa.Check(lambda s: s.str.len() > 0)),
        "archetype_name": pa.Column(str, pa.Check.isin(VALID_ARCHETYPES)),
        "score": pa.Column(int, [pa.Check.ge(0), pa.Check.le(100)]),
        "flagged": pa.Column(bool),
    },
    strict=True,
    coerce=True,
)


def validate_evaluation_responses(
    session_id: str,
    responses: dict[str, str],
) -> list[dict[str, str]]:
    """Validate evaluation responses against the schema.

    Args:
        session_id: The session ID for these responses.
        responses: Dict mapping question_id to YES/NO/PO response.

    Returns:
        List of validated response dicts.

    Raises:
        pa.errors.SchemaError: If any response fails validation.
    """
    rows = [
        {"session_id": session_id, "question_id": qid, "response": resp}
        for qid, resp in responses.items()
    ]
    df = pd.DataFrame(rows)
    validated = evaluation_response_schema.validate(df)
    return validated.to_dict(orient="records")  # type: ignore[return-value]


def validate_archetype_scores(
    scores: list[dict[str, object]],
) -> list[dict[str, object]]:
    """Validate computed archetype scores against the schema.

    Args:
        scores: List of archetype score dicts.

    Returns:
        List of validated score dicts.

    Raises:
        pa.errors.SchemaError: If any score fails validation.
    """
    df = pd.DataFrame(scores)
    validated = archetype_score_schema.validate(df)
    return validated.to_dict(orient="records")  # type: ignore[return-value]

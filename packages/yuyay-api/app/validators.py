"""Pandera data validation schemas for the YUYAY ETL pipeline.

Validates evaluation responses and archetype scores before
loading into PostgreSQL to ensure data integrity.
"""

from __future__ import annotations

import pandera as pa
from pandera.typing import Series


class EvaluationResponseSchema(pa.DataFrameModel):
    """Schema for validating raw evaluation responses.

    Validates that each response has a valid question ID
    and a valid YES/NO/PO response value.
    """

    question_id: Series[str] = pa.Field(
        isin=["1a", "1b", "2a", "2b", "3", "4", "5", "6", "7", "8", "9", "10"],
        description="Valid transformer question ID",
    )
    response: Series[str] = pa.Field(
        isin=["YES", "NO", "PO"],
        description="Valid YES/NO/PO response",
    )
    session_id: Series[str] = pa.Field(
        str_length_min=1,
        description="Non-empty session ID",
    )

    class Config:
        strict = True
        coerce = True


class ArchetypeScoreSchema(pa.DataFrameModel):
    """Schema for validating computed archetype scores.

    Validates that scores are in range and archetype names are valid.
    """

    session_id: Series[str] = pa.Field(
        str_length_min=1,
        description="Non-empty session ID",
    )
    archetype_name: Series[str] = pa.Field(
        isin=[
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
        ],
        description="Valid YUYAY archetype name",
    )
    score: Series[int] = pa.Field(
        ge=0,
        le=100,
        description="Score between 0 and 100",
    )
    flagged: Series[bool] = pa.Field(
        description="Whether this archetype was flagged",
    )

    class Config:
        strict = True
        coerce = True


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
    import pandas as pd

    rows = [
        {"session_id": session_id, "question_id": qid, "response": resp}
        for qid, resp in responses.items()
    ]
    df = pd.DataFrame(rows)
    validated = EvaluationResponseSchema.validate(df)
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
    import pandas as pd

    df = pd.DataFrame(scores)
    validated = ArchetypeScoreSchema.validate(df)
    return validated.to_dict(orient="records")  # type: ignore[return-value]

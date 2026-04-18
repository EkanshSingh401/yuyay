"""Transformer questions for the YUYAY Intelligence Framework."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Transformer:
    """A single transformer question from the YUYAY framework.

    Attributes:
        id: Short identifier for the question e.g. '1a', '2b', '10'.
        question: The full text of the transformer question.
    """

    id: str
    question: str

    def summary(self) -> str:
        """Return a formatted summary of this transformer question.

        Returns:
            A string with the id and question text.
        """
        return f"[{self.id}] {self.question}"


ALL_TRANSFORMERS: list[Transformer] = [
    Transformer(
        id="1a",
        question="Does the idea, good, service or issue serve my highest purpose?",
    ),
    Transformer(id="1b", question="Is it relevant?"),
    Transformer(id="2a", question="Do I have enough information to make a decision?"),
    Transformer(id="2b", question="Can we involve other stakeholders?"),
    Transformer(id="3", question="Am I being Wise?"),
    Transformer(id="4", question="Are Judgments or Bias present?"),
    Transformer(id="5", question="Have I used compassion and mercy in my decision?"),
    Transformer(id="6", question="Is my heart making the decision on its own?"),
    Transformer(
        id="7",
        question="Does this allow myself and others to be involved to reach peak performance levels?",
    ),
    Transformer(id="8", question="Will something of lasting endurance be created?"),
    Transformer(
        id="9",
        question="Will this build a strong foundation? (For me as an individual and for the corporation.)",
    ),
    Transformer(
        id="10",
        question="Does the idea, good, service or issue help heal the planet?",
    ),
]


def get_transformer_by_id(transformer_id: str) -> Transformer | None:
    """Look up a transformer question by its id.

    Args:
        transformer_id: The short identifier to search for e.g. '1a', '10'.

    Returns:
        The matching Transformer, or None if not found.
    """
    for transformer in ALL_TRANSFORMERS:
        if transformer.id == transformer_id:
            return transformer
    return None

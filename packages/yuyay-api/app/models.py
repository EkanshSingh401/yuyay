"""SQLAlchemy ORM models for the YUYAY Intelligence API."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class EvaluationSession(Base):
    """Core evaluation session — one per user evaluation attempt.

    Attributes:
        id: Unique session identifier.
        created_at: When the session was created.
        completed_at: When the session was completed.
        status: Current status — in_progress or complete.
        responses: JSON blob of question id to YES/NO/PO responses.
        yes_count: Number of YES responses.
        no_count: Number of NO responses.
        po_count: Number of PO responses.
        total_responses: Total number of responses.
        flags: JSON list of flagged question ids.
        whole_system_score: Co-Creation Wheel score out of 12.
        worldview_alignment: Whether aligned with Worldview center.
        user_id: Optional Clerk user ID for authenticated sessions.
    """

    __tablename__ = "evaluation_sessions"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String, default="in_progress")
    responses: Mapped[dict] = mapped_column(JSON, default=dict)
    yes_count: Mapped[int] = mapped_column(Integer, default=0)
    no_count: Mapped[int] = mapped_column(Integer, default=0)
    po_count: Mapped[int] = mapped_column(Integer, default=0)
    total_responses: Mapped[int] = mapped_column(Integer, default=0)
    flags: Mapped[list] = mapped_column(JSON, default=list)
    whole_system_score: Mapped[int] = mapped_column(Integer, default=0)
    worldview_alignment: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[str | None] = mapped_column(String, nullable=True)

    archetype_scores: Mapped[list[ArchetypeScore]] = relationship(
        "ArchetypeScore", back_populates="session", cascade="all, delete-orphan"
    )
    transformer_results: Mapped[list[TransformerResult]] = relationship(
        "TransformerResult", back_populates="session", cascade="all, delete-orphan"
    )


class ArchetypeScore(Base):
    """Computed score for a single archetype within an evaluation session.

    Attributes:
        id: Unique identifier.
        session_id: Foreign key to evaluation_sessions.
        archetype_name: Name of the archetype.
        score: Score from 0 to 100.
        flagged: Whether this archetype was flagged for deeper inquiry.
        created_at: When this record was created.
    """

    __tablename__ = "archetype_scores"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    session_id: Mapped[str] = mapped_column(
        String, ForeignKey("evaluation_sessions.id"), nullable=False
    )
    archetype_name: Mapped[str] = mapped_column(String, nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=0)
    flagged: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped[EvaluationSession] = relationship(
        "EvaluationSession", back_populates="archetype_scores"
    )


class TransformerResult(Base):
    """Individual transformer question result within an evaluation session.

    Attributes:
        id: Unique identifier.
        session_id: Foreign key to evaluation_sessions.
        question_id: The transformer question ID e.g. 1a, 1b, 2a.
        response: YES, NO, or PO.
        flagged: Whether this response was flagged.
        created_at: When this record was created.
    """

    __tablename__ = "transformer_results"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    session_id: Mapped[str] = mapped_column(
        String, ForeignKey("evaluation_sessions.id"), nullable=False
    )
    question_id: Mapped[str] = mapped_column(String, nullable=False)
    response: Mapped[str] = mapped_column(String, nullable=False)
    flagged: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    session: Mapped[EvaluationSession] = relationship(
        "EvaluationSession", back_populates="transformer_results"
    )


class FIOSQuery(Base):
    """Record of a FIOS LLM query.

    Attributes:
        id: Unique identifier.
        user_id: Clerk user ID.
        provider: LLM provider — anthropic, openai, google.
        model: Specific model used.
        prompt: The full enriched prompt sent.
        response: The LLM response.
        coherence_score: YUYAY coherence score 0-100.
        input_tokens: Input tokens used.
        output_tokens: Output tokens used.
        latency_ms: Query latency in milliseconds.
        estimated_cost_usd: Estimated cost in USD.
        created_at: When the query was made.
    """

    __tablename__ = "fios_queries"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str | None] = mapped_column(String, nullable=True)
    provider: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    coherence_score: Mapped[int] = mapped_column(Integer, default=0)
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    latency_ms: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    cost_record: Mapped[FIOSQueryCost | None] = relationship(
        "FIOSQueryCost", back_populates="query", cascade="all, delete-orphan"
    )


class FIOSQueryCost(Base):
    """Detailed cost breakdown for a FIOS query.

    Attributes:
        id: Unique identifier.
        query_id: Foreign key to fios_queries.
        input_cost_usd: Cost of input tokens.
        output_cost_usd: Cost of output tokens.
        total_cost_usd: Total cost.
        created_at: When this record was created.
    """

    __tablename__ = "fios_query_costs"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    query_id: Mapped[str] = mapped_column(
        String, ForeignKey("fios_queries.id"), nullable=False
    )
    input_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    output_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    query: Mapped[FIOSQuery] = relationship("FIOSQuery", back_populates="cost_record")


class ArchetypeAnalytics(Base):
    """Aggregated archetype distribution analytics.

    Attributes:
        id: Unique identifier.
        archetype_name: Name of the archetype.
        total_sessions: Total sessions where this archetype was scored.
        total_flagged: Times this archetype was flagged.
        average_score: Average score across all sessions.
        flag_rate: Percentage of sessions where this archetype was flagged.
        computed_at: When this aggregation was computed.
    """

    __tablename__ = "archetype_analytics"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    archetype_name: Mapped[str] = mapped_column(String, nullable=False)
    total_sessions: Mapped[int] = mapped_column(Integer, default=0)
    total_flagged: Mapped[int] = mapped_column(Integer, default=0)
    average_score: Mapped[float] = mapped_column(Float, default=0.0)
    flag_rate: Mapped[float] = mapped_column(Float, default=0.0)
    computed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class DailyMetrics(Base):
    """Daily rollup of platform metrics.

    Attributes:
        id: Unique identifier.
        date: The date this rollup covers.
        total_evaluations: Evaluations completed that day.
        total_fios_queries: FIOS queries made that day.
        total_yes_responses: YES responses across all evaluations.
        total_no_responses: NO responses across all evaluations.
        total_po_responses: PO responses across all evaluations.
        total_cost_usd: Total LLM cost that day.
        average_coherence_score: Average FIOS coherence score.
        computed_at: When this rollup was computed.
    """

    __tablename__ = "daily_metrics"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_evaluations: Mapped[int] = mapped_column(Integer, default=0)
    total_fios_queries: Mapped[int] = mapped_column(Integer, default=0)
    total_yes_responses: Mapped[int] = mapped_column(Integer, default=0)
    total_no_responses: Mapped[int] = mapped_column(Integer, default=0)
    total_po_responses: Mapped[int] = mapped_column(Integer, default=0)
    total_cost_usd: Mapped[float] = mapped_column(Float, default=0.0)
    average_coherence_score: Mapped[float] = mapped_column(Float, default=0.0)
    computed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

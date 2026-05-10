"""SQLAlchemy ORM models for the YUYAY Intelligence API."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass


class EvaluationSession(Base):
    """Database model for a YUYAY evaluation session.

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

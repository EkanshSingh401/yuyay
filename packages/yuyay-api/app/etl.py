"""ETL pipeline for YUYAY Intelligence Platform.

Extracts evaluation data, transforms it through validation and
aggregation, and loads results into analytics tables.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.logger import get_logger
from app.models import (
    ArchetypeAnalytics,
    ArchetypeScore,
    DailyMetrics,
    EvaluationSession,
    FIOSQuery,
    TransformerResult,
)

logger = get_logger(__name__)


async def extract_completed_sessions(
    session: AsyncSession,
) -> list[EvaluationSession]:
    """Extract all completed evaluation sessions.

    Args:
        session: Database session.

    Returns:
        List of completed EvaluationSession records.
    """
    result = await session.execute(
        select(EvaluationSession).where(EvaluationSession.status == "complete")
    )
    return list(result.scalars().all())


async def transform_and_load_archetype_scores(
    db: AsyncSession,
    eval_session: EvaluationSession,
) -> None:
    """Transform evaluation responses into per-archetype scores.

    Maps YES/NO/PO responses to archetype dimensions and
    loads individual scores into the archetype_scores table.

    Args:
        db: Database session.
        eval_session: The completed evaluation session to process.
    """
    archetype_question_map = {
        "The Seer": ["1a"],
        "The Architect": ["1b"],
        "The Bridgebuilder": ["2a"],
        "The Steward": ["2b"],
        "The Navigator": ["3"],
        "The Maker": ["4"],
        "The Catalyst": ["5"],
        "The Harmonizer": ["6"],
        "The Sage": ["7"],
        "The Oracle": ["8"],
        "The Alchemist": ["9"],
        "The Weaver": ["10"],
    }

    responses: dict[str, str] = eval_session.responses or {}
    flags: list[str] = eval_session.flags or []

    for archetype_name, question_ids in archetype_question_map.items():
        scores = []
        for qid in question_ids:
            response = responses.get(qid, "NO")
            if response == "YES":
                scores.append(100)
            elif response == "PO":
                scores.append(50)
            else:
                scores.append(0)

        avg_score = sum(scores) // len(scores) if scores else 0
        flagged = any(qid in flags for qid in question_ids)

        existing = await db.execute(
            select(ArchetypeScore).where(
                ArchetypeScore.session_id == eval_session.id,
                ArchetypeScore.archetype_name == archetype_name,
            )
        )
        if existing.scalar_one_or_none() is None:
            db.add(
                ArchetypeScore(
                    session_id=eval_session.id,
                    archetype_name=archetype_name,
                    score=avg_score,
                    flagged=flagged,
                )
            )


async def transform_and_load_transformer_results(
    db: AsyncSession,
    eval_session: EvaluationSession,
) -> None:
    """Transform evaluation responses into per-transformer records.

    Args:
        db: Database session.
        eval_session: The completed evaluation session to process.
    """
    responses: dict[str, str] = eval_session.responses or {}
    flags: list[str] = eval_session.flags or []

    for question_id, response in responses.items():
        existing = await db.execute(
            select(TransformerResult).where(
                TransformerResult.session_id == eval_session.id,
                TransformerResult.question_id == question_id,
            )
        )
        if existing.scalar_one_or_none() is None:
            db.add(
                TransformerResult(
                    session_id=eval_session.id,
                    question_id=question_id,
                    response=response,
                    flagged=question_id in flags,
                )
            )


async def compute_archetype_analytics(db: AsyncSession) -> None:
    """Aggregate archetype scores across all sessions.

    Computes average score and flag rate per archetype
    and upserts into the archetype_analytics table.

    Args:
        db: Database session.
    """
    result = await db.execute(
        select(
            ArchetypeScore.archetype_name,
            func.count(ArchetypeScore.id).label("total_sessions"),
            func.sum(ArchetypeScore.flagged.cast(type_=None)).label("total_flagged"),
            func.avg(ArchetypeScore.score).label("average_score"),
        ).group_by(ArchetypeScore.archetype_name)
    )
    rows = result.all()

    for row in rows:
        flag_rate = (
            float(row.total_flagged) / float(row.total_sessions)
            if row.total_sessions > 0
            else 0.0
        )
        analytics = ArchetypeAnalytics(
            archetype_name=row.archetype_name,
            total_sessions=row.total_sessions,
            total_flagged=int(row.total_flagged or 0),
            average_score=float(row.average_score or 0.0),
            flag_rate=flag_rate,
            computed_at=datetime.now(timezone.utc),
        )
        db.add(analytics)


async def compute_daily_metrics(db: AsyncSession) -> None:
    """Compute daily rollup metrics and load into daily_metrics table.

    Args:
        db: Database session.
    """
    today = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    eval_result = await db.execute(
        select(
            func.count(EvaluationSession.id).label("total"),
            func.sum(EvaluationSession.yes_count).label("yes"),
            func.sum(EvaluationSession.no_count).label("no"),
            func.sum(EvaluationSession.po_count).label("po"),
        ).where(EvaluationSession.status == "complete")
    )
    eval_row = eval_result.one()

    fios_result = await db.execute(
        select(
            func.count(FIOSQuery.id).label("total"),
            func.avg(FIOSQuery.coherence_score).label("avg_coherence"),
            func.sum(FIOSQuery.estimated_cost_usd).label("total_cost"),
        )
    )
    fios_row = fios_result.one()

    db.add(
        DailyMetrics(
            date=today,
            total_evaluations=int(eval_row.total or 0),
            total_fios_queries=int(fios_row.total or 0),
            total_yes_responses=int(eval_row.yes or 0),
            total_no_responses=int(eval_row.no or 0),
            total_po_responses=int(eval_row.po or 0),
            total_cost_usd=float(fios_row.total_cost or 0.0),
            average_coherence_score=float(fios_row.avg_coherence or 0.0),
            computed_at=datetime.now(timezone.utc),
        )
    )


async def run_etl_pipeline(db: AsyncSession) -> dict[str, int]:
    """Run the full ETL pipeline.

    Extracts completed sessions, transforms responses into
    normalized records, and loads aggregated analytics.

    Args:
        db: Database session.

    Returns:
        Dict with counts of records processed.
    """
    logger.info("etl_pipeline_started")

    sessions = await extract_completed_sessions(db)
    sessions_processed = 0

    for eval_session in sessions:
        await transform_and_load_archetype_scores(db, eval_session)
        await transform_and_load_transformer_results(db, eval_session)
        sessions_processed += 1

    await compute_archetype_analytics(db)
    await compute_daily_metrics(db)
    await db.commit()

    logger.info("etl_pipeline_complete", sessions_processed=sessions_processed)
    return {"sessions_processed": sessions_processed}

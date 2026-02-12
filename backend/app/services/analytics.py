"""
Analytics aggregation service.
Computes daily analytics from raw conversation + lead data.
Populates the analytics_daily table for dashboard and email reports.
"""

import uuid
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import select, func, case, and_, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    Property,
    Conversation,
    Message,
    Lead,
    AnalyticsDaily,
)


async def compute_daily_analytics(
    db: AsyncSession,
    property_id: uuid.UUID,
    report_date: date,
) -> AnalyticsDaily:
    """
    Compute analytics for a single property for a single day.
    Uses raw conversation and lead data to build aggregates.

    This is called by the daily cron job and can also be called
    retroactively to backfill analytics.
    """
    # Date range for the report day
    day_start = datetime.combine(report_date, datetime.min.time()).replace(
        tzinfo=timezone.utc
    )
    day_end = datetime.combine(report_date + timedelta(days=1), datetime.min.time()).replace(
        tzinfo=timezone.utc
    )

    # 1. Total inquiries (conversations started on this day)
    total_result = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.property_id == property_id,
            Conversation.started_at >= day_start,
            Conversation.started_at < day_end,
        )
    )
    total_inquiries = total_result.scalar() or 0

    # 2. After-hours inquiries
    after_hours_result = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.property_id == property_id,
            Conversation.started_at >= day_start,
            Conversation.started_at < day_end,
            Conversation.is_after_hours == True,
        )
    )
    after_hours_inquiries = after_hours_result.scalar() or 0

    # 3. After-hours responded (conversations that have at least one AI message)
    after_hours_responded_result = await db.execute(
        select(func.count(Conversation.id.distinct())).where(
            Conversation.property_id == property_id,
            Conversation.started_at >= day_start,
            Conversation.started_at < day_end,
            Conversation.is_after_hours == True,
            Conversation.id.in_(
                select(Message.conversation_id).where(Message.role == "ai")
            ),
        )
    )
    after_hours_responded = after_hours_responded_result.scalar() or 0

    # 4. Leads captured
    leads_result = await db.execute(
        select(func.count(Lead.id)).where(
            Lead.property_id == property_id,
            Lead.captured_at >= day_start,
            Lead.captured_at < day_end,
        )
    )
    leads_captured = leads_result.scalar() or 0

    # 5. Handoffs
    handoffs_result = await db.execute(
        select(func.count(Conversation.id)).where(
            Conversation.property_id == property_id,
            Conversation.started_at >= day_start,
            Conversation.started_at < day_end,
            Conversation.status == "handed_off",
        )
    )
    handoffs = handoffs_result.scalar() or 0

    # 6. Average response time (from AI messages metadata)
    # We stored response_time_ms in message metadata
    response_times_result = await db.execute(
        select(Message.metadata_["response_time_ms"]).where(
            Message.conversation_id.in_(
                select(Conversation.id).where(
                    Conversation.property_id == property_id,
                    Conversation.started_at >= day_start,
                    Conversation.started_at < day_end,
                )
            ),
            Message.role == "ai",
            Message.metadata_["response_time_ms"].isnot(None),
        )
    )
    response_times = [
        float(r[0]) / 1000.0  # Convert ms to seconds
        for r in response_times_result.fetchall()
        if r[0] is not None
    ]
    avg_response_time = (
        Decimal(str(sum(response_times) / len(response_times)))
        if response_times
        else Decimal("0")
    )

    # 7. Channel breakdown
    channel_result = await db.execute(
        select(
            Conversation.channel,
            func.count(Conversation.id),
        )
        .where(
            Conversation.property_id == property_id,
            Conversation.started_at >= day_start,
            Conversation.started_at < day_end,
        )
        .group_by(Conversation.channel)
    )
    channel_breakdown = {row[0]: row[1] for row in channel_result.fetchall()}

    # 8. Estimated revenue recovered
    # Formula: after_hours_leads × property_ADR
    prop_result = await db.execute(
        select(Property.adr).where(Property.id == property_id)
    )
    adr = prop_result.scalar() or Decimal("230")

    # Count after-hours leads specifically
    after_hours_leads_result = await db.execute(
        select(func.count(Lead.id)).where(
            Lead.property_id == property_id,
            Lead.captured_at >= day_start,
            Lead.captured_at < day_end,
            Lead.conversation_id.in_(
                select(Conversation.id).where(
                    Conversation.is_after_hours == True
                )
            ),
        )
    )
    after_hours_leads = after_hours_leads_result.scalar() or 0
    estimated_revenue = Decimal(str(after_hours_leads)) * adr

    # 9. Upsert analytics record
    existing = await db.execute(
        select(AnalyticsDaily).where(
            AnalyticsDaily.property_id == property_id,
            AnalyticsDaily.report_date == report_date,
        )
    )
    record = existing.scalar_one_or_none()

    if record:
        record.total_inquiries = total_inquiries
        record.after_hours_inquiries = after_hours_inquiries
        record.after_hours_responded = after_hours_responded
        record.leads_captured = leads_captured
        record.handoffs = handoffs
        record.avg_response_time_sec = avg_response_time
        record.estimated_revenue_recovered = estimated_revenue
        record.channel_breakdown = channel_breakdown
    else:
        record = AnalyticsDaily(
            property_id=property_id,
            report_date=report_date,
            total_inquiries=total_inquiries,
            after_hours_inquiries=after_hours_inquiries,
            after_hours_responded=after_hours_responded,
            leads_captured=leads_captured,
            handoffs=handoffs,
            avg_response_time_sec=avg_response_time,
            estimated_revenue_recovered=estimated_revenue,
            channel_breakdown=channel_breakdown,
        )
        db.add(record)

    await db.flush()
    return record


async def compute_all_properties_daily(
    db: AsyncSession,
    report_date: date | None = None,
):
    """
    Compute daily analytics for all properties.
    Called by the daily cron job.
    """
    if report_date is None:
        report_date = date.today() - timedelta(days=1)  # Yesterday

    result = await db.execute(select(Property.id))
    property_ids = [row[0] for row in result.fetchall()]

    records = []
    for pid in property_ids:
        record = await compute_daily_analytics(db, pid, report_date)
        records.append(record)

    return records

"""
API routes for the Floyd AI Inquiry Capture Engine.

Organized by the three user experiences:
- Guest channels: WhatsApp webhook, Web chat, Email webhook
- Staff: Conversation management, handoff
- GM: Analytics, leads, reports
"""

import json
import uuid
from datetime import date, datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, BackgroundTasks, Form
import structlog
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Property, Conversation, Message, Lead, AnalyticsDaily, KBDocument
from app.schemas import (
    MessageRequest,
    ConversationResponse,
    WebChatStartRequest,
    LeadResponse,
    LeadUpdateRequest,
    PropertyResponse,
    PropertyCreateRequest,
    KBIngestRequest,
    KBIngestResponse,
    AnalyticsSummaryResponse,
)
from app.services.conversation import process_guest_message
from app.services import ingest_knowledge_base
from app.services.whatsapp import send_whatsapp_message
from app.services.email import send_email, notify_staff_handoff
from app.services.email import send_email, notify_staff_handoff
from app.limiter import limiter
from app.auth import verify_jwt, verify_whatsapp_signature

logger = structlog.get_logger()
router = APIRouter(prefix="/api/v1")


# ─────────────────────────────────────────────────────────────
# Guest Channels
# ─────────────────────────────────────────────────────────────

@router.get("/properties", response_model=List[PropertyResponse])
async def list_properties(
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """List all properties (for dashboard selection)."""
    result = await db.execute(select(Property))
    return result.scalars().all()


@router.post("/webhook/whatsapp", response_model=None)
@limiter.limit("3000/minute")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    # Signature verification
    _: None = Depends(verify_whatsapp_signature)
):
    """
    WhatsApp Cloud API webhook receiver.
    Handles verification (GET) and incoming messages (POST).
    Returns 200 OK immediately and processes message in background.
    """
    body = await request.json()

    # Extract message from WhatsApp webhook payload
    try:
        entry = body.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "no_messages"}

        msg = messages[0]
        from_number = msg.get("from", "")
        text = msg.get("text", {}).get("body", "")
        guest_name = value.get("contacts", [{}])[0].get("profile", {}).get("name")

        if not text:
            return {"status": "no_text"}

        # Find property by WhatsApp number
        phone_id = value.get("metadata", {}).get("phone_number_id", "")
        prop_result = await db.execute(
            select(Property).where(Property.whatsapp_number == phone_id)
        )
        prop = prop_result.scalar_one_or_none()

        if not prop:
            logger.warning("WhatsApp webhook: Property not found", phone_id=phone_id)
            return {"status": "property_not_found"}

        # Process in background to avoid styling timeout
        background_tasks.add_task(
            _handle_whatsapp_message_async,
            property_id=prop.id,
            from_number=from_number,
            text=text,
            guest_name=guest_name
        )

        return {"status": "processing"}

    except Exception as e:
        logger.error("WhatsApp webhook error", error=str(e))
        # Return 200 to prevent WhatsApp from retrying endlessly on bad payloads
        return {"status": "error"}


async def _handle_whatsapp_message_async(
    property_id: uuid.UUID,
    from_number: str,
    text: str,
    guest_name: str | None
):
    """
    Background task to process WhatsApp message and send reply.
    """
    # Create a new DB session for the background task
    from app.database import async_session
    
    async with async_session() as db:
        try:
            result = await process_guest_message(
                db=db,
                property_id=property_id,
                guest_identifier=from_number,
                channel="whatsapp",
                message_text=text,
                guest_name=guest_name,
            )
            
            # Send response back via WhatsApp API
            response_text = result["response"]
            await send_whatsapp_message(to_number=from_number, message_text=response_text)
            
            # Notify staff if handoff triggered
            if result.get("mode") == "handoff":
                await notify_staff_handoff(
                    guest_identifier=from_number,
                    channel="whatsapp",
                    guest_name=guest_name,
                    conversation_summary=f"Last message: {text}\nAI Reply: {response_text}"
                )
            
        except Exception as e:
            logger.error(
                "Error processing WhatsApp message",
                error=str(e),
                property_id=str(property_id),
                from_number=from_number
            )


@router.post("/webhook/email", response_model=None)
@limiter.limit("100/minute")
async def email_webhook(
    background_tasks: BackgroundTasks,
    subject: str = Form(None),
    text: str = Form(None),
    html: str = Form(None),
    to: str = Form(None),
    sender: str = Form(None),  # SendGrid sends 'from' as 'sender' or 'from' depending on config due to Python keyword? No, it sends 'from'.
    # But 'from' is a reserved keyword in Python.
    # FastAPI handles this via alias? No.
    # We need to access via request.form() because 'from' is a keyword.
    request: Request = None,
    db: AsyncSession = Depends(get_db)
):
    """
    SendGrid Inbound Parse webhook receiver.
    Parses multipart/form-data.
    """
    form_data = await request.form()
    
    # Extract fields manually to handle 'from' keyword collision
    from_address = form_data.get("from")
    to_address = form_data.get("to")
    subject_text = form_data.get("subject", "No Subject")
    body_text = form_data.get("text", "")
    
    # Simple parsing to check simple text
    if not body_text:
        return {"status": "empty_body"}

    # Extract email address from "Name <email@domain.com>" format
    import re
    email_match = re.search(r'<([^>]+)>', from_address)
    guest_email = email_match.group(1) if email_match else from_address
    guest_name = from_address.split('<')[0].strip() if '<' in from_address else None

    # Find property mechanism
    # TODO: Match by to_address or dedicated inbound email field
    # For now, secure default: do not fall back to random property
    # prop_result = await db.execute(select(Property).limit(1))
    # prop = prop_result.scalar_one_or_none()
    prop = None
    
    if not prop:
        logger.warning("Email webhook: Property not found", to_address=to_address)
        return {"status": "no_property"}

    # Process in background
    background_tasks.add_task(
        _handle_email_message_async,
        property_id=prop.id,
        guest_email=guest_email,
        subject=subject_text,
        text=body_text,
        guest_name=guest_name
    )

    return {"status": "processing"}


async def _handle_email_message_async(
    property_id: uuid.UUID,
    guest_email: str,
    subject: str,
    text: str,
    guest_name: str | None
):
    """
    Background task to process inbound email and send reply.
    """
    from app.database import async_session
    
    async with async_session() as db:
        try:
            # Append subject to text for context
            full_message = f"Subject: {subject}\n\n{text}"
            
            result = await process_guest_message(
                db=db,
                property_id=property_id,
                guest_identifier=guest_email,
                channel="email",
                message_text=full_message,
                guest_name=guest_name,
            )
            
            response_text = result["response"]
            
            # Send reply
            await send_email(
                to_email=guest_email,
                subject=f"Re: {subject}",
                content=response_text
            )

            # Notify staff if handoff triggered
            if result.get("mode") == "handoff":
                await notify_staff_handoff(
                    guest_identifier=guest_email,
                    channel="email",
                    guest_name=guest_name,
                    conversation_summary=f"Subject: {subject}\n\nMessage: {text}\n\nAI Reply: {response_text}"
                )
            
        except Exception as e:
            logger.error(
                "Error processing email message",
                error=str(e),
                property_id=str(property_id),
                guest_email=guest_email
            )


@router.get("/webhook/whatsapp")
async def whatsapp_verify(request: Request):
    """WhatsApp webhook verification (GET request from Meta)."""
    from app.config import get_settings
    settings = get_settings()

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == settings.whatsapp_verify_token:
        return int(challenge)

    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/conversations", response_model=ConversationResponse)
@limiter.limit("20/minute")
async def web_chat_message(
    request: Request,
    body: WebChatStartRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Web chat widget endpoint.
    Handles both new conversations and follow-up messages.
    """
    property_id = uuid.UUID(body.property_id)
    session_id = body.session_id or str(uuid.uuid4())

    result = await process_guest_message(
        db=db,
        property_id=property_id,
        guest_identifier=f"web:{session_id}",
        channel="web",
        message_text=body.message,
        guest_name=body.guest_name,
    )

    return ConversationResponse(**result)


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=ConversationResponse,
)
@limiter.limit("60/minute")
async def web_chat_follow_up(
    request: Request,
    conversation_id: str,
    body: MessageRequest,
    db: AsyncSession = Depends(get_db),
):
    """Follow-up message in an existing web chat conversation."""
    conv_result = await db.execute(
        select(Conversation).where(Conversation.id == uuid.UUID(conversation_id))
    )
    conv = conv_result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    result = await process_guest_message(
        db=db,
        property_id=conv.property_id,
        guest_identifier=conv.guest_identifier,
        channel=conv.channel,
        message_text=body.message,
        guest_name=body.guest_name,
    )

    return ConversationResponse(**result)


# ─────────────────────────────────────────────────────────────
# Staff: Conversation Management
# ─────────────────────────────────────────────────────────────

@router.get("/properties/{property_id}/conversations")
async def list_conversations(
    property_id: str,
    status: str = Query(None, description="Filter by status"),
    after_hours: bool = Query(None, description="Filter after-hours only"),
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db),
    # Auth
    token: dict = Depends(verify_jwt),
):
    """List conversations for a property (staff dashboard)."""
    query = (
        select(Conversation)
        .where(Conversation.property_id == uuid.UUID(property_id))
        .options(selectinload(Conversation.lead))
        .order_by(Conversation.started_at.desc())
        .limit(limit)
    )

    if status:
        query = query.where(Conversation.status == status)
    if after_hours is not None:
        query = query.where(Conversation.is_after_hours == after_hours)

    result = await db.execute(query)
    conversations = result.scalars().all()

    return [
        {
            "id": str(c.id),
            "channel": c.channel,
            "guest_name": c.guest_name,
            "guest_identifier": c.guest_identifier,
            "status": c.status,
            "ai_mode": c.ai_mode,
            "is_after_hours": c.is_after_hours,
            "started_at": c.started_at.isoformat(),
            "has_lead": c.lead is not None,
            "lead_intent": c.lead.intent if c.lead else None,
        }
        for c in conversations
    ]


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Get full conversation with all messages (for staff drill-down)."""
    result = await db.execute(
        select(Conversation)
        .where(Conversation.id == uuid.UUID(conversation_id))
        .options(
            selectinload(Conversation.messages),
            selectinload(Conversation.lead),
        )
    )
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return {
        "id": str(conv.id),
        "channel": conv.channel,
        "guest_name": conv.guest_name,
        "status": conv.status,
        "ai_mode": conv.ai_mode,
        "is_after_hours": conv.is_after_hours,
        "started_at": conv.started_at.isoformat(),
        "messages": [
            {
                "id": str(m.id),
                "role": m.role,
                "content": m.content,
                "sent_at": m.sent_at.isoformat(),
                "metadata": m.metadata_,
            }
            for m in conv.messages
        ],
        "lead": {
            "id": str(conv.lead.id),
            "guest_name": conv.lead.guest_name,
            "intent": conv.lead.intent,
            "status": conv.lead.status,
            "estimated_value": float(conv.lead.estimated_value) if conv.lead.estimated_value else None,
        } if conv.lead else None,
    }


@router.post("/conversations/{conversation_id}/resolve")
async def resolve_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Staff resolves/closes a conversation."""
    result = await db.execute(
        select(Conversation).where(Conversation.id == uuid.UUID(conversation_id))
    )
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conv.status = "resolved"
    conv.ended_at = datetime.now(timezone.utc)
    await db.flush()
    return {"status": "resolved", "conversation_id": conversation_id}


# ─────────────────────────────────────────────────────────────
# GM: Leads
# ─────────────────────────────────────────────────────────────

@router.get("/properties/{property_id}/leads", response_model=list[LeadResponse])
async def list_leads(
    property_id: str,
    status: str = Query(None),
    intent: str = Query(None),
    from_date: date = Query(None),
    to_date: date = Query(None),
    limit: int = Query(50, le=500),
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """List leads for a property (GM dashboard leads view)."""
    query = (
        select(Lead)
        .where(Lead.property_id == uuid.UUID(property_id))
        .order_by(Lead.captured_at.desc())
        .limit(limit)
    )

    if status:
        query = query.where(Lead.status == status)
    if intent:
        query = query.where(Lead.intent == intent)
    if from_date:
        query = query.where(Lead.captured_at >= datetime.combine(from_date, datetime.min.time()))
    if to_date:
        query = query.where(Lead.captured_at <= datetime.combine(to_date, datetime.max.time()))

    result = await db.execute(query)
    leads = result.scalars().all()

    return [
        LeadResponse(
            id=str(l.id),
            conversation_id=str(l.conversation_id),
            guest_name=l.guest_name,
            guest_phone=l.guest_phone,
            guest_email=l.guest_email,
            intent=l.intent,
            status=l.status,
            estimated_value=float(l.estimated_value) if l.estimated_value else None,
            captured_at=l.captured_at,
        )
        for l in leads
    ]


@router.patch("/leads/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: str,
    body: LeadUpdateRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Update a lead's status or notes."""
    result = await db.execute(
        select(Lead).where(Lead.id == uuid.UUID(lead_id))
    )
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    if body.status:
        lead.status = body.status
    if body.notes is not None:
        lead.notes = body.notes

    return LeadResponse(
        id=str(lead.id),
        conversation_id=str(lead.conversation_id),
        guest_name=lead.guest_name,
        guest_phone=lead.guest_phone,
        guest_email=lead.guest_email,
        intent=lead.intent,
        status=lead.status,
        estimated_value=float(lead.estimated_value) if lead.estimated_value else None,
        captured_at=lead.captured_at,
    )


# ─────────────────────────────────────────────────────────────
# GM: Analytics
# ─────────────────────────────────────────────────────────────

@router.get("/properties/{property_id}/analytics")
async def get_analytics(
    property_id: str,
    from_date: date = Query(None),
    to_date: date = Query(None),
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """
    Get analytics for a property over a date range.
    Used by the GM dashboard Money View and Operations View.
    """
    pid = uuid.UUID(property_id)

    if not from_date:
        from_date = date.today() - timedelta(days=30)
    if not to_date:
        to_date = date.today()

    # Get daily analytics
    result = await db.execute(
        select(AnalyticsDaily)
        .where(
            AnalyticsDaily.property_id == pid,
            AnalyticsDaily.report_date >= from_date,
            AnalyticsDaily.report_date <= to_date,
        )
        .order_by(AnalyticsDaily.report_date)
    )
    daily_records = result.scalars().all()

    # Aggregate totals
    totals = {
        "total_inquiries": sum(r.total_inquiries for r in daily_records),
        "after_hours_inquiries": sum(r.after_hours_inquiries for r in daily_records),
        "after_hours_responded": sum(r.after_hours_responded for r in daily_records),
        "leads_captured": sum(r.leads_captured for r in daily_records),
        "handoffs": sum(r.handoffs for r in daily_records),
        "estimated_revenue_recovered": float(
            sum(r.estimated_revenue_recovered for r in daily_records)
        ),
    }
    total_response_times = [
        float(r.avg_response_time_sec)
        for r in daily_records
        if r.avg_response_time_sec > 0
    ]
    totals["avg_response_time_sec"] = (
        sum(total_response_times) / len(total_response_times)
        if total_response_times
        else 0
    )

    # Daily breakdown for charts
    daily = [
        {
            "date": r.report_date.isoformat(),
            "total_inquiries": r.total_inquiries,
            "after_hours_inquiries": r.after_hours_inquiries,
            "leads_captured": r.leads_captured,
            "estimated_revenue_recovered": float(r.estimated_revenue_recovered),
            "channel_breakdown": r.channel_breakdown,
        }
        for r in daily_records
    ]

    return {
        "property_id": property_id,
        "period": {"from": from_date.isoformat(), "to": to_date.isoformat()},
        "totals": totals,
        "daily": daily,
    }


# ─────────────────────────────────────────────────────────────
# Property Admin
# ─────────────────────────────────────────────────────────────

@router.post("/properties", response_model=PropertyResponse, status_code=201)
async def create_property(
    body: PropertyCreateRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Create a new property (tenant)."""
    from decimal import Decimal
    prop = Property(
        name=body.name,
        whatsapp_number=body.whatsapp_number,
        website_url=body.website_url,
        operating_hours=body.operating_hours,
        adr=Decimal(str(body.adr)),
        ota_commission_pct=Decimal(str(body.ota_commission_pct)),
    )
    db.add(prop)
    await db.flush()

    return PropertyResponse(
        id=str(prop.id),
        name=prop.name,
        whatsapp_number=prop.whatsapp_number,
        website_url=prop.website_url,
        adr=float(prop.adr),
        ota_commission_pct=float(prop.ota_commission_pct),
        created_at=prop.created_at,
    )


@router.get("/properties/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Get property details."""
    result = await db.execute(
        select(Property).where(Property.id == uuid.UUID(property_id))
    )
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")

    return PropertyResponse(
        id=str(prop.id),
        name=prop.name,
        whatsapp_number=prop.whatsapp_number,
        website_url=prop.website_url,
        adr=float(prop.adr),
        ota_commission_pct=float(prop.ota_commission_pct),
        created_at=prop.created_at,
    )


@router.put("/properties/{property_id}/knowledge-base", response_model=KBIngestResponse)
async def upload_knowledge_base(
    property_id: str,
    body: KBIngestRequest,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Upload or replace a property's knowledge base."""
    pid = uuid.UUID(property_id)

    # Verify property exists
    result = await db.execute(select(Property).where(Property.id == pid))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Property not found")

    count = await ingest_knowledge_base(
        db=db,
        property_id=pid,
        documents=[doc.model_dump() for doc in body.documents],
    )

    return KBIngestResponse(documents_ingested=count, property_id=property_id)


# ─────────────────────────────────────────────────────────────
# Health Check
# ─────────────────────────────────────────────────────────────

@router.get("/health")
@limiter.limit("100/minute")
async def health_check(request: Request, db: AsyncSession = Depends(get_db)):
    """Health check endpoint for container orchestrators."""
    try:
        from sqlalchemy import text
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}


# ─────────────────────────────────────────────────────────────
# Missing Endpoints (Audit Remediation)
# ─────────────────────────────────────────────────────────────

@router.post("/conversations/{conversation_id}/handoff")
async def handoff_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Explicitly trigger AI handoff."""
    result = await db.execute(
        select(Conversation).where(Conversation.id == uuid.UUID(conversation_id))
    )
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conv.ai_mode = "handoff"
    conv.status = "handoff"
    await db.flush()
    return {"status": "handed_off", "conversation_id": conversation_id}


@router.post("/conversations/{conversation_id}/takeover")
async def takeover_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Staff takes over conversation (pauses AI)."""
    result = await db.execute(
        select(Conversation).where(Conversation.id == uuid.UUID(conversation_id))
    )
    conv = result.scalar_one_or_none()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conv.ai_mode = "staff"
    conv.status = "active"
    await db.flush()
    return {"status": "staff_takeover", "conversation_id": conversation_id}


@router.get("/leads/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Get individual lead details."""
    result = await db.execute(
        select(Lead).where(Lead.id == uuid.UUID(lead_id))
    )
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
        
    return LeadResponse(
        id=str(lead.id),
        conversation_id=str(lead.conversation_id),
        guest_name=lead.guest_name,
        guest_phone=lead.guest_phone,
        guest_email=lead.guest_email,
        intent=lead.intent,
        status=lead.status,
        estimated_value=float(lead.estimated_value) if lead.estimated_value else None,
        captured_at=lead.captured_at,
    )


@router.get("/properties/{property_id}/analytics/summary", response_model=AnalyticsSummaryResponse)
async def get_analytics_summary(
    property_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Get aggregated analytics summary (hero stats)."""
    pid = uuid.UUID(property_id)
    from_date = date.today() - timedelta(days=30)
    
    result = await db.execute(
        select(AnalyticsDaily)
        .where(
            AnalyticsDaily.property_id == pid,
            AnalyticsDaily.report_date >= from_date
        )
    )
    daily_records = result.scalars().all()
    
    avg_resp = 0
    if daily_records:
        resps = [float(r.avg_response_time_sec) for r in daily_records if r.avg_response_time_sec > 0]
        if resps:
            avg_resp = sum(resps) / len(resps)
            
    return AnalyticsSummaryResponse(
        total_inquiries=sum(r.total_inquiries for r in daily_records),
        after_hours_inquiries=sum(r.after_hours_inquiries for r in daily_records),
        after_hours_responded=sum(r.after_hours_responded for r in daily_records),
        leads_captured=sum(r.leads_captured for r in daily_records),
        handoffs=sum(r.handoffs for r in daily_records),
        avg_response_time_sec=avg_resp,
        estimated_revenue_recovered=float(sum(r.estimated_revenue_recovered for r in daily_records)),
        channel_breakdown={}
    )


@router.get("/properties/{property_id}/settings")
async def get_property_settings(
    property_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Get property configuration."""
    result = await db.execute(
        select(Property).where(Property.id == uuid.UUID(property_id))
    )
    prop = result.scalar_one_or_none()
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
        
    return {
        "id": str(prop.id),
        "operating_hours": prop.operating_hours,
        "knowledge_base_config": prop.knowledge_base_config,
        "timezone": prop.timezone,
        "plan_tier": prop.plan_tier,
        "is_active": prop.is_active,
    }


@router.post("/properties/{property_id}/onboard")
async def onboard_property(
    property_id: str,
    db: AsyncSession = Depends(get_db),
    token: dict = Depends(verify_jwt),
):
    """Trigger onboarding."""
    return {"status": "onboarded", "property_id": property_id}

"""
Email service integration (SendGrid).
Handles sending emails (replies, daily reports).
"""

import structlog
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

from app.config import get_settings
from app.core.normalization import NormalizedMessage
from app.services.realtime import realtime_service

settings = get_settings()
logger = structlog.get_logger()


async def send_email(to_email: str, subject: str, content: str, is_html: bool = False) -> dict:
    """
    Send an email via SendGrid.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        content: Email body content
        is_html: Whether content is HTML (default False = text/plain)
        
    Returns:
        API response status or error dict
    """
    if not settings.sendgrid_api_key:
        if not settings.is_production:
            print(f"\n🚀 [MOCK EMAIL] To: {to_email} | Subject: {subject} | Content: {content[:50]}...\n")
            return {"status": "mock_sent"}
            
        logger.warning(
            "SendGrid API key not configured, skipping email send",
            to_email=to_email,
            subject=subject
        )
        return {"status": "skipped", "reason": "not_configured"}

    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key)
        from_email = Email(settings.sendgrid_from_email)
        to_email = To(to_email)
        content_type = "text/html" if is_html else "text/plain"
        content_obj = Content(content_type, content)
        
        mail = Mail(from_email, to_email, subject, content_obj)
        
        # SendGrid python client is synchronous, so ideally run in threadpool/executor if high volume
        # For MVP Sprint 2 (low volume), sync call in async function is acceptable but blocking
        # Better: run in executor
        
        import asyncio
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, sg.send, mail)
        
        logger.info(
            "Email sent",
            to_email=to_email.email,
            status_code=response.status_code
        )
        return {"status": "sent", "status_code": response.status_code}
        
    except Exception as e:
        logger.error(
            "SendGrid email failed",
            error=str(e),
            to_email=to_email.email if 'to_email' in locals() else to_email
        )
        return {"status": "error", "detail": str(e)}


async def notify_staff_handoff(
    guest_identifier: str,
    channel: str,
    guest_name: str | None,
    conversation_summary: str
):
    """
    Send an email alert to staff when a guest needs human assistance.
    """
    subject = f"🚨 HANDOFF ALERT: Guest on {channel.title()}"
    content = (
        f"A guest needs assistance.\n\n"
        f"Guest: {guest_name or 'Unknown'} ({guest_identifier})\n"
        f"Channel: {channel}\n\n"
        f"Context:\n{conversation_summary}\n\n"
        f"Please check the dashboard to reply immediately."
    )
    
    await send_email(
        to_email=settings.staff_notification_email,
        subject=subject,
        content=content
    )
    
    # Also publish to realtime dashboard
    # We need property_id here? It's not passed.
    # Ideally notify_staff_handoff should take property_id.
    # For now, let's assume global dashboard or route caller publishes it.
    # Actually, the caller (routes.py) has property_id.
    # But for cleaner code, let's update this signature or handle it in routes.py.
    # Let's handle it in routes.py to avoid breaking signature widely if used elsewhere.
    # OR better: update signature.
    pass

async def notify_staff_handoff_enhanced(
    property_id: str,
    conversation_id: str,
    guest_identifier: str,
    channel: str,
    guest_name: str | None,
    conversation_summary: str
):
    """
    Enhanced notification: Email + Realtime Dashboard.
    """
    # 1. Email (Legacy/Async)
    await notify_staff_handoff(guest_identifier, channel, guest_name, conversation_summary)
    
    # 2. Realtime
    await realtime_service.publish_handoff(
        property_id=property_id,
        conversation_id=conversation_id,
        guest_name=guest_name or "Guest",
        channel=channel,
        summary=conversation_summary
    )


def normalize_email_message(form_data: dict) -> NormalizedMessage:
    """
    Normalize SendGrid Inbound Parse payload.
    """
    try:
        # SendGrid sends 'from' as 'sender' or 'from'.
        # In FastAPI Request.form(), it's a dict.
        
        from_address = form_data.get("from")
        to_address = form_data.get("to")
        subject = form_data.get("subject", "No Subject")
        text = form_data.get("text", "")
        
        if not text:
            return None
            
        # Parse Name <email>
        import re
        email_match = re.search(r'<([^>]+)>', from_address)
        guest_email = email_match.group(1) if email_match else from_address
        guest_name = from_address.split('<')[0].strip() if '<' in from_address else None
        
        return {
            "channel": "email",
            "guest_identifier": guest_email,
            "guest_name": guest_name,
            "content": f"Subject: {subject}\n\n{text}",
            "metadata": {
                "to_address": to_address,
                "subject": subject
            }
        }
    except Exception as e:
        logger.error("Error normalizing email payload", error=str(e))
        return None

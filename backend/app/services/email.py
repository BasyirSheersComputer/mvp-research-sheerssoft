"""
Email service integration (SendGrid).
Handles sending emails (replies, daily reports).
"""

import structlog
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

from app.config import get_settings

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

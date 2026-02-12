"""
WhatsApp Cloud API integration service.
Handles sending messages via Meta Graph API.
"""

import httpx
import structlog
from app.config import get_settings

settings = get_settings()
logger = structlog.get_logger()

WHATSAPP_API_URL = "https://graph.facebook.com/v19.0"


async def send_whatsapp_message(to_number: str, message_text: str) -> dict:
    """
    Send a text message via WhatsApp Cloud API.
    
    Args:
        to_number: Recipient phone number (e.g. "60123456789")
        message_text: The message body
        
    Returns:
        The API response JSON or error dict
    """
    if not settings.whatsapp_api_token or not settings.whatsapp_phone_number_id:
        logger.warning(
            "WhatsApp API not configured, skipping send",
            to_number=to_number,
            message_text=message_text[:50]
        )
        return {"status": "skipped", "reason": "not_configured"}

    url = f"{WHATSAPP_API_URL}/{settings.whatsapp_phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_api_token}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text},
    }

    transport = httpx.AsyncHTTPTransport(retries=3)
    async with httpx.AsyncClient(transport=transport) as client:
        try:
            response = await client.post(url, json=payload, headers=headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            logger.info(
                "WhatsApp message sent",
                to_number=to_number,
                message_id=data.get("messages", [{}])[0].get("id")
            )
            return data
            
        except httpx.HTTPStatusError as e:
            logger.error(
                "WhatsApp API error",
                status_code=e.response.status_code,
                response=e.response.text,
                to_number=to_number
            )
            return {"status": "error", "detail": str(e), "response": e.response.text}
            
        except Exception as e:
            logger.error(
                "WhatsApp send failed",
                error=str(e),
                to_number=to_number
            )
            return {"status": "error", "detail": str(e)}

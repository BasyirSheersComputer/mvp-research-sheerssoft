
import structlog
import httpx
from app.config import get_settings
from app.core.normalization import NormalizedMessage

logger = structlog.get_logger()

async def send_whatsapp_message(to_number: str, message_text: str):
    """
    Sends a WhatsApp message via Meta Cloud API using async HTTP client.
    """
    settings = get_settings()
    
    # Check if we are in production or have a valid token
    # For Sprint 2 Simulator: Trust the log unless configured
    if not settings.whatsapp_api_token or not settings.whatsapp_phone_number_id:
        if not settings.is_production:
            print(f"\n🚀 [MOCK WHATSAPP] To: {to_number} | Msg: {message_text}\n")
            return {"status": "mock_sent"}
        
        logger.warning("WhatsApp API credentials missing", to=to_number)
        return {"status": "skipped", "reason": "missing_credentials"}

    url = f"https://graph.facebook.com/v18.0/{settings.whatsapp_phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {settings.whatsapp_api_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload, timeout=10.0)
            response.raise_for_status()
            logger.info("WhatsApp message sent", to=to_number, status=response.status_code)
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error("WhatsApp API error", status=e.response.status_code, response=e.response.text)
            raise
        except Exception as e:
            logger.error("WhatsApp send failed", error=str(e))
            raise

def normalize_whatsapp_message(payload: dict) -> NormalizedMessage:
    """
    Parse raw WhatsApp webhook payload into NormalizedMessage.
    Raises ValueError if payload is invalid or property_id cannot be determined here.
    Note: property_id relies on phone_number_id mapping which happens at route level.
    So this function returns a partial structure or dictates how to extract fields.
    
    Actually, to keep it clean, we extract the core fields here.
    """
    try:
        entry = payload.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
            return None
            
        msg = messages[0]
        from_number = msg.get("from")
        text_body = msg.get("text", {}).get("body")
        
        # Determine guest name
        contacts = value.get("contacts", [])
        guest_name = None
        if contacts:
            guest_name = contacts[0].get("profile", {}).get("name")
            
        # Get phone number ID for property lookup
        phone_number_id = value.get("metadata", {}).get("phone_number_id")
        
        if not from_number or not text_body:
            return None
            
        # We return a dict-like structure or simpler object to be enriched with property_id
        return {
            "channel": "whatsapp",
            "guest_identifier": from_number,
            "guest_name": guest_name,
            "content": text_body,
            "metadata": {
                "phone_number_id": phone_number_id,
                "whatsapp_message_id": msg.get("id")
            }
        }
        
    except Exception as e:
        logger.error("Error normalizing WhatsApp payload", error=str(e))
        return None

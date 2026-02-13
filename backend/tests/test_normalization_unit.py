
import pytest
from app.services.whatsapp import normalize_whatsapp_message
from app.services.email import normalize_email_message

def test_normalize_whatsapp():
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "display_phone_number": "1234567890",
                        "phone_number_id": "PHONE_NUMBER_ID"
                    },
                    "contacts": [{
                        "profile": {"name": "Test User"},
                        "wa_id": "16315551234"
                    }],
                    "messages": [{
                        "from": "16315551234",
                        "id": "wamid.HBgL...",
                        "timestamp": "1603059201",
                        "text": {"body": "Hello world"},
                        "type": "text"
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    
    normalized = normalize_whatsapp_message(payload)
    assert normalized is not None
    assert normalized["channel"] == "whatsapp"
    assert normalized["guest_identifier"] == "16315551234"
    assert normalized["guest_name"] == "Test User"
    assert normalized["content"] == "Hello world"
    assert normalized["metadata"]["phone_number_id"] == "PHONE_NUMBER_ID"

def test_normalize_email():
    payload = {
        "from": "John Doe <john@example.com>",
        "to": "reservations@hotel.com",
        "subject": "Booking Inquiry",
        "text": "I would like to book a room for 2 nights."
    }
    
    normalized = normalize_email_message(payload)
    assert normalized is not None
    assert normalized["channel"] == "email"
    assert normalized["guest_identifier"] == "john@example.com"
    assert normalized["guest_name"] == "John Doe"
    assert "Subject: Booking Inquiry" in normalized["content"]
    assert "I would like to book a room" in normalized["content"]

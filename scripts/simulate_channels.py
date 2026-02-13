import asyncio
import httpx
import json
import uuid
import sys
import os

# Add backend to path to import models if needed (though mostly HTTP here)
# sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

BASE_URL = "http://localhost:8000/api/v1"

async def simulate_whatsapp_message(text, from_number="60123456789", guest_name="Ali Guest"):
    """
    Simulates a webhook event from WhatsApp Cloud API.
    """
    print(f"\n📱 [WhatsApp Sim] Sending: '{text}' from {guest_name} ({from_number})")
    
    # Payload structure matches Meta's object
    payload = {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "WHATSAPP_BUSINESS_ID",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "15555555555",
                                "phone_number_id": "60193166666" # Matches Seeded Vivatel Number
                            },
                            "contacts": [
                                {
                                    "profile": {"name": guest_name},
                                    "wa_id": from_number
                                }
                            ],
                            "messages": [
                                {
                                    "from": from_number,
                                    "id": str(uuid.uuid4()),
                                    "timestamp": "1707800000",
                                    "text": {"body": text},
                                    "type": "text"
                                }
                            ]
                        },
                        "field": "messages"
                    }
                ]
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/webhook/whatsapp", json=payload)
        print(f"   Response: {response.status_code} {response.text}")
        if response.status_code != 200:
            print("   ❌ Webhook failed!")

async def simulate_email_message(subject, body, from_email="ali@gmail.com", guest_name="Ali Guest"):
    """
    Simulates a webhook event from SendGrid Inbound Parse.
    """
    print(f"\n📧 [Email Sim] Sending: Subject='{subject}' from {guest_name} <{from_email}>")
    
    # SendGrid sends multipart/form-data
    data = {
        "from": f"{guest_name} <{from_email}>",
        "to": "reservations@vivatel.com.my",
        "subject": subject,
        "text": body,
        "html": f"<p>{body}</p>",
        # SendGrid sends many other fields (SPF, DKIM, etc.) but we only need these
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/webhook/email", data=data)
        print(f"   Response: {response.status_code} {response.text}")

async def main():
    print("🚀 Starting Channel Simulator...")
    print("Target: Vivatel Kuala Lumpur (Seeded)")

    # 1. WhatsApp Conversation
    await simulate_whatsapp_message("Hi, do you have rooms available tomorrow?")
    await asyncio.sleep(2) # Wait for async processing
    
    # 2. Email Inquiry
    await simulate_email_message(
        subject="Group Booking Enquiry", 
        body="Hello, I would like to book 5 rooms for next weekend. Do you have a corporate rate?"
    )
    
    # 3. Handoff Trigger (WhatsApp)
    await asyncio.sleep(2)
    await simulate_whatsapp_message("I want to speak to a manager about a complaint.")

    print("\n✅ Simulation requests sent. Check backend logs for AI replies.")

if __name__ == "__main__":
    asyncio.run(main())

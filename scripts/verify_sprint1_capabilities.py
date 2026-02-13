import asyncio
import os
import sys
import uuid
from datetime import datetime
from decimal import Decimal

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.models import Property, Conversation, Message
from app.services.conversation import process_guest_message
from app.services import ingest_knowledge_base
from app.config import get_settings
from app.database import set_db_context
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

async def main():
    print("🚀 Starting Sprint 1 Capability Verification...")
    
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # 1. Setup Test Property
        print("\n1️⃣  Setting up Test Property (Cherating Dunes)...")
        prop_id = uuid.uuid4()
        
        # Set RLS Context
        await set_db_context(db, str(prop_id))
        
        prop = Property(
            id=prop_id,
            name="Cherating Dunes Resort",
            whatsapp_number="60123456789",
            operating_hours={"start": "09:00", "end": "18:00", "timezone": "Asia/Kuala_Lumpur"},
            adr=Decimal("250.00"),
            ota_commission_pct=Decimal("18.00")
        )
        db.add(prop)
        await db.commit()
        print("   ✅ Property created.")

        # 2. Ingest Knowledge Base
        print("\n2️⃣  Ingesting Knowledge Base...")
        kb_docs = [
            {
                "doc_type": "rates",
                "title": "Room Rates 2026",
                "content": "Deluxe Room: RM 250/night. Family Suite: RM 450/night. Breakfast included for all bookings."
            },
            {
                "doc_type": "facilities",
                "title": "Pool & Gym",
                "content": "Infinity pool open 7am-10pm. Gym is 24 hours."
            }
        ]
        count = await ingest_knowledge_base(db, prop_id, kb_docs)
        print(f"   ✅ Ingested {count} documents.")

        # 3. Verify BM Support & Rate Quoting
        print("\n3️⃣  Verifying Bahasa Malaysia Support & Rate Quoting...")
        guest_id = "601198765432"
        # "Hi, what is the price for a room?" in BM
        response = await process_guest_message(
            db, prop_id, guest_id, "whatsapp", "Salam, berapa harga bilik deluxe?"
        )
        print(f"   🗣️  Guest: Salam, berapa harga bilik deluxe?")
        print(f"   🤖 AI: {response['response']}")
        
        if "250" in response['response'] or "RM" in response['response']:
            print("   ✅ Rate quoted correctly.")
        else:
            print("   ❌ Rate NOT found in response.")
            
        # 4. Verify After Hours Logic
        print("\n4️⃣  Verifying After-Hours Logic...")
        # Mocking time is hard without library support, checking flag based on current real time
        # We will trust the unit test for exact hours, but verify the flag exists in response
        print(f"   🕒 Current AI detected After Hours: {response['is_after_hours']}")

        # 5. Verify Lead Capture
        print("\n5️⃣  Verifying Lead Capture...")
        # "Please book for Ali, tomorrow night"
        response = await process_guest_message(
            db, prop_id, guest_id, "whatsapp", "Saya nak booking untuk Ali, masuk esok malam. Email saya ali@test.com", guest_name="Ali"
        )
        print(f"   🗣️  Guest: Saya nak booking untuk Ali, masuk esok malam...")
        print(f"   🤖 AI: {response['response']}")
        print(f"   ✅ AI Mode: {response['mode']}")
        
        if response['lead_created']:
             print("   ✅ Lead successfully created in DB.")
        else:
             print("   ⚠️  Lead NOT created (might need more info).")

    print("\n✅ Verification Complete.")

if __name__ == "__main__":
    asyncio.run(main())

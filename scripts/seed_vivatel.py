import asyncio
import os
import sys
import uuid
from decimal import Decimal
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.models import Property, KBDocument
from app.services import ingest_knowledge_base
from app.config import get_settings
from app.database import set_db_context

async def seed_vivatel():
    print("🚀 Seeding Vivatel Kuala Lumpur...")
    
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as db:
        # 1. Create Property
        # Use a fixed UUID for Vivatel so we can reference it easily
        vivatel_id = uuid.UUID("a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11")
        
        # Set RLS context to allow creation/access
        await set_db_context(db, str(vivatel_id))
        
        existing = await db.get(Property, vivatel_id)
        if existing:
            print("   ⚠️  Vivatel property already exists. Updating...")
            prop = existing
        else:
            prop = Property(id=vivatel_id)
            
        prop.name = "Vivatel Kuala Lumpur"
        prop.whatsapp_number = "60193166666" # Mock number
        prop.notification_email = "reservations@vivatel.com.my"
        prop.website_url = "https://www.vivatel.com.my"
        prop.operating_hours = {"start": "09:00", "end": "18:00", "timezone": "Asia/Kuala_Lumpur"}
        prop.adr = Decimal("280.00")
        prop.ota_commission_pct = Decimal("18.00")
        prop.slug = "vivatel-kl"
        prop.plan_tier = "pilot"
        
        db.add(prop)
        await db.commit()
        print(f"   ✅ Property 'Vivatel Kuala Lumpur' ({vivatel_id}) ready.")

        # 2. Ingest Knowledge Base (Bilingual)
        print("\n2️⃣  Ingesting Bilingual Knowledge Base...")
        kb_docs = [
            {
                "doc_type": "rates",
                "title": "Room Rates / Harga Bilik 2026",
                "content": """
                **Supreme Deluxe Room**: RM 280 (Weekdays), RM 320 (Weekends).
                **Grand Suite**: RM 550 (Weekdays), RM 650 (Weekends).
                
                *Breakfast included for 2 pax.*
                *Sarapan termasuk untuk 2 orang.*
                """
            },
            {
                "doc_type": "facilities",
                "title": "Pool & Gym / Kolam & Gim",
                "content": """
                **Swimming Pool**: Level 5. Open 7:00 AM - 9:00 PM.
                **Gym**: Level 5. Open 24 hours with keycard.
                
                **Kolam Renang**: Tingkat 5. Buka 7:00 pagi - 9:00 malam.
                **Gim**: Tingkat 5. Buka 24 jam dengan kad akses.
                """
            },
             {
                "doc_type": "policies",
                "title": "Check-in & Check-out",
                "content": """
                Check-in: 3:00 PM. Check-out: 12:00 PM.
                Late check-out until 2:00 PM available for RM 50 (subject to availability).
                
                Daftar masuk: 3:00 petang. Daftar keluar: 12:00 tengah hari.
                """
            }
        ]
        
        # We need to re-set context just in case (though session persists)
        await set_db_context(db, str(vivatel_id))
        
        count = await ingest_knowledge_base(db, vivatel_id, kb_docs)
        print(f"   ✅ Ingested {count} documents for Vivatel.")

    print("\n✅ Vivatel Seeding Complete.")

if __name__ == "__main__":
    asyncio.run(seed_vivatel())

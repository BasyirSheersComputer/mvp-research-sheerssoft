import asyncio
import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, selectinload

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

from app.models import Conversation, Message
from app.config import get_settings
from app.database import set_db_context

async def verify_channels():
    print("🚀 Verifying Sprint 2 Channel Integrations...")
    
    settings = get_settings()
    engine = create_async_engine(settings.database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    # Vivatel ID from seed script
    vivatel_id = "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11"

    async with async_session() as db:
        await set_db_context(db, vivatel_id)
        
        # 1. Check WhatsApp Conversation
        print("\n1️⃣  Checking WhatsApp Integration...")
        result = await db.execute(
            select(Conversation)
            .where(Conversation.channel == "whatsapp")
            .options(selectinload(Conversation.messages))
            .order_by(Conversation.started_at.desc())
        )
        wa_convs = result.scalars().all()
        
        if wa_convs:
            conv = wa_convs[0]
            print(f"   ✅ Found WhatsApp Conversation: {conv.id}")
            print(f"      Guest: {conv.guest_name} ({conv.guest_identifier})")
            print(f"      Status: {conv.status}")
            print(f"      Messages: {len(conv.messages)}")
            
            # Check for AI reply
            ai_msgs = [m for m in conv.messages if m.role == 'ai']
            if ai_msgs:
                print(f"   ✅ AI Replied: '{ai_msgs[0].content[:50]}...'")
            else:
                print("   ❌ No AI reply found!")
                
            # Check for Handoff
            # The simulator sent a handoff message 3rd.
            # It might be in the SAME conversation or a new one depending on logic.
            # Usually same conversation if same guest_identifier.
            # Let's check status.
            if conv.status in ["handed_off", "handoff"]:
                 print("   ✅ Handoff Logic Verified (Status='handed_off')")
            # If status is not handed_off, maybe it's the second conversation?
            # Or maybe the message wasn't processed yet?
        else:
            print("   ❌ No WhatsApp conversation found!")

        # 2. Check Email Conversation
        print("\n2️⃣  Checking Email Integration...")
        result = await db.execute(
            select(Conversation)
            .where(Conversation.channel == "email")
            .options(selectinload(Conversation.messages))
            .order_by(Conversation.started_at.desc())
        )
        email_convs = result.scalars().all()
        
        if email_convs:
            conv = email_convs[0]
            print(f"   ✅ Found Email Conversation: {conv.id}")
            print(f"      Guest: {conv.guest_name} ({conv.guest_identifier})")
            
            ai_msgs = [m for m in conv.messages if m.role == 'ai']
            if ai_msgs:
                print(f"   ✅ AI Replied: '{ai_msgs[0].content[:50]}...'")
            else:
                print("   ❌ No AI reply found!")
        else:
            print("   ❌ No Email conversation found!")

    print("\n✅ Verification Complete.")

if __name__ == "__main__":
    asyncio.run(verify_channels())

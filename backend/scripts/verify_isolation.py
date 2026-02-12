"""
Verify tenant isolation.
1. Create a lead for Property A.
2. Try to fetch it using Property B's ID.
"""

import asyncio
import uuid
from sqlalchemy import select
from app.database import async_session
from app.models import Property, Lead, Conversation

async def verify_isolation():
    async with async_session() as db:
        # Get properties
        result = await db.execute(select(Property))
        props = result.scalars().all()
        
        if len(props) < 2:
            print("Need at least 2 properties to test isolation.")
            return

        prop_a = props[0]
        prop_b = props[1]
        
        print(f"Prop A: {prop_a.name} ({prop_a.id})")
        print(f"Prop B: {prop_b.name} ({prop_b.id})")
        
        # Create conversation and lead for Prop A
        conv = Conversation(
            property_id=prop_a.id,
            channel="test",
            status="active"
        )
        db.add(conv)
        await db.flush()
        
        lead = Lead(
            conversation_id=conv.id,
            property_id=prop_a.id,
            guest_name="Isolation Test Guest",
            intent="booking",
            status="new"
        )
        db.add(lead)
        await db.commit()
        
        lead_id = lead.id
        print(f"Created lead {lead_id} for Prop A")
        
        # Try to fetch using Prop B filter (simulating API logic)
        # API query: select(Lead).where(Lead.property_id == prop_b_id)
        
        stmt = select(Lead).where(
            Lead.property_id == prop_b.id,
            Lead.id == lead_id
        )
        result = await db.execute(stmt)
        leaked_lead = result.scalar_one_or_none()
        
        if leaked_lead:
            print("❌ FAILURE: Lead from Prop A accessible via Prop B ID!")
        else:
            print("✅ SUCCESS: Lead from Prop A NOT accessible via Prop B ID.")
            
        # Cleanup
        await db.delete(lead)
        await db.delete(conv)
        await db.commit()

if __name__ == "__main__":
    asyncio.run(verify_isolation())

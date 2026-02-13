"""
Manual chat interface for testing the AI from the command line.
Usage: python -m scripts.chat_manual
"""

import asyncio
import uuid
import sys
from datetime import datetime

import httpx

API_URL = "http://localhost:8000/api/v1"
# Use the seeded Vivatel property ID (this is the one we fetch dynamically)
DISABLE_SSL_VERIFY = True


async def get_vivatel_property_id():
    """Fetch the Vivatel property ID from the API."""
    async with httpx.AsyncClient() as client:
        # Assuming the seed script ran, we fetch the property by name/filter
        # Since we don't have a search endpoint, we just list properties (not implemented yet?)
        # Ah, we implemented create but not list all properties.
        # But we DO have GET /properties/{id}
        # In seeded setup, we need to know the ID.
        # Let's interact with the database directly or just ask the user to input.
        # BETTER: The seed script prints the ID.
        pass
    return None # Placeholder


async def chat_session():
    print("🤖 Nocturn AI Manual Chat Interface")
    print("---------------------------------")
    print("Connecting to backend...")
    
    # Check health
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{API_URL.replace('/api/v1', '')}/health")
            if resp.status_code != 200:
                print("❌ Backend not healthy. Is it running?")
                sys.exit(1)
        except Exception:
             print("❌ Could not connect to backend at http://localhost:8000")
             sys.exit(1)

    # We need a property ID.
    # For now, let's ask the user to paste it from the seed output, 
    # OR we can hack it by querying the DB directly if we run this via python access to app.database
    
    # Or simpler: Just hardcode a mechanism to 'find first property' 
    # Let's add a quick script to find the property ID
    from app.database import async_session
    from app.models import Property
    from sqlalchemy import select
    
    async with async_session() as db:
        result = await db.execute(select(Property).limit(1))
        prop = result.scalar_one_or_none()
        if not prop:
            print("❌ No property found. Did you run 'python -m scripts.seed_vivatel'?")
            sys.exit(1)
        property_id = str(prop.id)
        property_name = prop.name
        
    print(f"✅ Connected to property: {property_name} (ID: {property_id})")
    print("---------------------------------")
    print("Type your message (or 'quit' to exit)")
    
    guest_identifier = f"manual-test-{uuid.uuid4()}"
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["quit", "exit"]:
            break
            
        start_time = datetime.now()
        
        async with httpx.AsyncClient() as client:
            try:
                # We use the web chat endpoint for simplicity
                payload = {
                    "property_id": property_id,
                    "message": user_input,
                    "guest_name": "Tester",
                    "session_id": guest_identifier
                }
                response = await client.post(f"{API_URL}/conversations", json=payload, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                duration = (datetime.now() - start_time).total_seconds()
                
                print(f"🤖 AI ({duration:.1f}s): {data['response']}")
                if data.get('lead_created'):
                    print("   [LEAD CAPTURED! 🎯]")
                if data.get('mode') == 'handoff':
                    print("   [HANDOFF TRIGGERED! 👤]")
                    
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(chat_session())
    except KeyboardInterrupt:
        print("\nGoodbye!")

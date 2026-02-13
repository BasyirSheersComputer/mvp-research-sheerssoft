import asyncio
import os
import sys
import aiohttp
import uuid
from decimal import Decimal

# Add backend to path for models/config if needed, but we'll try to stick to requests
sys.path.append(os.path.join(os.path.dirname(__file__), "../backend"))

async def verify_dashboard():
    print("🚀 Verifying Sprint 3: Dashboard...")
    
    base_url = "http://localhost:8000/api/v1"
    
    async with aiohttp.ClientSession() as session:
        # 1. Login
        print("\n1️⃣  Testing Login...")
        login_data = {
            "username": "admin",
            "password": "password123"
        }
        async with session.post(f"{base_url}/auth/token", data=login_data) as resp:
            if resp.status != 200:
                print(f"   ❌ Login failed: {resp.status}")
                print(await resp.text())
                return
            
            data = await resp.json()
            token = data["access_token"]
            print(f"   ✅ Login successful. Token obtained.")
            headers = {"Authorization": f"Bearer {token}"}

        # 2. Get Properties
        print("\n2️⃣  Fetching Properties...")
        async with session.get(f"{base_url}/properties", headers=headers) as resp:
            if resp.status != 200:
                print(f"   ❌ Failed to fetch properties: {resp.status}")
                return
            
            props = await resp.json()
            if not props:
                print("   ⚠️  No properties found. Seeding might be needed.")
                return
            
            prop_id = props[0]["id"]
            prop_name = props[0]["name"]
            print(f"   ✅ Found property: {prop_name} ({prop_id})")

        # 3. Get Live Analytics
        print("\n3️⃣  Fetching Live Analytics...")
        async with session.get(f"{base_url}/properties/{prop_id}/analytics/live", headers=headers) as resp:
            if resp.status != 200:
                print(f"   ❌ Failed to fetch analytics: {resp.status}")
                print(await resp.text())
                return
            
            stats = await resp.json()
            print(f"   ✅ Analytics received:")
            print(f"      - Inquiries Today: {stats.get('total_inquiries')}")
            print(f"      - Leads Captured: {stats.get('leads_captured')}")
            print(f"      - Est. Revenue: {stats.get('estimated_revenue_recovered')}")

        # 4. Get Conversations (Inbox)
        print("\n4️⃣  Fetching Conversations (Inbox)...")
        async with session.get(f"{base_url}/properties/{prop_id}/conversations?limit=5", headers=headers) as resp:
            if resp.status != 200:
                print(f"   ❌ Failed to fetch conversations: {resp.status}")
                return
            
            convs = await resp.json()
            print(f"   ✅ Retrieved {len(convs)} conversations.")
            if convs:
                print(f"      - Latest: {convs[0].get('guest_name')} ({convs[0].get('channel')})")

        # 5. Get Leads
        print("\n5️⃣  Fetching Leads...")
        async with session.get(f"{base_url}/properties/{prop_id}/leads", headers=headers) as resp:
            if resp.status != 200:
                print(f"   ❌ Failed to fetch leads: {resp.status}")
                return
            
            leads = await resp.json()
            print(f"   ✅ Retrieved {len(leads)} leads.")
            if leads:
                print(f"      - Latest: {leads[0].get('guest_name')} - Status: {leads[0].get('status')}")

    print("\n✅ Sprint 3 Verification Complete.")

if __name__ == "__main__":
    asyncio.run(verify_dashboard())

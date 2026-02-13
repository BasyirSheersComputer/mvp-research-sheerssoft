import asyncio
import httpx
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001/api/v1"
ADMIN_USER = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password123")

async def main():
    print(f"Starting verification against {BASE_URL}...")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        # 1. Health Check
        print("\n[1] Checking Health...")
        resp = await client.get("/health")
        if resp.status_code == 200:
            print("✅ Health check passed")
            print(f"   Headers: {resp.headers}")
            if "x-request-id" in resp.headers:
                print(f"   ✅ Telemetry Header found: {resp.headers['x-request-id']}")
            else:
                print("   ❌ Telemetry Header MISSING")
        else:
            print(f"❌ Health check failed: {resp.status_code}")
            return

        # 2. Authentication
        print("\n[2] Testing Authentication...")
        resp = await client.post("/auth/token", data={"username": ADMIN_USER, "password": ADMIN_PASSWORD})
        if resp.status_code != 200:
            print(f"❌ Login failed: {resp.text}")
            return
        
        token = resp.json()["access_token"]
        print("✅ Login successful")
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Property Management & Soft Delete Field
        print("\n[3] Testing Property Creation & Schema...")
        prop_name = f"Test Property {datetime.now().isoformat()}"
        resp = await client.post("/properties", json={
            "name": prop_name,
            "adr": 150.0,
            "ota_commission_pct": 18.0
        }, headers=headers)
        
        if resp.status_code != 201:
            print(f"❌ Property creation failed: {resp.text}")
            return
            
        prop_data = resp.json()
        prop_id = prop_data["id"]
        print(f"✅ Property created: {prop_id}")
        
        # Verify deleted_at field exists in response (even if None)
        if "deleted_at" in prop_data:
             print("✅ 'deleted_at' field present in response")
        else:
             print("❌ 'deleted_at' field MISSING in response")

        # 4. Access Control (Self)
        print("\n[4] Testing Access Control (Authorized)...")
        resp = await client.get(f"/properties/{prop_id}", headers=headers)
        if resp.status_code == 200:
            print("✅ Access authorized")
        else:
            print(f"❌ Access failed: {resp.status_code}")

    print("\nVerification Complete.")

if __name__ == "__main__":
    asyncio.run(main())

"""
Load test script.
Simulates 50 concurrent conversations.
"""

import asyncio
import httpx
import time
import uuid

API_URL = "http://localhost:8000/api/v1"
CONCURRENT_USERS = 50

async def simulate_user(i: int):
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Start conversation
        session_id = str(uuid.uuid4())
        payload = {
            "property_id": "7a62dde9-92b6-4b13-bcc5-72814eb9bb23", # Vivatel ID (verified)
            "session_id": session_id,
            "message": "Do you have rooms available?",
            "guest_name": f"LoadTestUser-{i}"
        }
        
        try:
            start_time = time.time()
            resp = await client.post(f"{API_URL}/conversations", json=payload)
            duration = time.time() - start_time
            
            if resp.status_code == 200:
                print(f"User {i}: Success ({duration:.2f}s)")
                return True
            elif resp.status_code == 429:
                print(f"User {i}: Rate Limited ({duration:.2f}s)")
                return False
            else:
                print(f"User {i}: Error {resp.status_code} ({duration:.2f}s)")
                return False
                
        except Exception as e:
            print(f"User {i}: Exception {str(e)}")
            return False

async def main():
    print(f"Starting load test with {CONCURRENT_USERS} concurrent users...")
    tasks = [simulate_user(i) for i in range(CONCURRENT_USERS)]
    
    start_total = time.time()
    results = await asyncio.gather(*tasks)
    end_total = time.time()
    
    success_count = sum(1 for r in results if r)
    print(f"\nLoad Test Complete in {end_total - start_total:.2f}s")
    print(f"Success Rate: {success_count}/{CONCURRENT_USERS} ({success_count/CONCURRENT_USERS*100:.1f}%)")

if __name__ == "__main__":
    # Get property ID first?
    # Hardcoded Vivatel ID: c0768e5f-433a-48b0-abe0-0426c082f10f (from logs/seed)
    # Wait, previous logs showed UUID('c0768e5f...') was used.
    # I'll rely on that. If 404, script will fail.
    asyncio.run(main())

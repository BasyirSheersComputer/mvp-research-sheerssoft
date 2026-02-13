
import httpx
import uuid
import time
import json

# Configuration
API_URL = "http://localhost:8000/api/v1"

def run_uat():
    print("🚀 Starting UAT Scenario: Pilot Launch Readiness (Sync)")
    
    with httpx.Client(timeout=30.0) as client:
        # 1. Admin Login (to get token and property)
        print("\n[Step 1] Authenticating Admin...")
        login_res = client.post(
            f"{API_URL}/auth/token",
            data={"username": "admin", "password": "password123"}
        )
        if login_res.status_code != 200:
            print(f"❌ Login failed: {login_res.text}")
            return
        
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Admin authenticated.")

        # 2. Get Property
        print("\n[Step 2] Fetching Property...")
        prop_res = client.get(f"{API_URL}/properties", headers=headers)
        props = prop_res.json()
        if not props:
            print("❌ No properties found. Please seed the database.")
            return
        
        prop_id = props[0]["id"]
        prop_name = props[0]["name"]
        print(f"✅ Using Property: {prop_name} ({prop_id})")

        # 3. Guest Starts Conversation (Web Widget)
        print("\n[Step 3] Guest starts a chat...")
        session_id = str(uuid.uuid4())
        start_res = client.post(
            f"{API_URL}/conversations",
            json={
                "property_id": prop_id,
                "message": "Hi, I want to book a suite for my honeymoon.",
                "guest_name": "Alice Wonderland",
                "session_id": session_id
            }
        )
        if start_res.status_code != 200:
            print(f"❌ Failed to start chat: {start_res.text}")
            return
            
        conv_data = start_res.json()
        conversation_id = conv_data["conversation_id"]
        ai_reply = conv_data["response"]
        print(f"✅ Chat started. ID: {conversation_id}")
        print(f"🤖 AI Reply: {ai_reply}")

        # 4. Guest triggers Handoff (or AI detects it)
        print("\n[Step 4] Guest asks for human/complex request...")
        followup_res = client.post(
            f"{API_URL}/conversations/{conversation_id}/messages",
            json={
                "message": "I need to speak to a manager immediately about a special arrangement.",
                "guest_name": "Alice Wonderland"
            }
        )
        followup_data = followup_res.json()
        print(f"🤖 AI Reply: {followup_data['response']}")
        print(f"ℹ️  Mode: {followup_data.get('mode', 'unknown')}")
        
        # 5. Verify Dashboard Metrics (Active & Handoff)
        print("\n[Step 5] Verifying Dashboard Metrics...")
        time.sleep(1) 
        
        stats_res = client.get(f"{API_URL}/analytics/dashboard", headers=headers)
        stats = stats_res.json()
        
        print(f"📊 Dashboard Stats:")
        print(f"   - Active Conversations: {stats.get('active_conversations')}")
        print(f"   - Handoffs Pending: {stats.get('handed_off_conversations')}")
        
        conv_detail_res = client.get(f"{API_URL}/conversations/{conversation_id}", headers=headers)
        conv_detail = conv_detail_res.json()
        print(f"ℹ️  Conversation Status: {conv_detail['status']}")
        
        # 6. Staff Resolves Conversation
        print("\n[Step 6] Staff resolves the conversation...")
        resolve_res = client.post(
            f"{API_URL}/conversations/{conversation_id}/resolve",
            headers=headers
        )
        if resolve_res.status_code == 200:
            print("✅ Conversation resolved.")
        else:
            print(f"❌ Failed to resolve: {resolve_res.text}")

        # 7. Final Verification
        print("\n[Step 7] final Metric Check...")
        time.sleep(1)
        stats_final_res = client.get(f"{API_URL}/analytics/dashboard", headers=headers)
        stats_final = stats_final_res.json()
        print(f"📊 Final Stats:")
        print(f"   - Active Conversations: {stats_final.get('active_conversations')}")
        
        print("\n✅ UAT Scenario Complete!")

if __name__ == "__main__":
    run_uat()

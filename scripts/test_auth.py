
import httpx
import time

API_URL = "http://localhost:8001/api/v1"

def test_auth():
    print("Testing Auth...")
    start = time.time()
    try:
        response = httpx.post(
            f"{API_URL}/auth/token",
            data={"username": "admin", "password": "password123"},
            timeout=10.0
        )
        print(f"Status: {response.status_code}")
        print(f"Time: {time.time() - start:.2f}s")
        print(response.json())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_auth()

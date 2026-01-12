
import requests
import sys

def test_screenshot():
    url = "http://127.0.0.1:5000/screenshot/10"
    try:
        print(f"Fetching {url}...")
        resp = requests.get(url)
        print(f"Status: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('content-type')}")
        print(f"Content-Length: {len(resp.content)}")
        if resp.status_code == 200 and len(resp.content) > 0:
            print("SUCCESS: Screenshot served correctly.")
        else:
            print("FAILURE: Screenshot not served.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_screenshot()

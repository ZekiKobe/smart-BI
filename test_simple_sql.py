#!/usr/bin/env python
import requests
import json

def test_simple_sql():
    print("🔍 Testing Simple SQL Generation...")
    print("=" * 50)
    
    # Test with a very simple request
    url = "http://localhost:8000/api/generate-sql"
    payload = {
        "prompt": "Show me all customers",
        "user_id": 1,
        "model": "gemini"
    }
    
    try:
        print(f"Sending request to: {url}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, json=payload, timeout=30)
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"SQL: {result.get('sql', '')}")
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response Text: {response.text[:500]}...")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error - is the server running?")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_simple_sql() 
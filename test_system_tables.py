#!/usr/bin/env python
import requests
import json

def test_system_table_dashboard():
    print("Testing dashboard generation with system tables...")
    
    # Test the new dashboard API with system table queries
    url = "http://localhost:8000/api/generate-dashboard"
    
    test_prompts = [
        "Show me database statistics including transaction commits and rollbacks",
        "Create a dashboard showing table information and column counts",
        "Display user table statistics with insert, update, and delete counts"
    ]
    
    for i, prompt in enumerate(test_prompts):
        print(f"\n{i+1}. Testing prompt: {prompt}")
        
        payload = {
            "prompt": prompt,
            "user_id": 1,
            "model": "Gemini"
        }
        
        try:
            response = requests.post(url, json=payload)
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"   Dashboard ID: {result.get('dashboard_id')}")
                print(f"   Dashboard URL: {result.get('dashboard_url')}")
                print(f"   Message: {result.get('message')}")
            else:
                print(f"❌ Failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_system_table_dashboard() 
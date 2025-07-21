#!/usr/bin/env python
import requests
import json

def test_dashboard_generation():
    print("🎯 Testing Complete Dashboard Generation Pipeline...")
    print("=" * 60)
    
    # Test the dashboard generation API
    url = "http://localhost:8000/api/generate-dashboard"
    
    test_prompts = [
        "Create a dashboard showing database information and current date",
        "Show me a dashboard with database statistics"
    ]
    
    for i, prompt in enumerate(test_prompts):
        print(f"\n{i+1}. Testing dashboard generation: {prompt}")
        
        payload = {
            "prompt": prompt,
            "user_id": 1,
            "model": "gemini"
        }
        
        try:
            response = requests.post(url, json=payload)
            print(f"   Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ SUCCESS!")
                print(f"   Dashboard ID: {result.get('dashboard_id')}")
                print(f"   Dashboard URL: {result.get('dashboard_url')}")
                print(f"   Message: {result.get('message')}")
            else:
                print(f"   ❌ Failed: {response.text[:200]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Dashboard Generation Test Complete!")

if __name__ == "__main__":
    test_dashboard_generation() 
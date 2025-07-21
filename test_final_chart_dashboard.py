#!/usr/bin/env python
import requests
import json

def test_final_chart_dashboard():
    print("🔍 Final Test: Chart and Dashboard Creation...")
    print("=" * 60)
    
    url = "http://localhost:8000/api/generate-dashboard"
    
    # Test with a simple prompt that should work
    prompt = "Show me customer information"
    
    print(f"Testing: {prompt}")
    
    payload = {
        "prompt": prompt,
        "user_id": 1,
        "model": "gemini"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"Dashboard ID: {result.get('dashboard_id')}")
            print(f"Dashboard URL: {result.get('dashboard_url')}")
            print(f"Message: {result.get('message')}")
            
            print(f"\n🎉 Chart and Dashboard Creation is Working!")
            print(f"📊 Check Superset at: http://localhost:8088")
            print(f"🌐 Test UI at: http://localhost:3000")
            
        else:
            print(f"❌ Failed: {response.text[:300]}...")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    test_final_chart_dashboard() 
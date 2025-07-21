#!/usr/bin/env python
import requests
import json

def test_fixed_dashboard():
    print("🔍 Testing Fixed Dashboard Generation...")
    print("=" * 60)
    
    url = "http://localhost:8000/api/generate-dashboard"
    
    # Test with different prompts
    test_prompts = [
        "Show me sales orders by status",
        "Display customer information",
        "Show me product sales over time"
    ]
    
    for i, prompt in enumerate(test_prompts):
        print(f"\n{i+1}. Testing: {prompt}")
        
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
                print(f"   ❌ Failed: {response.text[:300]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Fixed Dashboard Generation Test Complete!")
    print("\n📊 Check Superset at: http://localhost:8088")
    print("🌐 Test UI at: http://localhost:3000")

if __name__ == "__main__":
    test_fixed_dashboard() 
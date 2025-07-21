#!/usr/bin/env python
import requests
import json

def test_odoo_dashboard_fix():
    print("🔍 Testing Dashboard Generation Fix with Odoo Data...")
    print("=" * 60)
    
    # Test the dashboard generation API with simple Odoo prompts
    url = "http://localhost:8000/api/generate-dashboard"
    
    test_prompts = [
        "Show me sales orders",
        "Display customer information"
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
                print(f"   ❌ Failed: {response.text[:300]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Dashboard Generation Fix Test Complete!")

if __name__ == "__main__":
    test_odoo_dashboard_fix() 
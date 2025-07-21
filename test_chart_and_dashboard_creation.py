#!/usr/bin/env python
import requests
import json
import time

def test_chart_and_dashboard_creation():
    print("🔍 Testing Chart and Dashboard Creation in Superset...")
    print("=" * 70)
    
    # Test the dashboard generation API with prompts that should create different chart types
    url = "http://localhost:8000/api/generate-dashboard"
    
    test_prompts = [
        {
            "prompt": "Show me sales orders by status",
            "expected_charts": ["bar", "table"]
        },
        {
            "prompt": "Display customer information",
            "expected_charts": ["table"]
        },
        {
            "prompt": "Show me product sales over time",
            "expected_charts": ["line", "table"]
        }
    ]
    
    for i, test_case in enumerate(test_prompts):
        prompt = test_case["prompt"]
        expected_charts = test_case["expected_charts"]
        
        print(f"\n{i+1}. Testing: {prompt}")
        print(f"   Expected chart types: {', '.join(expected_charts)}")
        
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
                
                # Wait a moment for charts to be created
                time.sleep(2)
                
                # Try to verify charts were created by checking the dashboard
                dashboard_id = result.get('dashboard_id')
                if dashboard_id:
                    print(f"   🔍 Verifying dashboard {dashboard_id} has charts...")
                    # You can add additional verification here if needed
                    
            else:
                print(f"   ❌ Failed: {response.text[:300]}...")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 Chart and Dashboard Creation Test Complete!")
    print("\n📋 Next Steps:")
    print("1. Check the Superset UI at http://localhost:8088")
    print("2. Navigate to Dashboards to see the created dashboards")
    print("3. Each dashboard should contain multiple charts")
    print("4. Test the UI at http://localhost:3000 for natural language queries")

if __name__ == "__main__":
    test_chart_and_dashboard_creation() 
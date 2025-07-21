#!/usr/bin/env python
import requests
import json

def test_odoo_sql_generation():
    print("🔍 Testing SQL Generation for Odoo Data...")
    print("=" * 60)
    
    # Test the SQL generation API with Odoo-related prompts
    url = "http://localhost:8000/api/generate-sql"
    
    test_prompts = [
        "Show me all sales orders",
        "List all products with their prices",
        "Show me customer information",
        "Display invoice data",
        "Show me the total sales amount",
        "List products by category"
    ]
    
    for i, prompt in enumerate(test_prompts):
        print(f"\n{i+1}. Testing prompt: {prompt}")
        
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
                print(f"   Generated SQL:")
                print(f"   {result.get('sql')}")
                print(f"   Provider: {result.get('llm_provider')}")
                print(f"   Time: {result.get('execution_time_ms')}ms")
            else:
                print(f"   ❌ Failed: {response.text[:200]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Odoo SQL Generation Test Complete!")

if __name__ == "__main__":
    test_odoo_sql_generation() 
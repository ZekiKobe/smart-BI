#!/usr/bin/env python
import requests
import json

def test_llm_sql_output():
    print("🔍 Testing LLM SQL Generation for Dashboard...")
    print("=" * 60)
    
    # Test the SQL generation API with dashboard-style prompts
    url = "http://localhost:8000/api/generate-sql"
    
    test_prompts = [
        "Create a dashboard showing database information and current date",
        "Show me a dashboard with database statistics"
    ]
    
    for i, prompt in enumerate(test_prompts):
        print(f"\n{i+1}. Testing SQL generation: {prompt}")
        
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
            else:
                print(f"   ❌ Failed: {response.text[:200]}...")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 SQL Generation Test Complete!")

if __name__ == "__main__":
    test_llm_sql_output() 
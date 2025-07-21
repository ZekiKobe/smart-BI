#!/usr/bin/env python
import requests
import json

def test_sql_generation():
    print("Testing SQL generation for system table queries using Gemini...")
    
    # Test the SQL generation API
    url = "http://localhost:8000/api/generate-sql"
    
    test_prompts = [
        "Show me the current date and database version"
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
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Success!")
                print(f"   SQL: {result.get('sql')}")
                print(f"   Execution Time: {result.get('execution_time_ms')}ms")
                print(f"   LLM Provider: {result.get('llm_provider')}")
            else:
                print(f"❌ Failed: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_sql_generation() 
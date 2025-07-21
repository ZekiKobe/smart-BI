#!/usr/bin/env python
import requests
import json

def test_direct_sql():
    print("🔍 Testing Direct SQL Generation (Bypassing Database)...")
    print("=" * 60)
    
    # Test the Gemini API directly
    print("1. Testing Direct Gemini API...")
    
    # You'll need to replace this with your actual API key
    api_key = "AIzaSyCJP8SiTbn8Lg_Kvs5QxEckiiORG2A5Hsg"  # From your settings
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {"parts": [
                {"text": "You are a SQL expert. Convert this natural language query to PostgreSQL SQL. Database schema: sale_order (id, name, partner_id, date_order, amount_total, state). Query: Show me all customers. Return ONLY the SQL query, no explanations."}
            ]}
        ]
    }
    
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            sql = result["candidates"][0]["content"]["parts"][0]["text"].strip()
            print(f"   ✅ Direct API Success!")
            print(f"   Generated SQL: {sql}")
        elif response.status_code == 429:
            print(f"   ⚠️ Rate Limited (429) - This is expected")
        else:
            print(f"   ❌ Failed: {response.text[:200]}...")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n2. Testing Backend Health...")
    try:
        health_response = requests.get("http://localhost:8000/api/health/")
        if health_response.status_code == 200:
            print(f"   ✅ Backend Health: SUCCESS")
        else:
            print(f"   ❌ Backend Health: Failed")
    except Exception as e:
        print(f"   ❌ Backend Health Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Direct SQL Test Complete!")

if __name__ == "__main__":
    test_direct_sql() 
#!/usr/bin/env python
import requests
import json

def test_system_fix():
    print("🔍 Testing System Fixes...")
    print("=" * 60)
    
    # Test 1: Health Check
    print("1. Testing Health Check...")
    try:
        health_response = requests.get("http://localhost:8000/api/health/")
        if health_response.status_code == 200:
            print(f"   ✅ Health Check: SUCCESS")
            print(f"   Response: {health_response.json()}")
        else:
            print(f"   ❌ Health Check: Failed - {health_response.status_code}")
    except Exception as e:
        print(f"   ❌ Health Check Error: {e}")
    
    # Test 2: SQL Generation (with rate limit handling)
    print("\n2. Testing SQL Generation...")
    sql_url = "http://localhost:8000/api/generate-sql"
    sql_payload = {
        "prompt": "Show me sales orders",
        "user_id": 1,
        "model": "gemini"
    }
    
    try:
        sql_response = requests.post(sql_url, json=sql_payload)
        if sql_response.status_code == 200:
            sql_result = sql_response.json()
            print(f"   ✅ SQL Generation: SUCCESS")
            print(f"   SQL: {sql_result.get('sql', '')[:100]}...")
        elif sql_response.status_code == 429:
            print(f"   ⚠️ SQL Generation: Rate Limited (429)")
            print(f"   This is expected due to Gemini API limits")
        else:
            print(f"   ❌ SQL Generation: Failed - {sql_response.status_code}")
            print(f"   Error: {sql_response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ SQL Generation Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 System Fix Test Complete!")
    print("\n📊 Backend API: http://localhost:8000")
    print("🌐 Frontend UI: http://localhost:3000")
    print("📈 Superset: http://localhost:8088")

if __name__ == "__main__":
    test_system_fix() 
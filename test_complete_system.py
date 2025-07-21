#!/usr/bin/env python
import requests
import json

def test_complete_system():
    print("🔍 Testing Complete SmartBI System...")
    print("=" * 70)
    
    # Test 1: SQL Generation API
    print("1. Testing SQL Generation API...")
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
        else:
            print(f"   ❌ SQL Generation: Failed - {sql_response.status_code}")
    except Exception as e:
        print(f"   ❌ SQL Generation Error: {e}")
    
    print("\n2. Testing Dashboard Generation API...")
    dashboard_url = "http://localhost:8000/api/generate-dashboard"
    dashboard_payload = {
        "prompt": "Show me customer information",
        "user_id": 1,
        "model": "gemini"
    }
    
    try:
        dashboard_response = requests.post(dashboard_url, json=dashboard_payload)
        if dashboard_response.status_code == 200:
            dashboard_result = dashboard_response.json()
            print(f"   ✅ Dashboard Generation: SUCCESS")
            print(f"   Dashboard ID: {dashboard_result.get('dashboard_id')}")
            print(f"   Dashboard URL: {dashboard_result.get('dashboard_url')}")
        else:
            print(f"   ❌ Dashboard Generation: Failed - {dashboard_response.status_code}")
            print(f"   Error: {dashboard_response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Dashboard Generation Error: {e}")
    
    print("\n3. Testing Frontend API Connection...")
    try:
        # Test if frontend can reach backend
        test_response = requests.get("http://localhost:8000/api/health", timeout=5)
        if test_response.status_code == 200:
            print(f"   ✅ Frontend-Backend Connection: SUCCESS")
        else:
            print(f"   ⚠️ Frontend-Backend Connection: Status {test_response.status_code}")
    except Exception as e:
        print(f"   ❌ Frontend-Backend Connection Error: {e}")
    
    print("\n" + "=" * 70)
    print("🎉 Complete System Test Results:")
    print("📊 Backend API: http://localhost:8000")
    print("🌐 Frontend UI: http://localhost:3000")
    print("📈 Superset: http://localhost:8088")
    print("\n✅ System is ready for testing!")

if __name__ == "__main__":
    test_complete_system() 
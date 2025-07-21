#!/usr/bin/env python
import requests
import json

# Test the generate SQL endpoint (direct view)
def test_generate_sql_direct():
    print("Testing Generate SQL endpoint (direct view)...")
    url = "http://localhost:8000/generate-sql/"
    
    payload = {
        "prompt": "Show me total sales by month",
        "user_id": 1,
        "model": "Gemini"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test the generate SQL endpoint (API)
def test_generate_sql_api():
    print("Testing Generate SQL endpoint (API)...")
    url = "http://localhost:8000/api/generate-sql"
    
    payload = {
        "prompt": "Show me total sales by month",
        "user_id": 1,
        "model": "Gemini"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test the generate dashboard endpoint
def test_generate_dashboard():
    print("\nTesting Generate Dashboard endpoint...")
    url = "http://localhost:8000/api/generate-dashboard"
    
    payload = {
        "prompt": "Create a dashboard showing sales trends and top products",
        "user_id": 1,
        "model": "Gemini"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

# Test the old generate dashboard endpoint
def test_old_generate_dashboard():
    print("\nTesting Old Generate Dashboard endpoint...")
    url = "http://localhost:8000/api/superset/generate_dashboard/"
    
    payload = {
        "prompt": "Show me sales data",
        "llm": "gemini"
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing SmartBI endpoints...")
    
    # Test all endpoints
    sql_direct_success = test_generate_sql_direct()
    sql_api_success = test_generate_sql_api()
    dashboard_success = test_generate_dashboard()
    old_dashboard_success = test_old_generate_dashboard()
    
    print("\n" + "="*50)
    print("RESULTS:")
    print(f"Generate SQL (direct): {'✅ PASS' if sql_direct_success else '❌ FAIL'}")
    print(f"Generate SQL (API): {'✅ PASS' if sql_api_success else '❌ FAIL'}")
    print(f"Generate Dashboard (new): {'✅ PASS' if dashboard_success else '❌ FAIL'}")
    print(f"Generate Dashboard (old): {'✅ PASS' if old_dashboard_success else '❌ FAIL'}")
    print("="*50) 
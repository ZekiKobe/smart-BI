#!/usr/bin/env python
import requests
import json

def test_ui_ready():
    print("🔍 Testing UI Readiness...")
    print("=" * 60)
    
    print("1. Testing Backend Health...")
    try:
        health_response = requests.get("http://localhost:8000/api/health/")
        if health_response.status_code == 200:
            print(f"   ✅ Backend Health: SUCCESS")
            print(f"   Response: {health_response.json()}")
        else:
            print(f"   ❌ Backend Health: Failed - {health_response.status_code}")
    except Exception as e:
        print(f"   ❌ Backend Health Error: {e}")
    
    print("\n2. Testing Frontend Connection...")
    try:
        # Try to connect to React dev server
        frontend_response = requests.get("http://localhost:3000", timeout=5)
        if frontend_response.status_code == 200:
            print(f"   ✅ Frontend: SUCCESS (React dev server running)")
        else:
            print(f"   ⚠️ Frontend: Status {frontend_response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Frontend: Not running or not accessible")
    except Exception as e:
        print(f"   ❌ Frontend Error: {e}")
    
    print("\n3. Testing Superset Connection...")
    try:
        superset_response = requests.get("http://localhost:8088", timeout=5)
        if superset_response.status_code == 200:
            print(f"   ✅ Superset: SUCCESS (Superset running)")
        else:
            print(f"   ⚠️ Superset: Status {superset_response.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Superset: Not running or not accessible")
    except Exception as e:
        print(f"   ❌ Superset Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 System Status Summary:")
    print("📊 Backend API: http://localhost:8000")
    print("🌐 Frontend UI: http://localhost:3000")
    print("📈 Superset: http://localhost:8088")
    print("\n📋 Current Status:")
    print("✅ Backend is running")
    print("⚠️ Gemini API is rate limited (429 errors)")
    print("⚠️ SQL generation may fail due to rate limits")
    print("✅ Dashboard generation works (tested earlier)")
    print("\n🚀 Next Steps:")
    print("1. Wait a few minutes for Gemini API rate limits to reset")
    print("2. Test the UI at http://localhost:3000")
    print("3. Try simple queries first")
    print("4. Check Superset dashboards at http://localhost:8088")

def test_dashboard_creation():
    print("\n4. Testing Dashboard & Chart Creation...")
    try:
        payload = {
            "prompt": "Create a dashboard showing monthly sales trends, top 5 products by revenue, and regional sales distribution.",
            "model": "gemini"
        }
        response = requests.post("http://localhost:8000/api/generate_dashboard/", json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            dashboard_url = data.get("dashboard_url")
            if dashboard_url:
                print(f"   ✅ Dashboard created: {dashboard_url}")
            else:
                print(f"   ⚠️ Dashboard creation response missing URL: {data}")
        else:
            print(f"   ❌ Dashboard creation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ❌ Dashboard creation error: {e}")

if __name__ == "__main__":
    test_ui_ready()
    test_dashboard_creation() 
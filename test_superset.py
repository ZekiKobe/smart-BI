#!/usr/bin/env python
import requests
import json

def test_superset():
    base_url = "http://localhost:8088"
    
    # Step 1: Authenticate
    print("1. Authenticating with Superset...")
    auth_url = f"{base_url}/api/v1/security/login"
    auth_payload = {
        "username": "admin",
        "password": "admin",
        "provider": "db",
        "refresh": True
    }
    
    try:
        auth_response = requests.post(auth_url, json=auth_payload)
        auth_response.raise_for_status()
        token = auth_response.json()["access_token"]
        print(f"✅ Authentication successful")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Get databases
    print("\n2. Getting databases...")
    try:
        db_response = requests.get(f"{base_url}/api/v1/database/", headers=headers)
        db_response.raise_for_status()
        databases = db_response.json()
        print(f"✅ Found {len(databases.get('result', []))} databases")
        for db in databases.get('result', []):
            print(f"   - ID: {db.get('id')}, Name: {db.get('database_name')}, Engine: {db.get('engine')}")
    except Exception as e:
        print(f"❌ Failed to get databases: {e}")
        return
    
    # Step 3: Check Superset configuration
    print("\n3. Checking Superset configuration...")
    try:
        config_response = requests.get(f"{base_url}/api/v1/config/", headers=headers)
        config_response.raise_for_status()
        config = config_response.json()
        print("✅ Superset configuration accessible")
        print(f"   CSRF Protection: {config.get('result', {}).get('CSRF_ENABLED', 'Unknown')}")
    except Exception as e:
        print(f"❌ Failed to get config: {e}")

if __name__ == "__main__":
    print("Testing Superset configuration...")
    test_superset() 
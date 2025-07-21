#!/usr/bin/env python
import asyncio
import httpx
import json

async def test_dataset_creation():
    base_url = "http://localhost:8088"
    
    async with httpx.AsyncClient() as client:
        # Step 1: Authenticate
        print("1. Authenticating...")
        auth_url = f"{base_url}/api/v1/security/login"
        auth_payload = {
            "username": "admin",
            "password": "admin",
            "provider": "db",
            "refresh": True
        }
        
        auth_response = await client.post(auth_url, json=auth_payload)
        auth_response.raise_for_status()
        token = auth_response.json()["access_token"]
        print("✅ Authentication successful")
        
        # Step 2: Get CSRF token
        print("\n2. Getting CSRF token...")
        csrf_url = f"{base_url}/api/v1/security/csrf_token/"
        headers = {"Authorization": f"Bearer {token}"}
        csrf_response = await client.get(csrf_url, headers=headers)
        csrf_response.raise_for_status()
        csrf_token = csrf_response.json()["result"]
        print("✅ CSRF token obtained")
        
        # Step 3: Test dataset creation with different payloads
        print("\n3. Testing dataset creation...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        }
        
        # Test with database ID 3 (PostgreSQL)
        dataset_payload = {
            "database": 3,
            "sql": "SELECT 1 as test",
            "table_name": "test_dataset",
            "schema": "public",
            "template_params": "{}"
        }
        
        try:
            dataset_response = await client.post(f"{base_url}/api/v1/dataset/", headers=headers, json=dataset_payload)
            print(f"Dataset creation status: {dataset_response.status_code}")
            if dataset_response.status_code == 200:
                print("✅ Dataset creation successful")
                dataset_id = dataset_response.json()["id"]
                print(f"   Dataset ID: {dataset_id}")
            else:
                print(f"❌ Dataset creation failed: {dataset_response.text}")
        except Exception as e:
            print(f"❌ Dataset creation error: {e}")

if __name__ == "__main__":
    print("Testing Superset dataset creation...")
    asyncio.run(test_dataset_creation()) 
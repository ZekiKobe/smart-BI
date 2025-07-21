#!/usr/bin/env python
import asyncio
import httpx
import json

async def test_sql_queries():
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
        
        # Step 3: Test different SQL queries
        print("\n3. Testing SQL queries...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        }
        
        # Test queries
        test_queries = [
            "SELECT 1 as test",
            "SELECT current_date as today",
            "SELECT version() as db_version",
            "SELECT current_user as user",
            "SELECT current_database() as database",
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' LIMIT 5",
            "SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' LIMIT 10"
        ]
        
        for i, sql in enumerate(test_queries):
            print(f"\n   Testing query {i+1}: {sql}")
            
            dataset_payload = {
                "database": 3,
                "sql": sql,
                "table_name": f"test_query_{i+1}",
                "schema": "public",
                "template_params": "{}"
            }
            
            try:
                dataset_response = await client.post(f"{base_url}/api/v1/dataset/", headers=headers, json=dataset_payload)
                print(f"   Status: {dataset_response.status_code}")
                if dataset_response.status_code == 201:
                    dataset_id = dataset_response.json()["id"]
                    print(f"   ✅ Success - Dataset ID: {dataset_id}")
                else:
                    print(f"   ❌ Failed: {dataset_response.text}")
            except Exception as e:
                print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("Testing SQL queries in PostgreSQL...")
    asyncio.run(test_sql_queries()) 
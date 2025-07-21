#!/usr/bin/env python
import asyncio
import httpx
import json

async def test_manual_sql():
    print("🔍 Testing Manual SQL Query in Superset...")
    
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
        
        # Step 3: Test the SQL query that LLM generated
        print("\n3. Testing LLM-generated SQL...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        }
        
        # Use the SQL that the LLM generated
        sql = """
        SELECT
          pg_stat_database.datname,
          pg_stat_database.numbackends,
          pg_stat_database.xact_commit,
          pg_stat_database.xact_rollback
        FROM pg_stat_database;
        """
        
        dataset_payload = {
            "database": 3,
            "sql": sql,
            "table_name": "llm_generated_stats",
            "schema": "public",
            "template_params": "{}"
        }
        
        try:
            dataset_response = await client.post(f"{base_url}/api/v1/dataset/", headers=headers, json=dataset_payload)
            print(f"Dataset creation status: {dataset_response.status_code}")
            if dataset_response.status_code == 201:
                dataset_id = dataset_response.json()["id"]
                print(f"✅ Dataset created successfully with ID: {dataset_id}")
                print(f"✅ LLM-generated SQL works in Superset!")
            else:
                print(f"❌ Dataset creation failed: {dataset_response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing LLM-generated SQL in Superset...")
    asyncio.run(test_manual_sql()) 
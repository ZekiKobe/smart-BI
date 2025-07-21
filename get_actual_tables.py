#!/usr/bin/env python
import asyncio
import httpx
import json

async def get_actual_tables():
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
        
        # Step 3: Create dataset with table names
        print("\n3. Getting table names...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        }
        
        # Get all tables
        sql = """
        SELECT 
            t.table_name,
            COUNT(c.column_name) as column_count
        FROM information_schema.tables t
        LEFT JOIN information_schema.columns c 
            ON t.table_name = c.table_name 
            AND t.table_schema = c.table_schema
        WHERE t.table_schema = 'public' 
        AND t.table_type = 'BASE TABLE'
        GROUP BY t.table_name
        ORDER BY t.table_name
        """
        
        dataset_payload = {
            "database": 3,
            "sql": sql,
            "table_name": "actual_tables",
            "schema": "public",
            "template_params": "{}"
        }
        
        try:
            dataset_response = await client.post(f"{base_url}/api/v1/dataset/", headers=headers, json=dataset_payload)
            print(f"Dataset creation status: {dataset_response.status_code}")
            if dataset_response.status_code == 201:
                dataset_id = dataset_response.json()["id"]
                print(f"✅ Dataset created with ID: {dataset_id}")
                
                # Step 4: Get the data from the dataset
                print("\n4. Getting table data...")
                data_url = f"{base_url}/api/v1/dataset/{dataset_id}/data/"
                data_response = await client.get(data_url, headers=headers)
                
                if data_response.status_code == 200:
                    data = data_response.json()
                    tables = data.get('result', [])
                    
                    print(f"\nFound {len(tables)} tables in the database:")
                    for table in tables:
                        table_name = table.get('table_name')
                        column_count = table.get('column_count')
                        print(f"  - {table_name} ({column_count} columns)")
                        
                        # Get columns for this table
                        columns_sql = f"""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns 
                        WHERE table_name = '{table_name}' 
                        AND table_schema = 'public'
                        ORDER BY ordinal_position
                        """
                        
                        columns_payload = {
                            "database": 3,
                            "sql": columns_sql,
                            "table_name": f"columns_{table_name}",
                            "schema": "public",
                            "template_params": "{}"
                        }
                        
                        try:
                            columns_response = await client.post(f"{base_url}/api/v1/dataset/", headers=headers, json=columns_payload)
                            if columns_response.status_code == 201:
                                columns_dataset_id = columns_response.json()["id"]
                                columns_data_url = f"{base_url}/api/v1/dataset/{columns_dataset_id}/data/"
                                columns_data_response = await client.get(columns_data_url, headers=headers)
                                
                                if columns_data_response.status_code == 200:
                                    columns_data = columns_data_response.json()
                                    columns = columns_data.get('result', [])
                                    
                                    for col in columns:
                                        col_name = col.get('column_name')
                                        col_type = col.get('data_type')
                                        nullable = col.get('is_nullable')
                                        print(f"    - {col_name}: {col_type} {'(nullable)' if nullable == 'YES' else '(not null)'}")
                        except Exception as e:
                            print(f"    ❌ Error getting columns: {e}")
                else:
                    print(f"❌ Could not get data: {data_response.status_code}")
            else:
                print(f"❌ Dataset creation failed: {dataset_response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Getting actual tables from PostgreSQL...")
    asyncio.run(get_actual_tables()) 
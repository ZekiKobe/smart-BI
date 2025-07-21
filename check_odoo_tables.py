#!/usr/bin/env python
import asyncio
import httpx
import json

async def check_odoo_tables():
    print("🔍 Checking Odoo tables in PostgreSQL database...")
    
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
        
        # Step 3: Get Odoo tables
        print("\n3. Getting Odoo tables...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        }
        
        # SQL to get Odoo tables
        sql = """
        SELECT 
            table_name,
            COUNT(column_name) as column_count
        FROM information_schema.tables t
        LEFT JOIN information_schema.columns c 
            ON t.table_name = c.table_name 
            AND t.table_schema = c.table_schema
        WHERE t.table_schema = 'public' 
        AND t.table_type = 'BASE TABLE'
        AND (table_name LIKE '%sale%' OR table_name LIKE '%product%' OR table_name LIKE '%partner%' OR table_name LIKE '%invoice%' OR table_name LIKE '%order%')
        GROUP BY table_name
        ORDER BY table_name
        LIMIT 20
        """
        
        dataset_payload = {
            "database": 3,
            "sql": sql,
            "table_name": "odoo_tables",
            "schema": "public",
            "template_params": "{}"
        }
        
        try:
            dataset_response = await client.post(f"{base_url}/api/v1/dataset/", headers=headers, json=dataset_payload)
            print(f"Dataset creation status: {dataset_response.status_code}")
            if dataset_response.status_code == 201:
                dataset_id = dataset_response.json()["id"]
                print(f"✅ Dataset created with ID: {dataset_id}")
                
                # Get the data
                data_url = f"{base_url}/api/v1/dataset/{dataset_id}/data/"
                data_response = await client.get(data_url, headers=headers)
                
                if data_response.status_code == 200:
                    data = data_response.json()
                    tables = data.get('result', [])
                    
                    print(f"\nFound {len(tables)} Odoo-related tables:")
                    for table in tables:
                        table_name = table.get('table_name')
                        column_count = table.get('column_count')
                        print(f"  - {table_name} ({column_count} columns)")
                        
                        # Get sample columns for this table
                        columns_sql = f"""
                        SELECT column_name, data_type
                        FROM information_schema.columns 
                        WHERE table_name = '{table_name}' 
                        AND table_schema = 'public'
                        ORDER BY ordinal_position
                        LIMIT 10
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
                                    
                                    print(f"    Columns: {', '.join([col.get('column_name') for col in columns[:5]])}")
                                    if len(columns) > 5:
                                        print(f"    ... and {len(columns) - 5} more columns")
                        except Exception as e:
                            print(f"    ❌ Error getting columns: {e}")
                else:
                    print(f"❌ Could not get data: {data_response.status_code}")
            else:
                print(f"❌ Dataset creation failed: {dataset_response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Checking Odoo tables in database...")
    asyncio.run(check_odoo_tables()) 
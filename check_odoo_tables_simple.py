#!/usr/bin/env python
import asyncio
import httpx
import json

async def check_odoo_tables_simple():
    print("🔍 Checking Odoo tables (simple approach)...")
    
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
        
        # Step 3: Get all tables first
        print("\n3. Getting all tables...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        }
        
        # Simple SQL to get all tables
        sql = """
        SELECT table_name
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_type = 'BASE TABLE'
        ORDER BY table_name
        """
        
        dataset_payload = {
            "database": 3,
            "sql": sql,
            "table_name": "all_tables",
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
                    
                    print(f"\nFound {len(tables)} total tables in database")
                    
                    # Filter for Odoo-related tables
                    odoo_tables = []
                    for table in tables:
                        table_name = table.get('table_name', '').lower()
                        if any(keyword in table_name for keyword in ['sale', 'product', 'partner', 'invoice', 'order', 'res_', 'account_']):
                            odoo_tables.append(table.get('table_name'))
                    
                    print(f"\nFound {len(odoo_tables)} Odoo-related tables:")
                    for table_name in odoo_tables[:15]:  # Show first 15
                        print(f"  - {table_name}")
                    
                    if len(odoo_tables) > 15:
                        print(f"  ... and {len(odoo_tables) - 15} more tables")
                    
                    # Get details for a few key tables
                    key_tables = ['sale_order', 'product_template', 'res_partner', 'account_invoice']
                    for key_table in key_tables:
                        if key_table in odoo_tables:
                            print(f"\n📋 Details for {key_table}:")
                            
                            # Get columns for this table
                            columns_sql = f"""
                            SELECT column_name, data_type
                            FROM information_schema.columns 
                            WHERE table_name = '{key_table}' 
                            AND table_schema = 'public'
                            ORDER BY ordinal_position
                            LIMIT 10
                            """
                            
                            columns_payload = {
                                "database": 3,
                                "sql": columns_sql,
                                "table_name": f"columns_{key_table}",
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
                                        
                                        for col in columns[:5]:
                                            col_name = col.get('column_name')
                                            col_type = col.get('data_type')
                                            print(f"    - {col_name}: {col_type}")
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
    print("Checking Odoo tables (simple approach)...")
    asyncio.run(check_odoo_tables_simple()) 
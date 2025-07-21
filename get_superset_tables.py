#!/usr/bin/env python
import requests
import json

def get_superset_tables():
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
        print("✅ Authentication successful")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return None
    
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
            
            # Step 3: Get tables for this database
            db_id = db.get('id')
            print(f"\n3. Getting tables for database {db_id}...")
            
            try:
                tables_response = requests.get(f"{base_url}/api/v1/database/{db_id}/tables/", headers=headers)
                if tables_response.status_code == 200:
                    tables = tables_response.json()
                    print(f"✅ Found {len(tables.get('result', []))} tables")
                    
                    schema = {"tables": {}, "relationships": []}
                    
                    for table in tables.get('result', []):
                        table_name = table.get('table_name')
                        schema_name = table.get('schema')
                        full_name = f"{schema_name}.{table_name}" if schema_name else table_name
                        
                        print(f"\n   Table: {full_name}")
                        
                        # Get columns for this table
                        try:
                            columns_response = requests.get(f"{base_url}/api/v1/database/{db_id}/table/{schema_name}/{table_name}/", headers=headers)
                            if columns_response.status_code == 200:
                                table_info = columns_response.json()
                                columns = table_info.get('result', {}).get('columns', [])
                                
                                schema["tables"][table_name] = {
                                    "columns": {},
                                    "description": f"Table containing {table_name} data"
                                }
                                
                                print(f"     Columns:")
                                for col in columns:
                                    col_name = col.get('column_name')
                                    col_type = col.get('type')
                                    schema["tables"][table_name]["columns"][col_name] = {
                                        "type": col_type,
                                        "nullable": col.get('nullable', True)
                                    }
                                    print(f"       - {col_name}: {col_type}")
                            else:
                                print(f"     ❌ Could not get columns: {columns_response.status_code}")
                        except Exception as e:
                            print(f"     ❌ Error getting columns: {e}")
                    
                    # Save the schema
                    with open(f'real_schema_db_{db_id}.json', 'w') as f:
                        json.dump(schema, f, indent=2)
                    
                    print(f"\n✅ Schema saved to real_schema_db_{db_id}.json")
                    print(f"Found {len(schema['tables'])} tables")
                    
                    return schema
                else:
                    print(f"❌ Could not get tables: {tables_response.status_code}")
            except Exception as e:
                print(f"❌ Error getting tables: {e}")
                
    except Exception as e:
        print(f"❌ Failed to get databases: {e}")
        return None

if __name__ == "__main__":
    print("Getting database schema through Superset...")
    schema = get_superset_tables()
    if schema:
        print("\nSchema structure:")
        print(json.dumps(schema, indent=2)) 
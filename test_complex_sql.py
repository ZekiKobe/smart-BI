#!/usr/bin/env python
import asyncio
import httpx
import json

async def test_complex_sql():
    print("🔍 Testing Complex LLM-Generated SQL...")
    
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
        
        # Step 3: Test the complex SQL query
        print("\n3. Testing complex SQL...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        }
        
        # Use the complex SQL that the LLM generated
        sql = """
        SELECT
          current_database() AS database_name,
          (SELECT COUNT(*) FROM information_schema.tables) AS total_tables,
          (SELECT COUNT(*) FROM information_schema.columns) AS total_columns,
          pg_stat_database.numbackends AS current_connections,
          pg_stat_database.xact_commit AS total_commits,
          pg_stat_database.xact_rollback AS total_rollbacks
        FROM pg_stat_database
        WHERE datname = current_database();
        """
        
        dataset_payload = {
            "database": 3,
            "sql": sql,
            "table_name": "complex_stats",
            "schema": "public",
            "template_params": "{}"
        }
        
        try:
            dataset_response = await client.post(f"{base_url}/api/v1/dataset/", headers=headers, json=dataset_payload)
            print(f"Dataset creation status: {dataset_response.status_code}")
            if dataset_response.status_code == 201:
                dataset_id = dataset_response.json()["id"]
                print(f"✅ Complex SQL dataset created successfully with ID: {dataset_id}")
                
                # Step 4: Create chart
                print("\n4. Creating chart...")
                chart_payload = {
                    "datasource_id": dataset_id,
                    "datasource_type": "table",
                    "viz_type": "table",
                    "slice_name": "Database Statistics",
                    "params": "{}",
                }
                
                chart_response = await client.post(f"{base_url}/api/v1/chart/", headers=headers, json=chart_payload)
                print(f"Chart creation status: {chart_response.status_code}")
                if chart_response.status_code == 201:
                    chart_id = chart_response.json()["id"]
                    print(f"✅ Chart created successfully with ID: {chart_id}")
                    
                    # Step 5: Create dashboard
                    print("\n5. Creating dashboard...")
                    dashboard_payload = {
                        "dashboard_title": "Database Statistics Dashboard",
                        "slug": "database-stats-dashboard",
                        "position_json": {
                            str(chart_id): {
                                "type": "CHART",
                                "id": chart_id,
                                "children": [],
                                "meta": {"chartId": chart_id},
                                "parents": [],
                                "position": {"row": 0, "col": 0}
                            }
                        }
                    }
                    
                    dashboard_response = await client.post(f"{base_url}/api/v1/dashboard/", headers=headers, json=dashboard_payload)
                    print(f"Dashboard creation status: {dashboard_response.status_code}")
                    if dashboard_response.status_code == 201:
                        dashboard_result = dashboard_response.json()
                        dashboard_id = dashboard_result.get("id")
                        dashboard_url = f"{base_url}/superset/dashboard/{dashboard_id}/"
                        print(f"✅ Dashboard created successfully!")
                        print(f"   Dashboard ID: {dashboard_id}")
                        print(f"   Dashboard URL: {dashboard_url}")
                    else:
                        print(f"❌ Dashboard creation failed: {dashboard_response.text}")
                else:
                    print(f"❌ Chart creation failed: {chart_response.text}")
            else:
                print(f"❌ Dataset creation failed: {dataset_response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("Testing complex SQL in complete pipeline...")
    asyncio.run(test_complex_sql()) 
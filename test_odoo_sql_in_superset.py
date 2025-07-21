#!/usr/bin/env python
import asyncio
import httpx
import json

async def test_odoo_sql_in_superset():
    print("🔍 Testing Odoo SQL Queries in Superset...")
    
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
        
        # Step 3: Test Odoo SQL queries
        print("\n3. Testing Odoo SQL queries...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token
        }
        
        # Test queries for Odoo data
        test_queries = [
            {
                "name": "Sales Orders",
                "sql": "SELECT * FROM sale_order LIMIT 10"
            },
            {
                "name": "Products with Prices",
                "sql": "SELECT pt.name, pt.list_price, pt.standard_price FROM product_template AS pt LIMIT 10"
            },
            {
                "name": "Customers",
                "sql": "SELECT * FROM res_partner LIMIT 10"
            },
            {
                "name": "Total Sales Amount",
                "sql": "SELECT SUM(amount_total) as total_sales FROM sale_order"
            },
            {
                "name": "Products by Category",
                "sql": "SELECT pc.name AS category_name, pt.name AS product_name FROM product_category AS pc JOIN product_template AS pt ON pc.id = pt.categ_id ORDER BY pc.name, pt.name LIMIT 10"
            }
        ]
        
        for i, query_info in enumerate(test_queries):
            print(f"\n   Testing {i+1}: {query_info['name']}")
            
            dataset_payload = {
                "database": 3,
                "sql": query_info["sql"],
                "table_name": f"odoo_test_{i+1}",
                "schema": "public",
                "template_params": "{}"
            }
            
            try:
                dataset_response = await client.post(f"{base_url}/api/v1/dataset/", headers=headers, json=dataset_payload)
                print(f"   Dataset creation status: {dataset_response.status_code}")
                if dataset_response.status_code == 201:
                    dataset_id = dataset_response.json()["id"]
                    print(f"   ✅ Success - Dataset ID: {dataset_id}")
                    
                    # Try to get data to verify it works
                    try:
                        data_url = f"{base_url}/api/v1/dataset/{dataset_id}/data/"
                        data_response = await client.get(data_url, headers=headers)
                        if data_response.status_code == 200:
                            data = data_response.json()
                            rows = data.get('result', [])
                            print(f"   📊 Data: {len(rows)} rows returned")
                        else:
                            print(f"   ⚠️  Could not get data: {data_response.status_code}")
                    except Exception as e:
                        print(f"   ⚠️  Data retrieval error: {e}")
                else:
                    print(f"   ❌ Failed: {dataset_response.text[:100]}...")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 Odoo SQL Testing Complete!")

if __name__ == "__main__":
    print("Testing Odoo SQL queries in Superset...")
    asyncio.run(test_odoo_sql_in_superset()) 
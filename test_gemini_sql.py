#!/usr/bin/env python
import requests
import json

def test_gemini_sql():
    api_key = "AIzaSyC75ct3TNPpdaVC3oo41QEUSfxFUW2OTFs"
    model = "gemini-1.5-flash"
    
    # Test with the exact format used by the application
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    # Test with the simple format first
    payload1 = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Convert this prompt to SQL: Show me total sales by month"
                    }
                ]
            }
        ]
    }
    
    print("Testing simple format...")
    try:
        response = requests.post(url, json=payload1, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Response: {result}")
            return True
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test with the full format used by llm_integration
    schema_context = {
        "tables": {
            "sales": {
                "columns": {
                    "id": "integer",
                    "product_id": "integer (foreign key to products.id)",
                    "amount": "decimal",
                    "sale_date": "date",
                    "region": "varchar"
                },
                "description": "Contains all sales transactions"
            },
            "products": {
                "columns": {
                    "id": "integer",
                    "name": "varchar",
                    "category": "varchar",
                    "price": "decimal"
                },
                "description": "Product catalog information"
            }
        },
        "relationships": [
            "sales.product_id references products.id"
        ]
    }
    
    prompt = f"You are a SQL expert. Convert this natural language query to PostgreSQL SQL. Database schema: {json.dumps(schema_context)} Query: Show me total sales by month Return ONLY the SQL query, no explanations."
    
    payload2 = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    print("\nTesting full format...")
    try:
        response = requests.post(url, json=payload2, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Response: {result}")
            return True
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    return False

if __name__ == "__main__":
    print("Testing Gemini SQL generation...")
    success = test_gemini_sql()
    if success:
        print("\n✅ Gemini SQL generation is working!")
    else:
        print("\n❌ Gemini SQL generation is not working.") 
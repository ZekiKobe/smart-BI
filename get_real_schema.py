#!/usr/bin/env python
import psycopg2
import json
from django.conf import settings
import os
import sys

# Add the smarterp_bi directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'smarterp_bi'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarterp_bi.settings')
import django
django.setup()

def get_real_schema():
    """Get the actual schema from PostgreSQL database"""
    try:
        # Connect to PostgreSQL using the same credentials as Superset
        conn = psycopg2.connect(
            host="host.docker.internal",
            port=5432,
            database="odooistic",
            user="postgres",
            password="postgres"  # You might need to adjust this
        )
        
        schema = {"tables": {}, "relationships": []}
        
        with conn.cursor() as cursor:
            # Get all tables in the public schema
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            print(f"Found {len(tables)} tables in database:")
            
            for table in tables:
                print(f"\nTable: {table}")
                
                # Get columns for this table
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = '{table}' 
                    AND table_schema = 'public'
                    ORDER BY ordinal_position
                """)
                columns = cursor.fetchall()
                
                schema["tables"][table] = {
                    "columns": {},
                    "description": f"Table containing {table} data"
                }
                
                print(f"  Columns:")
                for col_name, data_type, is_nullable, default_val in columns:
                    schema["tables"][table]["columns"][col_name] = {
                        "type": data_type,
                        "nullable": is_nullable == "YES",
                        "default": default_val
                    }
                    print(f"    - {col_name}: {data_type} {'(nullable)' if is_nullable == 'YES' else '(not null)'}")
                
                # Get foreign keys for this table
                cursor.execute(f"""
                    SELECT
                        kcu.column_name,
                        ccu.table_name AS foreign_table,
                        ccu.column_name AS foreign_column
                    FROM information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                        ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY' 
                    AND tc.table_name = '{table}'
                """)
                foreign_keys = cursor.fetchall()
                
                for fk in foreign_keys:
                    relationship = f"{table}.{fk[0]} references {fk[1]}.{fk[2]}"
                    schema["relationships"].append(relationship)
                    print(f"    Foreign Key: {relationship}")
        
        conn.close()
        
        # Save the schema to a file
        with open('real_schema.json', 'w') as f:
            json.dump(schema, f, indent=2)
        
        print(f"\n✅ Schema saved to real_schema.json")
        print(f"Found {len(schema['tables'])} tables and {len(schema['relationships'])} relationships")
        
        return schema
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        print("Make sure PostgreSQL is running and accessible")
        return None

if __name__ == "__main__":
    print("Reading actual database schema...")
    schema = get_real_schema()
    if schema:
        print("\nSchema structure:")
        print(json.dumps(schema, indent=2)) 
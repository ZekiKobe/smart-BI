# llm_integration/services.py
import httpx
from django.conf import settings
from .models import LLMProvider
import json

class LLMService:
    def __init__(self, provider):
        self.provider = provider
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def generate_sql(self, prompt, schema_context):
        # Google Gemini expects a different payload and endpoint
        if self.provider.name.lower() == "gemini":
            endpoint = f"{self.provider.base_url}:generateContent?key={self.provider.api_key}"
            payload = {
                "contents": [
                    {"parts": [
                        {"text": f"You are a SQL expert. Convert this natural language query to PostgreSQL SQL. Database schema: {schema_context} Query: {prompt} Return ONLY the SQL query, no explanations."}
                    ]}
                ]
            }
            headers = {
                "Content-Type": "application/json"
            }
        elif self.provider.name.lower() == "deepseek":
            # DeepSeek uses OpenAI-compatible API format
            endpoint = self.provider.base_url
            payload = {
                "model": "deepseek-coder",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a SQL expert. Convert natural language queries to PostgreSQL SQL. Return ONLY the SQL query, no explanations."
                    },
                    {
                        "role": "user",
                        "content": f"Database schema: {schema_context}\nQuery: {prompt}"
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            headers = {
                "Authorization": f"Bearer {self.provider.api_key}",
                "Content-Type": "application/json"
            }
        else:
            endpoint = f"{self.provider.base_url}/generate"
            payload = {
                "prompt": f"""
                You are a SQL expert. Convert this natural language query to PostgreSQL SQL.\nDatabase schema: {schema_context}\nQuery: {prompt}\nReturn ONLY the SQL query, no explanations.
                """,
                "temperature": 0.3,
                "max_tokens": 1000
            }
            headers = {
                "Authorization": f"Bearer {self.provider.api_key}",
                "Content-Type": "application/json"
            }

        response = await self.client.post(
            endpoint,
            headers=headers,
            json=payload
        )

        response.raise_for_status()
        # Parse response based on provider
        if self.provider.name.lower() == "gemini":
            return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        elif self.provider.name.lower() == "deepseek":
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return response.json().get("text", "").strip()
    
    async def generate_dashboard_spec(self, prompt, schema_context):
        # Prompt the LLM to return a list of chart specs (type, title, SQL, metrics, groupby, all_columns)
        llm_prompt = (
            f"You are a BI assistant. Given the following user request:\n"
            f"\"{prompt}\"\n"
            f"and this database schema:\n{schema_context}\n"
            "Break the request into individual charts. For each chart, return:\n"
            "- type (one of: bar, line, pie, table)\n"
            "- title\n"
            "- sql (PostgreSQL, valid for Superset dataset)\n"
            "- metrics (for bar/line/pie, e.g., ['sum__amount_total'])\n"
            "- groupby (for bar/line/pie, e.g., ['region'])\n"
            "- all_columns (for table, e.g., ['product_id', 'revenue'])\n"
            "Return the result as a JSON array, e.g.:\n"
            "[{\"type\": \"bar\", \"title\": \"Total Sales by Region\", \"sql\": \"...\", \"metrics\": [\"sum__amount_total\"], \"groupby\": [\"region\"]}, ...]\n"
            "Do not include explanations, just the JSON."
        )
        endpoint = f"{self.provider.base_url}:generateContent?key={self.provider.api_key}"
        payload = {
            "contents": [{"parts": [{"text": llm_prompt}]}]
        }
        headers = {"Content-Type": "application/json"}
        response = await self.client.post(endpoint, headers=headers, json=payload)
        response.raise_for_status()
        import json
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()
        # Remove code block markers if present
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        chart_specs = json.loads(text)
        print(f"[DEBUG] LLM chart specs: {chart_specs}")
        return chart_specs
    
    async def explain_data(self, data, question):
        # TODO: Replace this mock with actual LLM call
        # For now, return a sample explanation and insights
        return {
            "answer": "Sales dropped last quarter due to a decrease in demand in the North region.",
            "insights": [
                "North region sales decreased by 20% compared to previous quarter.",
                "Top 3 products saw a decline in sales volume.",
                "Overall revenue was impacted by seasonal trends."
            ]
        }

    @classmethod
    async def create(cls, provider_name=None):
        if provider_name:
            # Case-insensitive lookup
            provider = await LLMProvider.objects.filter(name__iexact=provider_name).afirst()
            if not provider:
                raise ValueError(f"LLMProvider matching query does not exist: {provider_name}")
        else:
            provider = await LLMProvider.objects.filter(is_active=True).afirst()
        if not provider:
            raise ValueError("No active LLMProvider found. Please configure at least one provider in the admin panel.")
        return cls(provider)

def get_schema_context():
    """
    Returns the database schema context for LLM to generate SQL queries
    """
    # Option 1: Static schema definition including Odoo tables
    schema = {
        "tables": {
            # Odoo Sales Tables
            "sale_order": {
                "columns": {
                    "id": "integer",
                    "name": "varchar",
                    "partner_id": "integer",
                    "date_order": "timestamp",
                    "amount_total": "numeric",
                    "state": "varchar",
                    "create_date": "timestamp"
                },
                "description": "Odoo sales orders table"
            },
            "sale_order_line": {
                "columns": {
                    "id": "integer",
                    "order_id": "integer",
                    "product_id": "integer",
                    "name": "varchar",
                    "product_uom_qty": "numeric",
                    "price_unit": "numeric",
                    "price_subtotal": "numeric"
                },
                "description": "Odoo sales order lines table"
            },
            # Odoo Product Tables
            "product_template": {
                "columns": {
                    "id": "integer",
                    "name": "varchar",
                    "list_price": "numeric",
                    "standard_price": "numeric",
                    "categ_id": "integer",
                    "type": "varchar",
                    "create_date": "timestamp"
                },
                "description": "Odoo product templates table"
            },
            "product_category": {
                "columns": {
                    "id": "integer",
                    "name": "varchar",
                    "parent_id": "integer",
                    "complete_name": "varchar"
                },
                "description": "Odoo product categories table"
            },
            # Odoo Partner Tables
            "res_partner": {
                "columns": {
                    "id": "integer",
                    "name": "varchar",
                    "email": "varchar",
                    "phone": "varchar",
                    "is_company": "boolean",
                    "customer_rank": "integer",
                    "supplier_rank": "integer",
                    "create_date": "timestamp"
                },
                "description": "Odoo partners/customers table"
            },
            # Odoo Invoice Tables
            "account_move": {
                "columns": {
                    "id": "integer",
                    "name": "varchar",
                    "partner_id": "integer",
                    "invoice_date": "date",
                    "amount_total": "numeric",
                    "state": "varchar",
                    "move_type": "varchar",
                    "create_date": "timestamp"
                },
                "description": "Odoo account moves/invoices table"
            },
            # System tables (for reference)
            "information_schema.tables": {
                "columns": {
                    "table_name": "varchar",
                    "table_schema": "varchar",
                    "table_type": "varchar"
                },
                "description": "System table containing information about all tables in the database"
            },
            "pg_stat_database": {
                "columns": {
                    "datname": "varchar",
                    "numbackends": "integer",
                    "xact_commit": "bigint",
                    "xact_rollback": "bigint"
                },
                "description": "System view containing database statistics"
            }
        },
        "relationships": [
            "sale_order.partner_id references res_partner.id",
            "sale_order_line.order_id references sale_order.id",
            "sale_order_line.product_id references product_template.id",
            "product_template.categ_id references product_category.id",
            "account_move.partner_id references res_partner.id"
        ],
        "available_functions": [
            "current_date() - returns current date",
            "current_timestamp() - returns current timestamp",
            "version() - returns PostgreSQL version",
            "current_user - returns current user",
            "current_database() - returns current database name",
            "SUM() - sum of values",
            "COUNT() - count of records",
            "AVG() - average of values"
        ]
    }
    
    # Option 2: Dynamic schema from database (advanced)
    if hasattr(settings, 'DYNAMIC_SCHEMA') and settings.DYNAMIC_SCHEMA:
        from django.db import connection
        schema = generate_dynamic_schema(connection)
    
    return json.dumps(schema)

def generate_dynamic_schema(connection):
    """Generate schema by introspecting the database"""
    schema = {"tables": {}, "relationships": []}
    with connection.cursor() as cursor:
        # Get tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            # Get columns
            cursor.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{table}'
            """)
            schema["tables"][table] = {
                "columns": {row[0]: row[1] for row in cursor.fetchall()},
                "description": f"Table containing {table} data"
            }
            
            # Get foreign keys (relationships)
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
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = '{table}'
            """)
            for row in cursor.fetchall():
                schema["relationships"].append(
                    f"{table}.{row[0]} references {row[1]}.{row[2]}"
                )
    
    return schema
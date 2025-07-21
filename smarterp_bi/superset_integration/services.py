# superset_integration/services.py
import httpx
import json
from django.conf import settings

class SupersetService:
    def __init__(self):
        self.base_url = settings.SUPERSET_BASE_URL
        self.username = settings.SUPERSET_USERNAME
        self.password = settings.SUPERSET_PASSWORD
        self.client = httpx.AsyncClient()
        self.access_token = None
    
    async def authenticate(self):
        auth_url = f"{self.base_url}/api/v1/security/login"
        payload = {
            "username": self.username,
            "password": self.password,
            "provider": "db",
            "refresh": True
        }
        
        response = await self.client.post(auth_url, json=payload)
        response.raise_for_status()
        self.access_token = response.json().get("access_token")
        
        # Get CSRF token
        csrf_url = f"{self.base_url}/api/v1/security/csrf_token/"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        csrf_response = await self.client.get(csrf_url, headers=headers)
        csrf_response.raise_for_status()
        self.csrf_token = csrf_response.json().get("result")
    
    async def create_dataset(self, sql, table_name, database_id):
        if not self.access_token:
            await self.authenticate()
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        if hasattr(self, 'csrf_token') and self.csrf_token:
            headers["X-CSRFToken"] = self.csrf_token
        dataset_url = f"{self.base_url}/api/v1/dataset/"
        payload = {
            "database": database_id,
            "sql": sql,
            "table_name": table_name,
            "schema": "public",
            "template_params": "{}"
        }
        response = await self.client.post(dataset_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["id"]

    async def create_chart(self, dataset_id, chart_type, title, chart_spec=None):
        if not self.access_token:
            await self.authenticate()
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        if hasattr(self, 'csrf_token') and self.csrf_token:
            headers["X-CSRFToken"] = self.csrf_token
        chart_url = f"{self.base_url}/api/v1/chart/"
        # Use chart_spec fields if provided
        metrics = chart_spec.get("metrics") if chart_spec else []
        groupby = chart_spec.get("groupby") if chart_spec else []
        columns = chart_spec.get("columns") if chart_spec else []
        all_columns = chart_spec.get("all_columns") if chart_spec else []
        # Create appropriate chart parameters based on chart type
        if chart_type == "table":
            params = {
                "all_columns": all_columns or columns or [],
                "order_by_cols": [],
                "row_limit": 1000
            }
        elif chart_type in ("bar", "line", "pie"):
            params = {
                "metrics": metrics or [],
                "groupby": groupby or [],
                "adhoc_filters": [],
                "row_limit": 1000
            }
        else:
            params = {}
        payload = {
            "datasource_id": dataset_id,
            "datasource_type": "table",
            "viz_type": chart_type,
            "slice_name": title,
            "params": json.dumps(params),
        }
        try:
            response = await self.client.post(chart_url, headers=headers, json=payload)
            response.raise_for_status()
            chart_id = response.json()["id"]
            print(f"✅ Chart created successfully: {title} (ID: {chart_id})")
            return chart_id
        except Exception as e:
            print(f"❌ Chart creation failed for {title}: {e}")
            # Fallback to table chart if other types fail
            if chart_type != "table":
                return await self.create_chart(dataset_id, "table", title, chart_spec)
            raise e

    async def create_dashboard(self, title, chart_specs, database_id=3):
        if not self.access_token:
            await self.authenticate()
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        if hasattr(self, 'csrf_token') and self.csrf_token:
            headers["X-CSRFToken"] = self.csrf_token
        chart_ids = []
        for i, chart in enumerate(chart_specs):
            import time
            timestamp = int(time.time())
            table_name = f"auto_dataset_{i}_{timestamp}_{title.lower().replace(' ', '_').replace('-', '_')[:20]}"
            print(f"[DEBUG] Creating dataset with SQL: {chart['sql']}")
            dataset_id = await self.create_dataset(chart["sql"], table_name, database_id)
            chart_id = await self.create_chart(dataset_id, chart["type"], chart["title"], chart)
            chart_ids.append(chart_id)
        dashboard_url = f"{self.base_url}/api/v1/dashboard/"
        
        # Create a unique slug to avoid conflicts
        import time
        timestamp = int(time.time())
        slug = f"{title.lower().replace(' ', '-').replace('-', '_')[:20]}_{timestamp}"
        
        payload = {
            "dashboard_title": title,
            "slug": slug,
            "position_json": json.dumps(self._generate_layout(chart_ids))
        }
        
        try:
            response = await self.client.post(dashboard_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Dashboard created successfully: {title} (ID: {result.get('id')})")
            return result
        except Exception as e:
            print(f"❌ Dashboard creation failed: {e}")
            # Try with a simpler payload
            simple_payload = {
                "dashboard_title": title,
                "slug": slug
            }
            response = await self.client.post(dashboard_url, headers=headers, json=simple_payload)
            response.raise_for_status()
            result = response.json()
            print(f"✅ Dashboard created with simple payload: {title} (ID: {result.get('id')})")
            return result

    def _generate_layout(self, chart_ids):
        # Simple layout: stack charts vertically
        layout = {}
        for i, chart_id in enumerate(chart_ids):
            layout[str(chart_id)] = {
                "type": "CHART",
                "id": chart_id,
                "children": [],
                "meta": {"chartId": chart_id},
                "parents": [],
                "position": {"row": i, "col": 0}
            }
        return layout

# --- LLM Service for Prompt-to-SQL ---
import os
import requests
from django.conf import settings

class LLMService:
    def __init__(self):
        self.gemini_api_key = getattr(settings, 'GEMINI_API_KEY', None)
        self.deepseek_api_key = getattr(settings, 'DEEPSEEK_API_KEY', None)

    def prompt_to_sql(self, prompt, llm):
        if llm == 'gemini' or llm == 'gemini-pro':
            return self._gemini_prompt_to_sql(prompt, model="gemini-1.5-flash")
        elif llm == 'gemini-2.0-flash':
            return self._gemini_prompt_to_sql(prompt, model="gemini-1.5-flash")
        elif llm == 'deepseek':
            return self._deepseek_prompt_to_sql(prompt)
        else:
            raise ValueError('Unsupported LLM selected')

    def _gemini_prompt_to_sql(self, prompt, model="gemini-pro"):
        # Use the correct Gemini endpoint and pass API key as query param
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key=" + self.gemini_api_key
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": f"Convert this prompt to SQL: {prompt}"}]}]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        sql = response.json()['candidates'][0]['content']['parts'][0]['text']
        return sql

    def _deepseek_prompt_to_sql(self, prompt):
        # Example DeepSeek API call (replace with actual endpoint if needed)
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.deepseek_api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-coder",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that converts prompts to SQL."},
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        # Parse the response to extract SQL (adjust as per actual API response)
        sql = response.json()['choices'][0]['message']['content']
        return sql
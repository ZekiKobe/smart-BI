# superset_integration/chart_services.py
import httpx
from django.conf import settings
from typing import List, Dict, Optional

class SupersetChartService:
    def __init__(self):
        self.base_url = settings.SUPERSET_BASE_URL
        self.username = settings.SUPERSET_USERNAME
        self.password = settings.SUPERSET_PASSWORD
        self.client = httpx.AsyncClient()
        self.access_token = None
    
    async def authenticate(self):
        """Authenticate with Superset and get access token"""
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
    
    async def fetch_all_charts(self, page: int = 1, page_size: int = 100) -> List[Dict]:
        """
        Fetch all charts from Superset with pagination
        Args:
            page: Page number to fetch (1-based)
            page_size: Number of items per page
        Returns:
            List of chart dictionaries
        """
        if not self.access_token:
            await self.authenticate()
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/api/v1/chart/?q=(page:{page},page_size:{page_size})"
        
        try:
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get("result", [])
        except httpx.HTTPStatusError as e:
            print(f"Error fetching charts: {e}")
            return []
    
    async def fetch_chart_by_id(self, chart_id: int) -> Optional[Dict]:
        """
        Fetch a specific chart by ID
        Args:
            chart_id: The ID of the chart to fetch
        Returns:
            Chart dictionary or None if not found
        """
        if not self.access_token:
            await self.authenticate()
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/api/v1/chart/{chart_id}"
        
        try:
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get("result")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"Chart {chart_id} not found")
            else:
                print(f"Error fetching chart {chart_id}: {e}")
            return None
    
    async def fetch_charts_by_dashboard(self, dashboard_id: int) -> List[Dict]:
        """
        Fetch all charts belonging to a specific dashboard
        Args:
            dashboard_id: The ID of the dashboard
        Returns:
            List of chart dictionaries
        """
        if not self.access_token:
            await self.authenticate()
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # First get the dashboard to find its chart IDs
        dashboard_url = f"{self.base_url}/api/v1/dashboard/{dashboard_id}"
        
        try:
            # Get dashboard details
            response = await self.client.get(dashboard_url, headers=headers)
            response.raise_for_status()
            dashboard = response.json().get("result", {})
            
            # Extract chart IDs from position_json
            position_json = json.loads(dashboard.get("position_json", "{}"))
            chart_ids = set()
            
            for component in position_json.values():
                if component.get("type") == "CHART":
                    chart_id = component.get("meta", {}).get("chartId")
                    if chart_id:
                        chart_ids.add(chart_id)
            
            # Fetch details for each chart
            charts = []
            for chart_id in chart_ids:
                chart = await self.fetch_chart_by_id(chart_id)
                if chart:
                    charts.append(chart)
            
            return charts
            
        except Exception as e:
            print(f"Error fetching dashboard charts: {e}")
            return []
    
    async def search_charts(self, search_term: str, page: int = 1, page_size: int = 20) -> List[Dict]:
        """
        Search charts by title or other attributes
        Args:
            search_term: Term to search for in chart titles
            page: Page number (1-based)
            page_size: Items per page
        Returns:
            List of matching charts
        """
        if not self.access_token:
            await self.authenticate()
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        filters = [{
            "col": "slice_name",
            "opr": "ct",
            "value": search_term
        }]
        
        url = f"{self.base_url}/api/v1/chart/?q=(filters:{filters},page:{page},page_size:{page_size})"
        
        try:
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get("result", [])
        except Exception as e:
            print(f"Error searching charts: {e}")
            return []
    
    async def fetch_chart_data(self, chart_id: int, form_data: Optional[Dict] = None) -> Dict:
        """
        Fetch the data for a specific chart
        Args:
            chart_id: The chart ID
            form_data: Optional form data to override chart parameters
        Returns:
            Dictionary containing chart data
        """
        if not self.access_token:
            await self.authenticate()
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # First get the chart to get its default form data
        chart = await self.fetch_chart_by_id(chart_id)
        if not chart:
            raise ValueError(f"Chart {chart_id} not found")
        
        # Use provided form_data or chart's default params
        request_data = form_data or json.loads(chart.get("params", "{}"))
        
        url = f"{self.base_url}/api/v1/chart/{chart_id}/data"
        
        try:
            response = await self.client.post(url, headers=headers, json=request_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching chart data: {e}")
            raise
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()

# Example usage:
async def example_usage():
    service = SupersetChartService()
    try:
        # Fetch all charts (paginated)
        charts = await service.fetch_all_charts(page=1, page_size=50)
        print(f"Found {len(charts)} charts")
        
        # Search for specific charts
        sales_charts = await service.search_charts("sales")
        print(f"Found {len(sales_charts)} sales charts")
        
        # Get charts for a dashboard
        dashboard_charts = await service.fetch_charts_by_dashboard(1)
        print(f"Dashboard has {len(dashboard_charts)} charts")
        
        # Get chart data
        if charts:
            chart_data = await service.fetch_chart_data(charts[0]['id'])
            print(f"Chart data: {chart_data}")
            
    finally:
        await service.close()
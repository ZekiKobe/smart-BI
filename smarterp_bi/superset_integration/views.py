from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import SupersetService, LLMService
import asyncio

# Create your views here.

class DashboardListView(APIView):
    def get(self, request):
        service = SupersetService()
        # Superset's dashboard list endpoint is /api/v1/dashboard/
        async def fetch_dashboards():
            if not service.access_token:
                await service.authenticate()
            headers = {"Authorization": f"Bearer {service.access_token}"}
            import httpx
            # Set a high page_size to get all dashboards
            url = f"{service.base_url}/api/v1/dashboard/?page_size=1000"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
        dashboards = asyncio.run(fetch_dashboards())
        return Response(dashboards)

class DashboardDetailView(APIView):
    def get(self, request, dashboard_id):
        service = SupersetService()
        async def fetch_dashboard():
            if not service.access_token:
                await service.authenticate()
            headers = {"Authorization": f"Bearer {service.access_token}"}
            import httpx
            url = f"{service.base_url}/api/v1/dashboard/{dashboard_id}/"
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
        dashboard = asyncio.run(fetch_dashboard())
        return Response(dashboard)

class GenerateDashboardView(APIView):
    def post(self, request):
        prompt = request.data.get('prompt')
        user_id = request.data.get('user_id', 1)
        model = request.data.get('model', 'gemini')
        
        print(f"Prompt: {prompt}, User ID: {user_id}, Model: {model}")
        
        if not prompt:
            print("Missing prompt")
            return Response({'error': 'Prompt is required.'}, status=400)
        
        # Import the correct LLM service
        from llm_integration.services import LLMService
        
        async def generate_dashboard():
            try:
                # Initialize LLM service with provider
                llm_service = await LLMService.create(model)
                
                # Get schema context for Odoo data
                schema_context = """
                PostgreSQL Database Schema with Odoo tables:
                
                -- Sales and Orders
                sale_order (id, name, partner_id, date_order, amount_total, state)
                sale_order_line (id, order_id, product_id, name, product_uom_qty, price_unit, price_subtotal)
                
                -- Products
                product_template (id, name, list_price, standard_price, type, categ_id)
                product_category (id, name, parent_id)
                
                -- Customers/Partners
                res_partner (id, name, email, phone, customer_rank, supplier_rank, is_company)
                
                -- Invoices
                account_move (id, name, partner_id, invoice_date, amount_total, state, move_type)
                account_move_line (id, move_id, account_id, debit, credit, name, product_id)
                
                -- Inventory
                stock_move (id, product_id, product_uom_qty, location_id, location_dest_id, state)
                stock_picking (id, name, partner_id, scheduled_date, state, picking_type_id)
                
                -- Users and Employees
                res_users (id, login, name, email, active)
                hr_employee (id, name, work_email, department_id, job_id)
                
                -- Relationships:
                -- sale_order.partner_id -> res_partner.id
                -- sale_order_line.order_id -> sale_order.id
                -- sale_order_line.product_id -> product_template.id
                -- product_template.categ_id -> product_category.id
                -- account_move.partner_id -> res_partner.id
                -- account_move_line.move_id -> account_move.id
                -- account_move_line.product_id -> product_template.id
                """
                
                # Generate dashboard spec with charts
                chart_specs = await llm_service.generate_dashboard_spec(prompt, schema_context)
                print(f"Generated {len(chart_specs)} chart specs")
                
                # Create dashboard in Superset
                superset_service = SupersetService()
                dashboard = await superset_service.create_dashboard(
                    title=f"Dashboard: {prompt[:50]}",
                    chart_specs=chart_specs,
                    database_id=3  # PostgreSQL database
                )
                
                return dashboard
                
            except Exception as e:
                print(f"Dashboard generation error: {e}")
                raise e
        
        try:
            dashboard = asyncio.run(generate_dashboard())
            print("Dashboard created successfully:", dashboard)
            
            dashboard_id = dashboard.get('id')
            dashboard_url = f"http://localhost:8088/superset/dashboard/{dashboard_id}/" if dashboard_id else None
            
            return Response({
                'dashboard_id': dashboard_id,
                'dashboard_url': dashboard_url,
                'message': 'Dashboard created successfully.'
            })
            
        except Exception as e:
            print(f"Error in dashboard generation: {e}")
            return Response({
                'error': f'Dashboard generation failed: {str(e)}'
            }, status=500)

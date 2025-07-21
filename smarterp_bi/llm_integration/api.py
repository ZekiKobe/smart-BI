# llm_integration/api.py
from ninja import NinjaAPI, Schema
from django.http import HttpRequest
from .services import LLMService, get_schema_context
from .models import QueryHistory
import time

api = NinjaAPI()

class GenerateSQLRequest(Schema):
    prompt: str
    user_id: int
    model: str = None

class SQLResponse(Schema):
    sql: str
    execution_time_ms: int
    llm_provider: str

@api.post("/generate-sql", response=SQLResponse)
async def generate_sql(request: HttpRequest, payload: GenerateSQLRequest):
    try:
        # Get schema context
        schema_context = get_schema_context()
        
        start_time = time.time()
        llm_service = await LLMService.create(payload.model) if payload.model else await LLMService.create()
        generated_sql = await llm_service.generate_sql(payload.prompt, schema_context)
        execution_time = int((time.time() - start_time) * 1000)
        
        # Save history
        await QueryHistory.objects.acreate(
            user_id=payload.user_id,
            natural_language_query=payload.prompt,
            generated_sql=generated_sql,
            llm_provider=llm_service.provider,
            execution_time_ms=execution_time
        )
        
        return {
            'sql': generated_sql,
            'execution_time_ms': execution_time,
            'llm_provider': llm_service.provider.name
        }
    
    except Exception as e:
        return api.create_response(
            request,
            {'error': str(e)},
            status=500
        )

class GenerateDashboardRequest(Schema):
    prompt: str
    user_id: int
    model: str = None

class DashboardResponse(Schema):
    dashboard_url: str
    dashboard_id: int
    message: str

@api.post("/generate_dashboard", response=DashboardResponse)
async def generate_dashboard(request: HttpRequest, payload: GenerateDashboardRequest):
    try:
        schema_context = get_schema_context()
        llm_service = await LLMService.create(payload.model) if payload.model else await LLMService.create()
        # Generate dashboard chart specs (list of dicts)
        chart_specs = await llm_service.generate_dashboard_spec(payload.prompt, schema_context)
        from superset_integration.services import SupersetService
        superset_service = SupersetService()
        # Use the prompt as the dashboard title, or a default
        dashboard_title = payload.prompt[:50] if payload.prompt else "AI Dashboard"
        dashboard_result = await superset_service.create_dashboard(
            dashboard_title, chart_specs
        )
        # Try to construct the dashboard URL if not present
        dashboard_id = dashboard_result.get("id", 0)
        dashboard_url = dashboard_result.get("url") or f"{superset_service.base_url}/superset/dashboard/{dashboard_id}/"
        return {
            "dashboard_url": dashboard_url,
            "dashboard_id": dashboard_id,
            "message": "Dashboard created successfully."
        }
    except Exception as e:
        return api.create_response(
            request,
            {"error": str(e)},
            status=500
        )

class ExplainDataRequest(Schema):
    question: str
    data: dict = None
    model: str = None

class ExplainDataResponse(Schema):
    answer: str
    insights: list = None

@api.post("/explain-data", response=ExplainDataResponse)
async def explain_data(request: HttpRequest, payload: ExplainDataRequest):
    try:
        llm_service = await LLMService.create(payload.model) if payload.model else await LLMService.create()
        # Use a mock implementation for now
        result = await llm_service.explain_data(payload.data, payload.question)
        return result
    except Exception as e:
        return api.create_response(
            request,
            {"error": str(e)},
            status=500
        )
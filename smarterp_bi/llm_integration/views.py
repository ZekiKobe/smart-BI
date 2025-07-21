# llm_integration/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .services import LLMService, get_schema_context  # Add import here
import time
import json
from .models import QueryHistory

@csrf_exempt
@require_http_methods(["POST"])
def generate_sql(request):
    try:
        data = json.loads(request.body)
        prompt = data.get("prompt")
        user_id = data.get("user_id")
        model = data.get("model", "gemini")
        
        if not prompt:
            return JsonResponse({"error": "Prompt is required"}, status=400)
        
        # Now get_schema_context is defined
        schema_context = get_schema_context()
        
        start_time = time.time()
        
        # Use asyncio to run async functions
        import asyncio
        async def generate():
            llm_service = await LLMService.create(model)
            return await llm_service.generate_sql(prompt, schema_context)
        
        generated_sql = asyncio.run(generate())
        execution_time = int((time.time() - start_time) * 1000)
        
        # Create query history (synchronous)
        QueryHistory.objects.create(
            user_id=user_id,
            natural_language_query=prompt,
            generated_sql=generated_sql,
            llm_provider=llm_service.provider,
            execution_time_ms=execution_time
        )
        
        return JsonResponse({
            "sql": generated_sql,
            "execution_time_ms": execution_time
        })
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
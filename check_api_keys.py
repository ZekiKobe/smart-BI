#!/usr/bin/env python
import os
import sys
import django

# Add the smarterp_bi directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'smarterp_bi'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarterp_bi.settings')
django.setup()

from llm_integration.models import LLMProvider
from django.conf import settings

def check_api_keys():
    print("Checking API keys...")
    
    # Check settings
    print(f"Settings GEMINI_API_KEY: {getattr(settings, 'GEMINI_API_KEY', 'Not set')}")
    print(f"Settings DEEPSEEK_API_KEY: {getattr(settings, 'DEEPSEEK_API_KEY', 'Not set')}")
    
    # Check database
    try:
        providers = LLMProvider.objects.all()
        print(f"\nFound {providers.count()} LLM providers in database:")
        for provider in providers:
            print(f"- {provider.name}: {provider.base_url}")
            print(f"  API Key: {provider.api_key[:20]}..." if provider.api_key else "  No API key")
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == '__main__':
    check_api_keys() 
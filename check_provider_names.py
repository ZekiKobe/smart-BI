#!/usr/bin/env python
import os
import sys

# Add the smarterp_bi directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'smarterp_bi'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarterp_bi.settings')
import django
django.setup()

from llm_integration.models import LLMProvider

def check_provider_names():
    providers = LLMProvider.objects.all()
    print("Provider names in database:")
    for provider in providers:
        print(f'  - "{provider.name}" (Active: {provider.is_active})')
        print(f'    Base URL: {provider.base_url}')
        print(f'    API Key: {provider.api_key[:10]}...')

if __name__ == "__main__":
    check_provider_names() 
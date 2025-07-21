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

def check_provider_status():
    print("Checking LLM provider status...")
    
    try:
        providers = LLMProvider.objects.all()
        print(f"\nFound {providers.count()} LLM providers:")
        for provider in providers:
            print(f"- {provider.name}: active={provider.is_active}, base_url={provider.base_url}")
            
        # Check for active providers
        active_providers = LLMProvider.objects.filter(is_active=True)
        print(f"\nActive providers: {active_providers.count()}")
        for provider in active_providers:
            print(f"- {provider.name}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_provider_status() 
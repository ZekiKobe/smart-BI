#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smarterp_bi.settings')
django.setup()

from llm_integration.models import LLMProvider

def setup_llm_providers():
    # Create Gemini provider
    gemini_provider, created = LLMProvider.objects.get_or_create(
        name='Gemini',
        defaults={
            'base_url': 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro',
            'api_key': 'AIzaSyC75ct3TNPpdaVC3oo41QEUSfxFUW2OTFs',
            'is_active': True
        }
    )
    if created:
        print(f"Created Gemini provider: {gemini_provider}")
    else:
        print(f"Gemini provider already exists: {gemini_provider}")

    # Create DeepSeek provider
    deepseek_provider, created = LLMProvider.objects.get_or_create(
        name='DeepSeek',
        defaults={
            'base_url': 'https://api.deepseek.com/v1/chat/completions',
            'api_key': 'sk-1592c0f6e07940f3a56e49c676f2a132',
            'is_active': True
        }
    )
    if created:
        print(f"Created DeepSeek provider: {deepseek_provider}")
    else:
        print(f"DeepSeek provider already exists: {deepseek_provider}")

    print("LLM providers setup complete!")

if __name__ == '__main__':
    setup_llm_providers() 
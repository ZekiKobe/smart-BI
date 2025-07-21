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

def fix_api_key():
    try:
        gemini_provider = LLMProvider.objects.get(name='Gemini')
        # Update to use the correct API key from settings
        gemini_provider.api_key = settings.GEMINI_API_KEY
        gemini_provider.save()
        print(f"Updated Gemini API key to: {gemini_provider.api_key[:20]}...")
    except LLMProvider.DoesNotExist:
        print("Gemini provider not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fix_api_key() 
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

def fix_gemini_url():
    try:
        gemini_provider = LLMProvider.objects.get(name='Gemini')
        # Fix the base URL to use the correct Gemini endpoint
        gemini_provider.base_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro'
        gemini_provider.save()
        print(f"Fixed Gemini URL: {gemini_provider.base_url}")
    except LLMProvider.DoesNotExist:
        print("Gemini provider not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fix_gemini_url() 
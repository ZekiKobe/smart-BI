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

def fix_gemini_model():
    try:
        gemini_provider = LLMProvider.objects.get(name='Gemini')
        # Update to use the working model
        gemini_provider.base_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash'
        gemini_provider.save()
        print(f"Updated Gemini model to: {gemini_provider.base_url}")
    except LLMProvider.DoesNotExist:
        print("Gemini provider not found")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fix_gemini_model() 
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

def update_gemini_key():
    try:
        # Get the new API key from user input
        new_key = input("Enter your new Gemini API key: ").strip()
        
        if not new_key:
            print("❌ No API key provided")
            return
        
        # Update the Gemini provider
        provider = LLMProvider.objects.filter(name__iexact='gemini').first()
        if provider:
            old_key = provider.api_key[:10] + "..."
            provider.api_key = new_key
            provider.save()
            print(f"✅ Gemini API key updated successfully!")
            print(f"   Old key: {old_key}")
            print(f"   New key: {new_key[:10]}...")
        else:
            print("❌ Gemini provider not found in database")
            
    except Exception as e:
        print(f"❌ Error updating API key: {e}")

if __name__ == "__main__":
    print("Updating Gemini API key...")
    update_gemini_key() 
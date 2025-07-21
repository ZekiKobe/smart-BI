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
    # EDIT THIS LINE WITH YOUR NEW API KEY
    new_key = "YOUR_NEW_GEMINI_API_KEY_HERE"  # Replace this with your actual API key
    
    if new_key == "YOUR_NEW_GEMINI_API_KEY_HERE":
        print("❌ Please edit this file and replace 'YOUR_NEW_GEMINI_API_KEY_HERE' with your actual API key")
        return
    
    try:
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